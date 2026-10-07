"""Telegram bot: ana menü, dropshipping dalları ve dallara ait akışlar.

Callback verisi şeması:
  menu, help, cancel
  br:<dal>                dal ana sayfası
  rm:<dal>                dal yol haritası
  st:<aşama id>           aşama görünümü (ör. st:c.sirket)
  tg:<görev id>           görevi işaretle / kaldır
  next:<dal>              sıradaki adım
  done:<görev id>         görevi tamamla ve sıradakine geç
  ps:<dal>                ürün analizini başlat
  pa:<kriter>:<puan>      ürün analizi cevabı
  fm:<dal>:<araç>         form aracını başlat (kâr hesabı, reklam testi...)
"""

import html
import logging
import os
import warnings

from telegram import InlineKeyboardButton as Btn
from telegram import InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.warnings import PTBUserWarning

from .branches import ALL_TASK_IDS, BRANCHES, branch_of_task
from .core import roadmap, scoring
from .core.branch import Branch, Field
from .formatting import parse_number
from .storage import Storage

# Konuşmalarda hem buton hem metin cevabı kullanıyoruz; per_message uyarısı bu kullanım için geçerli değil.
warnings.filterwarnings("ignore", category=PTBUserWarning, message=".*per_message.*")

log = logging.getLogger(__name__)

PS_NAME, PS_ASK, FORM_ASK = range(3)


def _storage(context: ContextTypes.DEFAULT_TYPE) -> Storage:
    return context.application.bot_data["storage"]


def _arg(update: Update, index: int = 1) -> str:
    return update.callback_query.data.split(":")[index]


async def _reply(update: Update, text: str, markup: InlineKeyboardMarkup | None = None) -> None:
    """Butondan geldiyse mesajı düzenler, komuttan/metinden geldiyse yeni mesaj gönderir."""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)
    else:
        await update.effective_chat.send_message(text, reply_markup=markup, parse_mode=ParseMode.HTML)


def _nav(branch: Branch | None = None) -> list[Btn]:
    row = [Btn("🏠 Ana Menü", callback_data="menu")]
    if branch:
        row.insert(0, Btn(f"⬅️ {branch.title}", callback_data=f"br:{branch.id}"))
    return row


# ---------- Genel ----------

WELCOME = (
    "👋 <b>Dropshipping Asistanına hoş geldin!</b>\n\n"
    "Stoksuz e-ticaretin her modelinde, şirket kurulumundan ürün seçimine, reklamdan ölçeklemeye "
    "kadar seni adım adım yönlendiririm. Bir dal seç:\n\n"
    "🅰️ <b>Yurt İçi:</b> Türk tedarikçi (XML bayilik) → Trendyol, Hepsiburada, kendi site\n"
    "🅱️ <b>E-İhracat:</b> Türk ürünleri → Etsy, Amazon, Shopify ile yurt dışına\n"
    "🅲 <b>Global:</b> Shopify + CJ/AliExpress tedarikçileri → ABD, UK, AB müşterileri"
)

HELP = (
    "<b>Komutlar</b>\n"
    "/start veya /menu: Ana menü\n"
    "/a, /b, /c: İlgili dropshipping dalına git\n"
    "/iptal: Devam eden analizi/hesabı iptal et\n"
    "/sifirla: Tüm yol haritası ilerlemeni sıfırla\n\n"
    "Her dalda: 🗺 Yol Haritası, 📍 Sıradaki Adım, 🔍 Ürün Analizi ve dala özel hesaplama araçları var."
)


def main_menu() -> InlineKeyboardMarkup:
    rows = [[Btn(b.title + ("" if b.ready else " 🚧"), callback_data=f"br:{b.id}")] for b in BRANCHES.values()]
    rows.append([Btn("ℹ️ Yardım", callback_data="help")])
    return InlineKeyboardMarkup(rows)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _reply(update, WELCOME, main_menu())


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _reply(update, HELP, InlineKeyboardMarkup([_nav()]))


async def reset_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _storage(context).reset(update.effective_user.id)
    await _reply(update, "🔄 Yol haritası ilerlemen sıfırlandı.", main_menu())


async def stale_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer("Bu işlem sona ermiş, menüden yeniden başlat.", show_alert=True)


# ---------- Dal ana sayfası ----------

def _branch_home(branch: Branch) -> InlineKeyboardMarkup:
    if not branch.ready:
        return InlineKeyboardMarkup([_nav()])
    rows = [
        [Btn("🗺 Yol Haritası", callback_data=f"rm:{branch.id}"), Btn("📍 Sıradaki Adım", callback_data=f"next:{branch.id}")],
        [Btn("🔍 Ürün Analizi", callback_data=f"ps:{branch.id}")],
    ]
    tool_buttons = [Btn(t.button, callback_data=f"fm:{branch.id}:{t.id}") for t in branch.tools]
    rows += [tool_buttons[i : i + 2] for i in range(0, len(tool_buttons), 2)]
    rows.append(_nav())
    return InlineKeyboardMarkup(rows)


async def show_branch(update: Update, context: ContextTypes.DEFAULT_TYPE, branch_id: str | None = None) -> None:
    branch = BRANCHES[branch_id or _arg(update)]
    await _reply(update, branch.summary, _branch_home(branch))


def _branch_command(branch_id: str):
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await show_branch(update, context, branch_id)

    return handler


# ---------- Yol haritası ----------

async def show_roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    branch = BRANCHES[_arg(update)]
    done = _storage(context).done_tasks(update.effective_user.id)
    ids = roadmap.task_ids(branch.stages)
    rows = []
    for s in branch.stages:
        d, n = roadmap.stage_progress(s, done)
        mark = "✅" if d == n else f"{d}/{n}"
        rows.append([Btn(f"{s.title}  ({mark})", callback_data=f"st:{s.id}")])
    rows.append(_nav(branch))
    text = (
        f"🗺 <b>{branch.title}: Yol Haritası</b>\n\n"
        f"İlerleme: {roadmap.progress_bar(sum(t in done for t in ids), len(ids))}\n\n"
        "Bir aşama seç:"
    )
    await _reply(update, text, InlineKeyboardMarkup(rows))


def _stage_view(branch: Branch, stage: roadmap.Stage, done: set[str]) -> tuple[str, InlineKeyboardMarkup]:
    d, n = roadmap.stage_progress(stage, done)
    text = (
        f"<b>{stage.title}</b>\n{roadmap.progress_bar(d, n)}\n\n"
        f"💡 {stage.guide}\n\n"
        "Tamamladığın adımlara dokunarak işaretle:"
    )
    rows = [
        [Btn(("✅ " if t.id in done else "⬜ ") + t.text, callback_data=f"tg:{t.id}")]
        for t in stage.tasks
    ]
    rows.append([Btn("⬅️ Yol Haritası", callback_data=f"rm:{branch.id}"), Btn("🏠 Ana Menü", callback_data="menu")])
    return text, InlineKeyboardMarkup(rows)


async def _render_stage(update: Update, context: ContextTypes.DEFAULT_TYPE, stage_id: str) -> None:
    branch = BRANCHES[stage_id.split(".", 1)[0]]
    stage = roadmap.find_stage(branch.stages, stage_id)
    text, markup = _stage_view(branch, stage, _storage(context).done_tasks(update.effective_user.id))
    await _reply(update, text, markup)


async def show_stage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _render_stage(update, context, _arg(update))


async def toggle_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task_id = _arg(update)
    if task_id not in ALL_TASK_IDS:
        await update.callback_query.answer("Bu adım artık yok.")
        return
    _storage(context).toggle_task(update.effective_user.id, task_id)
    await _render_stage(update, context, task_id.rsplit(".", 1)[0])


async def _render_next(update: Update, context: ContextTypes.DEFAULT_TYPE, branch: Branch) -> None:
    nxt = roadmap.next_task(branch.stages, _storage(context).done_tasks(update.effective_user.id))
    if nxt is None:
        text = f"🎉 {branch.title} yol haritasını tamamladın! Ölçekleme adımlarını haftalık tekrarla."
        await _reply(update, text, InlineKeyboardMarkup([_nav(branch)]))
        return
    stage, task = nxt
    text = f"📍 <b>Sıradaki adımın</b>\n\n<b>{stage.title}</b>\n👉 {task.text}\n\n💡 {stage.guide}"
    markup = InlineKeyboardMarkup(
        [
            [Btn("✅ Bunu tamamladım", callback_data=f"done:{task.id}")],
            [Btn("📂 Aşamaya git", callback_data=f"st:{stage.id}")],
            _nav(branch),
        ]
    )
    await _reply(update, text, markup)


async def show_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _render_next(update, context, BRANCHES[_arg(update)])


async def complete_and_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task_id = _arg(update)
    if task_id not in ALL_TASK_IDS:
        await update.callback_query.answer("Bu adım artık yok.")
        return
    storage = _storage(context)
    if task_id not in storage.done_tasks(update.effective_user.id):
        storage.toggle_task(update.effective_user.id, task_id)
    await _render_next(update, context, branch_of_task(task_id))


# ---------- Ürün analizi ----------

def _criterion_prompt(branch: Branch, index: int) -> tuple[str, InlineKeyboardMarkup]:
    c = branch.criteria[index]
    text = f"<b>Soru {index + 1}/{len(branch.criteria)}</b>\n\n{c.question}"
    rows = [[Btn(label, callback_data=f"pa:{c.key}:{score}")] for label, score in c.options]
    rows.append([Btn("✖️ İptal", callback_data="cancel")])
    return text, InlineKeyboardMarkup(rows)


async def ps_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    branch = BRANCHES[_arg(update)]
    context.user_data["ps"] = {"branch": branch.id, "answers": {}, "index": 0}
    await _reply(
        update,
        f"🔍 <b>Ürün Analizi</b> ({branch.title})\n\nAnaliz etmek istediğin ürünün adını yaz:",
    )
    return PS_NAME


async def ps_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    state = context.user_data["ps"]
    state["name"] = update.message.text.strip()[:100]
    text, markup = _criterion_prompt(BRANCHES[state["branch"]], 0)
    await update.message.reply_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)
    return PS_ASK


async def ps_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    state = context.user_data.get("ps")
    if state is None:
        await stale_button(update, context)
        return ConversationHandler.END
    branch = BRANCHES[state["branch"]]
    key, score = _arg(update, 1), int(_arg(update, 2))
    criterion = branch.criteria[state["index"]]
    if key != criterion.key or score not in {s for _, s in criterion.options}:
        await update.callback_query.answer("Lütfen son mesajdaki soruyu cevapla.")
        return PS_ASK

    state["answers"][key] = score
    state["index"] += 1
    if state["index"] < len(branch.criteria):
        text, markup = _criterion_prompt(branch, state["index"])
        await _reply(update, text, markup)
        return PS_ASK

    result = scoring.evaluate(branch.criteria, state["answers"])
    lines = [
        f"🔍 <b>{html.escape(state['name'])}</b> analiz sonucu\n",
        f"Skor: <b>{result.score}/100</b>",
        f"Karar: <b>{result.verdict}</b>",
    ]
    if result.red_flags:
        lines.append("\n🚩 <b>Kritik sorunlar</b>")
        lines += [f"• {t}" for t in result.red_flags]
    if result.weaknesses:
        lines.append("\n🔧 <b>Geliştirilecek noktalar</b>")
        lines += [f"• {t}" for t in result.weaknesses]
    rows = [[Btn("🔍 Başka ürün", callback_data=f"ps:{branch.id}")]]
    if branch.tools:
        first = branch.tools[0]
        lines.append(f"\n👉 Sonraki adım: {first.button} ile gerçek kârını kontrol et.")
        rows[0].append(Btn(first.button, callback_data=f"fm:{branch.id}:{first.id}"))
    rows.append(_nav(branch))
    context.user_data.pop("ps", None)
    await _reply(update, "\n".join(lines), InlineKeyboardMarkup(rows))
    return ConversationHandler.END


# ---------- Form araçları (kâr hesabı, reklam testi...) ----------

def _field_prompt(title: str, fields: tuple[Field, ...], index: int) -> str:
    f = fields[index]
    hint = "" if f.default is None else "\n<i>(Boş geçmek için - yaz)</i>"
    return f"<b>{title}</b> ({index + 1}/{len(fields)})\n\n{f.question}{hint}"


def _validate(f: Field, raw: str) -> float:
    """Kullanıcı girdisini alanın kurallarına göre sayıya çevirir; geçersizse ValueError mesajıyla."""
    if raw == "-" and f.default is not None:
        return f.default
    try:
        value = parse_number(raw)
    except ValueError:
        raise ValueError("⚠️ Geçerli bir sayı yaz (ör. 24,90).") from None
    if f.kind == "positive" and value <= 0:
        raise ValueError("⚠️ Bu değer 0'dan büyük olmalı.")
    if f.kind == "pct" and value >= 100:
        raise ValueError("⚠️ Yüzde değeri 100'den küçük olmalı.")
    return value


async def form_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    branch = BRANCHES[_arg(update, 1)]
    tool = branch.tool(_arg(update, 2))
    context.user_data["form"] = {"branch": branch.id, "tool": tool.id, "values": {}, "index": 0}
    await _reply(update, _field_prompt(tool.title, tool.fields, 0) + "\n\nİstediğin zaman /iptal yazabilirsin.")
    return FORM_ASK


async def form_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    state = context.user_data["form"]
    branch = BRANCHES[state["branch"]]
    tool = branch.tool(state["tool"])
    f = tool.fields[state["index"]]
    try:
        value = _validate(f, update.message.text.strip())
    except ValueError as e:
        await update.message.reply_text(str(e))
        return FORM_ASK

    state["values"][f.name] = value
    state["index"] += 1
    if state["index"] < len(tool.fields):
        await update.message.reply_text(
            _field_prompt(tool.title, tool.fields, state["index"]), parse_mode=ParseMode.HTML
        )
        return FORM_ASK

    context.user_data.pop("form", None)
    markup = InlineKeyboardMarkup(
        [[Btn("🔁 Yeniden hesapla", callback_data=f"fm:{branch.id}:{tool.id}")], _nav(branch)]
    )
    await update.message.reply_text(tool.report(state["values"]), reply_markup=markup, parse_mode=ParseMode.HTML)
    return ConversationHandler.END


# ---------- Konuşma ortak ----------

def _clear(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop("ps", None)
    context.user_data.pop("form", None)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _clear(context)
    await _reply(update, "✖️ İptal edildi.", main_menu())
    return ConversationHandler.END


async def to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _clear(context)
    await start(update, context)
    return ConversationHandler.END


async def to_branch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _clear(context)
    await show_branch(update, context)
    return ConversationHandler.END


def build_application(token: str, db_path: str) -> Application:
    app = Application.builder().token(token).build()
    app.bot_data["storage"] = Storage(db_path)

    fallbacks = [
        CommandHandler("iptal", cancel),
        CallbackQueryHandler(cancel, pattern="^cancel$"),
        CallbackQueryHandler(to_menu, pattern="^menu$"),
        CallbackQueryHandler(to_branch, pattern=r"^br:\w+$"),
        CommandHandler(["start", "menu"], to_menu),
    ]
    app.add_handler(
        ConversationHandler(
            entry_points=[CallbackQueryHandler(ps_start, pattern=r"^ps:\w+$")],
            states={
                PS_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ps_name)],
                PS_ASK: [CallbackQueryHandler(ps_answer, pattern=r"^pa:\w+:\d$")],
            },
            fallbacks=fallbacks,
            allow_reentry=True,
        )
    )
    app.add_handler(
        ConversationHandler(
            entry_points=[CallbackQueryHandler(form_start, pattern=r"^fm:\w+:\w+$")],
            states={FORM_ASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_answer)]},
            fallbacks=fallbacks,
            allow_reentry=True,
        )
    )

    app.add_handler(CommandHandler(["start", "menu"], start))
    app.add_handler(CommandHandler("yardim", show_help))
    app.add_handler(CommandHandler("sifirla", reset_progress))
    for branch_id in BRANCHES:
        app.add_handler(CommandHandler(branch_id, _branch_command(branch_id)))
    app.add_handler(CallbackQueryHandler(start, pattern="^menu$"))
    app.add_handler(CallbackQueryHandler(show_help, pattern="^help$"))
    app.add_handler(CallbackQueryHandler(show_branch, pattern=r"^br:\w+$"))
    app.add_handler(CallbackQueryHandler(show_roadmap, pattern=r"^rm:\w+$"))
    app.add_handler(CallbackQueryHandler(show_stage, pattern=r"^st:[\w.]+$"))
    app.add_handler(CallbackQueryHandler(toggle_task, pattern=r"^tg:[\w.]+$"))
    app.add_handler(CallbackQueryHandler(show_next, pattern=r"^next:\w+$"))
    app.add_handler(CallbackQueryHandler(complete_and_next, pattern=r"^done:[\w.]+$"))
    app.add_handler(CallbackQueryHandler(stale_button))
    return app


def main() -> None:
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN ortam değişkeni tanımlı değil. README'deki kuruluma bak.")
    app = build_application(token, os.environ.get("ETICARET_DB", "eticaret_bot.db"))
    log.info("Bot başlatıldı")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

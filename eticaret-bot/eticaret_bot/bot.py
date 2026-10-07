"""Telegram bot: menüler, yol haritası, ürün analizi ve kâr hesaplayıcı akışları."""

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

from .formatting import fmt_pct, fmt_tl, parse_number
from .modules import product_score, profit_calc, roadmap
from .storage import Storage

# Konuşmalarda hem buton hem metin cevabı kullanıyoruz; per_message uyarısı bu kullanım için geçerli değil.
warnings.filterwarnings("ignore", category=PTBUserWarning, message=".*per_message.*")

log = logging.getLogger(__name__)

PS_NAME, PS_ASK, PC_ASK = range(3)

PROFIT_FIELDS: tuple[tuple[str, str, float | None], ...] = (
    # (alan, soru, boş geçilirse varsayılan; None = zorunlu)
    ("sale_price", "🏷 Satış fiyatı (KDV dahil, TL)?", None),
    ("unit_cost", "📦 Ürünün birim alış maliyeti (KDV dahil, TL)?", None),
    ("commission_pct", "🏪 Pazaryeri komisyonu (%)? Kendi siten ise ödeme komisyonunu yaz (ör. 3).", None),
    ("shipping", "🚚 Sipariş başı kargo ücreti (KDV dahil, TL)?", None),
    ("ad_cost", "📣 Satış başı reklam harcaması (TL)? Bilmiyorsan 0 yaz.", 0.0),
    ("packaging", "🎁 Paketleme maliyeti (TL)? Yoksa 0 yaz.", 0.0),
    ("return_rate_pct", "↩️ Tahmini iade oranı (%)? Bilmiyorsan 5 yaz.", 5.0),
    ("vat_pct", "🧾 KDV oranı (%)? Çoğu ürün için 20.", 20.0),
)


def _storage(context: ContextTypes.DEFAULT_TYPE) -> Storage:
    return context.application.bot_data["storage"]


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [Btn("🗺 Yol Haritası", callback_data="rm"), Btn("📍 Sıradaki Adım", callback_data="next")],
            [Btn("🔍 Ürün Analizi", callback_data="ps"), Btn("💰 Kâr Hesapla", callback_data="pc")],
            [Btn("ℹ️ Yardım", callback_data="help")],
        ]
    )


def back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[Btn("🏠 Ana Menü", callback_data="menu")]])


async def _reply(update: Update, text: str, markup: InlineKeyboardMarkup | None = None, edit: bool = True):
    """Butondan geldiyse mesajı düzenler, komuttan/metinden geldiyse yeni mesaj gönderir."""
    query = update.callback_query
    if query:
        await query.answer()
        if edit:
            await query.edit_message_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)
            return
    await update.effective_chat.send_message(text, reply_markup=markup, parse_mode=ParseMode.HTML)


# ---------- Genel ----------

WELCOME = (
    "👋 <b>E-Ticaret Asistanına hoş geldin!</b>\n\n"
    "Sıfırdan mağaza kurmaktan ürün seçimine, yasal süreçten reklama kadar her adımda seni yönlendiririm.\n\n"
    "🗺 <b>Yol Haritası:</b> Tüm süreç adım adım, ilerlemeni kaydederim\n"
    "📍 <b>Sıradaki Adım:</b> Şu an ne yapman gerektiğini söylerim\n"
    "🔍 <b>Ürün Analizi:</b> Ürün adayını kriterlere göre puanlarım\n"
    "💰 <b>Kâr Hesapla:</b> Gerçek net kârını, başa baş ROAS'ı ve önerilen fiyatı hesaplarım"
)

HELP = (
    "<b>Komutlar</b>\n"
    "/start veya /menu: Ana menü\n"
    "/yolharitasi: Yol haritası\n"
    "/siradaki: Sıradaki adım\n"
    "/urun: Ürün analizi\n"
    "/kar: Kâr hesaplayıcı\n"
    "/iptal: Devam eden analizi/hesabı iptal et\n"
    "/sifirla: Yol haritası ilerlemeni sıfırla"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _reply(update, WELCOME, main_menu())


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _reply(update, HELP, back_to_menu())


async def reset_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _storage(context).reset(update.effective_user.id)
    await _reply(update, "🔄 Yol haritası ilerlemen sıfırlandı.", main_menu())


async def stale_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer("Bu işlem sona ermiş, menüden yeniden başlat.", show_alert=True)


# ---------- Yol haritası ----------

async def show_roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    done = _storage(context).done_tasks(update.effective_user.id)
    total_done = sum(t in done for t in roadmap.ALL_TASK_IDS)
    rows = []
    for s in roadmap.STAGES:
        d, n = roadmap.stage_progress(s, done)
        mark = "✅" if d == n else f"{d}/{n}"
        rows.append([Btn(f"{s.title}  ({mark})", callback_data=f"st:{s.id}")])
    rows.append([Btn("🏠 Ana Menü", callback_data="menu")])
    text = (
        "🗺 <b>E-Ticaret Yol Haritası</b>\n\n"
        f"Genel ilerleme: {roadmap.progress_bar(total_done, len(roadmap.ALL_TASK_IDS))}\n\n"
        "Bir aşama seç:"
    )
    await _reply(update, text, InlineKeyboardMarkup(rows))


def _stage_view(stage: roadmap.Stage, done: set[str]) -> tuple[str, InlineKeyboardMarkup]:
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
    rows.append([Btn("⬅️ Yol Haritası", callback_data="rm"), Btn("🏠 Ana Menü", callback_data="menu")])
    return text, InlineKeyboardMarkup(rows)


async def show_stage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    stage = roadmap.get_stage(update.callback_query.data.split(":", 1)[1])
    text, markup = _stage_view(stage, _storage(context).done_tasks(update.effective_user.id))
    await _reply(update, text, markup)


async def toggle_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task_id = update.callback_query.data.split(":", 1)[1]
    if task_id not in roadmap.ALL_TASK_IDS:
        await update.callback_query.answer("Bu adım artık yok.")
        return
    storage = _storage(context)
    storage.toggle_task(update.effective_user.id, task_id)
    stage = roadmap.get_stage(task_id.split(".", 1)[0])
    text, markup = _stage_view(stage, storage.done_tasks(update.effective_user.id))
    await _reply(update, text, markup)


async def show_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    nxt = roadmap.next_task(_storage(context).done_tasks(update.effective_user.id))
    if nxt is None:
        text = "🎉 Tüm yol haritasını tamamladın! Şimdi Analiz ve Büyüme döngüsünü haftalık tekrarla."
        await _reply(update, text, back_to_menu())
        return
    stage, task = nxt
    text = f"📍 <b>Sıradaki adımın</b>\n\n<b>{stage.title}</b>\n👉 {task.text}\n\n💡 {stage.guide}"
    markup = InlineKeyboardMarkup(
        [
            [Btn("✅ Bunu tamamladım", callback_data=f"done:{task.id}")],
            [Btn("📂 Aşamaya git", callback_data=f"st:{stage.id}"), Btn("🏠 Ana Menü", callback_data="menu")],
        ]
    )
    await _reply(update, text, markup)


async def complete_and_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task_id = update.callback_query.data.split(":", 1)[1]
    storage = _storage(context)
    if task_id in roadmap.ALL_TASK_IDS and task_id not in storage.done_tasks(update.effective_user.id):
        storage.toggle_task(update.effective_user.id, task_id)
    await show_next(update, context)


# ---------- Ürün analizi ----------

def _criterion_prompt(index: int) -> tuple[str, InlineKeyboardMarkup]:
    c = product_score.CRITERIA[index]
    text = f"<b>Soru {index + 1}/{len(product_score.CRITERIA)}</b>\n\n{c.question}"
    rows = [[Btn(label, callback_data=f"ps:{c.key}:{score}")] for label, score in c.options]
    rows.append([Btn("✖️ İptal", callback_data="cancel")])
    return text, InlineKeyboardMarkup(rows)


async def ps_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["ps"] = {"answers": {}, "index": 0}
    await _reply(
        update,
        "🔍 <b>Ürün Analizi</b>\n\nAnaliz etmek istediğin ürünün adını yaz:\n(ör. <i>Bambu kesme tahtası seti</i>)",
    )
    return PS_NAME


async def ps_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["ps"]["name"] = update.message.text.strip()[:100]
    text, markup = _criterion_prompt(0)
    await update.message.reply_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)
    return PS_ASK


async def ps_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    state = context.user_data.get("ps")
    _, key, score = update.callback_query.data.split(":")
    if state is None:
        await stale_button(update, context)
        return ConversationHandler.END
    if key != product_score.CRITERIA[state["index"]].key:
        await update.callback_query.answer("Lütfen son mesajdaki soruyu cevapla.")
        return PS_ASK

    state["answers"][key] = int(score)
    state["index"] += 1
    if state["index"] < len(product_score.CRITERIA):
        text, markup = _criterion_prompt(state["index"])
        await _reply(update, text, markup)
        return PS_ASK

    result = product_score.evaluate(state["answers"])
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
    lines.append("\n👉 Sonraki adım: 💰 Kâr Hesapla ile gerçek kârını kontrol et.")
    markup = InlineKeyboardMarkup(
        [
            [Btn("🔍 Başka ürün", callback_data="ps"), Btn("💰 Kâr Hesapla", callback_data="pc")],
            [Btn("🏠 Ana Menü", callback_data="menu")],
        ]
    )
    context.user_data.pop("ps", None)
    await _reply(update, "\n".join(lines), markup)
    return ConversationHandler.END


# ---------- Kâr hesaplayıcı ----------

def _profit_prompt(index: int) -> str:
    _, question, default = PROFIT_FIELDS[index]
    hint = "" if default is None else "\n<i>(Boş geçmek için - yaz)</i>"
    return f"💰 <b>Kâr Hesapla</b> ({index + 1}/{len(PROFIT_FIELDS)})\n\n{question}{hint}"


async def pc_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["pc"] = {"values": {}, "index": 0}
    await _reply(update, _profit_prompt(0) + "\n\nİstediğin zaman /iptal yazabilirsin.")
    return PC_ASK


async def pc_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    state = context.user_data["pc"]
    name, _, default = PROFIT_FIELDS[state["index"]]
    raw = update.message.text.strip()
    try:
        if raw == "-" and default is not None:
            value = default
        else:
            value = parse_number(raw)
    except ValueError:
        await update.message.reply_text("⚠️ Geçerli bir sayı yaz (ör. 249,90).")
        return PC_ASK
    if name == "sale_price" and value <= 0:
        await update.message.reply_text("⚠️ Satış fiyatı 0'dan büyük olmalı.")
        return PC_ASK
    if name in ("commission_pct", "return_rate_pct") and value >= 100:
        await update.message.reply_text("⚠️ Yüzde değeri 100'den küçük olmalı.")
        return PC_ASK

    state["values"][name] = value
    state["index"] += 1
    if state["index"] < len(PROFIT_FIELDS):
        await update.message.reply_text(_profit_prompt(state["index"]), parse_mode=ParseMode.HTML)
        return PC_ASK

    inp = profit_calc.ProfitInput(**state["values"])
    context.user_data.pop("pc", None)
    await update.message.reply_text(
        _profit_report(inp), reply_markup=_profit_markup(), parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END


def _profit_report(inp: profit_calc.ProfitInput) -> str:
    r = profit_calc.calculate(inp)
    status = "✅ Kârlı" if r.net_profit > 0 else "❌ Zarar ediyorsun"
    lines = [
        "💰 <b>Birim Kâr Analizi</b>\n",
        f"Satış fiyatı: {fmt_tl(inp.sale_price)}",
        f"KDV hariç ciro: {fmt_tl(r.net_revenue)}",
        f"Toplam maliyet (KDV hariç): {fmt_tl(r.total_cost)}",
        f"Ödenecek tahmini KDV: {fmt_tl(r.vat_payable)}",
        "",
        f"<b>Net kâr: {fmt_tl(r.net_profit)}</b> ({status})",
        f"Net marj: {fmt_pct(r.margin_pct)}",
        f"Ürün maliyetine göre getiri (ROI): {fmt_pct(r.roi_pct)}",
    ]
    if r.breakeven_roas is not None:
        lines.append(
            f"Başa baş ROAS: <b>{r.breakeven_roas:.2f}</b>".replace(".", ",")
            + "\n<i>(Reklama harcadığın her 1 TL bundan az ciro getiriyorsa zarar edersin)</i>"
        )
    else:
        lines.append("Başa baş ROAS: reklamsız bile zarar var, önce maliyet/fiyatı düzelt.")

    lines.append("\n🎯 <b>Hedef marja göre önerilen satış fiyatı</b>")
    for target in (15, 25, 35):
        price = profit_calc.suggest_price(inp, target)
        lines.append(f"• %{target} marj: " + (fmt_tl(price) if price else "komisyon çok yüksek, ulaşılamaz"))

    if r.margin_pct < 15:
        lines.append(
            "\n⚠️ Marj %15'in altında. İade, kampanya ve beklenmedik masraflar kârını silebilir."
        )
    lines.append("\n<i>Not: Gelir/kurumlar vergisi dahil değildir. Basitleştirilmiş hesaptır.</i>")
    return "\n".join(lines)


def _profit_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [Btn("🔁 Yeni hesap", callback_data="pc"), Btn("🔍 Ürün Analizi", callback_data="ps")],
            [Btn("🏠 Ana Menü", callback_data="menu")],
        ]
    )


# ---------- Konuşma ortak ----------

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("ps", None)
    context.user_data.pop("pc", None)
    await _reply(update, "✖️ İptal edildi.", main_menu())
    return ConversationHandler.END


async def to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("ps", None)
    context.user_data.pop("pc", None)
    await start(update, context)
    return ConversationHandler.END


def build_application(token: str, db_path: str) -> Application:
    app = Application.builder().token(token).build()
    app.bot_data["storage"] = Storage(db_path)

    fallbacks = [
        CommandHandler("iptal", cancel),
        CallbackQueryHandler(cancel, pattern="^cancel$"),
        CallbackQueryHandler(to_menu, pattern="^menu$"),
        CommandHandler(["start", "menu"], to_menu),
    ]
    app.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("urun", ps_start), CallbackQueryHandler(ps_start, pattern="^ps$")],
            states={
                PS_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ps_name)],
                PS_ASK: [CallbackQueryHandler(ps_answer, pattern=r"^ps:\w+:\d$")],
            },
            fallbacks=fallbacks,
            allow_reentry=True,
        )
    )
    app.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("kar", pc_start), CallbackQueryHandler(pc_start, pattern="^pc$")],
            states={PC_ASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, pc_answer)]},
            fallbacks=fallbacks,
            allow_reentry=True,
        )
    )

    app.add_handler(CommandHandler(["start", "menu"], start))
    app.add_handler(CommandHandler("yardim", show_help))
    app.add_handler(CommandHandler("yolharitasi", show_roadmap))
    app.add_handler(CommandHandler("siradaki", show_next))
    app.add_handler(CommandHandler("sifirla", reset_progress))
    app.add_handler(CallbackQueryHandler(start, pattern="^menu$"))
    app.add_handler(CallbackQueryHandler(show_help, pattern="^help$"))
    app.add_handler(CallbackQueryHandler(show_roadmap, pattern="^rm$"))
    app.add_handler(CallbackQueryHandler(show_stage, pattern=r"^st:\w+$"))
    app.add_handler(CallbackQueryHandler(toggle_task, pattern=r"^tg:[\w.]+$"))
    app.add_handler(CallbackQueryHandler(show_next, pattern="^next$"))
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

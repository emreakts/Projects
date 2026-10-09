"""Botun profil fotoğrafını assets/avatar.mp4 animasyonuyla değiştirir.

Kullanım (eticaret-bot klasöründe): .venv/bin/python -m eticaret_bot.set_avatar
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from telegram import Bot

from .bot import load_env_file

ASSETS = Path(__file__).resolve().parent.parent / "assets"


async def _upload(token: str, video: Path, main_frame: float) -> None:
    from telegram import InputProfilePhotoAnimated

    async with Bot(token) as bot:
        with video.open("rb") as f:
            await bot.set_my_profile_photo(InputProfilePhotoAnimated(animation=f, main_frame_timestamp=main_frame))


def main() -> None:
    load_env_file()
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN tanımlı değil. Önce botu baslat.command ile bir kez çalıştır.")
    video = ASSETS / "avatar.mp4"
    if not video.exists():
        raise SystemExit(f"{video} bulunamadı.")
    if not hasattr(Bot, "set_my_profile_photo"):
        raise SystemExit(
            "Yüklü Telegram kütüphanesi bu özelliği desteklemiyor (22.7+ gerekir).\n"
            f"Elle yükle: @BotFather → /setuserpic → botunu seç → {video} dosyasını video olarak gönder."
        )
    frame_file = ASSETS / "avatar_main_frame.txt"
    main_frame = float(frame_file.read_text()) if frame_file.exists() else 0.0
    asyncio.run(_upload(token, video, main_frame))
    print("✅ Profil animasyonu yüklendi. Telegram'da botun profiline bak (birkaç saniye sürebilir).")


if __name__ == "__main__":
    main()

#!/bin/bash
# macOS / Linux: çift tıkla (macOS) veya terminalde ./baslat.command çalıştır.
cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
    echo "[HATA] Python 3 bulunamadı. https://www.python.org/downloads/ adresinden kur ve tekrar çalıştır."
    read -r -p "Kapatmak için Enter'a bas..."
    exit 1
fi

if [ ! -x .venv/bin/python ]; then
    echo "İlk kurulum yapılıyor, lütfen bekle..."
    python3 -m venv .venv || { echo "[HATA] Sanal ortam oluşturulamadı."; read -r; exit 1; }
fi
.venv/bin/python -m pip install --disable-pip-version-check -q -r requirements.txt \
    || { echo "[HATA] Kütüphaneler kurulamadı. İnternet bağlantını kontrol et."; read -r; exit 1; }

if [ ! -f .env ]; then
    read -r -p "BotFather'dan aldığın token'ı yapıştır ve Enter'a bas: " TOKEN
    if [ -z "$TOKEN" ]; then
        echo "[HATA] Token boş olamaz."
        read -r; exit 1
    fi
    echo "TELEGRAM_BOT_TOKEN=$TOKEN" > .env
    echo "Token .env dosyasına kaydedildi."
fi

echo
echo "Bot çalışıyor. Telegram'da botuna /start yaz. Durdurmak için Ctrl+C."
.venv/bin/python -m eticaret_bot
echo
echo "Bot durdu. Token hatalıysa .env dosyasını silip bu dosyayı tekrar çalıştır."
read -r -p "Kapatmak için Enter'a bas..."

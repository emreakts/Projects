@echo off
chcp 65001 >nul
title Dropshipping Botu
cd /d "%~dp0"

rem --- Python var mi? ---
set PY=
py -3 --version >nul 2>nul && set PY=py -3
if not defined PY python --version >nul 2>nul && set PY=python
if not defined PY (
    echo.
    echo [HATA] Python bulunamadi.
    echo  1. https://www.python.org/downloads/ adresinden Python'u indir.
    echo  2. Kurulumun ilk ekraninda "Add python.exe to PATH" kutusunu MUTLAKA isaretle.
    echo  3. Kurulum bitince bu dosyaya tekrar cift tikla.
    echo.
    pause
    exit /b 1
)

rem --- Sanal ortam ve kutuphaneler (ilk calistirmada birkac dakika surebilir) ---
if not exist ".venv\Scripts\python.exe" (
    echo Ilk kurulum yapiliyor, lutfen bekle...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo [HATA] Sanal ortam olusturulamadi.
        pause
        exit /b 1
    )
)
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -q -r requirements.txt
if errorlevel 1 (
    echo [HATA] Kutuphaneler kurulamadi. Internet baglantini kontrol et.
    pause
    exit /b 1
)

rem --- Token ---
if exist ".env" goto calistir
echo.
echo BotFather'dan aldigin token'i yapistir (sag tik = yapistir) ve Enter'a bas:
set /p TOKEN=Token: 
if "%TOKEN%"=="" (
    echo [HATA] Token bos olamaz. Dosyaya tekrar cift tikla.
    pause
    exit /b 1
)
> ".env" echo TELEGRAM_BOT_TOKEN=%TOKEN%
echo Token .env dosyasina kaydedildi.

:calistir
echo.
echo Bot calisiyor. Telegram'da botuna /start yaz.
echo Bu pencere acik kaldigi surece bot calisir. Kapatmak icin pencereyi kapat.
echo.
".venv\Scripts\python.exe" -m eticaret_bot
echo.
echo Bot durdu. Yukaridaki mesaji oku. Token hataliysa .env dosyasini silip bu dosyayi tekrar calistir.
pause

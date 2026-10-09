FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY eticaret_bot ./eticaret_bot

# İlerleme veritabanı kalıcı volume'da tutulur
ENV ETICARET_DB=/data/eticaret_bot.db
VOLUME /data

CMD ["python", "-m", "eticaret_bot"]

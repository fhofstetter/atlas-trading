FROM python:3.12-slim

RUN addgroup --system trading && adduser --system --ingroup trading trading

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY server.py ./

ENV PORT=3458 \
    DATA_DIR=/data \
    PYTHONUNBUFFERED=1

USER trading

EXPOSE 3458

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:3458/api/health')"

CMD ["python", "server.py"]

FROM python:3.13

WORKDIR /app

COPY . /app

ENV RESULT_MAX_LENGTH=20 \
  DICTIONARIES_DIR=/app/dictionaries \
  HOST=0.0.0.0 \
  PORT=8080 \
  LOG_LEVEL=INFO

EXPOSE ${PORT}

CMD ["python", "server.py"]


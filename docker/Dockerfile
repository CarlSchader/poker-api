FROM python:alpine

WORKDIR /usr/src/app
COPY requirements.txt src/ ./

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV PORT=8080

EXPOSE 8080
ENTRYPOINT ["python3", "api.py"]
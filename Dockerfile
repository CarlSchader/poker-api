FROM python:alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./

ENV RANK_TABLE_PATH=ranks.json
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
EXPOSE 8080

RUN python3 generate.py ranks

ENTRYPOINT ["python", "api.py"]
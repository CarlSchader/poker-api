FROM python as build
WORKDIR /usr/src/app
COPY src/generate_rank_table.py src/cards.py src/validation.py src/compare.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 generate_rank_table.py ranks.json

FROM python:alpine as final
WORKDIR /usr/src/app
COPY requirements.txt src/ ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=build /usr/src/app/ranks.json ./
ENV RANK_TABLE_PATH=ranks.json
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
EXPOSE 80
ENTRYPOINT ["python3", "api.py"]
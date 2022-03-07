import os, sys, redis

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']

client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset='utf-8', decode_responses=True)

sys.argv[1]

f = open(sys.argv[1], 'r')

for line in f:
    split_line = line.split(':')
    if len(split_line) == 2:
        index = split_line[0].strip().replace('"', '')
        value = int(split_line[1].strip().replace(',', ''))
        client.set(index, value)
import os
from flask import Flask, request
import redis
from simulator import simulate_hand
from tables import load_table
from cards import value_map

SUITS = {'d': 'd', 'h': 'h', 's': 's', 'c': 'c'}
RANK_TABLE_PATH = os.environ['RANK_TABLE_PATH']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']

redic_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset='utf-8', decode_responses=True)
app = Flask(__name__)

print('loading rank table')
if RANK_TABLE_PATH == None:
    print('RANK_TABLE_PATH environment variable not set')
    exit(1)
else:
    rank_table = load_table(RANK_TABLE_PATH)

def convertHandParam(handParam, sep='-'):
    return tuple([(value_map[card[:-1].upper()], SUITS.get(card[-1].lower(), 'h')) for card in handParam.split(sep)])

def serializeHand(hand, count):
    sorted_hand = [str(card[0]) + card[1] for card in hand]
    sorted_hand.sort()
    return str(count) + ':' + '-'.join(sorted_hand)

@app.route('/')
def simulate():
    hand = request.args.get('hand')
    count = request.args.get('count')

    if hand:
        hand = convertHandParam(hand)
    else:
        hand = ((1, 's'), (1, 'c'), (1, 'h'))
    if count == None:
        count = 7
    else:
        count = int(count)
    
    serialized_hand = serializeHand(hand, count)

    response = redic_client.hgetall(serialized_hand)
    if not response:
        response = simulate_hand(hand, count, rank_table)
        redic_client.hset(serialized_hand, mapping=response)

    response['hand'] = serialized_hand
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
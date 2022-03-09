import os, signal, redis, math
from flask import Flask, request, Response
from waitress import serve
from simulator import createRanks, simulate_hand_redis
from cards import hand_tostring, value_map

signal.signal(signal.SIGTERM, lambda _ : exit(0))

SUITS = {'d': 'd', 'h': 'h', 's': 's', 'c': 'c'}
PORT = os.environ['PORT']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']

TOTAL_HANDS = math.comb(52, 5)

client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset='utf-8', decode_responses=True)

app = Flask(__name__)

def convertHandParam(handParam, sep='-'):
    return tuple([(value_map[card[:-1].upper()], SUITS.get(card[-1].lower(), 'h')) for card in handParam.split(sep)])

@app.route('/')
def simulate():
    print('Request to /', request.args)
    dbsize = client.dbsize()
    if dbsize < TOTAL_HANDS:
        print({'populating redis': '{} of {}'.format(dbsize, TOTAL_HANDS)})
        return {'populating redis': '{} of {}'.format(dbsize, TOTAL_HANDS)}

    hand = request.args.get('hand')
    count = request.args.get('count')
    shared = request.args.get('shared')

    if hand:
        hand = convertHandParam(hand)
    else:
        hand = ((1, 's'), (1, 'c'), (1, 'h'))
    if count == None:
        count = 7
    else:
        count = int(count)
    if shared:
        shared = convertHandParam(shared)
    else:
        shared = tuple()

    results = {}
    results['probabilities'] = simulate_hand_redis(hand + shared, count, client)
    
    if len(shared) > 0:
        ranks = createRanks(shared, len(shared) + len(hand), count, client)
        rank = int(ranks[frozenset(hand + shared)])
        results['pocket_ranking'] = {'rank': rank, 'total': len(ranks), 'percentile': 100 * (rank / len(ranks))}
        results['pocket_ranking']['note'] = 'This ranking takes into account the cards on the table'

    results['pocket'] = hand_tostring(hand)
    results['table'] = hand_tostring(shared)

    print('response body:', results)
    return results

@app.route('/health')
def health_check():
    print("health check")
    return Response(status=200)

if __name__ == '__main__':

    print('Serving on port: {}'.format(PORT))
    serve(app, host='0.0.0.0', port=PORT)
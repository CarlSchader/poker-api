import os, signal
from flask import Flask, request
from simulator import createRanks, simulate_hand_redis
from tables import load_table
from cards import hand_tostring, value_map

signal.signal(signal.SIGTERM, lambda _ : exit(0))

SUITS = {'d': 'd', 'h': 'h', 's': 's', 'c': 'c'}
PORT = os.environ['PORT']
RANK_TABLE_PATH = os.environ['RANK_TABLE_PATH']

app = Flask(__name__)

print('loading rank table')
if RANK_TABLE_PATH == None:
    print('RANK_TABLE_PATH environment variable not set')
    exit(1)
else:
    rank_table = load_table(RANK_TABLE_PATH)
    print(len(rank_table), 'entries')

def convertHandParam(handParam, sep='-'):
    return tuple([(value_map[card[:-1].upper()], SUITS.get(card[-1].lower(), 'h')) for card in handParam.split(sep)])

@app.route('/')
def simulate():
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
    results['probabilities'] = simulate_hand_redis(hand + shared, count, rank_table)
    
    if len(shared) > 0:
        ranks = createRanks(shared, len(shared) + len(hand), count, rank_table)
        rank = int(ranks[frozenset(hand + shared)])
        results['pocket_ranking'] = {'rank': rank, 'total': len(ranks), 'percentile': 100 * (rank / len(ranks))}
        results['pocket_ranking']['note'] = 'This ranking takes into account the cards on the table'

    results['pocket'] = hand_tostring(hand)
    results['table'] = hand_tostring(shared)



    return results

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
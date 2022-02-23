#!/usr/bin/python3
#cython: language_level=3

import math, functools
from cards import hand_tostring, make_deck, combinations, hand_names, serializeHand, value_map
from ranks import best_hand_functions
from compare import validators
from tables import load_array_as_dict, load_table
from redis_client import client as redis
from utils import dict_cmp

def simulate_hand(hand, end_hand_size, rank_table, exclude=set()):
    hand_size = len(hand)
    deck = make_deck(set(tuple(hand) + tuple(exclude)))
    count = 0
    total_rank = 0
    outcomes = {name: 0 for name in hand_names}
    
    total_possible_hands = 1
    if end_hand_size - hand_size > 0:
        total_possible_hands = math.comb(52 - hand_size, end_hand_size - hand_size)

    for comb in combinations(deck, end_hand_size - hand_size):
        count += 1
        for i in range(len(validators)):
            if validators[i](hand + comb):
                outcomes[hand_names[i]] += 1
                total_rank += rank_table[frozenset(best_hand_functions[i](hand + comb))]
                break

    hand_data = {'expected_rank': total_rank / total_possible_hands}
    for outcome in outcomes:
        hand_data[outcome] = outcomes[outcome] / total_possible_hands
    return hand_data

def simulate_hand_redis(hand, end_hand_size, rank_table, exclude=set()):
    serializedHand = serializeHand(hand, end_hand_size)
    results = redis.hgetall(serializedHand)
    
    if not results:
        results = simulate_hand(hand, end_hand_size, rank_table, exclude=set())
        redis.hset(serializedHand, mapping=results)
    
    return results

def createRanks(hand, current_hand_size, end_hand_size, rank_table, exclude=set()):
    deck = make_deck(set(tuple(hand) + tuple(exclude)))
    rank_array = []
    for comb in combinations(deck, current_hand_size - len(hand)):
        result = simulate_hand_redis(tuple(hand + comb), end_hand_size, rank_table)
        result['hand'] = frozenset(tuple(hand + comb))
        rank_array.append(result)
    
    rank_array.sort(key=functools.cmp_to_key(lambda x, y : dict_cmp(x, y, 'expected_rank')))
    rank_table = {}

    for i in range(len(rank_array)):
        result = rank_array[i]
        rank_table[result['hand']] = i
    
    return rank_table

if __name__ == '__main__':
    import sys
    
    print('loading rank table')
    rank_table = load_table("ranks.json")
    print('loading pairs table')
    holdem_pairs_table = load_array_as_dict("holdem-pairs-sorted.json")
    print('loading flops table')
    holdem_flops_table = load_array_as_dict("holdem-flops-sorted.json")
    # print('loading turns table')
    # holdem_turns_table = load_array_as_dict("holdem-turns-sorted.json")

    argsize = len(sys.argv)
    end_hand_size = 7
    hand = tuple()
    exclude = set()
    input_string = ""
    stats = {}

    while True:
        # input_string = input('end hand size: ')
        # if input_string == 'quit':
        #     break
        # else:
        #     end_hand_size = int(input_string)

        input_string = input('hand: ')
        if input_string == 'quit':
            break
        else:
            hand = tuple([(value_map[card[:-1].upper()], card[-1].lower()) for card in input_string.split(' ')])

        input_string = input('exclusion: ')
        if input_string == 'quit':
            break
        else:
            if len(input_string) == 0:
                exclude = set()
            else:
                exclude = set([(value_map[card[:-1]], card[-1]) for card in input_string.split(' ')])
        
        print()
        print('calculating')
        print(hand_tostring(hand))
        total = 0
        if end_hand_size == 7 and len(hand) == 2:
            stats = holdem_pairs_table[frozenset(hand)]
            total = len(holdem_pairs_table)
            print(stats)
            print('rank: {}, of {} percent: {}'.format(stats['rank'], total, int(100 * (stats['rank'] / total))))
        elif end_hand_size == 7 and len(hand) == 5:
            stats = holdem_flops_table[frozenset(hand)]
            total = len(holdem_flops_table)
            print(stats)
            print('rank: {}, of {} percent: {}'.format(stats['rank'], total, int(100 * (stats['rank'] / total))))
        else:
            print(simulate_hand(hand, end_hand_size, rank_table, exclude))
        print()
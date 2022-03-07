#!/usr/bin/python3
#cython: language_level=3

import math, functools
from cards import make_deck, combinations, hand_names, serializeHand
from ranks import best_hand_functions
from compare import validators
from utils import dict_cmp

def get_rank(hand, client=None):
    if client:
        rank = client.get(serializeHand(hand))
        if rank:
            return int(rank)
    return 0

def simulate_hand(hand, end_hand_size, exclude=set(), client=None):
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
                total_rank += get_rank(best_hand_functions[i](hand + comb), client)
                break

    hand_data = {'expected_rank': total_rank / total_possible_hands}
    for outcome in outcomes:
        hand_data[outcome] = outcomes[outcome] / total_possible_hands
    return hand_data

def simulate_hand_redis(hand, end_hand_size, client, exclude=set()):
    serializedHand = serializeHand(hand, end_hand_size)
    results = client.hgetall(serializedHand)
    
    if not results:
        results = simulate_hand(hand, end_hand_size, exclude, client)
        client.hset(serializedHand, mapping=results)
    
    return results

def createRanks(hand, current_hand_size, end_hand_size, exclude=set()):
    deck = make_deck(set(tuple(hand) + tuple(exclude)))
    rank_array = []
    for comb in combinations(deck, current_hand_size - len(hand)):
        result = simulate_hand_redis(tuple(hand + comb), end_hand_size)
        result['hand'] = frozenset(tuple(hand + comb))
        rank_array.append(result)
    
    rank_array.sort(key=functools.cmp_to_key(lambda x, y : dict_cmp(x, y, 'expected_rank')))
    ranked_table = {}

    for i in range(len(rank_array)):
        result = rank_array[i]
        ranked_table[result['hand']] = i
    
    return ranked_table
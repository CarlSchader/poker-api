#!/usr/bin/python3

import json
from operator import itemgetter

from importlib_metadata import functools
from card import string_tohand, suits, values
from compare import flush_cmp, number_of_a_kind_cmp, ranked_cmp_functions

def load_rank_table(path):
    f = open(path, 'r')
    rank_table_unset = json.load(f)
    f.close()
    rank_table = {}

    for hand_string in rank_table_unset:
        rank_table[frozenset(string_tohand(hand_string))] = rank_table_unset[hand_string]

    return rank_table

def best_hand_high_card(input_hand):
    hand = list(input_hand)
    for i in range(len(hand)):
        if hand[i][0] == 1:
            hand[i] = (len(values) + 1, hand[i][1])
    hand.sort(key=itemgetter(0), reverse=True)
    for i in range(len(hand)):
        if hand[i][0] == len(values) + 1:
            hand[i] = (1, hand[i][1])

    return tuple(hand[:min(len(hand), 5)])

def best_hand_number_of_a_kind(hand, number):
    counts = {}
    extras = []
    output_hand = []
    
    for card in hand:
        if card[0] in counts:
            counts[card[0]].append(card)
        else:
            counts[card[0]] = [card]

    for val in counts:
        if len(counts[val]) == number:
            for card in counts[val]:
                output_hand.append(card)
        else:
            for card in counts[val]:
                extras.append(card)
    
    output_hand = best_hand_high_card(output_hand)
    final_hand = []
    i = 0
    space_left = 5
    while space_left >= number and len(output_hand) >= i + number:
        final_hand += output_hand[i:i + number]
        i += number
        space_left -= number

    return tuple(final_hand) + best_hand_high_card(extras)[:space_left]

def best_hand_straight(hand):
    length = len(values)
    counts = [[] for _ in range(length + 1)]

    for card in hand:
        counts[card[0] - 1].append(card)
        if card[0] == 1:
            counts[len(counts) - 1].append(card)
            
    counts.reverse()

    consecutive = []
    for i in range(length + 1):
        cards = counts[i % length]
        if len(cards) > 0:
            consecutive.append(cards[0])
            if len(consecutive) == 5:
                return tuple(consecutive)
        else:
            consecutive = []
    
    return None
    
def best_hand_flush(hand):
    flush_dict = {suit: set() for suit in suits}
    flushes = []

    for card in hand:
        flush_dict[card[1]].add(card)
        
    for suit in flush_dict:
        if len(flush_dict[suit]) >= 5:
            flushes.append(best_hand_high_card(tuple(flush_dict[suit])))

    flushes.sort(key=functools.cmp_to_key(flush_cmp))

    return tuple(flushes[-1])

def best_hand_full_house(hand):
    counts = {}
    trips = []
    pairs = []

    for card in hand:
        if card[0] in counts:
            counts[card[0]].append(card)
        else:
            counts[card[0]] = [card]

    for suit in counts:
        if len(counts[suit]) >= 3:
            trips.append(counts[suit])
        elif len(counts[suit]) == 2:
            pairs.append(counts[suit])
    
    trips.sort(key=functools.cmp_to_key(ranked_cmp_functions[6]), reverse=True)
    rest = trips[1:] + pairs
    rest.sort(key=functools.cmp_to_key(ranked_cmp_functions[8]), reverse=True)

    return tuple(trips[0][:3]) + tuple(rest[0][:2])

best_hand_functions = (
    best_hand_straight,
    best_hand_straight,
    lambda h : best_hand_number_of_a_kind(h, 4),
    best_hand_full_house,
    best_hand_flush,
    best_hand_straight,
    lambda h : best_hand_number_of_a_kind(h, 3),
    lambda h : best_hand_number_of_a_kind(h, 2),
    lambda h : best_hand_number_of_a_kind(h, 2),
    best_hand_high_card
)
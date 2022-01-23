#!/usr/bin/python3

import math, json
from card import hand_tostring, make_deck, combinations
from validation import validators
from ranks import load_rank_table, best_hand_functions
from compare import ranked_validators

hands = [
    "royal flush",
    "straight flush",
    "four of a kind",
    "full house",
    "flush",
    "straight",
    "three of a kind",
    "two pair",
    "pair",
    "high card"
]

def prob(hand, condition, input_exclude=set()):
    exclude = set(input_exclude)
    exclude.update(hand)
    total = 0
    valid = 0

    for combination in combinations(make_deck(exclude), 7 - len(hand)):
        total += 1
        if condition(hand + combination):
            valid += 1

    return valid / total

def simulate(input_hand=set(), input_exclude=set()):
    hand = tuple(input_hand)
    exclude = set(input_exclude)
    exclude.update(hand)
    deck = make_deck(exclude)
    count = 0
    total = math.comb(len(deck), 7 - len(hand))
    total_score = math.comb(52, 5)
    rank_table = load_rank_table('ranks.json')
    total_rank = 0
    outcomes = {name: 0 for name in hands}

    for combination in combinations(deck, 7 - len(hand)):
        count += 1
        print('\t% ' + str(100 * (count / total)), end="\r")
        for i in range(len(ranked_validators)):
            if ranked_validators[i](hand + combination):
                outcomes[hands[i]] += 1
                total_rank += rank_table[frozenset(best_hand_functions[i](hand + combination))]
                break

    print('average rank', total_rank / total, 'out of', total_score)
    print('score', total_rank / (total * total_score))
    for outcome in outcomes:
        print('%', int(100 * (outcomes[outcome] / total)), outcome)
    

if __name__ == '__main__':
    simulate({(1, 's'), (1, 'h')})
#!/usr/bin/python3
#cython: language_level=3

import math
from cards import hand_tostring, make_deck, combinations, hand_names, value_map
from ranks import best_hand_functions
from compare import validators
from tables import load_array_as_dict, load_table

def simulate_hand(hand, end_hand_size, rank_table, exclude=set()):
    hand_size = len(hand)
    deck = make_deck(set(tuple(hand) + tuple(exclude)))
    count = 0
    total_rank = 0
    outcomes = {name: 0 for name in hand_names}
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
#!/usr/bin/python3
#cython: language_level=3

import math, functools
from cards import hand_tostring, hand_names, make_deck, combinations
from compare import ranked_cmp_functions
from validation import validators
from ranks import best_hand_functions
from tables import load_table, write_array, write_table
from simulator import simulate_hand

def generate_ranks(path):
    ranked_hands = [[] for _ in range(len(validators))]
    deck = make_deck()
    count = 0
    total = math.comb(len(deck), 5)
    for hand in combinations(deck, 5):
        for i in range(len(validators)):
            if validators[i](hand):
                ranked_hands[i].append(hand)
                break
        count += 1
        print('\t% ' + str(int(100 * (count / total))), end="\r")
    
    f = open(path, 'w')
    f.write('{\n')

    rank = total
    found = 0
    for i in range(len(ranked_hands)):
        ranked_hands[i].sort(key=functools.cmp_to_key(ranked_cmp_functions[i]), reverse=True)
        found += len(ranked_hands[i])
        print("\nsorted", i)
        for j in range(len(ranked_hands[i])):
            if i == len(ranked_hands) - 1 and j == len(ranked_hands[i]) - 1:
                f.write('\t"{}": {} \n'.format(hand_tostring(ranked_hands[i][j]), rank))
            else:
                f.write('\t"{}": {},\n'.format(hand_tostring(ranked_hands[i][j]), rank))
            rank -= 1

    f.write('}')
    f.close()

def holdem_thread(hand, rank_table, holdem_data, total_possible_hands):
    deck = make_deck(set(hand))
    hand_size = len(hand)
    count = 0
    total_rank = 0
    outcomes = {name: 0 for name in hand_names}

    for comb in combinations(deck, 7 - hand_size):
        print('\t% ' + str(100 * (count / total_possible_hands)), end="\r")
        count += 1
        for i in range(len(validators)):
            if validators[i](hand + comb):
                outcomes[hand_names[i]] += 1
                total_rank += rank_table[frozenset(best_hand_functions[i](hand + comb))]
                break
    
    hand_string = hand_tostring(hand)
    holdem_data[hand_string] = {'expected_rank': total_rank / total_possible_hands}
    for outcome in outcomes:
        holdem_data[hand_string][outcome] = outcomes[outcome] / total_possible_hands
    print(holdem_data[hand_string])

def generate_holdem_data(path, hand_size, batch_size):
    print('loading rank table')
    rank_table = load_table('ranks.json')

    print('loading holdem table')
    holdem_table = load_table(path)
    hand_count = 0
    hand_combs = math.comb(52, hand_size)

    print('calculating data for hands of size', hand_size)
    for hand in combinations(make_deck(), hand_size):
        hand_count += 1
        hand_set = frozenset(hand)
        if not hand_set in holdem_table: 
            print('\t', hand_count, 'of', hand_combs, 'calculating data for', hand_tostring(hand), end='\r')
            holdem_table[hand_set] = simulate_hand(hand, 7, rank_table)
            if hand_count % batch_size == 0 or hand_count == hand_combs:
                write_table(holdem_table, path)
        

def sort_dict(dictionary, cmp_func):
    arr = []
    for key in dictionary:
        arr.append((key, dictionary[key]))
    
    arr.sort(key=functools.cmp_to_key(lambda x, y : cmp_func(x[1], y[1])))
    return arr


def dict_cmp(key, x, y):
    if x[key] > y[key]:
        return 1
    elif x[key] < y[key]:
        return -1
    else:
        return 0

def generate_sorted_file(inpath, outpath, sort_key='expected_rank'):
    print('loading table')
    dictionary = load_table(inpath)
    
    print('sorting entries')
    sorted_array = sort_dict(dictionary, lambda x, y : dict_cmp(sort_key, x, y))

    print('writing array')
    write_array(sorted_array, outpath)


if __name__ == '__main__':
    import sys

    options = {
        "ranks": ((generate_ranks, "ranks.json"), ), 
        "holdem-pairs": ((generate_holdem_data, "holdem-pairs.json", 2, 1), ),
        "holdem-flops": ((generate_holdem_data, "holdem-flops.json", 5, 10000), ),
        "holdem-turns": ((generate_holdem_data, "holdem-turns.json", 6, 250000), ),
        "holdem-pairs-sort": ((generate_sorted_file, "holdem-pairs.json", "holdem-pairs-sorted.json", "expected_rank"), ),
        "holdem-flops-sort": ((generate_sorted_file, "holdem-flops.json", "holdem-flops-sorted.json", "expected_rank"), ),
        "holdem-turns-sort": ((generate_sorted_file, "holdem-turns.json", "holdem-turns-sorted.json", "expected_rank"), )
    }

    if len(sys.argv) < 2:
        print("one argument needed\noptions:")
        for opt in options:
            print('\t', opt)
    else:
        for procedure in options[sys.argv[1]]:
            procedure[0](*procedure[1:])

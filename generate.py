#!/usr/bin/python3
#cython: language_level=3

import json, math, functools, _thread
from simulator import combinations, make_deck
from card import hand_tostring, print_deck, hand_names
from compare import hand_cmp, ranked_validators, ranked_cmp_functions
from validation import validators
from ranks import load_rank_table, best_hand_functions



def generate_ranks(path):
    ranked_hands = [[] for _ in range(len(validators))]
    deck = make_deck()
    count = 0
    total = math.comb(len(deck), 5)
    for hand in combinations(deck, 5):
        for i in range(len(validators)):
            if ranked_validators[i](hand):
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
        for i in range(len(ranked_validators)):
            if ranked_validators[i](hand + comb):
                outcomes[hand_names[i]] += 1
                total_rank += rank_table[frozenset(best_hand_functions[i](hand + comb))]
                break
    
    hand_string = hand_tostring(hand)
    holdem_data[hand_string] = {'expected_rank': total_rank / total_possible_hands}
    for outcome in outcomes:
        holdem_data[hand_string][outcome] = outcomes[outcome] / total_possible_hands
    print(holdem_data[hand_string])

def generate_holdem_data(path, hand_size):
    print('loading rank table')
    rank_table = load_rank_table('ranks.json')

    holdem_data = {}
    total_possible_hands = math.comb(52 - hand_size, 7 - hand_size)

    print('calculating data for hands of size', hand_size)
    for hand in combinations(make_deck(), hand_size):
        print('calculating data for', hand_tostring(hand))
        try:
            print('new thread')
            _thread.start_new_thread(holdem_thread, (hand, rank_table, holdem_data, total_possible_hands))
        except:
            print('error creating new thread')
        # deck = make_deck(set(hand))
        # count = 0
        # total_rank = 0
        # outcomes = {name: 0 for name in hand_names}

        # for comb in combinations(deck, 7 - hand_size):
        #     print('\t% ' + str(100 * (count / total_possible_hands)), end="\r")
        #     count += 1
        #     for i in range(len(ranked_validators)):
        #         if ranked_validators[i](hand + comb):
        #             outcomes[hand_names[i]] += 1
        #             total_rank += rank_table[frozenset(best_hand_functions[i](hand + comb))]
        #             break
        
        # hand_string = hand_tostring(hand)
        # holdem_data[hand_string] = {'expected_rank': total_rank / total_possible_hands}
        # for outcome in outcomes:
        #     holdem_data[hand_string][outcome] = outcomes[outcome] / total_possible_hands
        # print(holdem_data[hand_string])
        
    
    print('writing to', path)
    f = open(path, 'w+')
    json.dump(holdem_data, f)
    f.close()

        

if __name__ == '__main__':
    import sys

    options = {
        "rank": ((generate_ranks, "ranks.json"), ), 
        "holdem-pairs": ((generate_holdem_data, "holdem-pairs.json", 2), ),
        "holdem-flops": ((generate_holdem_data, "holdem-flops.json", 5), ),
        "holdem-turns": ((generate_holdem_data, "holdem-turns.json", 6), ),
    }

    if len(sys.argv) < 2:
        print("one argument needed\noptions:")
        for opt in options:
            print('\t', opt)
    else:
        for procedure in options[sys.argv[1]]:
            procedure[0](*procedure[1:])

#!/usr/bin/python3
#cython: language_level=3

from operator import itemgetter
from card import make_deck, suits, values
from validation import validators

# comparison functions

def high_card_cmp(input_hand1, input_hand2):
    hand1 = list(input_hand1)
    for i in range(len(hand1)):
        if hand1[i][0] == 1:
            hand1[i] = (len(values) + 1,)
    hand1.sort(key=itemgetter(0), reverse=True)

    hand2 = list(input_hand2)
    for i in range(len(hand2)):
        if hand2[i][0] == 1:
            hand2[i] = (len(values) + 1,)
    hand2.sort(key=itemgetter(0), reverse=True)


    for i in range(min(len(hand1), len(hand2), 5)):
        if hand1[i][0] > hand2[i][0]:
            return 1
        elif hand1[i][0] < hand2[i][0]:
            return -1
    
    return 0

def number_of_a_kind_cmp(hand1, hand2, number):
    map1 = {}
    max1 = 0
    extras1 = []
    map2 = {}
    max2 = 0
    extras2 = []

    for card in hand1:
        if not card[0] in map1:
            map1[card[0]] = 1
        else:
            map1[card[0]] += 1

    for card in hand2:
        if not card[0] in map2:
            map2[card[0]] = 1
        else:
            map2[card[0]] += 1

    for val in map1:
        if map1[val] > number - 1 and val > max1:
            max1 = val
        else:
            extras1.append((val,))
    
    for val in map2:
        if map2[val] > number - 1 and val > max2:
            max2 = val
        else:
            extras2.append((val,))

    if max1 == 1:
        max1 = len(values) + 1
    if max2 == 1:
        max2 = len(values) + 1

    if max1 > max2:
        return 1
    elif max1 < max2:
        return -1
    else:
        return high_card_cmp(extras1, extras2)

def two_pair_cmp(hand1, hand2):
    map1 = {}
    pairs1 = []
    extras1 = []
    map2 = {}
    pairs2 = []
    extras2 = []

    for card in hand1:
        if not card[0] in map1:
            map1[card[0]] = 1
        else:
            map1[card[0]] += 1

    for card in hand2:
        if not card[0] in map2:
            map2[card[0]] = 1
        else:
            map2[card[0]] += 1

    for val in map1:
        if map1[val] > 1:
            pairs1.append((val,))
        else:
            extras1.append((val,))
    
    for val in map2:
        if map2[val] > 1:
            pairs2.append((val,))
        else:
            extras2.append((val,))

    cmp = high_card_cmp(pairs1, pairs2)
    if cmp == 1:
        return 1
    elif cmp == -1:
        return -1
    else:
        return high_card_cmp(extras1, extras2)

def straight_cmp(hand1, hand2):
    length = len(values)
    counts1 = [0 for i in range(length + 1)]
    counts2 = [0 for i in range(length + 1)]
    max1 = -1
    max2 = -1

    for card in hand1:
        if card[0] == 1:
            counts1[0] += 1
            counts1[len(counts1) - 1] += 1
        else:
            counts1[card[0] - 1] += 1
    counts1.reverse()

    for card in hand2:
        if card[0] == 1:
            counts2[0] += 1
            counts2[len(counts2) - 1] += 1
        else:
            counts2[card[0] - 1] += 1
    counts2.reverse()

    consecutive = 0
    for i in range(length + 1):
        if counts1[i % length] != 0:
            consecutive += 1
        else:
            consecutive = 0
            max1 = i
        if consecutive == 5:
            break

    consecutive = 0
    for i in range(length + 1):
        if counts2[i % length] != 0:
            consecutive += 1
        else:
            consecutive = 0
            max2 = i
        if consecutive == 5:
            break

    if max1 < max2:
        return 1
    elif max1 > max2:
        return -1
    else:
        return 0
    
def flush_cmp(hand1, hand2):
    suit_counts1 = {}
    flush_suit1 = ''
    suit_counts2 = {}
    flush_suit2 = ''
    
    for card in hand1:
        val = card[0]
        suit = card[1]
        
        if (not suit in suit_counts1):
            suit_counts1[suit] = [(val,)]
        else:
            suit_counts1[suit].append((val,))
            if len(suit_counts1[suit]) == 5:
                flush_suit1 = suit
    
    for card in hand2:
        val = card[0]
        suit = card[1]
        
        if (not suit in suit_counts2):
            suit_counts2[suit] = [(val,)]
        else:
            suit_counts2[suit].append((val,))
            if len(suit_counts2[suit]) == 5:
                flush_suit2 = suit
    
    return high_card_cmp(suit_counts1[flush_suit1], suit_counts2[flush_suit2])

def full_house_cmp(hand1, hand2):
    map1 = {}
    maxpair1 = 0
    maxtrip1 = 0
    map2 = {}
    maxpair2 = 0
    maxtrip2 = 0 

    for card in hand1:
        val = card[0]
        if val == 1:
            val = len(values) + 1
        if not val in map1:
            map1[val] = 1
        else:
            map1[val] += 1

    for card in hand2:
        val = card[0]
        if val == 1:
            val = len(values) + 1
        if not val in map2:
            map2[val] = 1
        else:
            map2[val] += 1

    for val in map1:
        if map1[val] == 2 and val > maxpair1:
            maxpair1 = val
        elif map1[val] > 2 and val > maxtrip1:
            maxtrip1 = val
    
    for val in map2:
        if map2[val] == 2 and val > maxpair2:
            maxpair2 = val
        elif map2[val] > 2 and val > maxtrip2:
            maxtrip2 = val

    if maxtrip1 > maxtrip2:
        return 1
    elif maxtrip1 < maxtrip2:
        return -1
    else:
        if maxpair1 > maxpair2:
            return 1
        elif maxpair1 < maxpair2:
            return -1
        else:
            return 0

ranked_cmp_functions = [
    lambda h1, h2 : 0,
    straight_cmp,
    lambda h1, h2 : number_of_a_kind_cmp(h1, h2, 4),
    full_house_cmp,
    flush_cmp,
    straight_cmp,
    lambda h1, h2 : number_of_a_kind_cmp(h1, h2, 3),
    two_pair_cmp,
    lambda h1, h2 : number_of_a_kind_cmp(h1, h2, 2),
    high_card_cmp
]

ranked_validators = [
    validators["royal flush"],
    validators["straight flush"],
    validators["four of a kind"],
    validators["full house"],
    validators["flush"],
    validators["straight"],
    validators["three of a kind"],
    validators["two pair"],
    validators["pair"],
    validators["high card"]
]

def hand_cmp(hand1, hand2):
    rank1 = 0
    rank2 = 0

    for i in range(len(ranked_validators)):
        if ranked_validators[i](hand1):
            rank1 = i
            break
    
    for i in range(len(ranked_validators)):
        if ranked_validators[i](hand2):
            rank2 = i
            break

    if rank1 == rank2:
        return ranked_cmp_functions[rank1](hand1, hand2)
    else:
        if rank1 > rank2:
            return 1
        elif rank1 < rank2:
            return -1
        else:
            return 0

if __name__ == '__main__':
    from card import combinations, hand_tostring
    import functools, sys

    hands = []
    deck = make_deck()
    test = 0
    if len(sys.argv) > 1:
        test = int(sys.argv[1])
    validator = ranked_validators[test]

    for hand in combinations(deck, 5):
        if validator(hand):
            hands.append(hand)
            if hand[0][0] == 1 and hand[1][0] == 1 and hand[2][0] == 1 and hand[3][0] == 1 and hand[4][0] == 1:
                print(hand)
    
    hands.sort(key=functools.cmp_to_key(ranked_cmp_functions[test]))

    for hand in hands:
        print(hand_tostring(hand))
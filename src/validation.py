#cython: language_level=3

# hand validation functions

from cards import suits, values

def royal_flush(hand):
    flush_dict = {suit: set() for suit in suits}

    for card in hand:
        if card[0] == 1 or card[0] > 9:
            flush_dict[card[1]].add(card[0])
            if len(flush_dict[card[1]]) >= 5:
                return True
    
    return False

def straight_flush(hand):
    length = len(values)
    suit_counts = {}

    for suit in suits:
        suit_counts[suit] = [0 for i in range(length)]

    for card in hand:
        suit_counts[card[1]][card[0] - 1] += 1

    for suit in suit_counts:
        consecutive = 0
        for i in range(length + 1):
            if suit_counts[suit][i % length] != 0:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive == 5:
                return True
        
    return False

def four_of_a_kind(hand):
    counts = {}

    for card in hand:
        if card[0] in counts:
            counts[card[0]] += 1
        else:
            counts[card[0]] = 1

    for card in counts:
        if counts[card] == 4:
            return True
    
    return False

def full_house(hand):
    counts = {}
    triple = 0
    double = 0

    for card in hand:
        if card[0] in counts:
            counts[card[0]] += 1
        else:
            counts[card[0]] = 1

    for card in counts:
        if counts[card] >= 3:
            triple += 1
        elif counts[card] >= 2:
            double += 1

    return triple >= 2 or (triple >= 1 and double >= 1)

def flush(hand):
    suit_counts = {}
    
    for card in hand:
        if card[1] in suit_counts:
            suit_counts[card[1]] += 1
            if suit_counts[card[1]] == 5:
                return True
        else:
            suit_counts[card[1]] = 1
    
    return False

def straight(hand):
    length = len(values)
    counts = [0 for i in range(length)]
    consecutive = 0

    for card in hand:
        counts[card[0] - 1] += 1

    for i in range(length + 1):
        if counts[i % length] != 0:
            consecutive += 1
        else:
            consecutive = 0
        if consecutive == 5:
            return True
        
    return False


def three_of_a_kind(hand):
    counts = {}

    for card in hand:
        if card[0] in counts:
            counts[card[0]] += 1
        else:
            counts[card[0]] = 1

    for card in counts:
        if counts[card] == 3:
            return True
    
    return False

def two_pair(hand):
    counts = {}
    pairs = 0

    for card in hand:
        if card[0] in counts:
            counts[card[0]] += 1
        else:
            counts[card[0]] = 1
    
    for card in counts:
        if counts[card] == 2:
            pairs += 1
    
    return pairs > 1

def pair(hand):
    counts = {}

    for card in hand:
        if card[0] in counts:
            counts[card[0]] += 1
        else:
            counts[card[0]] = 1

    for card in counts:
        if counts[card] == 2:
            return True
    
    return False

validators = [
    royal_flush,
    straight_flush,
    four_of_a_kind,
    full_house,
    flush,
    straight,
    three_of_a_kind,
    two_pair,
    pair,
    lambda x : True
]
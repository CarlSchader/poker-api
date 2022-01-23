# data types

suits = {'d': '\u2666','h': '\u2665', 'c': '\u2663', 's': '\u2660'}
suits_inverse = {'\u2666': 'd', '\u2665': 'h', '\u2663': 'c', '\u2660': 's'}
values = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
value_map = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}

# printing functions

def val_tostring(val):
    return values[(val - 1) % 13]

def suit_tostring(suit):
    return suits[suit]

def card_tostring(card):
    return val_tostring(card[0]) + suit_tostring(card[1])

def hand_tostring(hand):
    string = ""
    for i in range(len(hand) - 1):
        string += card_tostring(hand[i]) + ' '
    return string + card_tostring(hand[len(hand) - 1])

def print_deck(deck):
    for i in range(len(deck)):
        if i != len(deck) - 1:
            print(card_tostring(deck[i]), end=", ")
        else:
            print(card_tostring(deck[i]))

def string_tocard(string):
    return (value_map[string[:-1]], suits_inverse[string[-1]])

def string_tohand(string):
    card_strings = string.split(' ')
    hand = []
    
    for card_string in card_strings:
        hand.append(string_tocard(card_string))
    
    return tuple(hand)

# model functions

def make_deck(input_exclude_set=set()):
    exclude_set = set(input_exclude_set)
    deck = []
    for suit in suits:
        for val in range(1, 14):
            if not (val, suit) in exclude_set:
                deck.append((val, suit))
    return deck

def increment_indices(indices, size):
    length = len(indices)
    i = length - 1
    while i >= 0:
        indices[i] = (indices[i] + 1) % (size - (length - i - 1))
        if indices[i] != 0 or i == 0:
            break
        else:
            i -= 1
    
    i += 1
    while i < length:
        indices[i] = indices[i - 1] + 1
        i += 1


def combinations(container, number):
    size = len(container)
    container_tuple = tuple(container)
    indices = [i for i in range(number)]
    final_indices = [i for i in range(size - number, size)]
    done = False
    
    while not done:
        yield tuple([container_tuple[indices[i]] for i in range(number)])

        for i in range(number):
            if indices[i] == final_indices[i]:
                if i == number - 1:
                    done = True
            else:
                break
        
        increment_indices(indices, size)
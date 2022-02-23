import functools, math
from cards import combinations, make_deck, hand_tostring
from validation import validators
from compare import ranked_cmp_functions

def generate_rank_table(path):
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

if __name__ == '__main__':
    import sys
    generate_rank_table(sys.argv[1])
#cython: language_level=3

import json
from cards import hand_tostring, string_tohand

def load_table(path):
    try:
        f = open(path, 'r')
        table_unset = json.load(f)
        f.close()
        table = {}

        for hand_string in table_unset:
            table[frozenset(string_tohand(hand_string))] = table_unset[hand_string]

        return table
    except:
        return {}

def write_table(table, path):
    f = open(path, 'w+')
    f.write('{\n')
    i = 0
    for key in table:
        if i == len(table) - 1:
            f.write('\t"{}": {}\n'.format(hand_tostring(tuple(key)), json.dumps(table[key])))
        else:
            f.write('\t"{}": {},\n'.format(hand_tostring(tuple(key)), json.dumps(table[key])))
        i += 1
    f.write('}')
    f.close()

def write_array(array, path):
    f = open(path, 'w+')
    f.write('[\n')
    i = 0
    for elem in array:
        if i == len(array) - 1:
            f.write('\t{}\n'.format([hand_tostring(tuple(elem[0])), elem[1]]).replace("'", '"'))
        else:
            f.write('\t{},\n'.format([hand_tostring(tuple(elem[0])), elem[1]]).replace("'", '"'))
        i += 1
    f.write(']')
    f.close()

def load_array_as_dict(path):
    try:
        f = open(path, 'r')
        array = json.load(f)
        f.close()
        table = {}

        for i in range(len(array)):
            hand_string = array[i][0]
            stats = dict(array[i][1])
            stats['rank'] = i + 1
            table[frozenset(string_tohand(hand_string))] = stats
        return table
    except:
        return {}
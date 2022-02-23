import functools

def dict_cmp(x, y, key):
    if str(x[key]) > str(y[key]):
        return 1
    elif str(x[key]) < str(y[key]):
        return -1
    else:
        return 0

def sort_dict(dictionary, cmp_func):
    arr = []
    for key in dictionary:
        arr.append((key, dictionary[key]))
    
    arr.sort(key=functools.cmp_to_key(lambda x, y : cmp_func(x[1], y[1])))
    return arr
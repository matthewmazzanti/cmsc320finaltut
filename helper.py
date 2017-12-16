import re
from collections import defaultdict
import itertools as it

reg = [(re.compile('\'em'), 'them'),
       (re.compile('in\''), 'ing'),
       (re.compile('\[.*\]'),''),
       (re.compile('[\n]+'),'\n'),
       (re.compile('[^a-z\' \n]'), '')]

def clean_text(dirty):
    clean = dirty.lower()
    for ex,replace in reg:
        clean = ex.sub(replace,clean)

    return clean

def load_phones(file_name='cmudict-0.7b.phones'):
    phones = defaultdict(lambda: set([]))
    with open(file_name,'r') as f:
        for line in f:
            split = line.split()
            phones[split[1]].add(split[0])

    vowels = set([])
    for phone in phones['vowel']:
        vowels.add(phone)
        for i in range(0,2):
            vowels.add(phone + str(i))
    phones['vowel'] = vowels
    
    return phones

def rem_dup(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def flt(lst):
    return list(it.chain.from_iterable(lst))

def to_int_keys_best(l):
    """
    l: iterable of keys
    returns: a list with integer keys
    """
    seen = set()
    ls = []
    for e in l:
        if not e in seen:
            ls.append(e)
            seen.add(e)
    ls.sort()
    index = {v: i for i, v in enumerate(ls)}
    return [index[v] for v in l],ls

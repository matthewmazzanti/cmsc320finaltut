from itertools import zip_longest, islice


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


def suffix_matrix_best(s):
    """
    suffix matrix of s
    O(n * log(n)^2)
    """
    n = len(s)
    k = 1
    line,ls = to_int_keys_best(s)
    ans = [line]
    while max(line) < n - 1:
        line,_ = to_int_keys_best(
            [a * (n + 1) + b + 1
             for (a, b) in
             zip_longest(line, islice(line, k, None),
                         fillvalue=-1)])
        print(line)
        ans.append(line)
        k <<= 1
    return ans,ls


def suffix_array_best(s):
    """
    suffix array of s
    O(n * log(n)^2)
    """
    n = len(s)
    k = 1
    line = to_int_keys_best(s)
    while max(line) < n - 1:
        line = to_int_keys_best(
            [a * (n + 1) + b + 1
             for (a, b) in
             zip_longest(line, islice(line, k, None),
                         fillvalue=-1)])
        k <<= 1
    return line

mat,ls = suffix_matrix_best('banana')
print(mat)
for i in mat[2]:
    print(list(map(lambda x: ls[x],mat[0][i:])))

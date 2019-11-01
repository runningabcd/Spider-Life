# reverse str list

_list = [str(x) for x in range(1, 101)]

def reverse(_list=None):
    nos = len(_list)
    mid = nos // 2
    for x in range(0, mid):
        l_v = _list[x]
        h_v = _list[nos-x-1]
        _list[x] = h_v
        _list[nos-x-1] = l_v
    return _list

print(reverse(_list))

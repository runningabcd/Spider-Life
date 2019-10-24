'''
    #排序
'''

_list = [10, 11, 21, 9, 67, 1, 3, 5, 2, 31, 41, 45, 23, 13]


def buddle_sort(_list=None) -> list:
    for i in range(len(_list)):
        for j in range(i + 1, len(_list)):
            if _list[i] <= _list[j]:
                continue
            _list[i], _list[j] = _list[j], _list[i]
    return _list


def quick_sort(_list: list, left: int, right: int) -> list:
    if left >= right:
        return []
    low = left
    high = right
    mid = _list[low]
    while low < high:
        while low < high and _list[high] > mid:
            high -= 1
        _list[low] = _list[high]
        _list[high] = mid
        while low < high and _list[low] <= mid:
            low += 1
        _list[high] = _list[low]
        _list[low] = mid
    qucik_sort(_list, left, low - 1)
    qucik_sort(_list, low + 1, right)
    return _list


def binary_search(_list: list, key: int):
    low = 0
    high = len(_list)
    while low < high:
        mid = (low + high) // 2
        if key < _list[mid]:
            high = mid
        elif key > _list[mid]:
            low = mid + 1
        else:
            print('/'*66)
            break


if __name__ == '__main__':
    buddle_sort(_list)
    _lists = quick_sort(_list, 0, len(_list) - 1)
    binary_search(_lists, 10)

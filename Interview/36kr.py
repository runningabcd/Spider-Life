##### 好吧，算法这个词原来叫的这么随便

from Interview.utils import run_time
import timeit


# 111111

# 很多种方式可以实现呀，咱用递归试试
@run_time
def recursion_hex_str(a: str, b: str) -> str:
    _a = int(a, 3)
    _b = int(b, 3)
    c = _a + _b

    def reverse(n):
        result = ''
        if not n:
            return result
        result = reverse(n // 3)
        return result + str(n % 3)

    return reverse(c)


# 循环 面试官推荐做法
@run_time
def while_hex_str(a: str, b: str) -> str:
    _a = int(a, 3)
    _b = int(b, 3)
    c = _a + _b
    _c = []

    while 1:
        v = c // 3
        k = c % 3
        _c.append(str(k))
        if not v:
            break
        c = v

    _c.reverse()
    return ''.join(_c)


# timeit.repeat("while_hex_str('201', '102')", "from __main__ import while_hex_str",
#               number=1000)


# 222222

# 面试官说字典的效率较高，咱们测试下吧
# 小哥哥说面试官从来没用过eval

@run_time
def eval_hex_int(a: str, b: str) -> int:
    _a = a[::-1]
    _b = b[::-1]

    def str_int(ii):
        n = 0
        for i, v in enumerate(ii):
            n += eval(v) * (3 ** i)
        return n

    return str_int(_a) + str_int(_b)


# 咱不用eval
@run_time
def ord_hex_int(a: str, b: str) -> int:
    _a = a[::-1]
    _b = b[::-1]

    def str_int(ii):
        n = 0
        for i, v in enumerate(ii):
            _v = ord(v) - ord('0')
            n += _v * (3 ** i)
        return n

    return str_int(_a) + str_int(_b)


# 写个简单的吧
@run_time
def for_hex_int(a: str, b: str) -> int:
    _a = a[::-1]
    _b = b[::-1]

    def str_int(ii):
        n = 0
        for i, v in enumerate(ii):
            for j in range(0, 9):
                if v != str(j):
                    continue
                n += j * (3 ** i)
        return n

    return str_int(_a) + str_int(_b)


# 面试官推荐做法
@run_time
def dict_hex_int(a: str, b: str) -> int:
    _a = a[::-1]
    _b = b[::-1]
    nos = [x for x in range(0, 10)]
    strs = [str(y) for y in range(0, 10)]
    no_str = dict(zip(strs, nos))

    def str_int(ii):
        n = 0
        for i, v in enumerate(ii):
            n += no_str[v] * (3 ** i)
        return n

    return str_int(_a) + str_int(_b)

# timeit.repeat("for_hex_int('201', '102')", "from __main__ import for_hex_int",
#               number=1000)
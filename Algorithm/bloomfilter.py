'''
布隆过滤器原理
布隆过滤器（Bloom Filter）的核心实现是一个超大的位数组和几个哈希函数。假设位数组的长度为m，哈希函数的个数为k



具体的操作流程：假设集合里面有3个元素{x, y, z}，哈希函数的个数为3。首先将位数组进行初始化，将里面每个位都设置位0。对于集合里面的每一个元素，将元素依次通过3个哈希函数进行映射，每次映射都会产生一个哈希值，这个值对应位数组上面的一个点，然后将位数组对应的位置标记为1。查询W元素是否存在集合中的时候，同样的方法将W通过哈希映射到位数组上的3个点。如果3个点的其中有一个点不为1，则可以判断该元素一定不存在集合中。反之，如果3个点都为1，则该元素可能存在集合中。注意：此处不能判断该元素是否一定存在集合中，可能存在一定的误判率。可以从图中可以看到：假设某个元素通过映射对应下标为4，5，6这3个点。虽然这3个点都为1，但是很明显这3个点是不同元素经过哈希得到的位置，因此这种情况说明元素虽然不在集合中，也可能对应的都是1，这是误判率存在的原因。

布隆过滤器添加元素
将要添加的元素给k个哈希函数
得到对应于位数组上的k个位置
将这k个位置设为1
布隆过滤器查询元素
将要查询的元素给k个哈希函数
得到对应于位数组上的k个位置
如果k个位置有一个为0，则肯定不在集合中
如果k个位置全部为1，则可能在集合中
'''

import mmh3
from bitarray import bitarray

# zhihu_crawler.bloom_filter

# Implement a simple bloom filter with murmurhash algorithm.
# Bloom filter is used to check wether an element exists in a collection, and it has a good performance in big data situation.
# It may has positive rate depend on hash functions and elements count.


BIT_SIZE = 5000000


class BloomFilter:

    def __init__(self):
        # Initialize bloom filter, set size and all bits to 0
        bit_array = bitarray(BIT_SIZE)
        bit_array.setall(0)

        self.bit_array = bit_array

    def add(self, url):
        # Add a url, and set points in bitarray to 1 (Points count is equal to hash funcs count.)
        # Here use 7 hash functions.
        point_list = self.get_postions(url)

        for b in point_list:
            self.bit_array[b] = 1

    def contains(self, url):
        # Check if a url is in a collection
        point_list = self.get_postions(url)

        result = True
        for b in point_list:
            result = result and self.bit_array[b]

        return result

    def get_postions(self, url):
        # Get points positions in bit vector.
        point1 = mmh3.hash(url, 41) % BIT_SIZE
        point2 = mmh3.hash(url, 42) % BIT_SIZE
        point3 = mmh3.hash(url, 43) % BIT_SIZE
        point4 = mmh3.hash(url, 44) % BIT_SIZE
        point5 = mmh3.hash(url, 45) % BIT_SIZE
        point6 = mmh3.hash(url, 46) % BIT_SIZE
        point7 = mmh3.hash(url, 47) % BIT_SIZE

        return [point1, point2, point3, point4, point5, point6, point7]


#### scrapy 使用bloom filter

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilters(object):
    def __init__(self, server, key, blockNum=1):
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31]
        # self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.server = server
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            return False
        ret = True

        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)

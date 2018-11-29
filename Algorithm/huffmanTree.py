#### 哈夫曼算法

'''
霍夫曼编码是一种使用变长编码表编码源符号的无损压缩算法。它的核心思想是计算各个符号的权重，出现次数较多的符号拥有较大的权重，出现次数较少的符号拥有较小的权重。然后对符号进行前缀编码，用较短的编码表示拥有较长权重的符号，用较长的编码表示拥有较短权重的符号。这样，总体来说，对于符号出现次数不均衡的序列，霍夫曼编码就能够拥有较好的表现。

压缩过程
霍夫曼编码的压缩阶段主要有以下几个步骤：

读入符号，计算各个符号的权重。
根据符号的权重建立霍夫曼树。
依据霍夫曼树建立编码表。
压缩
计算权重
计算权重很容易理解。遍历符号，计算各个符号出现的次数。把出现的次数当作权重即可。实际实现中，如果以字节为单位压缩，考虑到一个字节有8位，最大能表示255。为了操作方便，可以将出现的次数除以最大的出现次数，再乘以256当作权重。这样，所有权重就刚分布在一个字节的表示范围以内。

同时，考虑到一个字节的编码刚好是0~255，可以建立一个数组，这个数组的下标表示对应的符号，这个数组的值表示符号的权重。


计算了各个符号的权重之后，就可以根据这些权重建立霍夫曼树。从霍夫曼树中，我们可以得到符号的前缀码表。

建立霍夫曼树
霍夫曼树是一颗二叉树，其每个节点至少有四个值——符号，权重，左树指针，右树指针。建立霍夫曼树主要有两种方式。第一种是使用一个优先队列（堆）。首先，为所有的符号创造一个节点，储存进这个符号本身和它的权重。然后将所有的节点压入优先队列，拥有最低权重的节点拥有最高的优先级（即，低权重的节点会先被弹出。）然后执行以下步骤：

如果优先队列中的元素大于一，弹出两个节点。以这两个节点为左右指针创建一颗新的霍夫曼树，其权重为作为节点之和。将这个新树压入优先队列。重复本步骤。
否则，弹出剩下的元素作为最终的霍夫曼树。
除了优先队列外，还可以使用两个队列来建立霍夫曼树。首先，像前面那样创建节点，按照权重排序所有节点。然后创建两个队列，将节点按照权重从低到高的顺序依次入其中一个队列1。然后执行以下步骤：

如果一个队列为空，从另一个队列中弹出两个元素；否则，比较两个队列首元素的权重，弹出权重最小的两个元素。用这两个元素作为子树建立一个新的霍夫曼树，其权重为两元素权重之和。将这颗新树压入队列2。重复本步骤，直到队列只剩下一个元素。
弹出这个元素作为最终的霍夫曼树。

建立编码表
根据得到的霍夫曼树，我们可以为符号建立一组前缀码。

如果一组编码，其中任意一个编码都不为另一个编码的前缀，那么我们就称这组编码为一组前缀码。将符号使用前缀码编码是极有意义的。这意味着，对于一组编码，我们可以不借助任何分割符解码其中的每一个符号。即，此时，这组编码是唯一可解的。

前面说过，霍夫曼树是一颗二叉树。因此，这颗二叉树的所有叶子节点的路径组成的编码即为一组前缀码。把左子树编码为0，将右子树编码为1。


压缩
把符号按照编码表替换为相应为即可。

如果用C语言实现，可以方便地直接对内存进行位操作。而Python的位操作比较麻烦。因此，可以先将所有二进制编码先视为字符串，然后每8位字符串转换为一个16进制数，转换为python中的bytes类型，直接写入文件即可。

将符号频率同编码一同写入文件，就可以在之后通过读取频率来解压。


解压过程
解压过程较简单，是前面压缩过程的逆操作。

首先读取符号频率，根据符号频率建立霍夫曼树，然后再根据霍夫曼树解压编码即可。

'''

import heapq


class HuffmanNode:
    def __init__(self, symbol=None, freq=None):
        self.symbol = symbol
        self.freq = freq
        self.parent = None
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def is_leaf(self):
        return not self.left and not self.right

    def get_code(self):
        # 调试用
        if not self.is_laef():
            raise ValueError("Not a leaf node.")

        code = ''
        node = self
        while node.parent:
            if node.parent.left == node:
                code = '0' + code
            else:
                code = '1' + code
            code = code.parent

        return code


class Huffman:
    BYTE_MAX_NUM = 255

    def __init__(self):
        self.origin = None
        self.compressed = None
        self.huffman_tree = None
        self.freqs = [0 for _ in range(self.BYTE_MAX_NUM + 1)]
        self.coding_table = [0 for _ in range(self.BYTE_MAX_NUM + 1)]
        self.reverse_table = {}
        self.coding_str = ''

    def _minimize_frequencies(self):
        # 缩小字频使其在一个字节范围以内
        max_freq = max(self.freqs)

        for symbol, freq in enumerate(self.freqs):
            scale_freq = int(self.BYTE_MAX_NUM * (freq / max_freq))
            scale_freq = 1 if not scale_freq and freq else scale_freq

            self.freqs[symbol] = scale_freq

    def _get_symbol_frequencies(self):
        for symbol in self.origin:
            self.freqs[symbol] += 1

        self._minimize_frequencies()

    def _initial_node_heap(self):
        self._heap = []
        for symbol, freq in enumerate(self.freqs):
            node = HuffmanNode(symbol, freq)
            heapq.heappush(self._heap, node)

    def _build_huffman_tree(self):
        self._initial_node_heap()

        while len(self._heap) > 1:
            node1 = heapq.heappop(self._heap)
            node2 = heapq.heappop(self._heap)

            new_node = HuffmanNode(symbol=None, freq=node1.freq + node2.freq)
            new_node.left, new_node.right = node1, node2
            node1.parent, node2.parent = new_node, new_node
            heapq.heappush(self._heap, new_node)

        self.huffman_tree = heapq.heappop(self._heap)
        del self._heap
        return self.huffman_tree

    def _build_coding_table(self, node, code_str=''):
        if node is None:
            return

        if node.symbol is not None:
            self.coding_table[node.symbol] = code_str
            self.reverse_table[code_str] = node.symbol

        self._build_coding_table(node.left, code_str + '0')
        self._build_coding_table(node.right, code_str + '1')

    def _pading_coding_str(self):
        pading_count = 8 - len(self.coding_str) % 8
        self.coding_str += '0' * pading_count
        state_str = '{:08b}'.format(pading_count)
        self.coding_str = state_str + self.coding_str

    def _prefix_coding_freqs(self):
        coding_freqs = []
        for freq in self.freqs:
            coding_freqs.append('{:08b}'.format(freq))
        coding_freqs = ''.join(coding_freqs)
        self.coding_str = coding_freqs + self.coding_str

    def _build_codeing_str(self):
        temp = []
        for symbol in self.origin:
            temp.append(self.coding_table[symbol])
        self.coding_str = ''.join(temp)

        self._pading_coding_str()
        self._prefix_coding_freqs()

        return self.coding_str

    def _get_compressed(self):
        assert (len(self.coding_str) % 8 == 0)

        b = bytearray()
        for index in range(0, len(self.coding_str), 8):
            code_num = int(self.coding_str[index:index + 8], 2)
            b.append(code_num)

        self.compressed = bytes(b)
        return self.compressed

    def _read_frequencies_from_compressed(self):
        coding_freqs = self.compressed[:self.BYTE_MAX_NUM + 1]
        for index, freq in enumerate(coding_freqs):
            self.freqs[index] = freq

    def _get_real_coding_from_compressed(self):
        pading_count = self.compressed[self.BYTE_MAX_NUM + 1]
        byte_coding_str = self.compressed[self.BYTE_MAX_NUM + 2:]
        coding_str = []
        for num in byte_coding_str:
            temp = bin(num)[2:]
            # 补足省略掉的前导零
            temp = '0' * (8 - len(temp)) + temp
            assert (len(temp) == 8)
            coding_str.append(temp)
        coding_str = ''.join(coding_str)
        assert (len(coding_str) % 8 == 0)
        real_coding_str = coding_str[:-pading_count]
        return real_coding_str

    def _decode_compressed(self):
        real_coding_str = self._get_real_coding_from_compressed()
        decode_content = []

        node = self.huffman_tree
        for state in real_coding_str:
            if state == '0':
                node = node.left
            elif state == '1':
                node = node.right

            if node.symbol is not None:
                assert (0 <= node.symbol <= self.BYTE_MAX_NUM)
                hex_str = hex(node.symbol)[2:]
                # fromhex方法将两个字符识别为一个16进制数
                # 所以单个数需要补零
                hex_str = '0' + hex_str if len(hex_str) == 1 else hex_str
                decode_content.append(hex_str)
                node = self.huffman_tree

        decode_content = ''.join(decode_content)
        return bytes.fromhex(decode_content)

    def clear(self):
        self.__init__()

    def encode(self, origin):
        self.clear()
        self.origin = origin
        self._get_symbol_frequencies()
        self._build_huffman_tree()
        self._build_coding_table(self.huffman_tree)
        self._build_codeing_str()

        return self._get_compressed()

    def compresse(self, filename, output_filename=None):
        with open(filename, 'rb') as file:
            origin = file.read()

        compressed_content = self.encode(origin)
        if output_filename is None:
            output_filename = filename + '.hfm'
        with open(output_filename, 'wb') as file:
            file.write(compressed_content)

        return True

    def decode(self, compressed):
        self.clear()
        self.compressed = compressed
        self._read_frequencies_from_compressed()
        self._build_huffman_tree()
        return self._decode_compressed()

    def uncompresse(self, filename, output_filename=None):
        with open(filename, 'rb') as file:
            compressed = file.read()

        decode_content = self.decode(compressed)
        if output_filename is None:
            if filename.endswith('.hfm'):
                output_filename = filename[:-4]
            else:
                output_filename = filename + '.dhfm'

        with open(output_filename, 'wb') as file:
            file.write(decode_content)

        return True

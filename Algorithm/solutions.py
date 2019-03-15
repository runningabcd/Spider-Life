'''
    btree find max depth
'''


class TreeNode(object):
    class ChildNode(object):
        class CCNode(object):
            left = None
            right = None

        left = CCNode()
        right = CCNode()

    left = ChildNode()
    right = ChildNode()


class Solution(object):

    def maxdepth(self, treenode:object) -> int:
        print('-'*66)
        if not treenode:
            return 0
        print('1' * 66)
        print(treenode)
        left = self.maxdepth(treenode.left)
        print('2' * 66)
        print(left)
        print(treenode)
        print('3' * 66)
        right = self.maxdepth(treenode.right)
        print('4' * 66)
        print(treenode)
        print(right)
        return max(left, right) + 1
 
#Manacher 马拉车回文串
class Solution4:
    def longestPalindrome(self, s: str) -> str:
        temp = ""
        for i in s:
            temp += "#" + i
        temp += "#"
        maxRight = 0
        pos = 0
        str_len = len(temp)
        RL = [0] * str_len
        max_len = 0
        for i in range(str_len):

            # 求 i 已 pos为对称中心的对称点 j
            j = 2 * pos - i
            # 判断 i 的位置 a i在maxright左边  b.i在maxright右边
            if maxRight > i:
                # 两种情况 根据 i 到 maxRight的距离判断 若是maxRight-i > RL[j] 那么 RL[j] = RL[i]
                # 若是maxRight-i < RL[j] 也就是说已j为中心的回文串不在已pos文中心的回文串中 那么 RL[i] >= maxRight-i
                RL[i] = min(RL[j], maxRight - i)
            else:
                # 否则的话从1开始
                RL[i] = 1
            # 左右拓展，判断是不是回文串，若是回文串，则加1
            while i - RL[i] >= 0 and i + RL[i] < len(temp) and temp[i - RL[i]] == temp[i + RL[i]]:
                RL[i] += 1
            # RL[i] - 1是已i为中心的回文串的半径 若是i+回文串半径超过maxRight 则 更新maxRight 以及pos
            if i + RL[i] - 1 > maxRight:
                maxRight = i + RL[i] - 1
                pos = i
            if RL[i] > max_len:
                max_len = RL[i]
                max_index = i
        return s[
               int((max_index - max_len) / 2 + 1):
               int((max_index + max_len) / 2)
               ]


# Z 字形变换
class Solution5(object):
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1:
            return s
        nr = numRows - 1
        str_len = len(s)
        dstr = ''
        for i in range(numRows):
            for j in range(i, str_len, 2 * nr):
                dstr += s[j]
                next_index = j + 2 * (nr - i)
                if next_index <= j:
                    continue
                if next_index >= str_len:
                    continue
                if i == 0:
                    continue
                dstr += s[next_index]
        return dstr

# 整数反转
class Solution6:
    def reverse(self, x: int) -> int:
        x = str(x)
        if '-' in x:
            x = int('-' + x[1:][::-1])
        else:
            x = int(x[::-1])
        if x < -2 ** 31 or x > 2 ** 31 - 1:
            return 0
        return x

# 字符串转换整数 (atoi)
class Solution7:
    def myAtoi(self, string: str) -> int:
        dig_list = [str(j) for j in range(0, 10)]
        words = ''.join([chr(97 + i) for i in range(26)])
        dstr = ''
        for i in iter(string.lstrip()):
            if not dstr:
                if i in words:
                    return 0
                if not i:
                    continue
                if i not in dig_list+['-', '+']:
                    return 0
                dstr+=i
            else:
                if i not in dig_list:
                    break
                else:
                    dstr+=i
        if len(dstr)<=1:
            if len(dstr) == 1:
                if dstr not in dig_list:
                    return 0
                else:
                    return int(dstr)
            return 0
        result = int(float(dstr))
        if result < -2 ** 31:
            return -2 ** 31
        elif result > 2 ** 31 - 1:
            return 2 ** 31 - 1
        return result

# 回文数
class Solution8:
    def isPalindrome(self, x: int) -> bool:
        if not x:
            return True
        str_x = str(x)
        if str_x != str_x[::-1]:
            return False
        return True


print(Solution().maxdepth(TreeNode()))

'''
    check tree is balance tree
'''


class Solution1(object):

    def maxdepth(self, treenode=None) -> int:
        if not treenode:
            return 1
        left = self.maxdepth(treenode.left)
        right = self.maxdepth(treenode.right)
        return max(right, left)

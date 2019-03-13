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
        s = '#' + '#'.join(s) + '#'
        maxRight = 0
        pos = 0
        RL = [0] * len(s)
        for i in range(len(s)):
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
            while i - RL[i] >= 0 and i + RL[i] < len(s) and s[i - RL[i]] == s[i + RL[i]]:
                RL[i] += 1
            # RL[i] - 1是已i为中心的回文串的半径 若是i+回文串半径超过maxRight 则 更新maxRight 以及pos
            if i + RL[i] - 1 > maxRight:
                maxRight = i + RL[i] - 1
                pos = i
            if RL[i] == max(RL):
                max_index = i
        lenth = max(RL)-1
        return s[max_index-lenth: max_index+lenth+1].replace('#', '')


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

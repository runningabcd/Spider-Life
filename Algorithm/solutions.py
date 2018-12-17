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

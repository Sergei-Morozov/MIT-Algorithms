"""
AVL trees

Invariant:
    - lenght of left/right for every node differ at most +/- 1

Details:
    - each node attr is height
    - rotate avl on each operation (left rotate / right rotate)

Implement:
    - delete
    - rotateLeft
    - rotateRight
    - rebalance
"""
from typing import Optional
from dataclasses import dataclass
from queue import Queue


def height(node):
    if node:
        return node.height
    return 0

def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1

@dataclass
class Node:
    """
    Node class
    """
    parent: Optional['Node']
    left: Optional['Node']
    right: Optional['Node']

    height: int
    value: int

    def insert(self, value):
        if value < self.value:
            if self.left:
                return self.left.insert(value)
            else:
                self.left = Node(self, None, None, 0, value)
                return self.left

        elif value > self.value:
            if self.right:
                return self.right.insert(value)
            else:
                self.right = Node(self, None, None, 0, value)
                return self.right

    def find_next_larger(self):
        """
        1. if right find min
        2. go up
        """
        if self.right:
            return self.right.find_min()
        else:
            current = self
            while current.parent and current is current.parent.right:
                current = current.parent
            return current.parent

    def find_min(self):
        if self.left:
            return self.left.find_min()
        return self

    def delete(self):
        """
        1. no child
        2. one child
        3. both childs
        """
        if self.left == None and self.right == None:
            if self is self.parent.left:
                self.parent.left = None
            elif self is self.parent.right:
                self.parent.right = None
            return self
        elif self.left == None or self.right == None:
            if self is self.parent.left:
                self.parent.left = self.right or self.left
            elif self is self.parent.right:
                self.parent.right = self.right or self.left
            return self
        else:
            node = self.find_next_larger()
            node.value, self.value = self.value, node.value
            node.delete()
            return node

    def find(self, value):
        if value == self.value:
            return self
        elif value < self.value:
            if self.left:
                return self.left.find(value)
        elif value > self.value:
            if self.right:
                return self.right.find(value)

    ### Utility class functions
    def _str(self):
        """Internal method for ASCII art."""
        label = str(self.value)
        if self.left is None:
            left_lines, left_pos, left_width = [], 0, 0
        else:
            left_lines, left_pos, left_width = self.left._str()
        if self.right is None:
            right_lines, right_pos, right_width = [], 0, 0
        else:
            right_lines, right_pos, right_width = self.right._str()
        middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
        pos = left_pos + middle // 2
        width = left_pos + middle + right_width - right_pos
        while len(left_lines) < len(right_lines):
            left_lines.append(' ' * left_width)
        while len(right_lines) < len(left_lines):
            right_lines.append(' ' * right_width)
        if (middle - len(label)) % 2 == 1 and self.parent is not None and \
           self is self.parent.left and len(label) < middle:
            label += '.'
        label = label.center(middle, '.')
        if label[0] == '.': label = ' ' + label[1:]
        if label[-1] == '.': label = label[:-1] + ' '
        lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                 ' ' * left_pos + '/' + ' ' * (middle-2) +
                 '\\' + ' ' * (right_width - right_pos)] + \
          [left_line + ' ' * (width - left_width - right_width) + right_line
           for left_line, right_line in zip(left_lines, right_lines)]

        return lines, pos, width
    def __str__(self):
        return '\n'.join(self._str()[0])

    def print(self):
        if self.left:
            self.left.print()
        print(self.value, ':', self.height)
        if self.right:
            self.right.print()

    def check_ri(self):
        """
        Check binary tree invariant
        """
        if self.left:
            assert self.left.parent == self
            assert self.value > self.left.value
            self.left.check_ri()
        if self.right:
            assert self.right.parent == self
            assert self.value < self.right.value
            self.right.check_ri()

@dataclass
class Tree:
    root: Node

    def insert(self, value):
        if self.root is None:
            self.root = Node(None, None, None, 0, value)
        else:
            new_node = self.root.insert(value)
            self.rebalance(new_node)

    def delete(self, value):
        self.root.find(value).delete()


    def print(self):
        self.root.print()
        self.root.check_ri()

    def get_next_larger(self, value):
        node = self.root.find(value)
        return node.find_next_larger()

    def rotate_right(self, nodeb):
        """
        - find node
        - rotate in 3 steps as diagram
        """
        print('kek_R', nodeb.value)

        nodea = nodeb.parent

        # 1. update parents link
        if nodea.parent is None:
            self.root = nodeb
        else:
            if nodea is nodea.parent.left:
                nodea.parent.left = nodeb
            else:
                nodea.parent.right = nodeb
        nodeb.parent = nodea.parent

        # 2. update right
        nodea.left = nodeb.right
        if nodea.left:
            nodea.left.parent = nodea

        # 3. Link a<->b
        nodea.parent = nodeb
        nodeb.right = nodea

        update_height(nodea)
        update_height(nodeb)

    def rotate_left(self, nodeb):
        """
        - find node
        - rotate in 3 steps as diagram
        """
        print('kek_L', nodeb.value)
        nodea = nodeb.parent

        # 1. update parents link
        if nodea.parent is None:
            self.root = nodeb
        else:
            if nodea is nodea.parent.left:
                nodea.parent.left = nodeb
            else:
                nodea.parent.right = nodeb
        nodeb.parent = nodea.parent

        # 2. update right
        nodea.right = nodeb.left
        if nodea.right:
            nodea.right.parent = nodea

        # 3. Link a<->b
        nodea.parent = nodeb
        nodeb.left = nodea

        update_height(nodea)
        update_height(nodeb)

    def rebalance(self, node):
        # return
        while node is not None:
            update_height(node)
            if height(node.left) >= height(node.right) + 2:
                if height(node.left.left) > height(node.left.right):
                    self.rotate_right(node.left)
                else:
                    self.rotate_left(node.left.right)
                    self.rotate_right(node.left)

            elif height(node.right) >= height(node.left) + 2:
                if height(node.right.left) > height(node.right.right):
                    self.rotate_right(node.right.left)
                    self.rotate_left(node.right)
                else:
                    self.rotate_left(node.right)

            node = node.parent


    def show_tree(self):
        from binarytree import build
        queue = Queue()
        queue.put(self.root)
        result = []
        while not queue.empty():
            item = queue.get()
            if item:
                result.append(item.value)
                if item.left:
                    queue.put(item.left)
                else:
                    queue.put(None)
                if item.right:
                    queue.put(item.right)
                else:
                    queue.put(None)
            else:
                result.append(item)
        print(result)
        print(build(result))


if __name__ == '__main__':

    """
      __10___
     /       \
    8        _35_
     \      /    \
      9    34    901
    """
    tree = Tree(None)
    tree.insert(10)
    tree.insert(8)
    tree.insert(9)
    tree.insert(7)
    tree.insert(6)
    tree.insert(5)
    tree.insert(4)



    tree.insert(35)
    tree.insert(34)
    tree.insert(901)
    print(tree.root)

    # exit()
    # print(tree.root.find(35).value)
    # print(tree.root.find_min().value)
    # print(tree.get_next_larger(9).value)
    # # tree.delete(9)
    # tree.show_tree()
    # tree.print()
    # tree.rotate_right(tree.root.find(34))
    # tree.rotate_left(tree.root.find(35))
    # tree.root.check_ri()
    # tree.show_tree()
    # tree.root.check_ri()

"""
Binary Search tree
    -insert

    -find
    -find_min
    -find_max

    -next_larger
    -next_smaller

    -delete

"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    parent: Optional['Node']
    left: Optional['Node']
    right: Optional['Node']
    value: int

    def insert(self, value):
        if value < self.value:
            if self.left:
                self.left.insert(value)
            else:
                self.left = Node(self, None, None, value)
        elif value > self.value:
            if self.right:
                self.right.insert(value)
            else:
                self.right = Node(self, None, None, value)

    def find(self, value):
        if value == self.value:
            return self
        elif value < self.value:
            if self.left:
                return self.left.find(value)
        elif value > self.value:
            if self.right:
                return self.right.find(value)

    def find_min(self):
        if self.left:
            return self.left.find_min()
        return self

    def find_max(self):
        if self.right:
            return self.right.find_max()
        return self

    def delete(self):
        """
        1. has no children - delete
        2. has one child - delete + replace
        3. has 2 childs - replace with next_larger and delete
        """
        if not self.left or not self.right:
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                if self.parent.left:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if self.parent.right:
                    self.parent.right.parent = self.parent
            return self
        else:
            s = self.next_larger()
            self.key, s.key = s.key, self.key
            return s.delete()

    def next_larger(self):
        """
        1 case: if right - get its min element
        2 case: not right - traverse to parent while on right side
        """
        if self.right:
            return self.right.find_min()

        current = self
        while current.parent and current.parent.right == current:
            current = current.parent
        return current.parent

    def next_smaller(self):
        """
        1 case: if left - get its max element
        2 case: not left - traverse to parent while on left side
        """
        if self.left:
            return self.left.find_max()

        current = self
        while current.parent and current.parent.left == current:
            current = current.parent
        return current.parent

    def print(self):
        if self.left:
            self.left.print()
        print(self.value)
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

    def __repr__(self):
        return str(self.value)
@dataclass
class Tree:
    root: Node

    def insert(self, value):
        self.root.insert(value)

    def find(self, value):
        return self.root.find(value)

    def find_min(self):
        return self.root.find_min()

    def find_max(self):
        return self.root.find_max()

    def delete(self, value):
        node = self.root.find(value)
        node.delete()


    def next_larger(self, value):
        node = self.root.find(value)
        return node.next_larger()

    def next_smaller(self, value):
        node = self.root.find(value)
        return node.next_smaller()

    def print(self):
        print("Tree -=start=-")
        self.root.print()
        print("Tree -=end=-")

    def check_ri(self):
        self.root.check_ri()



if __name__ == '__main__':
    tree = Tree(Node(None, None, None, 10))
    tree.insert(9)
    tree.insert(25)
    tree.insert(5)
    tree.insert(51)
    print(tree.find(25))
    print(tree.find_max())
    print(tree.find_min())
    print(tree.next_larger(25))
    print(tree.next_smaller(9))
    tree.delete(9)
    tree.print()
    tree.check_ri()








"""
File: linkedbst.py
Author: Ken Lambert
"""
import math

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import random
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        pass

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        height = self.height()
        size = self._size
        return height < 2 * math.log(size + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        elem_lst = []
        for elem in self:
            elem_lst.append(elem)
        final_list = []
        for num in range(low, high + 1):
            final_list.append(elem_lst[num])
        return final_list

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        order = self.inorder()
        final_list = []
        for elem in order:
            final_list.append(elem)
        self.clear()

        def build_tree(input_lst):
            if not input_lst:
                return None
            middle_index = len(input_lst) // 2
            self.add(input_lst.pop(middle_index))
            build_tree(input_lst[:middle_index])
            build_tree(input_lst[middle_index:])

        return final_list

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for elem in self.inorder():
            if item < elem:
                return elem

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        final_lst = []
        for elem in self.inorder():
            final_lst.append(elem)
        for elem in final_lst[::-1]:
            if item > elem:
                return elem

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        print("Process begun!")
        with open(path, "r") as file:
            start_time = time.time()
            word_list = []
            for word in file:
                word_list.append(word)
            rand_start = random.randint(0, len(word_list) - 10000)
            for num in range(rand_start, rand_start + 10000):
                word = word_list[num]
                word_list.index(word)
            timestamp_1 = time.time() - start_time
            print(f"REPORT: Searching for 10000 words in list in alphabetic order took {timestamp_1} seconds!")
            file.close()
        with open(path, "r") as file:
            new_bst = LinkedBST()
            # count_lst = []
            # for word in file:
            #     count_lst.append(word)
            rand_help = random.randint(0, 200000)
            counter = 0
            for word in file:
                if rand_help < counter < rand_help + 900:
                    new_bst.add(word.split("\n")[0])
                    counter += 1
                elif counter == rand_help + 900:
                    break
                else:
                    counter += 1
                    continue
            start_time_2 = time.time()
            help_list = []
            for elem in new_bst:
                help_list.append(elem)
            for _ in range(10000):
                rand_elem = random.randint(0, 898)
                word = help_list[rand_elem]
                help_list.index(word)
            timestamp_2 = time.time() - start_time_2
            print(f"REPORT: Searching for 10000 words in BST in alphabetic order took {timestamp_2} seconds!")
        with open(path, "r") as file:
            new_bst = LinkedBST()
            counter = 0
            for word in file:
                if counter < 901:
                    rand_choice = random.randint(0, 1)
                    if rand_choice == 0:
                        continue
                    else:
                        counter += 1
                        new_bst.add(word)
                else:
                    break
            start_time_3 = time.time()
            help_list = []
            for elem in new_bst:
                help_list.append(elem)
            for _ in range(10000):
                rand_elem = random.randint(0, len(help_list) - 1)
                word = help_list[rand_elem]
                help_list.index(word)
            timestamp_3 = time.time() - start_time_3
            print(f"REPORT: Searching for 10000 words in BST in non-alphabetic order took {timestamp_3} seconds!")
            with open(path, "r") as file:
                new_bst = LinkedBST()
                counter = 0
                for word in file:
                    if counter < 901:
                        rand_choice = random.randint(0, 1)
                        if rand_choice == 0:
                            continue
                        else:
                            counter += 1
                            new_bst.add(word)
                    else:
                        break
                help_list = new_bst.rebalance()
                start_time_3 = time.time()
                # help_list = []
                # for elem in balanced_bst:
                #     help_list.append(elem)
                for _ in range(10000):
                    rand_elem = random.randint(0, len(help_list) - 1)
                    word = help_list[rand_elem]
                    help_list.index(word)
                timestamp_3 = time.time() - start_time_3
                print(
                    f"REPORT: Searching for 10000 words in Balanced BST in non-alphabetic order took {timestamp_3} seconds!")
        return "Process finished!"


if __name__ == "__main__":
    bst = LinkedBST()
    print(bst.demo_bst("words.txt"))

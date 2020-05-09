import numpy as np


class AVB(ValueStore):
    def __init__(self):
        self.root = Node()


class Node:
    def __init__(self):
        self.left = Node()
        self.right = Node()
        self.central = Node()
        self.value = 0
        self.occurrences = 0


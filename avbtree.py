from value_store import ValueStore


class AVB(ValueStore):
    def __init__(self):
        self.root = Node(None, None)

    # add node
    def create_node(self, value, index) -> bool:
        self.put(self.root, value)
        return True

    def put(self, node, value):
        # case 1 and 2 - insert value in the same node, or children
        node.value_left = Value(value) if node.value_left is None else node.value_left
        node.value_right = Value(value) \
            if node.value_right is not None and node.value_right.value < value else node.value_right

        node.node_left = Node(node, value) if node.node_left is None and node.value_left > value else node.node_left
        node.node_right = Node(node, value) if node.node_right is None and node.value_right < value else node.node_right

        node.value_left.occurrences = node.value_left.occurrences \
            if node.value_left.value == value else node.value_left.occurrences
        node.value_right.occurrences = node.value_right.occurrences \
            if node.value_right.value == value else node.value_right.occurrences

        if value < node.value_left.value:
            node.value_left = self.put(node.value_left, value)
        elif value > node.value_right.value:
            node.value_right = self.put(node.value_right, value)
        else:
            node.node_central = Node(node, value) if node.node_central is None else node.node_central
            node.value_central = self.put(node.value_central, value)

        if node.value_left is not None and node.value_central is not None and node.value_right is not None:
            if node.parent.value_left is not None and node.parent.value_right is not None:
                node_tmp = Node(None, node.value_central)

                node_tmp.node_left = Node(node_tmp, node.value_left)
                node_tmp.node_right = Node(node_tmp, node.value_right)

            # wyważenie drzewa

        return node

    def __balance(self, node):
        right = Node1()
        right.values.add(node.values.pop(2))
        right.set_parent(node)
        parent_value = node.values.pop(1)
        left = Node1()
        left.values.add(node.values.pop(0))
        left.set_parent(node)

        if not node.parent.values.add(parent_value):
            node_ = self.__balance(node.parent)
            return node_
        return node


    def add(self, node, value):
        # if node is None:
        #     node = Node1()
        #     node.values.add(Value(value))
        # don't have children
        if len(node.children.array) == 0:
            if not node.values.add(Value(value)): # create children
                node = self.__balance(node)
        # have children
        elif node.values.smaller(value):
            self.add(node.children.array[0], value)
        elif node.values.greater(value):
            self.add(node.children.array[node.children.max_index()], value)
        else:
            if node.values.add(Value(value)):

        return node
class Node:
    def __init__(self, parent, value):
        self.node_left = Value(value)
        self.node_right = None
        self.node_central = None
        self.value_left = None
        self.value_right = None
        self.value_central = None  # ?
        self.parent = parent

class Node1:
    def __init__(self):
        self.parent = None
        self.children = SortArray(4, Node1, count=False)
        self.values = SortArray(3, Value, count=True)

    def set_parent(self, parent):
        self.parent = parent
        parent.children.add(self)

    def __gt__(self, other):
        if len(self.values.array) > 0 and len(other.values.array) > 0:
            return self.values.array[0] > other.values.array[len(other.values.array) - 1]
        else:
            return True

    def __lt__(self, other):
        if len(self.values.array) > 0 and len(other.values.array) > 0:
            return self.values.array[len(self.values.array) - 1] < other.values.array[0]
        else:
            return True

class SortArray:
    def __init__(self, max_capacity, clazz, count):
        self.max_capacity = max_capacity
        self.array = []
        self.clazz = clazz
        self.count = count

    # returns false when is full - signal to rearrange
    def add(self, element):
        if type(self.clazz) == type(element):
            if self.count:
                res = list(map(lambda x: x.instance == element, self.array))
                index = res.index(True) if res.count(True) > 0 else False
                if index:
                    self.array.append(Counter(element))
                flag = False
                for el in self.array:
                    if el.instance == element:
                        el.occurrences = el.occurrences + 1
                        flag = True
                        break
                if not flag:

            else:
                self.array.append(element)
            self.array.sort()
            return not len(self.array) == self.max_capacity
        else:
            raise "Attempting to add instance of type " + str(type(element)) + " to collection of type " + str(type(self.clazz))

    def pop(self, index):
        if index < len(self.array):
            return self.array.pop(index)

    def smaller(self, value):
        return len(self.array) > 0 and value < self.array[0]

    def greater(self, value):
        return len(self.array) > 0 and value > self.array[len(self.array) - 1]

    def max_index(self):
        return len(self.array) - 1

class Counter:
    def __init__(self, instance):
        self.instance = instance
        self.occurrences = 1

    def __gt__(self, other):
        return self.instance > other.instance

    def __lt__(self, other):
        return self.instance < self.instance

    def __eq__(self, other):
        return self.instance == self.instance

class Value:
    def __init__(self, value):
        self.value = value
        self.occurrences = 1

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other

    def __eq__(self, other):
        return self.value == other.value

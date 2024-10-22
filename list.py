from value_store import ValueStore
import numpy as np


def neighbour_weights(value1, value2, val_range):
    if type(value1) == float and type(value2) == float:
        return 1 - abs(value1 - value2) / val_range
    elif type(value1) == str and type(value2) == str:
        return 1. if value1 == value2 else 0.


class List(ValueStore):
    def __init__(self, granulation=1):
        self.node_list = []
        self.connection_weight = []
        self.change = False
        self.granulation = granulation
        self.value_range = 0
        self.length = 0

    def create_node(self, value, index) -> bool:
        self.change = False
        value = round(value, self.granulation) if type(value) == float else value
        self.node_list = list(map(lambda x: self.__update(x, value, index), self.node_list))
        if not self.change:
            val = Value(value)
            val.references.append(index)
            self.node_list.append(val)
            return True
        else:
            return False

    def compile(self):
        # convert prepared list to numpy array so it will be faster
        self.node_list.sort()
        # self.node_list = np.asarray(self.node_list).sort()
        if type(self.node_list[0].value) == float:
            self.value_range = self.node_list[len(self.node_list) - 1].value - self.node_list[0].value
        self.length = len(self.node_list)
        # debug
        # print("Sorted list: ", self.node_list)
        # print("Range of values: ", self.value_range)

    # todo vectorization
    def find_value_for_ref(self, index):
        for val in self.node_list:
            if index in val.references:
                return val.value

        return None

    def neighbour_weight(self, value):
        val = Value(value)
        return [neighbour_weights(x.value, value, self.value_range) for x in self.node_list]

    def __update(self, node, value, reference):
        if node.value == value:
            node.occurrences = node.occurrences + 1
            node.references.append(reference)
            self.change = True
        return node


class Value:
    def __init__(self, value):
        self.value = value
        self.occurrences = 1
        self.references = []

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __str__(self):
        return 'val: ' + str(self.value) + ' occ: ' + str(self.occurrences) + ' ref: ' + str(self.references)


class Instance:
    def __init__(self, index, connection_weight):
        self.index = index
        # 1 / len(value.references)
        self.connection_weight = connection_weight  # 1 / (occurrences of specified value in all objects)

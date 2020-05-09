from value_store import ValueStore
import numpy as np



class List(ValueStore):
    def __init__(self):
        self.node_list = []
        self.connection_weight = []
        self.change = False

    def add(self, element) -> bool:
        self.node_list.append(element)
        return True

    def create_node(self, value, index) -> bool:
        print(self.node_list)
        is_present = list(filter(lambda x: x.value == value, self.node_list))
        if len(is_present) == 0:
            val = Value(value)
            val.references.append(index)
            self.node_list.append(val)
            return True
        else:
            # debug
            print('Node with specified value exists and has length of: ', len(is_present))
            print('Typeof element: ', type(is_present[0]))
            self.node_list = list(map(lambda x: self.update(x, value, index), self.node_list))
            return False

    def update(self, node, value, reference):
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


class Instance:
    def __init__(self):
        self.index = None
        # 1 / len(value.references)
        self.connection_weight = 0  # 1 / (occurrences of specified value in all objects)

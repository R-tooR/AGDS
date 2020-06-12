from list import *
import numpy as np
import time

class AGDS:
    def __init__(self, data_frame):
        self.categories = {}
        self.dataset_len = len(data_frame[:])
        for attr in data_frame:
            i = 0
            self.categories[attr] = List(1)
            for v in data_frame[attr]:
                self.categories[attr].create_node(v, i)
                i = i + 1

            self.categories[attr].compile()
        self.conn_weight = 1/len(data_frame.keys())

    def calculate_for_index(self, index, sim_threshold=0.97):
        instances = np.zeros(self.dataset_len)
        for attr in self.categories.keys():
            res = self.categories[attr].find_value_for_ref(index)
            weig = self.categories[attr].neighbour_weight(res)
            nodes = self.categories[attr].node_list
            for i in range(0, self.categories[attr].length):
                instances[nodes[i].references] = instances[nodes[i].references] + weig[i]*self.conn_weight

        return instances, np.nonzero(instances > sim_threshold)

    def calculate_for_instance(self, instance, sim_threshold=0.9):
        instances = np.zeros(self.dataset_len)
        index = 0

        for attr in self.categories.keys():
            weig = self.categories[attr].neighbour_weight(instance[index])
            nodes = self.categories[attr].node_list
            for i in range(0, self.categories[attr].length):
                instances[nodes[i].references] = instances[nodes[i].references] + weig[i]*self.conn_weight
            index = index + 1

        return instances, np.nonzero(instances > sim_threshold)

    def get_graph(self, min_similarity, sim_table=None):
        start_time = time.time()
        attrs = {}
        start_x = 10
        start_y = 10
        layer_x = 300
        next_x = start_x
        layer_y = 300
        next_y = layer_y
        scale = 10
        step_value_node = 3
        step_instance_node = 3
        axis = 0
        instances = []
        edges = []
        pred_len_inst = self.dataset_len*step_instance_node*scale
        pred_len_attr = sum([self.categories[x].get_len()*step_value_node*scale + 100 for x in self.categories])
        mar_inst = (pred_len_attr - pred_len_inst)/2 if pred_len_attr - pred_len_inst > 0 else 0
        mar_val = (pred_len_inst - pred_len_attr)/2 if pred_len_inst - pred_len_attr > 0 else 0
        next_x = next_x + mar_inst
        for i in range(self.dataset_len):
            instances.append({'pos': [next_x, next_y]})
            next_x = next_x + step_instance_node*scale if axis == 0 else next_x
            next_y = next_y + step_instance_node*scale if axis == 1 else next_y

        next_x = start_x + mar_val
        next_y = start_y

        for attr in self.categories.keys():
            attrs[attr], next_x, next_y = self.categories[attr].get_subgraph(next_x, next_y, step_value_node, scale, axis)
            for value in attrs[attr]:
                for ref in value['value'].references:
                    if sim_table[ref] >= min_similarity:
                        edges.append({'start': (value['pos'][0], instances[ref]['pos'][0]),
                                      'end': (value['pos'][1], instances[ref]['pos'][1])})

            next_x = next_x + 100
        for i in range(self.dataset_len-1, -1, -1):
            if sim_table[i] < min_similarity:
                instances.pop(i)

        print("--- get_graph execution: %s seconds ---" % (time.time() - start_time))
        return attrs, instances, edges





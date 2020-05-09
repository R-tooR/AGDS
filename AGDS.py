from list import *
import numpy as np


class AGDS:
    def __init__(self, data_frame):
        self.categories = {}
        self.dataset_len = len(data_frame[:])
        # print('Dataset len: ', self.dataset_len)
        self.instances = np.zeros(self.dataset_len)
        for attr in data_frame:
            i = 0
            self.categories[attr] = List(1)
            # todo: vectorization
            for v in data_frame[attr]:
                self.categories[attr].create_node(v, i)
                i = i + 1
                # self.categories[attr].create_node(v, data_frame[attr].iloc[v])

            self.categories[attr].compile()
        self.conn_weight = 1/len(data_frame.keys())
        # print("Dataset: ", self.dataset_len)

    def calculate(self, index):
        for attr in self.categories.keys():
            print('Key: ', attr)
            print('Values: ', self.categories[attr])
            res = self.categories[attr].find_value_for_ref(index)
            weig = self.categories[attr].neighbour_weight(res)
            print(' WEI: ', weig)
            # for i in range(0, len(vals)):
            #     self.instances[vals[i].references] = self.instances[vals[i].references] + weig[i]*self.conn_weight
            #     # print("After adding: ", self.instances)
            nodes = self.categories[attr].node_list
            for i in range(0, self.categories[attr].length):
                self.instances[nodes[i].references] = self.instances[nodes[i].references] + weig[i]*self.conn_weight
                # print("After adding: ", self.instances)

        return self.instances, np.nonzero(self.instances > 0.97)





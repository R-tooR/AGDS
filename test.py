from AGDS import *
import pandas as pd
from pathlib import Path

values = [1, 2, 3, 4, 1, 2, 3, 5, 7]

l = List()
res = []
for i in range(0, 9):
    res.append(l.create_node(values[i], i))

print('Expected: [True, True, True, True, False, False, False, True, True]')
print('Actual: ', res)


print('val: 1 occ: 2 ref: [0, 4]')
print('val: 2 occ: 2 ref: [1, 5]')
print('val: 3 occ: 2 ref: [2, 6]')
print('val: 4 occ: 1 ref: [3]')
print('val: 5 occ: 1 ref: [7]')
print('val: 7 occ: 1 ref: [8]')

for node in l.node_list:
    print('val: ', node.value, 'occ: ', node.occurrences, 'ref: ', node.references)

values = [1.12, 2.47, 3.19, 4.07, 1.11, 2.35, 3.16, 5.55, 7.77]

l = List(1)
res = []
for i in range(0, 9):
    res.append(l.create_node(values[i], i))

# print('Expected: [True, True, True, True, False, False, False, True, True]')
# print('Actual: ', res)
#
#
# print('val: 1.1 occ: 2 ref: [0, 4]')
# print('val: 2 occ: 2 ref: [1, 5]')
# print('val: 3 occ: 2 ref: [2, 6]')
# print('val: 4 occ: 1 ref: [3]')
# print('val: 5 occ: 1 ref: [7]')
# print('val: 7 occ: 1 ref: [8]')

for node in l.node_list:
    # print('val: ', node.value, 'occ: ', node.occurrences, 'ref: ', node.references)
    print(node)

l.compile()
print(l.neighbour_weight(2.5))

df = pd.read_excel(Path('~/irisData.xls'), header=None, index_col=None)

agds = AGDS(df)

res = agds.calculate(7)

print(res)

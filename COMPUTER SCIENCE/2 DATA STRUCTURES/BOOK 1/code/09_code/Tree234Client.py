# Automated tests of the Treeￚ2ￚ3ￚ4 class

import sys
import Tree234
class Tree234(Tree234.Tree234):
   def height(self):           # Get the maximum level of any node
      return self.__height(self.__root) # Return -1 for no nodes

   def __height(self, node):
      return -1 if node is None else 0 if node.isLeaf() else (
         1 + self.__height(node.children[0]))

theTree = Tree234()

print('Created an empty 2-3-4 tree of height', theTree.height())
theTree.print()

keys = [
   int(a) if a.isdigit() else a for a in sys.argv[1:]
] if len(sys.argv) > 1 else [
   44, 27, 33, 65, 57, 49, 55, 83, 71, 86, 27, 52, 38, 40, 42, 78, 75, 74
]
print('Inserting', len(keys), 'key(s) in the following order:\n', keys)
order = 1
lastHeight = theTree.height()
for i, key in enumerate(keys):
   duplicate = key in keys[:i]
   if not theTree.insert(key, order):
      print('Insert of key', key, 'with data', order,
            'keys updated an existing key',
            'as expected' if duplicate else 'unexpectedly')
   if theTree.height() != lastHeight:
      lastHeight = theTree.height()
      print('Inserting key', key, 'after inserting', i,
            'other key(s) caused height to change to', lastHeight)
   order += 1

print('After inserting', len(keys), 'keys the 2-3-4 tree has height',
      theTree.height(), 'and contains:')
theTree.print()
root_data, root_keys = theTree.root()
print('The tree root node has keys:', root_keys, 'and data:', root_data)

goals = keys[:len(keys) // 2] + [39 if isinstance(keys[0], int) else '39']
for goal in goals:
   inTree = goal in keys
   found = theTree.search(goal)
   print('Searching for', goal, 'returns', found,
         'as expected' if (isinstance(found, int) if inTree else found is None)
         else 'unexpectedly')

print('Reinserting the same', len(keys), 'keys into the tree...')
for i, key in enumerate(keys):
   if theTree.insert(key, order):
      print('Reinserting key', key, 'with data', order,
            'unexpectedly added a new key to the tree')
   if theTree.height() != lastHeight:
      lastHeight = theTree.height()
      print('Reinserting key', key, 'with value', order, 'after inserting', i,
            'other key(s) caused height to change to', lastHeight)
   order += 1
print('Leaves tree with height', theTree.height(), 'and containing:')
theTree.print()
root_data, root_keys = theTree.root()
print('The tree root node has keys:', root_keys, 'and data:', root_data)

for order in ['pre', 'in', 'post']:
   print('Traversing the tree using', order, 'order')
   for key, data in theTree.traverse(order):
      print('{' + str(key) + ', ' + str(data) + '}', end=' ')
   print()

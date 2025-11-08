# Automated tests of the BinarySearchTree class

from BinarySearchTree import *
import sys

theTree = BinarySearchTree()
print('Created an empty binary search')

keys = [44, 27, 33, 65, 57, 49, 55, 83, 71, 86, 27]
if len(sys.argv) > 1:         # Use command line args if present
   keys = [int(a) for a in sys.argv[1:]]

count = 0
for key in keys:
   print('Inserting key', key, 'in tree returns', 
         theTree.insert(key, count))
   count += 1

print('Created a binary search tree with', theTree.nodes(), 'nodes across',
      theTree.levels(), 'levels')
theTree.print()
root_data, root_key = theTree.root()
print('The tree root node has key:', root_key, 'and data:', root_data)

dkeys = [keys[i] for i in range(0, len(keys), 3)] + [37, 40]
for key in dkeys:
   print('Searching for', key, 'returns', theTree.search(key))

for key in dkeys:
   print('Deleting', key, 'returns', theTree.delete(key))

print('The binary search tree now contains',
      theTree.nodes(), 'nodes across', theTree.levels(), 'levels')
theTree.print()
root_data, root_key = theTree.root()
print('The tree root node has key:', root_key, 'and data:', root_data)
min_key, min_data = theTree.minNode()
print('The minimum key is', min_key, 'with data', min_data)
max_key, max_data = theTree.maxNode()
print('The maximum key is', max_key, 'with data', max_data)

print('Testing the recursive in-order traversal using print function')
theTree.inOrderTraverse()

for func in (theTree.traverse_rec, theTree.traverse):
   print('Using {}recursive traversal generator'.format(
      '' if func == theTree.traverse_rec else 'non-'))
   for order in ['pre', 'in', 'post']:
      print(' Traversing the tree using', order, 'order')
      for key, data in func(order):
         print(' {' + str(key) + ', ' + str(data) + '}', end='')
      print()
   print(' Checking for exception for unknown traversal type')
   try:
      for item in func('bad order'):
         print(' Somehow traversal in "bad order" produced:', item)
   except ValueError as e:
      print(' Received expected value error:', e)

from random import *
random_tree = BinarySearchTree()
seed(3.14159)
for key, data in theTree.traverse('pre'):
   random_tree.insert(key, randrange(1000))
print('A tree with the same keys but random data:')
random_tree.print(indentBy=2)

total, count = 0, 0
for key, data in random_tree.traverse('pre'):
   total += data
   count += 1
average = total / count
below_average = []
for key, data in random_tree.traverse('in'):
   if data <= average:
      below_average.append((key, data))
print('Tree items with below average', average, 'data are:', 
      below_average)
below_average2 = [
   (key, data) for key, data in random_tree.traverse('in')
   if data <= average]
print('list comprehension does', 
      '' if below_average == below_average2 else 'not',
      'agree')

from AVLtree import *
import sys

t = AVLtree()

keys = [10, 7, 12, 3, 9, 6, 7] # Default keys

if len(sys.argv) > 1:         # Use command line args if present
   keys = [int(a) for a in sys.argv[1:]]

count = 0
for key in keys:
   print('Inserting', key, 'returns', t.insert(key, count))
   count += 1
   print('After inserting', key, ':', count,
         'the tree contains')
   t.print()

print('Traversing the tree in-order:')
for key, val in t.traverse('in'):
   print('Key', key, 'has value', val)

for key in keys:
   delFlag = t.delete(key)
   print('Deleting', key, 'returns', delFlag)
   if delFlag:
      print('After deleting', key, ':',
            'the tree contains')
      t.print()

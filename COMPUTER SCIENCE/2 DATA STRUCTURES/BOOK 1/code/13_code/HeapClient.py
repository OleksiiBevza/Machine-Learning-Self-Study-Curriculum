from Heap import *
import sys, random

def first(x): return x[0]

heap = Heap(key=first)

keys = [10, 7, 12, 3, 9, 6, 7, 11] # Default keys

if len(sys.argv) > 1:         # Use command line args if present
   keys = [int(''.join(c for c in arg if c.isdigit())) for arg in sys.argv[1:]]
   seed = sum(keys)
else:
   seed = 3.14159
random.seed(seed)
maxValue = 100
nValues = 100
nExtract = int(nValues * 0.2)
keys_for_highest = [random.randrange(maxValue) for i in range(nValues)]

for count, key in enumerate(keys):
   heap.insert((key, count))
   print('After inserting', key, ':', count, 'the heap contains')
   heap.print()

for i in range(len(heap)):
   print('Removing item #', i + 1, 'returns', heap.remove())
   print('Remaining heap:', heap)

print('After removing all items the heap contains:', heap)

pq = PriorityQueue(priority=first)
for count, key in enumerate(keys):
   pq.insert((key, count))

print('After inserting', len(keys),
      'in a priorty queue, it displays as', pq)
print('The underlying heap tree is:')
pq.print()
print('Traversing the items of the tree in breadth first order:')
for item in pq.traverse():
   print(item)

keys_copy = [x for x in keys]  # Copy of the keys array
print('Keys in array before calling heapsort:')
print(keys_copy)
heapsort(keys_copy)
print('Keys in array after calling heapsort:')
print(keys_copy)

print('Keys to use for test of highest:', keys_for_highest)
print('Result of extracting the', nExtract, 'highest among', nValues,
      'keys is', highest(nExtract, keys_for_highest, nValues))
print('Leaving the input array as:', keys_for_highest)

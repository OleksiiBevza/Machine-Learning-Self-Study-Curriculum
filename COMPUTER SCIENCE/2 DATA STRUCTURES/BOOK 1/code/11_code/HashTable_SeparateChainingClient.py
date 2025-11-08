from HashTable_SeparateChaining import *
from collections import *

# Allocate a hash table
hTable = HashTable()

testKeys = [x for x in range(0, 500, 5)]
sizes = []
size = hTable.cells()
while size < len(testKeys) * 2:
   if is_prime(size):
      sizes.append(size)
      size += size + 1
   else:
      size += 2
print('Expected hash table sizes:', sizes)
size = sizes[-1]
collisions = [i * size + 1 for i in range(3)] + [
   i * size - 5 for i in range(3)]
print('Adding test keys designed to cause collisions:',
      collisions)
testKeys += collisions

printAt = [1, 47]

print('Inserting', len(testKeys), 
      'keys into separate chaining hash table')
for key in testKeys:
   hTable.insert(key, key)
   if len(hTable) in printAt:
      print('After inserting', len(hTable), 
            'keys, the hash table contains\n', hTable)

print('Completed hash table:\n', hTable)
print(sum(1 if hTable.search(key) == key else 0 for
          key in testKeys),
      'keys found out of', len(hTable))
otherKey = (testKeys[0] + testKeys[1]) // 2
print('Search for', otherKey, 'returns', hTable.search(otherKey))
try:
   print('Attempting to delete', otherKey)
   hTable.delete(otherKey)
   print('Does not cause an exception!')
except Exception as e:
   print('{}orrectly causes the exception "{}"'.format(
      'C' if 'not found in hash table' in str(e) else 'Inc',
      e))
key = testKeys[len(testKeys) // 2]
print('Updating value of key', key, 'returns',
      hTable.insert(key, key + key))
print('Updated value of key', key, 'is', hTable.search(key),
      'and should be', key + key)
print('Deleting key', key, 'returns', hTable.delete(key))
print('Re-inserting', key + key, 'as value of key', key, 'returns',
      hTable.insert(key, key + key), 
      'and hashes to cell', hTable.hash(key), 'of', hTable.cells())

print('Traversing the hash table produces:')
count = 0
for key, value in hTable.traverse():
   print(' {}: {},'.format(repr(key), repr(value)),
         end='\n' if count % 5 == 4 else '')
   count += 1
print()

treeSizes = defaultdict(lambda: 0)
for i in range(hTable.cells()):
   cell = hTable.peek(i)
   treeSizes[cell if cell is None else sum(1 for x in cell.traverse())] += 1
for key in treeSizes:
   print('There are', treeSizes[key],
         'empty cells' if key is None else 'trees of size {}'.format(key))

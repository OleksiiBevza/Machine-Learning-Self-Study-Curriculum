from HashTable_OpenAddressing import *
from Hashing import *

# Allocate tables of each type
linearHashTable = HashTable(probe=linearProbe)
quadraticHashTable = HashTable(probe=quadraticProbe)
doubleHashTable = HashTable(probe=doubleHashProbe)
hashTables = [(linearHashTable, 'linear'),
              (quadraticHashTable, 'quadratic'),
              (doubleHashTable, 'double hash')]

testKeys = [x for x in range(0, 500, 5)]
size = linearHashTable.cells()
sizes = []
while size < len(testKeys) * 4:
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

for hashTable, tableName in hashTables:
   print('=' * 78)
   print('Inserting', len(testKeys), 'into', tableName,
         'open addressing hash table')
   for key in testKeys:
      hashTable.insert(key, key)
      if len(hashTable) in printAt:
         print('After inserting', len(hashTable), 
               'keys, the hash table contains\n', hashTable)

   print('Completed hash table:\n', hashTable)
   print(sum(1 if hashTable.search(key) == key else 0 for
             key in testKeys),
         'keys found out of', len(hashTable))
   otherKey = (testKeys[0] + testKeys[1]) // 2
   print('Search for', otherKey, 'returns', hashTable.search(otherKey))
   try:
      print('Attempting to delete', otherKey)
      hashTable.delete(otherKey)
      print('Does not cause an exception!')
   except Exception as e:
      print('{}orrectly causes the exception "{}"'.format(
         'C' if 'not found in hash table' in str(e) else 'Inc',
         e))
   key = testKeys[len(testKeys) // 2]
   print('Updating value of key', key, 'returns',
         hashTable.insert(key, key + key))
   print('Updated value of key', key, 'is', hashTable.search(key),
         'and should be', key + key)
   print('Deleting key', key, 'returns', hashTable.delete(key))
   print('Re-inserting', key + key, 'as value of key', key, 'returns',
         hashTable.insert(key, key + key))

# Show details of building up a hash table using double hashing
hTable = HashTable(probe=doubleHashProbe)
rowFormat = '{:4d} {:3d}{} {:11d} {:4d} {:5d} {:5d} | {}'
colHeader = rowFormat.replace('d', 's')
keys = [1, 38, 37, 16, 20, 3, 11, 24, 4, 16, 10, 31,
        18, 12, 30, 1, 19, 85, 41, 15, 25]
print('=' * 78)
print('Inserting', len(keys), 'items with', len(set(keys)),
      'unique keys in a double hashing hash table')
print(colHeader.format('Item', 'Key', ' ', 'Simple hash', 'Step', 
                       'Cells', 'Prime', 'Probe Sequence'))
for i, key in enumerate(keys):
   start = hTable.hash(key)
   cells =  hTable.cells()
   prime = primeBelow(cells)
   if (len(hTable) + 1) / cells > 0.5:
      print('Before growing table to insert', key, ', it contains:\n',
            hTable.tableString())
   visited = []
   for j in doubleHashProbe(start, key, cells):
      visited.append(j)
      cell = hTable.peek(j)
      if cell is None or cell[0] is None or cell[0] == key:
         break
   dupe = hTable.search(key) is not None
   print(rowFormat.format(
      i + 1, key, '*' if dupe else ' ', start, doubleHashStep(key, cells),
      cells, prime, ', '.join([str(i) for i in visited][1:])))
   hTable.insert(key, i + 1)
print('Final hash table contains:\n', hTable.tableString())
print('Traversing the hash table produces:')
count = 0
for key, value in hTable.traverse():
   print(' {}: {},'.format(repr(key), repr(value)),
         end='\n' if count % 5 == 4 else '')
   count += 1
print()
toDelete = keys[len(keys) // 2]
print('Deleting key', toDelete, 'returns', hTable.delete(toDelete))
print('Traversing the modified hash table produces:')
count = 0
for key, value in hTable.traverse():
   print(' {}: {},'.format(repr(key), repr(value)),
         end='\n' if count % 5 == 4 else '')
   count += 1
print()
   

from DoublyLinkedList import *

dlist = DoublyLinkedList()

for data in [(1968, 'Richard'), (1967, 'Maurice'), (1966, 'Alan')]:
   dlist.insertFirst(data)
for data in [(2015, 'Whitfield'), (2015, 'Martin'), 
             (2016, 'Tim'), 
             (2017, 'David'), (2017, 'John')]:
   dlist.insertLast(data)
print('After inserting', len(dlist), 
      'entries into the doubly linked list, it contains:\n', dlist, 
      'and empty =', dlist.isEmpty())

print('Traversing backwards through the list:')
dlist.traverseBackwards()

print('Deleting first entry returns:', dlist.deleteFirst())
print('Deleting last entry returns:', dlist.deleteLast())
def year(x): return x[0]
for date in [1967, 2015]:
   print('Deleting entry with key', date, 'returns', 
         dlist.delete(date, key=year))
print('List after deletions contains:', dlist)

for date in [1968, 2015]:
   data = (date + 1, '?')
   print('Inserting', data, 'after', date, 'returns',
         dlist.insertAfter(date, data, key=year))
print('List after insertions contains:', dlist)

print('Traversing backwards through the list:')
dlist.traverseBackwards()

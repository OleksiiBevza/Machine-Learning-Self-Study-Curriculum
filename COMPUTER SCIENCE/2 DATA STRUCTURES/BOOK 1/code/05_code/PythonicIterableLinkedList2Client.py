from PythonicIterableLinkedList2 import *

llist = LinkedList()

print('Initial list has', len(llist), 'element(s) and empty =', 
      llist.isEmpty())

print('Creating an iterator')
for item in llist:
   print('The next item is:', item)
print('End of iterator')

for person in ['Don', 'Ken', 'Ivan', 'Raj', 'Amir', 'Adi']:
   llist.insert(person)

print('After inserting', len(llist), 
      'persons into the linked list, it contains:\n', llist, 
      'and empty =', llist.isEmpty())

print('Creating an iterator')
for item in llist:
   print('The next item is:', item)
print('End of iterator')

print('Removing items from the linked list:')
for person in ['Ken', 'Ivan', 'Amir', 'Don', 'Adi', 'Raj']:
   llist.delete(person)
   print('After deleting', person, 'the list is', llist)


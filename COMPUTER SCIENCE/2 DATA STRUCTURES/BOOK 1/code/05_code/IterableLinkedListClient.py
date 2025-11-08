from IterableLinkedList import *

llist = LinkedList()

print('Initial list has', len(llist), 'element(s) and empty =', 
      llist.isEmpty())

it = llist.iterator()
print('Created an iterator', it)
while it.hasMore():
   print('The next item is:', it.next())
print('End of iterator')

people = ['Don', 'Ken', 'Ivan', 'Raj', 'Amir', 'Adi']
for person in people:
   llist.insert(person)

print('After inserting', len(llist), 
      'persons into the linked list, it contains:\n', llist, 
      'and empty =', llist.isEmpty())

it = llist.iterator()
print('Created an iterator', it)
try:
   while True:
      print('The next item is:', it.next())
except StopIteration:
   print('End of iterator')

print('Removing items from the linked list in different order:')
for person in people[3:] + people[:3]:
   llist.delete(person)
   print('After deleting', person, 'the list is', llist)

print('Test with complex data type')
def second(x):
   return x[1]

llist = LinkedList()
after = None
for i, person in enumerate(people):
   datum = (i * i, person)
   if after:
      llist.insertAfter(after, datum, key=second)
   else:
      llist.insert(datum)
      after = second(datum)

print('After inserting', len(llist) - 1, 
      'persons into the linked list after,', after, 
      'it contains:')
llist.traverse()

print('Removing items from the linked list in different order:')
for person in people[3:] + people[:3]:
   llist.delete(person, key=second)
   print('After deleting', person, 'the list is', llist)

print('Removing from an empty linked list should raise an exception ...')
try:
   llist.delete('non-existant')
   print('This should not be printed! Empty list allowed delete!')
except Exception as e:
   print('Exception was raised:\n', e)



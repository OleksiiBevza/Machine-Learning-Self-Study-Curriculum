from LinkedList import *

llist = LinkedList()

print('Initial list has', len(llist), 'element(s) and empty =', 
      llist.isEmpty())

people = ['Don', 'Ken', 'Ivan', 'Raj', 'Amir', 'Adi']
for person in people:
   llist.insert(person)

print('After inserting', len(llist), 
      'persons into the linked list, it contains:\n', llist, 
      'and empty =', llist.isEmpty())

first = llist.deleteFirst()
print('First item in the list is', first, 'and has been deleted')

mid = people[len(people) // 2]
print('Removing items by key from the linked list:')
llist.delete(mid)
print('After deleting', mid, 'the list is', llist)
for person in [p for p in people if p not in (first, mid)]:
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

print('Removing items by key from the linked list:')
for person in people:
   llist.delete(person, key=second)
   print('After deleting', person, 'the list is', llist)

print('Removing from an empty linked list should raise an exception ...')
try:
   llist.delete('non-existant')
   print('This should not be printed! Empty list allowed delete!')
except Exception as e:
   print('Exception was raised:\n', e)

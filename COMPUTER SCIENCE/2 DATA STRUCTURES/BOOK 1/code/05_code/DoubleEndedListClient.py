from DoubleEndedList import *

def second(x): return x[1]

dlist = DoubleEndedList()

print('Initial list has', len(dlist), 'element(s) and empty =', 
      dlist.isEmpty())
after = None
people = ['Raj', 'Amir', 'Adi', 'Don', 'Ken', 'Ivan']
for i, person in enumerate(people):
   if after:
      dlist.insertAfter(after, (i * i, person), key=second)
   else:
      dlist.insert((i * i, person))
      after = person

print('After inserting', len(dlist) - 1, 
      'persons into the linked list after', after, 'it contains:')
dlist.traverse()
print('First:', dlist.first(), 'and Last:', dlist.last())

next = (404, 'Tim')
dlist.insertLast(next)
print('After inserting', next, 'at the end, the double-ended list',
      'contains:\n', dlist)

dlist.insert(next)
print('After inserting', next, 'at the front, the double-ended list',
      'contains:\n', dlist)
print('Deleting the first item returns', dlist.deleteFirst(), 
      'and leaves the double-ended list containing:\n', dlist,
      'with first:', dlist.first(), 'and Last:', dlist.last())
print('Deleting the last item returns', 
      dlist.delete(second(dlist.last()), key=second), 
      'and leaves the double-ended list containing:\n', dlist,
      'with first:', dlist.first(), 'and Last:', dlist.last())

print('Removing some items from the linked list by key:')
for person in people[0:5:2]:
   dlist.delete(person, key=second)
   print('After deleting', person, 'the list is', dlist)
   if not dlist.isEmpty():
      print('The last item is', dlist.last())

print('Removing remaining items from the front of the linked list:')
while not dlist.isEmpty():
   print('After deleting', dlist.deleteFirst(), 'the list is', dlist)
   if not dlist.isEmpty():
      print('The last item is', dlist.last())

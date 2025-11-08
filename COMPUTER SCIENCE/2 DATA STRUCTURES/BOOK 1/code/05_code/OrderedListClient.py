from OrderedList import *

olist = OrderedList()
print('Initial list has', len(olist), 'element(s) and empty =', 
      olist.isEmpty())

for i in range(5):
   olist.insert((-1 - i) ** i) # Produces 1, -2, 9, -64, 625
print('After inserting', len(olist), 
      'numbers into the ordered list, it contains:\n', olist, 
      'and empty =', olist.isEmpty())

for value in [9, 999]:
   for sign in [-1, 1]:
      val = sign * value
      print('Trying to find', val, 'in ordered list returns',
            olist.find(val), ', search returns', olist.search(val))

print('Deleting items from the ordered list:')
for i in range(5):
   number = (-1 - i) ** i
   print('After deleting', olist.delete(number),
         'the list is', olist)


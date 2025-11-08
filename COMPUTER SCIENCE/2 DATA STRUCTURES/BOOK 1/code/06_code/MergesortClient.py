from Mergesort import *
from Array import *

values = [19, 49, 70, 72, 43, 80, 95, 46, 19, 18, 45, 6, 56, 85]
array = Array(len(values))
for value in values:
   array.insert(value)

print('Initial array contains', len(array), 'items')
array.traverse()

Mergesort(array)  

print('After applying Mergesort, array contains', len(array), 'items')
array.traverse()


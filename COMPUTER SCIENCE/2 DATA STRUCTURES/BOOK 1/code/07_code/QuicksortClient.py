from Quicksort import *
import random
import timeit
import math

def initArray(size=100, maxValue=100, seed=3.14159):
   """Create an Array of the specified size with a fixed sequence of
       'random' elements"""
   arr = Array(size)                   # Create the Array object
   random.seed(seed)                   # Set random number generator
   for i in range(size):               # to known state, then loop
      arr.insert(random.randrange(maxValue)) # Insert random numbers
   return arr                          # Return the filled Array

for size in [0, 1, 2, 3, 10]:
   arr = initArray(size)
   for pivot in [0] if size < 2 else [
         -1, arr.get(size // 2 - 1), arr.get(size // 2), 101]:
      print("Initialized array contains", arr)
      part_index = arr.partition(pivot)
      print("Partitioning an array of size", size, "around", pivot,
            "returns", part_index)
      print(" " * (28 + 4 * part_index) + "V")
      print("Partitioned array contains", arr)

arr = initArray(10)
print('Quicksorting', arr, ':')
arr.qsort_show()

arr = Array(12)
for i in [73, 80, 16, 47, 65, 88, 95, 31, 10, 24, 39, 56]:
   arr.insert(i)
print('Quicksorting', arr, ':')
arr.qsort_show()

arr = initArray()
print("Array containing", len(arr), "items:\n", arr)

test = 'initArray().quicksort()'
elapsed = timeit.timeit(test, number=100, globals=globals())
print(test, "took", elapsed, "seconds", flush=True)

arr.quicksort()
print('Sorted array contains:\n', arr)

print('Camparsion of quicksorting and inertion sorting speed')
print('Items Quicksort  N*logN  Ratio     | Insertion  N**2    Ratio')
for size in [50, 100, 200, 500, 1000]:
   q_test = 'initArray(size).quicksort()'
   q_elapsed = timeit.timeit(q_test, number=10, globals=globals())
   nlogn = size * math.log(size, 2)
   n2 = size * size
   i_test = 'initArray(size).insertionSort()'
   i_elapsed = timeit.timeit(i_test, number=10, globals=globals())
   print('{:5,d} {:5.3f} secs {:6.1e} {:6.3e} | {:5.3f} secs {:6.1e} {:6.3e}'
         .format(size, q_elapsed, nlogn, nlogn / q_elapsed,
                 i_elapsed, n2, n2 / i_elapsed))

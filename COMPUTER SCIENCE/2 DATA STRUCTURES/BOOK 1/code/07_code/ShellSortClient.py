from ShellSort import *
import random
import timeit

def initArray(size=100, maxValue=100, seed=3.14159):
    """Create an Array of the specified size with a fixed sequence of
       'random' elements"""
    arr = Array(size)                   # Create the Array object
    random.seed(seed)                   # Set random number generator
    for i in range(size):               # to known state, then loop
        arr.insert(random.randrange(maxValue)) # Insert random numbers
    return arr                          # Return the filled Array

arr = initArray()
print("Array containing", len(arr), "items:\n", arr)

test = 'initArray().ShellSort()'
elapsed = timeit.timeit(test, number=100, globals=globals())
print(test, "took", elapsed, "seconds", flush=True)

shifts = arr.ShellSort()
print('Sorted array contains:\n', arr, 'and took', shifts, 'cell shifts')

for size in [100, 200, 500, 1000, 2000, 5000]:
    shifts = initArray(size).ShellSort()
    pwr = 7/6
    print('Sorting an array of {:5,d} items took {:6,d} shifts, '
          'ratio to N**({:5.3f}) = {:6.3f}'
          .format(size, shifts, pwr, shifts / size ** pwr))


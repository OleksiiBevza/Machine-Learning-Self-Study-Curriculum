# Implement the mergesort algorithm on arrays

def identity(x): return x        # Identity function

from Array import *

class Mergesort(object):         # An object to mergesort Arrays
   def __init__(self,            # Constructor takes the unordered
                unordered,       # array and orders its items by using
                key=identity):   # mergesort on their keys
      self.__arr = unordered     # Array starts unordered 
      self.__key = key           # Key func. returns sort key of item
      n = len(unordered)         # Get number of items
      self.__work = Array(n)     # A work array of the same length
      for i in range(n):         # is needed to rearrange the items
         self.__work.insert(None) # Work array is filled with None
      self.mergesort(0, n)       # Call recursive sort on full array

   def mergesort(self, lo, hi):  # Perform mergesort on subrange
      if lo + 1 >= hi:           # If subrange has 1 or fewer items,
         return                  # then it is already sorted
      mid = (lo + hi) // 2       # Otherwise, find middle index
      self.mergesort(lo, mid)    # Sort the lower half of subrange,
      self.mergesort(mid, hi)    # Sort the upper half of subrange,
      self.merge(lo, mid, hi)    # Merge the 2 sorted halves

   def merge(self, lo, mid, hi): # Merge 2 sorted subranges of array
      n = 0                      # into work array which starts empty
      idxLo = lo                 # Use indices into lo and hi
      idxHi = mid                # subranges to track next items
      while (idxLo < mid and     # Loop until one of the subranges
             idxHi < hi):        # is empty
         itemLo = self.__arr.get(idxLo) # Get next items from the
         itemHi = self.__arr.get(idxHi) # two subranges
         if (self.__key(itemLo) <=   # Compare keys of those items
             self.__key(itemHi)):
            self.__work.set(n, itemLo) # Lo subrange is first so
            idxLo += 1           # copy item and advance to next
         else:
            self.__work.set(n, itemHi) # Hi subrange is first so
            idxHi += 1           # copy item and advance to next
         n += 1                  # One more item now in work array

      while idxLo < mid:         # Loop to copy remaining lo 
         self.__work.set(        # subrange items to work array
            n, self.__arr.get(idxLo))
         idxLo += 1
         n += 1

      while n > 0:               # Copy sorted work array contents
         n -= 1                  # back to input/output array in
         self.__arr.set(         # reverse order
            lo + n, self.__work.get(n))

# Implement Quicksort for Arrays using previous Array class

def identity(x): return x      # Identity function
import SortArray

class Array(SortArray.Array):  # Base new Array class on SortArray

   def partition_rec(          # Recursively partition array moving
         self,                 # items whose keys are below or equal
         pivot,                # a pivot value to the left/low side
         lo=0,                 # the rest to the right/high side
         hi=None,              # within the [lo, hi] range (inclusive)
         key=identity):        # Use key function to extract keys
      if hi is None:           # Default hi value is last index
         hi = len(self) - 1    # Everything above hi is in upper part
      while (lo <= hi and      # Increment lo until it goes past hi
             key(self.get(lo)) < pivot): # or we find a key that's not
         lo += 1               # in the lower partition
      while (lo < hi and       # Decrement hi until it matches lo
             pivot < key(self.get(hi))): # or we find the pivot or
         hi -= 1               # a key not in the upper partition
      if lo >= hi:             # If lo is at or above hi, then the
         return lo             # lower partition ends at lo
      self.swap(lo, hi)        # Otherwise, swap the items at lo & hi
      return self.partition_rec( # and recursively partition remaining
         pivot, lo + 1, hi - 1, key) # items in the array

   def partition(              # Loop to partition array, moving
         self,                 # items whose keys are below or equal
         pivot,                # a pivot value to the left/low side
         lo=0,                 # the rest to the right/high side
         hi=None,              # within the [lo, hi] range (inclusive)
         key=identity):        # Use key function to extract keys
      if hi is None:           # Default hi value is last index
         hi = len(self) - 1    # Everything above hi is in upper part
      while lo <= hi:          # Loop until no more items to inspect
         while (lo <= hi and   # Increment lo until it goes past hi
                key(self.get(lo)) < pivot): # or we find a key that's
            lo += 1            # not in the lower partition
         while (lo < hi and    # Decrement hi until it matches lo
                pivot < key(self.get(hi))): # or we find the pivot or
            hi -= 1            # a key not in the upper partition
         if lo >= hi:          # If lo is at or above hi, then the
            return lo          # lower partition ends at lo
         self.swap(lo, hi)     # Otherwise, swap the items at lo & hi
         lo, hi = lo + 1, hi - 1 # Continue partitioning in between
      return lo                # Range to partition is now empty

   def choosePivot(self, lo, hi): # Choose the pivot index around 
      return hi                # which to partition as the rightmost

   def quicksort_sketch(       # Sort items in an array between lo
         self, lo=0, hi=None,  # and hi indices using Hoare's
         key=identity):        # quicksort algorithm on the keys
      if hi is None:           # Fill in hi value if not specified
         hi = len(self) - 1
      if lo >= hi:             # If range has 1 or fewer cells,
         return                # then no sorting is needed
      
      pivot = self.choosePivot(lo, hi) # Choose a pivot

      hipart = self.partition( # Partition array around the key
         key(self.get(pivot)), # of the item at the pivot index and
         lo, hi, key)          # record where high part starts

      self.quicksort_sketch(lo, hipart - 1, key) # Sort lower part
      self.quicksort_sketch(hipart, hi, key) # Sort higher part

   def __partition(            # Private function partitions array by
         self,                 # items whose keys are below or equal
         pivot,                # a pivot value to the left/low side
         lo,                   # the rest to the right/high side
         hi,                   # within the [lo, hi] range (inclusive)
         key=identity):        # knowing at least one key == pivot
      while lo <= hi:          # Loop until no more items to inspect
         while (key(self.get(lo)) # Increment lo until we find a key 
                < pivot):      # that's not in the lower partition
            lo += 1            # Knowing pivot == one key in [lo,hi+1]
         while (lo < hi and    # Decrement hi until it matches lo
                pivot < key(self.get(hi))): # or we find the pivot or
            hi -= 1            # a key not in the upper partition
         if lo >= hi:          # If lo is at or above hi, then the
            return lo          # lower partition ends at lo
         self.swap(lo, hi)     # Otherwise, swap the items at lo & hi
         lo, hi = lo + 1, hi - 1 # Continue partitioning in between
      return lo                # Range to partition is now empty

   def qsort(                  # Sort items in an array between lo
         self, lo=0, hi=None,  # and hi indices using Hoare's
         key=identity):        # quicksort algorithm on the keys
      if hi is None:           # Fill in hi value if not specified
         hi = len(self) - 1
      if lo >= hi:             # If range has 1 or fewer cells,
         return                # then no sorting is needed
      pivot_i = hi             # Choose pivot index to be rightmost
      pivotItem = self.get(pivot_i) # Get item at pivot index
      hipart = self.__partition( # Partition array around the key
         key(pivotItem),       # of the item at the pivot index and
         lo, hi - 1, key)      # record where high part starts
      if hipart < pivot_i:     # If pivot index is above high
         self.swap(            # part start, then swap pivot item
            hipart, pivot_i)   # with high part start
      self.qsort(lo, hipart - 1, key) # Sort lower part
      self.qsort(hipart + 1, hi, key) # Sort higher part

   def qsort_show(             # Sort items in an array between lo
         self, lo=0, hi=None,  # and hi indices using Hoare's
         key=identity):        # quicksort algorithm on the keys
      if hi is None:           # Fill in hi value if not specified
         hi = len(self) - 1
      if lo >= hi:             # If range has 1 or fewer cells,
         return                # then no sorting is needed
      pivot_i = hi             # Choose pivot index to be rightmost
      pivotItem = self.get(pivot_i) # Get item at pivot index
      hipart = self.__partition( # Partition array around the key
         key(pivotItem),       # of the item at the pivot index and
         lo, hi - 1, key)      # record where high part starts
      if hipart < pivot_i:     # If pivot index is above high
         self.swap(            # part start, then swap pivot item
            hipart, pivot_i)   # with high part start
      print('Partitioning', lo, 'to', hi, 'leaves', self)
      self.qsort_show(lo, hipart - 1, key) # Sort lower part
      self.qsort_show(hipart + 1, hi, key) # Sort higher part

   def medianOfThree(          # Find median of lo, middle, and hi
         self, lo, hi,         # keys in subarray and put median
         key=identity):        # in hi position for partition
      mid = (lo + hi) // 2     # Compute middle index
      if key(self.get(lo)) > key(self.get(mid)): # Compare 1st pair
         self.swap(lo, mid)    # of keys and swap if lo > mid
      if key(self.get(lo)) > key(self.get(hi)): # Compare 2nd pair
         self.swap(lo, hi)     # of keys and swap if hi is lowest
      # At this point lo has the minimum of the 3 keys
      if key(self.get(hi)) > key(self.get(mid)): # Compare 3rd pair
         self.swap(hi, mid)    # of keys again and swap if hi > mid
      return self.get(hi)      # Return item with median key (@ hi)
         
   def insertionSort(          # Sort subarray by repeated inserts
         self,                 # This insertion sort will be used
         lo=0,                 # on small subarrays by quicksort
         hi=None,
         key=identity):
      if hi is None:           # Fill in hi value if not specified
         hi = len(self) - 1    # as last item in array
      for outer in range(lo + 1, hi + 1): # Mark one item
         temp = self.get(outer) # Store marked item in temp
         temp_key = key(temp)
         inner = outer         # Inner loop starts at mark at right
         while (inner > lo and # If inner hasn't reached lo and next
                temp_key < key(self.get(inner-1))): # item's key is
            self.set(inner, self.get(inner-1)) # smaller, then shift
            inner -= 1         # next item to right & move inner left
         self.set(inner, temp) # Move marked item to 'hole'

   def __part(                 # Private function partitions array by
         self,                 # items whose keys are below or equal
         pivot,                # a pivot value to the left/low side
         lo,                   # the rest to the right/high side
         hi,                   # within [lo, hi] knowing there is 1
         key=identity):        # key below pivot & pivot at hi+1
      while lo <= hi:          # Loop until no more items to inspect
         while (key(self.get(lo)) # Increment lo until we find a key 
                < pivot):      # that's not in the lower partition
            lo += 1            # Knowing pivot == one key in [lo,hi+1]
         while (pivot <        # Decrement hi until it points to key
                key(self.get(hi))): # in lower partition
            hi -= 1            # a key not in the upper partition
         if lo >= hi:          # If lo is at or above hi, then the
            return lo          # lower partition ends at lo
         self.swap(lo, hi)     # Otherwise, swap the items at lo & hi
         lo, hi = lo + 1, hi - 1 # Continue partitioning in between
      return lo                # Range to partition is now empty
      
   def quicksort(              # Sort items in an array between lo
         self,                 # and hi indices using Hoare's
         lo=0,                 # quicksort algorithm.  For short
         hi=None,              # subarrays, use insertion sort.
         short=3,              # Short must be 3 or more to enable
         key=identity):        # median of three choice of pivot
      if hi is None:           # Fill in hi value if not specified
         hi = len(self) - 1    # as last item in array
      short = max(3, short)    # Enforce short limit >= 3
      if hi - lo + 1 <= short: # If subarray is short, then use
         return self.insertionSort(lo, hi, key) # insertion sort
      pivotItem = self.medianOfThree( # Else find median key of lo,
         lo, hi, key)          # mid, hi and place item at hi index
      hipart = self.__part(    # Partition array around the key of
         key(pivotItem),       # the pivot item and
         lo + 1, hi - 1, key)  # record where high part starts
      self.swap(hipart, hi)    # Swap pivot with high part start
      self.quicksort(lo, hipart - 1, short, key) # Sort lower part
      self.quicksort(hipart + 1, hi, short, key) # Sort higher part

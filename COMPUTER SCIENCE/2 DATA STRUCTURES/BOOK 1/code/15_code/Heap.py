# Implement a Heap using a Python list/array

def identity(x): return x   # Identity function

class Heap(object):
   def __init__(self, key=identity, size=2): # Heap constructor
      self._arr = [None] * size # Heap stored as a list/array
      self._nItems = 0      # No items in initial heap
      self._key = key       # Function to get key from heap item

   def isEmpty(self): return self._nItems == 0 # Test for empty heap
    
   def isFull(self):  return self._nItems == len(self._arr)
    
   def __len__(self): return self._nItems  # Number of items
    
   def peek(self):          # Return item with maximum key
      return None if self.isEmpty() else self._arr[0]
         
   def parent(self, i):     # Get index of parent in heap tree
      return (i - 1) // 2   # Item i's parent index is half of i - 1

   def leftChild(self, i):  # Get index of left child in heap tree
      return i * 2 + 1      # Item i's left child is at twice i plus 1

   def rightChild(self, i): # Get index of right child in heap tree
      return i * 2 + 2      # Item i's right child -> twice i plus 2
    
   def insert(self, item):  # Insert a new item in a heap
      if self.isFull():     # If insertion would go beyond array
         self._growHeap()   # then expand heap array
      self._arr[self._nItems] = item # Store item at end of array
      self._nItems += 1     # Increase item count
      self._siftUp(self._nItems - 1) # Sift last item up

   def _growHeap(self):     # Grow the array for the heap
      current = self._arr   # Store the current array
      self._arr = [None] * max(1, 2 * len(self._arr)) # Double array
      for i in range(self._nItems): # Loop over all current items &
         self._arr[i] = current[i]  # copy them to the new array
    
   def remove(self):        # Remove top item of heap and return it
      if self.isEmpty():    # It's an error if the heap is empty
         raise Exception("Heap underflow")
      root = self._arr[0]   # Store the top item
      self._nItems -= 1     # Decrease item count
      self._arr[0] = self._arr[self._nItems] # Move last to root
      self._arr[self._nItems] = None # Clear for garbage collection
      self._siftDown(0)     # Move last item down into position
      return root           # Return top item
   
   def _siftUp_rec(self, i): # Sift item i up toward root to preserve
      if i <= 0:            # heap condition, recursively.  The root
         return             # node, i = 0, cannot go higher, so done.
      parent = self.parent(i) # Get the index of the parent node
      if (self._key(self._arr[parent]) < # If parent's key is less
          self._key(self._arr[i])): # than that of item i,
         self._swap(parent, i) # swap the items and
         self._siftUp(parent) # continue sift up at parent
   
   def _siftUp(self, i):    # Sift item i up toward root to preserve
      if i <= 0:            # heap condition.  The root node, i = 0,
         return             # cannot go higher, so done.
      item = self._arr[i]   # Store item at cell i
      itemkey = self._key(item) # and its key
      while 0 < i:          # While i is below the root
         parent = self.parent(i) # Get the index of its parent node
         if (self._key(self._arr[parent]) < # If parent's key is
             itemkey):      # less than that of item i,
            self._arr[i] = self._arr[parent] # copy parent to i
            i = parent      # and continue up tree
         else:              # If parent's key is greater or equal,
            break           # then we have found where item i belongs
      self._arr[i] = item   # Move item i into final position
         
   def _siftDown_rec(self, i): # Sift item i down to preserve heap cond.
      left, right = self.leftChild(i), self.rightChild(i) # Find child
      if left < len(self):  # indices and see if they are in heap
         if right < len(self): # If both children are present,
            maxi = right if (self._key(self._arr[left]) < # compare
                            self._key(self._arr[right]) # their keys
                           ) else left # and use largest
         else:              # No right child
            maxi = left     # So max child is on left
         if (self._key(self._arr[i]) < # If item i's key is less
             self._key(self._arr[maxi])): # than max child's key,
            self._swap(i, maxi) # then swap item i with max child
            self._siftDown(maxi) # and continue sift down

   def _siftDown(self, i):  # Sift item i down to preserve heap cond.
      firstleaf = len(self) // 2 # Get index of first leaf
      if i >= firstleaf:    # If item i is at or below leaf level,
         return             # it cannot be moved down
      item = self._arr[i]   # Store item at cell i
      itemkey = self._key(item) # and its key
      while i < firstleaf:  # While i above leaf level, find children
         left, right = self.leftChild(i), self.rightChild(i)
         maxi = left        # Assume left child has larger key
         if (right < len(self) and # If both children are present, and
             self._key(self._arr[left]) < # left child has smaller
             self._key(self._arr[right])): # key
            maxi = right    # then use right child
         if (itemkey <      # If item i's key is less
             self._key(self._arr[maxi])): # than max child's key,
            self._arr[i] = self._arr[maxi] # then move max child up
            i = maxi
         else:              # If item i's key is greater than or equal
            break           # to larger child, then found position
      self._arr[i] = item   # Move item to its final position
             
   def _swap(self, i, j):   # Swap item i and item j in heap array
      self._arr[i], self._arr[j] = self._arr[j], self._arr[i]

   def __str__(self):       # Convert heap to string
      ans = '<'             # Start with left bracket
      h = 0                 # Start at height 0
      width = 1             # Height level 0 has 1 key
      while width <= len(self): # Loop over all height levels
         if len(ans) > 1:   # After first height row is added,
            ans += ', '     # separate other rows with a comma + space
         ans += str(h) + ': (' + ', '.join( # Add row height plus keys
            [str(self._key(self._arr[j])) # joined by commas
             for j in range(width - 1, 
                            min(len(self), width - 1 + width))]) + ')'
         h += 1             # Go to next height level
         width += width     # where the width doubles
      return ans + '>'      # Close with right bracket and return

   def traverse(self):      # Generator to step through all heap items
      for i in range(len(self)): # Get each current item index
         yield self._arr[i] # and yield the item at the index
         
   def print(               # Print heap tree with root on left
         self, indentBy=2,  # indenting by a few spaces for each level
         indent='', i=0):   # starting with indent at node i
      if i >= len(self):    # If item i is not in tree
         return             # don't print it
      next = indent + ' ' * indentBy
      self.print(indentBy,  # Print right subtree of i at next indent
                  next, self.rightChild(i))
      print(indent, self._arr[i]) # Print item i after indent, then
      self.print(indentBy,  # Print left subtree of i at next indent
                 next, self.leftChild(i))

class PriorityQueue(Heap):  # Create a priority queue, using a heap
   def __init__(self, priority=identity): # Constructor
      super().__init__(     # Use the heap constructor
         key=priority)      # with the priority function as the key

   def __str__(self):       # String form of priortity queue only
      return '<PriorityQueue ' + (
         '(empty)' if self.isEmpty() else 'first: ' + str(self.peek())
      ) + '>'

def heapsort(array,         # Sort an array in-place by keys extracted
             key=identity): # from each item using the key function
   heapHi = len(array)      # Make entire array from 0 to heapHi
   heapify(array, heapHi, key) # into a heap using heapify
   while heapHi > 1:        # While heap has more than 1 item
      heapHi -= 1           # Decrement heap's higher boundary & swap
      array[0], array[heapHi] = array[heapHi], array[0] # max and last
      siftDown(array, 0, heapHi, key) # & sift down item moved to top

def siftDown(array,         # Sift item down in heap starting from
             j,             # node j
             N=None,        # down to but not including node N
             key=identity): # using key function to extract item's key
   if N is None:            # If N is not supplied,
      N = len(array)        # then use number of items in array
   firstleaf = N // 2       # Get index of first leaf in heap
   if j >= firstleaf:       # If item j is at or below leaf level,
      return                # it cannot be moved down
   item = array[j]          # Store item at cell j
   itemkey = key(item)      # and its key
   while j < firstleaf:     # While j above leaf level, find children
      left, right = j + j + 1, j + j + 2 # Get indices of children
      maxi = left           # Assume left child has larger key
      if (right < N and     # If both children are present, and
          key(array[left]) < # left child has smaller
          key(array[right])): # key
         maxi = right       # then use right child
      if (itemkey <         # If item j's key is less
          key(array[maxi])): # than max child's key,
         array[j] = array[maxi] # then move max child up
         j = maxi           # and continue from new "hole"
      else:                 # If item j's key is greater than or equal
         break              # to larger child, then found position
   array[j] = item          # Move item to its final position
   
def heapify(array,          # Organize an array of N items to satisfy
            N=None,         # the heap condition using keys extracted
            key=identity):  # from the items by the key function
   if N is None:            # If N is not supplied,
      N = len(array)        # then use number of items in array
   heapLo = N // 2          # The heap lies in the range [heapLo, N)
   while heapLo > 0:        # Heapify until the entire array is a heap
      heapLo -= 1           # Decrement heap's lower boundary
      siftDown(array, heapLo, N, key) # Sift down item at heapLo

def highest(K, array,       # Get the highest K items from an array
            N=None,         # of N items by heapifying the array based
            key=identity):  # on keys extracted by the key function
   if N is None:            # If N is not supplied,
      N = len(array)        # then use number of items in array
   heapify(array, N, key)   # Organize items into a heap
   result = [None] * K      # Construct an output array
   heapHi = N               # End of heap starts at last item
   while N - heapHi < K:    # While we have not yet removed K items,
      result[N - heapHi] = array[0] # Put max from heap in result
      heapHi -= 1           # Decrement heap's higher boundary & swap
      array[0], array[heapHi] = array[heapHi], array[0] # max and last
      siftDown(array, 0, heapHi, key) # & sift down item moved to top
   return result            # Return K-item result

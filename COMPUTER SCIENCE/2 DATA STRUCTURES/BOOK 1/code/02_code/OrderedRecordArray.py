# Implement an Ordered Array of Records structure

def identity(x):                    # The identity function
   return x

class OrderedRecordArray(object):
   def __init__(self, initialSize, key=identity):    # Constructor
      self.__a = [None] * initialSize  # The array stored as a list
      self.__nItems = 0                # No items in array initially
      self.__key = key                 # Key function gets record key

   def __len__(self):                  # Special def for len() func
      return self.__nItems             # Return number of items
   
   def get(self, n):                   # Return the value at index n
      if n >= 0 and n < self.__nItems: # Check if n is in bounds, and
         return self.__a[n]            # only return item if in bounds
      raise IndexError("Index " + str(n) + " is out of range")
         
   def traverse(self, function=print): # Traverse all items
      for j in range(self.__nItems):   # and apply a function
         function(self.__a[j])

   def __str__(self):                  # Special def for str() func
      ans = "["                        # Surround with square brackets
      for i in range(self.__nItems):   # Loop through items
         if len(ans) > 1:              # Except next to left bracket,
            ans += ", "                # separate items with comma
         ans += str(self.__a[i])       # Add string form of item
      ans += "]"                       # Close with right bracket
      return ans

   def find(self, key):             # Find index at or just below key
      lo = 0                        # in ordered list
      hi = self.__nItems-1          # Look between lo and hi
      
      while lo <= hi:
         mid = (lo + hi) // 2       # Select the midpoint
         
         if self.__key(self.__a[mid]) == key:  # Did we find it?
            return mid              # Return location of item

         elif self.__key(self.__a[mid]) < key: # Is key in upper half?
            lo = mid + 1            # Yes, raise the lo boundary
            
         else: 
            hi = mid - 1            # No, but could be in lower half
            
      return lo   # Item not found, return insertion point instead   

   def search(self, key):
      idx = self.find(key)          # Search for a record by its key
      if idx < self.__nItems and self.__key(self.__a[idx]) == key:
         return self.__a[idx]       # and return item if found
   
   def insert(self, item):    # Insert item into the correct position
      if self.__nItems >= len(self.__a): # If array is full,
         raise Exception("Array overflow") # raise exception

      j = self.find(self.__key(item))     # Find where item should go
      
      for k in range(self.__nItems, j, -1): # Move bigger items right
         self.__a[k] = self.__a[k-1]
         
      self.__a[j] = item      # Insert the item
      self.__nItems += 1      # Increment the number of items

   def delete(self, item):              # Delete any occurrence
      j = self.find(self.__key(item))   # Try to find the item
      if j < self.__nItems and self.__a[j] == item:  # If found,
         self.__nItems -= 1             # One fewer at end
         for k in range(j, self.__nItems): # Move bigger items left
            self.__a[k] = self.__a[k+1]
         return True                   # Return success flag

      return False            # Made it here; item not found

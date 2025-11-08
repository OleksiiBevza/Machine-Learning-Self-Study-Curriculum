# Implement a hash table usnig separate chaining
# This implementation makes use of the KeyValueList class to store
# the key-value pairs in each table cell

from Hashing import *
from KeyValueList import *
import sys

def simpleHash(key):        # A simple hashing function
   if isinstance(key, int): # Integers hash to themselves
      return key
   elif isinstance(key, str): # Strings are hashed by letters
      return sum(           # Multiply the code for each letter by
         256 ** i * ord(key[i]) # 256 to the power of its position
         for i in range(len(key))) # in the string
   elif isinstance(key, (list, tuple)): # For sequences,
      return sum(           # Multiply the simpleHash of each element
         256 ** i * simpleHash(key[i]) # by 256 to the power of its
         for i in range(len(key))) # position in the sequence
   raise Exception(         # Otherwise it's an unknown type
      'Unable to hash key of type ' + str(type(key)))
   
class HashTable(object):    # A hash table using separate chaining
   def __init__(            # The constructor takes the initial
         self, size=7,      # size of the table,
         hash=simpleHash,   # a hashing function, and
         maxLoadFactor=1.0): # the max load factor before growing
      self.__table = [None] * size # Allocate empty hash table
      self.__nItems = 0     # Track the count of items in the table
      self.__hash = hash    # Store given hash function, and max
      self.__maxLoadFactor = maxLoadFactor # load factor

   def __len__(self):       # The length of the hash table is the
      return self.__nItems  # number of cells that have items

   def cells(self):         # Get the size of the hash table in
      return len(self.__table) # terms of the number of cells

   def hash(self, key):     # Use the hashing function to get the
      return self.__hash(key) % self.cells() # default cell index

   def search(self,         # Get the value associated with a key
              key):         # in the hash table, if any
      i = self.hash(key)    # Get cell index by hashing key
      return (None if self.__table[i] is None else # If list exists,
              self.__table[i].search(key)) # search it, else None

   def insert(self,         # Insert or update the value associated
              key, value):  # with a given key
      i = self.hash(key)    # Get cell index by hashing key
      if self.__table[i] is None: # If the cell is empty,
         self.__table[i] = KeyValueList() # Create empty linked list
      flag = self.__table[i].insert(key, value) # Insert item in list
      if flag:              # If a node was added,
         self.__nItems += 1 # increment item count
         if self.loadFactor() > self.__maxLoadFactor: # When load
            self.__growTable() # factor exceeds limit, grow table
      return flag           # Return flag to indicate update
         
   def __growTable(self):   # Grow the table to accommodate more items
      oldTable = self.__table # Save old table
      size = len(oldTable) * 2 + 1 # Make new table at least 2 times
      while not is_prime(size): # bigger and a prime number of cells
         size += 2          # Only consider odd sizes
      self.__table = [None] * size # Allocate new table
      self.__nItems = 0     # Note that it is empty
      for i in range(len(oldTable)): # Loop through old cells and
         if oldTable[i]:    # if they contain a list, loop over
            for item in oldTable[i].traverse(): # all items
               self.insert(*item) # Re-hash the (key, value) tuple

   def loadFactor(self):    # Get the load factor for the hash table
      return self.__nItems / len(self.__table)
      
   def traverse(self):      # Traverse the key, value pairs in table
      for i in range(len(self.__table)): # Loop through all cells
         if self.__table[i]: # For those cells containing lists,
            for item in self.__table[i].traverse(): # traverse
               yield item   # the list yielding items

   def delete(self,         # Delete an item identified by its key
              key,          # from the hash table. Raise an exception
              ignoreMissing=False): # if not ignoring missing keys
      i = self.hash(key)    # Get cell index by hashing key
      if self.__table[i] is not None: # If cell i is not empty, try
         if self.__table[i].delete(key): # deleting item in list and
            self.__nItems -= 1 # if found, reduce count of items
            return True     # Return flag showing item was deleted
      if ignoreMissing:     # Otherwise, no deletion. If we ignore
         return False       # missing items, return flag
      raise Exception(      # Otherwise raise an exception
         'Cannot delete key {} not found in hash table'.format(key))

   def __str__(self):       # Convert table to a string representaion
      N = len(self.__table)
      out = '<HashTable of {} items'.format(self.__nItems)
      show = 5              # Number of cells to show at either end
      for i in range(min(show, N)): # First cells up to show - 1
         out += '\n  {:4d}-'.format(i)
         if self.__table[i]:
            out += str(self.__table[i])
      if N > 2 * show:
         out += '\n  ...'
      for i in range(max(N - show, show), N): # Last cells up to N - 1
         out += '\n  {:4d}-'.format(i)
         if self.__table[i]:
            out += str(self.__table[i])
      out += ' >'
      return out

   def tableString(self):   # Show the keys of all table cells as
      return '[{}]'.format(','.join( # a string
         ' ' if cell is None else # Empty cells are spaces,
         '[{}]'.format(     # Lists are square braces enclosing
            ', '.join(      # a list of keys separated by commas
               repr(key) for key, val in cell.traverse())
            for cell in self.__table)))

   def peek(self, i):       # Peek at contents of cell i
      return self.__table[i]

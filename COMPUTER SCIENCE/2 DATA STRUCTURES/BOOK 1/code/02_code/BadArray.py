# Implement an Array data structure as a simplified type of list. 

class Array(object):
   
   def __init__(self, initialSize):    # Constructor
      self.__a = [None] * initialSize  # The array stored as a list
      self.nItems = 0                  # No items in array initially

   def insert(self, item):             # Insert item at end
      self.__a[self.nItems] = item     # Item goes at current end
      self.nItems += 1                 # Increment number of items

   def search(self, item):
      for j in range(self.nItems):     # Search among current
         if self.__a[j] == item:       # If found,
            return self.__a[j]         # then return item
      
      return None                      # Not found -> None

   def delete(self, item):             # Delete first occurrence
      for j in range(self.nItems):     # of an item
         if self.__a[j] == item:       # Found item
            for k in range(j, self.nItems):  # Move items from
               self.__a[k] = self.__a[k+1]   # right over 1
            self.nItems -= 1           # One fewer in array now
            return True                # Return success flag
      
      return False     # Made it here, so couldn't find the item   

   def traverse(self, function=print): # Traverse all items
      for j in range(self.nItems):     # and apply a function
         function(self.__a[j])

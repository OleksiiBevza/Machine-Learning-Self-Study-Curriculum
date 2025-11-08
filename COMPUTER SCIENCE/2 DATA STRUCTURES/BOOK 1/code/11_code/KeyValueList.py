# Implement a singly linked list of (key, value) tuples

import LinkedList

def itemKey(item): return item[0] # Key is first element of item
def itemValue(item): return item[1] # Value is second element of item

class KeyValueList(LinkedList.LinkedList): # Customize LinkedList

   def insert(self, key, value): # Insert a key + value in list
      link = self.find(key, itemKey) # Find matching Link object
      if link is None:        # If not found,
         super().insert((key, value)) # insert item at front
         return True          # return success
      link.setData((key, value)) # Otherwise, update existing link's
      return False            # datum and return no-insert flag

   def search(self, key):     # Search by matching item key
      item = super().search(key, key=itemKey) # Locate key + value
      return itemValue(item) if item else None # Return value if any

   def delete(self, key):     # Delete a key from the list
      try:                    # Try the LinkedList deletion by key
         item = super().delete(key, itemKey) 
         return item          # If no exceptions, return deleted item
      except:                 # All exceptions mean key was not
         return False         # found, so return False
      
   def traverse(self):        # Linked list traverse generator
      link = self.getFirst()  # Start with first link
      while link is not None: # Keep going until no more links
         yield link.getData() # Yield the item
         link = link.getNext() # Move on to next link

   

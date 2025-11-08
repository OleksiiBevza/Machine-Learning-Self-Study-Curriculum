# Implement a Stack data structure using a linked list

from LinkedList import *

class LinkStack(object):
   def __init__(self):                 # Constructor for a
      self.__sList = LinkedList()      # stack stored as a linked list
        
   def push(self, item):               # Insert item at top of stack
      self.__sList.insert(item)        # Store item as first in list
        
   def pop(self):                      # Remove top item from stack
      return self.__sList.deleteFirst() # Return first and delete it
    
   def peek(self):                     # Return top item
      if not self.__sList.isEmpty():   # If stack is not empty
         return self.__sList.first()   # Return the top item
    
   def isEmpty(self):                  # Check if stack is empty
      return self.__sList.isEmpty()

   def __len__(self):                  # Return # of items on stack
      return len(self.__sList)
    
   def __str__(self):                  # Convert stack to string
      return str(self.__sList)

class Stack(LinkedList):               # Define stack by renaming
   push = LinkedList.insert            # Push is done by insert
   pop = LinkedList.deleteFirst        # Pop is done by deleteFirst
   peek = LinkedList.first             # Peek is done by first

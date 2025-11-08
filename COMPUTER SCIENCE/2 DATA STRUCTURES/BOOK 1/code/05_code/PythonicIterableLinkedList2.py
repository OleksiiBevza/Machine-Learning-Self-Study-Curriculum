# Implement an iterator for a singly linked list using Python hooks

import LinkedList

class LinkedList(LinkedList.LinkedList): # Redefine the linked list

   def __iter__(self):         # Define an iterator for the list
      next = self.getFirst()   # Start with first Link
      while next is not None:  # As long as the link is not None,
         yield next.getData()  # yield data for the link
         next = next.getNext() # then move on to next link

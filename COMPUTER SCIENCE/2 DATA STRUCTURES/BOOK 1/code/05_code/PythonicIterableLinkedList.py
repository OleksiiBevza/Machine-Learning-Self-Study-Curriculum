# Implement an iterator for a singly linked list using Python hooks

import LinkedList

class LinkedList(LinkedList.LinkedList): # Redefine the linked list
                             # with a self-made iterator class

   class __ListIterator(object):  # Private iterator class
      def __init__(self, llist):  # Construct an iterator over a
         self._llist = llist      # linked list
         self._next = llist.getFirst() # Start at first Link

      def __next__(self):         # Iterator's __next__() method
         if self._next is None:   # Check for end of list
            raise StopIteration   # At end, raise exception
         item = self._next.getData() # Store next data item
         self._next = self._next.getNext() # Advance to following
         return item

      def __iter__(self): return self
      
   def __iter__(self):
      return LinkedList.__ListIterator(self)

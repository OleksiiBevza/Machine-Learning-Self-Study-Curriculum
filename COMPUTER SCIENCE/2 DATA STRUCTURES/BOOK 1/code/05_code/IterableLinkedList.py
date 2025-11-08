# Implement an iterator for a singly linked list

import LinkedList

class LinkedList(LinkedList.LinkedList): # Redefine the linked list
                               # to include an iterator

   class __ListIterator(object):  # Private iterator class
      def __init__(self, llist):  # Construct an iterator over a
         self._llist = llist      # linked list
         self._next = llist.getFirst() # Start at first Link

      def next(self):             # Iterator's next() method
         if self._next is None:   # Check for end of list
            raise StopIteration   # At end, raise exception
         item = self._next.getData() # Store next data item
         self._next = self._next.getNext() # Advance to following
         return item

      def hasMore(self):          # Is there more to iterate?
         return self._next is not None  # Check for end of list

      def reset(self):            # Reset iterator to first link
         self._next = self._llist.getNext()
      
   def iterator(self):
      return LinkedList.__ListIterator(self)

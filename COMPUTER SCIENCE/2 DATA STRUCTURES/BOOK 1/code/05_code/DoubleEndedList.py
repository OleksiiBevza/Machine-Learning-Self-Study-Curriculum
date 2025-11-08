# Implement a double-ended linked list based on the singly linked list

from LinkedList import *

class DoubleEndedList(LinkedList): # A linked list with access to both
   def __init__(self):         # ends of the list
      self.__first = None      # Reference to first Link, if any
      self.__last = None       # Reference to last link, if any

   def getFirst(self): return self.__first # Return the first link

   def setFirst(self, link):   # Change the first link to a new Link
      if link is None or isinstance(link, Link): #Must be Link or None
         self.__first = link   # Update first link 
         if (link is None or   # When removing the first Link or
             self.getLast() is None): # the last Link is not set,
            self.__last = link # then update the last link, too.
      else:
         raise Exception("First link must be Link or None")

   def getLast(self): return self.__last # Return the last link

   def last(self):             # Return the last item in the list
      if self.isEmpty():       # as long as it is not empty
         raise Exception('No last element in empty list')
      return self.__last.getData()

   def insertLast(self, datum): # Insert a new datum at end of list
      if self.isEmpty():        # For empty lists, end is the front,
         return self.insert(datum) # so insert there
      link = Link(datum, None)  # Else make a new end Link with datum
      self.__last.setNext(link) # Add new Link after current last
      self.__last = link        # Change last to new end Link

   def insertAfter(            # Insert a new datum after the 1st
         self, goal, newDatum, # Link with a matching key
         key=identity):
      link = self.find(goal, key)  # Find matching Link object
      if link is None:         # If not found,
         return False          # return failure
      newLink = Link(          # Else build a new Link node with
         newDatum, link.getNext()) # new datum and remainder of list
      link.setNext(newLink)    # and insert after matching link
      if link is self.__last:  # If the update was after the last,
         self.__last = newLink # then update reference to last
      return True

   def delete(self, goal,      # Delete the first Link from the
              key=identity):   # list whose key matches the goal
      if self.isEmpty():       # Empty list? Raise an exception
         raise Exception("Cannot delete from empty linked list")

      previous = self          # Link or LinkedList before Link
      while previous.getNext() is not None: # to be deleted
         link = previous.getNext()  # Next link after previous
         if goal == key(link.getData()): # If next Link matches,
            if link is self.__last:   # and if it was the last Link,
               self.__last = previous # then move last back 1
            previous.setNext(      # Change the previous' next
               link.getNext())     # to be Link's next and return
            return link.getData()  # data since match was found
         previous = link           # Advance previous to next Link
         
      # Since loop ended without finding item exception
      raise Exception("No item with matching key found in list")

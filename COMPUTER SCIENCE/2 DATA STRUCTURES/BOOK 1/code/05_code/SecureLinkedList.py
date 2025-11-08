# Implement a singly linked list using a private Link class to
# avoid exposing Link.setNext() and LinkedList.find() methods

def identity(x): return x       # Identity function
NoneType = type(None)           # Get the NoneType class

class LinkedList(object):       # A linked list of data items
   def __init__(self):          # Constructor
      self.__first = None        # Reference to first Link
      
   class __Link(object):        # One datum in a linked list
      def __init__(self, datum, next=None): # Constructor
         self.__data = datum    # The datum for this link
         self.__next = next     # Reference to next Link

      def getData(self):        # Return the datum stored in this link
         return self.__data

      def setData(self, datum): # Change the datum in this Link
         self.__data = datum

      def _getNext(self): return self.__next # Return the next link

      def _setNext(self, link): # Change the next link to a new Link
         if isinstance(link, (  # Must be __Link or None
               type(self), NoneType)):
            self.__next = link
         else:
            raise Exception("Next link must be __Link or None")

      # Allow these accessor methods to be called by name mangling
      # within LinkedList methods
      _LinkedList__getNext = _getNext
      _LinkedList__setNext = _setNext

      def isLast(self):         # Test if link is last in the chain
         return self._getNext() is None  # True iff no next Link

      def __str__(self):        # Make a string representation of link
         return str(self.getData())
      
   # Methods of LinkedList class
   def __getFirst(self): return self.__first # Return the first link

   def __setFirst(self, link):  # Change the first link to a new Link
      if isinstance(link, (     # Must be __Link or None
            LinkedList.__Link, NoneType)):
         self.__first = link

   def __getNext(self): return self.__getFirst() # Return 1st link
   def __setNext(self, link):   # Change the next link to a new Link
      self.__setFirst(link)
   
   def isEmpty(self):           # Test for empty list
      return self.__getNext() is None  # True iff no next Link

   def first(self):             # Return the first item in the list
      if self.isEmpty():        # as long as it is not empty
         raise Exception('No first item in empty list')
      return self.__getFirst().getData()
   
   def traverse(self,          # Apply a function to all Links in list
                func=print):   # with the default being to print
      link = self.__getFirst()  # Start with first link
      while link is not None:  # Keep going until no more links
         func(link.getData())  # Apply the function to the item
         link = link._getNext() # Move on to next link

   def __len__(self):          # Get length of list
      l = 0
      link = self.__getFirst()  # Start with first link
      while link is not None:  # Keep going until no more links
         l += 1                # Count Link in chaing
         link = link._getNext() # Move on to next link
      return l
         
   def __str__(self):          # Build a string representation
      result = "["             # Enclose list in square brackets
      link = self.__getFirst()  # Start with first link
      while link is not None:  # Keep going until no more links
         if len(result) > 1:   # After first link,
            result += ' > '    # separate links with right arrowhead
         result += str(link)   # Append string version of link
         link = link._getNext() # Move on to next link
      return result + "]"      # Close with square bracket

   def insert(self, datum): # Insert a new datum at start of list
      link = LinkedList.__Link( # Make a new Link for the datum
         datum,
         self.__getFirst())      # What follows is the current list
      self.__setFirst(link)      # Update list to include new Link

   def __find(                  # Find the 1st Link whose key matches
         self, goal, key=identity): # the goal
      link = self.__getFirst()   # Start at first link
      while link is not None:   # Search until the end of the list
         if key(link.getData()) == goal:  # Does this Link match?
            return link         # If so, return the Link itself
         link = link._getNext() # Else, continue on along list
         
   def search(                     # Find 1st datum whose key matches
         self, goal, key=identity): # the goal
      link = self.__find(goal, key) # Look for matching Link object
      if link is not None:         # If found,
         return link.getData()     # return its datum

   def insertAfter(                # Insert a new datum after the 1st
         self, goal, newDatum,     # Link with a matching key
         key=identity):
      link = self.__find(goal, key) # Find matching Link object
      if link is None:             # If not found,
         return False              # return failure
      newLink = LinkedList.__Link( # Else build a new Link node with
         newDatum, link._getNext()) # new datum and remainder of list
      LinkedList.__Link._setNext(link, newLink)
      return True

   def delete(self, goal,          # Delete the first Link from the
              key=identity):       # list whose key matches the goal
      if self.isEmpty():           # Empty list? Raise an exception
         raise Exception("Cannot delete from empty linked list")

      previous = self              # Link or LinkedList before Link
      while previous.__getNext() is not None:  # to be deleted.
         link = previous.__getNext() 
         if goal == key(link.getData()): # If next Link matches,
            previous.__setNext(link._getNext()) # to be Link's next
            return True            # return since 1st match was found
         previous = link           # Advance previous to next Link
         
      # Since loop ended without finding item, raise exception
      raise Exception("No item with matching key found in list")

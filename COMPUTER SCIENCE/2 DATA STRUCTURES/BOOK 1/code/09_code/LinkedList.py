# Implement a singly linked list and a link class

def identity(x): return x      # Identity function

class Link(object):            # One datum in a linked list
   def __init__(self, datum, next=None): # Constructor
      self.__data = datum      # The datum for this link
      self.__next = next       # Reference to next Link

   def getData(self):          # Return the datum stored in this link
      return self.__data

   def setData(self, datum):   # Change the datum in this Link
      self.__data = datum

   def getNext(self): return self.__next # Return the next link

   def setNext(self, link):    # Change the next link to a new Link
      if link is None or isinstance(link, Link): #Must be Link or None
         self.__next = link
      else:
         raise Exception("Next link must be Link or None")

   def isLast(self):           # Test if link is last in the chain
      return self.getNext() is None  # True if & only if no next Link

   def __str__(self):          # Make a string representation of link
      return str(self.getData())

class LinkedList(object):      # A linked list of data elements
   def __init__(self):         # Constructor
      self.__first = None      # Reference to first Link

   def getFirst(self): return self.__first # Return the first link

   def setFirst(self, link):   # Change the first link to a new Link
      if link is None or isinstance(link, Link): # It must be None or
         self.__first = link   # a Link object
      else:
         raise Exception("First link must be Link or None")
      
   def getNext(self): return self.getFirst()    # First link is next
   def setNext(self, link): self.setFirst(link) # First link is next

   def isEmpty(self):          # Test for empty list
      return self.getFirst() is None # True if & only if no 1st Link

   def first(self):            # Return the first item in the list
      if self.isEmpty():       # as long as it is not empty
         raise Exception("No first item in empty list")
      return self.getFirst().getData() # Return data item (not Link)
   
   def traverse(self,          # Apply a function to all items in list
                func=print):   # with the default being to print
      link = self.getFirst()   # Start with first link
      while link is not None:  # Keep going until no more links
         func(link.getData())  # Apply the function to the item
         link = link.getNext() # Move on to next link

   def __len__(self):          # Get length of list
      l = 0
      link = self.getFirst()   # Start with first link
      while link is not None:  # Keep going until no more links
         l += 1                # Count Link in chain
         link = link.getNext() # Move on to next link
      return l
         
   def __str__(self):          # Build a string representation
      result = "["             # Enclose list in square brackets
      link = self.getFirst()   # Start with first link
      while link is not None:  # Keep going until no more links
         if len(result) > 1:   # After first link,
            result += " > "    # separate links with right arrowhead
         result += str(link)   # Append string version of link
         link = link.getNext() # Move on to next link
      return result + "]"      # Close with square bracket

   def insert(self, datum):    # Insert a new datum at start of list
      link = Link(datum,       # Make a new Link for the datum
                  self.getFirst()) # What follows is the current list
      self.setFirst(link)      # Update list to include new Link

   def find(                   # Find the 1st Link whose key matches
         self, goal, key=identity): # the goal
      link = self.getFirst()   # Start at first link
      while link is not None:  # Search until the end of the list
         if key(link.getData()) == goal:  # Does this Link match?
            return link        # If so, return the Link itself
         link = link.getNext() # Else, continue on along list
         
   def search(                 # Find 1st item whose key matches goal
         self, goal, key=identity):
      link = self.find(goal, key) # Look for Link object that matches
      if link is not None:     # If found,
         return link.getData() # return its datum

   def insertAfter(            # Insert a new datum after the first
         self, goal, newDatum, # Link with a matching key
         key=identity):
      link = self.find(goal, key)  # Find matching Link object
      if link is None:         # If not found,
         return False          # return failure
      newLink = Link(          # Else build a new Link node with
         newDatum, link.getNext()) # new datum and remainder of list
      link.setNext(newLink)    # and insert after matching link
      return True

   def deleteFirst(self):      # Delete first Link
      if self.isEmpty():       # Empty list? Raise an exception
         raise Exception("Cannot delete first of empty list")
      
      first = self.getFirst()  # Store first Link
      self.setFirst(first.getNext()) # Remove first link from list
      return first.getData()   # Return first Link's data

   def delete(self, goal,      # Delete the first Link from the
              key=identity):   # list whose key matches the goal
      if self.isEmpty():       # Empty list? Raise an exception
         raise Exception("Cannot delete from empty linked list")

      previous = self          # Link or LinkedList before Link
      while previous.getNext() is not None: # to be deleted
         link = previous.getNext()  # Next link after previous
         if goal == key(link.getData()): # If next Link matches,
            previous.setNext(  # change the previous' next
               link.getNext()) # to be Link's next and return
            return link.getData() # data since match was found
         previous = link       # Advance previous to next Link
         
      # Since loop ended without finding item, raise exception
      raise Exception("No item with matching key found in list")

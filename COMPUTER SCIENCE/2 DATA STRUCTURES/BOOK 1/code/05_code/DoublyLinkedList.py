# Implement a doubly linked linked list and link class from a
# singly linked list

def identity(x): return x         # Identity function

import LinkedList

class Link(LinkedList.Link):      # One datum in a linked list
   def __init__(self, datum,      # Constructor with datum
                next=None,        # and optional next and
                previous=None):   # previous pointers
      self.__data = datum
      self.__next = next          # reference to next item in list
      self.__previous = previous  # reference to previous item
        
   def getData(self): return self.__data   # Accessors
   def getNext(self): return self.__next
   def getPrevious(self): return self.__previous
   def setData(self, d): self.__data = d
   def setNext(self, link):             # Accessor that enforces type
      if link is None or isinstance(link, Link):
         self.__next = link
      else:
         raise Exception("Next link must be Link or None")
   def setPrevious(self, link):         # Accessor that enforces type
      if link is None or isinstance(link, Link):
         self.__previous = link
      else:
         raise Exception("Previous link must be Link or None")
        
   def isFirst(self): return self.__previous is None 

class DoublyLinkedList(LinkedList.LinkedList):
   def __init__(self):                 # Constructor
       self.__first, self.__last = None, None
       
   def getFirst(self): return self.__first # Accessors
   def getLast(self): return self.__last

   def setFirst(self, link):           # Set first link
      if link is None or isinstance(link, Link): # Check type
         self.__first = link
         if (self.__last is None or    # If list was empty or
             link is None):            # list is being truncated
            self.__last = link         # update both ends
      else:
         raise Exception("First link must be Link or None")

   def setLast(self, link):            # Set last link
      if link is None or isinstance(link, Link): # Check type
         self.__last = link
         if (self.__first is None or   # If list was empty or
             link is None):            # list is being truncated
            self.__first = link        # update both ends
      else:
         raise Exception("Last link must be Link or None")

   def traverseBackwards(      # Apply a function to all Links in list
         self, func=print):    # backwards from last to first
      link = self.getLast()    # Start with last link
      while link is not None:  # Keep going until no more links
         func(link)            # Apply the function to the link
         link = link.getPrevious() # Move on to previous link

   def insertFirst(self, datum): # Insert a new datum at start of list
      link = Link(datum,         # New link has datum
                  next=self.getFirst()) # and precedes current first
      if self.isEmpty():         # If list is empty,
         self.setLast(link)      # insert link as last (and first)
      else:                      # Otherwise, first Link in list
         self.getFirst().setPrevious(link) # now has new Link before
         self.setFirst(link)     # Update first link

   insert = insertFirst          # Override parent class insert()
   
   def insertLast(self, datum):  # Insert a new datum at end of list
      link = Link(datum,         # New link has datum
                  previous=self.getLast()) # and follows current last
      if self.isEmpty():         # If list is empty,
         self.setFirst(link)     # insert link as first (and last)
      else:                      # Otherwise, last Link in list
         self.getLast().setNext(link) # now has new Link after
         self.setLast(link)      # Update last link
    
   def deleteFirst(self):        # Delete and return first link's data
      if self.isEmpty():         # If list is empty, raise exception
         raise Exception("Cannot delete first of empty list") 
      first = self.getFirst()    # Store the first link
      self.setFirst(first.getNext()) # Remove first, advance to next
      if self.getFirst():        # If that leaves a link in the list,
         self.getFirst().setPrevious(None) # Update its predecessor
      return first.getData()     # Return data from first link
    
   def deleteLast(self):         # Delete and return last link's data
      if self.isEmpty():         # If list is empty, raise exception
         raise Exception("Cannot delete last of empty list") 
      last = self.getLast()      # Store the last link
      self.setLast(last.getPrevious()) # Remove last, advance to prev
      if self.getLast():         # If that leaves a link in the list,
         self.getLast().setNext(None) # Update its successor
      return last.getData()      # Return data from last link

   def insertAfter(                # Insert a new datum after the
         self, goal, newDatum,     # first Link with a matching key
         key=identity):
      link = self.find(goal, key)  # Find matching Link object
      if link is None:             # If not found,
         return False              # return failure
      if link.isLast():            # If matching Link is last,
         self.insertLast(newDatum) # then insert at end
      else:
         newLink = Link(           # Else build a new Link node with
            newDatum,              # the new datum that comes just
            previous=link,         # after the matching link and 
            next=link.getNext())   # before the remaining list
         link.getNext().setPrevious( # Splice in reverse link
            newLink)               # from link after matching link
         link.setNext(newLink)     # Add newLink to list
      return True

   def delete(self, goal,          # Delete the first Link from the
              key=identity):       # list whose key matches the goal
      link = self.find(goal, key)  # Find matching Link object
      if link is None:             # If not found, raise exception
         raise Exception("Cannot find link to delete in list")
      if link.isLast():            # If matching Link is last,
         return self.deleteLast()  # then delete from end
      elif link.isFirst():         # If matching Link is first,
         return self.deleteFirst() # then delete from front
      else:                        # Otherwise it's a middle link
         link.getNext().setPrevious( # Set next link's previous
            link.getPrevious())    # to link preceding the match
         link.getPrevious().setNext( # Set previous link's next
            link.getNext())        # to link following the match
         return link.getData()     # Return deleted data item

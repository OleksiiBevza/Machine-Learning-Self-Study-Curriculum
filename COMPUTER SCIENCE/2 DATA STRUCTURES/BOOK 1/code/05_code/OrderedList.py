# Implement an ordered linked list based on a singly linked list

from LinkedList import *

class OrderedList(LinkedList): # An ordered linked list where items
   def __init__(self,          # are in increasing order by key, which
                key=identity): # is retrieved by a func. on each item
      self.__first = None      # Reference to first Link, if any
      self.__key = key         # Function to retrieve key

   def getFirst(self): return self.__first # Return the first link

   def setFirst(self, link):   # Change the first link to a new Link
      if link is None or isinstance(link, Link): #Must be Link or None
         self.__first = link
      else:
         raise Exception("First link must be Link or None")

   def find(self, goal):       # Find the 1st Link whose key matches
                               # or is after the goal
      link = self.getFirst()   # Start at first link, and search
      while (link is not None and         # while not end of the list
             self.__key(link.getData()) < goal): # and before goal
         link = link.getNext() # Advance to next in list
      return link # Return Link at or just after goal or None for end
      
   def search(self, goal):     # Find 1st datum whose key matches goal
      link = self.find(goal)   # Look for Link object that matches
      if (link is not None and     # If Link found, and its key
          self.__key(link.getData()) == goal): # matches the goal
         return link.getData()     # return its datum

   def insert(self, newDatum): # Insert a new datum based on key order
      goal = self.__key(newDatum)  # Get target key 
      previous = self          # Link or OrderedList before goal Link
      while (previous.getNext() is not None and  # Has next link and
             self.__key(previous.getNext().getData()) 
             < goal):          # next link's key is before the goal
         previous = previous.getNext() # Advance to next link
      newLink = Link(          # Build a new Link node with new
         newDatum, previous.getNext()) # datum and remainder of list
      previous.setNext(newLink) # Update previous' first/next pointer

   def delete(self, goal):     # Delete first Link with matching key
      if self.isEmpty():       # Empty list? Raise an exception
         raise Exception("Cannot delete from empty linked list")

      previous = self          # Link or OrderedList before Link
      while (previous.getNext() is not None and  # Has next link and
             self.__key(previous.getNext().getData())
             < goal):          # next link's key is before the goal
         previous = previous.getNext()  # Advance to next link
      if (previous.getNext() is None or # If goal key not in next
          goal !=                       # Link after previous
          self.__key(previous.getNext().getData())):
         raise Exception("No datum with matching key found in list")

      toDelete = previous.getNext() # Store Link to delete
      previous.setNext(toDelete.getNext()) # Remove it from list
         
      return toDelete.getData() # Return data in deleted Link

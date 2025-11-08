# Implement a Priority Queue data structure using a Python list

def identity(x):  return x            # Identity function

class PriorityQueue(object):
   def __init__(self, size, pri=identity): # Constructor
      self.__maxSize = size           # Size of array
      self.__que = [None] * size      # Queue stored as a list
      self.__pri = pri                # Func. to get item priority
      self.__nItems = 0               # no items in queue
    
   def insert(self, item):            # Insert item at rear of
      if self.isFull():               # priority queue if not full
         raise Exception("Queue overflow")
      j = self.__nItems - 1           # Start at front
      while j >= 0 and (              # Look for place by priority
            self.__pri(item) >= self.__pri(self.__que[j])):
         self.__que[j+1] = self.__que[j] # Shift items to front
         j -= 1                       # Step towards rear
      self.__que[j+1] = item          # Insert new item at rear
      self.__nItems += 1
      return True
    
   def remove(self):                  # Return front item of priority
      if self.isEmpty():              # queue, if not empty, & remove
         raise Exception("Queue underflow")
      self.__nItems -= 1              # One fewer item in queue
      front = self.__que[self.__nItems] # Store frontmost item
      self.__que[self.__nItems] = None # Remove item reference        
      return front
    
   def peek(self):                    # Return frontmost item
      return None if self.isEmpty() else self.__que[self.__nItems-1]
        
   def isEmpty(self): return self.__nItems == 0
    
   def isFull(self):  return self.__nItems == self.__maxSize
    
   def __len__(self): return self.__nItems

   def __str__(self):                 # Convert pri. queue to string
      ans = "["                       # Start with left bracket
      for i in range(self.__nItems - 1, -1, -1): # Loop from front
         if len(ans) > 1:             # Except next to left bracket,
            ans += ", "               # separate items with comma
         ans += str(self.__que[i])    # Add string form of item
      ans += "]"                      # Close with right bracket
      return ans

# Implment a recursive solution to the Tower of Hanoi puzzle

from SimpleStack import *

class TowerOfHanoi(object):    # Model the tower on 3 spindles using
                               # 3 stacks
   def __init__(self, nDisks=3): # Constructor w/ starting number of
      self.__stacks = [None] * 3 # Stacks of disks
      self.__labels = ['L', 'M', 'R'] # Labels for stacks/spindles
      self.__nDisks = nDisks   # Total number of disks
      self.reset()

   def reset(self):            # Initialize state of puzzle
      for spindle in range(3): # Set up each of 3 spindles
         self.__stacks[spindle] = Stack( # Start w/ empty stack
            self.__nDisks)     # that can hold all the disks
         if spindle == 0:      # On the first spindle,
            for disk in range( # push the disks on the stack
                  self.__nDisks, 0, -1): # in descending order of size
               self.__stacks[spindle].push(disk)

   def label(self, spindle):   # Get the label of spindle
      return self.__labels[spindle]

   def height(self, spindle):  # Get the number of disks on a spindle
      return len(self.__stacks[spindle])

   def topDisk(self, spindle): # Get top disk number on a spindle or
      if not self.__stacks[spindle].isEmpty(): # None if no disks
         return self.__stacks[spindle].peek() # Peek at top disk

   def __str__(self):          # Show puzzle state as a string
      result = ""              # Start with empty string
      for spindle in range(3): # Loop over spindles
         if len(result) > 0:   # After first spindle,
            result += "\n"     # separate stacks on new lines
         result += (
            self.label(spindle) + ': ' + # Add spindle label
            str(self.__stacks[spindle])) # and spindle contents
      return result

   def move(self, source, to,  # Move a single disk from source
            show=False):       # spindle to another, possibly printing
      if self.__stacks[source].isEmpty(): # Source spindle must have
         raise Exception(      # a disk, or it's an error
            "Cannot move from empty spindle " + self.label(source))
      if (not self.__stacks[to].isEmpty() and # Destination cannot
          self.topDisk(source) > # have a disk smaller than that of
          self.topDisk(to)):   # source
         raise Exception(
            "Cannot move disk " + str(self.topDisk(source)) +
            "on top of disk " + str(self.topDisk(to)))
      self.__stacks[to].push(  # Push top disk of source spindle
         self.__stacks[source].pop()) # on to the 'to' spindle
      if show:
         print('Move disk', self.topDisk(to),
               'from spindle', self.label(source),
               'to', self.label(to))

   def solve(self,             # Solve the puzzle to move
             nDisks=None,      # N disks from
             start=0,          # starting spindle
             goal=2,           # to goal spindle
             spare=1,          # with spare spindle
             show=False):      # and possibly showing steps
      if nDisks is None:       # Default number of disks to move
         nDisks = self.height(start) # is all the disks on start
      if nDisks <= 0:          # If no request to move disks
         return                # there's nothing to do
      if self.height(start) < nDisks: # Check if there are fewer
         raise Exception(             # disks to move than requested
            "Not enough disks (" + str(nDisks) +
            ") on starting spindle " + self.label(start))

      self.solve(nDisks - 1,  # Move n - 1 from start to spare with
                 start, spare, goal, show) # goal as spare
      self.move(start, goal, show)  # Move nth from start to goal
      if show: print(self)          # Show puzzle state after move
      self.solve(nDisks - 1,  # Then move n - 1 from spare to goal
                 spare, goal, start, show) # with start as spare
      if (nDisks == self.__nDisks and   # Were all disks moved?
          show):              # then puzzle is solved and can show
         print("Puzzle complete") # conclusion if requested

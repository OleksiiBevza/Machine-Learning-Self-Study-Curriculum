# Implement ShellSort for Arrays using previous Array class

import SortArray

class Array(SortArray.Array):  # Base new Array class on SortArray
   
   def ShellSort(self):        # Sort using Shell's method:
      h = 1                    # Choose h to sort every h items
      while 3 * h + 1 < len(self): # Use Knuth's h sequence, find
         h = 3 * h + 1         # largest h less than array length
      nShifts = 0              # Count number of shifts
      while h > 0:             # Loop over decreasing h values
         for outer in range(h, len(self)): # Mark one item
            temp = self.get(outer)       # Store marked item in temp
            inner = outer                # Inner loop starts at mark
            while inner >= h and temp < self.get(inner-h): # If marked
               self.set(inner, self.get(inner-h)) # item smaller, then
               inner -= h                # shift item to right
               nShifts += 1              # Count shift 
            if inner < outer:  # If inner loop advanced a step, then
               self.set(inner, temp)     # Move marked item to 'hole'
               nShifts += 1    # and count the shift
         h = (h - 1) // 3      # Reduce h to sort smaller intervals
      return nShifts           # Return number of shifts
      

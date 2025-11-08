# Compute triangular numbers

def triangular_loop(nth): # Get the nth triangular number using a loop
   total = 0            # Keep a total of all the columns
   for n in range(nth, 0, -1): # Start at nth and go back to 1
      total += n        # add n (column height) to total
   return total         # Return the total of all the columns

def triangular(nth):    # Get the nth triangular number recursively
   if nth < 1: return 0 # For anything less than 1, it's 0
   return (nth +        # Otherwise add this column to the preceding
           triangular(nth - 1)) # triangular number

def triangular_rec(nth): # Get the nth triangular number - recursive
   return (0 if nth < 1 else # It's 0 for anything <1, else add nth to
           nth + triangular_rec(nth - 1)) # prec. triangular number

def show_triangular(nth): # Print the recursive execution steps of
   print('Computing triangular number #', nth) # computing the nth
   if nth < 1:            # triangular number.  Base case
      print('Base case. Returning 0') # Print the return information
      return 0
   value = nth + show_triangular(nth - 1) # Non-base case, get value
   print('Returning', value, 'for #', nth) # Print the return info
   return value

from LinkStack import *

def triangular_via_stack(nth): # Get the nth triangular number using
   todo = LinkStack()          # a stack of problem descriptions
   todo.push([nth, None])      # Description: nth and recursive result
   while not todo.isEmpty():   # Loop until no more problems to solve
      top = todo.peek()        # Look at topmost problem
      if top[1] is None:       # If recursive result is not solved,
         if top[0] < 1:        # check if top is base case
            top[1] = 0         # If so, then no recursion needed
         else:                 # Otherwise, solve smaller problem
            todo.push([top[0] - 1, None])
      else:                    # Topmost is solved
         top = todo.pop()      # Pop it off the stack
         if todo.isEmpty():    # If it was the last one,
            return top[1]      # then return the solution
         else:                 # Else add recursive call result to 
            caller = todo.peek() # caller's nth which is next on stack
            caller[1] = caller[0] + top[1]
   raise Exception("Stack empty without finding solution")

# Implement an infinite Fibonacci series as a Python generator

def Fibonacci():
   previous = 0
   current = 1
   while True:
      yield current
      next = previous + current
      previous = current
      current = next
      

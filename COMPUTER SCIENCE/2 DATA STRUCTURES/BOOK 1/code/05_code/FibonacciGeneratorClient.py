from FibonacciGenerator import *

count = 15
print('The first', count, 'numbers in the Fibonacci series are:')
for x in Fibonacci():
   if count < 1:
      break
   print(x)
   count -= 1
   

from Triangular import *

print('Testing triangular implementations')
functions = (triangular_loop, triangular, triangular_rec, triangular_via_stack)
for n in range(10):
   results = [func(n) for func in functions]
   results.append(n * (n + 1) // 2)
   if any(results[j] != results[j + 1] for j in range(len(results) - 1)):
      print('\nUh-oh.  Results are inconsistent for n = {}'.format(n))
      for func in functions:
         print(func.__name__, 'returns', func(n))
   else:
      print(n, end=' ')
print()
      

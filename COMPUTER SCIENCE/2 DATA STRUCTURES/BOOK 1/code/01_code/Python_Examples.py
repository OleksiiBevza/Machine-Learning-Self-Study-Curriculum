2**32 - 1

10**27 + 1

10**27 + 1.001

if 3 / 2 > 1:
   print("Bigger than 1")
else:
   print("Less than or equal to 1")

x = 9
if (x %
            2 == 0):
   if (x %
3 == 0):
      'Divisible by 6'
   else:
      'Divisible by 2'
else:
   if (x %
   3 == 0):
      'Divisible by 3'
   else:
      'Not divisible by 2 or 3'

x = 4
if (x %
            2 == 0):
   if (x %
3 == 0):
      'Divisible by 6'
else:
   if (x %
   3 == 0):
      'Divisible by 3'
   else:
      'Not divisible by 2 or 3'

total = 0
for x in [5, 4, 3, 2, 1]:
  total += x
total

height = [5, 4, 7, 2, 3]
weightedsum = 0
for i in range(len(height)):
   weightedsum += i * height[i]

weightedsum

for i, h in enumerate(height):
   weightedsum += i * h

weightedsum

x, y, z = 3, 4, 5
y
(x, y, z) = [7, 8, 9]
y

i, h = (0, 5)
weightedsum += i * h
i, h = (1, 4)
weightedsum += i * h
i, h = (2, 7)
weightedsum += i * h
i, h = (3, 2)
weightedsum += i * h
i, h = (4, 3)
weightedsum += i * h

left, middle, right = 'Elm', 'Asp', 'Oak'
left, middle, right
left, middle, right = middle, right, left
left, middle, right

left = middle = right = 'Gum'
left, middle, right

import math
math.pi
import os
os.path.splitext('myfile.ext')
filename, extension = os.path.splitext('myfile.ext')
extension

def weightedsum(values, weights, missing=0):
    sum = 0
    for i, val in enumerate(values):
       sum += val * (weights[i] if i < len(weights) else missing)
    return sum

weightedsum([4, 9, 16, 25], [2, 2])

weightedsum([4, 9, 16, 25], [2, 2], 1)

values = [7, 11, 13, 17, 19]
squares = []
for val in values:
    squares.append(val * val)

squares
[ x * x for x in values ]

[ x ** 3 for x in range(10, 21) ]

[ w.split('-') for w in ['ape', 'ape-man', 'hand-me-down'] ]

[ x ** 3 for x in range(10, 21) if x % 3 != 0 ]

[ c for c in 'We, the People...' if c.isalpha() ]



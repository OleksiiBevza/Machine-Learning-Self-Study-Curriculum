from TowerOfHanoi import *

# Test the exceptions
puzzle = TowerOfHanoi(2)
try:
   print('Trying to solve with', puzzle.height(0),
         'disks by asking to move', puzzle.height(0) + 1,
         'disks')
   puzzle.solve(nDisks=puzzle.height(0) + 1, show=True)
except Exception as e:
   print('Exception raised:', e)

try:
   print('Starting with puzzle:')
   print(puzzle)
   print('Trying to move a disk from', puzzle.label(1),
         'to', puzzle.label(2))
   puzzle.move(1, 2, True)
except Exception as e:
   print('Exception raised:', e)

   
for i in range(1, 4):
   puzzle = TowerOfHanoi(i)
   print('\nTower of Hanoi with', i, 'disks\n', puzzle)
   print('>>> TowerOfHanoi({}).solve(show=True)'.format(i))
   puzzle.solve(show=True)

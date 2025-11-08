from LinkStack import *

for stack in (LinkStack(), Stack()):
   print('\nInitial stack of type', type(stack),
         'holds:', stack, 'is empty =', stack.isEmpty())

   for i in range(5):
      stack.push(i ** 2)

   print('After pushing', len(stack), 
         'squares on to the stack, it contains', stack)
   print('The top of the stack is', stack.peek())

   while not stack.isEmpty():
      print('Popping', stack.pop(), 'off of the stack leaves',
            len(stack), 'item(s):', stack)

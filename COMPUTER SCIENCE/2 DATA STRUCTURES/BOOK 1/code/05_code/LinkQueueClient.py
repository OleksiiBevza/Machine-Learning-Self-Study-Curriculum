from LinkQueue import *

queue = Queue()

print('Initial queue:', queue, 'is empty =', queue.isEmpty())

for i in range(5):
   queue.enqueue(i ** 2)

print('After inserting', len(queue), 
      'squares on to the queue, it contains', queue)
print('The front of the queue is', queue.peek())

while not queue.isEmpty():
   print('Removing', queue.dequeue(), 'off of the queue leaves',
         len(queue), 'item(s):', queue)

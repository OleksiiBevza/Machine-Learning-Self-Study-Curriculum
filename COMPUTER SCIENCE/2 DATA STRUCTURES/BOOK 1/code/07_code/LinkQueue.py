# Implement a Queue data structure using a double ended linked list

from DoubleEndedList import *

class Queue(DoubleEndedList):            # Define queue by renaming
   enqueue = DoubleEndedList.insertLast  # Enqueue/insert at end
   dequeue = DoubleEndedList.deleteFirst # Dequeue/remove at first
   peek = DoubleEndedList.first          # Front of queue is first

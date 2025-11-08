from OrderedArray import *

maxSize = 11                  # Max size of the array
arr = OrderedArray(maxSize)   # Create the array object

arr.insert(77)                # Insert maxSize items
arr.insert(99)
arr.insert(44)                # Inserts not in order
arr.insert(55)
arr.insert(0)
arr.insert(12)
arr.insert(44)
arr.insert(99)
arr.insert(77)
arr.insert(0)
arr.insert(3)

print("Array containing", len(arr), "items:", arr)
   
arr.delete(0)                 # Delete a few items
arr.delete(99)
arr.delete(0)                 # Duplicate deletes
arr.delete(0)
arr.delete(3)

print("Array after deletions has", len(arr), "items:", arr)

print("find(44) returns", arr.find(44))
print("find(46) returns", arr.find(46))
print("find(77) returns", arr.find(77))

while len(arr) <= maxSize:    # Fill then overflow array
   try:
      arr.insert(len(arr))    # Insert the array's length
      print("After insert, array has", len(arr), "items")
   except Exception as e:
      print("Attempt to insert", len(arr), "failed")
      print("Array contains:", arr)
      print(e)
      break

from OrderedRecordArray import *

def second(x):                # Key on second element of record
    return x[1]

maxSize = 1000                             # Max size of the array
arr = OrderedRecordArray(maxSize, second)  # Create the array object

# Insert 10 items
for rec in [('a', 3.1), ('b', 7.5), ('c', 6.0), ('d', 3.1),
            ('e', 1.4), ('f', -1.2), ('g', 0.0), ('h', 7.5),
            ('i', 7.5), ('j', 6.0)]:
    arr.insert(rec)

print("Array containing", len(arr), "items:\n", arr)

# Delete a few items, including some duplicates
for rec in [('c', 6.0), ('g', 0.0), ('g', 0.0), 
            ('b', 7.5), ('i', 7.5)]:
    print("Deleting", rec, "returns", arr.delete(rec))

print("Array after deletions has", len(arr), "items:\n", arr)

for key in [-9.9, 4.4, 6.0, 7.5, 9.9]:
    index = arr.find(key)
    print("find(", key, ") returns", index,
          "and get(", index, ") returns", 
          arr.get(index) if index < len(arr) else '<out of bounds>')

# Second example - use simple integers to illustrate recursive binary
# search
arr = OrderedRecordArray(10)
for item in [3, 27, 14, 10, 88, 41, 67, 51, 95]:
   arr.insert(item)

print("Array containing", len(arr), "items:\n", arr)

for goal in [0, 10, 11, 99]:
   print("find(", goal, ") returns", arr.find(goal))

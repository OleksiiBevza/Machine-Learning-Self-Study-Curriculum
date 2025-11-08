# Example to demonstrate counting sort

keys = [67, 41, 64, 58, 69, 5, 2, 21, 95, 74, 25, 10, 98, 15, 64]
print('Original array of', len(keys), 'keys:\n', keys)

# Sort on 1s digit
sort1 = sorted(keys, key=lambda x: x % 10)
print('After sorting the keys on the 1s digit:\n', sort1)

# Counting the 10s digit
keysBy10s = [sum(1 if k // 10 == i else 0 for k in sort1) for i in range(10)]

# Cumulative counts by the 10s digit
cumulativeBy10s = [
   sum(1 if k // 10 <= i else 0 for k in sort1) for i in range(10)]
fmt = '{:2d}'
print('10s Digit   ', *(fmt.format(i) for i in range(10)))
print('Key Count   ', *(fmt.format(c) for c in keysBy10s))
print('Cumulative  ', *(fmt.format(c) for c in cumulativeBy10s))

# Sort on 10s digit
sort10 = sorted(sort1, key=lambda x: x // 10)
print('After sorting the keys on the 10s digit:\n', sort10)



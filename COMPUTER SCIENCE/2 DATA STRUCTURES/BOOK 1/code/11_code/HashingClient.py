from Hashing import *
import sys
from collections import *

word = "elf" if len(sys.argv) < 2 else sys.argv[1]
code = encode_word(word)
print('Simple encoding of', repr(word), 'is', code)
wordlistfile = '/usr/share/dict/words'
countlimit = 100
simulatedhash = defaultdict(lambda : list())
hashtablesize = 100000

print('Checking up to', countlimit, 
      'words whose simple enoding is', code, 
      'in', wordlistfile)
count = 0
with open(wordlistfile, 'r') as wordlist:
   for line in wordlist:
      w = line.strip() 
      if ('a' <= w[0] and len(w) <= 10 and w != word and
          encode_word(w) == code):
         count += 1
         if count < countlimit:
            print(w)
      if 'a' <= w[0]:
         unique_code = unique_encode_word(w) % hashtablesize
         simulatedhash[unique_code].append(w)
print(count, 'words in', wordlistfile, 
      'have the simple encoding of', code)

count = 0
collisions = 2
inspect = 'abductor'

print('Showing up to', countlimit, 
      'hash table cells having more than', collisions,
      'entries using the unique encoding hashed into',
      hashtablesize, 'cells')
for key in simulatedhash:
   if inspect in simulatedhash[key]:
      inspectcode = key
   if len(simulatedhash[key]) > collisions:
      if count < countlimit:
         print('The keys', simulatedhash[key], 'all hash to',
               key)
      count += 1

nearby = 5
print('Hashtable codes within', nearby, 'of', repr(inspect),
      'whose code is', inspectcode)
for code in range(inspectcode - nearby, inspectcode + nearby + 1):
   print('{:7d}: {}'.format(
      code, simulatedhash[code] if code in simulatedhash else ''))

wordseq = [word] if len(sys.argv) < 2 else sys.argv[1:]
for word in wordseq:
   print('Unique encoding of', repr(word), 'is',
         unique_encode_word(word),
         'and bitHash is 0x{:x}'.format(bitHash(word)))
   if word.isdigit():
      print('The bitHash of the integer', int(word), 
            'is 0x{:x}'.format(bitHash(int(word))))

print('The bitHash of the sequence', wordseq,
      'is 0x{:x}'.format(bitHash(wordseq)))

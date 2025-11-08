# Compute the anagrams of a string of characters

def anagrams(word):            # Return a list of anagrams for word
   if len(word) <= 1:          # Empty words and single letters
      return [word]            # have a single anagram, themselves
   result = []                 # Start with an empty list
   for part in anagrams(word[1:]): # Loop over smaller anagrams
      for i in range(len(part) + 1): # For each index in smaller word
         result.append(        # Add a new anagram with
            part[:i] +         # the smaller word up to the index
            word[0] +          # plus the 1st character of this word
            part[i:])          # plus the rest of the smaller word
   return result               # Return the list of bigger anagrams

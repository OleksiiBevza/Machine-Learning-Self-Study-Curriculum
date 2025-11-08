# A program to reverse the letters of a word

from SimpleStack import *

stack = Stack(100)          # Create a stack to hold letters

word = input("Word to reverse: ")

for letter in word:         # Loop over letters in word
   if not stack.isFull():   # Push letters on stack if not full
      stack.push(letter)
    
reverse = ''                # Build the reversed version
while not stack.isEmpty():  # by popping the stack until empty
   reverse += stack.pop()

print('The reverse of', word, 'is', reverse)

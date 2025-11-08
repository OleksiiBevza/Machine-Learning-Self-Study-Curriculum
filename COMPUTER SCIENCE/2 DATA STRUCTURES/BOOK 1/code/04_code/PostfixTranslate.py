from SimpleStack import Stack
from Queue import Queue

# Define operators and their precedence
# We group single character operators of equal precedence in strings
# Lowest precedence is on the left; highest on the right
# Parentheses are treated as high precedence operators
operators = ["|", "&", "+-", "*/%", "^", "()"]
def precedence(operator):  # Get the precedence of an operator
   for p, ops in enumerate(operators):  # Loop through operators
      if operator in ops:               # If found,
         return p + 1                   # return precedence (low = 1)
      # else not an operator, return None
        
def delimiter(character):   # Determine if character is delimiter
   return precedence(character) == len(operators)

def nextToken(s):           # Parse next token from input string
   token = ""               # Token is operator or operand
   s = s.strip()            # Remove any leading & trailing space
   if len(s) > 0:           # If not end of input
      if precedence(s[0]):  # Check if first char. is operator
         token = s[0]       # Token is a single char. operator
         s = s[1:]
      else:                 # its an operand, so take characters up
         while len(s) > 0 and not (   # to next operator or space
                precedence(s[0]) or s[0].isspace()):
            token += s[0]
            s = s[1:]
   return token, s  # Return the token, and remaining input string

def PostfixTranslate(formula): # Translate infix to Postfix
   postfix = Queue(100)     # Store postfix in queue temporarily
   s = Stack(100)           # Parser stack for operators
    
   # For each token in the formula  (fencepost loop)
   token, formula = nextToken(formula)
   while token:
      prec = precedence(token)  # Is it an operator?
      delim = delimiter(token)  # Is it a delimiter?
      if delim:
         if token == '(':   # Open parenthesis
            s.push(token)   # Push parenthesis on stack
         else:              # Closing parenthesis
            while not s.isEmpty(): # Pop items off stack
               top = s.pop()
               if top == '(':      # Until open paren found
                  break
               else:               # and put rest in output
                  postfix.insert(top)
                        
      elif prec:            # Input token is an operator
         while not s.isEmpty(): # Check top of stack
            top = s.pop()
            if (top == '(' or   # If open parenthesis, or a lower
                precedence(top) < prec): # precedence operator
                s.push(top)     # push it back on stack and
                break           # stop loop
            else:               # Else top is higher precedence
                postfix.insert(top) # operator, so output it
         s.push(token)          # Push input token (op) on stack

      else:                     # Input token is an operand
         postfix.insert(token)  # and goes straight to output
        
      token, formula = nextToken(formula) # Fencepost loop
    
   while not s.isEmpty():       # At end of input, pop stack
      postfix.insert(s.pop())   # operators and move to output

   ans = ""
   while not postfix.isEmpty(): # Move postfix items to string
      if len(ans) > 0:
         ans += " "             # Separate tokens with space
      ans += postfix.remove()
   return ans

if __name__ == '__main__':
    infix_expr = input("Infix expression to translate: ")
    print("The postfix representation of", infix_expr, "is:",
          PostfixTranslate(infix_expr))

from PostfixTranslate import *
from SimpleStack import *

def PostfixEvaluate(formula):  # Translate infix to Postfix and
                               # evaluate the result

   postfix = PostfixTranslate(formula) # Postfix string
   s = Stack(100)                      # Operand stack
    
   token, postfix = nextToken(postfix)
   while token:
      prec = precedence(token)  # Is it an operator?

      if prec:                  # If input token is an operator
         right = s.pop()        # Get left and right operands
         left = s.pop()         # from stack
         if token == '|':       # Perform operation and push
            s.push(left | right)
         elif token == '&':
            s.push(left & right)
         elif token == '+':
            s.push(left + right)
         elif token == '-':
            s.push(left - right)
         elif token == '*':
            s.push(left * right)
         elif token == '/':
            s.push(left / right)
         elif token == '%':
            s.push(left % right)
         elif token == '^':
            s.push(left ^ right)
                
      else:                     # Else token is operand
         s.push(int(token))     # Convert to integer and push
            
      print('After processing', token, 'stack holds:', s)
        
      token, postfix = nextToken(postfix) # Fencepost loop

   print('Final result =', s.pop()) # At end of input, print result

if __name__ == '__main__':
   infix_expr = input("Infix expression to evaluate: ")
   print("The postfix representation of", infix_expr, "is",
         PostfixTranslate(infix_expr))
   PostfixEvaluate(infix_expr)

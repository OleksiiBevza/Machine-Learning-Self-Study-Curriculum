from PostfixTranslate import *
from SimpleStack import *
from operator import *
operators = {
    '+': add, '-': sub, '/': truediv, '*': mul, '%': mod,
    '&': and_, '|': or_, '^': xor,
}

def PostfixEvaluate(formula):  # Translate infix to Postfix and
                               # evaluate the result

    postfix = PostfixTranslate(formula) # Postfix string
    s = Stack(100)                      # Operand stack
    
    token, postfix = nextToken(postfix)
    while token:
        prec = precedence(token)  # Is it an operator?

        if prec:                  # If input token is an operator
            right = s.pop()       # Get left and right operands
            left = s.pop()        # from stack
            s.push(operators[token](left, right)) # Perform operation and push
                
        else:                    # Else token is operand
            s.push(eval(token))  # Convert to number and push
            
        print('After processing', token, 'stack holds:', s)
        
        token, postfix = nextToken(postfix) # Fencepost loop

    print('Final result =', s.pop()) # At end of input, print result

if __name__ == '__main__':
    infix_expr = input("Infix expression to evaluate: ")
    print("The postfix representation of", infix_expr, "is",
          PostfixTranslate(infix_expr))
    PostfixEvaluate(infix_expr)

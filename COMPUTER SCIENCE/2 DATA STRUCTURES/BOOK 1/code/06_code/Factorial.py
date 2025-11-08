# Compute factorial numbers

def factorial(n):            # Get factorial of n
   if n < 1: return 1        # It's 1 for anything < 1
   return (n *               # Otherwise, multiply n 
           factorial(n - 1)) # by preceding factorial

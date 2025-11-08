# Test the BinarySearchTree class interactively
from BinarySearchTree import *

theTree = BinarySearchTree()  # Start with an empty tree

theTree.insert("Don",  "1974 1")  # Insert some data
theTree.insert("Herb", "1975 2")
theTree.insert("Ken",  "1979 1")
theTree.insert("Ivan", "1988 1")
theTree.insert("Raj",  "1994 1")
theTree.insert("Amir", "1996 1")
theTree.insert("Adi",  "2002 3")
theTree.insert("Ron",  "2002 3")
theTree.insert("Fran", "2006 1")
theTree.insert("Vint", "2006 2")
theTree.insert("Tim",  "2016 1")

def print_commands(names):    # Print a list of possible commands
   print('The possible commands are', names)

def clearTree():              # Remove all the nodes in the tree
   while not theTree.isEmpty():
      data, key = theTree.root()
      theTree.delete(key)
      
def traverseTree(traverseType="in"):  # Traverse & print all nodes
   for key, data in theTree.traverse(traverseType):
      print('{', str(key), ', ', str(data), '}', end=' ')
   print()

commands = [  # Command names, functions, and their parameters
   ['print', theTree.print, []],
   ['insert', theTree.insert, ('key', 'data')],
   ['delete', theTree.delete, ('key', )],
   ['search', theTree.search, ('key', )],
   ['traverse', traverseTree, ('type', )],
   ['clear', clearTree, []],
   ['help', print_commands, []],
   ['?', print_commands, []],
   ['quit', None, []],
]
# Collect all the command names in a list
command_names = ", ".join(c[0] for c in commands)
for i in range(len(commands)): # Put command names in argument list
   if commands[i][1] == print_commands: # of print_commands
      commands[i][2] = [command_names]
# Create a dictionary mapping first character of command name to
# command specification (name, function, parameters/args)
command_dict = dict((c[0][0], c) for c in commands)

# Print information for interactive loop
theTree.print()
print_commands(command_names)
ans = ' '

# Loop to get a command from the user and execute it
while ans[0] != 'q':
   print('The tree has', theTree.nodes(), 'nodes across',
         theTree.levels(), 'levels')
   ans = input("Enter first letter of command: ").lower()
   if len(ans) == 0:
      ans = '?'
   if ans[0] in command_dict:
      name, function, parameters = command_dict[ans[0]]
      if function is not None:
         print(name)
         if isinstance(parameters, list):
            arguments = parameters
         else:
            arguments = []
            for param in parameters:
               arg = input("Enter " + param + " for " + name + " " +
                           "command: ")
               arguments.append(arg)
         try:
            result = function(*arguments)
            print('Result:', result)
         except Exception as e:
            print('Exception occurred')
            print(e)
   else:
      print("Invalid command: '", ans, "'")

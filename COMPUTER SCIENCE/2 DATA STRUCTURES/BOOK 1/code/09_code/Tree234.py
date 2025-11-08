# Implement 2-3-4 trees using Tree and Node classes
# Nodes contain up to 3 key-data pairs and up to 4 child links

from LinkStack import *

class Tree234(object):        # A 2-3-4 multiway tree class

   maxLinks = 4               # Maximum number of child links
   maxKeys = maxLinks - 1     # Maximum number of key-value pairs
   
# To preserve node integrity, node keys and children links should
# not be accessible from the caller, so we make the entire
# Node class hidden, but leave its attributes public for ease
# of manipulating them in the Tree class

   class __Node(object):      # A node in a 2-3-4 tree
      def __init__(           # Constructor takes a key-data pair
            self,             # since every node must have 1 item
            key,              # It also takes a list of children,
            data,             # either empty or a pair that must
            *children):       # both be of __Node type.
         valid = [x for x in children # Extract valid child links
                  if isinstance(x, type(self))]
         if len(valid) not in (0, 2): # Check number of children
            raise ValueError(
               "2-3-4 tree nodes must be created with 0 or 2 children")
         self.nKeys = 1       # Exactly 1 key-data pair is kept
         self.keys = [key] * Tree234.maxKeys # Store array of keys
         self.data = [data] * Tree234.maxKeys # Store array of values
         self.nChild = len(valid) # Store number of children
         self.children = (    # Store list of child links
            valid + [None] * (Tree234.maxLinks - len(valid)))

      def __str__(self):      # Represent a node as a string of keys
         return '<Node234 ' + '-'.join( # joined by hyphens w/ prefix
            str(k) for k in self.keys[:self.nKeys]) + '>'
      
      def isLeaf(self):       # Test for leaf nodes
         return self.nChild == 0

      def insertKeyValue(     # Insert a key value pair into the
            self,             # sorted list of keys. If key is already
            key,              # in list, its value will be updated.
            data,             # If key is not in list, add new subtree
            subtree=None):    # if provided, just after the new key
         i = 0                # Start looking at lowest key
         while (i < self.nKeys and # Loop until i points to a key
                self.keys[i] < key): # equal or greater than goal
            i += 1            # Advance to next key
         if i == Tree234.maxKeys: # Check if goal is beyond capacity
            raise Exception(
               'Cannot insert key into full 2-3-4 node')
         if self.keys[i] == key: # If the key is already in keys
            self.data[i] = data # then update value of this key
            return False      # Return flag: no new key added 
         j = self.nKeys       # Otherwise point j at highest key
         if j == Tree234.maxKeys: # Before shifting keys,
            raise Exception(  # raise exception if keys are maxed out
               'Cannot insert key into full 2-3-4 node')
         while i < j:         # Loop over keys higher than key i
            self.keys[j] = self.keys[j-1] # and shift keys, values
            self.data[j] = self.data[j-1] # and children to right
            self.children[j+1] = self.children[j]
            j -= 1            # Advance to lower key
         self.keys[i] = key   # Put new key and value in hole created
         self.data[i] = data  # by shifting array contents
         self.nKeys += 1      # Increment number of keys
         if subtree:          # If a subtree was provided, store it
            self.children[i + 1] = subtree # in hole created
            self.nChild += 1  # This node now has one more child
         return True          # Return flag: a new key was added

   def __init__(              # The 2-3-4 tree organizes items in 
         self):               # nodes by their keys.
      self.__root = None      # Tree starts empty.
   
   def isEmpty(self):         # Check for empty tree
      return self.__root is None

   def root(self):            # Get the data and keys of the root node
      if self.isEmpty():      # If the tree is empty, raise exception
         raise Exception("No root node in empty tree")
      nKeys = self.__root.nKeys # Get active key count
      return (                # Otherwise return root data and key
         self.__root.data[:nKeys], # arrays shortened to current
         self.__root.keys[:nKeys]) # active keys
      
   def __find(self,           # Find a node with a key that matches
              goal,           # the goal and its parent node.
              current, parent, # Start at current and track its parent
              prepare=True):  # Prepare nodes for insertion, if asked
      if current is None:     # If there is no tree left to explore,
         return (current, parent) # then return without finding node
      i = 0                   # Index to keys of current node
      while (i < current.nKeys and # Loop through keys in current
             current.keys[i] < goal): # node to find goal
         i += 1
      if (i < current.nKeys and   # If key i is valid and matches goal
          goal == current.keys[i]):
         return (current, parent) # return current node & parent
      if (prepare and         # If asked to prepare for insertion and
          current.nKeys == Tree234.maxKeys): # node is full,
         current, parent = self.__splitNode( # then split node, update
            current, parent, goal) # current and parent, and adjust i
         i = 0 if goal < current.keys[0] else 1 # for new current
      return ((prepare and current, parent) # Return current if
              if current.isLeaf() else # it's a leaf being prepared
              self.__find(    # Otherwise continue search recursively
                 goal,        # to find goal
                 current.children[i], # in the ith child of current
                 current, prepare))   # and current as parent

   def __splitNode(           # Split a full node during top-down
         self,                # find operation.  
         toSplit,             # Node to split (current)
         parent,              # Parent of node to split (or tree)
         goal):               # Goal key to find
      if toSplit.isLeaf():    # Make new node for Key 2, either as a
         newNode = self.__Node( # leaf node
            toSplit.keys[2],  # with key 2 and value 2 as its
            toSplit.data[2])  # sole key-value pair
      else:
         newNode = self.__Node( # or as an internal node
            toSplit.keys[2],  # with key 2 and value 2 as its
            toSplit.data[2],  # sole key-value pair and the highest
            *toSplit.children[2:toSplit.nChild]) # 2 child links
      toSplit.nKeys = 1       # Only key 0 and data 0 are kept in
      toSplit.nChild = max(   # node to split and child count is
         0, toSplit.nChild - 2) # either 0 or 2
      if parent is self:      # If parent is empty (top of 2-3-4 tree)
         self.__root = self.__Node( # make a new root node
            toSplit.keys[1],  # with key 1 and value 1
            toSplit.data[1],  # and the node to split plus new node
            toSplit, newNode) # as child nodes
         parent = self.__root # New root becomes parent
      else:                   # For existing parent node,
         parent.insertKeyValue( # insert key 1 in parent with 
            toSplit.keys[1],  # new node as its higher subtree
            toSplit.data[1], newNode)
      return (toSplit         # Find resumes at node to split if goal
              if goal < toSplit.keys[1] # is less than key 1
              else newNode,   # else new node
              parent)         # Parent is either new root or same
         
   def search(self, goal):    # Public method to get data associated
      node, p = self.__find(  # with a goal key. First, find node
         goal, self.__root,   # starting at root with self as parent
         self, prepare=False) # without splitting any nodes
      if node:                # If node was found, return appropriate
         return node.data[    # data. It's the first data (index 0) if
            0 if node.nKeys < 2 or # there's only 1 key or
            goal < node.keys[1] else  # if the goal < key 1, else it's
            1 if goal == node.keys[1] # the 2nd data if goal == key 1
            else 2]                   # Otherwise it's the 3rd data

   def insert(self,           # Insert a new key-value pair in a 
              key,            # 2-3-4 tree by finding the node where
              value):         # it belongs, possibly splitting nodes
      node, p = self.__find(  # First, find insertion node for key
         key, self.__root,    # starting at root with self as parent
         self, prepare=True)  # and splitting full nodes
      if node is None:        # If no node was found for insertion
         if p is self:        # Check if the parent is the tree
            self.__root = self.__Node( # Make a root node with just
               key, value)    # 1 key value pair
            return True       # and return True for node creation
         raise Exception(     # If not root, then something is wrong
            '__find did not find 2-3-4 node for insertion')
      return node.insertKeyValue( # Otherwise, insert key in node
         key, value)          # with no subtree, returning insert flag

   def traverse(self,         # Traverse the tree in pre, in, or post
                traverseType="in"): # order based on type
      if traverseType not in [ # Verify traversal type is an
            'pre', 'in', 'post']: # accepted value
         raise ValueError(
            "Unknown traversal type: " + str(traverseType))
      
      stack = Stack()         # Create a stack
      stack.push(self.__root) # Put root node in stack
      
      while not stack.isEmpty(): # While there is work in the stack
         item = stack.pop()   # Get next item
         if isinstance(item, self.__Node): # If it's a tree node
            last = max(       # Find last child or last key index
               item.nChild,   # going 1 past last key for post order
               item.nKeys + (1 if traverseType == 'post' else 0))
            for c in range(last - 1, -1, -1): # Loop in reverse
               if (traverseType == 'post' and # For post-order, push
                   0 < c and c - 1 < item.nKeys): # last data item
                  stack.push((item.keys[c - 1], item.data[c - 1]))
               if (traverseType == 'in' and # For in-order, push
                   c < item.nKeys): # valid data items to yield
                  stack.push((item.keys[c], item.data[c]))
               if c < item.nChild: # For valid child links,
                  stack.push(item.children[c]) # traverse child
               if (traverseType == 'pre' and # For pre-order, push
                   c < item.nKeys): # valid data items to yield
                  stack.push((item.keys[c], item.data[c]))
         elif item:           # Every other non-None item is a
            yield item        # (key, data) pair to be yielded
   
   def print(self,            # Print a tree sideways with 1 key
             indentBy=4):     # on each line and indenting each level
      self.__pTree(self.__root, # by some blanks.  Start at root node
                   "", indentBy) # with no indent
       
   def __pTree(self,          # Recursively print a 2-3-4 subtree,
               node,          # sideways with the root node left 
               indent,        # justified; indent shows its level
               indentBy=4):   # Increase indent level for subtrees
      if node:                # Only print if there is a node
         for c in range(      # Loop through children and keys from 
               max(node.nKeys, node.nChild) - 1, # highest to
               -1, -1):       # lowest
            if c < node.nKeys: # Only print valid keys
               print(indent + str(node) + # Print key and value after
                     ': ' + str(node.keys[c]) + # indent prefix 
                     '->' + str(node.data[c]))
            if c < node.nChild: # Only print valid child subtrees
               self.__pTree(node.children[c],
                            indent + " " * indentBy, indentBy)

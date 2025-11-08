# Implement AVL trees using Tree and Node classes
# These are balanced binary trees

from LinkStack import *
    
class AVLtree(object):

# To preserve node integrity, node keys and children links should
# not be accessible from the caller, so we make the entire
# Node class hidden, but leave its attributes public for ease
# of manipulating them in the Tree class

   class __Node(object):      # A node in an AVL tree
      def __init__(           # Constructor takes a key-data pair
            self,             # since every node must have 1 item
            key, data):
         self.key, self.data = key, data # Store item key & data
         self.left = self.right = None   # Empty child links
         self.updateHeight()  # Set initial height of node
    
      def updateHeight(self): # Update height of node from children
         self.height = max(   # Get maximum child height using 0 for
            child.height if child else 0 # empty child links
            for child in (self.left, self.right)
         ) + 1                # Add 1 for this node
     
      def heightDiff(self):   # Return difference in child heights
         left  = self.left.height  if self.left  else 0
         right = self.right.height if self.right else 0
         return left - right  # Return difference in heights

      def __str__(self):      # Represent a node as a string using a
         return 'AVL>' + str(self.key) # prefix and its key
     
   def __init__(self):        # Constructor for empty AVL tree
      self.__root = None      # No root node in empty tree

   def isEmpty(self):         # Check for empty tree
      return self.__root is None

   def __find(self, goal, node): # Find a node that matches goal key
      while node is not None: # Loop until we reach an empty link
         if node.key == goal: # Check if current node's key matches
            return node       # and return it if it does
         elif goal < node.key: # Else if goal is below current node,
            node = node.left  # then search left subtree
         else:
            node = node.right # Else search the right subtree
      return None             # If loop ends, goal wasn't found

   def search(self, goal):    # Search for an item whose key matches a
      node = self.__find(goal, self.__root) # goal starting at root
      if node is not None:    # Return the node's data, if found
         return node.data
   
   def insert(self, key, data): # Insert an item into the AVL tree
      self.__root, flag = self.__insert( # Reset the root to be the
         self.__root, key, data) # modified tree and return the
      return flag             # the insert vs. update flag
      
   def __insert(self,         # Insert an item into an AVL subtree
                node,         # rooted a particular node, returning
                key, data):   # the modified node & insertion flag
      if node is None:        # For an empty subtree, return a new
         return self.__Node(key, data), True # node in the tree
      
      if key == node.key:     # If node already has the insert key,
         node.data = data     # then update it with the new data
         return node, False   # Return the node and False for flag
          
      elif key < node.key:    # Does the key belong in left subtree?
         node.left, flag = self.__insert( # If so, insert on left and
            node.left, key, data) # update the left link
         if node.heightDiff() > 1: # If insert made node left heavy

            if node.left.key < key: # If inside grandchild inserted,
               node.left = self.rotateLeft( # then raise grandchild
                  node.left) 
                   
            node = self.rotateRight( # Correct left heavy tree by
               node)          # rotating right around this node
          
      else:                   # Otherwise key belongs in right subtree
         node.right, flag = self.__insert( # Insert it on right and
            node.right, key, data) # update the right link
         if node.heightDiff() < -1: # If insert made node right heavy

            if key < node.right.key: # If inside grandchild inserted,
               node.right = self.rotateRight( # then raise grandchild
                  node.right) 
                   
            node = self.rotateLeft( # Correct right heavy tree by
               node)          # rotating left around this node
       
      node.updateHeight()     # Update this node's height
      return node, flag       # Return the updated node & insert flag

   def rotateRight(self, top): # Rotate a subtree to the right
      toRaise = top.left      # The node to raise is top's left child
      top.left = toRaise.right # The raised node's right crosses over
      toRaise.right = top     # to be the left subtree under the old
      top.updateHeight()      # top.  Then the heights must be updated
      toRaise.updateHeight()
      return toRaise          # Return raised node to update parent

   def rotateLeft(self, top): # Rotate a subtree to the left
      toRaise = top.right     # The node to raise is top's right child
      top.right = toRaise.left # The raised node's left crosses over
      toRaise.left = top      # to be the right subtree under the old
      top.updateHeight()      # top.  Then the heights must be updated
      toRaise.updateHeight()
      return toRaise          # Return raised node to update parent

   def traverse(self,         # Non-recursive generator to traverse
                traverseType='in'): # tree in pre, in, or post order
      if traverseType not in [ # Verify traversal type is an
            'pre', 'in', 'post']: # accepted value
         raise ValueError(
            "Unknown traversal type: " + str(traverseType))
      
      stack = Stack()         # Create a stack
      stack.push(self.__root) # Put root node in stack
      
      while not stack.isEmpty(): # While there is work in the stack
         item = stack.pop() # Get next item
         if isinstance(item, self.__Node): # If it's a tree node
            if traverseType == 'post': # For post-order, put it last
               stack.push((item.key, item.data))
            stack.push(item.right) # Traverse right child
            if traverseType == 'in': # For pre-order, put item 2nd
               stack.push((item.key, item.data))
            stack.push(item.left)  # Traverse left child
            if traverseType == 'pre': # For pre-order, put item 1st
               stack.push((item.key, item.data))
         elif item:           # Every other non-None item is a
            yield item        # (key, value) pair to be yielded

   def print(self,            # Print a tree sideways with 1 node
             indentBy=4):     # on each line and indenting each level
      self.__pTree(self.__root, # by some blanks.  Start at root node
                   "", indentBy) # with no indent
       
   def __pTree(self,          # Recursively print a subtree, sideways 
               node,          # with the root node left justified
               indent,        # using indent as prefix for its level
               indentBy=4):   # Increase indent level for subtrees
      if node:                # Only print if there is a node
         self.__pTree(node.right,  # Print the right subtree
                      indent + " " * indentBy, indentBy)
         print(indent, node, '(',  # Print this node, its height, &
               node.height, node.heightDiff(), ')') # balsnce
         self.__pTree(node.left,   # Print the left subtree
                      indent + " " * indentBy, indentBy)
         
   def __str__(self):         # Show tree in string form as key-value
      return '{{{}}}'.format( # pairs surrounded in curly braces
         ', '.join('{}: {}'.format( # Pairs are formatted key: value
            repr(key), repr(val))
                   for key, val in self.traverse('pre')))
   
   def delete(self, goal):    # Delete a node whose key matches goal
      self.__root, flag = self.__delete( # Delete starting at root and
         self.__root, goal)   # update root link
      return flag             # Return flag indicating goal node found
      
   def __delete(self,         # Delete matching goal key from subtree
                node, goal):  # rooted at node. Return modified node
      if node is None:        # If subtree is empty,
         return None, False   # then no matching goal key
      
      if goal < node.key:     # Is node to delete in left subtree?
         node.left, flag = self.__delete( # If so, delete from left
            node.left, goal)  # update the left link and store flag
         node = self.__balanceLeft(node) # Correct any imbalance

      elif goal > node.key:   # Is node to delete in right subtree?
         node.right, flag = self.__delete( # If so, delete from right
            node.right, goal) # update the right link and store flag
         node = self.__balanceRight(node) # Correct any imbalance
            
      # Else node's key matches goal, so determine deletion case
      elif node.left is None: # If no left child, return right child
         return node.right, True # as remainder, flagging deletion
      elif node.right is None: # If no right child, return left child
         return node.left, True # as remainder, flagging deletion
      # Deleted node has two children so find successor in right
      else:                   # subtree and replace this item 
         node.key, node.data, node.right= self.__deleteMin(node.right)
         node = self.__balanceRight(node) # Correct any imbalance
         flag = True          # The goal was found and deleted

      node.updateHeight()     # Update height of node after deletion
      return node, flag       # Return modified node and delete flag

   def __deleteMin(           # Find minimum node of subtree, delete
         self,                # it, return minimum key, data pair and
         node):               # updated link to parent
      if node.left is None:   # If left child link is empty, then
         return (node.key, node.data, # this node is minimum and its
                 node.right)  # right subtree, if any, replaces it
      key, data, node.left = self.__deleteMin( # Else, delete minimum
         node.left)           # from left subtree
      node = self.__balanceLeft(node) # Correct any imbalance
      node.updateHeight()     # Update height of node
      return (key, data, node)
         
   def __balanceLeft(self, node): # Rebalance after left deletion
      if node.heightDiff() < -1: # If node is right heavy, then
         if node.right.heightDiff() > 0: # If the right child is left
            node.right = self.rotateRight( # heavy, then rotate
               node.right)    # it to the right first
            
         node = self.rotateLeft( # Correct right heavy tree by
            node)             # rotating left around this node
      return node             # Return top node

   def __balanceRight(self, node): # Rebalance after right deletion
      if node.heightDiff() > 1: # If node is left heavy, then
         if node.left.heightDiff() < 0: # If the left child is right
            node.left = self.rotateLeft( # heavy, then rotate
               node.left)     # it to the left first
            
         node = self.rotateRight( # Correct left heavy tree by
            node)             # rotating right around this node
      return node             # Return top node

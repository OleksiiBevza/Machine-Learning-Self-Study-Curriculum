# Implement a nondirectional graph using classes for vertices and edges

class Vertex(object):       # A vertex in a graph
   def __init__(self, name): # Constructor: stores a vertex name
      self.name = name      # Store the name

   def __str__(self):       # Summarize vertex in a string
      return '<Vertex {}>'.format(self.name)

class Graph(object):        # A graph containing vertices and edges
   def __init__(self):      # Constructor
      self._vertices = []   # A list/array of vertices
      self._adjMat = {}     # A hash table mapping vertex pairs to 1

   def nVertices(self):     # Get the number of graph vertices, i.e.
      return len(self._vertices) # the length of the vertices list

   def nEdges(self):        # Get the number of graph edges by 
      return len(self._adjMat) // 2 # dividing the # of keys by 2

   def __str__(self):       # Summarize the graph in a string
      nVertices = self.nVertices()
      nEdges = self.nEdges()
      return '<Graph of {} vert{} and {} edge{}>'.format(
         nVertices, 'ex' if nVertices == 1 else 'ices',
         nEdges, '' if nEdges == 1 else 's')
   
   def addVertex(self, vertex): # Add a new vertex to the graph
      self._vertices.append(vertex) # Place at end of vertex list

   def validIndex(self, n): # Check that n is a valid vertex index
      if n < 0 or self.nVertices() <= n: # If it lies outside the
         raise IndexError   # valid range, raise an exception
      return True           # Otherwise it's valid
   
   def getVertex(self, n):  # Get the nth vertex in the graph
      if self.validIndex(n): # Check that n is a valid vertex index
         return self._vertices[n] # and return nth vertex

   def addEdge(self, A, B): # Add an edge between two vertices A & B
      self.validIndex(A)    # Check that vertex A is valid
      self.validIndex(B)    # Check that vertex B is valid
      if A == B:            # If vertices are the same
         raise ValueError   # raise exception
      self._adjMat[A, B] = 1 # Add edge in one direction and
      self._adjMat[B, A] = 1 # the reverse direction

   def hasEdge(self, A, B): # Check for edge between vertices A & B
      self.validIndex(A)    # Check that vertex A is valid
      self.validIndex(B)    # Check that vertex B is valid
      return self._adjMat.get( # Look in adjacency matrix hash table
         (A, B), False)     # Return either the edge count or False

   def vertices(self):      # Generate sequence of all vertex indices
      return range(self.nVertices()) # Same as range up to nVertices
   
   def adjacentVertices(    # Generate a sequence of vertex indices
         self, n):          # that are adjacent to vertex n
      self.validIndex(n)    # Check that vertex n is valid
      for j in self.vertices(): # Loop over all other vertices
         if j != n and self.hasEdge(n, j): # If other vertex connects
            yield j         # via edge, yield other vertex index
            
   def adjacentUnvisitedVertices( # Generate a sequence of vertex
         self, n,           # indices adjacent to vertex n that do
         visited,           # not already show up in the visited list
         markVisits=True):  # and mark visits in list, if requested
      for j in self.adjacentVertices(n): # Loop through adjacent 
         if not visited[j]: # vertices, check visited
            if markVisits:  # flag, and if unvisited, optionally
               visited[j] = True # mark the visit
            yield j         # and yield the vertex index

   def depthFirst(          # Traverse the vertices in depth-first
         self, n):          # order starting at vertex n
      self.validIndex(n)    # Check that vertex n is valid
      visited = [False] * self.nVertices() # Nothing visited initially
      stack = Stack()       # Start with an empty stack 
      stack.push(n)         # and push the starting vertex index on it
      visited[n] = True     # Mark vertex n as visited
      yield (n, stack)      # Yield initial vertex and initial path
      while not stack.isEmpty(): # Loop until nothing left on stack
         visit = stack.peek() # Top of stack is vertex being visited
         adj = None
         for j in self.adjacentUnvisitedVertices( # Loop over adjacent
            visit, visited): # vertices marking them as we visit them
            adj = j         # Next vertex is first adjacent unvisited
            break           # one, and the rest will be visited later
         if adj is not None: # If there's an adjacent unvisited vertex
            stack.push(adj) # Push it on stack and
            yield (adj, stack) # yield it with the path leading to it
         else:              # Otherwise we're visiting a dead end so
            stack.pop()     # pop the vertex off the stack

   def breadthFirst(        # Traverse the vertices in breadth-first
         self, n):          # order starting at vertex n
      self.validIndex(n)    # Check that vertex n is valid
      visited = [False] * self.nVertices() # Nothing visited initially
      queue = Queue()       # Start with an empty queue and
      queue.insert(n)       # insert the starting vertex index on it
      visited[n] = True     # and mark starting vertex as visited
      while not queue.isEmpty(): # Loop until nothing left on queue
         visit = queue.remove() # Visit vertex at front of queue
         yield visit        # Yield vertex to visit it
         for j in self.adjacentUnvisitedVertices( # Loop over adjacent
               visit, visited): # unvisited vertices
            queue.insert(j) # and insert them in the queue
            
   def minimumSpanningTree( # Compute a minimum spanning tree
         self, n):          # starting at vertex n
      self.validIndex(n)    # Check that vertex n is valid
      tree = Graph()        # Initial MST is an empty graph
      vMap = [None] * self.nVertices() # Array to map vertex indices
      for vertex, path in self.depthFirst(n):
         vMap[vertex] = tree.nVertices() # DF visited vertex will be
         tree.addVertex(    # last vertex in MST as we add it
            self.getVertex(vertex))
         if len(path) > 1:  # If the path has more than one vertex,
            tree.addEdge(   # add last edge in path to MST, mapping
               vMap[path[-2]], vMap[path[-1]]) # vertex indices
      return tree

   def print(self,          # Print all the graph's vertices and edges
             prefix=''):    # Prefix each line with the given string
      print('{}{}'.format(prefix, self)) # Print summary form of graph
      for vertex in self.vertices(): # Loop over all vertex indices
         print('{}{}:'.format(prefix, vertex), # Print vertex index
               self.getVertex(vertex)) # and string form of vertex
         for k in range(vertex + 1, self.nVertices()): # Loop over
            if self.hasEdge(vertex, k): # higher vertex indices, if
               print(prefix, # there's an edge to it, print edge
                     self._vertices[vertex].name,
                     '<->',
                     self._vertices[k].name)
      
class Stack(list):          # Use list to define Stack class
   def push(self, item): self.append(item) # push == append
   def peek(self): return self[-1] # Last element is top of stack
   def isEmpty(self): return len(self) == 0

class Queue(list):          # Use list to define Queue class
   def insert(self, j): self.append(j) # insert == append
   def peek(self): return self[0] # First element is front of queue
   def remove(self): return self.pop(0) # Remove first element
   def isEmpty(self): return len(self) == 0

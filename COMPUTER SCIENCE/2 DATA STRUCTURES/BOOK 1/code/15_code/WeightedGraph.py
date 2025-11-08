# Implement a weighted graph using classes for vertices and edges

from Heap import Heap
import math

class Vertex(object):       # A vertex in a graph
   def __init__(self, name): # Constructor: stores a vertex name
      self.name = name      # Store the name

   def __str__(self):       # Summarize vertex in a string
      return '<Vertex {}>'.format(self.name)

class WeightedGraph(object): # A graph containing vertices and edges
   def __init__(self):      # with weights.
      self._vertices = []   # A list/array of vertices
      self._adjMat = {}     # Hash table maps vertex pairs to weight

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

   def addEdge(             # Add edge of weight w between two
         self, A, B, w):    # vertices A & B
      self.validIndex(A)    # Check that vertex A is valid
      self.validIndex(B)    # Check that vertex B is valid
      if A == B:            # If vertices are the same
         raise ValueError   # raise exception
      self._adjMat[A, B] = w # Add edge in one direction and
      self._adjMat[B, A] = w # the reverse direction

   def hasEdge(self, A, B): # Check for edge between vertices A & B
      return ((A, B) in self._adjMat and # If vertex tuple in adjMat
              self._adjMat[A, B] < math.inf) # and has finite weight

   def edgeWeight(self, A, B): # Get edge weight between vertices 
      self.validIndex(A)    # Check that vertex A is valid
      self.validIndex(B)    # Check that vertex B is valid
      return (              # If vertex tuple in adjMat, return
         self._adjMat[A, B] if (A, B) in self._adjMat
         else math.inf)     # the weight stored there otherwise +∞

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
            
   def minimumSpanningTree( # Compute a spanning tree minimizing edge
         self, n):          # weight starting at vertex n
      self.validIndex(n)    # Check that vertex n is valid
      tree = WeightedGraph() # Initial MST is an empty weighted graph
      nVerts = self.nVertices() # Number of vertices
      vMap = [None] * nVerts # Array to map vertex indices into MST
      edges = Heap(         # Use heap for explored edges
         key=weight,        # Store (A, B) vertex pair & weight in
         )                  # each heap item, order by negative weight
      vMap[n] = 0           # Map start vertex into MST
      tree.addVertex(self.getVertex(n)) # Copy vertex n into MST
      while tree.nVertices() < nVerts: # Loop until all verts mapped
         for vertex in self.adjacentVertices(n): # For all adjacent
            if vMap[vertex] is None: # vertices that are not mapped,
               edges.insert( # put weighted edges in heap
                  ((n, vertex), self.edgeWeight(n, vertex)))
         edge, w = (        # Get first edge and weight, if one exists
            (None, 0) if edges.isEmpty() else edges.remove())
         while (not edges.isEmpty() and  # While there are more edges
                vMap[edge[1]] is not None): # and current edge in MST,
            edge, w = edges.remove()        # go on to next edge
         if (edge is None or # If we didn't find an edge or it goes
             vMap[edge[1]] is not None): # to a mapped vertex
            break           # there are no more edges to be added
         n = edge[1]        # Otherwise get new vertex and
         vMap[n] = tree.nVertices() # map it into MST
         tree.addVertex(self.getVertex(n)) # copy it into MST
         tree.addEdge(      # Add weighted edge to MST mapping
            vMap[edge[0]], vMap[edge[1]], w) # vertex indices
      return tree           # Return the minimum spanning tree

   def shortestPath(        # Find shortest path between two vertices,
         self, start, end): # if it exists, as list of vertex indices
      visited = {}          # Hash table of visited vertices
      costs = {             # Hash of path costs to vertices including
         start: (0, start)} # their predecessor vertex
      while end not in visited: # Loop until we visit the end vertex
         nextVert, cost = None, math.inf # Look for next vertex 
         for vertex in costs: # among unvisited vertices whose cost
            if (vertex not in visited and # to reach is the lowest
                costs[vertex][0] <= cost):
               nextVert, cost = vertex, costs[vertex][0]
         # print('\nIteration', len(visited), 'Costs table:')
         # for k in costs:
         #    print('  ', k, self.getVertex(k).name, ': ', costs[k])
         # print('Visited:', visited, 'and next vertex is', nextVert)
         if nextVert is None: # If no unvisited vertex could be found
            break           # we cannot get to the end, so exit loop
         visited[nextVert] = 1 # Visit vertex at end of lowest cost
         for adj in self.adjacentVertices(nextVert): # path and
            if adj not in visited: # adjacent, unvisited vertices
               pathCost = (    # Extended path costs weight of adj.
                  self.edgeWeight(nextVert, adj) + # edge plus cost of
                  costs[nextVert][0])  # path so far 
               if (adj not in costs or # If reached adj for first time
                   costs[adj][0] > pathCost): # or old path costlier,
                  costs[adj] = ( # update cost to reach vertex
                     pathCost, nextVert) # via extended path
               
      path = []             # Build output path from end
      while end in visited: # Path only contains visited vertices
         path.append(end)   # Append end vertex
         if end == start:   # If we reached the start,
            break           # we're done.  Otherwise go to 
         end = costs[end][1] # predecessor via lowest cost path
      return list(reversed(path)) # Return path from start to end
      
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
                     self._vertices[k].name,
                     self.edgeWeight(vertex, k))

def weight(edge): return - edge[1] # Get neg. weight from edge tuple

class Stack(list):          # Use list to define Stack class
   def push(self, item): self.append(item) # push == append
   def peek(self): return self[-1] # Last element is top of stack
   def isEmpty(self): return len(self) == 0

class Queue(list):          # Use list to define Queue class
   def insert(self, j): self.append(j) # insert == append
   def peek(self): return self[0] # First element is front of queue
   def remove(self): return self.pop(0) # Remove first element
   def isEmpty(self): return len(self) == 0

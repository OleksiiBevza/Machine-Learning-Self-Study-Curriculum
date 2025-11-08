# Implement methods to sort directed graph vertices topologically

import project_14_1_solution

Vertex = project_14_1_solution.Vertex

class Graph(                # A graph with [non-]directed edges
      project_14_1_solution.Graph):
   
   def predecessorVertices( # Generate a sequence of vertex indices
         self, n):          # that are adjacent predecessors to n
      self.validIndex(n)    # Check that vertex index n is valid
      for j in self.vertices(): # Loop over all other vertices
         if j != n and self.hasEdge(j, n): # If other vertex connects
            yield j         # via edge, yield other vertex index

   def onlyVisitedPredecessors( # Test whether vertex n's predecessors
         self, n, visited): # have all been visited, if any
      return all(visited[p] # All predecessors must have been set in
                 for p in self.predecessorVertices(n)) # visited array

   def findUnvisitedWithoutPredecessor( # Find a vertex without
         self, visited):    # unvisited predecessor vertices, if any
      for vertex in self.vertices(): # Loop over all vertices
         if (not visited[vertex] and # If vertex is unvisited and has
             self.onlyVisitedPredecessors( # only visited
                vertex, visited)): # predecessors,
            return vertex   # then return it
      return None           # Otherwise there's a cycle or no vertices

   def sortVerticesTopologically( # Return a sequence of all vertex
         self):             # indices sorted topologically
      result = []           # Result list of vertices
      nVertices = self.nVertices() # Number of vertices
      visited = [None] * nVertices # Array to mark visited vertices
      while len(result) < nVertices: # Loop until all vertices handled
         vertex = self.findUnvisitedWithoutPredecessor( # Find an
               visited)     # unvisited vertex without predecessors
         if vertex is None: # If no such vertex exists, then raise an
            raise Exception('Cycle in graph, cannot sort') # exception
         result.append(vertex) # Append unvisited vertex and
         visited[vertex] = True # mark it as visited
      return result

   def degree(self, n):     # Get degree of vertex as (in, out) pair
      self.validIndex(n)    # Validate vertex index
      inb, outb = 0, 0      # Count inbound and outbound edges
      for j in self.vertices(): # Loop over all vertices
         if j != n:         # other than target vertex
            if self.hasEdge(j, n): # If other vertex precedes
               inb += 1            # increase inbound degree
            if self.hasEdge(n, j): # If other vertex succeeds n
               outb += 1           # increase outbound degree
      return (inb, outb)    # Return inbound and outbound degree
   
   def sortVertsTopologically( # Return sequence of all vertex indices
         self):             # sorted topologically more efficiently
      vertsByDegree = [     # Make an empty hash table for every
         {} for j in range( # possible degree, max = nVerts - 1 or
            min(self.nVertices(), self.nEdges() + 1))] #  nEdges
      inDegree = [0] * self.nVertices() # Indegree for each vertex
      for vertex in self.vertices(): # Loop over all vertices, record
         inDegree[vertex] = self.degree(vertex)[0] # inbound degree
         vertsByDegree[     # In hash table for this inbound degree
            inDegree[vertex]][vertex] = 1 # insert vertex
      result = []           # Result list is initially empty
      while len(            # While there are vertices with inbound
            vertsByDegree[0]) > 0: # degree of 0
         vertex, _ = vertsByDegree[0].popitem() # take vertex out of
         result.append(vertex) # hash table & add it to end of result
         for s in self.adjacentVertices( # Loop over vertex's
               vertex):     # successors; move them to lower degree
            vertsByDegree[ # In hash table holding successor vertex
               inDegree[s]].pop(s) # delete the successor
            inDegree[s] -= 1 # Decrease inbound degree of successor
            vertsByDegree[ # In hash table for lowered inbound degree
               inDegree[s]][s] = 1 # insert modified successor
      if len(result) == self.nVertices(): # All vertices in result?
         return result      # Yes, then return it, otherwise cycle
      raise Exception('Cycle in graph, cannot sort') 

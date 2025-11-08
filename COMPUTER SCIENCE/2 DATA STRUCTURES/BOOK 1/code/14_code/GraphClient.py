from Graph import *

import sys, random

# Default vertex names
verts = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

seed = 3.14159

if len(sys.argv) > 1:         # Use command line args if present
   verts = sys.argv[1:]
   seed = hash(''.join(verts))

random.seed(seed)             # Use consistent random seed
maxEdges = len(verts) ** 2 // 4  # Upper limit on number of edges

graph = Graph()
print('Initial graph:', graph)

nVerts = len(verts)
for vert in verts:
   graph.addVertex(Vertex(vert))

print('After adding', nVerts, 'vertices, graph contains')
graph.print()

for i in range(maxEdges):
   j = random.randrange(nVerts - 1)
   k = random.randrange(j + 1, nVerts)
   if graph.hasEdge(j, k):
      print('Skipping duplicate edge from', j, 'to', k)
   else:
      print('Adding edge from', j, 'to', k)
      graph.addEdge(j, k)

print('After adding edges, graph', graph, 'contains')
graph.print()

print('Checking some random potential edges')
for i in range(10):
   j = random.randrange(nVerts - 1)
   k = random.randrange(j + 1, nVerts)
   print('Does graph have edge from',
         j, graph.getVertex(j).name, 'to', 
         k, graph.getVertex(k).name, '?',
         'yes' if graph.hasEdge(j, k) else 'no')

for start in (0, nVerts - 1):
   print('Depth-first traversal of graph starting at', start, ':')
   for visit, path in graph.depthFirst(start):
      print('Visiting', graph.getVertex(visit).name, 'via', path,
            ''.join(graph.getVertex(j).name for j in path))
   print('End depth-first traversal')
   print('Breadth-first traversal of graph starting at', start, ':')
   for visit in graph.breadthFirst(start):
      print('Visiting', graph.getVertex(visit).name)
   print('End breadth-first traversal')
   print('Minimuum-spanning tree graph starting at', start, ':')
   graph.minimumSpanningTree(start).print()
   
print('Checking that bad indices cause exceptions')
for j, k in ((0, 0), (-1, 0), (0, graph.nVertices())):
   try:
      print('Trying to create an edge from', j, 'to', k)
      graph.addEdge(j, k)
   except IndexError as e:
      print('IndexError was raised')
   except ValueError as e:
      print('ValueError was raised')
print('All index tests passed')

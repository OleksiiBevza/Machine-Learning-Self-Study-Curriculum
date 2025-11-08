from WeightedGraph import *

import sys, random

# Default vertex names
verts = ['Blum', 'Cerf', 'Dahl', 'Gray', 'Kay', 'Naur']
MSTedges = [
   (0, 1, 31), (0, 2, 24), (1, 2, 35), (1, 3, 49), (1, 4, 38), (1, 5, 87),
   (2, 3, 41), (2, 4, 52), (3, 4, 25), (3, 5, 46), (4, 5, 43)
]
SPedges = [
   (0, 1, 22), (0, 2, 16), (1, 2, 29), (1, 3, 34), (1, 4, 26), (1, 5, 65),
   (2, 3, 28), (2, 4, 24), (3, 4, 25), (3, 5, 30), (4, 5, 36)
]

seed = 3.14159

if len(sys.argv) > 1:         # Use command line args if present
   verts = sys.argv[1:]
   seed = hash(''.join(verts))
   
random.seed(seed)             # Use consistent random seed
nVerts = len(verts)

if len(sys.argv) > 1:         # Make random edges for command line verts
   maxEdges = nVerts ** 2 // 4  # Upper limit on number of edges
   MSTedges, SPedges = [], []
   for edges in [MSTedges, SPedges]:
      print('Making edges for', 
            'minimum spanning tree' if edegs is MSTedges else 'shortest path')
      for i in range(maxEdges):
         j = random.randrange(nVerts - 1)
         k = random.randrange(j + 1, nVerts)
         weight = random.randrange(1, 100)
         if (j, k) in [(a, b) for a, b, _ in edges]:
            print('Skipping duplicate edge from', j, 'to', k)
         else:
            print('Adding edge from', j, 'to', k, 'with weight', weight)
            edges.append((j, k, weight))

graph = WeightedGraph()
print('Initial weighted graph:', graph)

nVerts = len(verts)
for vert in verts:
   graph.addVertex(Vertex(vert))

print('After adding', nVerts, 'vertices, weighted graph contains')
graph.print()

for j, k, weight in MSTedges:
   graph.addEdge(j, k, weight)
print('After adding minimum spanning tree edges, weighted graph contains')
graph.print()

print('Checking some random potential edges')
for i in range(10):
   j = random.randrange(nVerts - 1)
   k = random.randrange(j + 1, nVerts)
   print('Does weighted graph have edge from',
         j, graph.getVertex(j).name, 'to', 
         k, graph.getVertex(k).name, '?',
         'yes' if graph.hasEdge(j, k) else 'no',
         'weight:', graph.edgeWeight(j, k))

for start in (0, nVerts - 1):
   print('Depth-first traversal of weighted graph starting at', start, ':')
   for visit, path in graph.depthFirst(start):
      print('Visiting', graph.getVertex(visit).name, 'via', path,
            '-'.join(graph.getVertex(j).name for j in path))
   print('End depth-first traversal')
   print('Breadth-first traversal of weighted graph starting at', start, ':')
   for visit in graph.breadthFirst(start):
      print('Visiting', graph.getVertex(visit).name)
   print('End breadth-first traversal')
   print('Minimuum-spanning tree of weighted graph starting at', start, ':')
   graph.minimumSpanningTree(start).print()
   
print('\nChecking that bad indices cause exceptions')
for j, k in ((0, 0), (-1, 0), (0, graph.nVertices())):
   try:
      print('Trying to create an edge from', j, 'to', k)
      graph.addEdge(j, k, 0)
   except IndexError as e:
      print('IndexError was raised')
   except ValueError as e:
      print('ValueError was raised')
print('All index tests passed.\n')

graph = WeightedGraph()
for vert in [None, 'A']:
   if vert:
      graph.addVertex(Vertex(vert))
   print('Minimuum-spanning tree of weighted graph', graph,
         'starting at 0 is')
   try:
      graph.minimumSpanningTree(0).print()
   except Exception as e:
      print('minimumSpnningTree() raised exception:', e)
print('All tests of minimum spanning tree on trivial graphs passed.\n')

graph = WeightedGraph()
nVerts = len(verts)
for vert in verts:
   graph.addVertex(Vertex(vert))

for j, k, weight in SPedges:
   graph.addEdge(j, k, weight)
print('After adding shortest path edges, weighted graph contains')
graph.print()

for end in (nVerts - 1, nVerts - 2):
   start = 0
   shortest = graph.shortestPath(start, end)
   cost = 0 if len(shortest) < 2 else sum(
      graph.edgeWeight(shortest[i], shortest[i+1]) 
      for i in range(len(shortest) - 1))
   print('Shortest path from', start, graph.getVertex(start).name,
         'to', end,  graph.getVertex(end).name, 'with cost', cost, 'is:',
         [(v, graph.getVertex(v).name) for v in shortest])

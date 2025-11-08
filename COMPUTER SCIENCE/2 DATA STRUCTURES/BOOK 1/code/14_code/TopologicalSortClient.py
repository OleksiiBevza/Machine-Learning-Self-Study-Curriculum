from TopologicalSort import *
import sys, random

# Default vertex names
verts = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

seed = 3.14159

if len(sys.argv) > 1:         # Use command line args if present
   verts = sys.argv[1:]
   seed = hash(''.join(verts))

random.seed(seed)             # Use consistent random seed
maxEdges = len(verts) ** 2 // 8  # Upper limit on number of edges

graph = Graph(directed=True)  # Make a directed graph
print('Initial graph:', graph)

nVerts = len(verts)           # Place vertices in graph
for vert in verts:
   graph.addVertex(Vertex(vert))

if nVerts > 1:                # For non-trivial graph sizes
   for i in range(maxEdges):  # make a set of random directed edges
      j = random.randrange(nVerts)
      k = random.randrange(nVerts)
      while k == j:              # Don't allow edges to same vert
         k = random.randrange(nVerts)
      if graph.hasEdge(j, k):
         print('Skipping duplicate edge from', j, 'to', k)
      else:
         print('Adding edge from', j, 'to', k)
         graph.addEdge(j, k)

print('After adding vertices and edges, graph', graph, 'contains')
graph.print()

topo, prev_topo = [], []       # Hold current and previous sort results
methods = (Graph.sortVerticesTopologically, # Try basic and
           Graph.sortVertsTopologically) # improved sort methods
while not topo:                # Try sorting until a result is found
   for method in methods:
      prev_topo = topo
      try:
         print('Attempt to sort vertices topologically using', method)
         topo = method(graph)
      except Exception as e:   # Exception occurs if graph has cycle
         print('Raised exception\n', e)
         if graph.nEdges() == 0:
            break
         elif method == methods[-1]: # For last method, try removing a
            remove = random.randrange(graph.nEdges()) # random edge
            for i, edge in enumerate(graph._adjMat): # from the graph
               if i == remove:
                  break
            print('Randomly chose edge', graph.getVertex(edge[0]).name, '->',
                  graph.getVertex(edge[1]).name, 'to delete')
            del graph._adjMat[edge]
            
print('Final graph', graph, 'contains')
graph.print()
print('Sorting the vertices topologically returns:',
      ''.join(graph.getVertex(j).name for j in topo))
if prev_topo != topo:
   print('Previous topological sort returned:',
         ''.join(graph.getVertex(j).name for j in prev_topo))

from Graph import *
from pprint import *

vertices = []                  # A list of vertices
vertices.append(Vertex('A'))
vertices.append(Vertex('B'))
vertices.append(Vertex('C'))
vertices.append(Vertex('D'))

# An adjacency matrix big enough for all the vertices
# built using list comprehensions
adjMat = [ [False for v in range(len(vertices))] 
           for _ in range(len(vertices)) ]
adjMat[1][3] = True
adjMat[3][1] = True

pprint(adjMat)

# An attempt to make the adjacency matrix by copying N times
badMat = [ [False] * len(vertices) ] * len(vertices)
badMat[1][3] = True

# The inner array is copied four times and shared for all rows
pprint(badMat)

# Build an adjacency list structure big enough for all the vertices
adjList = [ [] for v in range(len(vertices)) ]
adjList[1].append(3)
adjList[3].append(1)

pprint(adjList)

# An attempt to make the adjacency list by copying N times
badList = [[]] * len(vertices)
badList[1].append(3)

pprint(badList)

# Example DF and BF traversals
graph = Graph()
graph.addVertex(Vertex('A'))
graph.addVertex(Vertex('B'))
graph.addVertex(Vertex('C'))
graph.addVertex(Vertex('D'))
graph.addVertex(Vertex('E'))
graph.addVertex(Vertex('F'))
graph.addVertex(Vertex('G'))
graph.addVertex(Vertex('H'))
graph.addVertex(Vertex('I'))
graph.addEdge(0, 1)
graph.addEdge(0, 2)
graph.addEdge(0, 3)
graph.addEdge(0, 4)
graph.addEdge(1, 5)
graph.addEdge(5, 7)
graph.addEdge(3, 6)
graph.addEdge(6, 8)
print('Depth-first traversal')
for vert, path in graph.depthFirst(0):
   print(graph.getVertex(vert).name,
         end='')
print()

graph.addEdge(2, 7)
print('Breadth-first traversal')
for vert in graph.breadthFirst(0):
   print(graph.getVertex(vert).name,
         end='')
print()
print('Depth-first traversal of', graph)
for vert, path in graph.depthFirst(0):
   print(graph.getVertex(vert).name,
         end='')
print()

graph2 = Graph()
graph2.addVertex(Vertex('A'))
graph2.addVertex(Vertex('B'))
graph2.addVertex(Vertex('C'))
graph2.addVertex(Vertex('D'))
graph2.addVertex(Vertex('E'))
graph2.addVertex(Vertex('F'))
graph2.addEdge(0, 1)
graph2.addEdge(0, 3)
graph2.addEdge(1, 3)
graph2.addEdge(1, 4)
graph2.addEdge(2, 5)
graph2.addEdge(3, 4)
print('Initial graph')
graph2.print()
print()
start = 0
tree = graph2.minimumSpanningTree(start)
print('Minimum spanning tree starting at', start)
tree.print()




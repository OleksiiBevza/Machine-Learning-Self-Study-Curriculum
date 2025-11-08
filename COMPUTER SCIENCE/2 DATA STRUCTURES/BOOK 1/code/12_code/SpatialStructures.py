from math import *

RADIUS_OF_EARTH = 6371    # radius in kilometers

# return the Euclidean distance between points (x1,y1) and (x2,y2)
def euclideanDistance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return (dx*dx + dy*dy) ** 0.5

# return the haversine distance between (lon1, lat1) and (lon2, lat2)
def haversineDistance(lon1, lat1, lon2, lat2):
    lat1 = radians(lat1)    # trig functions need radians
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    dLon = lon2 - lon1      # difference of longitudes
    dLat = lat2 - lat1      # difference of latitudes
    
    # Haversine formula:
    a = sin(dLat/2)**2 
    if dLon != 0:  # save some trig for dLon == 0
        a += cos(lat1) * cos(lat2) * sin(dLon/2)**2
    
    # Numerical issues at antipodal points requires min, max:
    return 2 * RADIUS_OF_EARTH * asin(min(1, max(a, 0)**0.5))


# Notation: 
# If cartesian coordinates are stored in the object, 
# then a == x coordinate,  b == y coordinate
#
# If geographic coordinates are stored in the object,
# then a == longitude,  b == latitude
#

# Object to define a bounding box
class Bounds(object): 
    def __init__(self, left = -inf, right  = inf, 
                       top  =  inf, bottom = -inf):
        Bounds.adjust(self, left, right, top, bottom)
        
    # mutator to initialize/change bounds in existing object
    def adjust(self, left, right, top, bottom):
        self.__l = left
        self.__r = right
        self.__t = top
        self.__b = bottom        
        
    # return a new Bounds, where some of the 
    # current boundaries have been adjusted
    def adjusted(self, left = None, right = None, 
                       top = None,  bottom = None):
  
        if left   == None: left   = self.__l
        if right  == None: right  = self.__r
        if top    == None: top    = self.__t
        if bottom == None: bottom = self.__b
        
        return Bounds(left, right, top, bottom)
    
    # return True if bounds of the rectangles intersect.
    # Two rectangles don't intersect if one is totally to 
    # the left of or above the other. So we negate to 
    # determine if they do intersect.    
    def intersects(self, other):
        return not (
            # check if self's box is to left or right of other
            self.__r < other.__l  or  self.__l > other.__r or 
            
            # check if self's box is above or below other
            self.__b > other.__t  or  self.__t < other.__b)  
    
    # return True if the bounds of self fall within other
    def within(self, other):
        return (self.__r < other.__r and 
                self.__l > other.__l and
                self.__t < other.__t and
                self.__b > other.__b)

# A bounding box that surrounds a search circle.
# Properly handles distorted circles resulting 
# from geographic coordinates.
class CircleBounds(Bounds):
    def __deltas(self, a, b, r, func):
        # When r is infinity, bounds are always infinite
        # For cartesian coordinates, the edges of the bounding 
        # box are r away from the center of the search circle.
        if r == inf or func == euclideanDistance:
            deltaA = deltaB = r
            
        else: # geographic coordinates
            # The width of the bounding box is determined by
            # the width of the distorted circle at its widest point.
            alpha = r / RADIUS_OF_EARTH
            gamma = radians(90 - abs(b)) # b is latitude
            
            # if the circle itself crosses the pole then 
            # alpha >= gamma, so we set deltaA as inf,
            # effectively treating the width as if it were inf 
            if alpha >= gamma:
                deltaA = inf
            else:
                # the circle doesn't cross a pole, so get
                # longitude angle from center of circle at 
                # the circle's widest width calculated using
                # a spherical right triangle identity. 
                deltaA = degrees(asin(sin(alpha) / sin(gamma)))
            
            # latitude angle directly above/below the 
            # center of the circle. This works since above
            # or below is directly on a meridian. 
            deltaB = degrees(alpha)
                
        return deltaA, deltaB

    # create the bounding box that surrounds the search
    # circle at a,b,r using the specified distance function
    def __init__(self, a, b, r, func):
        # remember the circle's parameters for later
        self.__a, self.__b, self.__r = a, b, r       
        self.__func = func

        # get the width/height of the bounding box
        deltaA, deltaB = self.__deltas(a, b, r, func)
                
        # initialize the superclass's rectangular bounds
        super().__init__(a - deltaA,  # left
                         a + deltaA,  # right
                         b + deltaB,  # top
                         b - deltaB)  # bottom
    
    # if the circle's radius changed, mutate its bounds    
    def adjust(self, r):
        if r != self.__r:
            self.__r = r
            
            # new dimensions of bounding box
            deltaA, deltaB = self.__deltas(
                self.__a, self.__b, r, self.__func)
            
            # update the box
            super().adjust(self.__a - deltaA,  # left
                           self.__a + deltaA,  # right
                           self.__b + deltaB,  # top
                           self.__b - deltaB)  # bottom    


class PointList(object):
    def __init__(self, kind): # must specify type of coordinate
        if kind == 'cartesian': 
            self.__distance = euclideanDistance
        elif kind == 'geographic':
            self.__distance = haversineDistance
        else: 
            raise Exception("Invalid kind of coordinate")
        
        self.__points = [ ]       # keep points in a list
    
    def insert(self, a, b, data):
        # Insert the data for the (a,b) coordinates.
        # Loop through the points looking for an exact match
        for i in range(len(self.__points)):
            p = self.__points[i]
            if p[0] == a and p[1] == b:         # Replace data
                self.__points[i] = (a, b, data) # for a duplicate
                return
            
        self.__points.append((a, b, data))  # not there, so append
    
    # delete the point at a,b
    # Return the deleted point's data if found, or None
    def delete(self, a, b):
        # Loop through the points looking for an exact match
        for i in range(len(self.__points)): 
            p = self.__points[i]
            if p[0] == a and p[1] == b: # found a match
                del self.__points[i]    # delete the point
                return p[2]             # return its data
            
        return None                     # point wasn't there
    
    def traverse(self):                 
        for p in self.__points:         # yield each of the tuples
            yield p
        
    def findExact(self, a, b):          # Return data for exact point
        for p in self.__points:         # Loop through all points
            if p[0] == a and p[1] == b: # found exact match
                return p[2]             # so return its data
        return None                     # Couldn't find a match!

          
    def findNearest(self, a, b):     # find closest point to (a,b)
        if len(self.__points) == 0:  # No points yet?
            return None

        distance = inf               # Assume no nearest point
        for p in self.__points:      # For each point
            newDist = self.__distance(a, b, p[0], p[1])
            if newDist == 0:         # Nothing could be closer!
                return p[0], p[1], p[2], 0 
            if newDist < distance:   # If it is closest so far,
                distance = newDist   # remember the distance,
                answer   = p         # and the point
                
        return answer[0], answer[1], answer[2], distance  
    
    
class Grid(object):
    # Generator to yield grid offsets in concentric 
    # layers, starting at the center 0,0
    @staticmethod
    def offsets():
        yield 0,0
        
        layer = 1
        while True:
            for num in range(-layer+1, layer):
                yield    num,  layer # yield offsets for the
                yield    num, -layer # cells along each side
                yield -layer, num
                yield  layer, num
                
            yield -layer,  layer # yield offsets for the 
            yield  layer,  layer # corners of the layer
            yield  layer, -layer
            yield -layer, -layer            
                
            layer += 1  # move on to the next layer

    def __init__(self, kind, cellSize): 
        if cellSize <= 0:
            raise Exception("Cell size must be positive")        
        self.__cellSize = cellSize

        if kind == 'cartesian': 
            self.__distance = euclideanDistance
            
        elif kind == 'geographic':
            self.__distance = haversineDistance

        else: 
            raise Exception("Invalid kind of coordinate")
   
        # dict key: (row, col) tuple
        # dict data: list of (a, b, data) tuples
        self.__cells = dict()
        
    # inputs: x,y  or  long,lat
    # returns row,col tuple specifying grid cell
    def __getCell(self, a, b):
        col = floor(a / self.__cellSize)
        row = floor(b / self.__cellSize)
        return row, col

    # Insert either an x,y,data or longitude,latitude,data point
    def insert(self, a, b, data): 
        cell = self.__getCell(a, b)  # which cell contains point?
        if cell in self.__cells:             # existing cell?
            c = self.__cells[cell]
            for i in range(len(c)):
                p = c[i]                     # For each point in cell 
                if p[0] == a and p[1] == b:  # replace data for  
                    c[i] = (a, b, data)      # a duplicate
                    return
                
            c.append((a,b,data)) # append new point to cell 
        else:                       
            self.__cells[cell] = [(a,b,data)] # create new cell
    
    def traverse(self): 
        for cell in self.__cells:        # for each cell in the grid
            for p in self.__cells[cell]: # for each point in the cell
                yield p                  # yield the tuple

    # returns the Bounds of a given row,col of a cell
    def __getCellBounds(self, cell):
        left = cell[1] * self.__cellSize
        right = left + self.__cellSize
        
        bottom = cell[0] * self.__cellSize
        top = bottom + self.__cellSize
        
        return Bounds(left, right, top, bottom)
    
    # return Bounds of the layer with cell at its center
    def __getLayerBounds(self, cell, layer):
        left = (cell[1]-layer) * self.__cellSize
        right = left + (self.__cellSize * (layer * 2 + 1))
        
        bottom = (cell[0]-layer) * self.__cellSize
        top = bottom + (self.__cellSize * (layer * 2 + 1))
        
        return Bounds(left, right, top, bottom)

    # Returns true if the query circle falls within the specified
    # layer surrounding the search coordinates.
    # a,b are the coordinates of the query circle center
    # cbounds is the current Bounds of the query circle
    def __withinLayer(self, cBounds, a, b, layer): 
        # get the bounds of the layer
        cell = self.__getCell(a, b)     # row,col of cell
        layerBounds = self.__getLayerBounds(cell, layer) 
        
        # check if the circle's bounds are within the layer
        return cBounds.within(layerBounds)
       

    # Find the data associated with exact match of coordinates 
    def findExact(self, a, b):         
        cell = self.__getCell(a, b) # which cell contains a,b
        points = self.__cells.get(cell, None) # get list of points
        if points: # there are points for the cell
            for p in points: # check each point and seek a match
                if p[0] == a and p[1] == b: 
                    return p[2] # return the data for exact match
        return None

    # find the closest point to (a,b)
    def findNearest(self, a, b):
        if len(self.__cells) == 0:  # A: Nothing in grid yet
            return None
        
        answer = None  # B: remember the closest point so far

        # The current search circle and its bounds so far
        distance = inf 
        cBounds = CircleBounds(a, b, distance, self.__distance)
        
        # C: get cell containing the query point a,b
        cell = self.__getCell(a, b) 
        
        curLayer = 0      # D: the layer we're up to
        
        # E: for each offset
        for off in Grid.offsets():
            #F: what layer is this new offset?
            layer = max(abs(off[0]), abs(off[1]))
            
            # G: if we're about to consider a new layer, 
            # but the search circle falls entirely within
            # the prior layer, then there's no need to continue.
            if layer != curLayer and answer and \
               self.__withinLayer(cBounds, a, b, curLayer):
                break 
            curLayer = layer  # remember what layer we're up to
            
            # H: get the points stored in the cell at that offset
            offsetCell = cell[0]+off[0], cell[1]+off[1]
            points = self.__cells.get(offsetCell, None)
                
            # I: if there are points in the cell, and 
            # the search circle intersects the cell... 
            if points and \
               cBounds.intersects(self.__getCellBounds(offsetCell)):
                                  
                for p in points: # J: for each point in the grid cell
                    
                    # compute distance to that point from query point
                    newDist = self.__distance(a, b, p[0], p[1])
                    
                    if newDist == 0: # exact match?
                        return p[0], p[1], p[2], 0
                    
                    if newDist < distance:  # new point closer? 
                        distance = newDist  # remember the distance
                        answer = p          # and the point, and
                        cBounds.adjust(distance) # adjust circle's bounds
        
        # K: returns a, b, data, distance to query point
        return answer[0], answer[1], answer[2], distance

class Node(object):
    # a,b corresponds to either x,y or long,lat
    def __init__(self, a, b, data):
        self.a = a  # coordinates of the point
        self.b = b
        self.data = data # data associated with point   
        
        # Four children of the Node
        self.NE = self.SE = self.SW = self.NW = None
        
    def __str__(self):
        return "({}, {}: {!r})".format(self.a, self.b, self.data)


class QuadTree(object):
        
    def __init__(self, kind): # must specify type of coordinate
        if kind == 'cartesian': 
            self.__distance = euclideanDistance
        elif kind == 'geographic':
            self.__distance = haversineDistance
        else: 
            raise Exception("Invalid kind of coordinate")
        
        self.__root = None 
        
    
    def insert(self, a, b, data): # Wrapper. Always succeeds.
        self.__root = self.__insert(self.__root, a, b, data)   
    
    # Recursive private method that does the inserting    
    def __insert(self, n, a, b, data):
        
        # return a new Node if we've reached None
        if not n: return Node(a, b, data)
        
        # if the point to be inserted is identical to the current node, 
        # overwrite the data, and don't recurse any further
        if n.a == a and n.b == b:
            n.data = data
            return n
      
        # recurse down into the appropriate quadrant
        if   a >= n.a and b >  n.b: n.NE = self.__insert(n.NE, a, b, data)
        elif a >  n.a and b <= n.b: n.SE = self.__insert(n.SE, a, b, data)
        elif a <= n.a and b <  n.b: n.SW = self.__insert(n.SW, a, b, data)
        else:                       n.NW = self.__insert(n.NW, a, b, data)   
           # a <  n.a and b >= n.b          
        
        return n  
    
    def traverse(self):
        s = [ ]  # initialize stack with root
        if self.__root: s.append(self.__root)

        while len(s) > 0: # stack's not empty?
            
            # process Node at top of stack
            n = s.pop()  
            yield n.a, n.b, n.data
            
            # push each child onto stack
            if n.NE: s.append(n.NE)
            if n.SE: s.append(n.SE)
            if n.SW: s.append(n.SW)
            if n.NW: s.append(n.NW)            
   
    # Wrapper method - returns the data object associated with a,b
    def findExact(self, a, b): return self.__find(self.__root, a, b)
   
    def __find(self, n, a, b):
        if not n: return None  # Couldn't find the exact point
      
        # Did we find the exact point? Return the data
        if n.a == a and n.b == b: return n.data

        # Recurse down into the appropriate quadrant.
        # If a,b is anywhere, it MUST be in that quadrant.
        if   a >= n.a and b >  n.b: return self.__find(n.NE, a, b)
        elif a >  n.a and b <= n.b: return self.__find(n.SE, a, b)
        elif a <= n.a and b <  n.b: return self.__find(n.SW, a, b)
        else:                       return self.__find(n.NW, a, b)   
           # a <  n.a and b >= n.b  

    # find a nearby (but not necessarily the nearest) point 
    # to a,b by recursing as deep as possible into the tree. 
    def __nearPoint(self, n, a, b):
        # Base cases:
        if not n: return None # reached None so return it
      
        if a == n.a and b == n.b: return n # found exact point
        
        # recurse down into the appropriate quadrant
        if   a >= n.a and b >  n.b: ans = self.__nearPoint(n.NE, a, b)
        elif a >  n.a and b <= n.b: ans = self.__nearPoint(n.SE, a, b)
        elif a <= n.a and b <  n.b: ans = self.__nearPoint(n.SW, a, b)
        else:                       ans = self.__nearPoint(n.NW, a, b)   
           # a <  n.a and b >= n.b          
      
        # if we found a lower Node near this point return it
        # otherwise return the current node
        return ans if ans else n

    # Returns the nearest Node and distance to query point a,b. 
    def __nearest(self, n, # current Node being visit
                  a, b,    # query point
                  dist,    # distance to candidate
                  cand,    # best candidate so far
                  bounds): # Bounds of current quadrant
        
        # Reached a None node, or already found
        # a perfect match? Return our answer.
        if not n or dist == 0: return cand, dist
      
        # Is the current quad tree point closer than 
        # the candidate? If so, update the candidate
        fn = self.__distance
        newDist  = fn(a, b, n.a, n.b)
        if newDist < dist:
            cand = n  
            dist = newDist
        
        # bounding box surrounding the search circle
        cBounds = CircleBounds(a, b, dist, fn)

        # For each child node - update bounds for that quadrant 
        # if the search circle's bounds intersects the child 
        # quadrant's new bounds, descend to that child node.
        newB = bounds.adjusted(left = n.a, top = n.b)
        if cBounds.intersects(newB): 
            cand, dist = self.__nearest(n.SE, a, b, dist, cand, newB)
            cBounds.adjust(dist) # adjust the circle's bounds if necessary
            
        # likewise for the other three quadrants
        newB = bounds.adjusted(left = n.a, bottom = n.b)
        if cBounds.intersects(newB): 
            cand, dist = self.__nearest(n.NE, a, b, dist, cand, newB) 
            cBounds.adjust(dist)
                
        newB = bounds.adjusted(right = n.a, top = n.b)  
        if cBounds.intersects(newB): 
            cand, dist = self.__nearest(n.SW, a, b, dist, cand, newB)
            cBounds.adjust(dist)
        
        newB = bounds.adjusted(right = n.a, bottom = n.b)
        if cBounds.intersects(newB): 
            cand, dist = self.__nearest(n.NW, a, b, dist, cand, newB) 
            # no need to update circle's bounds after last quadrant

        return cand, dist # best candidate seen so far


    # returns a,b,data,distance of point nearest to query a,b.  
    def findNearest(self, a, b):
        if not self.__root: return None # No points yet!
        
        # Descend the tree and find the leaf node nearby
        # to this query point. This quickly sets an upper 
        # bound on the nearest possible point 
        ans  = self.__nearPoint(self.__root, a, b)
        dist = self.__distance(a, b, ans.a, ans.b)

        # Now we will descend the tree once more, refining 
        # the candidate by progressively shrinking the radius.
        # The bounds of the root node are infinite
        bounds =  Bounds()
        ans, dist = self.__nearest(self.__root, a, b, dist, ans, bounds)

        return ans.a, ans.b, ans.data, dist
    
    # return (total leafs, total leaf depth)
    def treeStats(self, depth = 1, n = 'foo'):
        if n == 'foo': n = self.__root
        
        if n.SW == None and n.SE == None and n.NW == None and n.NE == None:
            return (1, depth)
        
        ans = [0, 0]
        for child in [n.NE, n.SE, n.SW, n.NW]:
            if child:
                tmp = self.treeStats(depth+1, child)
                ans[0] += tmp[0]
                ans[1] += tmp[1]
            
        return ans[0], ans[1]

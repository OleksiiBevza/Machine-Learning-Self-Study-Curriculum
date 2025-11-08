import random, sys
from math import *
from SpatialStructures import *

import time

def __experiment(bgq, bounds, numPoints, numQueries):
    start = time.time()
    for i in range(numPoints):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
        bgq.insert(x, y, (x, y))
        #if i%100 == 0:
            #if time.time() - start > 2:
                #break        

    start = time.time()
    for i in range(numQueries):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
        ans = bgq.findNearest(x, y)
        #if i%10 == 0:
            #if time.time() - start > 2:
                #break
        
    queryTime = time.time() - start
    
    return queryTime

def __doRound(bounds, points, queries, sep=',', header=False):
    if header:
        print(sep.join(
            # ('Points', 'PointList', 'Grid 0.5 deg', 'Grid 1.0 deg',  'Quadtree')
            ('Points', 'Grid 0.5 deg', 'Grid 1.0 deg',  'Quadtree')
        ))
    print(points, end = sep, flush=True)
    
    #bgq = PointList('geographic')
    #ans = __experiment(bgq, bounds, points, queries)
    #print(ans, end=sep, flush=True)
    
    bgq = Grid('geographic', 0.5)
    ans = __experiment(bgq, bounds, points, queries)
    print(ans, end=sep, flush=True)  
    
    bgq = Grid('geographic', 1)
    ans = __experiment(bgq, bounds, points, queries)
    print(ans, end=sep, flush=True)   
    
    bgq = QuadTree('geographic')
    ans = __experiment(bgq, bounds, points, queries)
    print(ans, flush=True)  
    
def __timingExperiments():
    bounds = [-125.6, 23.77, -60.8, 49.72]  # USA
    first = True
    for points in range(100000, 4000001, 200000):
        __doRound(bounds, points, 1000, header=first)
        first = False
        
def __compare_findExact_time_findNearest_geographic():

    # USA: -125.6,23.77,-60.8,49.72
    
    bounds = [-125.6, 23.77, -60.8, 49.72]  # USA
    b = PointList('geographic')
    g = Grid('geographic', 1)
    q = QuadTree('geographic')
    pts = []

    NUMPTS = 20000  # the number of points to insert 
    NUMQ = 1000
    
    for i in range(NUMPTS):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
        
        # The key is the x,y coord, the data is just a tuple of the key
        b.insert(x, y, (x, y))
        g.insert(x, y, (x, y))
        q.insert(x, y, (x, y))
        pts.append((x, y))
    
    ### make sure all the points can still be found
    badExact = 0
    for p in pts:
        bAns = b.findExact(p[0], p[1])
        gAns = g.findExact(p[0], p[1])
        qAns = q.findExact(p[0], p[1])
        
        if gAns != bAns: 
            badExact += 1
            print(gAns, bAns)
            
    print(badExact, "errors searching for exact match out of", NUMPTS, "points", flush=True)

    badNearest = 0
    for i in range(NUMQ):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
        
        # The key is the x,y coord, the data is just a tuple of the key
        #bAns = b.findNearest(x, y)
        gAns = g.findNearest(x, y)
        qAns = q.findNearest(x, y)
        
        if gAns != qAns: 
            badNearest += 1
            print(gAns, qAns)
                    
    print(badNearest, "errors searching for nearest match out of", NUMQ, "points", flush=True)
    
    start = time.time()
    for i in range(NUMQ):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
    end = time.time()
    emptyTime = end - start
    print("Empty time:", emptyTime, flush=True)
        
    #start = time.time()
    #for i in range(NUMQ):
        #x = random.uniform(bounds[0],bounds[2])
        #y = random.uniform(bounds[1], bounds[3])
        #bAns = b.findNearest(x, y)
    #end = time.time()
    #bruteTime = end - start
    #print("Brute: total time:", bruteTime-emptyTime, 
          #"Per query time:", (bruteTime-emptyTime) / NUMQ, flush=True)
    
    start = time.time()
    for i in range(NUMQ):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
        gAns = g.findNearest(x, y)
    end = time.time()
    gridTime = end - start
    print("Grid: total time:", gridTime-emptyTime, 
          "Per query time:", (gridTime-emptyTime) / NUMQ, flush=True)    
    
    start = time.time()
    for i in range(NUMQ):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
        qAns = q.findNearest(x, y)
    end = time.time()
    quadTime = end - start
    print("Quad: total time:", quadTime-emptyTime, 
          "Per query time:", (quadTime-emptyTime) / NUMQ, flush=True)  


def __time_insertion_findNearest_compare_completeness_geographic():
    
    bounds = [-125.6, 23.77, -60.8, 49.72]  # USA
    b = PointList('geographic')
    g = Grid('geographic', 1)
    q = QuadTree('geographic')
    
    checkBrute = False
    
    pts = []

    NUMPTS = 160000  # the number of points to insert 
    NUMQ = 4000
    
    print("Generating points...", flush=True)
    start = time.time()
    for i in range(NUMPTS):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
        pts.append((x, y))
    print("Generated", NUMPTS, "points in", time.time() - start, "seconds", flush=True)
   
    if checkBrute:
        print("Inserting in BruteForce...", flush=True)
        start = time.time()    
        for p in pts:
            # The key is the x,y coord, the data is just a tuple of the key
            b.insert(p[0], p[1], p)
        print("Brute inserted", NUMPTS, "points in", time.time() - start, "seconds", flush=True)    
        
    print("Inserting in grid...", flush=True)
    start = time.time()    
    for p in pts:
        # The key is the x,y coord, the data is just a tuple of the key
        g.insert(p[0], p[1], p)
    print("Grid inserted", NUMPTS, "points in", time.time() - start, "seconds", flush=True)

    print("Inserting in quad...", flush=True)
    start = time.time()
    for p in pts:
        # The key is the x,y coord, the data is just a tuple of the key
        q.insert(p[0], p[1], p)
    print("Quad inserted", NUMPTS, "points in", time.time() - start, "seconds", flush=True)

    ans = q.treeStats()
    print("Quadtree stats: total leaves:", ans[0], "total leaf depth:", ans[1], 
          "Average leaf depth", ans[1]/ans[0], flush=True)
    
    ### make sure all the points can still be found
    print("Starting exact finds...", flush=True)
    start = time.time()    
    badExact = 0
    for p in pts:
        if checkBrute:
            bAns = b.findExact(p[0], p[1])
        gAns = g.findExact(p[0], p[1])
        qAns = q.findExact(p[0], p[1])
        
        if gAns != qAns or (checkBrute and bAns != qAns): 
            badExact += 1
            print(gAns, qAns)
    
    print("Completed", NUMPTS, "exact finds in", time.time() - start, "seconds")
    print(badExact, "errors searching for exact match out of", NUMPTS, "points", flush=True)

    start = time.time()    
    badExact = 0
    for p in pts:
        gAns = g.findExact(p[0], p[1])
    delta = time.time() - start
    print("Grid - exact: total time:", delta,  
          "Per query time:", delta / NUMPTS, flush=True) 
    
    start = time.time()    
    badExact = 0
    for p in pts:
        qAns = q.findExact(p[0], p[1])
    delta = time.time() - start
    print("Quad - exact: total time:", delta,  
          "Per query time:", delta / NUMPTS, flush=True)       
    
    badNearest = 0
    for i in range(NUMQ):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
        
        # The key is the x,y coord, the data is just a tuple of the key
        if checkBrute:
            bAns = b.findNearest(x, y)
        gAns = g.findNearest(x, y)
        qAns = q.findNearest(x, y)
        
        if gAns != qAns or (checkBrute and bAns != qAns):
            badNearest += 1
            print(gAns, qAns)
                    
    print(badNearest, "errors searching for nearest match out of", NUMQ, "points", flush=True)
    
    start = time.time()
    for i in range(NUMQ):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
    end = time.time()
    emptyTime = end - start
    print("Empty time:", emptyTime, flush=True)
        
    #start = time.time()
    #for i in range(NUMQ):
        #x = random.uniform(bounds[0],bounds[2])
        #y = random.uniform(bounds[1], bounds[3])
        #bAns = b.findNearest(x, y)
    #end = time.time()
    #bruteTime = end - start
    #print("Brute: total time:", bruteTime-emptyTime, 
          #"Per query time:", (bruteTime-emptyTime) / NUMQ, flush=True)
    
    start = time.time()
    for i in range(NUMQ):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
        gAns = g.findNearest(x, y)
    end = time.time()
    gridTime = end - start
    print("Grid: total time:", gridTime-emptyTime, 
          "Per query time:", (gridTime-emptyTime) / NUMQ, flush=True)    
    
    start = time.time()
    for i in range(NUMQ):
        x = random.uniform(bounds[0],bounds[2])
        y = random.uniform(bounds[1], bounds[3])
        qAns = q.findNearest(x, y)
    end = time.time()
    quadTime = end - start
    print("Quad: total time:", quadTime-emptyTime, 
          "Per query time:", (quadTime-emptyTime) / NUMQ, flush=True)  

def myRange(a, b=None, c=None):
    inc = 1
    if not b:
        start = 0
        end = a
    else:
        start = a
        end = b
        if c: inc = c

    cur = start
    while (inc > 0 and cur < end) or \
          (inc < 0 and cur > end):
            yield cur
            cur += inc

# check if the bounding box due east of the top of the circle is ok
def isValid(long, lat, r):
    dLat = degrees(r / RADIUS_OF_EARTH)
    top = lat + dLat
    bot = lat - dLat
    
    dLong = degrees(r / (RADIUS_OF_EARTH * cos(radians(top))))
    right = long + dLong
    
    for curLat in myRange(top, bot, -0.01):
        dist = haversineDistance(long, lat, right, curLat)
        if dist < r:
            print("ERR:", long, lat, r, dist, "curLat", curLat, "TOP/BOT:", top, bot)
            return False
    return True

# test QuadTree and Grid traversal
def __test_traverse():
    q = QuadTree('cartesian')
    g = Grid('cartesian', 0.1)
    pts = []
    
    for i in range(100000):
        x = random.random()
        y = random.random()
        d = random.random()
        q.insert(x, y, d)
        g.insert(x, y, d)
        pts.append((x, y, d))
    
    print("finished inserting {} points into quadtree and grid".format(
        len(pts)), flush=True)

    insertedSet = set(pts)
    for pointSet in (q, g):
        ans = set(pointSet.traverse())
        print("finished traversing {}".format(pointSet), flush=True)
        
        if len(ans) != len(insertedSet):
            print("Didn't get all the points back from {}!".format(pointSet))
            print('Traversed {} distinct points, '
                  'but inserted {} distinct points'.format(
                      len(ans), len(insertedSet)))
            for missing in insertedSet - ans:
                print('{} was inserted but not traversed'.format(missing))
            for unexpected in ans - insertedSet:
                print('{} was traversed but not inserted'.format(unexpected))
   
def __main():
    __time_insertion_findNearest_compare_completeness_geographic()
    __compare_findExact_time_findNearest_geographic()
    __test_traverse()
        

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-timing':
        __timingExperiments()
    else:
        __main()

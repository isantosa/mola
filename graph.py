#http://www.iti.fh-flensburg.de/lang/algorithmen/graph/dijkstra.htm
#http://www.iti.fh-flensburg.de/lang/algorithmen/graph/shortest-paths.htm
#http://en.wikipedia.org/wiki/Dijkstra_algorithm
from Queue import PriorityQueue
from mola.grid import GridManager
from mola.core import *

# graph has getWeight
# weightedGraph ?
# how about cost
class Graph:
    ''' basic graph class. weighted graphs should implement different weightFunction'''

    def __init__(self,neighbours):
        self.neighbours=neighbours
        self.weightFunction=lambda a,b:1
    def getNeighbours(self,u):
        return self.neighbours[u]
    def size(self):
        return len(self.neighbours)
    def weight(self,index1,index2):
        return self.weightFunction(index1,index2)

    @classmethod
    def fromGrid2D(cls,nX,nY,nbs8=False,continous=False):
        gm=GridManager(nX,nY)
        neighbours=[0]*gm.length
        for i in range(gm.length):
            neighbours[i]=gm.getNbs2D(i,nbs8,continous)
        return cls(neighbours)

    @classmethod
    def fromGridHex(cls,nX,nY,continous=False):
        gm=GridManager(nX,nY)
        neighbours=[0]*gm.length
        for i in range(gm.length):
            neighbours[i]=gm.getNbs2DHex(i,continous)
        return cls(neighbours)

    def fromMeshFaces(mesh):
        pass

    def fromMeshEdges(mesh):
        pass

    def fromMeshVertices(mesh):
        pass

class GraphAnalyser:
    """
    works with graphs which provide 3 methods: size(), getNeighbours(), and weight()
    this class stores all distances in order to allow a fast calculation of path to predefined starting points
    usage: construct a Graphanalyser
    1. compute distance to a list of starting points
    2. getShortest Path from end point to those starting point
    """
    def __init__(self,graph):
        n=graph.size()
        self.graph=graph
        self.dist = [1000000]*n
        self.pred = [-1]*n

    def computeDistancesToNodes(self,startIndexes):
    	pq = PriorityQueue()
        for i in startIndexes:
            self.dist[i] = 0
            pq.put((0, i))
    	while not pq.empty(): #and not tree[end]:
            u= pq.get()[1]
            nbs = self.graph.getNeighbours(u)
            for v in nbs:
                d=self.dist[u]+self.graph.weight(u,v)
                if d < self.dist[v]:
                    self.dist[v] = d
                    self.pred[v] = u
                    pq.put((d, v))

    def getShortestPath(self,v):
        p=[]
    	while (v != -1):
            p.append(v)
    	    v = self.pred[v]
    	return p

    def computeTrafficAndCentrality(self,nodes):
        self.traffic = [0]*n
    	self.centrality = [0]*n
    	for i in range(len(nodes)-1):
            startI=nodes[i]
            self.dist = [100000]*n
            self.pred = [-1]*n
            computeDistancesToNodes([startI])
            for j in range(i,len(nodes)):
                endI = nodes[j]
                if endI != startI:
                    self.centrality[startI] += self.dist[endI]
                    self.centrality[endI] += self.dist[endI]
                    path = getShortestPath(endI)
                    for ii in path:
    					cI = path[ii]
    					self.traffic[cI]+=1

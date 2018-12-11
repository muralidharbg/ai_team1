from copy import copy, deepcopy

class Graph:

    def __init__( self ):
        
        # This is 'y' in Eq. 2
        self.orderedVertexList = []
        
        # This is M in Eq. 2
        self.numberOfVertices = 0;
        
    # end constructor
    
    def getLossFunction( self, secondGraph, norm = 1.5 ):
        
        M = self.getNumberOfVertices()
        D = self.getSimilarityScore( secondGraph, norm )
        delta = ( 1 / M ) * ( M - D )
        
        #print( delta )
        return delta
        
    # end function getLossFunction
    
    # Compute the similarity score between this graph
    # and the input graph based Eq. 2
    def getSimilarityScore( self, secondGraph, norm = 1.5 ):
                
        X =\
         len( self.getNodesWithDifferentNeighbors( secondGraph ) )
         
        VSizes =\
         self.getForwardStreakCardinality( secondGraph )
         
        WSizes =\
         self.getBackwardStreakCardinality( secondGraph )
         
        VSum = 0
        
        for v in VSizes:
            
            VSum = VSum + v**norm
             
        # end for v 
        
        WSum = 0
        
        for w in WSizes:
            
            WSum = WSum + w**norm
            
        # end for w
        
        similarityScore = ( X + VSum + 0.5 * WSum )**( 1/norm )
        
        return similarityScore
        
    # end function getSimilarityScore
    
    # Get the cardinality of each backward streak
    # This returns a list, where ith value is the
    # size of the ith backward streak. Basically,
    # |W_i| in Eq. 2
    def getBackwardStreakCardinality( self, secondGraph ):
        
        cardinality = []
        
        backwardStreaks =\
         self.getBackwardStreak( secondGraph )
         
        for streak in backwardStreaks:
             
            cardinality.append( len( streak ) )
             
        # end for
        
        return cardinality
        
    # end function getBackwardStreakCardinality
    
    # Get backward streaks
    # This returns W in Eq. 2
    def getBackwardStreak( self, secondGraph ):
        
        secondGraphBackward =\
         secondGraph.createBackwardGraph()
         
        backwardStreaks =\
         self.getForwardStreak( secondGraphBackward )
         
        return backwardStreaks 
        
    # end function getBackwardStreak
    
    # Create a new graph from the current one
    # Everything is the same but the vector
    # list is in the reversed order
    def createBackwardGraph( self ):
        
        backwardVectorList =\
         deepcopy( list( reversed( self.orderedVertexList ) ) )
         
        backwardGraph = Graph()
        
        backwardGraph.initializeADummyGraph( backwardVectorList )
        
        return backwardGraph
        
    # end function createBackwardGraph
    
    # Get the cardinality of the ith forward
    # streak in this graph and the input graph
    # This is similar to V_i in Eq. 2 
    # It returns a list that where ith location
    # is the cardinality of ith streak
    def getForwardStreakCardinality( self, secondGraph ):
        
        cardinality = []
        forwardStreaks = self.getForwardStreak( secondGraph )
        
        for streak in forwardStreaks:
            
            cardinality.append( len( streak ) )
            
        # end for
        
        return cardinality
        
    # end function getForwardStreakCardinality
    
    # Compute and return all forward streaks 
    # This is equivalent to V in Eq. 2
    def getForwardStreak( self, secondGraph ):
        
        forwardStreaks = []
        flatForwardStreaks = [];
        intersection = self.getIntersection( secondGraph )
        
        for node in intersection:
            
            if node in flatForwardStreaks:
                continue
            
            currentStreak = [node]
            index1 = self.orderedVertexList.index( node )
            index2 = secondGraph.orderedVertexList.index( node )
            
            while index1 < self.getNumberOfVertices()-1 and\
            index2 < secondGraph.getNumberOfVertices()-1:
                
                index1 = index1 + 1
                index2 = index2 + 1
                
                if self.orderedVertexList[index1] !=\
                secondGraph.orderedVertexList[index2]:
                    break
                
                currentStreak.append( self.orderedVertexList[index1] )
                flatForwardStreaks.append( self.orderedVertexList[index1] )
                
            # end while
            
            if len( currentStreak ) == 1:
                continue
            
            forwardStreaks.append( currentStreak )
            
        # end for node
        
        return forwardStreaks
        
    # end function getForwardStreak
    
    # This function returns the number of nodes in this
    # graph and the input graph that have different neighbors.
    # This is similar to |X| in Eq.2
    def getNodesWithDifferentNeighborsCardinality(\
        self, secondGraph ):
        
        nodesWithDifferentNeighbors =\
        self.getNodesWithDifferentNeighbors( secondGraph )
        
        return len( nodesWithDifferentNeighbors )
        
    # end function getNodesWithDifferentNeighborsCardinality
    
    # This function returns nodes in this graph and 
    # the input graph that have different neighbors.
    # Both neighbors must be different.
    # This computes X in Eq. 2 in the paper
    def getNodesWithDifferentNeighbors( self, secondGraph ):
        
        nodesWithDifferentNeighbors = []
        
        # Find common nodes in both graphs
        intersection = self.getIntersection( secondGraph )
        
        for node in intersection:
            
            flag = False
            
            neighborsThisGraph =\
            self.getNeighborsOfNode( node )
            
            neighborsSecondGraph =\
            secondGraph.getNeighborsOfNode( node )
            
            for neighbor in neighborsThisGraph:
                
                if neighbor in neighborsSecondGraph:
                    
                    flag = True
                                
            # end for neighbor
            
            if flag == True:
                continue
            
            nodesWithDifferentNeighbors.append( node )
            
        # end for node
        
        return nodesWithDifferentNeighbors
        
    # end function getNodesWithDifferentNeighbors
    
    # This function computes all the neighbors 
    # of the node 'node' in the graph
    def getNeighborsOfNode( self, node ):
        
        if node not in self.orderedVertexList:
            return []
        
        if self.numberOfVertices == 1: 
            return []
        
        index = self.orderedVertexList.index( node )
        
        if index == 1: 
            return [self.orderedVertexList[index+1]]
        
        if index == self.numberOfVertices-1:
            return [self.orderedVertexList[index-1]]
        
        return [self.orderedVertexList[index-1],\
                 self.orderedVertexList[index+1] ]
            
        
    # end function getNeighborsOfNode
    
    # Given this graph and an input graph, this function
    # computes the nodes that are common between the two
    def getIntersection( self, secondGraph ):
        
        intersection = [];
        
        # Find the common nodes
        for node in self.orderedVertexList:
        
            if node in secondGraph.orderedVertexList:
                intersection.append( node )
        
        # end for
        
        return intersection
        
    # end function getIntersection
    
    # Load a dummy graph so we have something to 
    # start with
    def initializeADummyGraph( self, nodesOrder = [] ):       
        
        if len( nodesOrder ) == 0:
            self.orderedVertexList =\
             [1, 3, 4, 5, 7, 6, 10, 9, 8]
             
        else:
            self.orderedVertexList =\
            nodesOrder
        # end if
         
        self.updateNumberOfVertices();
        
    # end function initializeADummyGraph
    
    # Determine how many nodes are there in the 
    # graph
    def getNumberOfVertices( self ):
        
        return len( self.orderedVertexList )
        
    # end function getNumberOfVertices
    
    # Make sure the number of nodes is consistend 
    # with the graph
    def updateNumberOfVertices( self ):
        
        self.numberOfVertices = self.getNumberOfVertices();
        
    # end function updateNumberOfVertices
    
# end class Graph

mygraph = Graph();
labelGraph = Graph();
mygraph.initializeADummyGraph()
labelGraph.initializeADummyGraph( [1,2,3,4,5,6,7,8,9,10] )
my_loss = labelGraph.getLossFunction( mygraph ) 

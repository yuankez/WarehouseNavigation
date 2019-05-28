# Python program to print DFS traversal from a
# given given graph
from collections import defaultdict
import numpy as np
from pprint import pprint

# This class represents a directed graph using
# adjacency list representation
class Graph:

    # Constructor
    def __init__(self, vertices, adjacency_Matrix):

        # print("Total number of vertices :\t ", vertices)
        # print("Warehouse Dimensions :\t", rows," X ", cols)

        print("Graph Constructor Called\n")
        # default dictionary to store graph
        self.graph = defaultdict(list)
        self.adjMatrix = adjacency_Matrix
        self.numVertices = vertices
        # function to add an edge to graph

    # Add Edges to the Graph
    def addEdge(self, u, v):
        self.graph[u].append(v)
        print(self.graph)
        pass

    # Recursive DFS Traversal
    def DFSUtil(self, v, visited, numVertices):
        print("*** DFSuntill CALLED FOR VERTEX **** :", v)
        # print("length Visited : ", len(visited))
        # Mark the current node as visited and print it

        # visited == 1
        if (visited[v] == -1):
            # print("DFS LOOP : ", v)
            print("\t>> Shelf detected at vetex, ", v)
            print("\t>> Skip to the next vertex ", v + 1)
            v = v + 1
            self.DFSUtil(v + 1, visited, numVertices)
        else:
            visited[v] = 1
            print("\tVisited : ", visited)

        # Recurse for all the vertices attached vertex
        shelfSkipCouter = 0
        # for i in self.graph[v]:
        # print("Print self.graph ", self.graph[v])
        for i in self.graph[v]:
            print("\tLoop : ", i)
            if (visited[i] == -1):          # shelf detected, not apart of tree traversal
                print("\t\t >> shelf skiped")
                # shelfSkipCouter = shelfSkipCouter + 1
                self.DFSUtil(i + 1, visited, numVertices)
            elif (visited[i] == 0):
                print("\t\t >> recusive call")
                self.DFSUtil(i, visited, numVertices)    # recursive call if not visited

    def newDFS(self, visited, pc_matrix, startingVertex, depthMax):
        distanceCounter = 0
        path = []
        visited = []
        currentVertex = startingVertex

        path.append(currentVertex)
        visited.append(currentVertex)
        # intizalize the next vertex
        nextNodeFound = False
        for j in range(self.numVertices):
            if(pc_matrix[startingVertex][j] == -1):
                nextVertex = j
                pc_matrix[nextVertex][currentVertex] = -1
                print(pc_matrix)
                nextNodeFound = True
                break
        if nextNodeFound == False:
            print("Error, improper starting vertex, no edges found")
            return
        else:
            print("Inital Starting At Vertex : ", currentVertex )
            print("\tNext node to visted, ", nextVertex)

        path.append(nextVertex)
        visited.append(nextVertex)

        currentVertex = nextVertex
        distanceCounter = distanceCounter + 1
        finishedExploring = False
        currentNodeVisited = False

        # PERFORM DFS
        while finishedExploring == False:
            print("VERTEX CURRENTLY AT : ", currentVertex)
            print("\tPC MATRIX BEFORE:")
            pprint(pc_matrix)



            # find the next next vertex
            nextNodeFound = False
            # if(currentNodeVisited == False):
            for j in range(numVertices):
                if pc_matrix[currentVertex][j] == 1:
                    nextVertex = j

                    # check to see if next node is in visisted list
                    nextNodeVisited = False
                    for i in range(len(visited)):
                        if nextVertex == visited[i]:
                            nextNodeVisited = True
                            print("Next Node Already Visited : ", nextVertex)
                            break

                    if(nextNodeVisited == False):
                        # update pc_matrix
                        pc_matrix[nextVertex][currentVertex] = -1
                        print("PC MATRIX MODEFIED")
                        # add vertex to visited list
                        visited.append(nextVertex)
                        nextNodeFound = True
                        print("\tNext node to visit, ", nextVertex)
                    break


            # if you didn't find the next node, back track your steps
            if(nextNodeFound == False):
                print("\tBack Tracking: end of branch reached at ", currentVertex)
                if (currentVertex == startingVertex):
                    print("GRAPH EXPLORED: LOCATION NOT FOUND")
                    return distanceCounter

                # get rid of last path vertex
                path.pop()

                # make sure pc_Matrix is marked

                nextVertex = path[-1]
                print("\tNext node to visted, ", nextVertex)
                pc_matrix[nextVertex][currentVertex] = -1

                currentVertex = nextVertex
                distanceCounter = distanceCounter - 1
            else:
                path.append(nextVertex)
                currentVertex = nextVertex
                distanceCounter = distanceCounter + 1
            print("PATH : ", path)
            print("VISITED : ", visited)

    # recursive DFSUtil()
    def DFS(self, vertex, shelfVertices, numVertices):

        print("Starting Location : ", vertex)
        print("length of visited : ", len(self.graph))

        # Modefied the AdjMatrix to show the parent
        intialPC = self.parent_Child_Matrix(vertex)
        visited = []
        # visited is going to be the size of the total number of vertices
        # Legend for visited
        # visited = -1  : there is a shelf at this vertex, not included in DFS traversal
        # visited = 0   : vertex has not been visited
        # visited = 1   : vertex has be visited

        shelfVertex = -1
        notVisited = 0

        # Initalize all vertices as not visited
        for i in range(numVertices):
            visited.append(notVisited)

        print("Visited : ", visited)
        print("Shelves to mark : ", shelfVertices)

        # Mark shelf vertices in the visited list
        # check to make sure starting location vertex isnt a shelf
        shelfCounter = 0
        for i in range(len(shelfVertices)):
            if shelfVertices[i] == 1:
                if(vertex == i):
                    print("Error: vertex is shelf")
                    return
                visited[i] = -1
                shelfCounter = shelfCounter + 1

        maxDepth = numVertices - shelfCounter
        print("After Shelf : ", visited)
        print("Final list: ", visited)

        self.newDFS(visited, intialPC, vertex, maxDepth)

        # Mark all the vertices as not visited
        # NOTE TO SELF:
        # Your orginal warehouse graph contains vertices that are shelves
        # The shelves must not be apart of the DFS or there is an indexing error
        # visited = [False] * (len(self.graph))

        # Call the recursive helper function to print
        # DFS traversal
        # self.DFSUtil(vertex, visited, numVertices)

    def parent_Child_Matrix(self, parentVertex):
        print("Creating Matrix for Backtracking Parent-Child")

        # create the starting point for parent node to explore as -1
        # If there is an edge, mark as 1
        # else mark as 0
        pc_Matrix = []
        parentFound = False
        for i in range(self.numVertices):
            row = []

            for j in range(self.numVertices):
                # If row is same as parent node, mark the first edge for initial exploration
                if i == parentVertex:
                    if self.adjMatrix[i][j] == 1 and parentFound == False:
                        row.append(-1)
                        parentFound = True
                    elif self.adjMatrix[i][j] == 1:
                        row.append(1)
                    else:
                        row.append(0)
                else: # for all other nodes
                    if self.adjMatrix[i][j] == 1:
                        row.append(1)
                    else:
                        row.append(0)
            pc_Matrix.append(row)
            print("\trow ", i, row)
        return pc_Matrix

        # Initialize the parent node as -1

def convert2DtoOneD(orginal2D, rows, cols):
    # Orinalnal 2D matrix
    # (row - 1, 0) ...      (row - 1, col - 1)
    #  ...
    # (1,1) > (1,1) > ... > (1, col - 1)
    # (0,0) > (0,1) > ... > (0, col - 1)

    # Return 1D matrix (this required for the nodes to make their graph
    # ((row - 1)) ...      (row - 1, col - 1)
    #  ...
    # (1 + col - 1) > (2 + col -1) > ... > (col - 1 + (col - 1))
    # (0) > (1) > ... > (col - 1)
    print("CONVERT 2-D TO 1-D ARRAY CALLED")
    newOneD = []
    # newOneD = orginal2D.flatten()
    print("ORGINAL 2D ARRAY:\n", orginal2D, "\n")

    for i in range(rows):
        for j in range(cols):
            # print("1-D INDEX = ", rows * i + j, "\n")
            newOneD.append(orginal2D[i][j])

    setShelves(newOneD, len(newOneD))

    print("2D SHELVES LEGEND Returning New 1D ARRAY:")
    printRowCount = 0
    printColCount = 0
    for i in range(rows * cols):
        if(i % cols == 0):
            print("Row : ", printRowCount)
            printColCount = 0
            print("\tCol ", printColCount, ", Vertex ", i, " : ",newOneD[i])
            printRowCount = printRowCount + 1
            printColCount = printColCount + 1
        else:
            print("\tCol ", printColCount, ", Vertex ", i, " : ", newOneD[i])
            printColCount = printColCount + 1
    print("TOTAL VERTICES: ", len(newOneD))
    print("NEW 1-D FORMAT: ", newOneD, "\n")
    return newOneD

def makeTESTSHELVES(rows, cols):
    for i in range(rows):
        shelfLine = []
        for j in range(cols):
            shelfLine.append(0)
        testShelf.append(shelfLine)
        print("Row ", i, shelfLine)

    # print("Converting into 1-D Shelves\n")
    # print("TEST SHELF:\n", testShelf)
    return testShelf

# DEBUGGING FUNCTION
# Set's artifical shelfList (final function will use .cvs file values)
# Returns shelfList, vertices which are shelves
#       ^^ needed to differentiante between nodes in DFS
def setShelves(shelves, numVertices):
    print("PLACEHOLDER FUNCTION: MAKE ANY VERTEX DIVISIBLE BY 4 A SHELF")
    shelfList = []

    for i in range(numVertices):
        divisibleBy4 = i % 4
        if(divisibleBy4 == 0 and i != 0):
            shelves[i] = 1
            shelfList.append(i)
    print("SHELVES LOCATED AT : ", shelfList)
    # for i in range(numVertices):
    #     if(shelves[i] == 1):
    #         print("Vertex ", i)

    return

# Returns the list of vertices that have shelves
# Used in DFS to ensure shelves aren't used in tree traversal
def getShelfVertices(shelfList, numVertices):
    shelfVertices = []

    shelfAtVertex = 1
    for i in range(numVertices):
        if(shelfList[i] == shelfAtVertex):
            shelfVertices.append(i)

    print("Shelves at Vertices: ", shelfVertices)
    return shelfVertices
#
# # Modefies the DFS visited list to remove shelf vertices from the DFS tree traversal
# # Used in DFS to ensure shelves aren't used in tree traversal
# def removeShelvesFromVisited(shelfList, visited):
#     for i in range(len(shelfList)):
#         index = shelfList[i]
#

# Returns the row coordinate and column coordinate from vertex
def getCoordinateVertex(vertex, rows, cols):
    print("FIND COORDINATE OF VERTEX: ", vertex)
    index = []
    # initialize to -1 to make sure they work
    row_Coordinate = -1
    col_Coordinate = -1

    for i in range(rows):
        for j in range(cols):
            calcIndex = cols * i + j
            if(vertex == calcIndex):
                row_Coordinate = i
                col_Coordinate = j
    print("ROW COORDINATE : ", row_Coordinate)
    print("COL COORDINATE : ", col_Coordinate)

    index.append(row_Coordinate)
    index.append(col_Coordinate)
    print("INDEX : ", index)
    return row_Coordinate, col_Coordinate

# def createWarehouseGraph(graph, numVertices, rows, cols, shelfList):
#     # Uses 1-D Lists to ensure easy static access
#     # Refer to 2-D to 1-D function for legend
#     # EXAMPLE)
#     # (row - 1, 0) ...      (row - 1, col - 1)
#     #  ...
#     # (1,1)      ^              ^
#     # (0,0) > (0,1) > ... > (0, col - 1)
#
#     # Build edges from shelf locations
#     #   1) check to the right of the node
#     #       a) if at the leftmost column (col - 1) no edge
#     #   2) check above the node
#     #       a) if at the topmost column graph (row - 1) no edge
#     #   3) if there is no shelf add an edge
#     print("Creating Warehouse")
#     print("Number Vertices ", numVertices)
#     print("Length of ShelfList ", len(shelfList))
#     noShelf = 0
#     maxRow = rows - 1
#     maxCol = cols - 1
#     print(maxRow, " ", maxCol)
#     #adjecency matrix
#     # -1    : is a shelf, not apart of tree traversal
#     # 0     : is not connected in dfs graph
#     # 1     : an edge, connected point
#     for vertex in range(numVertices):
#         print("VERTEX : ", vertex)
#         row_Coor, col_Coor = getCoordinateVertex(vertex, rows, cols)
#
#         # print("Vertex : ", vertex, "\tRow ", row_Coor, " Col ", col_Coor)
#         # if(row_Coor == maxRow):
#         #     print("why max row ", maxRow)
#         # if(col_Coor == maxCol):
#         #     print("why max col ", maxCol)
#
#         # check if the vertex itself is a shelf
#         if (shelfList[vertex] == noShelf):
#             # make sure to no add an edge to right at the end of column
#             if(col_Coor != maxCol):
#                 # check if there is a shelf to the right
#                 rightOfVertex = vertex + 1
#                 if(shelfList[rightOfVertex] == noShelf):
#                     graph.addEdge(vertex, rightOfVertex)
#                     print("EDGE CREATED : ( ", vertex, ", ", rightOfVertex, " )")
#
#             # make sure to no add an edge above at the top row
#             if(row_Coor != maxRow):
#                 # check if there is a shelf above
#                 aboveVertex = vertex + cols
#                 if(shelfList[aboveVertex] == noShelf):
#                     graph.addEdge(vertex, aboveVertex)
#                     print("EDGE CREATED : ( ", vertex, ", ", aboveVertex, " )")
#     return


# Version 2 adj matrix
def createWarehouseGraph(numVertices, rows, cols, shelfList):
    print("Creating Warehouse")
    print("Number Vertices ", numVertices)
    print("Length of ShelfList ", len(shelfList))
    print("ShelfList : ", shelfList)
    noShelf = 0
    maxRow = rows - 1
    maxCol = cols - 1
    print(maxRow, " ", maxCol)
    #adjecency matrix
    # -2    : is the same node
    # -1    : is a shelf, not apart of tree traversal
    # 0     : is not connected in dfs graph
    # 1     : an edge, connected point

    print("Creating Adjacency Matrix")
    adjacencyMatrix = []
    sameVertex = -2
    Shelf = -1
    noedge = 0
    edge = 1

    # Step 1) Initalizalize Adj Matrix sameVertex, Shelf
    #   ^^ doesnt fall under these categories is a no edge
    for i in range(numVertices):
        adj_Row = []
        for j in range(numVertices):
            if shelfList[i] != noShelf:
                adj_Row.append(Shelf)
            elif shelfList[j] != noShelf:
                adj_Row.append(Shelf)
            elif i == j:
                adj_Row.append(sameVertex)
            else:
                adj_Row.append(noedge)
        adjacencyMatrix.append(adj_Row)
        # Debugging
        print("Row ", i, " ", adj_Row)
    # print("Initial Total AM : ", adjacencyMatrix)

    # Step 2) Determine the Edges based on
    # Is the Vertex a shelf? skip it
    #   a. to the right of vertex
    #       - check vertex + 1 for shelf
    #       - check for end of column
    #   b. to the left of vertex
    #       - check vertex - 1 for shelf
    #       - check for start of column
    #   c. above vertex
    #       - check vertex + rowSize for shelf
    #       - check for topmost column
    #   d. below vertex
    #       - check vertex - rowSize shelf
    #       - check for bottommost column
    for vertex in range(numVertices):
        row_Coor, col_Coor = getCoordinateVertex(vertex, rows, cols)
        print("\tVertex ", vertex, " [ ", row_Coor,", ", col_Coor, " ]")

        # is vertex a shelf? No, then see what it's connected to
        if (shelfList[vertex] == noShelf):

            # a. check right of column
            if(col_Coor != maxCol):
                # check if there is a shelf to the right
                rightOfVertex = vertex + 1
                if(shelfList[rightOfVertex] == noShelf):
                    adjacencyMatrix[vertex][rightOfVertex] = edge
                    print("\tRIGHT EDGE CREATED : ( ", vertex, ", ", rightOfVertex, " )")

            # b. check left of vertex
            if(col_Coor != 0):
                leftOfVertex = vertex - 1
                if(shelfList[leftOfVertex] == noShelf):
                    adjacencyMatrix[vertex][leftOfVertex] = edge
                    print("\tLEFT EDGE CREATED : ( ", vertex, ", ", leftOfVertex, " )")

            # c. make sure to no add an edge above at the top row
            if(row_Coor != maxRow):
                # check if there is a shelf above
                aboveVertex = vertex + cols
                if(shelfList[aboveVertex] == noShelf):
                    adjacencyMatrix[vertex][aboveVertex] = edge
                    print("\tABOVE EDGE CREATED : ( ", vertex, ", ", aboveVertex, " )")

            # d. check below vertex
            if(row_Coor != 0):
                belowVertex = vertex - cols
                if(shelfList[belowVertex] == noShelf):
                    adjacencyMatrix[vertex][belowVertex] = edge
                    print("\tBELOW EDGE CREATED : ( ", vertex, ", ", belowVertex, " )")

    print("ADJ MATRIX")
    print(adjacencyMatrix)
    return adjacencyMatrix

# Create a graph given in the above diagram

# row = 16
# col = 25

# numVertices = row * col

# SMALL TEST FOR DEBUGGING INDIVIDUAL FUNCTIONS
rows = 4
cols = 3
numVertices = rows * cols
testShelf = []

testShelf = makeTESTSHELVES(rows, cols)
newTestShelf = convert2DtoOneD(testShelf, rows, cols)

# Create the warehouse based on warehouse dimensions and shelf locations
# Create warehouse produce adjacency matrix
adjMatrix = createWarehouseGraph(numVertices, rows, cols, newTestShelf)

graph = Graph(numVertices, adjMatrix)
# Paramenters: DFS(self, vertex, shelfVertices, numVertices)
graph.DFS(11, newTestShelf, numVertices)

# print(newTestShelf)
# make a shelf boolean matrix to test,
# initiallized no shelves = 0
# shelf will be marked as = 1


#
#
#
# graph.addEdge(0, 1)
# graph.addEdge(0, 2)
# graph.addEdge(1, 2)
# graph.addEdge(2, 0)
# graph.addEdge(2, 3)
# graph.addEdge(3, 3)
#
# print("Following is DFS from (starting from vertex 2)")
# graph.DFS(2)

# This code is contributed by Neelam Yadav
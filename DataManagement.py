import sys
import os
import math
#from WarehouseMap import Map
import json
import time
from collections import defaultdict
import collections

from queue import *

class Data:
    #global result_key,result_val
    #result_key = defaultdict(dict)
    #result_val = {}
    #def __init__(self, path,):
    #will change to self._init later

    def _init_(self):
        pass
    def inputdata(self, path):
        #filename = "/Users/Yuank/Desktop/WarehouseNavigation/MyFile.txt"
        filename = "" + path
        dataFile = open(filename, 'r')
        print("File read.")
        time.sleep(1)
        header = dataFile.readline().strip().split('\t')
        #print("Headers of Data = ", header)
        data = []
        count = 0
        temp = 0
        self.result_key = defaultdict(dict)
        self.result_val = {}
        # Currently in a list format with nested dictionary for every individual header
        for line in dataFile:
            col = line.strip().split('\t')
            row = dict()
            for j, i in enumerate(header):
                row[i] = col[j]
            data.append(row)

        for i in data:
            for key, value in i.items():
                if key == 'ProductID':
                    temp = value
                    # del result_key[temp]
                else:
                    self.result_val[key] = int(float(value))
            temp_dict = self.result_val.copy()
            self.result_key[temp] = temp_dict
            self.result_val.clear()
            count += 1
            #print(self.result_key)
            if count == 100:
               break
        dataFile.close()
        self.currentPos_list = list()
        for i in self.result_key.items():
            self.currentPos_list.append([i[1]['xLocation'], i[1]['yLocation']])
        print("before add", self.currentPos_list)

        #return self.result_key

    def finditemsinformation(self, product_ID):
        keys = self.result_key.keys()
        #print(self.result_key)
        #print(self.result_key[product_ID])
        if product_ID not in keys:
            print("Database does not have this item. Input Over")
        for key,value in self.result_key.items():
            if key == product_ID:
                print("Product: ", product_ID, "Location is: [", self.result_key[product_ID]['xLocation'],',', self.result_key[product_ID]['yLocation'],']')

    def print(self):
        print("[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]\n"
              "[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]\n"
              "[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]"
              "\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]\n[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1] \n[3, 0, 2, 0, 1, 1, 1, 1, 1, 1, 1]")
        print("find the path, get into it from North")
    def printworldtemp(self, startlocation, productID):
        self.rowmax = 0
        self.colmax = 0

        shelflist = list()
        self.avaliablepath = list()
        self.map = list()
        #self.print()
        for key,value in self.result_key.items():
            shelflist.append([self.result_key[key]['xLocation'], self.result_key[key]['yLocation']])
            tempy = self.result_key[key]['yLocation']
            tempx = self.result_key[key]['xLocation']
            if tempx > int(self.rowmax):
                self.rowmax = self.result_key[key]['xLocation']
            if  tempy > int(self.colmax):
                self.colmax = self.result_key[key]['yLocation']

        print("warehouse row siz is: ", self.rowmax, "warehouse column size is: ", self.colmax)

        self.directionclear(productID)

        for i in range(self.colmax+1):
            templist = list()
            for h in range(self.rowmax+2):
                if h == self.rowmax+1 and i < 10:
                    print(" ",self.colmax - i,"", end = '')
                elif h == self.rowmax+1 and i >= 10:
                    print(" ", self.colmax - i, " ",end='')
                elif [h,self.colmax -i] == startlocation:
                    self.avaliablepath.append([h,i])
                    print("  B  ", end = '')
                    if self.isvalid(h, self.colmax -i) == True and h <= self.rowmax and i <= self.colmax:
                        templist.append(1)
                    elif self.isvalid(h, self.colmax -i) == False and h <= self.rowmax and i <= self.colmax:
                        raise Exception("start location on the shelf wrong")
                        # or print pick up
                       # break
                elif [h,self.colmax -i] in shelflist:
                    print("  S  ", end = '')
                    if self.isvalid(h, self.colmax -i) == True and h <= self.rowmax and i <= self.colmax:
                        templist.append(1)
                        print('error')
                    elif self.isvalid(h,self.colmax- i) == False and h <= self.rowmax and i <= self.colmax:
                        #print(h,self.colmax-i)
                        templist.append(2)
                else:
                    if [h, self.colmax - i] != startlocation:
                        if self.isvalid(h, self.colmax-i) == True and h <= self.rowmax and i <= self.colmax:
                            templist.append(1)
                        elif self.isvalid(h, self.colmax-i) == False and h <= self.rowmax and i <= self.colmax:
                            #print("map has error . problem",h,i)
                            templist.append(0)
                        print("  .  ", end = '')
            self.map.append(templist)
            print('\n')

        for i in range(self.rowmax+2):
            if i == 0:
                print("", end = '')
            elif i == self.rowmax+1:
                print(" ", i-1," \n")
            elif i == self.rowmax+2:
                break
            elif i >= 10:
                print("  ", i-1, end = '')
            else:
                print(" ",i-1," ", end = '')
        for i in self.map:
            print(i)
        time.sleep(2)
        print("=============================================================================\n")
        #self.print()
    def printSolution(self, sol):
        sol.reverse()
        for i in (sol):
            print(i)
        print("=============================================================================\n")
        #print(sol)
        # for i in sol:
        #     for j in i:
        #         print(str(j) + " ", end="")
        #     print("")

    def findpathtoitem1(self, productID):
         #self.directionclear(productID)
         self.theitem = productID
         self.path_graph = dict()
         self.maprow = 0
         self.mapcal = 0
         for i in self.map:
             self.maprow = len(i)
             self.mapcal = self.mapcal + 1
         sol = [[0 for j in range(self.maprow)] for i in range(self.mapcal)]
         #print("here", sol)
         if self.theitem == '0':
             tempx = 0
             tempy = 0
         else:
           #  print(self.theitem)
           #  print(self.result_key)
             tempx = self.result_key[self.theitem]['xLocation']
             tempy = self.result_key[self.theitem]['yLocation']
         if self.mapsolutioncheck(self.map, 0, 0, sol) == False:
             print("Solution doesn't exist");
             return False

         self.printSolution(sol)
         return True

    def mapsolutioncheck(self, mapsize, x, y, sol):
        countx = 0
        for i in mapsize:

            for h in i:
                #print(self.productplacex,self.productplacey)
                #print(h,len(i))
                if h == self.productplacex and countx == self.productplacey:
                    # h is x ---- row y is cal ---- count
                    break
            countx = countx + 1
        if x == self.productplacex and y == self.productplacey:
            sol[x][y] = 3
            return True

            # Check if maze[x][y] is valid
        if self.isSafe(mapsize,x, y) == True:
            # mark x, y as part of solution path
            #print(x,y)
            sol[x][y] = 2

            # Move forward in x direction
            if self.mapsolutioncheck(mapsize, x + 1, y, sol) == True:
                return True

            # If moving in x direction doesn't give solution
            # then Move down in y direction
            if self.mapsolutioncheck(mapsize, x, y + 1, sol) == True:
                return True

            # If none of the above movements work then
            # BACKTRACK: unmark x, y as part of solution path
            sol[x][y] = 0
            return False


    def isSafe(self, maze, x, y ):
        #print(maze)
        # for i in maze:
        #     print(len(i))
        # print(len(maze))
        # print(self.maprow)
        # print(x,y)
        #print(len(maze))
        print(maze[x][y])
        if x >= 0 and x <= self.maprow-1 and y >= 0 and y <= self.mapcal-1 and maze[x][y] == 1:
            return True
        return False

    def directionclear(self, destination):
        for key,value in self.result_key.items():

            if key == destination:
                self.productplacex = self.result_key[key]['xLocation']
                self.productplacey = self.result_key[key]['yLocation']
                if self.result_key[key]['AccessS'] == 1:
                    if (self.productplacex-1,self.productplacey) not in self.currentPos_list and self.productplacex-1 >= 0:
                        self.currentPos_list.append([self.productplacex-1,self.productplacey])
                    if (self.productplacex+1,self.productplacey) not in self.currentPos_list and self.productplacex+1 <= self.rowmax:
                        self.currentPos_list.append([self.productplacex+1,self.productplacey])
                    if (self.productplacex,self.productplacey+1) not in self.currentPos_list and self.productplacey+1 <= self.colmax:
                        self.currentPos_list.append([self.productplacex,self.productplacey+1])

                elif self.result_key[key]['AccessN'] == 1:
                    if (self.productplacex-1,self.productplacey) not in self.currentPos_list and self.productplacex-1 >= 0:
                        self.currentPos_list.append([self.productplacex-1,self.productplacey])
                        #print(self.rowmax)
                    if (self.productplacex+1,self.productplacey) not in self.currentPos_list and self.productplacex+1 <= self.rowmax:
                        self.currentPos_list.append([self.productplacex+1, self.productplacey])
                        #print("why not")

                    if (self.productplacex,self.productplacey-1) not in self.currentPos_list and self.productplacey-1 >= 0:
                        self.currentPos_list.append([self.productplacex,self.productplacey-1])
                       # print("lool")
                    print("added successful", self.currentPos_list)
                elif self.result_key[key]['AccessE'] == 1:
                    if (self.productplacex-1,self.productplacey) not in self.currentPos_list and self.productplacex-1 >= 0:
                        self.currentPos_list.append([self.productplacex-1,self.productplacey])
                    if (self.productplacex,self.productplacey-1) not in self.currentPos_list and self.productplacey-1 >= 0:
                        self.currentPos_list.append([self.productplacex,self.productplacey-1])
                    if (self.productplacex,self.productplacey+1) not in self.currentPos_list and self.productplacey+1 <= self.colmax:
                        self.currentPos_list.append([self.productplacex,self.productplacey+1])
                    print("added successful",self.currentPos_list)
                elif self.result_key[key]['AccessW'] == 1:
                    if (self.productplacex+1,self.productplacey) not in self.currentPos_list and self.productplacex-1 >= 0:
                        self.currentPos_list.append([self.productplacex+1,self.productplacey])
                    if (self.productplacex,self.productplacey-1) not in self.currentPos_list and self.productplacey-1 >= 0:
                        self.currentPos_list.append([self.productplacex,self.productplacey-1])
                    if (self.productplacex,self.productplacey+1) not in self.currentPos_list and self.productplacey+1 <= self.colmax:
                        self.currentPos_list.append([self.productplacex, self.productplacey+1])
                    print("added successful",self.currentPos_list)

                #self.currentPos_list.append([i[1]['xLocation'], i[1]['yLocation']])

    def isvalid(self, row, column):
        if [row, column] in self.currentPos_list:
            #print(True)
            return False#
        else:
           # print(False)
            return True

    def findpathtoitem(self, productID):
        keys = self.result_key.keys()
        aimproduct = dict()
        currentlocation = [0,0]
        movehistory = list()
        movehistory.append(currentlocation)
        if productID not in keys:
            print("Database does not have this item. Input Over")
        for key,value in self.result_key.items():
            if key == productID:
                aimproduct[key] = value
        aimproductlocation = [aimproduct[productID]['xLocation'], aimproduct[productID]['yLocation']]
        print("start location: [0,0] ")
        time.sleep(1)
        print("product want to pick:", productID, "product location: ", aimproductlocation)
        time.sleep(1)



        print("Robot facing to left")



        for i in range(int(aimproductlocation[0])):
            if (int(aimproductlocation[0]) - int(currentlocation[0])) >= 0:
                currentlocation = [int(currentlocation[0])+1, int(currentlocation[1])]
                movehistory.append(currentlocation)
                time.sleep(1)
                print("Robot Moved Forward. Location now:", currentlocation)
        print("Robot turning left:")
        time.sleep(1)
        print("Robot moving up:")
        time.sleep(1)


        for h in range(int(aimproductlocation[1])):
            if (int(aimproductlocation[1]) - int(currentlocation[1])) >= 0:
                currentlocation = [int(currentlocation[0]), int(currentlocation[1])+1]
                movehistory.append(currentlocation)
                time.sleep(1)
                print("Robot Moved Forward. Location now:", currentlocation)
        if(currentlocation[0] == int(aimproductlocation[0]) and currentlocation[1] == int(aimproductlocation[1])):
            time.sleep(1)
            print("found the item! Pick it back!")
            time.sleep(1)
            check = input("If want to check the move history type yes, exit type no")
            if check == 'yes':
                print(movehistory)
            else:
                print("over")
        else:
            print('error, cant find the item')

    def findShortestWay(self, maze, ball, hole):
        """
        :type maze: List[List[int]]
        :type ball: List[int]
        :type hole: List[int]
        :rtype: str
        """
        ball, hole = tuple(ball), tuple(hole)
        dmap = collections.defaultdict(lambda: collections.defaultdict(int))
        w, h = len(maze), len(maze[0])
        for dir in 'dlru': dmap[hole][dir] = hole
        for x in range(w):
            for y in range(h):
                if maze[x][y] or (x, y) == hole: continue
                dmap[(x, y)]['u'] = dmap[(x - 1, y)]['u'] if x > 0 and dmap[(x - 1, y)]['u'] else (x, y)
                dmap[(x, y)]['l'] = dmap[(x, y - 1)]['l'] if y > 0 and dmap[(x, y - 1)]['l'] else (x, y)
        for x in range(w - 1, -1, -1):
            for y in range(h - 1, -1, -1):
                if maze[x][y] or (x, y) == hole: continue
                dmap[(x, y)]['d'] = dmap[(x + 1, y)]['d'] if x < w - 1 and dmap[(x + 1, y)]['d'] else (x, y)
                dmap[(x, y)]['r'] = dmap[(x, y + 1)]['r'] if y < h - 1 and dmap[(x, y + 1)]['r'] else (x, y)
        bmap = {ball: (0, '')}
        distance = lambda pa, pb: abs(pa[0] - pb[0]) + abs(pa[1] - pb[1])
        queue = collections.deque([(ball, 0, '')])
        while queue:
            front, dist, path = queue.popleft()
            for dir in 'dlru':
                if dir not in dmap[front]: continue
                np = dmap[front][dir]
                ndist = dist + distance(front, np)
                npath = path + dir
                if np not in bmap or (ndist, npath) < bmap[np]:
                    bmap[np] = (ndist, npath)
                    queue.append((np, ndist, npath))
        return bmap[hole][1] if hole in bmap else 'impossible'

    def inputproductIDcheck(self, productlist):
        templist = list()
        for key, value in self.result_key.items():
            templist.append(key)
        for i in productlist:
            if i not in templist:
                return False
        return True

    """
    def construct_graph(self):
        path_graph = dict()
        for position in self.avaliablepath:
            path_graph[position] = set()
        for key in path_graph:
            for position in self.currentPos_list:
                if position[0] == key[0] - 1 and position[1] == key[1]:
                    path_graph[key].add(position)
                elif position[0] == key[0] + 1 and position[1] == key[1]:
                    path_graph[key].add(position)
                elif position[0] == key[0] and position[1] == key[1] + 1:
                    path_graph[key].add(position)
                elif position[0] == key[0] and position[1] == key[1] - 1:
                    path_graph[key].add(position)
        return path_graph
    def shortest_path(self, graph, start, goal, path=None):
        # print(start,goal)
        if path is None:
            path = list()
        path = path + [start]
        if start == goal:
            self.found_shorest_back = True
            return path
        if start not in graph:
            return None
        # shortest = None
        paths = []
        for node in graph[start]:
            if not self.found_shorest_back:
                if node not in path:
                    new_path = self.shortest_path(graph, node, goal, path)
                    for p in new_path:
                        paths.append(p)
        return paths
"""


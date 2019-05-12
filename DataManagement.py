import sys
import os
import math
#from WarehouseMap import Map
import json
import time
from collections import defaultdict
import collections
#import Queue

from queue import *

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

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
        self.totalpath = 0
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
            # if count == 1000:
            #    break
        dataFile.close()
        #print(self.result_key.keys())
        self.currentPos_list = list()
        for i in self.result_key.items():
            #print(i[1])
            if [i[1]['xLocation'], i[1]['yLocation']] not in self.currentPos_list:
                self.currentPos_list.append([i[1]['xLocation'], i[1]['yLocation']])
        self.itemdict = defaultdict()
        self.rowmax = 0
        self.colmax = 0
        self.findrowcolmax()
        print("warehouse row siz is: ", self.rowmax, "warehouse column size is: ", self.colmax)
        return [self.rowmax,self.colmax]
        #print("before add", self.currentPos_list)

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

    def inserttobackend(self, startlocation, productID, count):
        self.count = count
        #set max length row and column
        self.startlocation = startlocation
        self.itemwewant = productID
        # associate with ID number x,y location and its direction
        # Positions contain shelf

        # find the entry location
        self.accessdestination = self.directionclear(productID)

        # find the item location
        self.itemwewantlocation = [self.productplacex,self.productplacey]

        # find row and colmax of map

        # store 2-D demention Map
        self.map = list()
        self.map = self.addinfotomap()#map[col][row]
        self.map.reverse()
        for i in self.map:
            print(i)
        self.map.reverse()

        #find path to item
        self.findpathtoitem1(startlocation,self.itemwewantlocation)
        return self.itemwewantlocation
        print('\n')
           # self.printworldtemp_frontend(startlocation,productID)

    def printworldtemp_frontend(self, startlocation, productID):

        self.avaliablepath = list()
        #self.print()
        for key,value in self.result_key.items():
            tempy = self.result_key[key]['yLocation']
            tempx = self.result_key[key]['xLocation']
            if tempx > int(self.rowmax):
                self.rowmax = self.result_key[key]['xLocation']
            if  tempy > int(self.colmax):
                self.colmax = self.result_key[key]['yLocation']

        print("warehouse row siz is: ", self.rowmax, "warehouse column size is: ", self.colmax)

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
                        # or print pick up
                       # break
                elif [h,self.colmax -i] in self.currentPos_list:
                    print("  S  ", end = '')
                else:
                    if [h, self.colmax - i] != startlocation:
                        print("  .  ", end = '')
            self.map.append(templist)
            print('\n')
        self.printcolumnnuber()
        time.sleep(2)
        print("=============================================================================\n")
        #self.print()


    def findpathtoitem1(self, startlocation, destination):
        self.startlocationrow = startlocation[0]
        self.startlocationcol = startlocation[1]
        destinationrow = destination[0]
        destinationcol = destination[1]
        ##################  structure
        self.rqueue = Queue()
        self.cqueue = Queue()
        self.map# using map exchange martrix size map
            #self.visited.append(temp)
        #print(self.map)

        #variable to track the number of steps taken.
        self.move_count = 0
        self.nodes_left_in_layer = 1
        self.nodes_in_next_layer = 0

        #track whether the 'E' character ever gets reached during the BFS
        self.reached_end = False

        #RxC matrix of false values used to track whether the node at position (i, j) has been visited
        self.visited = []
        for y in range(self.colmax):
            temp = []
            for x in range(self.rowmax):
                temp.append(False)
            self.visited.append(temp)


        self.dr = [-1, +1, 0 , 0] #direction vector for row and column
        self.dc = [0 , 0 , +1, -1]

        self.shortestpath = self.findpathtoitem1_solve()

        if self.shortestpath != 'The path is not eixt':
            self.totalpath += int(self.shortestpath)
            if self.count == 0:
                print("The Starting Location is ", "[", self.startlocationrow, ",", self.startlocationcol, "]")
                print("The Destination Location is ", "[", self.productplacex, ",", self.productplacey, "]")
                print("The shortest path from", self.startlocation)
                print("To Product ID: ", self.itemwewant, "Location: ", self.itemwewantlocation)
                print("The shortest path from Starting Position", self.startlocation, "to Next Product: ", self.itemwewant,
                      "Location: ", self.itemwewantlocation, "is", self.shortestpath)
                print("Now it take total steps: ", self.totalpath)
            elif self.count >= 0:
                print("Now it keep going from ", "[", self.startlocationrow, ",", self.startlocationcol, "]")
                print("To the next product ID", self.itemwewant)
                print("The next product location is ", "[", destinationrow, ",", destinationcol, "]")
                print("The shortest path from last product", self.startlocation, "to Next Product, ID:", self.itemwewant,"location:", self.itemwewantlocation,"is",self.shortestpath)
                print("Now it take total steps: ", self.totalpath)
        else:
            if self.count == 0:
                print("The Starting Location is ", "[", self.startlocationrow, ",", self.startlocationcol, "]")
                print("The Destination Location is ", "[", self.productplacex, ",", self.productplacey, "]")
                print("The shortest path from", self.startlocation)
                print("To Product ID: ", self.itemwewant, "Location: ", self.itemwewantlocation)
                print("self.shortestpath")
            elif self.count >= 0:
                print("Now it keep going from ", "[", self.startlocationrow, ",", self.startlocationcol, "]")
                print("To the next product ID:", self.itemwewant)
                print("The next product location is ", "[", destinationrow, ",", destinationcol, "]")
                print("The shortest path from last product", self.startlocation, "to Next Product: ", self.itemwewant, "Location: ", self.itemwewantlocation, "is", self.shortestpath)
                print("Now it take total steps: ", self.totalpath, "going back")

    def findpathtoitem1_solve(self):
        self.rqueue.enqueue(self.startlocationrow)
        self.cqueue.enqueue(self.startlocationcol)
        #print("debugging findsolve")
        #print(self.rqueue.size(),self.cqueue.size())
        self.visited[self.startlocationcol][self.startlocationrow] = True
        #print(self.map[1][2])
        while self.rqueue.size() > 0:
            r = self.rqueue.dequeue()
            c = self.cqueue.dequeue()
            #print(self.map[r][c])
            if self.map[c][r] == 3:
                self.reached_end = True
                break

            self.explor_neighbours(r,c)
            self.nodes_left_in_layer -= 1
            if self.nodes_left_in_layer == 0:
                self.nodes_left_in_layer = self.nodes_in_next_layer
                self.nodes_in_next_layer = 0
                self.move_count += 1
                #print(self.move_count)
        if self.reached_end:
            return self.move_count + 1 # at the front door need one more step
        return "The path is not eixt"

        pass

    def explor_neighbours(self, r, c):
        for i in range(4):
            rr = r + self.dr[i]# rr is current row coordinate
            cc = c + self.dc[i]#cc is current col coordinat
            if rr < 0 or cc < 0: # rr and cc is neighbouring cell of (r,c)
                continue
            if rr >= self.rowmax or cc >= self.colmax:
                continue

            #skip visited locations or blocked cells

            if self.visited[cc][rr]:
                continue
            if self.map[cc][rr] == '0':
                continue

            self.rqueue.enqueue(rr)
            self.cqueue.enqueue(cc)
            #print(self.rqueue.items)
            self.visited[cc][rr] = True
            self.nodes_in_next_layer = self.nodes_in_next_layer+1




    def directionclear(self, destination):
        for key,value in self.result_key.items():

            if key == destination:
                self.productplacex = self.result_key[key]['xLocation']
                self.productplacey = self.result_key[key]['yLocation']
                if self.result_key[key]['AccessS'] == 1:
                    return [self.productplacex,self.productplacey-1]

                elif self.result_key[key]['AccessN'] == 1:
                    return [self.productplacex, self.productplacey +1]
                       # print("lool")
                    #print("added successful", self.currentPos_list)
                elif self.result_key[key]['AccessE'] == 1:
                    return [self.productplacex+1, self.productplacey]
                    #print("added successful",self.currentPos_list)
                elif self.result_key[key]['AccessW'] == 1:
                    return [self.productplacex-1, self.productplacey - 1]

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
        print(distance(ball,hole))
        return bmap[hole][1] if hole in bmap else 'impossible'

    def inputproductIDcheck(self, productlist):
        templist = list()
        for key, value in self.result_key.items():
            templist.append(key)
        for i in productlist:
            if i not in templist:
                return False
        return True

    def printcolumnnuber(self):
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

    def findrowcolmax(self):
        for key, value in self.result_key.items():
            self.itemdict[key] = [self.result_key[key]['xLocation'], self.result_key[key]['yLocation']]
            #print(self.itemdict)
            tempy = self.result_key[key]['yLocation']
            tempx = self.result_key[key]['xLocation']
            if tempx > int(self.rowmax):
                self.rowmax = self.result_key[key]['xLocation']
            if tempy > int(self.colmax):
                self.colmax = self.result_key[key]['yLocation']

    def addinfotomap(self):
        for i in range(self.colmax):
            #print(i,"number i ")
            templist = list()
            for h in range(self.rowmax):
                #print("number h",h)
                if [h,i] == self.startlocation:
                    #raise Exception("start location on the shelf wrong")
                    # break
                    templist.append(2)
                elif [h,i] == self.accessdestination:
                    templist.append(3)
                    #print("check here", h,i)
                elif [h, i] in self.currentPos_list:
                    templist.append(0)
                else:
                    templist.append(1)
            self.map.append(templist)
        #print("look here", self.map[15][19])
        return self.map
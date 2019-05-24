import sys
import os
import math
#from WarehouseMap import Map
import json
import time
from collections import defaultdict
import collections
from itertools import combinations, permutations
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

    def analysisinput(self, itemslist,startlocation):
        self.storpath = []
        self.itemslist = itemslist
        self.primelist = list(permutations(self.itemslist, len(self.itemslist)))
        self.pathdict = defaultdict()
        self.startlocation = startlocation
        self.count = 0
        printmap = 0
        self.totalpathlist = []
        #print(self.primelist)
        self.itemwepreviouswant = 0
        for prime in self.primelist:
            for item in prime:
                if self.count == 0:
                    self.inserttobackend(startlocation,item,printmap)
                    self.itemwepreviouswant = item
                else:
                    self.inserttobackend(self.itemwewantlocation,item,printmap)
                    self.itemwepreviouswant = item
                self.count += 1
                printmap += 1
            self.count = 0
            self.totalpathlist.append(self.totalpath)
            self.totalpath = 0
            #print(self.totalpathlist)
        realshortest = 0
        for i in self.totalpathlist:
             if realshortest == 0:
                 realshortest = i
             elif i <= realshortest:
                 realshortest = i
        return ("The shortest path is: ", realshortest)


    def inserttobackend(self, startlocation, productID,counts):
        #self.count = count
        #set max length row and column
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

        colnumber = 0
        templist = []
        # for i in self.map:
        #     print(i, self.colmax-colnumber)
        #     colnumber += 1
        # for i in range(self.rowmax):
        #     templist.append(i)
        # print(templist)
        ##################################################put it back later
        if counts == 0:
            self.printworldtemp_frontend()
        self.map.reverse()

        #find path to item
        self.path = self.findpathtoitem1(startlocation,self.itemwewantlocation)
        if self.path != 'The path is not eixt':
            self.totalpath += int(self.path)
        #return self.itemwewantlocation
        #print('\n')
           # self.printworldtemp_frontend(startlocation,productID)
        if self.count == 0:
            self.storpath.append([startlocation, [self.itemwewant, self.path]])
        else:
            self.storpath.append([self.itemwepreviouswant, [self.itemwewant, self.path]])

        #print(self.storpath)

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
        if len(self.storpath)>0:
            for key in self.storpath:
                if key[0] == self.itemwepreviouswant and key[1][0] == self.itemwewant:
                    return key[1][1]
                else:
                    pass

        for y in range(self.colmax):
            temp = []
            for x in range(self.rowmax):
                temp.append(False)
            self.visited.append(temp)


        self.dr = [-1, +1, 0 , 0] #direction vector for row and column
        self.dc = [0 , 0 , +1, -1]

        self.shortestpath = self.findpathtoitem1_solve()
        return self.shortestpath
        #     if self.count == 0:
        #         print("The Starting Location is ", "[", self.startlocationrow, ",", self.startlocationcol, "]")
        #         print("The Destination Location is ", "[", self.productplacex, ",", self.productplacey, "]")
        #         print("The shortest path from", self.startlocation)
        #         print("To Product ID: ", self.itemwewant, "Location: ", self.itemwewantlocation)
        #         print("The shortest path from Starting Position", self.startlocation, "to Next Product: ", self.itemwewant,
        #               "Location: ", self.itemwewantlocation, "is", self.shortestpath)
        #         print("Now it take total steps: ", self.totalpath)
        #     elif self.count >= 0:
        #         print("Now it keep going from ", "[", self.startlocationrow, ",", self.startlocationcol, "]")
        #         print("To the next product ID", self.itemwewant)
        #         print("The next product location is ", "[", destinationrow, ",", destinationcol, "]")
        #         print("The shortest path from last product", self.startlocation, "to Next Product, ID:", self.itemwewant,"location:", self.itemwewantlocation,"is",self.shortestpath)
        #         print("Now it take total steps: ", self.totalpath)
        # else:
        #     if self.count == 0:
        #         print("The Starting Location is ", "[", self.startlocationrow, ",", self.startlocationcol, "]")
        #         print("The Destination Location is ", "[", self.productplacex, ",", self.productplacey, "]")
        #         print("The shortest path from", self.startlocation)
        #         print("To Product ID: ", self.itemwewant, "Location: ", self.itemwewantlocation)
        #         print("self.shortestpath")
        #     elif self.count >= 0:
        #         print("Now it keep going from ", "[", self.startlocationrow, ",", self.startlocationcol, "]")
        #         print("To the next product ID:", self.itemwewant)
        #         print("The next product location is ", "[", destinationrow, ",", destinationcol, "]")
        #         print("The shortest path from last product", self.startlocation, "to Next Product: ", self.itemwewant, "Location: ", self.itemwewantlocation, "is", self.shortestpath)
        #         print("Now it take total steps: ", self.totalpath, "going back")

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
                elif [h,i] == self.itemwewantlocation:
                    templist.append(4)
                    #print("check here", h,i)
                elif [h, i] in self.currentPos_list:
                    templist.append(0)
                else:
                    templist.append(1)
            self.map.append(templist)
        #print("look here", self.map[15][19])
        return self.map

    def printworldtemp_frontend(self):

        self.avaliablepath = list()
        # self.print()
        count_number = 0
        for y in self.map:
            templist = list()
            for x in y:

                if x == 1:
                    print("  .  ", end='')
                elif x == 0:
                    print("  S  ", end='')
                    # or print pick up
                    # break
                elif x == 2:
                    print("  B  ", end='')
                elif x == 3:
                    print("  E  ", end='')
                elif x == 4:
                    print("  D  ", end='')
            print(self.colmax - 1 - count_number)
            count_number += 1
            print("\n")

        for i in range(self.rowmax):
            if i < 10:
                print(" ", i, " ", end='')
            elif i == 10:
                print(" ", i, " ", end='')
            else:
                print("", i, " ", end='')
        time.sleep(1)
        print("\n")
        print("=============================================================================\n")
        # self.print()

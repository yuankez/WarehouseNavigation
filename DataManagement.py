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
            # if count == 50:
            #     break
        dataFile.close()
        #print(self.result_key.keys())
        self.currentPos_list = list()
        for i in self.result_key.items():
            if [i[1]['xLocation'], i[1]['yLocation']] not in self.currentPos_list:
                self.currentPos_list.append([i[1]['xLocation'], i[1]['yLocation']])
        self.itemdict = defaultdict()
        self.rowmax = 0
        self.colmax = 0
        self.findrowcolmax()

        # store 2-D demention Map
        self.map = self.addinfotomap()#map[col][row]
        self.map.reverse()
        self.printworldtemp_frontend()
        self.map.reverse()

        print("warehouse row siz is: ", self.rowmax, "warehouse column size is: ", self.colmax)
        return [self.rowmax,self.colmax]

        #return self.result_key

    def finditemsinformation(self, product_ID):
        keys = self.result_key.keys()
        if product_ID not in keys:
            print("Database does not have this item. Input Over")
        for key,value in self.result_key.items():
            if key == product_ID:
                print("Product: ", product_ID, "Location is: [", self.result_key[product_ID]['xLocation'],',', self.result_key[product_ID]['yLocation'],']')

    def analysisinput(self, itemslist,startlocation):
        self.storpath = []
        self.pathlist = []
        self.itemslist = itemslist
        self.primelist = list(permutations(self.itemslist, len(self.itemslist)))
        self.pathdict = defaultdict()
        self.startlocation = startlocation
        count = 0
        printmap = 0
        self.totalpathlist = []
        self.itemwepreviouswant = 0
        self.mapstore = []

        for prime in self.primelist:
            for item in prime:
                if count == 0:
                    self.startlocation = startlocation
                    self.startlocation = self.inserttobackend(self.startlocation,item,count)
                    #print("The starting location",self.startlocation)
                    self.itemwepreviouswant = item
                else:
                    self.startlocation = self.inserttobackend(self.startlocation, item, count)
                    self.itemwepreviouswant = item

                count += 1
                printmap += 1
            self.mapstore.append([self.totalpath, self.map])
            count = 0
            self.totalpathlist.append(self.totalpath)
            self.addinfotomap()
            self.totalpath = 0
            self.itemwepreviouswant = 0
            self.startlocation = startlocation

        realshortest = 0
        for i in self.totalpathlist:
             if realshortest == 0:
                 realshortest = i
             elif i <= realshortest:
                 realshortest = i

        pathlist = self.putresultpath()
        map2 = self.addinfotomap2(pathlist)
        #self.printworldtemp_frontend2(self.mapstore)
        self.printworldtemp_frontend2(map2)

        return ("The shortest path is: ", realshortest)


    def inserttobackend(self, startlocation, productID, counts):

        #set max length row and column
        self.itemwewant = productID
        # associate with ID number x,y location and its direction
        # Positions contain shelf

        # find the entry location
        self.accessdestination = self.directionclear(productID)

        # find the item location
        self.itemwewantlocation = [self.productplacex,self.productplacey]

        # find row and colmax of map
        self.changemapinfo()

        #find path to item
        self.path = self.findpathtoitem1(startlocation,self.itemwewantlocation)
        if self.path[0] != 'The path is not eixt':
            self.totalpath += int(self.path[0])
            self.pathlist.append(self.path[1])
        #print(self.pathlist)
        #return self.itemwewantlocation
        #print('\n')
           # self.printworldtemp_frontend(startlocation,productID)
        if counts == 0:
            self.storpath.append([startlocation, [self.itemwewant, self.path]])
        else:
            self.storpath.append([self.itemwepreviouswant, [self.itemwewant, self.path]])

        return self.itemwewantlocation

    def findpathtoitem1(self, startlocation, destination):
        self.startlocationrow = startlocation[0]
        self.startlocationcol = startlocation[1]
        destinationrow = destination[0]
        destinationcol = destination[1]
        ##################  structure
        self.rqueue = Queue()
        self.cqueue = Queue()
        self.map  # using map exchange martrix size map
        # self.visited.append(temp)
        # print(self.map)
        self.node_parent = {}
        self.path = []
        # use to store the shortest path

        # variable to track the number of steps taken.
        self.move_count = 0
        self.nodes_left_in_layer = 1
        self.nodes_in_next_layer = 0

        # track whether the 'E' character ever gets reached during the BFS
        self.reached_end = False

        # RxC matrix of false values used to track whether the node at position (i, j) has been visited
        self.visited = []
        for y in range(self.colmax):
            temp = []
            for x in range(self.rowmax):
                temp.append(False)
            self.visited.append(temp)

        self.dr = [-1, +1, 0, 0]  # direction vector for row and column
        self.dc = [0, 0, +1, -1]

        self.shortestpath = self.findpathtoitem1_solve()
       # print(self.shortestpath, "I am here")

        if self.shortestpath != 'The path is not eixt':
            # self.totalpath += self.shortestpath
            return [self.shortestpath, self.path]
        else:
            raise ValueError('The path is not eixt')
            return 0

    def findpathtoitem1_solve(self):
        self.rqueue.enqueue(self.startlocationrow)
        self.cqueue.enqueue(self.startlocationcol)
        self.visited[self.startlocationcol][self.startlocationrow] = True
        while self.rqueue.size() > 0:
            r = self.rqueue.dequeue()
            c = self.cqueue.dequeue()
            if self.map[c][r] == 3:
                self.reached_end = True
                self.backtrack(r, c)  # find the path
                break

            self.explor_neighbours(r, c)
            self.nodes_left_in_layer -= 1
            if self.nodes_left_in_layer == 0:
                self.nodes_left_in_layer = self.nodes_in_next_layer
                self.nodes_in_next_layer = 0
                self.move_count += 1
        if self.reached_end:
            return self.move_count + 1  # at the front door need one more step
        return "The path is not eixt"

        pass

    def explor_neighbours(self, r, c):
        for i in range(4):
            rr = r + self.dr[i]  # rr is current row coordinate
            cc = c + self.dc[i]  # cc is current col coordinat
            if rr < 0 or cc < 0:  # rr and cc is neighbouring cell of (r,c)
                continue
            if rr >= self.rowmax or cc >= self.colmax:
                continue

            # skip visited locations or blocked cells

            if self.visited[cc][rr]:
                continue
            if self.map[cc][rr] == 0:
                continue

            self.rqueue.enqueue(rr)
            self.cqueue.enqueue(cc)
            self.visited[cc][rr] = True
            self.node_parent[(cc, rr)] = (c, r)
            self.nodes_in_next_layer = self.nodes_in_next_layer + 1

    def backtrack(self, r, c):
        pr, pc = r, c
        while pr != self.startlocationrow or pc != self.startlocationcol:
            # print(pr,pc)
            self.path.append((pr, pc))
            # print("append",(pc,pr))
            pc, pr = self.node_parent[(pc, pr)]
            # print("parent,",(pc,pr))
        # print(self.node_parent)
        # print(pc,pr)
        # print(self.startlocationrow,self.startlocationcol)
        self.path.append((pr, pc))
        self.path.reverse()



    def directionclear(self, destination):
        for key,value in self.result_key.items():

            if key == destination:
                self.productplacex = self.result_key[key]['xLocation']
                self.productplacey = self.result_key[key]['yLocation']
                if self.result_key[key]['AccessS'] == 1:
                    return [self.productplacex,self.productplacey-1]

                elif self.result_key[key]['AccessN'] == 1:
                    return [self.productplacex, self.productplacey +1]
                elif self.result_key[key]['AccessE'] == 1:
                    return [self.productplacex+1, self.productplacey]
                elif self.result_key[key]['AccessW'] == 1:
                    return [self.productplacex-1, self.productplacey - 1]


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
        self.map = list()
        for i in range(self.colmax):
            templist = list()
            for h in range(self.rowmax):
                #print("number h",h)
                # if [h,i] == self.startlocation:
                #     #raise Exception("start location on the shelf wrong")
                #     # break
                #     templist.append(2)
                # elif [h,i] == self.accessdestination:
                #     templist.append(3)
                # elif [h,i] == self.itemwewantlocation:
                #     templist.append(4)
                    #print("check here", h,i)
                if [h, i] in self.currentPos_list:
                    templist.append(0)
                else:
                    templist.append(1)
            self.map.append(templist)
        #print("look here", self.map[15][19])
        return self.map

    def changemapinfo(self):
        self.map[self.startlocation[1]][self.startlocation[0]] = 2
        self.map[self.accessdestination[1]][self.accessdestination[0]] = 3
        self.map[self.itemwewantlocation[1]][self.itemwewantlocation[0]] = 4



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

    def putresultpath(self):
        resultlist = []
        for i in self.pathlist:
            for g in i:
                #print(g)
                resultlist.append(g)
        return resultlist

    def addinfotomap2(self,resultlist):
        print("final path list:", resultlist)
        map2 = []
        #print(resultlist)
        #print([1,2] in resultlist)
        for i in range(self.colmax):
            # print(i,"number i ")
            templist = list()
            for h in range(self.rowmax):
                # print("number h",h)
                if [h, i] == self.startlocation:
                    # raise Exception("start location on the shelf wrong")
                    # break
                    templist.append(2)
                elif [h,i] == self.accessdestination:
                    templist.append(3)
                elif (h,i) in resultlist:
                    templist.append(5)
                elif [h, i] in self.currentPos_list:
                    templist.append(0)
                elif [h, i] == self.itemwewantlocation:
                    templist.append(4)
                    # print("check here", h,i)
                else:
                    templist.append(1)
            #print(templist)
            map2.append(templist)
        # print("look here", self.map[15][19])
        return map2


    # def printworldtemp_frontend2(self, mapstore):
    #     count_number = 0
    #     findshortes = 10000000
    #     map2 = list()
    #     for key in mapstore:
    #         if key[0] <= findshortes:
    #             findshortes = key[0]
    #             map2 = key[1]
    #     map2.reverse()
    #     for y in map2:
    #         templist = list()
    #         for x in y:
    #
    #             if x == 1:
    #                 print(" . ", end='')
    #             elif x == 0:
    #                 print(" S ", end='')
    #                 # or print pick up
    #                 # break
    #             elif x == 2:
    #                 print(" B ", end='')
    #             elif x == 3:
    #                 print(" O ", end='')
    #             elif x == 4:
    #                 print(" D ", end='')
    #             elif x == 5:
    #                 print(" O ", end='')
    #         print(self.colmax - 1 - count_number)
    #         count_number += 1
    #     for i in range(self.rowmax):
    #
    #         if i < 10:
    #             print("", i, "", end='')
    #         elif i == 10:
    #             print("", i, "", end='')
    #         else:
    #             print("",i, end='')
    #     time.sleep(1)
    #     print("\n")
    #     print("=============================================================================\n")
    def printworldtemp_frontend2(self, map2):
        count_number = 0
        map2.reverse()
        for y in map2:
            templist = list()
            for x in y:

                if x == 1:
                    print(" . ", end='')
                elif x == 0:
                    print(" S ", end='')
                    # or print pick up
                    # break
                elif x == 2:
                    print(" B ", end='')
                elif x == 3:
                    print(" O ", end='')
                elif x == 4:
                    print(" D ", end='')
                elif x == 5:
                    print(" O ", end='')
            print(self.colmax - 1 - count_number)
            count_number += 1
        for i in range(self.rowmax):

            if i < 10:
                print("", i, "", end='')
            elif i == 10:
                print("", i, "", end='')
            else:
                print("",i, end='')
        time.sleep(1)
        print("\n")
        print("=============================================================================\n")
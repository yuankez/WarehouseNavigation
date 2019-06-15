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
import threading
import datetime
import time

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

from itertools import combinations, permutations


class Algorithm():


    def Brut_Force(self, distance_dict, testcase):

        # result path
        storepath = []

        # dict
        pathdict = distance_dict

        #steps count for shortest path
        shortest_path_count = 0
        Final_path_cout = 0

        #every possible combination for testcase
        primelist = list(permutations(testcase, len(testcase)))
        items_to_item = pathdict.keys()

        #print("Prime list",primelist)
        #print("Path dict keys:", items_to_item, "values", pathdict.values())
        #starting location is solid

        startlocation = '0'
        # for i in range(0, len(primelist), int(len(primelist)/2)):
        #     print(primelist[i:i + int(len(primelist)/2)])
        #     mythread = Getmessage(lineslist, i * (length // (n - 1)), (i + 1) * (length // (n - 1)), findstr)  # 创建类线程对象，将文件均等分割，将分割后的索引传入
        #     mythread.start()  # 开启线程
        #     threadlist.append(mythread)  # 将线程装入列表

        for prime in primelist:
            # print("This time prime:", prime)
            for item in prime:
                if shortest_path_count >= Final_path_cout and Final_path_cout != 0:
                    pass
                elif (startlocation, item) in items_to_item:
                    shortest_path_count += pathdict.get((startlocation,item))
                    startlocation = item
                elif (item, startlocation) in items_to_item:
                    shortest_path_count += pathdict.get((item,startlocation))
                    startlocation = item
            if Final_path_cout == 0:
                Final_path_cout = shortest_path_count
                storepath = prime
            elif Final_path_cout > shortest_path_count:
                Final_path_cout = shortest_path_count
                storepath = prime
            shortest_path_count = 0
        print("The shortes path after optimized is:", storepath)
        storepath = storepath + ('01',)
        print("The steps count for total:", Final_path_cout)

        return [Final_path_cout, storepath]


    def Nearest_Neighbour(self, distance_dict, testcase, startlocation, Init_Map,colmax, rowmax, Items_information):
        self.result_key = Items_information
        self.map = Init_Map
        self.colmax = colmax
        self.rowmax = rowmax
        self.testcase = testcase
        self.startID = '0'
        self.endID = '01'


        distance_map = self.make_distance_map(self, distance_dict,self.testcase,startlocation, Items_information)


        return distance_map











    def make_distance_map(self, distance_dict, testcase, startlocation, Items_information):
        self.testcase = sorted(testcase + ['0'])
        self.temp_testcase = self.testcase.copy()

        Map = []
        result_order = []
        #print(self.testcase)
        temp_shortest = 999999
        temp_shortest_item = ''
        first_startlocation = startlocation
        print("input startlocation:", first_startlocation)

        count = 0
        result = 0
        first_item = self.testcase[count]

        while(len(self.temp_testcase) != 0):
            if first_item in self.temp_testcase:
                self.temp_testcase.remove(first_item)
            for item in self.temp_testcase:
                if count == 0:
                    item_location = self.finditemsinformation(self,item)
                    accessdestination_X = self.find_location(self, item)
                    shortest = self.findpathtoitem1(self, startlocation, accessdestination_X)

                    self.map[accessdestination_X[1]][accessdestination_X[0]] = 1
                    #print(temp_shortest>shortest)
                    if temp_shortest > shortest:
                        temp_shortest = shortest
                        temp_shortest_item = item
                else:
                    #print(first_item)
                    first_startlocation = self.finditemsinformation(self, first_item)
                    item_location = self.finditemsinformation(self, item)

                    accessdestination_X = self.find_location(self, item)

                    shortest = self.findpathtoitem1(self, first_startlocation, accessdestination_X)
                    self.map[accessdestination_X[1]][accessdestination_X[0]] = 1

                    if temp_shortest > shortest:
                        temp_shortest = shortest
                        temp_shortest_item = item

            Map = Map + [first_item,"->",temp_shortest_item,':', temp_shortest]
            result_order = result_order + [temp_shortest_item]
            result += temp_shortest
            self.temp_testcase.remove(temp_shortest_item)
            count += 1
            self.testcase.remove(first_item)
            first_item = temp_shortest_item
            temp_shortest_item = ''
            temp_shortest = 99999

        result_order = result_order + ['01']
        #print(Map)
        #print(result)
        #print(result_order)

        return (result_order, result)





    def findpathtoitem1(self, startlocation, destination):
        startlocationrow = startlocation[0]
        startlocationcol = startlocation[1]
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

        shortestpath = self.findpathtoitem1_solve(self, startlocationrow, startlocationcol)
        # print(self.shortestpath, "I am here")

        if shortestpath != 'The path is not eixt':
            return shortestpath
        else:
            raise ValueError('The path is not eixt')
            return 0

    def findpathtoitem1_solve(self, startlocationrow, startlocationcol):

        self.rqueue.enqueue(startlocationrow)
        self.cqueue.enqueue(startlocationcol)
        self.visited[startlocationcol][startlocationrow] = True
        while self.rqueue.size() > 0:
            r = self.rqueue.dequeue()
            c = self.cqueue.dequeue()
            if self.map[c][r] == 3:
                self.reached_end = True
                #self.backtrack(self, r, c, startlocationrow, startlocationcol)  # find the path
                break

            self.explor_neighbours(self, r, c)
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

    def backtrack(self, r, c, startlocationrow, startlocationcol):
        pr, pc = r, c
        while pr != startlocationrow or pc != startlocationcol:
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


    def find_location(self, destination):
        for key, value in self.result_key.items():  # fix next
            if key == destination:
                self.productplacex = self.result_key[key]['xLocation']
                self.productplacey = self.result_key[key]['yLocation']
                destination = [self.productplacex, self.productplacey]
                self.map[self.productplacey][self.productplacex] = 4
                if self.result_key[key]['AccessS'] == 1:
                    self.map[self.productplacey - 1][self.productplacex] = 3
                    accessdestination = [self.productplacex, self.productplacey - 1]
                    return accessdestination

                elif self.result_key[key]['AccessN'] == 1:
                    self.map[self.productplacey + 1][self.productplacex] = 3
                    accessdestination = [self.productplacex, self.productplacey + 1]
                    return accessdestination

                elif self.result_key[key]['AccessE'] == 1:
                    self.map[self.productplacey][self.productplacex + 1] = 3
                    accessdestination = [self.productplacex + 1, self.productplacey]
                    return accessdestination
                elif self.result_key[key]['AccessW'] == 1:
                    self.map[self.productplacey][self.productplacex - 1] = 3
                    accessdestination = [self.productplacex - 1, self.productplacey]
                    return accessdestination


    def finditemsinformation(self, product_ID):
        keys = self.result_key.keys()
        if product_ID not in keys:
            print("Database does not have this item. Input Over")
        for key,value in self.result_key.items():
            if key == product_ID:
                return [self.result_key[product_ID]['xLocation'], self.result_key[product_ID]['yLocation']]

    def find_location2(self, destination):
        for key, value in self.result_key.items():  # fix next
            if key == destination:
                self.productplacex = self.result_key[key]['xLocation']
                self.productplacey = self.result_key[key]['yLocation']

                if self.result_key[key]['AccessS'] == 1:

                    accessdestination = [self.productplacex, self.productplacey - 1]
                    return  accessdestination

                elif self.result_key[key]['AccessN'] == 1:

                    accessdestination = [self.productplacex, self.productplacey + 1]
                    return  accessdestination

                elif self.result_key[key]['AccessE'] == 1:

                    accessdestination = [self.productplacex + 1, self.productplacey]
                    return accessdestination

                elif self.result_key[key]['AccessW'] == 1:

                    accessdestination = [self.productplacex - 1, self.productplacey]
                    return accessdestination






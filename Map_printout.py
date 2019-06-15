import sys
import os
import math
#from WarehouseMap import Map
import json
import time
from collections import defaultdict
import collections
import itertools #import combinations, permutations
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

class Map_print():


    def __init__(self):
        self.rowmax = 0
        self.colmax = 0
        self.map = list()
        self.startlocation_input = list()
        self.result_key = dict()
        self.totalpath = 0
        self.itemslist = list()
        self.currentPos_list = []
        self.startlocation_ID = '0'
        self.item_to_item_distance = dict() # new thing

    def load_data(self,testcase, startlocation, colmax, rowmax, Init_Map, Items_information, item_to_item_Distance):
        self.itemslist = sorted(testcase + [self.startlocation_ID])
        self.startlocation_input = startlocation
        self.map = Init_Map
        self.result_key = Items_information
        self.rowmax = rowmax
        self.colmax = colmax
        self.item_to_item_distance = item_to_item_Distance.copy() # new
        for i in self.result_key.items():
            if [i[1]['xLocation'], i[1]['yLocation']] not in self.currentPos_list:
                self.currentPos_list.append([i[1]['xLocation'], i[1]['yLocation']])
        self.analysisinput()

    def finditemsinformation(self, product_ID):
        keys = self.result_key.keys()
        if product_ID not in keys:
            print("Database does not have this item. Input Over")
        for key,value in self.result_key.items():
            if key == product_ID:
                print("Product: ", product_ID, "Location is: [", self.result_key[product_ID]['xLocation'],',', self.result_key[product_ID]['yLocation'],']')

    def analysisinput(self):
        self.pathlist = []
        items_distance = defaultdict()
        self.storpath = []
        count = 0
        printmap = 0
        #self.totalpathlist = []
        self.itemwepreviouswant = 0

        item_to_item_list = list(itertools.combinations(self.itemslist, 2))
        # print("item to item list:", item_to_item_list)

        for i in item_to_item_list:
            items_distance = self.inserttobackend(i, items_distance)
        # print("item to item distance", items_distance)
        #print(self.pathlist)

        pathlist = self.putresultpath()
        map2 = self.addinfotomap2(pathlist)
        # self.printworldtemp_frontend2(self.mapstore)
        self.printworldtemp_frontend2(map2)
        #self.mapstore = []





    def inserttobackend(self, start_to_productID, items_distance):


        #startlocation ID
        self.startlocation_ID = start_to_productID[0]
        startlocation = self.find_item_information(self.startlocation_ID)


        #EndLocation ID
        itemwewant = start_to_productID[1]

        # associate with ID number x,y location and its direction
        # Positions contain shelf

        # find the entry location
        #self.accessdestination = self.directionclear(productID)

        destination_entry = self.changemapinfo(itemwewant, startlocation)

        self.accessdestination = destination_entry[1]
        # find the item location
        self.itemwewantlocation = destination_entry[0]#[self.productplacex,self.productplacey]


        #find path to item
        self.path = self.findpathtoitem1(startlocation, self.itemwewantlocation)
        # print("path is :",self.path)

        if self.path[0] != 'The path is not eixt':
            #self.totalpath += int(self.path[0])
            #print(self.totalpath)
            self.pathlist.append(self.path[1])
        #print(self.pathlist)# change it to a key associate path list which
        #return self.itemwewantlocation
        #print('\n')
        #    # self.printworldtemp_frontend(startlocation,productID)
        # if counts == 0:
        #     self.storpath.append([startlocation, [self.itemwewant, self.path]])
        # else:
        #     self.storpath.append([self.itemwepreviouswant, [self.itemwewant, self.path]])

        self.map[self.accessdestination[1]][self.accessdestination[0]] = 1

        #store to distance_dict
        items_distance[start_to_productID] = self.path[0]

        return items_distance

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

        shortestpath = self.findpathtoitem1_solve(startlocationrow, startlocationcol)
       # print(self.shortestpath, "I am here")

        if shortestpath != 'The path is not eixt':
            self.totalpath += shortestpath
            return [shortestpath, self.path]
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
                self.backtrack(r, c,startlocationrow,startlocationcol)  # find the path
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


    def inputproductIDcheck(self, productlist):
        templist = list()
        for key, value in self.result_key.items():
            templist.append(key)
        for i in productlist:
            if i not in templist:
                return False
        return True

    def addinfotomap(self):
        map = list()
        for i in range(self.colmax):
            templist = list()
            for h in range(self.rowmax):
                if [h, i] in self.currentPos_list:
                    templist.append(0)
                else:
                    templist.append(1)
            map.append(templist)
        #print("look here", self.map[15][19])
        return map

    def changemapinfo(self, destination, startlocation):
        self.map[startlocation[1]][startlocation[0]] = 2
        for key,value in self.result_key.items():#fix next
            if key == destination:
                self.productplacex = self.result_key[key]['xLocation']
                self.productplacey = self.result_key[key]['yLocation']
                destination = [self.productplacex,self.productplacey]
                self.map[self.productplacey][self.productplacex] = 4
                if self.result_key[key]['AccessS'] == 1:
                    self.map[self.productplacey-1][self.productplacex] = 3
                    accessdestination = [self.productplacex,self.productplacey-1]
                    return [destination, accessdestination]

                elif self.result_key[key]['AccessN'] == 1:
                    self.map[self.productplacey + 1][self.productplacex] = 3
                    accessdestination = [self.productplacex, self.productplacey +1]
                    return [destination, accessdestination]

                elif self.result_key[key]['AccessE'] == 1:
                    self.map[self.productplacey][self.productplacex+1] = 3
                    accessdestination = [self.productplacex+1, self.productplacey]
                    return [destination, accessdestination]
                elif self.result_key[key]['AccessW'] == 1:
                    self.map[self.productplacey][self.productplacex -1] = 3
                    accessdestination = [self.productplacex-1, self.productplacey]
                    return [destination, accessdestination]


    def find_item_information(self, product_ID):
        if product_ID == '0':
           # print("input location", self.startlocation_input)
            return self.startlocation_input
        for key,value in self.result_key.items():#fix next
            if key == product_ID:
                productplacex = self.result_key[key]['xLocation']
                productplacey = self.result_key[key]['yLocation']
                if self.result_key[key]['AccessS'] == 1:
                    accessdestination = [productplacex,productplacey-1]
                    return accessdestination

                elif self.result_key[key]['AccessN'] == 1:
                    accessdestination = [productplacex, productplacey +1]
                    return accessdestination

                elif self.result_key[key]['AccessE'] == 1:
                    accessdestination = [productplacex+1, productplacey]
                    return accessdestination
                elif self.result_key[key]['AccessW'] == 1:
                    accessdestination = [productplacex-1, productplacey]
                    return accessdestination
        return "The Product ID you looking is not exit"


    def printworldtemp_frontend(self):

        self.avaliablepath = list()
        # self.print()
        count_number = 0
        for y in self.map:
            templist = list()
            for x in y:

                if x == 1:
                    print("  .  ", end = '')
                elif x == 0:
                    print("  S  ", end = '')
                    # or print pick up
                    # break
                elif x == 2:
                    print("  B  ", end = '')
                elif x == 3:
                    print("  E  ", end = '')
                elif x == 4:
                    print("  D  ", end = '')
            print(self.colmax - 1 - count_number)
            count_number += 1
            print("\n")

        for i in range(self.rowmax):
            if i < 10:
                print(" ", i, " ", end = '')
            elif i == 10:
                print(" ", i, " ", end = '')
            else:
                print("", i, " ", end = '')
        time.sleep(1)
        print("\n")
        print("=============================================================================\n")
        # self.print()


    def addinfotomap2(self,resultlist):
        #print("final path list:", resultlist)
        #if(self.result_key != None):
        # print("Before printing the key")
        # print("Size of reultkey", len(self.result_key))
        # print("Single resultkey", self.result_key.get(0))
        # print("Element of resultkey", self.result_key[0] )
        # print("itemlist", self.itemslist[0])
        # print("ITEM TO ITEM DISTANCE ", self.item_to_item_distance)
        # print("ITEM DISTANCEC IS :", self.item_to_item_distance.get((self.itemslist[0],self.itemslist[1])))

        print("\nPath Directions To: ")
        for i in range(len(self.itemslist)):
            if(i != 0):
                print("item ", self.itemslist[i])

        print("\nStart.")
        # states of the path direction
        starting = -1
        arrivedAtItem = 0
        goRight = 1
        goLeft = 2
        goUp = 3
        goDown = 4

        curr_x, curr_y = resultlist[0]
        direction_steps_count = 0
        curr_direction = starting

        item_index = 0
        item_curr, item_next = self.itemslist[item_index], self.itemslist[item_index+1]
        distanceToNextItem = self.item_to_item_distance.get((self.itemslist[item_index],self.itemslist[item_index+1]))
        item_steps_count = 0
        total_num_items = len(self.itemslist) - 1
        lastItemReached = False
        #print("Current Item: ", item_curr, "Next Item ", item_next, "Distance to Travel ", distanceToNextItem, "Total items ", total_num_items)
        # print("Go to item ", item_next)
        # print("Distance", distanceToNextItem)
        for i in range(1,len(resultlist)):
            x_next, y_next = resultlist[i]

            #print(x_next, y_next)
            change_x = x_next - curr_x
            change_y = y_next - curr_y

            # go right
            if(change_x == 1 and change_y == 0):
                next_direction = goRight
            # go left
            elif(change_x == -1 and change_y == 0):
                next_direction = goLeft
            # go up
            elif(change_x == 0 and change_y == 1):
                next_direction = goUp
            # go down
            elif(change_x == 0 and change_y == -1):
                next_direction = goDown

            # check to see if item is reached
            if(item_steps_count == distanceToNextItem and item_steps_count != 0):
                print("Pick up item ", item_next)

                # update next_direction
                next_direction = arrivedAtItem


                # restart the steps for direction
                direction_steps_count = 0
                item_steps_count = 0

                # update information to get to next item
                item_index = item_index + 1
                if item_index == total_num_items:
                    lastItemReached = True

                if(lastItemReached == True):
                    print("Navigation finished.")
                    break
                else:
                    item_curr = self.itemslist[item_index]
                    item_next = self.itemslist[item_index + 1]
                    distanceToNextItem = self.item_to_item_distance.get((self.itemslist[item_index], self.itemslist[item_index + 1]))
                    # print("Go to item ", item_next)
                    # print("Distance", distanceToNextItem)


            # check to see if you changed direction
            if (curr_direction != next_direction and curr_direction != starting and curr_direction != arrivedAtItem):
                if(curr_direction == goRight):
                    print("\tTake ", direction_steps_count, "\tstep(s) to the east.")
                elif(curr_direction == goLeft):
                    print("\tTake ", direction_steps_count, "\tstep(s) to the west.")
                elif(curr_direction == goUp):
                    print("\tTake ", direction_steps_count, "\tstep(s) to the north.")
                elif(curr_direction == goDown):
                    print("\tTake ", direction_steps_count, "\tstep(s) to the south.")
                # reset the number of direction_steps_count
                direction_steps_count = 0

            # update direction
            direction_steps_count = direction_steps_count + 1
            curr_x, curr_y = x_next, y_next
            curr_direction = next_direction

            # update the steps to next item
            item_steps_count = item_steps_count + 1

        map2 = []
        #print(resultlist)
        #print([1,2] in resultlist)
        for i in range(self.colmax):
            # print(i,"number i ")
            templist = list()
            for h in range(self.rowmax):
                # print("number h",h)
                if [h, i] == self.startlocation_input:
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

    def printworldtemp_frontend2(self, map2):
        count_number = 0
        map2.reverse()
        for y in map2:
            templist = list()
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



    def putresultpath(self):
        resultlist = []
        for i in self.pathlist:
            for g in i:
                #print(g)
                resultlist.append(g)
        return resultlist
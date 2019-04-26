import sys
import os
import math
#from WarehouseMap import Map
import json
import time
from collections import defaultdict

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
        header = dataFile.readline().strip().split('\t')
        print("Headers of Data = ", header)
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
                    self.result_val[key] = value
            temp_dict = self.result_val.copy()
            self.result_key[temp] = temp_dict
            self.result_val.clear()
            count += 1
            #print(self.result_key)
            if count == 100:
                break
        dataFile.close()
        #return self.result_key

    def finditemsinformation(self, product_ID):
        keys = self.result_key.keys()
        #print(keys)
        #print(self.result_key[product_ID])
        if product_ID not in keys:
            print("Database does not have this item. Input Over")
        for key,value in self.result_key.items():
            if key == product_ID:
                print("Product: ", product_ID, "Location is: [", self.result_key[product_ID]['xLocation'],',', self.result_key[product_ID]['yLocation'],']')


    def printworldtemp(self, startlocation):
        rowmax = 0
        colmax = 0
        shelflist = dict()
        self.avaliablepath = list()
        for key,value in self.result_key.items():
            shelflist.append([int(float(self.result_key[key]['xLocation'])), int(self.result_key[key]['yLocation'])])
            tempy = int(self.result_key[key]['yLocation'])
            tempx = int(float(self.result_key[key]['xLocation']))
            if tempx > int(rowmax):
                rowmax = int(float(self.result_key[key]['xLocation']))
            if  tempy > int(colmax):
                colmax = int(self.result_key[key]['yLocation'])
        print("warehouse row siz is: ", rowmax, "warehouse column size is: ", colmax)
        for i in range(colmax):
            for h in range(rowmax):
                if [h,i] == startlocation:
                    self.avaliablepath.append([h,i])
                    print("  B  ", end = '')
                if [h,i] in shelflist:
                    print("  S  ", end = '')
                else:
                    self.avaliablepath.append([h,i])
                    print("  .  ", end = '')
            print('\n')
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


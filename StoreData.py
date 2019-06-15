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


class StoreData:


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
        #self.printworldtemp_frontend()
        self.map.reverse()

        print("Warehouse Dimensions: ", self.rowmax, " X ", self.colmax)
        return [self.map, self.rowmax,self.colmax, self.result_key]

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

    def printworldtemp_frontend(self):
        print("=============================================================================\n")
        print("WAREHOUSE MAP WITH PATHS\n")
        print("Legend:\n\tS = shelf\n\tB = your starting location\n\tO = path in warehouse\n")
        print("   North\nWest\tEast\n   South\n")

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

    def findrowcolmax(self):
        for key, value in self.result_key.items():
            self.itemdict[key] = [self.result_key[key]['xLocation'], self.result_key[key]['yLocation']]
            # print(self.itemdict)
            tempy = self.result_key[key]['yLocation']
            tempx = self.result_key[key]['xLocation']
            if tempx > int(self.rowmax):
                self.rowmax = self.result_key[key]['xLocation']
            if tempy > int(self.colmax):
                self.colmax = self.result_key[key]['yLocation']
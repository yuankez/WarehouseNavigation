import sys
import os
import math
#from WarehouseMap import Map
import json
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
            print(self.result_key)
            if count == 5:
                break
        dataFile.close()
        #return self.result_key

    def finditemsinformation(self, product_ID):
        keys = self.result_key.keys()
        print(keys)
        #print(self.result_key[product_ID])
        if product_ID not in keys:
            print("Database does not have this item. Input Over")
        for key,value in self.result_key.items():
            if key == product_ID:
                print("Product: ", product_ID, "Location is: [", self.result_key[product_ID]['xLocation'],',', self.result_key[product_ID]['yLocation'],']')


    def printworldtemp(self):
        rowmax = 0
        colmax = 0
        for key,value in self.result_key.items():
            tempx = self.result_key[key]['xLocation']
            tempy = self.result_key[key]['yLocation']
            print(tempx, tempy)
            if int(tempx) > int(rowmax):
                rowmax = self.result_key[key]['xLocation']
            if  int(tempy) > int(colmax):
                colmax = self.result_key[key]['yLocation']
        for i in range(colmax):
            for h in range(rowmax):
                print(" . ")
            print('\n')

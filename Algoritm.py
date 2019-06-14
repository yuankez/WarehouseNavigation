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

        print("The shortes path is:", storepath)
        print("The steps count:", Final_path_cout)

        return [shortest_path_count, storepath]


    def Nearest_Neighbour(self, distance_dict, testcase):
        #nearest_neighbour
        nearest = []
        temp = ()
        temp_start = ()

        # dict
        pathdict = distance_dict

        #steps count for shortest path
        smallest = 999999
        shortest_path_count = 0
        Final_path_cout = 0

        #start_ID
        starting_point = '0'

        #every possible combination for testcase
        primelist = list(permutations(testcase, len(testcase)))
        items_to_item = pathdict.keys()

        print(items_to_item)

        # for item in items_to_item:
        #     if item[0] == starting_point and smallest > int(pathdict.get(item)):
        #         print("starting point for now is", starting_point, "item", item)
        #
        #         smallest = int(pathdict.get(item))
        #         temp = item
        #     elif item[0] != starting_point:
        #         nearest = nearest + [temp, smallest]
        #         print("item", item)
        #         starting_point = item[0]
        #         print( "now starting", starting_point, "item", item)
        #         smallest = int(pathdict.get(item))
        count = 0
        for item in items_to_item:
            print(item)
            if item[0] == starting_point:
                temp = temp + (item,)
                print("temp", temp)
            else:
                temp_start = temp_start + (temp,)
                temp = ()
                starting_point = item[0]
                temp = temp + (item,)
                if count == len(items_to_item)-1:
                    temp_start = temp_start + (temp,)
            count += 1
        print("check list", temp_start)

        for item in temp_start:
            for distance in item:
                print(list(distance))
                #if pathdict.get(distance)

        #print(nearest)

        #
        # for item_key in items_to_item:
        #     if item_key[0] == starting_point:
        #         for item_next_key in items_to_item:
        #             if items_next_key[1]
        #











from collections import defaultdict
from DataManagement import Data
from Algoritm import Algorithm
from Map_printout import Map_print
import StoreData
import time
#import psutil
import os

def runtestcase(testcase, startlocation, data, colmax, rowmax, Init_Map, Items_information, item_to_item_distance, printmap, elapsedTime):

    count = 0
    start = 0

    stopwatch_start = time.process_time()

    #load data to the system
    data.load_data(testcase, startlocation,colmax,rowmax,Init_Map,Items_information)

    #anaylsis input_bfs
    item_to_item_distance = data.analysisinput()

    #Brute_force_algorithm
    #result = Algorithm.Brut_Force(Algorithm,item_to_item_distance, testcase)

    #minmize_optimaztion
    result = Algorithm.Brut_Force(Algorithm,item_to_item_distance, testcase)
    final_step_couht = result[0]
    Optimize_order = list(result[1])

    #print_the_best_rout

    printmap.load_data(Optimize_order, startlocation, colmax,rowmax,Init_Map,Items_information)








    #print(data.analysisinput(testcase, startlocation))
    stopwatch_end = time.process_time()
    runningTime = stopwatch_end - stopwatch_start
    elapsedTime.append(runningTime)
    print("Elapsed Time of BFS :", runningTime, " seconds")

def printTestCaseTime(elapsedTime, startlocation):
    print('Running Time of BFS')
    print('Starting Location: ', startlocation)
    for i in range(len(elapsedTime)):
        #print("Testcase", i + 1,"\t", elapsedTime[i], " seconds")
        print(elapsedTime[i])

def printMemoryUsage():
    # Prints Memory Usage: using psutil
    # In print statement look at used=
    # Only run one testcase at a time
    # print(psutil.virtual_memory())
    print('PID For User Control:', os.getpid())
    #process = psutil.Process(os.getpid())   # get mem
    #print(process.memory_info().rss)



def takealistoforder(inputlistoforder):
    filename = "" + inputlistoforder
    dataFile = open(filename, 'r')
    count = 1
    listdict = dict()
    for line in dataFile:
        temp = line.split()
        listdict[count] = temp
        count+=1
    #print(listdict[1])
    return listdict
    pass


def main():
    # Accept file path
    data = Data ()
    storedata = StoreData.StoreData()
    printmap = Map_print()
    item_to_item_distance = defaultdict()
    #datafile = input("please give a valid data file to input!\n")
    #/Users/Yuank/Desktop/WarehouseNavigation/qvBox-warehouse-data-s19-v01.txt
    rowcolmax = []
    #rowcolmax\
    DataStore_result = storedata.inputdata("qvBox-warehouse-data-s19-v01.txt")
    Init_Map = DataStore_result[0]
    Map_row_max = DataStore_result[1]
    Map_col_max = DataStore_result[2]
    Items_information = DataStore_result[3]

    #itemcheck = input("Input the product id you want to check\n")

    #inputlistoforder = input("please input the order list path you want: EX: qvBox-warehouse-orders-list-part01.txt")
    #inputlistoforder = "qvBox-warehouse-orders-list-part01.txt"

    #because of the huge database, for now only print one item
    #data.finditemsinformation('1')
    print("The Input of row and col length is", Map_row_max,",",  Map_col_max)
    #
    startlocationrow = 0 #input("Please the start location row number: " )
    startlocationcal = 0 #input("Please the start location col number: " )
    startlocation = [int(startlocationrow),int(startlocationcal)]


    #print("Init_map", Init_Map)
    print("row max", Map_row_max)
    print("col max", Map_col_max)
    #print(Items_information)

    #productpick = '149'
    #productpick = input("Input the product id you want to pick EX: 149\n")
    # or input by user
    #testcaseold = ['1','108335', '340367']
    testcase1 = ['1','623','1520']
    testcase2 = ['391825'] #upgoing
    testcase3 = ['108335',	'391825',	'340367',	'286457',	'661741']#desecending order  1045 670
    testcase4 = ['1520','1387', '1958','2010','1355','1045','2029', '2826', '2947','1025', '670','626', '302', '219', '102']#random order

    testcase5 = ['74','45','102','149', '1045','670','2029', '2826', '1']# xlocation bump back and force
    testcase6 = ['1','74','102','102','149']# try to pick up same item twice
    testcase7 = ['1','74','102','103','149']#one of item not exit '103'
    testcase8 = ['16643','123462'	,'119063',	'128827',	'188598',	'323836',	'660999', '336712','1734057','82591', '343071']
    testcase9 = ['16643','123462'	,'119063',	'128827',	'188598',	'323836',	'660999', '336712','1734057','82591','259577',
                 '1075851','365562',	'259577'	,'343071',	'1080194']

    count = 0
    #data.inserttobackend([0,0], '149',count)
    elapsedTime = []

    # singel test case
    runtestcase(testcase3, startlocation, data, Map_col_max, Map_row_max, Init_Map, Items_information, item_to_item_distance, printmap,elapsedTime)

    printTestCaseTime(elapsedTime, startlocation)
    printMemoryUsage()

    #      List of Order
    #takeorderaslist(startlocation, data, elapsedTime)

    #inputlistoforder = input("please input the order list path you want: EX: qvBox-warehouse-orders-list-part01.txt")
    # inputlistoforder = "qvBox-warehouse-orders-list-part01.txt"
    #
    # orderlist = takealistoforder(inputlistoforder)
    #
    # orderlistnumber = int(input("pleast input which order list number you want to choose: EX: 1 "))
    # testcase = orderlist[int(orderlistnumber)]
    # del orderlist[int(orderlistnumber)]
    # runtestcase(testcase, startlocation, data, elapsedTime)
    #
    #
    #
    #
    #
    # templist2 = orderlist.keys()
    # templist = []
    # for i in templist2:
    #     templist.append(i)
    # for i in range(len(orderlist)):
    #     temp = input("Please input next order list to pick the next one: EX, Next or 2")
    #     if temp == 'next':
    #         orderlistnumber = orderlistnumber + 1
    #         while (1):
    #             if orderlistnumber in templist:
    #                 break
    #             elif orderlistnumber >= len(templist):
    #                 break
    #             else:
    #                 orderlistnumber = orderlistnumber + 1
    #         runtestcase(orderlist[orderlistnumber], startlocation, data, elapsedTime)
    #         del orderlist[int(orderlistnumber)]
    #         templist.remove(orderlistnumber)
    #     elif temp == 'exit':
    #         print("Pick up has been stoped")
    #         break
    #     else:
    #         orderlistnumber = temp
    #         runtestcase(orderlist[int(orderlistnumber)], startlocation, data, elapsedTime)
    #         del orderlist[int(orderlistnumber)]
    #         templist.remove(orderlistnumber)
    # printTestCaseTime(elapsedTime, startlocation)
    # printMemoryUsage()

main()

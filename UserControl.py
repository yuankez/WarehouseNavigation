from collections import defaultdict
from DataManagement import Data
from Algoritm import Algorithm
from Map_printout import Map_print
import StoreData
import time
# import psutil
import os

def runtestcase(testcase, startlocation, endlocation, data, colmax, rowmax, Init_Map, Items_information, item_to_item_distance, printmap, elapsedTime):

    count = 0
    start = 0
    Optimize_order = list()

    stopwatch_start = time.process_time()

    #load data to the system
    #print(type(data))
    data.load_data(testcase, startlocation, colmax,rowmax,Init_Map,Items_information, item_to_item_distance)

    #anaylsis input_bfs
    item_to_item_distance = data.analysisinput()

    print("\nSelect the corresponding number of the algorithm you'd like to run.")
    print("\t1. Modified Brute Force")
    print("\t2. Greedy Algorithm")
    choice = int(input("Enter the number: "))
    if choice == 1 or choice == 2:
        choiceValid = True
    else:
        choiceValid = False

    while(choiceValid == False):
        choice = int(input(("\tINVALID INPUT. Please enter 1 or 2: ")))
        if choice == 1 or choice == 2:
            choiceValid = True
        else:
            choiceValid = False
    #Brute_force_algorithm
    if choice == 1:
        while(1):
            Threadind_or_not = input(
                "Please choose to use the MultiThread Or Not\n 1 for Brute Force \n 2 for Mutithread Brute Force")
            if Threadind_or_not == '1':
                result = Algorithm.Brut_Force2(Algorithm, item_to_item_distance, testcase)
                # BRUTE FORCE
                Optimize_order = list(result[1])
                break
            elif Threadind_or_not == '2':
                result = Algorithm.Brut_Force(Algorithm, item_to_item_distance, testcase)
                # BRUTE FORCE
                Optimize_order = list(result[1])
                break
        result = Algorithm.Brut_Force(Algorithm,item_to_item_distance, testcase)
        #BRUTE FORCE
        Optimize_order = list(result[1])
    elif choice == 2:

        result = Algorithm.Nearest_Neighbour(Algorithm,item_to_item_distance, testcase, startlocation, Init_Map, colmax, rowmax, Items_information)
        Optimize_order = result[0]


    #print_the_best_rout

    printmap.load_data(Optimize_order, startlocation, endlocation, colmax,rowmax,Init_Map,Items_information,item_to_item_distance)

    print("The total step is:", result[1])

    print("The worker exit at", endlocation)








    #print(data.analysisinput(testcase, startlocation))
    stopwatch_end = time.process_time()
    runningTime = stopwatch_end - stopwatch_start
    elapsedTime.append(runningTime)
    print("Elapsed Time For Search :", runningTime, " seconds")

def printTestCaseTime(elapsedTime, startlocation):
    print('Running Time of Search')
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
    #print("Memory Usage", process.memory_info().rss, " Bytes")



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

# def takeorderaslist(path,startlocation,data):
#     inputlistoforder = input("please input the order list path you want: EX: qvBox-warehouse-orders-list-part01.txt")
#     inputlistoforder = "qvBox-warehouse-orders-list-part01.txt"
#     orderlist = takealistoforder(inputlistoforder)
#     orderlistnumber = int(input("pleast input which order list number you want to choose: EX: 1 "))
#     testcase = orderlist[int(orderlistnumber)]
#     del orderlist[int(orderlistnumber)]
#     orderlist = takealistoforder(path)
#     templist = []
#     templist2 = orderlist.keys()
#     templist = []
#     for i in templist2:
#         templist.append(i)
#     for i in range(len(orderlist)):
#         temp = input("Please input next order list to pick the next one: EX, Next or 2")
#         if temp == 'next':
#             orderlistnumber = orderlistnumber + 1
#             while (1):
#                 if orderlistnumber in templist:
#                     break
#                 elif orderlistnumber >= len(templist):
#                     break
#                 else:
#                     orderlistnumber = orderlistnumber + 1
#             runtestcase(orderlist[orderlistnumber], startlocation, data, elapsedTime)
#             del orderlist[int(orderlistnumber)]
#             templist.remove(orderlistnumber)
#         elif temp == 'exit':
#             print("Pick up has been stoped")
#             break
#         else:
#             orderlistnumber = temp
#             runtestcase(orderlist[int(orderlistnumber)], startlocation, data, elapsedTime)
#             del orderlist[int(orderlistnumber)]
#             templist.remove(orderlistnumber)

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
    testcaseold = ['1','108335', '340367']
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
    #itemcheck = input("Input the product id you want to check\n")

    #inputlistoforder = input("please input the order list path you want: EX: qvBox-warehouse-orders-list-part01.txt")
    #inputlistoforder = "qvBox-warehouse-orders-list-part01.txt"

    #because of the huge database, for now only print one item
    #data.finditemsinformation('1')

    elapsedTime = []

    count = 0
    #Option Menu
    Option = -1
    productpick = ''
    input_testcase = []
    print("Welcome to the Warehouse Navigator\n")
    while(Option != 3):
        print("============================\n\n")
        print("Option Menu:\nSelect the corresponding number of navgation mode you'd like to run.")
        print("\t1. Use Sample Testcase")
        print("\t2. Use Order list")
        print("\t3. Exit the program")
        Option = int(input("Enter the number: "))
        print("\n")

        if Option == 1:
            print("1. Sample Test Case Selected")
            # input_start_location
            startlocationrow = int(input("Please the start location row number: "))
            while (startlocationrow < 0 or startlocationrow > Map_row_max):
                startlocationrow = int(input(("\tINVALID INPUT. Please try again: ")))
            startlocationcal = int(input("Please the start location col number: "))
            while (startlocationcal < 0 or startlocationcal > Map_col_max):
                startlocationcal = int(input(("\tINVALID INPUT. Please try again: ")))
            startlocation = [int(startlocationrow), int(startlocationcal)]

            # input end location
            endlocationrow = int(input("Please the end location row number: "))
            while (endlocationrow < 0 or endlocationrow > Map_row_max):
                endlocationrow = int(input(("\tINVALID INPUT. Please try again: ")))
            endlocationcal = int(input("Please the start location col number: "))
            while (endlocationcal < 0 or endlocationcal > Map_col_max):
                endlocationcal = int(input(("\tINVALID INPUT. Please try again: ")))
            endlocation = [int(endlocationrow), int(endlocationcal)]

            if count == 0:
                print("Used testcase:", testcase3)
                runtestcase(testcase3, startlocation, endlocation, data, Map_col_max, Map_row_max, Init_Map,
                            Items_information, item_to_item_distance, printmap, elapsedTime)

                printTestCaseTime(elapsedTime, startlocation)
                printMemoryUsage()
                count = 1
            if count == 1:
                print("Used testcase:", testcase5)
                runtestcase(testcase5, startlocation, endlocation, data, Map_col_max, Map_row_max, Init_Map,
                            Items_information, item_to_item_distance, printmap, elapsedTime)

                printTestCaseTime(elapsedTime, startlocation)
                printMemoryUsage()
                count == 0


        elif Option == 2:
            # input_start_location
            print("2. Order List Selected")
            startlocationrow = int(input("Please the start location row number: "))
            while (startlocationrow < 0 or startlocationrow > Map_row_max):
                startlocationrow = int(input(("\tINVALID INPUT. Please try again: ")))
            startlocationcal = int(input("Please the start location col number: "))
            while (startlocationcal < 0 or startlocationcal > Map_col_max):
                startlocationcal = int(input(("\tINVALID INPUT. Please try again: ")))
            startlocation = [int(startlocationrow), int(startlocationcal)]

            # input end location
            endlocationrow = int(input("Please the end location row number: "))
            while (endlocationrow < 0 or endlocationrow > Map_row_max):
                endlocationrow = int(input(("\tINVALID INPUT. Please try again: ")))
            endlocationcal = int(input("Please the start location col number: "))
            while (endlocationcal < 0 or endlocationcal > Map_col_max):
                endlocationcal = int(input(("\tINVALID INPUT. Please try again: ")))
            endlocation = [int(endlocationrow), int(endlocationcal)]
            #      List of Order
            # takeorderaslist(startlocation, data, elapsedTime)

            inputlistoforder = input("Please input the order list path you want: qvBox-warehouse-orders-list-part01.txt")
            inputlistoforder = "qvBox-warehouse-orders-list-part01.txt"

            orderlist = takealistoforder(inputlistoforder)

            print("Order list number input is valid from 0 to 100.")
            orderlistnumber = int(input("Please input which order list number you want to choose: "))
            while(orderlistnumber < 0 or orderlistnumber > 100):
                orderlistnumber = int(input(("\tINVALID INPUT. Please try again: )")))

            testcase = orderlist[int(orderlistnumber)]
            del orderlist[int(orderlistnumber)]
            runtestcase(testcase, startlocation,endlocation, data, Map_col_max, Map_row_max, Init_Map,
                        Items_information, item_to_item_distance, printmap, elapsedTime)

            # templist2 = orderlist.keys()
            # templist = []
            # for i in templist2:
            #     templist.append(i)
            # for i in range(len(orderlist)):
            #     temp = input("Please input next order list to pick the next one: EX, Next or 2")
            #     if temp == 'next' or temp == "Next":
            #         orderlistnumber = orderlistnumber + 1
            #         while (1):
            #             if orderlistnumber in templist:
            #                 break
            #             elif orderlistnumber >= len(templist):
            #                 break
            #             else:
            #                 orderlistnumber = orderlistnumber + 1
            #         runtestcase(orderlist[orderlistnumber], startlocation, endlocation, data, Map_col_max, Map_row_max, Init_Map,
            #             Items_information, item_to_item_distance, printmap, elapsedTime)
            #         del orderlist[int(orderlistnumber)]
            #         templist.remove(orderlistnumber)
            #     elif temp == 'exit':
            #         print("Pick up has been stoped")
            #         break
            #     else:
            #         orderlistnumber = temp
            #         runtestcase(orderlist[int(orderlistnumber)], startlocation, endlocation, data, Map_col_max, Map_row_max, Init_Map,
            #             Items_information, item_to_item_distance, printmap, elapsedTime)
            #         del orderlist[int(orderlistnumber)]
            #         templist.remove(orderlistnumber)
            # printTestCaseTime(elapsedTime, startlocation)
            # printMemoryUsage()
        elif Option == 3:
            print("3. Exiting Program Selected")
        else:
            print("INVALID INPUT. Please enter a value of 1, 2 or 3.")




    #productpick = '149'
    #productpick = input("Input the product id you want to pick EX: 149\n")
    # or input by user


    count = 0
    #data.inserttobackend([0,0], '149',count)
    # elapsedTime = []
    #
    #
    # inputlistoforder = input("please input the order list path you want: qvBox-warehouse-orders-list-part01.txt")
    # inputlistoforder = "qvBox-warehouse-orders-list-part01.txt"
    # order = takealistoforder(inputlistoforder)
    # # print("ORDER ", order)
    # orderlistnumber = int(input("Please input which order you'd like to find (0 to 100): EX: 1 "))
    # testcase = order[int(orderlistnumber)]
    #
    # # single test case
    # runtestcase(testcase3, startlocation,endlocation, data, Map_col_max, Map_row_max, Init_Map, Items_information, item_to_item_distance, printmap,elapsedTime)
    #
    # printTestCaseTime(elapsedTime, startlocation)
    # printMemoryUsage()



main()

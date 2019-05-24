from collections import defaultdict
import DataManagement
import time
import psutil
import os

def runtestcase(testcase, startlocation, data, elapsedTime):
    count = 0
    start = 0
    stopwatch_start = time.process_time()
    # for i in testcase:
    #     if start  > len(testcase) - 1:
    #         break
    #     if start == 0:
    #         newstartlocation = data.inserttobackend(startlocation, testcase[start], count)
    #         print(newstartlocation)
    #     elif start > 0:
    #         print("here")
    #         newstartlocation = data.inserttobackend(newstartlocation, testcase[start],count)
    #     count += 1
    #     start += 1
    print(data.analysisinput(testcase, startlocation))
    stopwatch_end = time.process_time()
    runningTime = stopwatch_end - stopwatch_start
    #elapsedTime.append(runningTime)
    #print("Elapsed Time of BFS :", runningTime, " seconds")

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
    process = psutil.Process(os.getpid())   # get mem
    print(process.memory_info().rss)


def takealistoforder(inputlistoforder):
    filename = "" + inputlistoforder
    dataFile = open(filename, 'r')
    count = 1
    listdict = dict()
    for line in dataFile:
        temp = line.split()
        listdict[count] = temp
        count+=1
    print(listdict[1])
    return listdict
    pass
def main():
    # Accept file path
    data = DataManagement.Data()
    #datafile = input("please give a valid data file to input!\n")
    #/Users/Yuank/Desktop/WarehouseNavigation/qvBox-warehouse-data-s19-v01.txt
    rowcolmax = []
    rowcolmax = data.inputdata("qvBox-warehouse-data-s19-v01.txt")
    #itemcheck = input("Input the product id you want to check\n")
    inputlistoforder = input("please input the order list path you want: EX: qvBox-warehouse-orders-list-part01.txt")
    inputlistoforder = "qvBox-warehouse-orders-list-part01.txt"

    orderlist = takealistoforder(inputlistoforder)
    #because of the huge database, for now only print one item
    #data.finditemsinformation('1')
    print("The Input of row and col length is", rowcolmax[0]-1, rowcolmax[1]-1)
    startlocationrow = input("Please the start location row number: " )
    startlocationcal = input("Please the start location col number: " )
    startlocation = [int(startlocationrow),int(startlocationcal)]

    orderlistnumber = int(input("pleast input which order list number you want to choose: EX: 1 "))
    testcase = orderlist[int(orderlistnumber)]
    del orderlist[int(orderlistnumber)]

    #productpick = '149'
    #productpick = input("Input the product id you want to pick EX: 149\n")
    # or input by user
    #testcaseold = ['1','108335', '340367']
    testcase1 = ['1']
    testcase2 = ['108335'] #upgoing
    testcase3 = ['1','1520','1387', '1355','1045', '670']#desecending order
    testcase4 = ['1520','1387', '1958','2010','1355','1045','2029', '2826', '2947','1025', '670','626', '302', '219', '102']#random order
    testcase5 = ['1','74','45','102','149','670']# xlocation bump back and force
    testcase6 = ['1','74','102','102','149']# try to pick up same item twice
    testcase7 = ['1','74','102','103','149']#one of item not exit '103'

    count = 0
    #data.inserttobackend([0,0], '149',count)
    elapsedTime = []

    #startlocation = input("where you want to start")

    runtestcase(testcase, startlocation, data, elapsedTime)

    # start = 0
    # for i in testcase4:
    #     if start  > len(testcase2) - 1:
    #         break
    #     if start == 0:
    #         newstartlocation = data.inserttobackend(startlocation, testcase2[start], count)
    #         print(newstartlocation)
    #     elif start > 0:
    #         #print("here")
    #         newstartlocation = data.inserttobackend(newstartlocation, testcase2[start],count)
    #     count += 1
    #     start += 1


    #print("S means shelf location, B means start begin location")
    #productpick = input("Input the product id you want to pick EX: 149\n")
    listproduct = ['0','45', '149']
    #data.findpathtoitem1('1')
    # for i in testcaseold:
    #     data.printworldtemp( startlocation, productpick)
        #data.findpathtoitem1(i)

    printTestCaseTime(elapsedTime, startlocation)
    printMemoryUsage()
    templist = []
    templist2= orderlist.keys()
    templist = []
    for i in templist2:
        templist.append(i)
    for i in range(len(orderlist)):
        temp = input("Please input next order list to pick the next one: EX, Next or 2")
        if temp == 'next':
            orderlistnumber = orderlistnumber+1
            while(1):
                if orderlistnumber in templist:
                    break
                elif orderlistnumber >= len(templist):
                    break
                else:
                    orderlistnumber = orderlistnumber + 1
            runtestcase(orderlist[orderlistnumber], startlocation, data, elapsedTime)
            del orderlist[int(orderlistnumber)]
            templist.remove(orderlistnumber)
        elif temp == 'exit':
            print("Pick up has been stoped")
            break
        else:
            orderlistnumber = temp
            runtestcase(orderlist[int(orderlistnumber)], startlocation, data, elapsedTime)
            del orderlist[int(orderlistnumber)]
            templist.remove(orderlistnumber)
main()
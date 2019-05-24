from collections import defaultdict
import DataManagement
import WarehouseMap

def main():
    # Accept file path
    data = DataManagement.Data()
    board = WarehouseMap.Map()
    #datafile = input("please give a valid data file to input!\n")
    #/Users/Yuank/Desktop/WarehouseNavigation/qvBox-warehouse-data-s19-v01.txt
    rowcolmax = []
    rowcolmax = data.inputdata("/Users/Yuank/Desktop/WarehouseNavigation/qvBox-warehouse-data-s19-v01.txt")
    #itemcheck = input("Input the product id you want to check\n")

    #because of the huge database, for now only print one item
    #data.finditemsinformation('1')
    print("The Input of row and col length is", rowcolmax[0]-1, rowcolmax[1]-1)
    startlocationrow = input("Please the start location row number, the row max input is: ")
    startlocationcal = input("Please the start location col number, the col max input is: ")
    startlocation = [int(startlocationrow),int(startlocationcal)]
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

    #startlocation = input("where you want to start")
    print(data.analysisinput(testcase2,startlocation))
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


main()
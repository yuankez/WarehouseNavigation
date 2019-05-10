from collections import defaultdict
import DataManagement
import WarehouseMap

def main():
    # Accept file path
    data = DataManagement.Data()
    board = WarehouseMap.Map()
    #datafile = input("please give a valid data file to input!\n")
    #/Users/Yuank/Desktop/WarehouseNavigation/qvBox-warehouse-data-s19-v01.txt
    data.inputdata("/Users/Yuank/Desktop/WarehouseNavigation/qvBox-warehouse-data-s19-v01.txt")
    #itemcheck = input("Input the product id you want to check\n")

    #because of the huge database, for now only print one item
    #print("because of the huge database, for now only print one item")
    data.finditemsinformation('1')

    startlocation = [0,0];
    productpick = '149'
    #productpick = input("Input the product id you want to pick EX: 149\n")
    # or input by user
    testcase1 = ['1']
    testcase2 = ['102', '219', '302','626', '670'] #upgoing
    testcase3 = ['1520','1387', '1355','1045', '1025', '670','626', '302', '219', '102']#desecending order
    testcase4 = ['1520','1387', '1958','2010','1355','1045','2029', '2826', '2947','1025', '670','626', '302', '219', '102']#random order
    testcase5 = ['1','74','45','102','149']# xlocation bump back and force
    testcase6 = ['1','74','102','102','149']# try to pick up same item twice
    testcase7 = ['1','74','102','103','149']#one of item not exit '103'

    #startlocation = input("where you want to start")
    data.printworldtemp(startlocation,productpick)
    #print("S means shelf location, B means start begin location")
    #productpick = input("Input the product id you want to pick EX: 149\n")
    listproduct = ['0','45', '149']
    for i in listproduct:
        data.printworldtemp(startlocation, productpick)
        #data.findpathtoitem1(i)


main()
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
    # or input by user
    #startlocation = input("where you want to start")
    data.printworldtemp(startlocation)
    #print("S means shelf location, B means start begin location")
    #productpick = input("Input the product id you want to pick EX: 149\n")
    #data.findpathtoitem('149')

main()
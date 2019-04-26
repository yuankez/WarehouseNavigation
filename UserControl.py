from collections import defaultdict
import DataManagement
import WarehouseMap

def main():
    # Accept file path
    data = DataManagement.Data()
    board = WarehouseMap.Map()
    #datafile = input("/Users/Yuank/Desktop/WarehouseNavigation/MyFile.txt")
    data.inputdata("/Users/Yuank/Desktop/WarehouseNavigation/MyFile.txt")
    #item_pick = input("Input the product id you want to pick\n")
    data.finditemsinformation('149')
    data.printworldtemp()

main()
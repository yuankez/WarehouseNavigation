class Map():
    # warehouse Structure
    class warehousebase:
        Product_placed = False;
        Place_empty = True;
        shelf_full = False;
        product_picked = False;
        Robot_actived = False;
        # Set check point here to observe the condition and operate
        # the system easily

    # ===============================================================
    # =                 Constructor
    # ===============================================================

    def __init__(self, file=None):
            #Assume our ware house map is 24*24 which has 576 shelf
            self.__colDimension = 24 #shelf consider as int in our warehouse
            self.__rowDimension = 24


    # ===============================================================
    # =             warehouse Printing Functions
    # ===============================================================

    def __printWorldInfo(self):
        self.__printBoardInfo()
        self.__printAgentInfo()

    def __printBoardInfo(self):
        for r in range(self.__rowDimension - 1, -1, -1):
            for c in range(self.__colDimension):
                self.__print_shelf_locate(c, r)
            #print("")
            print("")

    def __print_shelf_locate(self, c, r):
        shelf = ""
        shelf += "."



    def __printDirectionInfo(self):


    def _printRobotMove(self):
        # print robot's move
        if self.__lastAction == Robot.Action.TURN_LEFT:
            print("Last Action: Turned Left")

        elif self.__lastAction == Robot.Action.TURN_RIGHT:
            print("Last Action: Turned Right")

        elif self.__lastAction == Robot.Action.FORWARD:
            print("Last Action: Moved Forward")


        elif self.__lastAction == Robot.Action.GRAB:
            print("Last Action: Grabbed")

        else:
            print("Last Action: Invalid")

    def __printPerceptInfo(self):
        perceptString = "Percepts: "

        if perceptString[-1] == ' ' and perceptString[-2] == ',':
            perceptString = perceptString[:-2]

        print(perceptString)

    # ===============================================================
    # =                 Helper Functions
    # ===============================================================

    def __randomInt(self, limit):
        return random.randrange(limit)
    # ===============================================================
    # =                Add Features
    # ===============================================================
    def __addFeatures(self, file=None):
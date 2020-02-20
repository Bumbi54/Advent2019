import time
from collections import deque
import operator
import networkx as nx

def readInput(fileName):
    """
    Read input file and parse it into a list
    :param fileName: name of input file
    :return: list of input file content (each line is new element)
    """
    with open(fileName, 'r') as file:

        return list(map(int, file.readline().split(",")))


class IncodeComputer:

    def __init__(self, instructionList, inputValues):
        self.instructionList = instructionList[:]
        self.finishedBool = False
        self.inputValues = inputValues
        self.index = 0
        self.relativeBase = 0
        self.outOfMemorySpace = {}
        self.outputString = ''

    def getElementFromMemory(self, address):
        '''
        This function get values from memory or certain address.
        :param instructionList: memory space
        :param address: address from which we will retrieve value
        :return:
        '''

        if address >= len(self.instructionList) and address not in self.outOfMemorySpace.keys():
            return 0
        elif address >= len(self.instructionList) and address in self.outOfMemorySpace.keys():
            return self.outOfMemorySpace[address]
        else:
            return self.instructionList[address]

    def threeRegisterInstruction(self, firstParameterMode, secondParameterMode, thirdParameterMode):
        '''
        Get values of for three registers. Depending on mode. For instruction that uses three registers.
        :param firstParameterMode: 0 for position mode or 1 for immediate mode. For first register.
        :param secondParameterMode: 0 for position mode or 1 for immediate mode. For second register.
        :param thirdParameterMode: 0 for position mode or 1 for immediate mode. For third register.
        :return:
        '''

        if firstParameterMode == 0:
            firstRegister = self.getElementFromMemory(self.getElementFromMemory(self.index + 1))
        elif firstParameterMode == 2:
            firstRegister = self.getElementFromMemory(self.relativeBase + self.getElementFromMemory(self.index + 1))
        else:
            firstRegister = self.getElementFromMemory(self.index + 1)

        if secondParameterMode == 0:
            secondRegister = self.getElementFromMemory(self.getElementFromMemory(self.index + 2))
        elif secondParameterMode == 2:
            secondRegister = self.getElementFromMemory(self.relativeBase + self.getElementFromMemory(self.index + 2))
        else:
            secondRegister = self.getElementFromMemory(self.index + 2)

        if thirdParameterMode == 2:
            thirdRegister = self.relativeBase + self.getElementFromMemory(self.index + 3)
        else:
            thirdRegister = self.getElementFromMemory(self.index + 3)

        return firstRegister, secondRegister, thirdRegister

    def twoRegisterInstruction(self, firstParameterMode, secondParameterMode):
        '''
        Get values of for two registers. Depending on mode. For instruction that uses three registers.
        :param firstParameterMode: 0 for position mode or 1 for immediate mode. For first register.
        :param secondParameterMode: 0 for position mode or 1 for immediate mode. For second register.
        :return:
        '''

        if firstParameterMode == 0:
            firstRegister = self.getElementFromMemory(self.getElementFromMemory(self.index + 1))
        elif firstParameterMode == 2:
            firstRegister = self.getElementFromMemory(self.relativeBase + self.getElementFromMemory(self.index + 1))
        else:
            firstRegister = self.getElementFromMemory(self.index + 1)

        if secondParameterMode == 0:
            secondRegister = self.getElementFromMemory(self.getElementFromMemory(self.index + 2))
        elif secondParameterMode == 2:
            secondRegister = self.getElementFromMemory(self.relativeBase + self.getElementFromMemory(self.index + 2))
        else:
            secondRegister = self.getElementFromMemory(self.index + 2)

        return firstRegister, secondRegister

    def defaultRunOfProgram(self):
        '''
        Run the program by reading opcodes
        :param instructionList: list of program instructions
        :return:
        '''


        incrementStep = 4

        while (self.index < len(self.instructionList)):

            curentInstruction = self.instructionList[self.index] % 100
            firstParameterMode = (self.instructionList[self.index] // 100) % 10
            secondParameterMode = (self.instructionList[self.index] // 1000) % 10
            thirdParameterMode = (self.instructionList[self.index] // 10000) % 10

            if curentInstruction == 99:
                print("Jej Break")
                self.finishedBool = True
                break
            elif curentInstruction == 1:
                incrementStep = 4
                firstRegister, secondRegister, thirdRegister = self.threeRegisterInstruction(firstParameterMode,
                                                                                             secondParameterMode,
                                                                                             thirdParameterMode)
                # print(f"thirdRegister: {thirdRegister}, len(self.instructionList):{len(self.instructionList)}")
                if thirdRegister >= len(self.instructionList):
                    self.outOfMemorySpace[thirdRegister] = firstRegister + secondRegister
                else:
                    self.instructionList[thirdRegister] = firstRegister + secondRegister
            elif curentInstruction == 2:
                incrementStep = 4
                firstRegister, secondRegister, thirdRegister = self.threeRegisterInstruction(firstParameterMode,
                                                                                             secondParameterMode,
                                                                                             thirdParameterMode)

                if thirdRegister >= len(self.instructionList):
                    self.outOfMemorySpace[thirdRegister] = firstRegister * secondRegister
                else:
                    self.instructionList[thirdRegister] = firstRegister * secondRegister
            elif curentInstruction == 3:
                incrementStep = 2
                if len(self.inputValues) == 0:
                    #print("Input values is empty")
                    break
                else:
                    if firstParameterMode == 2:
                        if self.relativeBase + self.getElementFromMemory(self.index + 1) > len(self.instructionList):
                            self.outOfMemorySpace[
                                self.relativeBase + self.getElementFromMemory(self.index + 1)] = self.inputValues.pop(0)
                        else:
                            self.instructionList[
                                self.relativeBase + self.getElementFromMemory(self.index + 1)] = self.inputValues.pop(0)
                    else:
                        if self.getElementFromMemory(self.index + 1) > len(self.instructionList):
                            self.outOfMemorySpace[self.getElementFromMemory(self.index + 1)] = self.inputValues.pop(0)
                        else:
                            self.instructionList[self.getElementFromMemory(self.index + 1)] = self.inputValues.pop(0)

            elif curentInstruction == 4:
                incrementStep = 2

                if firstParameterMode == 0:
                    self.outputString += "," + str(self.getElementFromMemory(self.getElementFromMemory(self.index + 1)))
                elif firstParameterMode == 2:
                    self.outputString += "," + str(
                        self.getElementFromMemory(self.relativeBase + self.getElementFromMemory(self.index + 1)))
                else:
                    self.outputString += "," + str(self.getElementFromMemory(self.index + 1))
                #print(f"tempoutputString: {outputString}")
            elif curentInstruction == 5:
                incrementStep = 3
                firstRegister, secondRegister = self.twoRegisterInstruction(firstParameterMode, secondParameterMode)
                # print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}")
                if firstRegister != 0:
                    self.index = secondRegister
                    incrementStep = 0
            elif curentInstruction == 6:
                incrementStep = 3
                firstRegister, secondRegister = self.twoRegisterInstruction(firstParameterMode, secondParameterMode)
                # print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}")
                if firstRegister == 0:
                    self.index = secondRegister
                    incrementStep = 0
            elif curentInstruction == 7:
                incrementStep = 4
                firstRegister, secondRegister, thirdRegister = self.threeRegisterInstruction(firstParameterMode,
                                                                                             secondParameterMode,
                                                                                             thirdParameterMode)
                # print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
                if firstRegister < secondRegister:
                    if thirdRegister > len(self.instructionList):
                        self.outOfMemorySpace[thirdRegister] = 1
                    else:
                        self.instructionList[thirdRegister] = 1
                else:
                    if thirdRegister > len(self.instructionList):
                        self.outOfMemorySpace[thirdRegister] = 0
                    else:
                        self.instructionList[thirdRegister] = 0
            elif curentInstruction == 8:
                incrementStep = 4
                firstRegister, secondRegister, thirdRegister = self.threeRegisterInstruction(firstParameterMode,
                                                                                             secondParameterMode,
                                                                                             thirdParameterMode)
                # print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
                if firstRegister == secondRegister:
                    if thirdRegister > len(self.instructionList):
                        self.outOfMemorySpace[thirdRegister] = 1
                    else:
                        self.instructionList[thirdRegister] = 1
                else:
                    if thirdRegister > len(self.instructionList):
                        self.outOfMemorySpace[thirdRegister] = 0
                    else:
                        self.instructionList[thirdRegister] = 0

            elif curentInstruction == 9:
                incrementStep = 2

                if firstParameterMode == 0:
                    self.relativeBase += self.getElementFromMemory(self.getElementFromMemory(self.index + 1, ))
                elif firstParameterMode == 2:
                    # self.relativeBase += self.instructionList[self.relativeBase + self.instructionList[self.index + 1]]
                    # print(self.getElementFromMemory(self.instructionList, self.relativeBase + self.getElementFromMemory(self.instructionList, self.index + 1, self.outOfMemorySpace), self.outOfMemorySpace))
                    self.relativeBase += self.getElementFromMemory(
                        self.relativeBase + self.getElementFromMemory(self.index + 1))

                    # self.getElementFromMemory(self.instructionList, self.getElementFromMemory(self.instructionList, self.index + 1, self.outOfMemorySpace), self.outOfMemorySpace)
                else:
                    self.relativeBase += self.instructionList[self.index + 1]

            else:
                break
                print("Wrong opcodes instruction")

            self.index += incrementStep
            # print(self.instructionList)

        # print(f"outputString:{outputString}")
        # print(self.instructionList)
        return [int(value) for value in self.outputString.split(",")[1:]]

def findOxigenSystem(instructionList):
    '''
    Find Oxigen System by moving robot an maping the ship.
    :param instructionList: list of inscructions that will be ran
    :return:
    '''

    startPosition = (0,0)
    directions = {
                     (0, 1) : 4,
                     (0, -1) : 3,
                     (1, 0): 2,
                     (-1, 0) : 1
                }
    queue = deque()
    shipMap = {}
    shipMapDistance = {}

    queue.append([(0, 0), 0, []])
    #queue.append([(0,1), 1, [4]] )
    #queue.append([(0, -1), 1, [3]])
    #queue.append([(1, 0), 1,[2]])
    #queue.append([(-1, 0), 1, [1]])
    print(queue)

    while(queue):

        currentLocation = queue.pop()


        for direction in directions.keys():

            newCoordinate = tuple(map(operator.add, direction, currentLocation[0]))


            incodeProgram = IncodeComputer(instructionList, currentLocation[2][:] )
            incodeProgram.inputValues.append( directions[direction] )
            locationType = incodeProgram.defaultRunOfProgram()


            if newCoordinate in shipMap.keys() and shipMap.get(newCoordinate)  != locationType[-1]:
                print("------------------------------------------------------------------------------------------------------")
                print("veliki problemi")
                print(f"shipMap.get(newCoordinate): {shipMap.get(newCoordinate)}")


            shipMap[newCoordinate] = locationType[-1]

            if locationType[-1] != 0:

                if newCoordinate not in shipMapDistance.keys():
                    #print(f"Here: currentLocation[2]:{currentLocation[2]}, directions[direction]:{directions[direction]}, currentLocation[2] + [directions[direction]]: {currentLocation[2] + [directions[direction]]}")
                    shipMapDistance[newCoordinate] = currentLocation[1] + 1
                    queue.append([newCoordinate, currentLocation[1] + 1, currentLocation[2] + [directions[direction]] ])

                elif shipMapDistance[newCoordinate] > currentLocation[1] + 1:
                    #print("Here or here")
                    shipMapDistance[newCoordinate] = currentLocation[1] + 1
                    queue.append([newCoordinate, currentLocation[1] + 1, currentLocation[2] + [directions[direction]] ])

        #print(f"queue: {queue}")
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #time.sleep(2)

    print(shipMapDistance)
    print(shipMap)


def fillShipWithOxygen(shipMap, oxygenLocation):
    '''
    Calculate number of minutes it takes to fill ship with Oxygen
    :param shipMap: dictionary that represents ship
    :param oxygenLocation: location of Oxygen tank in ship, start position

    :return:
    '''

    directions = [
                     (0, 1),
                     (0, -1),
                     (1, 0),
                     (-1, 0),
                ]

    G = nx.Graph()
    pathLength= 0

    for x, y in shipMap.keys():
        if shipMap.get((x,y)) != 0:
            for direction in directions:
                neighbor = tuple(map(operator.add, direction, (x,y )))
                if shipMap.get(neighbor, 0) != 0:
                    G.add_edge((x,y), neighbor)

    print(G.nodes)
    for node in list(G.nodes) :

        newPath =  len(nx.shortest_path(G,oxygenLocation,node))

        if newPath > pathLength :
            pathLength = newPath

    return pathLength - 1

if __name__ == "__main__":

    instructionList = readInput("input.txt")
    print(f"instructionList: {instructionList}")

    #lenghtToOxigen = findOxigenSystem(instructionList)
    #print(f"lenghtToOxigen: {lenghtToOxigen}")

    #this was calculated prior but I used static because it takes a log time to get this data
    shipMap = {(0, 1): 0, (0, -1): 1, (1, 0): 0, (-1, 0): 0, (0, 0): 1, (0, -2): 1, (1, -1): 0, (-1, -1): 0, (0, -3): 0, (1, -2): 1, (-1, -2): 0, (1, -3): 0, (2, -2): 1, (2, -1): 0, (2, -3): 0, (3, -2): 1, (3, -1): 0, (3, -3): 0, (4, -2): 1, (4, -1): 0, (4, -3): 0, (5, -2): 1, (5, -1): 0, (5, -3): 0, (6, -2): 1, (6, -1): 0, (6, -3): 0, (7, -2): 1, (7, -1): 0, (7, -3): 0, (8, -2): 1, (8, -1): 0, (8, -3): 0, (9, -2): 1, (9, -1): 0, (9, -3): 0, (10, -2): 1, (10, -1): 0, (10, -3): 0, (11, -2): 1, (11, -1): 0, (11, -3): 0, (12, -2): 1, (12, -1): 0, (12, -3): 0, (13, -2): 1, (13, -1): 0, (13, -3): 0, (14, -2): 1, (14, -1): 0, (14, -3): 1, (15, -2): 0, (14, -4): 1, (15, -3): 0, (14, -5): 1, (15, -4): 0, (13, -4): 0, (14, -6): 1, (15, -5): 0, (13, -5): 0, (14, -7): 1, (15, -6): 0, (13, -6): 0, (14, -8): 1, (15, -7): 0, (13, -7): 0, (14, -9): 0, (15, -8): 0, (13, -8): 1, (13, -9): 0, (12, -8): 1, (12, -7): 0, (12, -9): 0, (11, -8): 1, (11, -7): 0, (11, -9): 0, (10, -8): 1, (10, -7): 0, (10, -9): 1, (9, -8): 0, (10, -10): 1, (9, -9): 0, (10, -11): 0, (11, -10): 1, (9, -10): 0, (11, -11): 0, (12, -10): 1, (12, -11): 1, (13, -10): 0, (12, -12): 1, (13, -11): 0, (12, -13): 0, (13, -12): 1, (11, -12): 0, (13, -13): 0, (14, -12): 1, (14, -11): 0, (14, -13): 0, (15, -12): 1, (15, -11): 0, (15, -13): 0, (16, -12): 1, (16, -11): 1, (16, -13): 0, (17, -12): 0, (16, -10): 1, (17, -11): 0, (16, -9): 0, (17, -10): 1, (15, -10): 1, (15, -9): 0, (14, -10): 1, (17, -9): 0, (18, -10): 1, (18, -9): 1, (18, -11): 0, (19, -10): 0, (18, -8): 1, (19, -9): 0, (18, -7): 1, (19, -8): 0, (17, -8): 0, (18, -6): 1, (19, -7): 0, (17, -7): 0, (18, -5): 0, (19, -6): 0, (17, -6): 1, (17, -5): 0, (16, -6): 1, (16, -5): 1, (16, -7): 1, (16, -8): 1, (16, -4): 1, (16, -3): 1, (17, -4): 0, (16, -2): 1, (17, -3): 0, (16, -1): 1, (17, -2): 0, (16, 0): 1, (17, -1): 0, (15, -1): 0, (16, 1): 0, (17, 0): 1, (15, 0): 0, (17, 1): 0, (18, 0): 1, (18, 1): 1, (18, -1): 1, (19, 0): 0, (18, -2): 1, (19, -1): 0, (18, -3): 1, (19, -2): 0, (18, -4): 1, (19, -3): 0, (19, -4): 0, (18, 2): 1, (19, 1): 0, (18, 3): 1, (19, 2): 0, (17, 2): 0, (18, 4): 1, (19, 3): 0, (17, 3): 0, (18, 5): 0, (19, 4): 0, (17, 4): 1, (17, 5): 0, (16, 4): 1, (16, 5): 1, (16, 3): 0, (15, 4): 0, (16, 6): 1, (15, 5): 0, (16, 7): 0, (17, 6): 0, (15, 6): 1, (15, 7): 0, (14, 6): 1, (14, 7): 0, (14, 5): 1, (13, 6): 0, (14, 4): 1, (13, 5): 0, (14, 3): 1, (13, 4): 0, (14, 2): 1, (15, 3): 0, (13, 3): 0, (14, 1): 0, (15, 2): 1, (13, 2): 1, (13, 1): 0, (12, 2): 1, (12, 3): 0, (12, 1): 0, (11, 2): 1, (11, 3): 0, (11, 1): 0, (10, 2): 1, (10, 3): 0, (10, 1): 0, (9, 2): 1, (9, 3): 0, (9, 1): 0, (8, 2): 1, (8, 3): 1, (8, 1): 0, (7, 2): 0, (8, 4): 1, (7, 3): 0, (8, 5): 0, (9, 4): 1, (7, 4): 0, (9, 5): 0, (10, 4): 1, (10, 5): 1, (11, 4): 0, (10, 6): 1, (11, 5): 0, (10, 7): 1, (11, 6): 0, (9, 6): 0, (10, 8): 1, (11, 7): 0, (9, 7): 0, (10, 9): 0, (11, 8): 0, (9, 8): 1, (9, 9): 0, (8, 8): 1, (8, 9): 0, (8, 7): 1, (7, 8): 0, (8, 6): 1, (7, 7): 0, (7, 6): 1, (7, 5): 0, (6, 6): 1, (6, 7): 0, (6, 5): 0, (5, 6): 1, (5, 7): 0, (5, 5): 0, (4, 6): 1, (4, 7): 1, (4, 5): 0, (3, 6): 0, (4, 8): 1, (3, 7): 0, (4, 9): 1, (5, 8): 0, (3, 8): 0, (4, 10): 1, (5, 9): 0, (3, 9): 0, (4, 11): 0, (5, 10): 0, (3, 10): 1, (3, 11): 0, (2, 10): 1, (2, 11): 0, (2, 9): 1, (1, 10): 0, (2, 8): 1, (1, 9): 0, (2, 7): 1, (1, 8): 0, (2, 6): 1, (1, 7): 0, (2, 5): 1, (1, 6): 0, (2, 4): 1, (3, 5): 0, (1, 5): 0, (2, 3): 0, (3, 4): 1, (1, 4): 0, (3, 3): 0, (4, 4): 1, (4, 3): 1, (5, 4): 0, (4, 2): 1, (5, 3): 0, (4, 1): 0, (5, 2): 1, (3, 2): 0, (5, 1): 0, (6, 2): 1, (6, 3): 1, (6, 1): 1, (6, 0): 1, (7, 1): 0, (7, 0): 1, (5, 0): 1, (4, 0): 1, (3, 0): 1, (3, 1): 0, (2, 0): 1, (2, 1): 1, (2, 2): 1, (1, 1): 0, (1, 2): 1, (1, 3): 0, (0, 2): 1, (0, 3): 0, (-1, 2): 1, (-1, 3): 0, (-1, 1): 0, (-2, 2): 1, (-2, 3): 1, (-2, 1): 0, (-3, 2): 0, (-2, 4): 1, (-3, 3): 0, (-2, 5): 0, (-1, 4): 1, (-3, 4): 0, (-1, 5): 0, (0, 4): 1, (0, 5): 1, (0, 6): 1, (0, 7): 0, (-1, 6): 1, (-1, 7): 0, (-2, 6): 1, (-2, 7): 1, (-3, 6): 0, (-2, 8): 1, (-3, 7): 0, (-2, 9): 0, (-1, 8): 0, (-3, 8): 1, (-3, 9): 0, (-4, 8): 1, (-4, 9): 0, (-4, 7): 0, (-5, 8): 1, (-5, 9): 0, (-5, 7): 0, (-6, 8): 1, (-6, 9): 0, (-6, 7): 0, (-7, 8): 1, (-7, 9): 0, (-7, 7): 0, (-8, 8): 1, (-8, 9): 0, (-8, 7): 0, (-9, 8): 1, (-9, 9): 0, (-9, 7): 0, (-10, 8): 1, (-10, 9): 0, (-10, 7): 0, (-11, 8): 1, (-11, 9): 0, (-11, 7): 0, (-12, 8): 1, (-12, 9): 1, (-12, 7): 0, (-13, 8): 0, (-12, 10): 1, (-13, 9): 0, (-12, 11): 0, (-11, 10): 0, (-13, 10): 1, (-13, 11): 0, (-14, 10): 1, (-14, 11): 0, (-14, 9): 0, (-15, 10): 1, (-15, 11): 0, (-15, 9): 0, (-16, 10): 1, (-16, 11): 1, (-16, 9): 0, (-17, 10): 0, (-16, 12): 1, (-17, 11): 0, (-16, 13): 0, (-15, 12): 0, (-17, 12): 1, (-17, 13): 0, (-18, 12): 1, (-18, 13): 1, (-18, 11): 0, (-19, 12): 0, (-18, 14): 1, (-19, 13): 0, (-18, 15): 0, (-17, 14): 1, (-19, 14): 0, (-17, 15): 0, (-16, 14): 1, (-16, 15): 1, (-15, 14): 0, (-16, 16): 1, (-15, 15): 0, (-16, 17): 1, (-15, 16): 0, (-17, 16): 0, (-16, 18): 1, (-15, 17): 0, (-17, 17): 0, (-16, 19): 0, (-15, 18): 1, (-17, 18): 1, (-17, 19): 0, (-18, 18): 1, (-18, 19): 0, (-18, 17): 1, (-19, 18): 0, (-18, 16): 1, (-19, 17): 0, (-19, 16): 1, (-19, 15): 0, (-20, 16): 1, (-20, 17): 1, (-20, 15): 1, (-21, 16): 0, (-20, 14): 1, (-21, 15): 0, (-20, 13): 1, (-21, 14): 0, (-20, 12): 1, (-21, 13): 0, (-20, 11): 1, (-21, 12): 0, (-20, 10): 1, (-19, 11): 0, (-21, 11): 0, (-20, 9): 1, (-19, 10): 0, (-21, 10): 0, (-20, 8): 1, (-19, 9): 0, (-21, 9): 0, (-20, 7): 0, (-19, 8): 1, (-21, 8): 0, (-19, 7): 0, (-18, 8): 1, (-18, 9): 1, (-18, 7): 0, (-17, 8): 1, (-17, 9): 0, (-17, 7): 0, (-16, 8): 1, (-16, 7): 1, (-15, 8): 0, (-16, 6): 1, (-15, 7): 0, (-16, 5): 0, (-15, 6): 1, (-17, 6): 0, (-15, 5): 0, (-14, 6): 1, (-14, 7): 1, (-14, 5): 0, (-13, 6): 1, (-13, 7): 0, (-13, 5): 0, (-12, 6): 1, (-12, 5): 0, (-11, 6): 1, (-11, 5): 0, (-10, 6): 1, (-10, 5): 0, (-9, 6): 1, (-9, 5): 0, (-8, 6): 1, (-8, 5): 1, (-7, 6): 0, (-8, 4): 1, (-7, 5): 0, (-8, 3): 0, (-7, 4): 0, (-9, 4): 1, (-9, 3): 0, (-10, 4): 1, (-10, 3): 1, (-11, 4): 0, (-10, 2): 1, (-11, 3): 0, (-10, 1): 1, (-9, 2): 0, (-11, 2): 0, (-10, 0): 1, (-9, 1): 0, (-11, 1): 0, (-10, -1): 0, (-9, 0): 0, (-11, 0): 1, (-11, -1): 0, (-12, 0): 1, (-12, 1): 0, (-12, -1): 0, (-13, 0): 1, (-13, 1): 0, (-13, -1): 0, (-14, 0): 1, (-14, 1): 1, (-14, -1): 0, (-15, 0): 0, (-14, 2): 1, (-15, 1): 0, (-14, 3): 0, (-13, 2): 0, (-15, 2): 1, (-15, 3): 0, (-16, 2): 1, (-16, 3): 1, (-16, 1): 0, (-17, 2): 0, (-16, 4): 1, (-17, 3): 0, (-15, 4): 1, (-17, 4): 1, (-17, 5): 0, (-18, 4): 1, (-18, 5): 1, (-18, 3): 0, (-19, 4): 0, (-18, 6): 1, (-19, 5): 0, (-19, 6): 1, (-20, 6): 1, (-20, 5): 1, (-21, 6): 0, (-20, 4): 1, (-21, 5): 0, (-20, 3): 1, (-21, 4): 0, (-20, 2): 1, (-19, 3): 0, (-21, 3): 0, (-20, 1): 1, (-19, 2): 0, (-21, 2): 0, (-20, 0): 1, (-19, 1): 0, (-21, 1): 0, (-20, -1): 0, (-19, 0): 1, (-21, 0): 0, (-19, -1): 0, (-18, 0): 1, (-18, 1): 1, (-18, -1): 0, (-17, 0): 1, (-17, 1): 0, (-17, -1): 0, (-16, 0): 1, (-16, -1): 1, (-16, -2): 1, (-15, -1): 0, (-16, -3): 1, (-15, -2): 0, (-17, -2): 0, (-16, -4): 1, (-15, -3): 0, (-17, -3): 0, (-16, -5): 0, (-15, -4): 0, (-17, -4): 1, (-17, -5): 0, (-18, -4): 1, (-18, -3): 0, (-18, -5): 1, (-19, -4): 0, (-18, -6): 1, (-19, -5): 0, (-18, -7): 0, (-17, -6): 0, (-19, -6): 1, (-19, -7): 0, (-20, -6): 1, (-20, -5): 1, (-20, -7): 1, (-21, -6): 0, (-20, -8): 1, (-21, -7): 0, (-20, -9): 1, (-19, -8): 0, (-21, -8): 0, (-20, -10): 1, (-19, -9): 0, (-21, -9): 0, (-20, -11): 1, (-19, -10): 0, (-21, -10): 0, (-20, -12): 1, (-19, -11): 0, (-21, -11): 0, (-20, -13): 1, (-19, -12): 0, (-21, -12): 0, (-20, -14): 1, (-19, -13): 0, (-21, -13): 0, (-20, -15): 1, (-19, -14): 0, (-21, -14): 0, (-20, -16): 1, (-19, -15): 0, (-21, -15): 0, (-20, -17): 1, (-19, -16): 0, (-21, -16): 0, (-20, -18): 1, (-19, -17): 0, (-21, -17): 0, (-20, -19): 0, (-19, -18): 1, (-21, -18): 0, (-19, -19): 0, (-18, -18): 1, (-18, -17): 1, (-18, -19): 0, (-17, -18): 0, (-18, -16): 1, (-17, -17): 0, (-18, -15): 1, (-17, -16): 0, (-18, -14): 1, (-17, -15): 0, (-18, -13): 1, (-17, -14): 0, (-18, -12): 1, (-17, -13): 0, (-18, -11): 1, (-17, -12): 0, (-18, -10): 1, (-17, -11): 0, (-18, -9): 1, (-17, -10): 0, (-18, -8): 1, (-17, -9): 0, (-17, -8): 1, (-17, -7): 0, (-16, -8): 1, (-16, -7): 0, (-16, -9): 0, (-15, -8): 1, (-15, -7): 0, (-15, -9): 0, (-14, -8): 1, (-14, -7): 1, (-14, -9): 0, (-13, -8): 0, (-14, -6): 1, (-13, -7): 0, (-14, -5): 0, (-13, -6): 1, (-15, -6): 1, (-15, -5): 0, (-16, -6): 1, (-13, -5): 0, (-12, -6): 1, (-12, -5): 0, (-12, -7): 0, (-11, -6): 1, (-11, -5): 0, (-11, -7): 0, (-10, -6): 1, (-10, -5): 0, (-10, -7): 0, (-9, -6): 1, (-9, -5): 0, (-9, -7): 0, (-8, -6): 1, (-8, -5): 0, (-8, -7): 1, (-7, -6): 0, (-8, -8): 1, (-7, -7): 0, (-8, -9): 1, (-7, -8): 0, (-9, -8): 0, (-8, -10): 1, (-7, -9): 0, (-9, -9): 0, (-8, -11): 0, (-7, -10): 0, (-9, -10): 1, (-9, -11): 0, (-10, -10): 1, (-10, -9): 1, (-10, -11): 0, (-11, -10): 0, (-10, -8): 1, (-11, -9): 0, (-11, -8): 1, (-12, -8): 1, (-12, -9): 1, (-12, -10): 1, (-13, -9): 0, (-12, -11): 1, (-13, -10): 0, (-12, -12): 1, (-11, -11): 0, (-13, -11): 0, (-12, -13): 0, (-11, -12): 1, (-13, -12): 0, (-11, -13): 0, (-10, -12): 1, (-10, -13): 1, (-9, -12): 0, (-10, -14): 1, (-9, -13): 0, (-10, -15): 0, (-9, -14): 0, (-11, -14): 1, (-11, -15): 0, (-12, -14): 1, (-12, -15): 0, (-13, -14): 1, (-13, -13): 0, (-13, -15): 0, (-14, -14): 1, (-14, -13): 0, (-14, -15): 1, (-15, -14): 0, (-14, -16): 1, (-15, -15): 0, (-14, -17): 0, (-13, -16): 0, (-15, -16): 1, (-15, -17): 0, (-16, -16): 1, (-16, -15): 1, (-16, -17): 1, (-16, -18): 1, (-16, -19): 1, (-15, -18): 0, (-16, -20): 1, (-15, -19): 0, (-17, -19): 0, (-16, -21): 0, (-15, -20): 1, (-17, -20): 1, (-17, -21): 0, (-18, -20): 1, (-18, -21): 0, (-19, -20): 1, (-19, -21): 0, (-20, -20): 1, (-20, -21): 0, (-21, -20): 0, (-15, -21): 0, (-14, -20): 1, (-14, -19): 0, (-14, -21): 0, (-13, -20): 1, (-13, -19): 0, (-13, -21): 0, (-12, -20): 1, (-12, -19): 0, (-12, -21): 0, (-11, -20): 1, (-11, -19): 0, (-11, -21): 0, (-10, -20): 1, (-10, -19): 1, (-10, -21): 0, (-9, -20): 0, (-10, -18): 1, (-9, -19): 0, (-10, -17): 0, (-9, -18): 1, (-11, -18): 0, (-9, -17): 0, (-8, -18): 1, (-8, -17): 0, (-8, -19): 1, (-7, -18): 0, (-8, -20): 1, (-7, -19): 0, (-8, -21): 0, (-7, -20): 1, (-7, -21): 0, (-6, -20): 1, (-6, -19): 0, (-6, -21): 0, (-5, -20): 1, (-5, -19): 0, (-5, -21): 0, (-4, -20): 1, (-4, -19): 0, (-4, -21): 0, (-3, -20): 1, (-3, -19): 0, (-3, -21): 0, (-2, -20): 1, (-2, -19): 1, (-2, -21): 0, (-1, -20): 0, (-2, -18): 1, (-1, -19): 0, (-2, -17): 1, (-1, -18): 0, (-3, -18): 0, (-2, -16): 1, (-1, -17): 0, (-3, -17): 0, (-2, -15): 1, (-1, -16): 0, (-3, -16): 0, (-2, -14): 1, (-1, -15): 0, (-3, -15): 0, (-2, -13): 1, (-1, -14): 0, (-3, -14): 0, (-2, -12): 1, (-1, -13): 0, (-3, -13): 0, (-2, -11): 0, (-1, -12): 0, (-3, -12): 1, (-3, -11): 0, (-4, -12): 1, (-4, -11): 0, (-4, -13): 0, (-5, -12): 1, (-5, -11): 0, (-5, -13): 0, (-6, -12): 1, (-6, -11): 1, (-6, -13): 0, (-7, -12): 1, (-7, -11): 0, (-7, -13): 0, (-8, -12): 1, (-8, -13): 1, (-8, -14): 1, (-8, -15): 0, (-7, -14): 1, (-7, -15): 0, (-6, -14): 1, (-6, -15): 0, (-5, -14): 1, (-5, -15): 0, (-4, -14): 1, (-4, -15): 1, (-4, -16): 1, (-4, -17): 0, (-5, -16): 1, (-5, -17): 0, (-6, -16): 1, (-6, -17): 1, (-7, -16): 1, (-7, -17): 0, (-8, -16): 1, (-9, -16): 1, (-9, -15): 0, (-10, -16): 1, (-11, -16): 1, (-11, -17): 0, (-12, -16): 1, (-12, -17): 1, (-12, -18): 1, (-13, -17): 0, (-13, -18): 1, (-14, -18): 1, (-6, -18): 1, (-5, -18): 1, (-4, -18): 1, (-6, -10): 1, (-6, -9): 1, (-5, -10): 0, (-6, -8): 1, (-5, -9): 0, (-6, -7): 1, (-5, -8): 0, (-6, -6): 1, (-5, -7): 0, (-6, -5): 1, (-5, -6): 0, (-6, -4): 1, (-5, -5): 0, (-7, -5): 0, (-6, -3): 0, (-5, -4): 1, (-7, -4): 0, (-5, -3): 0, (-4, -4): 1, (-4, -3): 0, (-4, -5): 0, (-3, -4): 1, (-3, -3): 0, (-3, -5): 0, (-2, -4): 1, (-2, -3): 1, (-2, -5): 1, (-1, -4): 0, (-2, -6): 1, (-1, -5): 0, (-2, -7): 1, (-1, -6): 0, (-3, -6): 0, (-2, -8): 1, (-1, -7): 0, (-3, -7): 0, (-2, -9): 0, (-1, -8): 0, (-3, -8): 1, (-3, -9): 0, (-4, -8): 1, (-4, -7): 1, (-4, -9): 1, (-4, -10): 1, (-3, -10): 1, (-2, -10): 1, (-1, -10): 1, (-1, -9): 0, (-1, -11): 0, (0, -10): 1, (0, -9): 0, (0, -11): 1, (1, -10): 0, (0, -12): 1, (1, -11): 0, (0, -13): 1, (1, -12): 0, (0, -14): 1, (1, -13): 0, (0, -15): 1, (1, -14): 0, (0, -16): 1, (1, -15): 0, (0, -17): 0, (1, -16): 1, (1, -17): 0, (2, -16): 1, (2, -15): 0, (2, -17): 0, (3, -16): 1, (3, -15): 0, (3, -17): 0, (4, -16): 1, (4, -15): 0, (4, -17): 1, (5, -16): 0, (4, -18): 1, (5, -17): 0, (4, -19): 1, (5, -18): 0, (3, -18): 0, (4, -20): 1, (5, -19): 0, (3, -19): 0, (4, -21): 0, (5, -20): 1, (3, -20): 1, (3, -21): 0, (2, -20): 1, (2, -19): 0, (2, -21): 0, (1, -20): 1, (1, -19): 0, (1, -21): 0, (0, -20): 1, (0, -19): 1, (0, -21): 0, (0, -18): 1, (1, -18): 1, (2, -18): 1, (5, -21): 0, (6, -20): 1, (6, -19): 0, (6, -21): 0, (7, -20): 1, (7, -19): 0, (7, -21): 0, (8, -20): 1, (8, -19): 0, (8, -21): 0, (9, -20): 1, (9, -19): 0, (9, -21): 0, (10, -20): 1, (10, -19): 1, (10, -21): 0, (11, -20): 0, (10, -18): 1, (11, -19): 0, (10, -17): 0, (11, -18): 1, (9, -18): 0, (11, -17): 0, (12, -18): 1, (12, -17): 0, (12, -19): 0, (13, -18): 1, (13, -17): 0, (13, -19): 0, (14, -18): 1, (14, -17): 0, (14, -19): 0, (15, -18): 1, (15, -17): 0, (15, -19): 0, (16, -18): 1, (16, -17): 1, (16, -19): 0, (17, -18): 0, (16, -16): 1, (17, -17): 0, (16, -15): 0, (17, -16): 1, (15, -16): 0, (17, -15): 0, (18, -16): 1, (18, -15): 1, (18, -17): 1, (19, -16): 0, (18, -18): 1, (19, -17): 0, (18, -19): 1, (19, -18): 0, (18, -20): 1, (19, -19): 0, (17, -19): 0, (18, -21): 0, (19, -20): 0, (17, -20): 1, (17, -21): 0, (16, -20): 1, (16, -21): 0, (15, -20): 1, (15, -21): 0, (14, -20): 1, (14, -21): 0, (13, -20): 1, (13, -21): 0, (12, -20): 1, (12, -21): 0, (18, -14): 1, (19, -15): 0, (18, -13): 1, (19, -14): 0, (17, -14): 1, (17, -13): 0, (16, -14): 1, (15, -14): 1, (15, -15): 0, (14, -14): 1, (14, -15): 1, (13, -14): 0, (14, -16): 1, (13, -15): 0, (13, -16): 1, (12, -16): 1, (12, -15): 0, (11, -16): 1, (11, -15): 0, (10, -16): 1, (10, -15): 1, (9, -16): 0, (10, -14): 1, (9, -15): 0, (10, -13): 1, (11, -14): 1, (9, -14): 0, (11, -13): 0, (12, -14): 1, (10, -12): 1, (9, -13): 0, (9, -12): 1, (9, -11): 0, (8, -12): 1, (8, -11): 1, (8, -13): 0, (7, -12): 0, (8, -10): 1, (7, -11): 0, (8, -9): 0, (7, -10): 1, (7, -9): 0, (6, -10): 1, (6, -9): 0, (6, -11): 0, (5, -10): 1, (5, -9): 0, (5, -11): 0, (4, -10): 1, (4, -9): 1, (4, -11): 0, (3, -10): 0, (4, -8): 1, (3, -9): 0, (4, -7): 1, (5, -8): 0, (3, -8): 0, (4, -6): 1, (5, -7): 0, (3, -7): 0, (4, -5): 0, (5, -6): 1, (3, -6): 0, (5, -5): 0, (6, -6): 1, (6, -5): 1, (6, -7): 0, (7, -6): 0, (6, -4): 1, (7, -5): 0, (7, -4): 1, (5, -4): 1, (4, -4): 1, (3, -4): 1, (3, -5): 0, (2, -4): 1, (2, -5): 1, (1, -4): 0, (2, -6): 1, (1, -5): 0, (2, -7): 1, (1, -6): 0, (2, -8): 1, (1, -7): 0, (2, -9): 1, (1, -8): 1, (1, -9): 0, (0, -8): 1, (0, -7): 1, (0, -6): 1, (0, -5): 1, (0, -4): 1, (2, -10): 1, (2, -11): 1, (2, -12): 1, (3, -11): 0, (2, -13): 0, (3, -12): 1, (3, -13): 0, (4, -12): 1, (4, -13): 1, (5, -12): 0, (4, -14): 1, (5, -13): 0, (5, -14): 1, (3, -14): 1, (2, -14): 1, (5, -15): 0, (6, -14): 1, (6, -13): 1, (6, -15): 0, (7, -14): 1, (7, -13): 0, (7, -15): 0, (8, -14): 1, (8, -15): 1, (8, -16): 1, (8, -17): 1, (7, -16): 0, (8, -18): 1, (9, -17): 0, (7, -17): 0, (7, -18): 1, (6, -18): 1, (6, -17): 1, (6, -16): 1, (6, -12): 1, (8, -4): 1, (8, -5): 0, (9, -4): 1, (9, -5): 0, (10, -4): 1, (10, -5): 1, (11, -4): 0, (10, -6): 1, (11, -5): 0, (11, -6): 1, (9, -6): 1, (9, -7): 0, (8, -6): 1, (8, -7): 1, (8, -8): 1, (7, -7): 0, (7, -8): 1, (6, -8): 1, (12, -6): 1, (12, -5): 1, (12, -4): 1, (18, -12): 1, (19, -13): 0, (19, -12): 0, (-4, -6): 1, (-2, -2): 1, (-1, -3): 0, (-2, -1): 0, (-3, -2): 1, (-3, -1): 0, (-4, -2): 1, (-4, -1): 0, (-5, -2): 1, (-5, -1): 0, (-6, -2): 1, (-6, -1): 1, (-7, -2): 0, (-6, 0): 1, (-7, -1): 0, (-6, 1): 0, (-5, 0): 1, (-7, 0): 0, (-5, 1): 0, (-4, 0): 1, (-4, 1): 1, (-3, 0): 1, (-3, 1): 0, (-2, 0): 1, (-4, 2): 1, (-4, 3): 1, (-5, 2): 0, (-4, 4): 1, (-5, 3): 0, (-4, 5): 0, (-5, 4): 1, (-5, 5): 0, (-6, 4): 1, (-6, 5): 1, (-6, 3): 1, (-6, 2): 1, (-7, 3): 0, (-7, 2): 1, (-7, 1): 0, (-8, 2): 1, (-8, 1): 1, (-8, 0): 1, (-8, -1): 1, (-8, -2): 1, (-9, -1): 0, (-8, -3): 1, (-9, -2): 0, (-8, -4): 1, (-7, -3): 0, (-9, -3): 0, (-9, -4): 1, (-10, -4): 1, (-10, -3): 0, (-11, -4): 1, (-11, -3): 0, (-12, -4): 1, (-12, -3): 0, (-13, -4): 1, (-13, -3): 0, (-14, -4): 1, (-14, -3): 1, (-14, -2): 1, (-13, -2): 1, (-12, -2): 1, (-11, -2): 1, (-10, -2): 1, (-6, 6): 1, (-5, 6): 1, (-4, 6): 1, (-16, -14): 1, (-16, -13): 1, (-16, -12): 1, (-15, -13): 0, (-16, -11): 1, (-15, -12): 0, (-16, -10): 1, (-15, -11): 0, (-15, -10): 1, (-14, -10): 1, (-14, -11): 1, (-14, -12): 1, (-20, -4): 1, (-21, -5): 0, (-20, -3): 1, (-21, -4): 0, (-20, -2): 1, (-19, -3): 0, (-21, -3): 0, (-19, -2): 1, (-21, -2): 0, (-18, -2): 1, (-18, 2): 1, (-14, 4): 1, (-13, 4): 1, (-13, 3): 0, (-12, 4): 1, (-12, 3): 1, (-12, 2): 1, (-14, 8): 1, (-18, 10): 1, (-20, 18): 1, (-21, 17): 0, (-20, 19): 0, (-21, 18): 0, (-15, 19): 0, (-14, 18): 1, (-14, 19): 0, (-14, 17): 1, (-13, 18): 0, (-14, 16): 1, (-13, 17): 0, (-14, 15): 1, (-13, 16): 0, (-14, 14): 1, (-13, 15): 0, (-14, 13): 0, (-13, 14): 1, (-13, 13): 0, (-12, 14): 1, (-12, 15): 0, (-12, 13): 0, (-11, 14): 1, (-11, 15): 0, (-11, 13): 0, (-10, 14): 1, (-10, 15): 0, (-10, 13): 0, (-9, 14): 1, (-9, 15): 0, (-9, 13): 0, (-8, 14): 1, (-8, 15): 0, (-8, 13): 1, (-7, 14): 0, (-8, 12): 1, (-7, 13): 0, (-8, 11): 1, (-7, 12): 0, (-9, 12): 0, (-8, 10): 1, (-7, 11): 0, (-9, 11): 0, (-7, 10): 1, (-9, 10): 1, (-10, 10): 1, (-10, 11): 1, (-10, 12): 1, (-11, 11): 0, (-11, 12): 1, (-12, 12): 1, (-13, 12): 1, (-14, 12): 1, (-6, 10): 1, (-6, 11): 1, (-5, 10): 0, (-6, 12): 1, (-5, 11): 0, (-6, 13): 1, (-5, 12): 0, (-6, 14): 1, (-5, 13): 0, (-6, 15): 1, (-5, 14): 0, (-6, 16): 1, (-5, 15): 0, (-7, 15): 0, (-6, 17): 1, (-5, 16): 0, (-7, 16): 0, (-6, 18): 1, (-5, 17): 0, (-7, 17): 0, (-6, 19): 0, (-5, 18): 1, (-7, 18): 1, (-7, 19): 0, (-8, 18): 1, (-8, 19): 0, (-8, 17): 0, (-9, 18): 1, (-9, 19): 0, (-9, 17): 0, (-10, 18): 1, (-10, 19): 0, (-10, 17): 1, (-11, 18): 0, (-10, 16): 1, (-11, 17): 0, (-9, 16): 1, (-11, 16): 1, (-12, 16): 1, (-12, 17): 1, (-12, 18): 1, (-12, 19): 0, (-8, 16): 1, (-5, 19): 0, (-4, 18): 1, (-4, 19): 0, (-4, 17): 0, (-3, 18): 1, (-3, 19): 0, (-3, 17): 0, (-2, 18): 1, (-2, 19): 0, (-2, 17): 0, (-1, 18): 1, (-1, 19): 0, (-1, 17): 0, (0, 18): 1, (0, 19): 0, (0, 17): 1, (1, 18): 0, (0, 16): 1, (1, 17): 0, (0, 15): 0, (1, 16): 1, (-1, 16): 0, (1, 15): 0, (2, 16): 1, (2, 17): 0, (2, 15): 1, (3, 16): 0, (2, 14): 1, (3, 15): 0, (2, 13): 0, (3, 14): 0, (1, 14): 1, (1, 13): 0, (0, 14): 1, (0, 13): 0, (-1, 14): 1, (-1, 15): 0, (-1, 13): 0, (-2, 14): 1, (-2, 15): 0, (-2, 13): 1, (-3, 14): 0, (-2, 12): 1, (-3, 13): 0, (-2, 11): 1, (-1, 12): 0, (-3, 12): 0, (-2, 10): 1, (-1, 11): 0, (-3, 11): 0, (-1, 10): 1, (-3, 10): 1, (-4, 10): 1, (-4, 11): 1, (-4, 12): 1, (-4, 13): 1, (-4, 14): 1, (-4, 15): 1, (-4, 16): 1, (-3, 15): 0, (-3, 16): 1, (-2, 16): 1, (-1, 9): 0, (0, 10): 1, (0, 11): 1, (0, 9): 1, (0, 8): 1, (0, 12): 1, (1, 11): 0, (1, 12): 1, (2, 12): 1, (3, 12): 1, (3, 13): 0, (4, 12): 1, (4, 13): 1, (5, 12): 0, (4, 14): 1, (5, 13): 0, (4, 15): 0, (5, 14): 1, (5, 15): 0, (6, 14): 1, (6, 15): 1, (6, 13): 0, (7, 14): 0, (6, 16): 1, (7, 15): 0, (6, 17): 1, (7, 16): 0, (5, 16): 0, (6, 18): 1, (7, 17): 0, (5, 17): 0, (6, 19): 0, (7, 18): 1, (5, 18): 1, (5, 19): 0, (4, 18): 1, (4, 19): 0, (4, 17): 1, (3, 18): 1, (3, 19): 0, (3, 17): 0, (2, 18): 1, (2, 19): 0, (4, 16): 1, (7, 19): 0, (8, 18): 1, (8, 19): 0, (8, 17): 0, (9, 18): 1, (9, 19): 0, (9, 17): 0, (10, 18): 1, (10, 19): 0, (10, 17): 0, (11, 18): 1, (11, 19): 0, (11, 17): 0, (12, 18): 1, (12, 19): 0, (12, 17): 0, (13, 18): 1, (13, 19): 0, (13, 17): 0, (14, 18): 1, (14, 19): 0, (14, 17): 1, (15, 18): 0, (14, 16): 1, (15, 17): 0, (14, 15): 1, (15, 16): 0, (13, 16): 0, (14, 14): 1, (15, 15): 0, (13, 15): 0, (14, 13): 0, (15, 14): 0, (13, 14): 1, (13, 13): 0, (12, 14): 1, (12, 15): 1, (12, 13): 0, (11, 14): 0, (12, 16): 1, (11, 15): 0, (11, 16): 1, (10, 16): 1, (10, 15): 1, (9, 16): 0, (10, 14): 1, (9, 15): 0, (10, 13): 1, (9, 14): 0, (10, 12): 1, (11, 13): 0, (9, 13): 0, (10, 11): 0, (11, 12): 0, (9, 12): 1, (9, 11): 0, (8, 12): 1, (8, 13): 1, (8, 11): 1, (7, 12): 0, (8, 10): 1, (7, 11): 0, (9, 10): 1, (7, 10): 1, (7, 9): 0, (6, 10): 1, (6, 11): 1, (6, 9): 1, (6, 8): 1, (6, 12): 1, (5, 11): 0, (10, 10): 1, (11, 10): 1, (11, 11): 0, (11, 9): 0, (12, 10): 1, (12, 11): 0, (12, 9): 0, (13, 10): 1, (13, 11): 0, (13, 9): 0, (14, 10): 1, (14, 11): 0, (14, 9): 0, (15, 10): 1, (15, 11): 0, (15, 9): 0, (16, 10): 1, (16, 11): 0, (16, 9): 0, (17, 10): 1, (17, 11): 0, (17, 9): 0, (18, 10): 1, (18, 11): 1, (18, 9): 1, (19, 10): 0, (18, 8): 1, (19, 9): 0, (18, 7): 1, (19, 8): 0, (17, 8): 1, (17, 7): 0, (16, 8): 1, (15, 8): 1, (14, 8): 1, (13, 8): 1, (13, 7): 0, (12, 8): 1, (12, 7): 1, (12, 6): 1, (12, 5): 1, (12, 4): 1, (18, 6): 1, (19, 7): 0, (19, 6): 0, (18, 12): 1, (19, 11): 0, (18, 13): 0, (19, 12): 0, (17, 12): 1, (17, 13): 0, (16, 12): 1, (16, 13): 1, (15, 12): 1, (15, 13): 0, (14, 12): 1, (13, 12): 1, (12, 12): 1, (16, 14): 1, (16, 15): 0, (17, 14): 1, (17, 15): 0, (18, 14): 1, (18, 15): 1, (19, 14): 0, (18, 16): 1, (19, 15): 0, (18, 17): 0, (19, 16): 0, (17, 16): 1, (17, 17): 0, (16, 16): 1, (16, 17): 1, (16, 18): 1, (16, 19): 0, (17, 18): 1, (17, 19): 0, (18, 18): 2, (18, 19): 0, (19, 18): 0, (8, 14): 1, (7, 13): 0, (8, 15): 1, (8, 16): 1, (8, 0): 1, (9, 0): 1, (10, 0): 1, (11, 0): 1, (12, 0): 1, (13, 0): 1, (14, 0): 1, (6, 4): 1, (15, 1): 0, (16, 2): 1}
    oxygenLocation = (18, 18)

    minutes = fillShipWithOxygen(shipMap, oxygenLocation)
    print(f"fillShipWithOxygen: {minutes}")



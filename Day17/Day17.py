import time
from collections import deque
import operator

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
                print("Give me:")
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

def buildMap(instructionList):
    '''
    Run Incode program that will build a map
    :param instructionList: list of instructions that will be ran
    :return:
    '''

    mapDict = {}
    i,j = 0, 0
    maxX = 0
    maxY = 0

    incodeProgram = IncodeComputer(instructionList, [] )
    map = incodeProgram.defaultRunOfProgram()
    print(f"map:{map}")

    for location in map:
        locationCoordinates = (i, j)
        if location == 46:
            location = "."
        elif location == 35:
            location = "#"
        elif location == 10:
            location = "\n"

        mapDict[locationCoordinates] = location

        if i > maxY:
            maxX = i

        if j > maxX:
            maxY = j

        j += 1
        if location == "\n":
            j = 0
            i += 1

    print(mapDict)

    return mapDict, maxX, maxY

def findCameras(shipMap, maxX, maxY):
    '''
    Find cameras in map
    :param map: map in which we try to find camera
    :param maxX: maximum X element in map
    :param maxY: maximum Y element in map
    :return:
    '''

    directions = [
                     (0, 1),
                     (0, -1),
                     (1, 0),
                     (-1, 0),
                ]
    cameraList = []

    for location, value in shipMap.items():

        neighborList = []
        if value == "#":
            for direction in directions:
                neighbor = tuple(map(operator.add, direction, location))
                neighborList.append(shipMap.get(neighbor, 0))
        if neighborList.count("#") == 4:
            cameraList.append(location)

    return cameraList

def calculateAlignment(cameraList):

    '''
    Calulcate alignment  for all of the cameras.
    :param cameraList: list of camera positions
    :return:
    '''

    alignment = 0

    for cameraLocation in cameraList:
        alignment += cameraLocation[0] * cameraLocation[1]

    return alignment

def printMap(instructionList):
    '''
    Print map to a file.
    :param instructionList:
    :return:
    '''

    incodeProgram = IncodeComputer(instructionList, [] )
    shipMap = incodeProgram.defaultRunOfProgram()
    print(shipMap)
    shipMap = ''.join(map(str, shipMap))
    print(shipMap)
    shipMap = shipMap.replace("46", ".")
    shipMap = shipMap.replace("35", "#")
    shipMap = shipMap.replace("10", "\n")

    with open("output.txt", 'w') as file:
        file.write(shipMap)

def collectDust(instructionList):
    '''
    Find how much dust robot collectes.
    :param instructionList: list of instructions that will be ran
    :return:
    '''

    #all numbers here were calculated by hand

    print("--------------------------------------------------------------------------------------------------------")

    instructionList[0] = 2
    incodeProgram = IncodeComputer(instructionList, [] )
    output = incodeProgram.defaultRunOfProgram()
    incodeProgram.outputString = ""
    print(f"output:{output}")

    inputRoutine = [65,44,65,44,67,44,66,44,67,44,66,44,67,44,66,44,67,44,65,10]
    #inputRoutine = [65, 10]

    incodeProgram.inputValues = incodeProgram.inputValues + inputRoutine
    print(f"incodeProgram.inputValues:{incodeProgram.inputValues}")
    output = incodeProgram.defaultRunOfProgram()
    print(f"output:{output}")
    incodeProgram.outputString = ""
    print(f"incodeProgram.inputValues:{incodeProgram.inputValues}")

    inputRouteA = [82, 44, 49, 48, 44, 76, 44, 49, 50, 44, 82, 44, 54, 10]
    #inputRouteA = [82, 49, 48, 44, 10]
    inputRouteB = [82, 44, 49, 48, 44, 76, 44, 49, 50, 44, 76, 44, 49, 50, 10]
    inputRouteC = [82, 44, 54, 44, 82, 44, 49, 48, 44, 82, 44, 49, 50, 44, 82, 44, 54, 10]

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    incodeProgram.inputValues = incodeProgram.inputValues + inputRouteA
    print(f"incodeProgram.inputValues:{incodeProgram.inputValues}")
    output = incodeProgram.defaultRunOfProgram()
    print(f"output:{output}")
    incodeProgram.outputString = ""
    incodeProgram.outputString = ""
    print(f"incodeProgram.inputValues:{incodeProgram.inputValues}")

    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    incodeProgram.inputValues = incodeProgram.inputValues + inputRouteB
    print(f"incodeProgram.inputValues:{incodeProgram.inputValues}")
    output = incodeProgram.defaultRunOfProgram()
    print(f"output:{output}")
    incodeProgram.outputString = ""
    print(f"incodeProgram.inputValues:{incodeProgram.inputValues}")

    print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
    incodeProgram.inputValues = incodeProgram.inputValues + inputRouteC
    print(f"incodeProgram.inputValues:{incodeProgram.inputValues}")
    output = incodeProgram.defaultRunOfProgram()
    print(f"output:{output}")
    incodeProgram.outputString = ""
    print(f"incodeProgram.inputValues:{incodeProgram.inputValues}")

    incodeProgram.inputValues = incodeProgram.inputValues + [110, 10]
    print(f"incodeProgram.inputValues:{incodeProgram.inputValues}")
    output = incodeProgram.defaultRunOfProgram()
    print(f"output:{output}")
    incodeProgram.outputString = ""
    print(f"incodeProgram.inputValues:{incodeProgram.inputValues}")

if __name__ == "__main__":

    instructionList = readInput("input.txt")
    print(f"instructionList: {instructionList}")

    #shipMap, maxX, maxY = buildMap(instructionList)
    #print(f"buildMap: {shipMap}, maxY: {maxX}, maxY:{maxY}")

    #cameraList = findCameras(shipMap, maxX - 1, maxY - 1)
    #print(f"findCameras: {cameraList}")

    #alignment  = calculateAlignment(cameraList)
    #print(f"calculateAlignment: {alignment }")

    dust  = collectDust(instructionList)
    print(f"collectDust: {dust }")

    printMap(instructionList)



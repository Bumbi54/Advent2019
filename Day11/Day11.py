import matplotlib.pyplot as plt


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
            secondRegister =  self.getElementFromMemory(self.relativeBase + self.getElementFromMemory(self.index + 2))
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
            firstRegister =  self.getElementFromMemory(self.relativeBase + self.getElementFromMemory(self.index + 1))
        else:
            firstRegister = self.getElementFromMemory(self.index + 1)

        if secondParameterMode == 0:
            secondRegister = self.getElementFromMemory(self.getElementFromMemory(self.index + 2))
        elif secondParameterMode == 2:
            secondRegister =  self.getElementFromMemory(self.relativeBase + self.getElementFromMemory(self.index + 2))
        else:
            secondRegister = self.getElementFromMemory(self.index + 2)

        return firstRegister, secondRegister

    def defaultRunOfProgram(self):
        '''
        Run the program by reading opcodes
        :param instructionList: list of program instructions
        :return:
        '''

        outputString = ''
        incrementStep = 4

        while(self.index < len(self.instructionList)):

            curentInstruction = self.instructionList[self.index]  % 100
            firstParameterMode = (self.instructionList[self.index] // 100) % 10
            secondParameterMode = (self.instructionList[self.index] // 1000) % 10
            thirdParameterMode = (self.instructionList[self.index] // 10000) % 10

            if curentInstruction == 99:
                print("Jej Break")
                self.finishedBool = True
                break
            elif curentInstruction == 1:
                incrementStep = 4
                firstRegister, secondRegister, thirdRegister = self.threeRegisterInstruction(firstParameterMode, secondParameterMode, thirdParameterMode)
                #print(f"thirdRegister: {thirdRegister}, len(self.instructionList):{len(self.instructionList)}")
                if thirdRegister >= len(self.instructionList):
                    self.outOfMemorySpace[thirdRegister] = firstRegister + secondRegister
                else:
                    self.instructionList[thirdRegister] = firstRegister + secondRegister
            elif curentInstruction == 2:
                incrementStep = 4
                firstRegister, secondRegister, thirdRegister = self.threeRegisterInstruction(firstParameterMode, secondParameterMode, thirdParameterMode)

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
                            self.outOfMemorySpace[self.relativeBase + self.getElementFromMemory(self.index + 1)] = self.inputValues .pop()
                        else:
                            self.instructionList[self.relativeBase + self.getElementFromMemory(self.index + 1)] = self.inputValues .pop()
                    else:
                        if self.getElementFromMemory(self.index + 1) > len(self.instructionList):
                            self.outOfMemorySpace[self.getElementFromMemory(self.index + 1)] = self.inputValues .pop()
                        else:
                            self.instructionList[self.getElementFromMemory(self.index + 1)] = self.inputValues .pop()

            elif curentInstruction == 4:
                incrementStep = 2

                if firstParameterMode == 0:
                    outputString += "," + str(self.getElementFromMemory(self.getElementFromMemory(self.index + 1)))
                elif firstParameterMode == 2:
                    outputString += "," + str(self.getElementFromMemory(self.relativeBase + self.getElementFromMemory(self.index + 1)))
                else:
                    outputString += "," + str(self.getElementFromMemory(self.index + 1))
                print(f"tempoutputString: {outputString}")
            elif curentInstruction == 5:
                incrementStep = 3
                firstRegister, secondRegister = self.twoRegisterInstruction(firstParameterMode, secondParameterMode)
                #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}")
                if firstRegister != 0:
                    self.index = secondRegister
                    incrementStep = 0
            elif curentInstruction == 6:
                incrementStep = 3
                firstRegister, secondRegister = self.twoRegisterInstruction(firstParameterMode, secondParameterMode)
                #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}")
                if firstRegister == 0:
                    self.index = secondRegister
                    incrementStep = 0
            elif curentInstruction == 7:
                incrementStep = 4
                firstRegister, secondRegister, thirdRegister = self.threeRegisterInstruction(firstParameterMode, secondParameterMode, thirdParameterMode)
                #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
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
                firstRegister, secondRegister, thirdRegister = self.threeRegisterInstruction(firstParameterMode, secondParameterMode, thirdParameterMode)
                #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
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
                    self.relativeBase += self.getElementFromMemory(self.getElementFromMemory(self.index + 1,))
                elif firstParameterMode == 2:
                    #self.relativeBase += self.instructionList[self.relativeBase + self.instructionList[self.index + 1]]
                    #print(self.getElementFromMemory(self.instructionList, self.relativeBase + self.getElementFromMemory(self.instructionList, self.index + 1, self.outOfMemorySpace), self.outOfMemorySpace))
                    self.relativeBase += self.getElementFromMemory(self.relativeBase + self.getElementFromMemory(self.index + 1))

                    #self.getElementFromMemory(self.instructionList, self.getElementFromMemory(self.instructionList, self.index + 1, self.outOfMemorySpace), self.outOfMemorySpace)
                else:
                    self.relativeBase += self.instructionList[self.index + 1]

            else:
                break
                print("Wrong opcodes instruction")

            self.index += incrementStep
            #print(self.instructionList)

        #print(f"outputString:{outputString}")
        #print(self.instructionList)
        return [int(value) for value in  outputString.split(",")[1:]]

def paintShip(instructionList ):
    '''
    Control robot to move in grid and paint the ship. First output from incode program give color to paint. Second parameter gives direction (left, right) for robot to move.
    Input to incode program is 0 if robot is currentlly over black color and 1 if it over white color.
    :param instructionList: list of instructions from which we will get out fro the robot
    :return:
    '''

    shipPanels = {(0, 0): 1}
    curentColor = 0
    currentPosition = (0, 0)
    currentDirection = (-1, 0)

    incodeProgram = IncodeComputer(instructionList, [])


    while not incodeProgram.finishedBool:

        if currentPosition not in shipPanels.keys():
            curentColor = 0
        else:
            curentColor = shipPanels[currentPosition]

        #incodeProgram.inputValues.append(curentColor)
        #programOutput = incodeProgram.defaultRunOfProgram()
        #print(f"resultInstuctionList: {programOutput}")

        incodeProgram.inputValues.append(curentColor)
        programOutput = incodeProgram.defaultRunOfProgram()
        print(f"incodeProgram.defaultRunOfProgram: {programOutput}")

        shipPanels[currentPosition] = programOutput[0]

        if currentDirection == (-1, 0):
            if programOutput[1] == 1:
                currentDirection = (0, 1)
            else:
                currentDirection = (0, -1)

        elif currentDirection == (1, 0):
            if programOutput[1] == 1:
                currentDirection = (0, -1)
            else:
                currentDirection = (0, 1)

        elif currentDirection == (0, 1):
            if programOutput[1] == 1:
                currentDirection = (1, 0)
            else:
                currentDirection = (-1, 0)

        elif currentDirection == (0, -1):
            if programOutput[1] == 1:
                currentDirection = (-1, 0)
            else:
                currentDirection = (1, 0)

        currentPosition = (currentPosition[0] + currentDirection[0],  currentPosition[1] + currentDirection[1])


        print(f"currentPosition: {currentPosition}, currentDirection: {currentDirection}, shipPanels:{shipPanels}")


    return shipPanels

def paint(shipPanels):
    '''
    Paint ship panels.
    :param shipPanels: dictinary representing ship panels
    :return:
    '''

    with open("output.txt", 'w') as file:

        previousX = 0
        for x in range(9):
            for y in range(50):

                coordinate = (x , y)
                if coordinate in shipPanels.keys():
                    value = shipPanels[coordinate]
                else:
                    value = "#"
                if previousX < coordinate[0]:
                    file.write("\n")
                    previousX = coordinate[0]
                if value == 0:
                    file.write(" ")
                elif value == 1:
                    file.write("1")
                else:
                    #file.write(str(shipPanels[coordinate]))
                    file.write(" ")
                #file.write(str(coordinate))

if __name__ == "__main__":

    instructionList = readInput("input.txt")
    print(f"self.instructionList: {instructionList}")

    shipPanels = paintShip(instructionList)
    print(f"paintShip: {len(shipPanels.keys())}")

    paint(shipPanels)





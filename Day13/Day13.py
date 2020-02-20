import time

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
                                self.relativeBase + self.getElementFromMemory(self.index + 1)] = self.inputValues.pop()
                        else:
                            self.instructionList[
                                self.relativeBase + self.getElementFromMemory(self.index + 1)] = self.inputValues.pop()
                    else:
                        if self.getElementFromMemory(self.index + 1) > len(self.instructionList):
                            self.outOfMemorySpace[self.getElementFromMemory(self.index + 1)] = self.inputValues.pop()
                        else:
                            self.instructionList[self.getElementFromMemory(self.index + 1)] = self.inputValues.pop()

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

def parseScreen(inscructionList):
    '''
    Go through list and parse it into diciantry that will represent screen.
    :param inscructionList: list of inscructions that will be ran
    :return:
    '''

    incodeProgram = IncodeComputer(inscructionList, [])

    output = incodeProgram.defaultRunOfProgram()
    print(output)


    screenDict = {}

    for index in range(0, len(output), 3):

        screenDict[(output[index], output[index + 1])] = output[index + 2]

    return screenDict

def playGame(inscructionList):
    '''
    Play the game
    :param inscructionList: list of inscructions that will be ran
    :return:
    '''
    print("-----------------------------------------------------------------------------------------------------------------------")
    inscructionList[0] = 2

    incodeProgram = IncodeComputer(inscructionList, [])

    ballPosition = (0, 0)
    paddlePosition = (0, 0)

    while(not incodeProgram.finishedBool):
        print("-----------------------------------------------------------------------------------------------------------------------")
        incodeProgram.outputString = ''
        output = incodeProgram.defaultRunOfProgram()
        print(f"output:{output}")

        for index in range(0, len(output), 3):

            screenDict[(output[index], output[index + 1])] = output[index + 2]

            if output[index + 2] == 4:
                ballPosition = (output[index], output[index + 1])

            if output[index + 2] == 3:
                paddlePosition = (output[index], output[index + 1])


        print(f"screenDict: {screenDict}")
        print(f"score: {screenDict[(-1, 0)]}")
        print(f"ballPosition: {ballPosition}")
        print(f"paddlePosition: {paddlePosition}")

        if paddlePosition[0] > ballPosition[0]:
            print("-1, -1")
            incodeProgram.inputValues.append(-1)
        elif paddlePosition[0] < ballPosition[0]:
            print("+1, +1")
            incodeProgram.inputValues.append(1)
        else:
            incodeProgram.inputValues.append(0)
        #time.sleep(2)

if __name__ == "__main__":

    inscructionList = readInput("input.txt")
    print(f"inscructionList: {inscructionList}")

    screenDict = parseScreen(inscructionList)
    print(f"screenDict: {screenDict}")

    print(f"Number of block tiles: {list(screenDict.values()).count(2)}")

    output = playGame(inscructionList)
    print(f"playGame: {output}")



from itertools import permutations
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


    def threeRegisterInstruction(self, firstParameterMode, secondParameterMode, thirdParameterMode, index):
        '''
        Get values of for three registers. Depending on mode. For instruction that uses three registers.
        :param instructionList: list of instructions
        :param firstParameterMode: 0 for position mode or 1 for immediate mode. For first register.
        :param secondParameterMode: 0 for position mode or 1 for immediate mode. For second register.
        :param thirdParameterMode: 0 for position mode or 1 for immediate mode. For third register.
        :param index:
        :return:
        '''

        getElementFromList = lambda list, index, offset: list[list[index + offset]]

        if firstParameterMode == 0:
            firstRegister = getElementFromList(self.instructionList, index, 1)
        else:
            firstRegister = self.instructionList[index + 1]

        if secondParameterMode == 0:
            secondRegister = getElementFromList(self.instructionList, index, 2)
        else:
            secondRegister = self.instructionList[index + 2]

        thirdRegister = self.instructionList[index + 3]

        return firstRegister, secondRegister, thirdRegister

    def twoRegisterInstruction(self, firstParameterMode, secondParameterMode, index):
        '''
        Get values of for two registers. Depending on mode. For instruction that uses three registers.
        :param instructionList: list of instructions
        :param firstParameterMode: 0 for position mode or 1 for immediate mode. For first register.
        :param secondParameterMode: 0 for position mode or 1 for immediate mode. For second register.
        :param index:
        :return:
        '''

        getElementFromList = lambda list, index, offset: list[list[index + offset]]

        if firstParameterMode == 0:
            firstRegister = getElementFromList(self.instructionList, index, 1)
        else:
            firstRegister = self.instructionList[index + 1]

        if secondParameterMode == 0:
            secondRegister = getElementFromList(self.instructionList, index, 2)
        else:
            secondRegister = self.instructionList[index + 2]

        return firstRegister, secondRegister

    def defaultRunOfProgram(self):
        '''
        Run the program by reading opcodes
        :return:
        '''

        outputString = ''
        getElementFromList = lambda list, index, offset: list[list[index + offset]]
        incrementStep = 4
        #self.index = 0

        while(self.index < len(self.instructionList)):

            curentInstruction = self.instructionList[self.index]  % 100
            firstParameterMode = (self.instructionList[self.index] // 100) % 10
            secondParameterMode = (self.instructionList[self.index] // 1000) % 10
            thirdParameterMode = (self.instructionList[self.index] // 1000) % 10

            #print(f"curentInstruction: {curentInstruction}, firstParameterMode:{firstParameterMode}, secondParameterMode:{secondParameterMode}, thirdParameterMode:{thirdParameterMode}")

            if curentInstruction == 99:
                print("Jej Break")
                self.finishedBool = True
                break
            elif curentInstruction == 1:
                incrementStep = 4
                firstRegister, secondRegister, thirdRegister = self.threeRegisterInstruction(firstParameterMode, secondParameterMode, thirdParameterMode, self.index)
                #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
                self.instructionList[thirdRegister] = firstRegister + secondRegister
            elif curentInstruction == 2:
                incrementStep = 4
                firstRegister, secondRegister, thirdRegister = self.threeRegisterInstruction(firstParameterMode, secondParameterMode, thirdParameterMode, self.index)
                #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
                self.instructionList[thirdRegister] = firstRegister * secondRegister
            elif curentInstruction == 3:
                incrementStep = 2
                #print("Input command")
                if len(self.inputValues) == 0:
                    #print("Input values is empty")
                    break
                else:
                    self.instructionList[self.instructionList[self.index + 1]] = self.inputValues.pop()

            elif curentInstruction == 4:
                incrementStep = 2
                outputString += "" + str(getElementFromList(self.instructionList, self.index, 1))
                #print(f"outputStringin line: {outputString}")
                #print(f"self.instructionList line: {self.instructionList}")

            elif curentInstruction == 5:
                incrementStep = 3
                firstRegister, secondRegister = self.twoRegisterInstruction(firstParameterMode, secondParameterMode, self.index)
                #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}")
                if firstRegister != 0:
                    self.index = secondRegister
                    incrementStep = 0
            elif curentInstruction == 6:
                incrementStep = 3
                firstRegister, secondRegister = self.twoRegisterInstruction(firstParameterMode, secondParameterMode, self.index)
                #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}")
                if firstRegister == 0:
                    self.index = secondRegister
                    incrementStep = 0
            elif curentInstruction == 7:
                incrementStep = 4
                firstRegister, secondRegister, thirdRegister = threeRegisterInstruction(self.instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, self.index)
                #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
                if firstRegister < secondRegister:
                    self.instructionList[thirdRegister] = 1
                else:
                    self.instructionList[thirdRegister] = 0
            elif curentInstruction == 8:
                incrementStep = 4
                firstRegister, secondRegister, thirdRegister = threeRegisterInstruction(self.instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, self.index)
                #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
                if firstRegister == secondRegister:
                    self.instructionList[thirdRegister] = 1
                else:
                    self.instructionList[thirdRegister] = 0
            else:
                break
                print("Wrong opcodes instruction")

            self.index += incrementStep
            #print(instructionList)

        #print(f"outputString:{outputString}")
        #print(instructionList)

        if outputString:
            return int(outputString)
        else:
            return 0

        #return int(outputString)

def findHigtest(instructionList):
    '''
    Find highest output signal
    :return:
    '''

    perm = permutations([0, 1, 2, 3, 4])

    highest = 0

    for i in list(perm):
        print(f"i: {i}")
        output = 0
        amplifierA = IncodeComputer(instructionList, [output, int(i[0])])
        amplifierB = IncodeComputer(instructionList, [output, int(i[1])])
        amplifierC = IncodeComputer(instructionList, [output, int(i[2])])
        amplifierD = IncodeComputer(instructionList, [output, int(i[3])])
        amplifierE = IncodeComputer(instructionList, [output, int(i[4])])

        amplifierA.inputValues = [output, int(i[0])]
        output = amplifierA.defaultRunOfProgram()
        amplifierB.inputValues = [output, int(i[1])]
        output = amplifierB.defaultRunOfProgram()
        amplifierC.inputValues = [output, int(i[2])]
        output = amplifierC.defaultRunOfProgram()
        amplifierD.inputValues = [output, int(i[3])]
        output = amplifierD.defaultRunOfProgram()
        amplifierE.inputValues = [output, int(i[4])]
        output = amplifierE.defaultRunOfProgram()

        #time.sleep(60)

        print(f"output: {output}")
        if highest < output:
            highest = output

    return highest

def findHigtestFeedbackLoop(instructionList):
    '''
    Find highest output signal from feedback loop
    :return:
    '''

    perm = permutations([5, 6, 7, 8, 9])

    highest = 0

    for i in list(perm):
        print(f"i: {i}")
        output = 0

        amplifierA = IncodeComputer(instructionList, [output, int(i[0])])
        amplifierB = IncodeComputer(instructionList, [output, int(i[1])])
        amplifierC = IncodeComputer(instructionList, [output, int(i[2])])
        amplifierD = IncodeComputer(instructionList, [output, int(i[3])])
        amplifierE = IncodeComputer(instructionList, [output, int(i[4])])

        amplifierA.inputValues = [output, int(i[0])]
        output = amplifierA.defaultRunOfProgram()
        amplifierB.inputValues = [output, int(i[1])]
        output = amplifierB.defaultRunOfProgram()
        amplifierC.inputValues = [output, int(i[2])]
        output = amplifierC.defaultRunOfProgram()
        amplifierD.inputValues = [output, int(i[3])]
        output = amplifierD.defaultRunOfProgram()
        amplifierE.inputValues = [output, int(i[4])]
        output = amplifierE.defaultRunOfProgram()

        print(f"output: {output}")

        while not amplifierA.finishedBool and not amplifierB.finishedBool and not amplifierC.finishedBool and not amplifierD.finishedBool and not amplifierE.finishedBool:

            #time.sleep(4)

            amplifierA.inputValues = [output]
            output = amplifierA.defaultRunOfProgram()
            print(f"outputa: {output}")
            amplifierB.inputValues = [output]
            output = amplifierB.defaultRunOfProgram()
            print(f"outputB: {output}")
            amplifierC.inputValues = [output]
            output = amplifierC.defaultRunOfProgram()
            print(f"outputC: {output}")
            amplifierD.inputValues = [output]
            output = amplifierD.defaultRunOfProgram()
            print(f"outputD: {output}")
            amplifierE.inputValues = [output]
            output = amplifierE.defaultRunOfProgram()
            print(f"outputE: {output}")

            print(f"outputTotal: {output}")
        #time.sleep(800)

        print(f"output: {output}")
        if highest < output:
            highest = output

    return highest

if __name__ == "__main__":

    instructionList = readInput("input.txt")
    print(f"instructionList: {instructionList}")

    #highestOutput = findHigtest(instructionList)
    #print(f"highestOutput: {highestOutput}")

    highestFeedbackLoopOutput = findHigtestFeedbackLoop(instructionList)
    print(f"highestFeedbackLoopOutput: {highestFeedbackLoopOutput}")





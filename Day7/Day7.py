
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


def threeRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, index):
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
        firstRegister = getElementFromList(instructionList, index, 1)
    else:
        firstRegister = instructionList[index + 1]

    if secondParameterMode == 0:
        secondRegister = getElementFromList(instructionList, index, 2)
    else:
        secondRegister = instructionList[index + 2]

    thirdRegister = instructionList[index + 3]

    return firstRegister, secondRegister, thirdRegister

def twoRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, index):
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
        firstRegister = getElementFromList(instructionList, index, 1)
    else:
        firstRegister = instructionList[index + 1]

    if secondParameterMode == 0:
        secondRegister = getElementFromList(instructionList, index, 2)
    else:
        secondRegister = instructionList[index + 2]

    return firstRegister, secondRegister

def defaultRunOfProgram(instructionList, inputValue):
    '''
    Run the program by reading opcodes
    :param instructionList: list of program instructions
    :return:
    '''

    outputString = ''
    getElementFromList = lambda list, index, offset: list[list[index + offset]]
    incrementStep = 4
    index = 0

    instructionList = instructionList[:]
    while(index < len(instructionList)):
    #for index in range(0, len(instructionList), 4):

        curentInstruction = instructionList[index]  % 100
        firstParameterMode = (instructionList[index] // 100) % 10
        secondParameterMode = (instructionList[index] // 1000) % 10
        thirdParameterMode = (instructionList[index] // 1000) % 10

        #print(f"curentInstruction: {curentInstruction}, firstParameterMode:{firstParameterMode}, secondParameterMode:{secondParameterMode}, thirdParameterMode:{thirdParameterMode}")

        if curentInstruction == 99:
            break
        elif curentInstruction == 1:
            incrementStep = 4
            firstRegister, secondRegister, thirdRegister = threeRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, index)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
            instructionList[thirdRegister] = firstRegister + secondRegister
        elif curentInstruction == 2:
            incrementStep = 4
            firstRegister, secondRegister, thirdRegister = threeRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, index)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
            instructionList[thirdRegister] = firstRegister * secondRegister
        elif curentInstruction == 3:
            incrementStep = 2
            instructionList[instructionList[index + 1]] = inputValue.pop()
            #if len(inputValue) == 2:
            #    instructionList[instructionList[index + 1]] = inputValue.pop()
            #else:
            #    instructionList[instructionList[index + 1]] = inputValue
        elif curentInstruction == 4:
            incrementStep = 2
            outputString += "" + str(getElementFromList(instructionList, index, 1))
            #print(f"outputStringin line: {outputString}")
            #print(f"self.instructionList line: {instructionList}")

        elif curentInstruction == 5:
            incrementStep = 3
            firstRegister, secondRegister = twoRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, index)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}")
            if firstRegister != 0:
                index = secondRegister
                incrementStep = 0
        elif curentInstruction == 6:
            incrementStep = 3
            firstRegister, secondRegister = twoRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, index)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}")
            if firstRegister == 0:
                index = secondRegister
                incrementStep = 0
        elif curentInstruction == 7:
            incrementStep = 4
            firstRegister, secondRegister, thirdRegister = threeRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, index)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
            if firstRegister < secondRegister:
                instructionList[thirdRegister] = 1
            else:
                instructionList[thirdRegister] = 0
        elif curentInstruction == 8:
            incrementStep = 4
            firstRegister, secondRegister, thirdRegister = threeRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, index)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
            if firstRegister == secondRegister:
                instructionList[thirdRegister] = 1
            else:
                instructionList[thirdRegister] = 0

        else:
            break
            print("Wrong opcodes instruction")

        index += incrementStep
        #print(instructionList)

    #print(f"outputString:{outputString}")
    #print(instructionList)
    return int(outputString)

def findHigtest(instructionList):
    '''
    Find highest output signal
    :return:
    '''

    perm = permutations([0, 1, 2, 3, 4])

    highest = 0

    for i in list(perm):
        print(f"i: {i}")
        output = defaultRunOfProgram(instructionList, [0, int(i[0])])
        output = defaultRunOfProgram(instructionList, [output, int(i[1])])
        output = defaultRunOfProgram(instructionList, [output, int(i[2])])
        output = defaultRunOfProgram(instructionList, [output, int(i[3])])
        output = defaultRunOfProgram(instructionList, [output, int(i[4])])

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
        while True:
            output = defaultRunOfProgram(instructionList, [output, int(i[0])])
            output = defaultRunOfProgram(instructionList, [output, int(i[1])])
            output = defaultRunOfProgram(instructionList, [output, int(i[2])])
            output = defaultRunOfProgram(instructionList, [output, int(i[3])])
            output = defaultRunOfProgram(instructionList, [output, int(i[4])])

            if output == 139629729:
                print("fhere ia ma: instructionList:{instructionList}")
                time.sleep(1520)

        print(f"output: {output}")
        if highest < output:
            highest = output

    return highest

if __name__ == "__main__":

    instructionList = readInput("input.txt")
    print(f"instructionList: {instructionList}")

    highestOutput = findHigtest(instructionList)
    print(f"highestOutput: {highestOutput}")

    #highestFeedbackLoopOutput = findHigtestFeedbackLoop(instructionList)
    #print(f"highestFeedbackLoopOutput: {highestFeedbackLoopOutput}")





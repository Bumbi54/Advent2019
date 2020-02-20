


def readInput(fileName):
    """
    Read input file and parse it into a list
    :param fileName: name of input file
    :return: list of input file content (each line is new element)
    """
    with open(fileName, 'r') as file:

        return list(map(int, file.readline().split(",")))

def getElementFromMemory(instructionList, address, outOfMemorySpace):
    '''
    This function get values from memory or certain address.
    :param instructionList: memory space
    :param address: address from which we will retrieve value
    :param outOfMemorySpace: dictionary that contains memory values that are out of initial memory scope
    :return:
    '''

    if address > len(instructionList) and address not in outOfMemorySpace.keys():
        return 0
    elif address > len(instructionList) and address in outOfMemorySpace.keys():
        return outOfMemorySpace[address]
    else:
        return instructionList[address]

def threeRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, index, relativeBase, outOfMemorySpace):
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
        firstRegister = getElementFromMemory(instructionList, getElementFromMemory(instructionList, index + 1, outOfMemorySpace), outOfMemorySpace)
        #firstRegister = getElementFromList(instructionList, index, 1)
    elif firstParameterMode == 2:
        firstRegister = getElementFromMemory(instructionList, relativeBase + getElementFromMemory(instructionList, index + 1, outOfMemorySpace), outOfMemorySpace)
        #firstRegister =  instructionList[relativeBase + instructionList[index + 1] ]
    else:
        firstRegister = getElementFromMemory(instructionList, index + 1, outOfMemorySpace)

    if secondParameterMode == 0:
        secondRegister = getElementFromMemory(instructionList, getElementFromMemory(instructionList, index + 2, outOfMemorySpace), outOfMemorySpace)
    elif secondParameterMode == 2:
        secondRegister =  getElementFromMemory(instructionList, relativeBase + getElementFromMemory(instructionList, index + 2, outOfMemorySpace), outOfMemorySpace)
    else:
        secondRegister = getElementFromMemory(instructionList, index + 2, outOfMemorySpace)

    if thirdParameterMode == 2:
        thirdRegister = relativeBase + getElementFromMemory(instructionList, index + 3, outOfMemorySpace)
    else:
        thirdRegister = getElementFromMemory(instructionList, index + 3, outOfMemorySpace)

    return firstRegister, secondRegister, thirdRegister

def twoRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, index, relativeBase, outOfMemorySpace):
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
        firstRegister = getElementFromMemory(instructionList, getElementFromMemory(instructionList, index + 1, outOfMemorySpace), outOfMemorySpace)
    elif firstParameterMode == 2:
        firstRegister =  getElementFromMemory(instructionList, relativeBase + getElementFromMemory(instructionList, index + 1, outOfMemorySpace), outOfMemorySpace)
    else:
        firstRegister = getElementFromMemory(instructionList, index + 1, outOfMemorySpace)

    if secondParameterMode == 0:
        secondRegister = getElementFromMemory(instructionList, getElementFromMemory(instructionList, index + 2, outOfMemorySpace), outOfMemorySpace)
    elif secondParameterMode == 2:
        secondRegister =  getElementFromMemory(instructionList, relativeBase + getElementFromMemory(instructionList, index + 2, outOfMemorySpace), outOfMemorySpace)
    else:
        secondRegister = getElementFromMemory(instructionList, index + 2, outOfMemorySpace)

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
    relativeBase = 0
    outOfMemorySpace = {}

    instructionList = instructionList[:]
    while(index < len(instructionList)):
    #for index in range(0, len(instructionList), 4):

        curentInstruction = instructionList[index]  % 100
        firstParameterMode = (instructionList[index] // 100) % 10
        secondParameterMode = (instructionList[index] // 1000) % 10
        thirdParameterMode = (instructionList[index] // 10000) % 10

        #print(f"curentInstruction: {curentInstruction}, firstParameterMode:{firstParameterMode}, secondParameterMode:{secondParameterMode}, thirdParameterMode:{thirdParameterMode}, index:{index}, relativeBase:{relativeBase}")
        #print(outOfMemorySpace)
        if curentInstruction == 99:
            break
        elif curentInstruction == 1:
            incrementStep = 4
            firstRegister, secondRegister, thirdRegister = threeRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, index, relativeBase, outOfMemorySpace)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
            if thirdRegister > len(instructionList):
                outOfMemorySpace[thirdRegister] = firstRegister + secondRegister
            else:
                instructionList[thirdRegister] = firstRegister + secondRegister
        elif curentInstruction == 2:
            incrementStep = 4
            firstRegister, secondRegister, thirdRegister = threeRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, index, relativeBase, outOfMemorySpace)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
            if thirdRegister > len(instructionList):
                outOfMemorySpace[thirdRegister] = firstRegister * secondRegister
            else:
                instructionList[thirdRegister] = firstRegister * secondRegister
        elif curentInstruction == 3:
            incrementStep = 2
            #print(getElementFromMemory(instructionList, index + 1, outOfMemorySpace))

            if firstParameterMode == 2:
                if relativeBase + getElementFromMemory(instructionList, index + 1, outOfMemorySpace) > len(instructionList):
                    outOfMemorySpace[relativeBase + getElementFromMemory(instructionList, index + 1, outOfMemorySpace)] = inputValue
                else:
                    instructionList[relativeBase + getElementFromMemory(instructionList, index + 1 , outOfMemorySpace)] = inputValue
            else:
                if getElementFromMemory(instructionList, index + 1, outOfMemorySpace) > len(instructionList):
                    outOfMemorySpace[getElementFromMemory(instructionList, index + 1, outOfMemorySpace)] = inputValue
                else:
                    instructionList[getElementFromMemory(instructionList, index + 1, outOfMemorySpace)] = inputValue

        elif curentInstruction == 4:
            incrementStep = 2

            if firstParameterMode == 0:
                outputString += "," + str(getElementFromMemory(instructionList, getElementFromMemory(instructionList, index + 1, outOfMemorySpace), outOfMemorySpace))
            elif firstParameterMode == 2:
                outputString += "," + str(getElementFromMemory(instructionList, relativeBase + getElementFromMemory(instructionList, index + 1, outOfMemorySpace), outOfMemorySpace))
            else:
                outputString += "," + str(getElementFromMemory(instructionList, index + 1, outOfMemorySpace))
        elif curentInstruction == 5:
            incrementStep = 3
            firstRegister, secondRegister = twoRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, index, relativeBase, outOfMemorySpace)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}")
            if firstRegister != 0:
                index = secondRegister
                incrementStep = 0
        elif curentInstruction == 6:
            incrementStep = 3
            firstRegister, secondRegister = twoRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, index, relativeBase, outOfMemorySpace)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}")
            if firstRegister == 0:
                index = secondRegister
                incrementStep = 0
        elif curentInstruction == 7:
            incrementStep = 4
            firstRegister, secondRegister, thirdRegister = threeRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, index, relativeBase, outOfMemorySpace)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
            if firstRegister < secondRegister:
                if thirdRegister > len(instructionList):
                    outOfMemorySpace[thirdRegister] = 1
                else:
                    instructionList[thirdRegister] = 1
            else:
                if thirdRegister > len(instructionList):
                    outOfMemorySpace[thirdRegister] = 0
                else:
                    instructionList[thirdRegister] = 0
        elif curentInstruction == 8:
            incrementStep = 4
            firstRegister, secondRegister, thirdRegister = threeRegisterInstruction(instructionList, firstParameterMode, secondParameterMode, thirdParameterMode, index, relativeBase, outOfMemorySpace)
            #print( f"firstRegister: {firstRegister}, secondRegister:{secondRegister}, thirdRegister:{thirdRegister}")
            if firstRegister == secondRegister:
                if thirdRegister > len(instructionList):
                    outOfMemorySpace[thirdRegister] = 1
                else:
                    instructionList[thirdRegister] = 1
            else:
                if thirdRegister > len(instructionList):
                    outOfMemorySpace[thirdRegister] = 0
                else:
                    instructionList[thirdRegister] = 0

        elif curentInstruction == 9:
            incrementStep = 2

            if firstParameterMode == 0:
                relativeBase += getElementFromMemory(instructionList, getElementFromMemory(instructionList, index + 1, outOfMemorySpace), outOfMemorySpace)
            elif firstParameterMode == 2:
                #relativeBase += instructionList[relativeBase + instructionList[index + 1]]
                #print(getElementFromMemory(instructionList, relativeBase + getElementFromMemory(instructionList, index + 1, outOfMemorySpace), outOfMemorySpace))
                relativeBase += getElementFromMemory(instructionList, relativeBase + getElementFromMemory(instructionList, index + 1, outOfMemorySpace), outOfMemorySpace)

                #getElementFromMemory(instructionList, getElementFromMemory(instructionList, index + 1, outOfMemorySpace), outOfMemorySpace)
            else:
                relativeBase += instructionList[index + 1]

        else:
            break
            print("Wrong opcodes instruction")

        index += incrementStep
        #print(instructionList)

    print(f"outputString:{outputString}")
    print(instructionList)
    return instructionList


if __name__ == "__main__":

    instructionList = readInput("input.txt")
    print(f"instructionList: {instructionList}")

    resultInstuctionList = defaultRunOfProgram(instructionList, 2)
    print(f"resultInstuctionList: {resultInstuctionList}")







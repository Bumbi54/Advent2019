


def readInput(fileName):
    """
    Read input file and parse it into a list
    :param fileName: name of input file
    :return: list of input file content (each line is new element)
    """
    with open(fileName, 'r') as file:

        return list(map(int, file.readline().split(",")))

def defaultRunOfProgram(instructionList):
    '''
    Run the program by reading opcodes
    :param instructionList: list of program instructions
    :return:
    '''

    instructionList = instructionList[:]
    for index in range(0, len(instructionList), 4):

        getElementFromList = lambda list, index, offset: list[list[index + offset]]

        if instructionList[index] == 99:
            break
        elif instructionList[index] == 1:
            instructionList[instructionList[index + 3]] = getElementFromList(instructionList, index, 1) + getElementFromList(instructionList, index, 2)
        elif instructionList[index] == 2:
            instructionList[instructionList[index + 3]] = getElementFromList(instructionList, index, 1) * getElementFromList(instructionList, index, 2)
        else:
            break
            print("Wrong opcodes instruction")

    print(instructionList)
    return instructionList

def runOfProgram1202Alarm(instructionList):
    '''
    Run the program by reading opcodes
    :param instructionList: list of program instructions
    :return:
    '''

    instructionList = instructionList[:]
    instructionList[1] = 12
    instructionList[2] = 2

    for index in range(0, len(instructionList), 4):

        getElementFromList = lambda list, index, offset: list[list[index + offset]]

        if instructionList[index] == 99:
            break
        elif instructionList[index] == 1:
            instructionList[instructionList[index + 3]] = getElementFromList(instructionList, index, 1) + getElementFromList(instructionList, index, 2)
        elif instructionList[index] == 2:
            instructionList[instructionList[index + 3]] = getElementFromList(instructionList, index, 1) * getElementFromList(instructionList, index, 2)
        else:
            break
            print("Wrong opcodes instruction")

    print(instructionList)
    return instructionList

def runOfProgram1202AlarmSpecificOutput(instructionList, output):
    '''
    Run the program by reading opcodes
    :param instructionList: list of program instructions
    :return:
    '''

    for noun in range(100):
        for verb in range(100):
            #print(f"noun: {noun}, verb:{verb}")
            instructionListTmp = instructionList[:]

            instructionListTmp[1] = noun
            instructionListTmp[2] = verb

            for index in range(0, len(instructionListTmp), 4):

                getElementFromList = lambda list, index, offset: list[list[index + offset]]

                if instructionListTmp[index] == 99:
                    break
                elif instructionListTmp[index] == 1:
                    instructionListTmp[instructionListTmp[index + 3]] = getElementFromList(instructionListTmp, index, 1) + getElementFromList(instructionListTmp, index, 2)
                elif instructionListTmp[index] == 2:
                    instructionListTmp[instructionListTmp[index + 3]] = getElementFromList(instructionListTmp, index, 1) * getElementFromList(instructionListTmp, index, 2)
                else:
                    break
                    print("Wrong opcodes instruction")

            if instructionListTmp[0] == output:

                print(instructionListTmp)
                return noun, verb, instructionListTmp


if __name__ == "__main__":

    instructionList = readInput("input.txt")
    print(f"instructionList: {instructionList}")

    resultInstuctionList = defaultRunOfProgram(instructionList)
    print(f"resultInstuctionList: {resultInstuctionList}")

    resultInstuctionList1202 = runOfProgram1202Alarm(instructionList)
    print(f"runOfProgram1202Alarm: {resultInstuctionList1202}")

    noun, verb, instructionListTmp = runOfProgram1202AlarmSpecificOutput(instructionList, 19690720)
    print(f"runOfProgram1202AlarmSpecificOutput! noun:{noun}, verb:{verb}, instructionListTmp:{instructionListTmp}")






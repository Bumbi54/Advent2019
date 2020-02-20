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
                #print("Jej Break")
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
                #print("Give me:")
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


def sendPackets(instructionList):
    """
    Set up network of 50 devices and send packet between them.
    :return:
    """

    listOfDevices = []
    deviceQue = {}
    flag = True

    for deviceIndex in range(50):
        incodeProgram = IncodeComputer(instructionList,  [deviceIndex])
        listOfDevices.append((deviceIndex ,incodeProgram))
        incodeProgram.defaultRunOfProgram()
        deviceQue[deviceIndex] = []


    while flag:

        for device in listOfDevices:

            inputValues =[-1]
            nextPacket = deviceQue[device[0]]

            if nextPacket:
                inputValues = nextPacket[:2]
                deviceQue[device[0]] = nextPacket[2:]

            device[1].inputValues = inputValues
            output = device[1].defaultRunOfProgram()
            #print(f"Device: {device[0]} output: {output}")

            for packetToSend in range(0,len(output), 3):
                if output[packetToSend] == 255:
                    flag = False
                    return (output[packetToSend + 1], output[packetToSend + 2])
                deviceQue[output[packetToSend]].append(output[packetToSend + 1] )
                deviceQue[output[packetToSend]].append(output[packetToSend + 2] )
                if output[packetToSend] == 255:
                    flag = False

            device[1].outputString = ""

def sendPacketsNat(instructionList):
    """
    Set up network of 50 devices and send packet between them.
    :return:
    """

    listOfDevices = []
    deviceQue = {}
    flag = True

    natDevice = IncodeComputer(instructionList, [255])
    natDevice.defaultRunOfProgram()
    natRegistry = []
    natHistory = set()

    for deviceIndex in range(50):
        incodeProgram = IncodeComputer(instructionList,  [deviceIndex])
        listOfDevices.append((deviceIndex ,incodeProgram))
        incodeProgram.defaultRunOfProgram()
        deviceQue[deviceIndex] = []

    while flag:

        blockInNetwork = []
        for device in listOfDevices:

            inputValues =[-1]
            nextPacket = deviceQue[device[0]]

            if nextPacket:
                inputValues = nextPacket[:2]
                deviceQue[device[0]] = nextPacket[2:]
            else:
                blockInNetwork.append(1)

            device[1].inputValues = inputValues
            output = device[1].defaultRunOfProgram()

            if not output:
                blockInNetwork.append(1)
            #print(f"Device: {device[0]} output: {output}")

            for packetToSend in range(0,len(output), 3):
                if output[packetToSend] == 255:
                    natPacket = [output[packetToSend + 1], output[packetToSend + 2]]
                    natRegistry = natPacket

                else:
                    deviceQue[output[packetToSend]].append(output[packetToSend + 1] )
                    deviceQue[output[packetToSend]].append(output[packetToSend + 2] )

            device[1].outputString = ""

        if blockInNetwork.count(1) == 100:

            if tuple(natPacket) in natHistory:
                return natPacket

            deviceQue[0] += natRegistry
            natHistory.add(tuple(natRegistry))




if __name__ == "__main__":

    instructionList = readInput("input.txt")
    print(f"instructionList: {instructionList}")

    packet = sendPackets(instructionList)
    print(f"sendPackets: {packet}")

    packet = sendPacketsNat(instructionList)
    print(f"sendPacketsNat: {packet}")


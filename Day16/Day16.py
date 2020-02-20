from itertools import cycle
import numpy as np
from operator import mul
import time


def readInput(fileName):
    """
    Read input file and parse it into a string
    :param fileName: name of input file
    :return: list of input file content (each line is new element)
    """
    with open(fileName, 'r') as file:
        fileContent = file.readlines()

    return [int(number) for number in  fileContent[0]]

def calculate(inputList, numberOfIterations):
    '''
    Calculate output after {numberOfIterations} of iterations
    '''

    repeatingPattern = [0, 1, 0, -1]
    counter = 0

    while True:
        output = []
        for index in range(len(inputList)):

            currentPatern = list(np.repeat(repeatingPattern, index + 1))
            currentPatern = (currentPatern * (len(inputList) // len(currentPatern) + 1))[1:len(inputList) + 1]

            result = sum(list(map(mul, currentPatern, inputList)))
            output.append(abs(result) % 10)

        inputList = output
        counter += 1
        #print(f"output: {output}")

        if counter == numberOfIterations:
            break

    return output

def calculatePartTwo(inputList, numberOfIterations):
    '''
    Calculate output after {numberOfIterations} of iterations
    '''

    repeatingPattern = [0, 1, 0, -1]
    counter = 0

    offset =  int("".join(map(str, inputList[:7])))

    paritalList = inputList[offset:len(inputList)]

    while True:
        output = []
        result = sum(paritalList)
        for index in range(len(paritalList)):


            #print(result)
            output.append(abs(result) % 10)
            result -= paritalList[index]

        paritalList = output
        counter += 1
        #print(f"output: {output}")
        if counter == numberOfIterations:
            break

    return output

if __name__ == "__main__":

    inputList = readInput("input.txt")
    print(f"readInput: {inputList}")

    #outputList = calculate(inputList, 100)
    #print(f"calculate: {outputList[:8]}")

    outputList = calculatePartTwo(inputList * 10000, 100 )
    print(f"calculatePartTwo: {outputList[:8]}")


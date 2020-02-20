

import time
import operator
from collections import deque, defaultdict

def readInput(fileName):
    """
    Read input file and parse it into a string
    :param fileName: name of input file
    :return: list of input file content (each line is new element)
    """
    with open(fileName, 'r') as file:
        fileContent = file.readlines()

    return fileContent

def parseInputFile(inputList):
    """
    Parse input file into coordinate system, and extract keys from it.
    """

    keyDict = {}
    doorDict = {}
    caveSystem = {}
    x = 0
    y = 0
    startPosition = (0, 0)

    for line in inputList:
        for location in line:

            if location == "@":
                startPosition = (x ,y)

            if  location != "\n":

                if "a" <= location <= "z":
                    keyDict[location] = (x, y)
                elif "A" <= location <= "Z":
                    doorDict[location] = (x, y)

                caveSystem[(x, y)] = location

            if location == "\n":
                y = 0
                x += 1
            else:
                y += 1

    return caveSystem, keyDict, doorDict, startPosition


def modifyaFile(caveSystem):

    directions = [
                (0, 1),
                (1, 0),
                (-1, 0),
                (0, -1)
                ]
    for _ in range(10000):
        for x in range(81):
            for y in range(81):

                #element = caveSystem[(x,y)]

                neighbours = []

                for direction in directions:

                     neighbours.append(caveSystem.get(tuple(map(operator.add, direction, (x,y)))))

                if neighbours.count("#") == 3 and caveSystem[(x, y)] == ".":
                    caveSystem[(x, y)] = "#"

    with open("output.txt", 'w') as file:
            for x in range(81):
                for y in range(81):
                    file.write(str(caveSystem[(x,y)]))

                    if y == 81 - 1 :
                        file.write("\n")



if __name__ == "__main__":

    inputList = readInput("input-copy.txt")
    print(f"readInput: {inputList}")

    caveSystem, keyDict, doorDict, startPosition = parseInputFile(inputList)
    print(f"parseInputFile, caveSystem:{caveSystem}, keyDict:{keyDict}, doorDict: {doorDict}, startPosition: {startPosition}")

    modifyaFile(caveSystem)
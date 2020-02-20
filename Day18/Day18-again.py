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

            if location != "#" and location != "\n":

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

class Path():

    def __init__(self, currentLocation, length ):
        self.currentLocation = currentLocation
        #self.visitedLocations = visitedLocations
        self.length  = length


def collectKeys(caveSystem, keyDict, doorDict, startPosition):
    """
    Find shortest path that find all of the keys in cave.
    """

    print(startPosition)
    caveSystem[startPosition] = "."

    directions = [
                (1, 0),
                (-1, 0),
                 (0, 1),
                (0, -1)
                ]
    resultLength = 9999999999999999999999999
    resultLength = 7440

    numberOfKEys = len(keyDict)

    queueKeys = deque()
    queueKeys.append((startPosition, '', 0 ))
    #print(queueKeys)
    visited = set()

    while queueKeys:

        positionKeys = queueKeys.pop()

        if positionKeys in visited:
            continue

        if resultLength < positionKeys[2]:
            continue

        queue = deque()
        startPath = (positionKeys[0], positionKeys[2])
        queue.append(startPath)
        keysVisisted = defaultdict(int)
        visitedLocations = {}

        while queue:

            currentPath = queue.pop()
            #print(f"currentPath: {currentPath.currentLocation}, length: {currentPath.length}, ")
            """
            for direction in directions:

                newPosition = tuple(map(operator.add, direction, currentPath.currentLocation))
                
                """
            for newPosition in [
                (currentPath[0][0] + 1, currentPath[0][1]),
                (currentPath[0][0] - 1, currentPath[0][1]),
                (currentPath[0][0], currentPath[0][1] + 1),
                (currentPath[0][0], currentPath[0][1] - 1),
            ]:

                if newPosition not in caveSystem:
                    continue

                if newPosition in visitedLocations:
                    continue

                if resultLength < currentPath[1]:
                    continue

                visitedLocations[newPosition] = currentPath[1] + 1
                newPositionValue = caveSystem.get(newPosition)
                if ("A" <= newPositionValue <= "Z" and newPositionValue.lower() not in positionKeys[1]) or newPositionValue == "#":
                    continue

                if "a" <= newPositionValue <= "z" and newPositionValue not in positionKeys[1]:
                    keysVisisted[newPositionValue] = (newPosition, currentPath[1] + 1)

                else:
                    #locations = currentPath.visitedLocations.copy()
                    #locations.add(newPosition)
                    newPath = (newPosition, currentPath[1] + 1)
                    queue.append(newPath)

        #if len(keysVisisted) == 0:
        if numberOfKEys == len(positionKeys[1]):

            resultLength = min(resultLength, positionKeys[2])
            print(f"resultLength: {resultLength}")
            continue

        visited.add(positionKeys)

        for key, value in keysVisisted.items():
            if resultLength > value[1] + 1:
                queueKeys.append((value[0], ''.join(sorted(str(positionKeys[1]) + key)),  value[1]))

        #print(keysVisisted)
    return resultLength

def collectKeys2(caveSystem, keyDict, doorDict, startPosition):
    """
    Find shortest path that find all of the keys in cave.
    """
    queue = deque()
    startPath = Path(startPosition, set([startPosition]), set(), 0)
    queue.append(startPath)
    directions = [
                (0, 1),
                (1, 0),
                (-1, 0),
                (0, -1)
                ]
    resultLength = []

    while queue:
        currentPath = queue.pop()

        for direction in directions:

            flag = True
            newPosition = tuple(map(operator.add, direction, currentPath.currentLocation))
            print(f"currentPath.currentLocation:{currentPath.currentLocation}, newPosition: {newPosition}")
            #time.sleep(1)
            if newPosition not in currentPath.visitedLocations and caveSystem.get(newPosition, "#") != "#":

                print("Am i here")
                visitedKeys = currentPath.visitedKeys.copy()
                locations = currentPath.visitedLocations.copy()

                if  "a" <= caveSystem.get(newPosition) <= "z":

                    if caveSystem.get(newPosition)  not in visitedKeys:
                        locations = set()

                    visitedKeys.add(caveSystem.get(newPosition))


                    print(len(visitedKeys),  len(keyDict.keys()))
                    if len(visitedKeys) == len(keyDict.keys()):
                        print(f"Hope: {currentPath.length + 1}")
                        resultLength.append(currentPath.length + 1)
                        flag = False


                if flag and (("A" <= caveSystem.get(newPosition) <= "Z" and caveSystem.get(newPosition).lower() in visitedKeys)
                        or caveSystem.get(newPosition) == "@" or caveSystem.get(newPosition) == "." or
                        ("a" <= caveSystem.get(newPosition) <= "z")  and caveSystem.get(newPosition) ):
                    print("Adding new to queue")
                    locations.add(newPosition)


                    newPath = Path(newPosition, locations, visitedKeys, currentPath.length + 1)
                    queue.append(newPath)

    return resultLength


if __name__ == "__main__":

    inputList = readInput("input.txt")
    print(f"readInput: {inputList}")

    caveSystem, keyDict, doorDict, startPosition = parseInputFile(inputList)
    print(f"parseInputFile, caveSystem:{caveSystem}, keyDict:{keyDict}, doorDict: {doorDict}, startPosition: {startPosition}")

    resultLength = collectKeys( caveSystem, keyDict, doorDict, startPosition)
    print(f"collectKeys: {resultLength}")
    print(f"collectKeys: {resultLength}")


import time
import operator
from collections import deque, defaultdict
import heapq
counter2 = 0

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
    startPosition = []

    for line in inputList:
        for location in line:

            if location == "@":
                startPosition.append((x ,y))

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

    caveSystem[startPosition] = "."

    directions = [
                (1, 0),
                (-1, 0),
                 (0, 1),
                (0, -1)
                ]
    resultLength = 9999999999999999999999999
    numberOfKEys = len(keyDict)

    queueKeys = deque()
    queueKeys.append((startPosition, '', 0 ))

    visited = set()
    queueKeys = [(0, startPosition, '' )]

    while queueKeys:

        positionKeys = heapq.heappop(queueKeys)
        if numberOfKEys == len(positionKeys[2]):

            resultLength = min(resultLength, positionKeys[0])
            print(f"resultLength: {resultLength}")
            break

        if (positionKeys[1],positionKeys[2]) in visited:
            continue
        visited.add((positionKeys[1], positionKeys[2]))

        queue = deque()
        startPath = (positionKeys[1], positionKeys[0])
        queue.append(startPath)
        keysVisisted = defaultdict(int)
        visitedLocations = set()

        while queue:

            currentPath = queue.popleft()
            for direction in directions:
                newPosition = tuple(map(operator.add, direction, currentPath[0]))

                if newPosition not in caveSystem:
                    continue

                if newPosition in visitedLocations:
                    continue

                visitedLocations.add(newPosition)
                newPositionValue = caveSystem.get(newPosition)
                if ("A" <= newPositionValue <= "Z" and newPositionValue.lower() not in positionKeys[2]) or newPositionValue == "#":
                    continue

                if "a" <= newPositionValue <= "z" and newPositionValue not in positionKeys[2]:
                    keysVisisted[newPositionValue] = (newPosition, currentPath[1] + 1)

                else:
                    newPath = (newPosition, currentPath[1] + 1)
                    queue.append(newPath)

        for key, value in keysVisisted.items():
                heapq.heappush(queueKeys, (value[1], value[0], ''.join(sorted(str(positionKeys[2]) + key))  ))

    return resultLength

def partTwo(caveSystem, keyDict, doorDict, startPosition):
    """
    Find shortest path that find all of the keys in cave.
    """

    directions = [
                (1, 0),
                (-1, 0),
                 (0, 1),
                (0, -1)
                ]
    resultLength = 9999999999999999999999999
    numberOfKEys = len(keyDict)

    #queueKeys = deque()
    #queueKeys.append((startPosition, '', 0 ))

    visited =  set()
    queueKeys = [(0, startPosition, '' )]
    print(queueKeys)

    while queueKeys:

        positionKeys = heapq.heappop(queueKeys)
        #print(f"positionKeys: {positionKeys}")
        if numberOfKEys == len(positionKeys[2]):

            resultLength = min(resultLength, positionKeys[0])
            print(f"resultLength: {resultLength}")
            break

        for  robot in positionKeys[1]:

            if (robot,positionKeys[2]) in visited:
                #print(visited[robotIndex])
                continue
            visited.add((robot, positionKeys[2]))

            queue = deque()
            startPath = (robot, positionKeys[0])
            queue.append(startPath)
            keysVisisted = defaultdict(int)
            visitedLocations = set()

            while queue:

                currentPath = queue.popleft()
                for direction in directions:
                    newPosition = tuple(map(operator.add, direction, currentPath[0]))

                    if newPosition not in caveSystem:
                        continue

                    if newPosition in visitedLocations:
                        continue

                    visitedLocations.add(newPosition)
                    newPositionValue = caveSystem.get(newPosition)
                    if ("A" <= newPositionValue <= "Z" and newPositionValue.lower() not in positionKeys[2]) or newPositionValue == "#":
                        continue

                    if "a" <= newPositionValue <= "z" and newPositionValue not in positionKeys[2]:
                        keysVisisted[newPositionValue] = (newPosition, currentPath[1] + 1)

                    else:
                        newPath = (newPosition, currentPath[1] + 1)
                        queue.append(newPath)

            for key, value in keysVisisted.items():

                newRobotsLocations = []
                for tempRobot in positionKeys[1]:
                    if tempRobot != robot:
                        newRobotsLocations.append(tempRobot)
                    else:
                        newRobotsLocations.append(value[0])
                #print(f"newRobotsLocations: {newRobotsLocations}")
                heapq.heappush(queueKeys, (value[1], newRobotsLocations, ''.join(sorted(str(positionKeys[2]) + key))  ))
        #time.sleep(1)
    return resultLength

if __name__ == "__main__":

    inputList = readInput("input.txt")
    print(f"readInput: {inputList}")

    caveSystem, keyDict, doorDict, startPosition = parseInputFile(inputList)
    print(f"parseInputFile, caveSystem:{caveSystem}, keyDict:{keyDict}, doorDict: {doorDict}, startPosition: {startPosition}")

    #resultLength = collectKeys( caveSystem, keyDict, doorDict, startPosition[0])
    #print(f"collectKeys: {resultLength}")

    resultLength = partTwo( caveSystem, keyDict, doorDict, startPosition)
    print(f"partTwo: {resultLength}")
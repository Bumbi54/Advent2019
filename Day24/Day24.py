import time
from collections import deque
import operator

def readInput(fileName):
    """
    Read input file and parse it into a dictinary
    :param fileName: name of input file
    :return: grid as dictionary
    """

    bugsMap = {}
    maxX = 0
    maxY = 0

    with open(fileName, 'r') as file:

        x = 0
        for line in file.readlines():

            y = 0
            for locationChar in line:

                if locationChar == ".":
                   bugsMap[(x,y)] = 0
                elif locationChar == "#":
                    bugsMap[(x, y)] = 1

                maxY = max(maxY, y)
                y += 1
            x += 1
            maxX = max(maxX, x)


    return bugsMap, maxX, maxY

def lifeCycle(bugsMap, maxX, maxY):
    """
    Simulate life cycle until map repeats.
    :param bugMap: dictionary that represent
    :param maxX: maximum value of x dimension
    :param maxY: maximum value of y dimension
    :return:
    """

    mapHistory = set()
    directions = [
                     (0, 1),
                     (0, -1),
                     (1, 0),
                     (-1, 0),
                ]
    temp = -1
    while True:
        mapAsString = ""
        bugsMapTemp = bugsMap.copy()

        for x in range(maxX):
            for y in range(maxY):
                locationValue = bugsMap[(x, y)]
                mapAsString += str(locationValue)

                neighborsList = []
                for direction in directions:
                    neighbor = tuple(map(operator.add, direction, (x, y)))
                    neighborsList.append(bugsMap.get(neighbor, -1))

                if locationValue == 1 and neighborsList.count(1) != 1:
                    bugsMapTemp[(x, y)] = 0

                if locationValue == 0 and neighborsList.count(1) in [1, 2]:
                    bugsMapTemp[(x, y)] = 1

        if mapAsString in mapHistory:
            break

        mapHistory.add(mapAsString)

        bugsMap = bugsMapTemp
        #time.sleep(1)

    counter = 1
    result = 0
    for x in range(maxX):
        stringToPrint = ""
        for y in range(maxY):
            result += counter * bugsMap[(x, y)]
            counter = counter + counter
            stringToPrint += str(bugsMap[(x, y)])
        print(stringToPrint)

    return result

def lifeCycleRecursive(bugsMap, maxX, maxY):
    """
    Simulate life cycle of bugs recursively.
    :param bugMap: dictionary that represent
    :param maxX: maximum value of x dimension
    :param maxY: maximum value of y dimension
    :return:
    """

    emptyMap = { key : 0 for key in  bugsMap.keys()}
    mapHistory = set()
    directions = [
                     (0, 1),
                     (0, -1),
                     (1, 0),
                     (-1, 0),
                ]
    mapsDict = {}

    for mapIndex in range(0, 206):
        mapsDict[mapIndex] = emptyMap.copy()

    mapsDict[103] = bugsMap

    for _ in range(200):

        bugRecursiveMapTemp = mapsDict.copy()

        for index, bugRecursiveMap in mapsDict.items():

            if index == 0 or index == 205:
                continue

            bugsMapTemp = bugRecursiveMap.copy()

            for x in range(maxX):
                for y in range(maxY):

                    if x == 2 and y == 2:
                        continue
                    locationValue = bugsMapTemp[(x, y)]

                    neighborsList = []
                    for direction in directions:
                        neighbor = tuple(map(operator.add, direction, (x, y)))
                        neighborsList.append(bugRecursiveMap.get(neighbor, -1))

                    if x ==0 and y == 0:
                        upperRecursiveMap = mapsDict[index - 1]
                        neighborsList.append(upperRecursiveMap[(1, 2)])
                        neighborsList.append(upperRecursiveMap[(2, 1)])

                    elif x == maxX - 1 and y == maxY - 1:
                        upperRecursiveMap = mapsDict[index - 1]
                        neighborsList.append(upperRecursiveMap[(2, 3)])
                        neighborsList.append(upperRecursiveMap[(3, 2)])

                    elif x == 0 and y == maxY - 1:
                        upperRecursiveMap = mapsDict[index - 1]
                        neighborsList.append(upperRecursiveMap[(1, 2)])
                        neighborsList.append(upperRecursiveMap[(2, 3)])

                    elif x == maxX - 1 and y == 0:
                        upperRecursiveMap = mapsDict[index - 1]
                        neighborsList.append(upperRecursiveMap[(2, 1)])
                        neighborsList.append(upperRecursiveMap[(3, 2)])

                    elif x ==0:
                        upperRecursiveMap = mapsDict[index - 1]
                        neighborsList.append(upperRecursiveMap[(1, 2)])

                    elif y ==0:
                        upperRecursiveMap = mapsDict[index - 1]
                        neighborsList.append(upperRecursiveMap[(2, 1)])

                    elif x == maxX - 1:
                        upperRecursiveMap = mapsDict[index - 1]
                        neighborsList.append(upperRecursiveMap[(3, 2)])

                    elif y == maxY - 1:
                        upperRecursiveMap = mapsDict[index - 1]
                        neighborsList.append(upperRecursiveMap[(2, 3)])

                    elif x == 1 and y == 2:
                        lowerRecursiveMap = mapsDict[index + 1]
                        neighborsList.append(lowerRecursiveMap[(0, 0)])
                        neighborsList.append(lowerRecursiveMap[(0, 1)])
                        neighborsList.append(lowerRecursiveMap[(0, 2)])
                        neighborsList.append(lowerRecursiveMap[(0, 3)])
                        neighborsList.append(lowerRecursiveMap[(0, 4)])

                    elif x == 3 and y == 2:
                        lowerRecursiveMap = mapsDict[index + 1]
                        neighborsList.append(lowerRecursiveMap[(4, 0)])
                        neighborsList.append(lowerRecursiveMap[(4, 1)])
                        neighborsList.append(lowerRecursiveMap[(4, 2)])
                        neighborsList.append(lowerRecursiveMap[(4, 3)])
                        neighborsList.append(lowerRecursiveMap[(4, 4)])

                    elif x == 2 and y == 1:
                        lowerRecursiveMap = mapsDict[index + 1]
                        neighborsList.append(lowerRecursiveMap[(0, 0)])
                        neighborsList.append(lowerRecursiveMap[(1, 0)])
                        neighborsList.append(lowerRecursiveMap[(2, 0)])
                        neighborsList.append(lowerRecursiveMap[(3, 0)])
                        neighborsList.append(lowerRecursiveMap[(4, 0)])

                    elif x == 2 and y == 3:
                        lowerRecursiveMap = mapsDict[index + 1]
                        neighborsList.append(lowerRecursiveMap[(0, 4)])
                        neighborsList.append(lowerRecursiveMap[(1, 4)])
                        neighborsList.append(lowerRecursiveMap[(2, 4)])
                        neighborsList.append(lowerRecursiveMap[(3, 4)])
                        neighborsList.append(lowerRecursiveMap[(4, 4)])


                    if locationValue == 1 and neighborsList.count(1) != 1:
                        bugsMapTemp[(x, y)] = 0

                    if locationValue == 0 and neighborsList.count(1) in [1, 2]:

                        bugsMapTemp[(x, y)] = 1

            bugRecursiveMapTemp[index] = bugsMapTemp

        mapsDict = bugRecursiveMapTemp

    result = 0
    for index, bugRecursiveMap in mapsDict.items():
            counter = 1
            print(f"Map index: {index}. Map value:")
            for x in range(maxX):
                stringToPrint = ""
                for y in range(maxY):
                    if x == 2 and y == 2:
                        stringToPrint += "?"
                    else:
                        if bugRecursiveMap[(x, y)] == 1:
                            result += 1

                        stringToPrint += str(bugRecursiveMap[(x, y)])
                print(stringToPrint)

    return result

if __name__ == "__main__":

    bugsMap, maxX, maxY = readInput("input.txt")
    print(f"readInput: {maxX, maxY, bugsMap}")

    #result = lifeCycle(bugsMap, maxX, maxY)
    #print(f"readInput: {result}")

    result = lifeCycleRecursive(bugsMap, maxX, maxY)
    print(f"readInput: {result}")
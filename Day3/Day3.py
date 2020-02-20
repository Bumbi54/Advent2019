
import re
import time

def readInput(fileName):
    """
    Read input file and parse it into a list
    :param fileName: name of input file
    :return: list of input file content (each line is new element)
    """
    with open(fileName, 'r') as file:

        fileContent = []
        for line in file:
            fileContent.append(line.strip().split(","))

        return fileContent

def parseWires(wiresPaths):
    '''
    Parse wires paths into a dict
    :param wiresPaths:
    :return:
    '''

    manhattanDistance = lambda firstPoint, secondPoint: abs(firstPoint[0] - secondPoint[0]) + abs(firstPoint[1] - secondPoint[1])

    coordinateList = set()
    conflictList = []
    currentLocation = (0, 0)
    for path in wiresPaths[0]:

            pathChange = (0, 0)
            result = re.search("([R,L,D,U])(\d+)", path)

            if result:
                #print(f"direction: {result.group(1)}, distance:{result.group(2)}")

                if result.group(1) == 'R':
                    pathChange = (0, 1)
                elif result.group(1) == 'L':
                    pathChange = (0, -1)
                elif result.group(1) == 'U':
                    pathChange = (-1, 0)
                elif result.group(1) == 'D':
                    pathChange = (1, 0)

                for index in range(1, int(result.group(2)) + 1):
                    currentLocation = tuple(map(sum,zip(currentLocation,pathChange)))

                    coordinateList.add(currentLocation)
            else:
                print("Wrong regular expresion")

    print(coordinateList)
    print(conflictList)

    currentLocation = (0, 0)
    for path in wiresPaths[1]:

        pathChange = (0, 0)
        result = re.search("([R,L,D,U])(\d+)", path)

        if result:
            # print(f"direction: {result.group(1)}, distance:{result.group(2)}")

            if result.group(1) == 'R':
                pathChange = (0, 1)
            elif result.group(1) == 'L':
                pathChange = (0, -1)
            elif result.group(1) == 'U':
                pathChange = (-1, 0)
            elif result.group(1) == 'D':
                pathChange = (1, 0)

            for index in range(1, int(result.group(2)) + 1):
                currentLocation = tuple(map(sum, zip(currentLocation, pathChange)))

                if currentLocation in coordinateList:
                    conflictList.append(currentLocation)
        else:
            print("Wrong regular expresion")

    print(coordinateList)
    print(conflictList)


    minimalDistanceConflict = manhattanDistance(conflictList[0], (0,0))
    for conflict in conflictList[1:]:
        distanceToZero = manhattanDistance(conflict, (0,0))

        if distanceToZero < minimalDistanceConflict:
            minimalDistanceConflict = distanceToZero

    print(f"minimalDistanceConflict: {minimalDistanceConflict}")

    return conflictList

def parseWiresSecond(wiresPaths, conflictList):
    '''
    Parse wires paths into a dict
    :param wiresPaths:
    :return:
    '''

    print("--------------------------------------------------------------------------------------------------")
    coordinateDictFirst = {}
    coordinateDictSecond = {}
    currentLocation = (0, 0)
    steps = 0
    for path in wiresPaths[0]:

            pathChange = (0, 0)
            result = re.search("([R,L,D,U])(\d+)", path)

            if result:
                #print(f"direction: {result.group(1)}, distance:{result.group(2)}")
                if result.group(1) == 'R':
                    pathChange = (0, 1)
                elif result.group(1) == 'L':
                    pathChange = (0, -1)
                elif result.group(1) == 'U':
                    pathChange = (-1, 0)
                elif result.group(1) == 'D':
                    pathChange = (1, 0)

                for index in range(1, int(result.group(2)) + 1):
                    steps += 1
                    currentLocation = tuple(map(sum,zip(currentLocation,pathChange)))
                    #print(f"currentLocation: {currentLocation}")
                    coordinateDictFirst[currentLocation] = steps

            else:
                print("Wrong regular expresion")

    print(coordinateDictFirst)
    print(conflictList)

    steps = 0
    currentLocation = (0, 0)
    for path in wiresPaths[1]:

        pathChange = (0, 0)
        result = re.search("([R,L,D,U])(\d+)", path)

        if result:
            # print(f"direction: {result.group(1)}, distance:{result.group(2)}")

            if result.group(1) == 'R':
                pathChange = (0, 1)
            elif result.group(1) == 'L':
                pathChange = (0, -1)
            elif result.group(1) == 'U':
                pathChange = (-1, 0)
            elif result.group(1) == 'D':
                pathChange = (1, 0)

            for index in range(1, int(result.group(2)) + 1):
                steps += 1
                currentLocation = tuple(map(sum, zip(currentLocation, pathChange)))
                # print(f"currentLocation: {currentLocation}")
                coordinateDictSecond[currentLocation] = steps
        else:
            print("Wrong regular expresion")

    print(coordinateDictSecond)
    print(conflictList)

    minimalDistanceToIntersection = 999999999999999999999999
    for location in conflictList:
        minimalDistanceToIntersection = min(minimalDistanceToIntersection, coordinateDictFirst[location] + coordinateDictSecond[location])


    print(f"minimalDistanceToIntersection: {minimalDistanceToIntersection}")

if __name__ == "__main__":

    wiresPaths = readInput("input.txt")
    print(f"wiresPaths: {wiresPaths}")

    conflictList = parseWires(wiresPaths)

    parseWiresSecond(wiresPaths, conflictList)




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
    Parse input file into coordinate system, and extract portals from it.
    """
    outerPortal = {}
    innerPortal = {}
    outerPortalReverse = {}
    innerPortalReverse = {}
    maze = {}
    x = 0
    y = 0
    maxY = 0

    for line in inputList:
        for location in line:

            if location != "#" and location != "\n" and location != " ":

                maze[(x, y)] = location

            if location == "\n":
                y = 0
                x += 1
            else:
                y += 1
                maxY = max(y, maxY)

    print(maze)
    print(x , maxY)
    for key, value in maze.items():
        if value.isupper():

            if key[0] in [0, x] or key[1] in [0, maxY - 1]:
                #outer portals
                if maze.get((key[0] + 1, key[1]), "0").isupper() and maze.get((key[0] + 2, key[1])) == ".":
                    outerPortal[(key[0] + 2, key[1])] = value + maze.get((key[0] + 1, key[1]))
                    outerPortalReverse[value + maze.get((key[0] + 1, key[1]))] = (key[0] + 2, key[1])
                    #del maze[(key[0], key[1])]
                    #del maze[(key[0] + 1, key[1])]

                elif maze.get((key[0], key[1] + 1), "0").isupper() and maze.get((key[0], key[1] + 2)) == ".":
                    outerPortal[(key[0], key[1] + 2)] = value + maze.get((key[0] , key[1] + 1))
                    outerPortalReverse[value + maze.get((key[0], key[1] + 1))] = (key[0], key[1] + 2)
                    #del maze[(key[0], key[1])]
                    #del maze[(key[0], key[1] + 1)]

                elif maze.get((key[0] - 1, key[1]), "0").isupper() and maze.get((key[0] - 2, key[1])) == ".":
                    outerPortal[(key[0] - 2, key[1])] =  maze.get((key[0] - 1, key[1])) + value
                    outerPortalReverse[maze.get((key[0] - 1, key[1])) + value] = (key[0] - 2, key[1])
                    #del maze[(key[0], key[1])]
                    #del maze[(key[0] - 1, key[1])]

                elif maze.get((key[0], key[1] - 1), "0").isupper() and maze.get((key[0], key[1] - 2)) == ".":
                    outerPortal[(key[0], key[1] - 2)] =  maze.get((key[0] , key[1] - 1)) + value
                    outerPortalReverse[maze.get((key[0], key[1] - 1)) + value ] = (key[0], key[1] - 2)
                    #del maze[(key[0], key[1])]
                    #del maze[(key[0], key[1] - 1)]

            else:
                # inner portals
                if maze.get((key[0] + 1, key[1]), "0").isupper() and maze.get((key[0] + 2, key[1])) == ".":
                    innerPortal[(key[0] + 2, key[1])] = value + maze.get((key[0] + 1, key[1]))
                    innerPortalReverse[value + maze.get((key[0] + 1, key[1]))] = (key[0] + 2, key[1])
                    #del maze[(key[0], key[1])]
                    #del maze[(key[0] + 1, key[1])]

                elif maze.get((key[0], key[1] + 1), "0").isupper() and maze.get((key[0], key[1] + 2)) == ".":
                    innerPortal[(key[0], key[1] + 2)] = value + maze.get((key[0], key[1] + 1))
                    innerPortalReverse[value + maze.get((key[0], key[1] + 1))] = (key[0], key[1] + 2)
                    #del maze[(key[0], key[1] )]
                    #del maze[(key[0] , key[1] + 1)]

                elif maze.get((key[0] - 1, key[1]), "0").isupper() and maze.get((key[0] - 2, key[1])) == ".":
                    innerPortal[(key[0] - 2, key[1])] =  maze.get((key[0] - 1, key[1])) + value
                    innerPortalReverse[maze.get((key[0] - 1, key[1])) + value ] = (key[0] - 2, key[1])
                    #del maze[(key[0], key[1])]
                    #del maze[(key[0] - 1, key[1])]

                elif maze.get((key[0], key[1] - 1), "0").isupper() and maze.get((key[0], key[1] - 2)) == ".":
                    innerPortal[(key[0], key[1] - 2)] = maze.get((key[0], key[1] - 1)) + value
                    innerPortalReverse[maze.get((key[0], key[1] - 1)) + value ] = (key[0], key[1] - 2)
                    #del maze[(key[0], key[1])]
                    #del maze[(key[0], key[1] - 1)]

    return maze, innerPortal, outerPortal, innerPortalReverse, outerPortalReverse

class Path():

    def __init__(self, currentLocation, length ):
        self.currentLocation = currentLocation
        #self.visitedLocations = visitedLocations
        self.length  = length


def pathInMaze(maze, innerPortal, outerPortal, innerPortalReverse, outerPortalReverse, startPosition):
    """
    Find shortest path in maze from AA to ZZ.
    """

    directions = [
                (1, 0),
                (-1, 0),
                 (0, 1),
                (0, -1)
                ]
    endPosition = outerPortalReverse["ZZ"]
    queue = deque()
    startLocation = (startPosition, 0)
    queue.append(startLocation)
    visitedLocations = set()
    visitedLocations.add(startPosition)
    result = 0
    flag = True

    while flag:

        currentLocation = queue.popleft()
        #print(f"currentLocation: {currentLocation}")

        for direction in directions:
            newPosition = tuple(map(operator.add, direction, currentLocation[0]))

            if newPosition == endPosition:
                flag = False
                result = currentLocation[1] + 1
                break

            if newPosition not in maze:
                continue

            if newPosition in visitedLocations:
                continue

            visitedLocations.add(newPosition)
            newPositionValue = maze.get(newPosition)

            if newPosition in outerPortal:
                portalPosition = innerPortalReverse[outerPortal[newPosition]]
                queue.append((portalPosition, currentLocation[1] + 2))

            elif newPosition in innerPortal:
                portalPosition = outerPortalReverse[innerPortal[newPosition]]
                queue.append((portalPosition, currentLocation[1] + 2))

            else:
                queue.append((newPosition, currentLocation[1] + 1))

    return result


def pathInMazeLayers(maze, innerPortal, outerPortal, innerPortalReverse, outerPortalReverse, startPosition):
    """
    Find shortest path in maze from AA to ZZ.
    """

    directions = [
                (1, 0),
                (-1, 0),
                 (0, 1),
                (0, -1)
                ]
    endPosition = outerPortalReverse["ZZ"]
    queue = deque()
    startLocation = (startPosition, 0, 0)
    queue.append(startLocation)
    visitedLocations = set()
    visitedLocations.add((startPosition, 0))
    result = 0
    flag = True

    while flag:

        currentLocation = queue.popleft()
        #print(f"currentLocation: {currentLocation}")

        for direction in directions:
            newPosition = tuple(map(operator.add, direction, currentLocation[0]))

            if newPosition == endPosition and currentLocation[2] == 0:
                flag = False
                result = currentLocation[1] + 1
                break
            elif newPosition == endPosition or newPosition == startPosition:
                continue

            if newPosition not in maze:
                continue

            if (newPosition, currentLocation[2]) in visitedLocations:
                continue

            visitedLocations.add((newPosition, currentLocation[2]))
            newPositionValue = maze.get(newPosition)

            if newPosition in outerPortal:
                portalPosition = innerPortalReverse[outerPortal[newPosition]]
                if currentLocation[2] != 0:
                    queue.append((portalPosition, currentLocation[1] + 2, currentLocation[2] - 1))

            elif newPosition in innerPortal:
                portalPosition = outerPortalReverse[innerPortal[newPosition]]
                queue.append((portalPosition, currentLocation[1] + 2, currentLocation[2] + 1))

            else:
                queue.append((newPosition, currentLocation[1] + 1, currentLocation[2]))

    return result


if __name__ == "__main__":

    inputList = readInput("input.txt")
    print(f"readInput: {inputList}")

    maze, innerPortal, outerPortal, innerPortalReverse, outerPortalReverse = parseInputFile(inputList)
    print(f"parseInputFile, maze:{maze},\n innerPortal:{innerPortal},\n outerPortal: {outerPortal},\n innerPortalReverse: {innerPortalReverse},\n outerPortalReverse: {outerPortalReverse}")

    #result = pathInMaze(maze, innerPortal, outerPortal, innerPortalReverse, outerPortalReverse, outerPortalReverse["AA"])
    #print(f"pathInMaze: {result}")

    result = pathInMazeLayers(maze, innerPortal, outerPortal, innerPortalReverse, outerPortalReverse, outerPortalReverse["AA"])
    print(f"pathInMaze: {result}")

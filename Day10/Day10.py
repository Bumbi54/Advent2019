
import math


def readInput(fileName):
    """
    Read input file and parse it into a list
    :param fileName: name of input file
    :return: list of input file content (each line is new element)
    """

    asteroidMatrix = []

    with open(fileName, 'r') as file:
        return file.readlines()

def parseAsteroids(asteroidMatrix):
    '''
    Parse asteroids into set as pair of coordinates.
    :param asteroidMatrix:
    :return:
    '''

    asteroidSet = set()

    for x, asteroidLine in enumerate(asteroidMatrix):
        for y, asteroid in enumerate(asteroidLine):

            if asteroid == "#":
                asteroidSet.add((x,y))

    return asteroidSet

def findSpotForMonitoring(asteroidSet):
    '''
    Find an asteroid that has most line of sight asteroids.
    :param asteroidSet:
    :return:
    '''

    maximumAsteroids = (0,0)

    print(asteroidSet)

    for x, y in asteroidSet:

        visitedAsteroids = set()

        #print(f"x:{x}, y:{y}")
        for tempX, tempY in asteroidSet:
            #print(f"tempX:{tempX},tempY:{tempY}, tempCount: {tempCount}")
            if x != tempX or y != tempY:
                if (y - tempY) == 0:
                    #print(f"Inf. tempX:{tempX},tempY:{tempY}, tempCount: {tempCount}")
                    if "inf+" not in visitedAsteroids and x > tempX:
                        visitedAsteroids.add("inf+")

                    elif "inf-" not in visitedAsteroids and x < tempX:
                        visitedAsteroids.add("inf-")

                else:
                    angle = math.atan2((x - tempX) , (y - tempY))

                    #print(f"angle: {angle}, tempX:{tempX}, tempY:{tempY}")

                    visitedAsteroids.add(str(angle))

        if len(visitedAsteroids) > maximumAsteroids[0]:
            maximumAsteroids = (len(visitedAsteroids), (x, y))

        #print(f"x, y: {x}, {y}, visitedAsteroids: {visitedAsteroids}, tempCount: {len(visitedAsteroids)}")

    return maximumAsteroids

def asteroidDestroyer(asteroidSet, stationLocation):
    '''
    Destroy asteroids in circle from a station location.
    :param asteroidSet:
    :return:
    '''

    maximumAsteroids = (0,0)

    print(f"asteroidSet: {asteroidSet}")

    x = stationLocation[0]
    y = stationLocation[1]

    visitedAsteroids = {}
    visistedAstoroidsLocations = []

    for tempX, tempY in asteroidSet:
        if x != tempX or y != tempY:
            if (y - tempY) == 0:
                if 1.5707963267948  not in visitedAsteroids.keys() and x > tempX:
                    angle = 1.5707963267948

                elif -1.5707963267948 not in visitedAsteroids.keys() and x < tempX:
                    angle = -1.5707963267948

                if (angle) not in visitedAsteroids.keys():
                    visitedAsteroids[(angle)] = ((tempX, tempY), math.hypot( x - tempX , y - tempY ))

                elif visitedAsteroids[(angle)][1] < math.hypot( x - tempX , y - tempY ):
                    visitedAsteroids[(angle)] = ((tempX, tempY), math.hypot(x - tempX, y - tempY))

            else:
                angle = math.atan2((x - tempX) , (y - tempY))

                if (angle) not in visitedAsteroids.keys():
                    visitedAsteroids[(angle)] = ((tempX, tempY), math.hypot( x - tempX , y - tempY ))

                elif visitedAsteroids[(angle)][1] < math.hypot( x - tempX , y - tempY ):
                    visitedAsteroids[(angle)] = ((tempX, tempY), math.hypot(x - tempX, y - tempY))


                    #visistedAstoroidsLocations.append((tempX, tempY))

                #visitedAsteroids.add(str(angle))

    sortedAsteroidsID = sorted(visitedAsteroids.keys())

    print(f"visitedAsteroids: {sortedAsteroidsID}")
    print(f"visitedAsteroids: {visitedAsteroids}")
    print(f"visitedAsteroids: {len(visitedAsteroids.keys())}")

    beginningIndex = 0
    for index, value in enumerate(sortedAsteroidsID):

        if value == 1.5707963267948:
            beginningIndex = index
            break

    print(f"beginningIndex: {beginningIndex}")

    twoHundred = ((beginningIndex + 200) - 1) % len(visitedAsteroids.keys())

    print(f"sortedAsteroidsID[twoHundred]: {sortedAsteroidsID[twoHundred]}")

    return visitedAsteroids[sortedAsteroidsID[twoHundred]][0][0] + visitedAsteroids[sortedAsteroidsID[twoHundred]][0][1] * 100


if __name__ == "__main__":

    asteroidMatrix = readInput("input.txt")
    print(f"asteroidMatrix: {asteroidMatrix}")

    asteroidSet = parseAsteroids(asteroidMatrix)
    print(f"parseAsteroids: {asteroidSet}")
    #print(f"parseAsteroids: {sorted(asteroidSet, key=lambda tup: tup[1])}")

    location = findSpotForMonitoring(asteroidSet)
    print(f"findSpotForMonitoring: {location}")

    twoHundred = asteroidDestroyer(asteroidSet, location[1])
    print(f"asteroidDestroyer: {twoHundred}")






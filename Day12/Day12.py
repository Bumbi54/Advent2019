import re
import time
import math

def parseInput(fileName):
    """
    Parse input file and parse it into a dictinary
    :param fileName: name of input file
    :return: list of input file content (each line is new element)
    """

    starSystem = {}
    fileList = []

    with open(fileName, 'r') as file:
        fileList = file.readlines()

    for planet in fileList:
        m = re.match(r'<x=([+-]?\d+), y=([+-]?\d+), z=([+-]?\d+)>', planet.rstrip() )
        starSystem[(int(m.group(1)), int(m.group(2)), int(m.group(3)))] = [0, 0, 0]

    return starSystem


def calculatePositions(starSystem, numberOfStep):
    '''
    Calculate position of objects for each time step. First calculate gravity and then apply  it to velocity.
    :param starSystem:
    :return:
    '''

    counter = 0
    while(counter != numberOfStep):
        for affectedMoon in starSystem:
            velocityEntry = starSystem[affectedMoon]
            #print(f"affectedMoon: {affectedMoon}")
            for moon in starSystem:
                #print(f"moon: {moon}")
                for coordinateAxi in range(3):

                    velocityAxe = affectedMoon[coordinateAxi] - moon[coordinateAxi]
                    if velocityAxe > 0:
                        velocityEntry[coordinateAxi] += -1
                    elif velocityAxe < 0:
                        velocityEntry[coordinateAxi] += +1

            starSystem[affectedMoon] = velocityEntry

        newStarSystem = {}
        #apply velocity and gravity
        for moon in starSystem:
            newStarSystem[tuple(map(sum, zip(moon, starSystem[moon])))] = starSystem[moon]

        starSystem = newStarSystem
        counter += 1

    #calculate energy
    totalEnergy = 0
    for moon in starSystem:

        totalPotentialenergy = 0
        totalKineticEnergy = 0

        for coordinate in range(3):
            totalPotentialenergy += abs(moon[coordinate])
            totalKineticEnergy += abs(starSystem[moon][coordinate])

        totalEnergy += totalPotentialenergy * totalKineticEnergy

    print(f"totalEnergy: {totalEnergy}")


def planetRepetitionOlder(starSystem):
    '''
    Find when first coordinate and velocity pair repeats itself..
    :param starSystem:
    :return:
    '''

    universeHistory = set()
    universeHistory.add(str(starSystem))
    counter = 0
    print(universeHistory)

    while(True):
        for affectedMoon in starSystem:
            velocityEntry = starSystem[affectedMoon]
            #print(f"affectedMoon: {affectedMoon}")
            for moon in starSystem:
                #print(f"moon: {moon}")
                for coordinateAxi in range(3):

                    velocityAxe = affectedMoon[coordinateAxi] - moon[coordinateAxi]
                    if velocityAxe > 0:
                        velocityEntry[coordinateAxi] += -1
                    elif velocityAxe < 0:
                        velocityEntry[coordinateAxi] += +1

            starSystem[affectedMoon] = velocityEntry

        newStarSystem = {}
        #apply velocity and gravity
        for moon in starSystem:
            newStarSystem[tuple(map(sum, zip(moon, starSystem[moon])))] = starSystem[moon]

        if  str(starSystem) in universeHistory:
            print(f"Repetition at the step: %s" % counter)
            break;

        else:
             universeHistory.add(str(starSystem))

        starSystem = newStarSystem
        counter += 1

    return counter + 1

def planetRepetitionOld(starSystem):
    '''
    Find when first coordinate and velocity pair repeats itself..
    :param starSystem:
    :return:
    '''

    universeHistory = set()
    universeHistory.add(str(starSystem))
    counter = 0
    print(universeHistory)

    while(True):
        for affectedMoon in starSystem:
            velocityEntry = starSystem[affectedMoon]
            #print(f"affectedMoon: {affectedMoon}")
            for moon in starSystem:
                #print(f"moon: {moon}")
                for coordinateAxi in range(3):

                    velocityAxe = affectedMoon[coordinateAxi] - moon[coordinateAxi]
                    if velocityAxe > 0:
                        velocityEntry[coordinateAxi] += -1
                    elif velocityAxe < 0:
                        velocityEntry[coordinateAxi] += +1

            starSystem[affectedMoon] = velocityEntry

        newStarSystem = {}
        #apply velocity and gravity
        for moon in starSystem:
            newStarSystem[tuple(map(sum, zip(moon, starSystem[moon])))] = starSystem[moon]

        if  str(starSystem) in universeHistory:
            print(f"Repetition at the step: %s" % counter)
            break;

        else:
             universeHistory.add(str(starSystem))

        starSystem = newStarSystem
        counter += 1

    return counter + 1


def planetRepetition(starSystem):
    '''
    Find when first coordinate and velocity pair repeats itself..
    :param starSystem:
    :return:
    '''

    universeHistory = []

    print(universeHistory)

    for axi in range(3):

        oneDimension = set()
        oneDimensionSystem = { (position[axi], starSystem[position][axi]) for position in  starSystem }
        originalSystemState = { (position[axi], starSystem[position][axi]) for position in  starSystem }

        #print(f"oneDimension: {oneDimension}")
        counter = 0

        while(True):

            newStarSystemTemp = set()
            counter += 1

            for affectedMoon in oneDimensionSystem:
                #print(f"affectedMoon: {affectedMoon}")
                velocityEntry = affectedMoon[1]
                for moon in oneDimensionSystem:

                    velocityAxe = affectedMoon[0] - moon[0]
                    if velocityAxe > 0:
                        velocityEntry += -1
                    elif velocityAxe < 0:
                        velocityEntry += +1

                newStarSystemTemp.add((affectedMoon[0], velocityEntry))

            #apply velocity and gravity
            newStarSystem = set()
            for moon in newStarSystemTemp:
                #print(moon)
                newEntry = (sum(moon), moon[1])
                newStarSystem.add(newEntry)

            if originalSystemState == newStarSystem:
                print(f"Repetition at the step: %s" % counter)
                print(f"oneDimensionSystem: {oneDimensionSystem}, newEntry: {newEntry}")
                break;

            oneDimensionSystem = newStarSystem

        universeHistory.append(counter)
    print(f"universeHistory: {universeHistory}")

    temp = (universeHistory[0] * universeHistory[1]) // math.gcd(universeHistory[0] , universeHistory[1])

    return  temp * universeHistory[2] // math.gcd(temp , universeHistory[2])

if __name__ == "__main__":

    starSystem = parseInput("input.txt")
    print(f"parseInput: {starSystem}")

    #energy = calculatePositions(starSystem, 1000)
    #print(f"calculatePositions: {energy}")

    repetingStep = planetRepetition(starSystem)
    print(f"planetRepetition: {repetingStep}")



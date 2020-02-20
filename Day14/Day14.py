import re
import time
import math
import copy

def parseInput(fileName):
    """
    Parse input file and parse it into a dictinary
    :param fileName: name of input file
    :return: list of input file content (each line is new element)
    """

    pipeLine = {}
    fileList = []

    with open(fileName, 'r') as file:
        fileList = file.readlines()
    print(fileList)
    for pipe in fileList:
        m = re.match(r'(.*) => (\d+) (.*)', pipe.rstrip() )
        pipeLine[ m.group(3)] = (m.group(2) ,m.group(1).split(","))

    return pipeLine

def partTwo(pipeLine):
    '''
    Calculate how much fuel is produced for 1 trillion ore.
    :param pipeLine: production pipeline
    :return:
    '''

    ores = oreToFuel(pipeLine, 1)
    tempFuelCount = 1000000000000 // ores
    while True:
        ores = oreToFuel(pipeLine, tempFuelCount)
        #print(ores)

        if ores > 1000000000000:
            break
        tempFuelCount += 3000

    print("Next while")
    while True:
        ores = oreToFuel(pipeLine, tempFuelCount)

        #print(ores)

        if ores <= 1000000000000:
            break
        tempFuelCount -= 1


    return tempFuelCount

def oreToFuel(pipeLine, fuelNeeded):
    '''
    Calculate how much ore is needed to produce {fuelNeeded} fuel.
    :param pipeLine: production pipeline
    :param oresForFuel: quantity of needed fuel
    :return:
    '''
    tempFuelMaterial = pipeLine["FUEL"][1]
    fuelMaterial = []
    leftOverMaterial = {}

    for material in tempFuelMaterial:
        temp = material.lstrip().split(" ")
        fuelMaterial.append( f"{int(temp[0]) * fuelNeeded} {temp[1]}" )

    while(len(fuelMaterial) != sum([1 for material in fuelMaterial if "ORE" in material])  ):

        newFuelMaterial = []
        for material in fuelMaterial:
            quantity, type = material.lstrip().split(" ")
            nextMaterial = pipeLine.get(type)

            if type == "ORE":
                newFuelMaterial.append(material)

            elif leftOverMaterial.get(type, 0) >= int(quantity):
                leftOverMaterial[type] =  leftOverMaterial.get(type, 0) - int(quantity)

            elif int(quantity) + leftOverMaterial.get(type, 0) <=  int(nextMaterial[0]):
                newFuelMaterial += nextMaterial[1]
                leftOverMaterial[type] =  int(nextMaterial[0]) - int(quantity) + leftOverMaterial.get(type, 0)
            else:

                difference = math.ceil((int(quantity) - leftOverMaterial.get(type, 0)) / int(nextMaterial[0]))
                leftOverMaterial[type] = difference *  int(nextMaterial[0]) + leftOverMaterial.get(type, 0) - int(quantity)

                for material in nextMaterial[1]:
                    temp = material.lstrip().split(" ")
                    temp[0] = int(temp[0])
                    newFuelMaterial.append(str(temp[0] * difference) + " " + temp[1])

        tempDict = {}
        for material in newFuelMaterial:
            temp = material.lstrip().split(" ")

            if temp[1] not in tempDict:
                tempDict[temp[1]] = int(temp[0])
            else:
                tempDict[temp[1]] += int(temp[0])

        newFuelMaterial = []
        for key,value in tempDict.items():
            newFuelMaterial.append(f"{str(value)} {str(key)}")

        fuelMaterial = copy.deepcopy(newFuelMaterial)

    return int(fuelMaterial[0].split(" ")[0])

if __name__ == "__main__":

    pipeLine = parseInput("input.txt")
    print(f"parseInput: {pipeLine}")

    ores = oreToFuel(pipeLine, 1)
    print(f"oreToFuel: {ores}")

    ores = partTwo(pipeLine)
    print(f"partTwo: {ores}")

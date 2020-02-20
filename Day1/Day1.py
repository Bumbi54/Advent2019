
import math



def readInput(fileName):
    """
    Read input file and parse it into a list
    :param fileName: name of input file
    :return: list of input file content (each line is new element)
    """
    with open(fileName, 'r') as file:

        fileContent = []
        for line in file:
            fileContent.append(line.strip())

        return fileContent

def calculateFuel(listModuleMass):
    '''
    Calculate total fuel needed for all modules
    :param listModuleMass: list of modul mass
    :return: total fuel needed
    '''

    totalFuel = 0

    for moduleMass in listModuleMass:

        #caluculate fuel for single module
        fuel = math.trunc(int(moduleMass) / 3) - 2
        #print(f"For module mass: {moduleMass}, {fuel} tons on fuel are needed.")
        totalFuel += fuel

    return totalFuel

def calculateFuelWithFuelForFuel(listModuleMass):
    '''
    Calculate total fuel needed for all modules. Include calculation of needed fuel for the fuel mass.
    :param listModuleMass: list of modul mass
    :return: total fuel needed
    '''

    totalFuel = 0

    for moduleMass in listModuleMass:

        #caluculate fuel for single module
        fuel = math.trunc(int(moduleMass) / 3) - 2
        #print(f"For module mass: {moduleMass}, {fuel} tons on fuel are needed.")
        totalFuel += fuel

        while (fuel > 0):
            #print(f"Extra fuel calculation for mass: {fuel}")
            fuel = calculateFuelForSingleMass(fuel)
            if fuel > 0:
                #print(f"Extra fuel needed: {fuel}")
                totalFuel += fuel
            #else:
            #    print("No fuel needed")

    return totalFuel

def calculateFuelForSingleMass(mass):
    '''
    Calculate fuel needed for single mass.
    :param listModuleMass: list of modul mass
    :return: total fuel needed
    '''

    #caluculate fuel for single mass
    fuel = math.trunc(int(mass) / 3) - 2
    #print(f"For mass: {mass}, {fuel} tons on fuel are needed.")
    return fuel

def calculateFuelAlt(listModuleMass):
    '''
    Calculate total fuel needed for all modules
    :param listModuleMass: list of modul mass
    :return: total fuel needed
    '''

    return  sum([ math.trunc(int(moduleMass) / 3) - 2 for  moduleMass in  listModuleMass])

def calculateFuelOp(listModuleMass):
    '''
    Calculate total fuel needed for all modules. With map function.
    :param listModuleMass: list of modul mass
    :return: total fuel needed
    '''

    return  sum( map(lambda x : math.trunc(int(x) / 3) - 2 ,listModuleMass)  )

if __name__ == "__main__":

    inputMassList = readInput("input.txt")
    print(f"inputMassList: {inputMassList}")

    totalFuel = calculateFuel(inputMassList)
    print(f"Total fuel needed: {totalFuel}")

    totalFuel = calculateFuel(inputMassList)
    print(f"Total fuel needed: {totalFuel}. Alternative calculation!")

    totalFuel = calculateFuelOp(inputMassList)
    print(f"Total fuel needed: {totalFuel}. Overpowered way!")

    totalFuel = calculateFuelWithFuelForFuel(inputMassList)
    print(f"Total fuel needed: {totalFuel}. Calculate Fuel WithFuel For Fuel!")


import re
import copy
import networkx as nx


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

def parseOrbits(localOrbitMap):
    '''
    Parse input data of oribt map into dictinary
    :param localOrbitMap: list of planet orbits
    :return:
    '''

    #dictinary represeting maps. Key is current planet. Values is tuple in which first value is parent planet and second values is total number of orbits.
    orbitDictionary = {
                        "COM" : ("",0)
                        }

    queue = copy.deepcopy(localOrbitMap)

    while len(queue):
        newQueue = []

        for planet in queue:

                result = re.search("(.+)\)(.+)", planet)

                if result:
                    if result.group(1) in orbitDictionary.keys():
                        orbitDictionary[result.group(2)] = (result.group(1), orbitDictionary[result.group(1)][1] + 1 )
                    else:
                        newQueue.append(planet)
                else:
                    print("Parsing data failed. Check input file.")

        queue = copy.deepcopy(newQueue)

    return orbitDictionary

def parseOrbitsIntoTree(localOrbitMap):
    '''
    Parse input data of oribt map into tree
    :param localOrbitMap: list of planet orbits
    :return:
    '''

    #dictinary represeting maps. Key is current planet. Values is tuple in which first value is parent planet and second values is total number of orbits.
    orbitDictionary = {
                        "COM" : ("",0)
                        }
    orbits = nx.Graph()
    orbits.add_node("COM")
    #orbits.add_edges_from([("a", "b")])

    print(f"orbits..nodes():{orbits.nodes()}")
    print(f"orbits.edges():{orbits.edges()}")
    #print(f"orbits..nodes():{orbits.nodes()}")

    queue = copy.deepcopy(localOrbitMap)

    while len(queue):
        newQueue = []

        for planet in queue:

                result = re.search("(.+)\)(.+)", planet)

                if result:
                    if result.group(1) in orbitDictionary.keys():
                        orbitDictionary[result.group(2)] = (result.group(1), orbitDictionary[result.group(1)][1] + 1 )
                        orbits.add_edges_from([(result.group(1), result.group(2))])
                    else:
                        newQueue.append(planet)
                else:
                    print("Parsing data failed. Check input file.")

        queue = copy.deepcopy(newQueue)

    print(f"orbits..nodes():{orbits.nodes()}")
    print(f"orbits.edges():{orbits.edges()}")

    return orbits


def totalNumberOfOrbits(orbitDictionary):
    '''
    Calculate total number of orbits. Both direct and indirect.
    :param orbitDictionary: dictinary that represents planets and their orbits
    :return:
    '''

    numbarOfOrbits = 0

    for planet in orbitDictionary.values():

        numbarOfOrbits += planet[1]

    return numbarOfOrbits

def shortestPath(orbitTree):
    '''
    Calculate shortest path between planets "YOU" and "SAN"
    :param orbitTree: tree that represents planets and their orbits
    :return:
    '''

    return len(nx.shortest_path(orbitTree, "YOU", "SAN")) - 3


if __name__ == "__main__":


    localOrbitMap = readInput("input.txt")
    print(f"localOrbitMap: {localOrbitMap}")


    #orbitDictionary = parseOrbits(localOrbitMap)
    #print(f"parseOrbits: {orbitDictionary}")

    #numbarOfOrbits = totalNumberOfOrbits(orbitDictionary)
    #print(f"numbarOfOrbits: {numbarOfOrbits}")

    orbitTree = parseOrbitsIntoTree(localOrbitMap)
    print(f"parseOrbitsIntoTree: {orbitTree}")

    pathLength = shortestPath(orbitTree)
    print(f"shortestPath: {pathLength}")





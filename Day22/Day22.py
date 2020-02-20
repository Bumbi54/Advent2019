import time
import re
import operator

def readInput(fileName):
    """
    Read input file and parse it into a list
    :param fileName: name of input file
    :return: list of input file content (each line is new element)
    """
    listOfActions = []
    with open(fileName, 'r') as file:

        for line in file.readlines():

            m = re.search(r'deal with increment (\d+)', line)
            if m:
                listOfActions.append(("deal with increment", int(m.group(1))))

            m = re.search(r'cut ([+-]?\d+)', line)
            if m:
                listOfActions.append(("cut", int(m.group(1))))

            m = re.search(r'deal into new stack', line)
            if m:
                listOfActions.append("deal into new stack")

    return listOfActions

def cardsShuffle(listOfActions):
    """
    Shufle a deck of card by doign action from list of actions.
    """
    size = 10007
    deckOfCards = list(range(size))
    #deckOfCards = list(range(10))
    print(f"deckOfCards: {deckOfCards}")

    for action in listOfActions:
        if action == "deal into new stack":
            deckOfCards.reverse()
        elif "cut" in action:
            deckOfCards = deckOfCards[action[1]:] + deckOfCards[:action[1]]
        elif "deal with increment" in action:
            newDeck = {}
            for iteration in range(size):
                newDeck[(action[1]*iteration) % size] = deckOfCards[iteration]
            deckOfCards = []
            for key in sorted(newDeck.keys()):
                deckOfCards.append(newDeck[key])

    return deckOfCards

def cardsShuffle2(listOfActions):
    """
    Shufle a deck of card by doign action from list of actions.
    """
    size = 119315717514047
    deckOfCards = list(range(size))
    #deckOfCards = list(range(10))
    print(f"deckOfCards: {deckOfCards}")

    for _ in range(1):

        for action in listOfActions:
            if action == "deal into new stack":
                deckOfCards.reverse()
            elif "cut" in action:
                deckOfCards = deckOfCards[action[1]:] + deckOfCards[:action[1]]
            elif "deal with increment" in action:
                newDeck = {}
                for iteration in range(size):
                    newDeck[(action[1]*iteration) % size] = deckOfCards[iteration]
                deckOfCards = []
                for key in sorted(newDeck.keys()):
                    deckOfCards.append(newDeck[key])

    return deckOfCards

if __name__ == "__main__":

    listOfActions = readInput("input.txt")
    print(f"readInput: {listOfActions}")

    result = cardsShuffle(listOfActions)
    print(f"cardsShuffle: {result}")

    for index, card in enumerate(result):
        if card == 2019:
            print(f"index of 2019: {index}")

    result2 = cardsShuffle2(listOfActions)
    print(f"cardsShuffle: {result2}")

    for index, card in enumerate(result2):
        if card == 2020:
            print(f"index of 2020: {index}")



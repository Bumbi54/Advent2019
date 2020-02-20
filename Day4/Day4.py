
from collections import Counter









def countPasswords(start, end):


    listOfPasswords = []

    for password in range(start, end):

        passwordList = list(map(int, str(password)))

        twoAdjacentDigitsFlag = False
        rightIncreaseFlag = True

        for index in range(1, len(passwordList)):
            #print(f"index:{index}")
            #print(f"passwordList[index]:{passwordList[index]}")
            #print(f"passwordList[index - 1]:{passwordList[index - 1]}")
            if passwordList[index] == passwordList[index - 1]:
                twoAdjacentDigitsFlag = True

            if passwordList[index] < passwordList[index - 1]:
                rightIncreaseFlag = False

        if twoAdjacentDigitsFlag and rightIncreaseFlag:
            listOfPasswords.append(password)

    print(f"listOfPasswords:{listOfPasswords}")
    print(f"len(listOfPasswords):{len(listOfPasswords)}")


def countPasswordsSecond(start, end):

    listOfPasswords = []

    for password in range(start, end):

        passwordList = list(map(int, str(password)))

        twoAdjacentDigitsFlag = False
        rightIncreaseFlag = True

        for index in range(1, len(passwordList)):
            #print(f"index:{index}")
            #print(f"passwordList[index]:{passwordList[index]}")
            #print(f"passwordList[index - 1]:{passwordList[index - 1]}")
            if passwordList[index] == passwordList[index - 1]:
                twoAdjacentDigitsFlag = True

            if passwordList[index] < passwordList[index - 1]:
                rightIncreaseFlag = False

        if twoAdjacentDigitsFlag and rightIncreaseFlag and 2 in Counter(passwordList).values():
            listOfPasswords.append(password)

    print(f"listOfPasswords:{listOfPasswords}")
    print(f"len(listOfPasswords):{len(listOfPasswords)}")






if __name__ == "__main__":

    countPasswordsSecond(387638, 919123)
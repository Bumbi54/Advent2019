
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
            fileContent.append(line.strip())

        return fileContent


def parseImage(imageString):
    '''
    Parse image in layers
    :param imageString: unparsed string representation of string
    :return:
    '''

    imageLayers = []
    layer = 0
    counter = 0

    while layer < len(imageString):

        layerMatrix = []

        for i in range(6):
            oneDimensionLayer = []
            for j in range (25):

                oneDimensionLayer.append(imageString[counter])
                #print(i, j, counter, imageString[counter], layerMatrix, oneDimensionLayer)
                counter += 1

            layerMatrix.append(oneDimensionLayer)

        #print(f"layerMatrix: {layerMatrix}")
        imageLayers.append(layerMatrix)
        layer += 25 * 6


    return imageLayers


def findZeroLayer(imageLayers):
    '''
    Find Layer with smallest number of 0
    :param imageLayers: image parsed into layers
    :return:
    '''

    minLayer = (0, 99999999)

    for layer in imageLayers:

        #print(layer)
        tempCount = sum( dimension.count('0') for dimension in layer )

        if minLayer[1] > tempCount:
            minLayer = (layer, tempCount)


    print(minLayer)
    return sum( dimension.count('1') for dimension in minLayer[0] ) * sum( dimension.count('2') for dimension in minLayer[0] )


def decodePictureparsedImageList(parsedImageList):
    '''
    Decode picture. Get color for each pixel by stacking layers.
    :param parsedImageList: parsed image into 2D array where first dimension is layer
    :return:
    '''


    parsedImageToColor = []

    for i in range(6):
        for j in range(25):

            color = '2'
            for layerIndex in range(len(parsedImageList)):

                if parsedImageList[layerIndex][i][j] != '2':
                    #print(i,j, parsedImageList[layerIndex][i][j])
                    color = parsedImageList[layerIndex][i][j]
                    break

            parsedImageToColor.append(color)
    print(parsedImageToColor)
    print(len(parsedImageToColor))

    with open("output.txt", 'w') as file:

        for index, pixel in enumerate(parsedImageToColor):

            if index % 25 == 0:
                file.write("\n")

            if pixel == '0':
                file.write(" ")
            else:
                file.write(pixel)






if __name__ == "__main__":


    imageString = readInput("input.txt")
    print(f"imageString: {imageString}")

    parsedImageList = parseImage(imageString[0])
    print(f"parsedImageList: {parsedImageList}")

    result = findZeroLayer(parsedImageList)
    print(f"findZeroLayer: {result}")

    result = decodePictureparsedImageList(parsedImageList)
    print(f"decodePictureparsedImageList: {result}")



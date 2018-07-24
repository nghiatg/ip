from PIL import Image
import numpy as np
from src import utils
import math
import time
from scipy import ndimage


def readImage(inputPath):
    return Image.open(inputPath)


# too slow
def savePixelGrayValueToMatrixSlow(img):
    rgbMatrix = np.array(img)
    rs = np.apply_along_axis(convertToGrayValue, 2, rgbMatrix)
    return rs


def savePixelGrayValueToMatrix(img):
    rgbMatrix = np.array(img)
    matrix1 = rgbMatrix[:, :, 0] * 0.299
    matrix2 = rgbMatrix[:, :, 1] * 0.587
    matrix3 = rgbMatrix[:, :, 2] * 0.114
    return matrix1 + matrix2 + matrix3


def smoothingMaxMin(grayMatrix, margin):
    count = 0
    rs = np.empty(grayMatrix.shape)
    height = grayMatrix.shape[0]
    width = grayMatrix.shape[1]
    for y in range(height):
        for x in range(width):
            value = grayMatrix[y][x]
            grayMatrix[y][x] = grayMatrix[y][x - 1] if x > 0 else grayMatrix[y][x + 1]
            max = np.max(grayMatrix[y - margin if y >= margin else 0: y + margin + 1,
                         x - margin if x >= margin else 0: x + margin + 1])
            min = np.min(grayMatrix[y - margin if y >= margin else 0: y + margin + 1,
                         x - margin if x >= margin else 0: x + margin + 1])

            if (value > max):
                count += 1
                grayMatrix[y][x] = max
            elif (value < min):
                count += 1
                grayMatrix[y][x] = min
            else:
                grayMatrix[y][x] = value

            # if(value > max):
            #     count += 1
            #     rs[y][x] = max
            # elif (value < min):
            #     count += 1
            #     rs[y][x] = min
            # else:
            #     rs[y][x] = value
            # grayMatrix[y][x] = value
    print("count : " + str(count))
    # return rs


def convertToGrayValue(rgbValue):
    return (0.299 * rgbValue[0] + 0.587 * rgbValue[1] + 0.114 * rgbValue[2])


def writeImage(mode, size, outputPath):
    newImg = Image.new(mode, size)
    newImg.save(outputPath)


def changeImageToGray(input, output):
    img = readImage(input)
    # pix = img.load()
    grayMatrix = savePixelGrayValueToMatrix(img)
    imgMatrix = np.transpose(np.array([grayMatrix, grayMatrix, grayMatrix]), (1, 2, 0))
    imgRS = Image.fromarray(imgMatrix.astype('uint8'))
    # imgRS.show()
    imgRS.save(output)


def smoothingAvg(grayMatrix, margin):
    start = time.clock()
    width = grayMatrix.shape[1]
    height = grayMatrix.shape[0]
    
    # create sum matrix
    biggerMatrix = utils.saveToBiggerMatrix(grayMatrix, margin)
    sum_Y_Matrix = np.zeros((height, width + margin * 2))
    for y in range(margin, biggerMatrix.shape[0] - margin):
        for i in range(y - margin, y + margin + 1):
            sum_Y_Matrix[y - margin, :] += biggerMatrix[i, :]
    sumMatrix = np.zeros(grayMatrix.shape)
    for x in range(margin, biggerMatrix.shape[1] - margin):
        for i in range(x - margin, x + margin + 1):
            sumMatrix[:, x - margin] += sum_Y_Matrix[:, i]
            
    # create neighbor-count matrix
    onesMatrix = np.ones(grayMatrix.shape)
    biggerMatrix = utils.saveToBiggerMatrix(onesMatrix, margin)
    sum_Y_Matrix_Count = np.zeros((height, width + margin * 2))
    for y in range(margin, biggerMatrix.shape[0] - margin):
        for i in range(y - margin, y + margin + 1):
            sum_Y_Matrix_Count[y - margin, :] += biggerMatrix[i, :]
    sumMatrixCount = np.zeros(grayMatrix.shape)
    for x in range(margin, biggerMatrix.shape[1] - margin):
        for i in range(x - margin, x + margin + 1):
            sumMatrixCount[:, x - margin] += sum_Y_Matrix_Count[:, i]
    rs = np.floor(sumMatrix / sumMatrixCount)
    return rs


def sharpen(grayMatrix, howSharp):
    kernel = np.zeros((3, 3))
    kernel.fill(-1 * howSharp / 9)
    kernel[1][1] = howSharp
    return utils.convolve(grayMatrix, kernel)


def smoothingAvgFromScipy(grayMatrix, margin):
    return ndimage.generic_filter(grayMatrix, np.nanmean, size=2 * margin + 1, mode='constant', cval=np.NaN)

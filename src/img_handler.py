from PIL import Image
import numpy as np
from src import utils
import math

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


def smoothingAvg(grayMatrix, margin):
    height = grayMatrix.shape[0]
    width = grayMatrix.shape[1]
    for y in range(height):
        for x in range(width):
            grayMatrix[y][x] = grayMatrix[y][x - 1] if x > 0 else grayMatrix[y][x + 1]
            grayMatrix[y][x] = np.average(grayMatrix[y - margin if y >= margin else 0: y + margin + 1,
                                          x - margin if x >= margin else 0: x + margin + 1])
    return grayMatrix


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

def smoothingAvg2(grayMatrix,margin):
    width = grayMatrix.shape[1]
    height = grayMatrix.shape[0]
    biggerMatrix = utils.saveToBiggerMatrix(grayMatrix,margin)
    # print(biggerMatrix)
    sum_Y_Matrix = np.zeros((height, width + margin*2))
    for y in range(margin,biggerMatrix.shape[0]-margin):
        for i in range(y - margin, y + margin + 1):
            sum_Y_Matrix[y-margin,:] += biggerMatrix[i,:]
    sumMatrix = np.zeros(grayMatrix.shape)
    for x in range(margin,biggerMatrix.shape[1]-margin):
        for i in range(x - margin, x + margin + 1):
            # print(sumMatrix[:,x-margin])
            # print(biggerMatrix[:,i])
            sumMatrix[:,x-margin] += sum_Y_Matrix[:,i]
    rs = np.empty(grayMatrix.shape)
    for y in range(height):
        for x in range(width):
            top = y - margin if y >= margin else 0
            bottom = y + margin if y + margin < height else height - 1
            left = x - margin if x >= margin else 0
            right = x + margin if x + margin < width else width  - 1
            numberOfNearPixels = (bottom - top + 1) * (right - left + 1)
            rs[y][x] = np.round(sumMatrix[y][x]/numberOfNearPixels)
    return rs

def sharpen(grayMatrix, howSharp):
    kernel = np.zeros((3,3))
    kernel.fill(-1 * howSharp / 8)
    kernel[1][1] = howSharp
    return utils.convolve(grayMatrix,kernel)





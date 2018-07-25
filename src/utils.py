import numpy as np
import math
def from2dTo1d(yIndex, xIndex, width):
    return yIndex * width + xIndex


# [y,x]
def from1dTo2d(id, width):
    rs = np.empty((1, 2))
    rs[0][0] = int(math.floor(id / width))
    rs[0][1] = int(id % width)
    return rs


def saveToBiggerMatrix(data_matrix, margin):
    rs = np.zeros(shape=(data_matrix.shape[0] + margin * 2, data_matrix.shape[1] + margin * 2))
    rs[margin:rs.shape[0] - margin, margin:rs.shape[1] - margin] = data_matrix
    return rs


def convolve(theMatrix, kernel):
    mWidth = theMatrix.shape[1]
    mHeight = theMatrix.shape[0]
    kWidth = kernel.shape[1]
    kHeight = kernel.shape[0]
    margin = math.floor(kWidth / 2)
    biggerMatrix = saveToBiggerMatrix(theMatrix,margin)
    rs = np.zeros((mHeight,mWidth))
    for yM in range(mHeight):
        for yK in range(kHeight):
            rs[yM,:] += np.convolve(biggerMatrix[yM+yK,:],np.flipud(kernel[yK,:]),'valid')
    return rs


# derection in degrees
# output : [a,b] --> y = ax + b , x = (y-b)/a
def getGraph(currentPoint, direction):
    ab = np.empty((1,2))
    ab[0][0] = math.tan(math.radians(direction))
    ab[0][1] = currentPoint[0][0] + 0.5 - (currentPoint[0][1] + 0.5) * ab[0][0]
    return ab


# all is 2D
# direction is degrees

def getSgn(matrix):
    return (np.sign(np.sign(matrix) + 1) * 2 - 1)

def rejectNotExpendablePoints(points , width):
    count = 0;
    rs = []
    for id in points:
        count = 0
        if(id - width in points):
            count += 1
        if (id - width - 1 in points):
            count += 1
        if (id - width + 1 in points):
            count += 1
        if (id - 1 in points):
            count += 1
        if (id - 1 in points):
            count += 1
        if (id + width in points):
            count += 1
        if (id + width - 1 in points):
            count += 1
        if (id + width + 1 in points):
            count += 1
        if(count >= 2):
            rs.append(id)
    return rs

def oppositeDirection(direction1, direction2, acceptableDiff):
    return direction1 * -1 - acceptableDiff <= direction2 <= direction1 * -1 + acceptableDiff
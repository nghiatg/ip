from builtins import print

import numpy as np
import math
from src import utils
from time import clock


small_threshold = 0
big_threshold = 10
np.set_printoptions(threshold=np.inf)
# execute 2 tiems for 2 direction
def swt(edgePoints, dirMatrix):

    # list of strokeWidth
    sws = []
    
    height = dirMatrix.shape[0]
    width = dirMatrix.shape[1]
    swtMatrix = np.empty(dirMatrix.shape)
    swtMatrix.fill(100)
    edgePoints2D = np.empty((len(edgePoints),2))
    edgeMatrix = np.zeros(dirMatrix.shape)
    for i in range(len(edgePoints)):
        point = utils.from1dTo2d(edgePoints[i],width)
        edgeMatrix[int(point[0][0])][int(point[0][1])] = 1
        edgePoints2D[i] = utils.from1dTo2d(edgePoints[i],width)
    # first phase
    # first time
    for i in range(edgePoints2D.shape[0]):
        currentPoint = np.array([[edgePoints2D[i][0], edgePoints2D[i][1]]])
        gradientDirection = dirMatrix[int(edgePoints2D[i][0])][int(edgePoints2D[i][1])]     # also stroke-width direction
        strokeWidth = findStrokeWidthInDirection(currentPoint, edgeMatrix, gradientDirection, dirMatrix)
        # print("\n\n\n")
        # print(currentPoint)
        # print(str(gradientDirection))
        # print(strokeWidth)

        if strokeWidth.shape[0] < 2:
            continue
        sws.append(strokeWidth)

        for y in range(strokeWidth.shape[0]):
            if (swtMatrix[int(strokeWidth[y][0])][int(strokeWidth[y][1])] > strokeWidth.shape[0]):
                swtMatrix[int(strokeWidth[y][0])][int(strokeWidth[y][1])] = strokeWidth.shape[0]
                
    # second time
    for i in range(edgePoints2D.shape[0]):
        currentPoint = np.array([[edgePoints2D[i][0], edgePoints2D[i][1]]])
        gradientDirection = dirMatrix[int(edgePoints2D[i][0])][int(edgePoints2D[i][1])] - 180  # also stroke-width direction
        strokeWidth = findStrokeWidthInDirection(currentPoint, edgeMatrix, gradientDirection, dirMatrix)
        if strokeWidth.shape[0] == 0:
            continue
        sws.append(strokeWidth)
        for y in range(strokeWidth.shape[0]):
            if (swtMatrix[int(strokeWidth[y][0])][int(strokeWidth[y][1])] > strokeWidth.shape[0]):
                swtMatrix[int(strokeWidth[y][0])][int(strokeWidth[y][1])] = strokeWidth.shape[0]
                
    # second phase
    # for sw in sws:
    #     if sw.shape[0] == 0:
    #         continue
    #     for i in range(sw.shape[0]):
    #         if (swtMatrix[int(sw[i][0])][int(sw[i][1])] > sw.shape[0]):
    #             swtMatrix[int(sw[i][0])][int(sw[i][1])] = sw.shape[0]

    return swtMatrix

def findStrokeWidthInDirection(currentPoint, edgeMatrix, direction, dirMatrix):
    print("\n\n")
    print(currentPoint)
    # time = clock()
    strokeWidth = currentPoint.copy()
    incrementX = math.cos(math.radians(direction))
    incrementY = math.sin(math.radians(direction))
    oldX = currentPoint[0][1]
    oldY = currentPoint[0][0]
    newX = oldX
    newY = oldY
    # print(clock()-time)
    # time1=clock()
    while True:
        # print("\t"+str(clock()-time1))
        # time1=clock()
        # print("\n")
        # time1 = clock()
        while math.floor(newX) == oldX and math.floor(newY) == oldY:
            newX = newX + incrementX
            newY = newY + incrementY
        newX = math.floor(newX)
        newY = math.floor(newY)
        # print(clock() - time1)
        # time2 = clock()

        if newX >= dirMatrix.shape[1] or newX < 0 or newY <0 or newY >= dirMatrix.shape[0]:
            break
        oldX = newX
        oldY = newY
        nextPoint = np.array([[newY,newX]])
        # print(clock() - time2)
        # time3 = clock()
        strokeWidth = np.append(strokeWidth,nextPoint,0)
        # print(clock() - time3)
        # time4 = clock()

        if edgeMatrix[int(newY)][int(newX)] == 0:
            # print(clock() - time4)
            continue
        # print(clock() - time4)
        # time5 = clock()
        directionNextPoint = dirMatrix[newY][newX]
        # print(clock() - time5)
        # time6 = clock()
        if not utils.similarDirection(direction,directionNextPoint,30):
            strokeWidth = np.zeros((0,0))
        # print(clock() - time6)

        break
    # print("rs")
    # print(strokeWidth)
    # print(clock() - time1)
    # print(clock() - time)
    print(strokeWidth.shape[0])
    return strokeWidth



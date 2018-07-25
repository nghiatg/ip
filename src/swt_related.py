from builtins import print

import numpy as np
import math
from src import utils
from time import clock


small_threshold = 0
big_threshold = 15
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
    # print(edgePoints2D)
    # listEdgePoints = edgePoints2D.tolist()

    # print(dirMatrix[1,:])

    # print(type(dirMatrix))
    # print(dirMatrix.shape)
    #
    # print(edgePoints2D[1][0])
    # print(edgePoints2D[1][1])
    # print(dirMatrix[0.0][0.0])
    
    # first phase    
    # first time
    for i in range(edgePoints2D.shape[0]):
        currentPoint = np.array([[edgePoints2D[i][0], edgePoints2D[i][1]]])
        gradientDirection = dirMatrix[int(edgePoints2D[i][0])][int(edgePoints2D[i][1])]     # also stroke-width direction
        strokeWidth = findStrokeWidthInDirectionNew(currentPoint,edgeMatrix,gradientDirection,dirMatrix)
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
        strokeWidth = findStrokeWidthInDirectionNew(currentPoint, edgeMatrix, gradientDirection, dirMatrix)
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



# return list of ndarray((x,2)) of points (2D) in the strokeWidth
#  edgePoints is a list
def findStrokeWidthInDirection(currentPoint, edgePoints, direction, dirMatrix):
    # print(edgePoints)
    # print("\n\n\n")
    # print(currentPoint)
    # print(direction)
    strokeWidth = currentPoint.copy()
    ab = utils.getGraph(currentPoint,direction)
    # print(ab)
    # nextPoint = np.empty((1,2))
    # nextPoint.fill(-1)
    consideringY = int(currentPoint[0][0])
    oldX = int(currentPoint[0][1])


    if(direction == 0):
        for runX in range(oldX + 1, dirMatrix.shape[1]):
            nextPoint = np.array([[consideringY,runX]])
            strokeWidth = np.append(strokeWidth,nextPoint,axis=0)
            # print(nextPoint)
            # print(nextPoint in edgePoints)
            if nextPoint.tolist()[0] in edgePoints:
                # print(True)
                directionOfConsideringPoint = dirMatrix[int(nextPoint[0][0])][int(nextPoint[0][1])]
                if (direction * -1 - 30 > directionOfConsideringPoint or direction * -1 + 30 < directionOfConsideringPoint):
                    strokeWidth = np.zeros((0,0))
                break
            else:
                print("nope")
        return strokeWidth
    elif(direction == 180 or direction == -180) :
        for runX in range(oldX-1,-1,-1):
            nextPoint = np.array([[consideringY,runX]])
            # print(nextPoint)
            # print(nextPoint in edgePoints)
            strokeWidth = np.append(strokeWidth,nextPoint,axis=0)
            if nextPoint.tolist()[0] in edgePoints:
                directionOfConsideringPoint = dirMatrix[int(nextPoint[0][0])][int(nextPoint[0][1])]
                if (direction * -1 - 30 > directionOfConsideringPoint or direction * -1 + 30 < directionOfConsideringPoint):
                    strokeWidth = np.zeros((0, 0))
                break
            else:
                print("nope")
        return strokeWidth
    elif(direction < 0):
        stop = False
        while not stop:
            consideringY -= 1
            if consideringY < 0:
                return strokeWidth
            consideringX = int(math.floor((consideringY + 0.5 - ab[0][1]) / ab[0][0]))
            if consideringX == oldX:
                nextPoint = np.array([[consideringY,consideringX]])
                strokeWidth = np.append(strokeWidth, nextPoint, axis=0)
                directionOfNextPoint = dirMatrix[consideringY][consideringX]
                if nextPoint.tolist()[0] in edgePoints:
                    stop = True
                    if direction * -1 - 30 > directionOfNextPoint or direction * -1 + 30 < directionOfNextPoint:
                        strokeWidth = np.zeros((0, 0))
                    continue
            for runX in range(oldX if consideringX > oldX else consideringX, consideringX if consideringX > oldX else oldX):
                if runX < 0 or runX >= dirMatrix.shape[1]:
                    # strokeWidth = np.zeros((0, 0))
                    stop = True
                    break
                nextPoint = np.array([[consideringY-1, runX]])
                directionOfNextPoint = dirMatrix[consideringY-1][runX]
                strokeWidth = np.append(strokeWidth,nextPoint,axis=0)
                if nextPoint.tolist()[0] in edgePoints:
                    stop = True
                    if direction * -1 -30 > directionOfNextPoint or direction * -1 +30 < directionOfNextPoint:
                        strokeWidth = np.zeros((0,0))
                    break
            if stop == False:
                if consideringX < 0 or consideringX >= dirMatrix.shape[1]:
                    # strokeWidth = np.zeros((0, 0))
                    stop = True
                else:
                    nextPoint = np.array([[consideringY, consideringX]])
                    directionOfNextPoint = dirMatrix[consideringY][consideringX]
                    strokeWidth = np.append(strokeWidth, nextPoint, axis=0)
                    if nextPoint.tolist()[0] in edgePoints:
                        stop = True
                        if direction * -1 - 30 > directionOfNextPoint or direction * -1 + 30 < directionOfNextPoint:
                            strokeWidth = np.zeros((0, 0))
            oldX = consideringX
        return strokeWidth

    elif(direction > 0):
        stop = False
        while not stop:
            # print('----------')
            # print(strokeWidth)
            consideringY += 1
            if consideringY >= dirMatrix.shape[1]:
                return strokeWidth
            consideringX = int(math.floor((consideringY + 0.5 - ab[0][1]) / ab[0][0]))
            # print(consideringY)
            # print(consideringX)
            if consideringX == oldX:
                nextPoint = np.array([[consideringY, consideringX]])
                strokeWidth = np.append(strokeWidth, nextPoint, axis=0)
                directionOfNextPoint = dirMatrix[consideringY][consideringX]
                if nextPoint.tolist()[0] in edgePoints:
                    # print("\t\t" + str(nextPoint))
                    stop = True
                    if direction * -1 - 30 > directionOfNextPoint or direction * -1 + 30 < directionOfNextPoint:
                        # print("here")
                        # print(nextPoint)
                        # print(nextPoint in edgePoints)
                        # print(np.where(edgePoints == nextPoint))
                        # print(direction)
                        # print(directionOfNextPoint)
                        strokeWidth = np.zeros((0, 0))
                    continue
            for runX in range(oldX if consideringX > oldX else consideringX, consideringX if consideringX > oldX else oldX):
                if runX < 0 or runX >= dirMatrix.shape[1]:
                    # strokeWidth = np.zeros((0, 0))
                    stop = True
                    break
                nextPoint = np.array([[consideringY - 1, runX]])
                directionOfNextPoint = dirMatrix[consideringY - 1][runX]
                strokeWidth = np.append(strokeWidth, nextPoint, axis=0)
                if nextPoint.tolist()[0] in edgePoints:
                    stop = True
                    if direction * -1 - 30 > directionOfNextPoint or direction * -1 + 30 < directionOfNextPoint:
                        strokeWidth = np.zeros((0, 0))
                    break
            if stop == False:
                if consideringX < 0 or consideringX >= dirMatrix.shape[1]:
                    # strokeWidth = np.zeros((0, 0))
                    stop = True
                else:
                    nextPoint = np.array([[consideringY, consideringX]])
                    directionOfNextPoint = dirMatrix[consideringY][consideringX]
                    strokeWidth = np.append(strokeWidth, nextPoint, axis=0)
                    if nextPoint.tolist()[0] in edgePoints:
                        stop = True
                        if direction * -1 - 30 > directionOfNextPoint or direction * -1 + 30 < directionOfNextPoint:
                            strokeWidth = np.zeros((0, 0))
            oldX = consideringX
            # print('------------')
        return strokeWidth



def findStrokeWidthInDirectionNew(currentPoint, edgeMatrix, direction, dirMatrix):
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
        if not utils.oppositeDirection(direction,directionNextPoint,30):
            strokeWidth = np.zeros((0,0))
        # print(clock() - time6)

        break
    # print("rs")
    # print(strokeWidth)
    # print(clock() - time1)
    # print(clock() - time)
    print(strokeWidth.shape[0])
    return strokeWidth



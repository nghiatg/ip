import numpy as np
import math
from src import utils

# edgeMAtrix : ndarray,shape = (2,2), edge = 1 , the rest = 0
# edgePoints : python list
# output : matrix where each element is the width of stroke contains that element
def swt(edgePoints, dirMatrix):
    height = dirMatrix.shape[0]
    width = dirMatrix.shape[1]
    swtMatrix = np.empty(dirMatrix.shape)
    swtMatrix.fill(100)
    edgePoints2D = np.empty((len(edgePoints),2))
    eliminatedEdgePoints = []
    for i in range(len(edgePoints)):
        edgePoints2D[i] = utils.from1dTo2d(edgePoints[i],width)

    for i in range(edgePoints2D.shape[0]):
        currentPoint = np.array([[edgePoints2D[i][0], edgePoints2D[i][1]]])
        if currentPoint in eliminatedEdgePoints:
            continue
        gradientDirection = dirMatrix[edgePoints2D[i][0]][edgePoints2D[i][1]]     # also stroke-width direction
        strokeWidth = findStrokeWidthInDirection(currentPoint,edgePoints2D,gradientDirection,dirMatrix,eliminatedEdgePoints)
        for i in range(strokeWidth.shape[0]):
            swtMatrix[strokeWidth[i][0]][strokeWidth[i][1]] = strokeWidth.shape[0]
    return swtMatrix


def findStrokeWidthInDirection(currentPoint, edgePoints, direction, dirMatrix, eliminated):
    strokeWidth = np.array(currentPoint)
    ab = utils.getGraph(currentPoint,direction)
    nextPoint = np.empty((1,2))
    nextPoint.fill(-1)
    consideringY = currentPoint[0][0]
    oldX = currentPoint[0][1]
    if (direction < 0):
        while True:
            consideringY -= 1
            consideringX = math.floor((consideringY + 0.5 - ab[0][1]) / ab[0][0])
            for runX in range(oldX if consideringX > oldX else consideringX, consideringX if consideringX > oldX else oldX):
                strokeWidth = np.append(strokeWidth,np.array([[consideringY + 1, runX]]),axis=0)
            consideringPoint = np.array([[consideringY,consideringX]])
            strokeWidth = np.append(strokeWidth,consideringPoint,axis=0)
            if(consideringPoint in edgePoints):
                if(dirMatrix[consideringPoint[0][0]][consideringPoint[0][1]] not in range(direction * -1 -30, direction * -1 + 30)):
                    eliminated.append(consideringPoint)
                    strokeWidth = None
                break
            oldX = consideringX
        return strokeWidth
    else:
        while True:
            consideringY += 1
            consideringX = math.floor((consideringY + 0.5 - ab[0][1]) / ab[0][0])
            for runX in range(oldX if consideringX > oldX else consideringX, consideringX if consideringX > oldX else oldX):
                strokeWidth = np.append(strokeWidth,np.array([[consideringY - 1, runX]]),axis=0)
            consideringPoint = np.array([[consideringY, consideringX]])
            strokeWidth = np.append(strokeWidth, consideringPoint, axis=0)
            if(consideringPoint in edgePoints):
                if (dirMatrix[consideringPoint[0][0]][consideringPoint[0][1]] not in range(direction * -1 - 30, direction * -1 + 30)):
                    eliminated.appen(consideringPoint)
                    strokeWidth = None
                break
            oldX = consideringX
        return strokeWidth



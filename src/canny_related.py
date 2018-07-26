import numpy as np
from src import utils
horizontalMask = np.empty(shape=(3, 3))
verticalMask = np.empty(shape=(3, 3))
bigThreshold = 150
smallThreshold = 20


def initiateMask():
    horizontalMask[0] = ([-1, 0, 1])
    horizontalMask[1] = ([-2, 0, 2])
    horizontalMask[2] = ([-1, 0, 1])
    verticalMask[0] = ([-1, -2, -1])
    verticalMask[1] = ([0, 0, 0])
    verticalMask[2] = ([1, 2, 1])

# type 1 : horizontal
# type 2 : vertical
def getGradientMatrix(gray_matrix, type):
    if (type == 1):
        return utils.convolve(gray_matrix,horizontalMask)
    else:
        return utils.convolve(gray_matrix,verticalMask)


def getMagnitudeMatrix(horMatrix, verMatrix):
    return np.sqrt(horMatrix ** 2 + verMatrix ** 2)


def getDirectionMatrix(horMatrix, verMatrix):
    np.seterr(all='ignore')
    # print(horMatrix[1,:])
    # print(verMatrix[1,:])
    rawRs = np.degrees(np.arctan(verMatrix / horMatrix))
    # print(rawRs[1,:])
    # sgnHorMatrix = np.sign(horMatrix)
    # sgnHorMatrix -= 1
    # sgnHorMatrix *= -1
    # sgnrawMatrix = np.sign(rawRs)
    # addToRs = sgnrawMatrix * sgnHorMatrix * -90
    addToRs = (utils.getSgn(horMatrix) - 1) * utils.getSgn(rawRs) * 90
    rs = (addToRs + rawRs)
    # print(rs[1,:])
    # print(np.floor(horMatrix[125:136,125:136]))
    # print(np.floor(rawRs[125:136,125:136]))
    # print(np.floor(rs[125:136,125:136]))
    return rs




# use 1d index
def cannyGetEdgePoints(magMatrix, dirMatrix, width, useSmallThreshold):
    mag = magMatrix.flatten()
    dir = dirMatrix.flatten()
    points = []
    # apply big threshold
    gt = np.where(mag >= bigThreshold)
    for id in gt[0]:
        if (dirInWhichBucket(dir[id]) == 3):
            if (isHorMax(id, mag, width)):
                points.append(id)
        elif (dirInWhichBucket(dir[id]) == 1):
            if (isBackwardSlashMax(id, mag, width)):
                points.append(id)
        elif (dirInWhichBucket(dir[id]) == 4):
            if (isVerMax(id, mag, width)):
                points.append(id)
        elif (dirInWhichBucket(dir[id]) == 2):
            if (isForwardSlashMax(id, mag, width)):
                points.append(id)

    print("all : " + str(len(points)))
    return points

# location:
# 0   1   2
# 3   4   5
# 6   7   8
def getMagValue(id, magFlatten, relativeLocation, width):
    if (relativeLocation == 0):
        try:
            return magFlatten[id - width - 1]
        except:
            return 0
    elif (relativeLocation == 1):
        try:
            return magFlatten[id - width]
        except:
            return 0
    elif (relativeLocation == 2):
        try:
            return magFlatten[id - width + 1]
        except:
            return 0
    elif (relativeLocation == 3):
        try:
            return magFlatten[id - 1]
        except:
            return 0
    elif (relativeLocation == 5):
        try:
            return magFlatten[id + 1]
        except:
            return 0
    elif (relativeLocation == 6):
        try:
            return magFlatten[id + width - 1]
        except:
            return 0
    elif (relativeLocation == 7):
        try:
            return magFlatten[id + width]
        except:
            return 0
    elif (relativeLocation == 8):
        try:
            return magFlatten[id + width + 1]
        except:
            return 0


# location:
# 0   1   2
# 3   4   5
# 6   7   8
def getDirValue(id, dirFlatten, relativeLocation, width):
    if (relativeLocation == 0):
        try:
            return dirFlatten[id - width - 1]
        except:
            return 181
    elif (relativeLocation == 1):
        try:
            return dirFlatten[id - width]
        except:
            return 181
    elif (relativeLocation == 2):
        try:
            return dirFlatten[id - width + 1]
        except:
            return 181
    elif (relativeLocation == 3):
        try:
            return dirFlatten[id - 1]
        except:
            return 181
    elif (relativeLocation == 5):
        try:
            return dirFlatten[id + 1]
        except:
            return 181
    elif (relativeLocation == 6):
        try:
            return dirFlatten[id + width - 1]
        except:
            return 181
    elif (relativeLocation == 7):
        try:
            return dirFlatten[id + width]
        except:
            return 181
    elif (relativeLocation == 8):
        try:
            return dirFlatten[id + width + 1]
        except:
            return 181


def isHorMax(id, magFlatten, width):
    if (getMagValue(id, magFlatten, 3, width) < magFlatten[id] and getMagValue(id, magFlatten, 5, width) < magFlatten[
        id]):
        return True
    else:
        return False


def isVerMax(id, magFlatten, width):
    if (getMagValue(id, magFlatten, 1, width) < magFlatten[id] and getMagValue(id, magFlatten, 7, width) < magFlatten[
        id]):
        return True
    else:
        return False


def isForwardSlashMax(id, magFlatten, width):
    if (getMagValue(id, magFlatten, 2, width) < magFlatten[id] and getMagValue(id, magFlatten, 6, width) < magFlatten[
        id]):
        return True
    else:
        return False


def isBackwardSlashMax(id, magFlatten, width):
    if (getMagValue(id, magFlatten, 0, width) < magFlatten[id] and getMagValue(id, magFlatten, 8, width) < magFlatten[
        id]):
        return True
    else:
        return False


# parameter : gradient direction
#       1 : \
#       2 : /
#       3 : -
#       4 : |
def dirInWhichBucket(dirValue):
    if((dirValue < 22.5 and dirValue >= -22.5) or (dirValue >= 157.5 and dirValue < -157.5)):
        return 3
    elif((dirValue < 67.5 and dirValue >= 22.5) or (dirValue >= -157.5 and dirValue < -112.5)):
        return 1
    elif((dirValue < 112.5 and dirValue >= 67.5) or (dirValue >= -112.5 and dirValue < -67.5)):
        return 4
    else:
        return 2


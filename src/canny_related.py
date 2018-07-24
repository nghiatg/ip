import numpy as np
from src import utils
horizontalMask = np.empty(shape=(3, 3))
verticalMask = np.empty(shape=(3, 3))
bigThreshold = 50
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
def getGradientMatrix(biggerMatrix, type):
    rs = np.empty(shape=(biggerMatrix.shape[0] - 2, biggerMatrix.shape[1] - 2))

    if (type == 1):
        for y in range(1, biggerMatrix.shape[1] - 2):
            leftConvolution = np.convolve(horizontalMask[:, 0], biggerMatrix[:, y - 1], mode="valid")
            rightConvolution = np.convolve(horizontalMask[:, 2], biggerMatrix[:, y + 1], mode="valid")
            rs[:, y - 1] = leftConvolution + rightConvolution
        return rs
    else:
        for x in range(1, biggerMatrix.shape[0] - 2):
            upperConvolution = np.convolve(verticalMask[0, :], biggerMatrix[x - 1, :], mode="valid")
            bottomConvolution = np.convolve(verticalMask[2, :], biggerMatrix[x + 1, :], mode="valid")
            rs[x - 1, :] = upperConvolution + bottomConvolution
        return rs


def getMagnitudeMatrix(horMatrix, verMatrix):
    return np.sqrt(horMatrix ** 2 + verMatrix ** 2)


def getDirectionMatrix(horMatrix, verMatrix):
    np.seterr(all='ignore')
    return np.degrees(np.arctan(horMatrix / verMatrix))


# use 1d index
def cannyGetEdgePoints(magMatrix, dirMatrix, width, useSmallThreshold):
    mag = magMatrix.flatten()
    dir = dirMatrix.flatten()
    points = []
    # apply big threshold
    gt = np.where(mag >= bigThreshold)
    for id in gt[0]:
        if (dir[id] <= 22.5 or dir[id] > 157.5):
            if (isHorMax(id, mag, width)):
                points.append(id)
        elif (dir[id] <= 67.5):
            if (isBackwardSlashMax(id, mag, width)):
                points.append(id)
        elif (dir[id] <= 112.5):
            if (isVerMax(id, mag, width)):
                points.append(id)
        elif (dir[id] <= 157.5):
            if (isForwardSlashMax(id, mag, width)):
                points.append(id)

    if(useSmallThreshold == True):
        # apply small threshold
        print("done big threshold")
        considering = [0]
        newConsidering = points.copy()

        while (considering):
            considering = newConsidering
            newConsidering = []
            print("\nconsidering : " + str(len(considering)))
            for id in considering:

                # bucket 3
                if (dirInWhichBucket(dir[id]) == 3):
                    if ((id - width not in points) and getMagValue(id, mag, 1, width) >= smallThreshold
                            and getDirValue(id, dir, 1,width) != 181 and (dirInWhichBucket(getDirValue(id, dir, 1, width)) == 3)):
                        if (isHorMax(id - width, mag, width)):
                            points.append(id - width)
                            newConsidering.append(id - width)
                    if ((id + width not in points) and getMagValue(id, mag, 7, width) >= smallThreshold
                            and getDirValue(id,dir,7,width) != 181 and (dirInWhichBucket(getDirValue(id, dir, 7, width)) == 3)):
                        if (isHorMax(id + width, mag, width)):
                            points.append(id + width)
                            newConsidering.append(id + width)
                # bucket 1
                elif (dirInWhichBucket(dir[id]) == 1):
                    if ((id - width + 1 not in points) and getMagValue(id, mag, 2, width) >= smallThreshold
                            and getDirValue(id, dir, 2, width) != 181 and (dirInWhichBucket(getDirValue(id, dir, 2, width)) == 1)):
                        if (isBackwardSlashMax(id - width + 1, mag, width)):
                            points.append(id - width + 1)
                            newConsidering.append(id - width + 1)
                    if ((id + width - 1 not in points) and getMagValue(id, mag, 6, width) >= smallThreshold
                            and getDirValue(id, dir, 6, width) != 181 and (dirInWhichBucket(getDirValue(id, dir, 6, width)) == 1)):
                        if (isBackwardSlashMax(id + width - 1, mag, width)):
                            points.append(id + width - 1)
                            newConsidering.append(id + width - 1)

                # bucket 4
                elif (dirInWhichBucket(dir[id]) == 4):
                    if ((id - 1 not in points) and getMagValue(id, mag, 3, width) >= smallThreshold
                            and getDirValue(id, dir,3,width) != 181 and (dirInWhichBucket(getDirValue(id, dir, 3, width)) == 4)):
                        if (isVerMax(id - 1, mag, width)):
                            points.append(id - 1)
                            newConsidering.append(id - 1)
                    if ((id + 1 not in points) and getMagValue(id, mag, 5, width) >= smallThreshold
                            and getDirValue(id, dir,5,width) != 181 and (dirInWhichBucket(getDirValue(id, dir, 5, width)) == 4)):
                        if (isVerMax(id + 1, mag, width)):
                            points.append(id + 1)
                            newConsidering.append(id + 1)

                # bucket 2
                elif (dirInWhichBucket(dir[id]) == 2):
                    if ((id - width - 1 not in points) and getMagValue(id, mag, 0, width) >= smallThreshold
                            and getDirValue(id, dir, 0, width) != 181 and (dirInWhichBucket(getDirValue(id, dir, 0, width)) == 2)):
                        if (isForwardSlashMax(id - width - 1, mag, width)):
                            points.append(id - width - 1)
                            newConsidering.append(id - width - 1)
                    if ((id + width + 1 not in points) and getMagValue(id, mag, 8, width) >= smallThreshold
                            and getDirValue(id, dir, 8, width) != 181 and (dirInWhichBucket(getDirValue(id, dir, 8, width)) == 2)):
                        if (isForwardSlashMax(id + width + 1, mag, width)):
                            points.append(id + width + 1)
                            newConsidering.append(id + width + 1)

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
    if (getMagValue(id, magFlatten, 1, width) < magFlatten[id] and getMagValue(id, magFlatten, 7, width) < magFlatten[
        id]):
        return True
    else:
        return False


def isVerMax(id, magFlatten, width):
    if (getMagValue(id, magFlatten, 3, width) < magFlatten[id] and getMagValue(id, magFlatten, 5, width) < magFlatten[
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


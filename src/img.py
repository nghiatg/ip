from PIL import Image
import numpy as np
import math
import time

horizontalMask = np.empty(shape=(3, 3))
verticalMask = np.empty(shape=(3, 3))
ip2 = "..\\sunset_winter.jpg"
op2 = "..\\sunset_winter_edge.jpg"
bigThreshold = 150
smallThreshold = 75


def readImage(inputPath):
    return Image.open(inputPath)


def savePixelGrayValueToMatrix(img):
    rgbMatrix = np.array(img)
    rs = np.apply_along_axis(convertToGrayValue,2,rgbMatrix)
    return rs


def smoothingMaxMin(grayMatrix,margin):
    count = 0
    rs = np.empty(grayMatrix.shape)
    height = grayMatrix.shape[0]
    width = grayMatrix.shape[1]
    for y in range(height):
        for x in range(width):
            value = grayMatrix[y][x]
            grayMatrix[y][x] = grayMatrix[y][x-1] if x>0 else grayMatrix[y][x+1]
            max = np.max(grayMatrix[y-margin if y>=margin else 0 : y+margin+1,x-margin if x>=margin else 0 : x+margin+1])
            min = np.min(grayMatrix[y-margin if y>=margin else 0 : y+margin+1,x-margin if x>=margin else 0 : x+margin+1])

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

def smoothingAvg(grayMatrix,margin):
    count = 0
    rs = np.empty(grayMatrix.shape)
    height = grayMatrix.shape[0]
    width = grayMatrix.shape[1]
    for y in range(height):
        for x in range(width):
            grayMatrix[y][x] = grayMatrix[y][x-1] if x>0 else grayMatrix[y][x+1]
            grayMatrix[y][x] = np.average(grayMatrix[y-margin if y>=margin else 0 : y+margin+1,x-margin if x>=margin else 0 : x+margin+1])


def initiateMask():
    horizontalMask[0] = ([-1, 0, 1])
    horizontalMask[1] = ([-2, 0, 2])
    horizontalMask[2] = ([-1, 0, 1])
    verticalMask[0] = ([-1, -2, -1])
    verticalMask[1] = ([0, 0, 0])
    verticalMask[2] = ([1, 2, 1])


def saveToBiggerMatrix(data_matrix,margin):
    rs = np.zeros(shape=(data_matrix.shape[0] + margin * 2, data_matrix.shape[1] + margin * 2))
    rs[margin:rs.shape[0] - margin, margin:rs.shape[1] - margin] = data_matrix
    return rs


def convertToGrayValue(rgbValue):
    return (0.299 * rgbValue[0] + 0.587 * rgbValue[1] + 0.114 * rgbValue[2])


def writeImage(mode, size, outputPath):
    newImg = Image.new(mode, size)
    newImg.save(outputPath)


def changeImageToGray(input, output):
    img = readImage(input)
    # pix = img.load()
    grayMatrix = savePixelGrayValueToMatrix(img)
    imgMatrix = np.transpose(np.array([grayMatrix,grayMatrix,grayMatrix]),(1,2,0))
    imgRS = Image.fromarray(imgMatrix.astype('uint8'))
    # imgRS.show()
    imgRS.save(output)


# type 1 : horizontal
# type 2 : vertical
def getGradientMatrix(biggerMatrix, type):
    rs = np.empty(shape=(biggerMatrix.shape[0] - 2, biggerMatrix.shape[1] - 2))
    if (type == 1):
        for x in range(1, biggerMatrix.shape[0] - 2):
            for y in range(1, biggerMatrix.shape[1] - 2):
                rs[x][y] = sum(biggerMatrix[x - 1:x + 2, y - 1:y + 2].flatten() * horizontalMask.flatten())
                # print(str(x) + "\t" + str(y) + "\t" + str(rs[x][y]))
        return rs
    else:
        for x in range(1, biggerMatrix.shape[0] - 2):
            for y in range(1, biggerMatrix.shape[1] - 2):
                rs[x][y] = sum(biggerMatrix[x - 1:x + 2, y - 1:y + 2].flatten() * verticalMask.flatten())
        return rs

def getMagnitudeMatrix(horMatrix,verMatrix):
    rs = np.empty(shape=horMatrix.shape)
    for x in range(0, horMatrix.shape[0] - 1):
        for y in range(0, horMatrix.shape[1] - 1):
            rs[x][y] = math.sqrt(horMatrix[x][y] * horMatrix[x][y] + verMatrix[x][y] * verMatrix[x][y])
    return rs


def getDirectionMatrix(horMatrix,verMatrix):
    np.seterr(all='ignore')
    rs = np.empty(shape=horMatrix.shape)
    for x in range(0, horMatrix.shape[0] - 1):
        for y in range(0, horMatrix.shape[1] - 1):
            rs[x][y] = math.degrees(math.atan(horMatrix[x][y] / verMatrix[x][y]))
    return rs


# use 1d index
def cannyGetEdgePoints(magMatrix,dirMatrix,width):
    mag = magMatrix.flatten()
    dir = dirMatrix.flatten()
    # print(type(dir))
    # print(dir.size)
    # print(dir.shape)
    points = []
    # apply big threshold
    gt = np.where(mag >= bigThreshold)
    # print(gt.shape)
    for id in gt[0]:
        # print(id)
        # print(dir[id])
        if(dir[id] <= 22.5 or dir[id] > 157.5):
            if(isHorMax(id,mag,width)):
                points.append(id)
        elif (dir[id] <= 67.5 ):
            if (isBackwardSlashMax(id,mag,width)):
                points.append(id)
        elif (dir[id] <= 112.5 ):
            if (isVerMax(id,mag,width)):
                points.append(id)
        elif (dir[id] <= 157.5 ):
            if (isForwardSlashMax(id,mag,width)):
                points.append(id)

    # apply small threshold
    considering = points.copy()
    while(considering):
        print(len(considering))
        for id in considering:
            if (dir[id] <= 22.5 or dir[id] > 157.5):
                if((id-width not in points) and getMagValue(id,mag,1,width) >= smallThreshold and getDirValue(id,dir,1,width) != -1 and (getDirValue(id,dir,1,width) <= 22.5 or getDirValue(id,dir,1,width) > 157.5)):
                    if(isHorMax(id - width,mag,width)):
                        points.append(id-width)
                        considering.append(id - width)
                if ((id+width not in points) and getMagValue(id,mag,7,width) >= smallThreshold and getDirValue(id,dir,7,width) != -1 and (getDirValue(id, dir, 7, width) <= 22.5 or getDirValue(id, dir, 7, width) > 157.5)):
                    if (isHorMax(id + width, mag, width)):
                        points.append(id+width)
                        considering.append(id + width)

            elif (dir[id] <= 67.5):
                if ((id-width+1 not in points) and getMagValue(id,mag,2,width) >= smallThreshold and getDirValue(id, dir, 2, width) != -1 and (
                        getDirValue(id, dir, 2, width) <= 67.5 and getDirValue(id, dir, 2, width) > 22.5)):
                    if (isBackwardSlashMax(id - width + 1, mag, width)):
                        points.append(id - width + 1)
                        considering.append(id - width + 1)
                if ((id+width-1 not in points) and getMagValue(id,mag,6,width) >= smallThreshold and getDirValue(id, dir, 6, width) != -1 and (
                        getDirValue(id, dir, 6, width) <= 67.5 and getDirValue(id, dir, 6, width) > 22.5)):
                    if (isBackwardSlashMax(id + width - 1, mag, width)):
                        points.append(id + width - 1)
                        considering.append(id + width - 1)

            elif (dir[id] <= 112.5):
                if ((id-1 not in points) and getMagValue(id,mag,3,width) >= smallThreshold and getDirValue(id, dir, 3, width) != -1 and (
                        getDirValue(id, dir, 3, width) <= 112.5 and getDirValue(id, dir, 3, width) > 67.5)):
                    if (isVerMax(id - 1, mag, width)):
                        points.append(id - 1)
                        considering.append(id - 1)
                if ((id+1 not in points) and getMagValue(id,mag,5,width) >= smallThreshold and getDirValue(id, dir, 5, width) != -1 and (
                        getDirValue(id, dir, 5, width) <= 67.5 and getDirValue(id, dir, 5, width) > 22.5)):
                    if (isVerMax(id  + 1, mag, width)):
                        points.append(id + 1)
                        considering.append(id + 1)

            elif (dir[id] <= 157.5):
                if ((id-width-1 not in points) and getMagValue(id,mag,0,width) >= smallThreshold and getDirValue(id, dir, 0, width) != -1 and (
                        getDirValue(id, dir, 0, width) <= 67.5 and getDirValue(id, dir, 0, width) > 22.5)):
                    if (isForwardSlashMax(id - width - 1, mag, width)):
                        points.append(id - width - 1)
                        considering.append(id - width - 1)
                if ((id+width+1 not in points) and getMagValue(id,mag,8,width) >= smallThreshold and getDirValue(id, dir, 8, width) != -1 and (
                        getDirValue(id, dir, 8, width) <= 67.5 and getDirValue(id, dir, 8, width) > 22.5)):
                    if (isForwardSlashMax(id + width + 1, mag, width)):
                        points.append(id + width + 1)
                        considering.append(id + width + 1)
            considering.remove(id)
    return points



# location:
# 0   1   2
# 3   4   5
# 6   7   8
def getMagValue(id,magFlatten,relativeLocation,width):
    if(relativeLocation == 0):
        try:
            return magFlatten(id-width-1)
        except:
            return 0
    elif (relativeLocation == 1):
        try:
            return magFlatten(id - width)
        except:
            return 0
    elif (relativeLocation == 2):
        try:
            return magFlatten(id - width + 1)
        except:
            return 0
    elif (relativeLocation == 3):
        try:
            return magFlatten(id - 1)
        except:
            return 0
    elif (relativeLocation == 5):
        try:
            return magFlatten(id + 1)
        except:
            return 0
    elif (relativeLocation == 6):
        try:
            return magFlatten(id + width - 1)
        except:
            return 0
    elif (relativeLocation == 7):
        try:
            return magFlatten(id + width)
        except:
            return 0
    elif (relativeLocation == 8):
        try:
            return magFlatten(id + width + 1)
        except:
            return 0


# location:
# 0   1   2
# 3   4   5
# 6   7   8
def getDirValue(id,dirFlatten,relativeLocation,width):
    if(relativeLocation == 0):
        try:
            return dirFlatten(id-width-1)
        except:
            return -1
    elif (relativeLocation == 1):
        try:
            return dirFlatten(id - width)
        except:
            return -1
    elif (relativeLocation == 2):
        try:
            return dirFlatten(id - width + 1)
        except:
            return -1
    elif (relativeLocation == 3):
        try:
            return dirFlatten(id - 1)
        except:
            return -1
    elif (relativeLocation == 5):
        try:
            return dirFlatten(id + 1)
        except:
            return -1
    elif (relativeLocation == 6):
        try:
            return dirFlatten(id + width - 1)
        except:
            return -1
    elif (relativeLocation == 7):
        try:
            return dirFlatten(id + width)
        except:
            return -1
    elif (relativeLocation == 8):
        try:
            return dirFlatten(id + width + 1)
        except:
            return -1


def isHorMax(id,magFlatten,width):
    if(getMagValue(id,magFlatten,1,width) < magFlatten[id] and getMagValue(id,magFlatten,7,width) < magFlatten[id]):
        return True
    return False
def isVerMax(id,magFlatten,width):
    if(getMagValue(id,magFlatten,3,width) < magFlatten[id] and getMagValue(id,magFlatten,5,width) < magFlatten[id]):
        return True
    return False
def isForwardSlashMax(id,magFlatten,width):
    if(getMagValue(id,magFlatten,2,width) < magFlatten[id] and getMagValue(id,magFlatten,6,width) < magFlatten[id]):
        return True
    return False
def isBackwardSlashMax(id,magFlatten,width):
    if(getMagValue(id,magFlatten,0,width) < magFlatten[id] and getMagValue(id,magFlatten,8,width) < magFlatten[id]):
        return True
    return False

def from2dTo1d(yIndex,xIndex,width):
    return yIndex * width + xIndex


# [y,x]
def from1dTo2d(id,width):
    rs = np.empty((1,2))
    rs[0][0] = int(round(id/width))
    rs[0][1] = id % width
    return rs


if __name__ == '__main__':
    start = time.clock()
    initiateMask()
    img = readImage(ip2)
    gray_matrix = savePixelGrayValueToMatrix(img)
    print(-1)
    smoothGrayMatrix = smoothingAvg(gray_matrix,1)
    print(0)
    biggerMatrix = saveToBiggerMatrix(gray_matrix,1)
    # biggerMatrix = saveToBiggerMatrix(smoothGrayMatrix,1)
    print(1)
    horizontalGradientMatrix = getGradientMatrix(biggerMatrix,1)
    print(2)
    verticalGradientMatrix = getGradientMatrix(biggerMatrix,2)
    print(3)
    magnitudeMatrix = getMagnitudeMatrix(horizontalGradientMatrix,verticalGradientMatrix)
    print(4)
    directionMatrix = getDirectionMatrix(horizontalGradientMatrix,verticalGradientMatrix)
    print(5)
    edgePoints = cannyGetEdgePoints(magnitudeMatrix,directionMatrix,img.size[0])
    print(6)
    edgeImg = Image.new("1", img.size,255)
    print(7)
    pix = edgeImg.load()
    for id in edgePoints:
        location = from1dTo2d(id,img.size[0])
        pix[location[0][1],location[0][0]] = 0
    edgeImg.save(op2)
    print("--- %s seconds ---" % (time.clock() - start))






    # edgeImg = Image.new("RGB", img.size, (255, 255, 255))
    # changeImageToGray(ip,op)

    # pix = edgeImg.load()
    # for index in np.argwhere(gradientMatrix > threshold):
    #     pix[np.asscalar(index[0]),np.asscalar(index[1])] = (0,0,0)
    # edgeImg.save(op)

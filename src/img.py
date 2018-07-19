from PIL import Image
import numpy as np

horizontalMask = np.empty(shape=(3, 3))
verticalMask = np.empty(shape=(3, 3))
ip = "E:\\study\\img\\otherstuff\\344967.png"
op = "E:\\study\\img\\otherstuff\\344967_gray.png"
threshold = 200


def readImage(inputPath):
    return Image.open(inputPath)


def savePixelGrayValueToMatrix(img):
    rgbMatrix = np.array(img)
    rs = np.apply_along_axis(convertToGrayValue,2,rgbMatrix)
    return rs


def savePixelGrayValueToImgMatrix(img):
    rgbMatrix = np.array(img)
    rs = np.apply_along_axis(convertToGrayArr,2,rgbMatrix)
    return rs


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


def convertToGrayArr(rgbValue):
    grayValue = (0.299 * rgbValue[0] + 0.587 * rgbValue[1] + 0.114 * rgbValue[2])
    return np.array([grayValue,grayValue,grayValue])


def writeImage(mode, size, outputPath):
    newImg = Image.new(mode, size)
    newImg.save(outputPath)


def changeImageToGray(input, output):
    img = readImage(input)
    # pix = img.load()
    grayMatrix = savePixelGrayValueToMatrix(img)
    print(grayMatrix.shape)
    imgMatrix = np.transpose(np.array([grayMatrix,grayMatrix,grayMatrix]),(1,2,0))
    print(imgMatrix.shape)
    for x in range(10):
        print(10*x)
        print(imgMatrix[101*x][101*x][0])
        print(imgMatrix[101*x][101*x][1])
        print(imgMatrix[101*x][101*x][2])
        print(grayMatrix[101*x][101*x])
        print("\n")

    imgRS = Image.fromarray(imgMatrix.astype('uint8'))
    # imgRS.show()
    print(imgRS.mode)
    imgRS.save(output)



    # for x in range(img.size[0]):
    #     for y in range(img.size[1]):
    #         pix[x, y] = (int(round(grayMatrix[y,x])), int(round(grayMatrix[y,x])),int(round(grayMatrix[y,x])))
    # img.save(output)


# type 1 : horizontal
# type 2 : vertical
def getGradientMatrix(biggerMatrix, type):
    rs = np.empty(shape=(biggerMatrix.shape[0] - 2, biggerMatrix.shape[1] - 2))
    if (type == 1):
        for x in range(1, biggerMatrix.shape[0] - 2):
            for y in range(1, biggerMatrix.shape[1] - 2):
                rs[x][y] = sum(biggerMatrix[x - 1:x + 2, y - 1:y + 2].flatten() * horizontalMask.flatten())
                print(str(x) + "\t" + str(y) + "\t" + str(rs[x][y]))
        return rs
    else:
        for x in range(1, biggerMatrix.shape[0] - 2):
            for y in range(1, biggerMatrix.shape[1] - 2):
                rs[x][y] = sum(biggerMatrix[x - 1:x + 2, y - 1:y + 2].flatten() * verticalMask.flatten())
        return rs


if __name__ == '__main__':
    # initiateMask()
    # img = readImage(ip)
    # data_matrix = savePixelGrayValueToArr(img)
    # biggerMatrix = saveToBiggerMatrix(data_matrix)
    # gradientMatrix = getGradientMatrix(biggerMatrix, 1)
    # edgeImg = Image.new("RGB", img.size, (255, 255, 255))
    changeImageToGray(ip,op)

    # pix = edgeImg.load()
    # for index in np.argwhere(gradientMatrix > threshold):
    #     pix[np.asscalar(index[0]),np.asscalar(index[1])] = (0,0,0)
    # edgeImg.save(op)

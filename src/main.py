import time
from PIL import Image
from src.utils import from2dTo1d,from1dTo2d, saveToBiggerMatrix
from src.canny_related import initiateMask, getGradientMatrix, getMagnitudeMatrix, getDirectionMatrix, cannyGetEdgePoints
from src.img_handler import readImage, savePixelGrayValueToMatrix, smoothingAvg, smoothingAvg2
from src import test
import numpy as np
ip = "..\\trump.jpg"
op = "..\\trump_edge.jpg"
# ip = "..\\sunset_winter.jpg"
# op = "..\\sunset_winter_edge.jpg"

def realMain():
    start = time.clock()
    initiateMask()
    img = readImage(ip)
    gray_matrix = savePixelGrayValueToMatrix(img)
    # gray_matrix = smoothingAvg2(gray_matrix, 1)
    biggerMatrix = saveToBiggerMatrix(gray_matrix, 1)
    horizontalGradientMatrix = getGradientMatrix(biggerMatrix, 1)
    verticalGradientMatrix = getGradientMatrix(biggerMatrix, 2)
    magnitudeMatrix = getMagnitudeMatrix(horizontalGradientMatrix, verticalGradientMatrix)
    directionMatrix = getDirectionMatrix(horizontalGradientMatrix, verticalGradientMatrix)
    print(np.where(directionMatrix < 0)[0].shape)
    edgePoints = cannyGetEdgePoints(magnitudeMatrix, directionMatrix, img.size[0], True)
    edgeImg = Image.new("1", img.size, 255)
    pix = edgeImg.load()
    for id in edgePoints:
        location = from1dTo2d(id, img.size[0])
        pix[location[0][1], location[0][0]] = 0
    edgeImg.save(op)
    print("--- %s seconds ---" % (time.clock() - start))

def testMain():
    # test.testSmoothAvg()
    print(test.twiceReturn())

if __name__ == '__main__':
    realMain()
    # testMain()
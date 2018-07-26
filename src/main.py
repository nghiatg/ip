import time
import os
from PIL import Image
from src.utils import from2dTo1d,from1dTo2d, saveToBiggerMatrix
from src.canny_related import initiateMask, getGradientMatrix, getMagnitudeMatrix, getDirectionMatrix, cannyGetEdgePoints
from src.img_handler import readImage, savePixelGrayValueToMatrix, smoothingAvg, smoothingAvgFromScipy
from src import test
from src import swt_related
import numpy as np
from src import img_handler
img_name = "bunny"
ip = "..\\" + img_name + ".jpg"
edgeOp = "..\\" + img_name + "_edge.jpg"
swtOp = "..\\" + img_name + "_swt.jpg"
# ip = "..\\sunset_winter.jpg"
# op = "..\\sunset_winter_edge.jpg"

def realMain():
    try:
        os.remove(op)
    except:
        pass
    start = time.clock()
    initiateMask()
    img = readImage(ip)
    gray_matrix = savePixelGrayValueToMatrix(img)
    gray_matrix = smoothingAvg(gray_matrix, 1)
    gray_matrix = smoothingAvg(gray_matrix, 1)
    # gray_matrix = smoothingAvg(gray_matrix, 1)
    # gray_matrix = smoothingAvg(gray_matrix, 1)
    # gray_matrix = smoothingAvg(gray_matrix, 1)
    gray_matrix = img_handler.sharpen(gray_matrix,2)
    # gray_matrix = smoothingAvg(gray_matrix, 1)
    # gray_matrix = smoothingAvg(gray_matrix, 1)
    biggerMatrix = saveToBiggerMatrix(gray_matrix, 1)
    horizontalGradientMatrix = getGradientMatrix(biggerMatrix, 1)
    verticalGradientMatrix = getGradientMatrix(biggerMatrix, 2)
    magnitudeMatrix = getMagnitudeMatrix(horizontalGradientMatrix, verticalGradientMatrix)
    directionMatrix = getDirectionMatrix(horizontalGradientMatrix, verticalGradientMatrix)
    edgePoints = cannyGetEdgePoints(magnitudeMatrix, directionMatrix, img.size[0], False)

    edgeImg = Image.new("1", img.size, 255)
    pix = edgeImg.load()
    for id in edgePoints:
        location = from1dTo2d(id, img.size[0])
        pix[location[0][1], location[0][0]] = 0
    edgeImg.save(edgeOp)



    swtMatrix = swt_related.swt(edgePoints,directionMatrix)
    pixelsInText = np.where(np.logical_and(np.greater_equal(swtMatrix,swt_related.small_threshold),np.greater_equal(swt_related.big_threshold,swtMatrix)))
    swtImg = Image.new("1", img.size, 255)
    pixSwt = swtImg.load()
    for i in range(pixelsInText[0].size):
        pixSwt[int(pixelsInText[1][i]), int(pixelsInText[0][i])] = 0
    swtImg.save(swtOp)
    print("--- %s seconds ---" % (time.clock() - start))

def testMain():
    test.testSmoothAvg()
    # print(test.twiceReturn())
    # test.testConvolve()

if __name__ == '__main__':
    realMain()
    # testMain()
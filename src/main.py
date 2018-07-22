import time
from PIL import Image
from src.utils import from2dTo1d,from1dTo2d, saveToBiggerMatrix
from src.canny_related import initiateMask, getGradientMatrix, getMagnitudeMatrix, getDirectionMatrix, cannyGetEdgePoints
from src.img_handler import readImage, savePixelGrayValueToMatrix, smoothingAvg

ip = "..\\sunset_winter.jpg"
op = "..\\sunset_winter_edge.jpg"


if __name__ == '__main__':
    start = time.clock()
    initiateMask()
    img = readImage(ip)
    gray_matrix = savePixelGrayValueToMatrix(img)
    print(-1)
    time1 = time.clock()
    print(time1-start)
    smoothGrayMatrix = smoothingAvg(gray_matrix, 1)
    print(0)
    time2 = time.clock()
    print(time2-time1)
    biggerMatrix = saveToBiggerMatrix(gray_matrix, 1)
    print(1)
    time3 = time.clock()
    print(time3-time2)
    horizontalGradientMatrix = getGradientMatrix(biggerMatrix, 1)
    print(2)
    time4 = time.clock()
    print(time4-time3)
    verticalGradientMatrix = getGradientMatrix(biggerMatrix, 2)
    print(3)
    time5 = time.clock()
    print(time5-time4)
    magnitudeMatrix = getMagnitudeMatrix(horizontalGradientMatrix, verticalGradientMatrix)
    print(4)
    time6 = time.clock()
    print(time6-time5)
    directionMatrix = getDirectionMatrix(horizontalGradientMatrix, verticalGradientMatrix)
    print(5)
    time7 = time.clock()
    print(time7-time6)
    edgePoints = cannyGetEdgePoints(magnitudeMatrix, directionMatrix, img.size[0])
    print(6)
    time8 = time.clock()
    print(time8-time7)
    edgeImg = Image.new("1", img.size, 255)
    print(7)
    pix = edgeImg.load()
    for id in edgePoints:
        location = from1dTo2d(id, img.size[0])
        try:
            pix[location[0][1], location[0][0]] = 0
        except:
            print(id)
            print(location[0][1])
            print(location[0][0])
    edgeImg.save(op)
    print("--- %s seconds ---" % (time.clock() - start))
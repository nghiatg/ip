import numpy as np
from src import img_handler
from src import utils

def testSmoothAvg():
    t = np.arange(100).reshape((10,10))
    print(t)
    # print("\n\n\n")
    # print(img_handler.smoothingAvg2(t,1))
    # print("\n\n\n")
    print(img_handler.smoothingAvg2(t,2))

def twiceReturn():
    if(5>0):
        return 1
    print("this sucks")
    return 0

def testConvolve():
    t = np.arange(16).reshape((4,4))
    kernel = np.arange(9).reshape((3,3))
    print(t)
    print(kernel)
    print(utils.convolve(t,kernel))
import numpy as np
from src import img_handler
from src import utils
import time

def testSmoothAvg():
    t = np.arange(1200*1920).reshape((1200,1920))
    # t = np.arange(100).reshape((10,10))
    print(t)
    # print("\n\n\n")
    # print(img_handler.smoothingAvg2(t,1))
    # print("\n\n\n")
    start = time.clock()
    t1 = (img_handler.smoothingAvg(t,1))
    time1 = time.clock()
    t2 = (img_handler.smoothingAvg(t,1))
    time2 = time.clock()
    print(time1 - start)
    print(time2 - time1)
    t3 = t1-t2
    print(np.where(t3 > 0))

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
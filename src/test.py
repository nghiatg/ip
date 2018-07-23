import numpy as np
from src import img_handler

def testSmoothAvg():
    t = np.arange(100).reshape((10,10))
    print(t)
    print("\n\n\n")
    print(img_handler.smoothingAvg2(t,1))
    print("\n\n\n")
    print(img_handler.smoothingAvg(t,1))

def twiceReturn():
    if(5>0):
        return 1
    print("this sucks")
    return 0
import numpy as np
import math
def from2dTo1d(yIndex, xIndex, width):
    return yIndex * width + xIndex


# [y,x]
def from1dTo2d(id, width):
    rs = np.empty((1, 2))
    rs[0][0] = int(math.floor(id / width))
    rs[0][1] = id % width
    return rs


def saveToBiggerMatrix(data_matrix, margin):
    rs = np.zeros(shape=(data_matrix.shape[0] + margin * 2, data_matrix.shape[1] + margin * 2))
    rs[margin:rs.shape[0] - margin, margin:rs.shape[1] - margin] = data_matrix
    return rs

# -*- coding: utf-8 -*-
import os
import math
import json
from PIL import Image

def DCT(img, size):
    """ Discrete cosine transform
        get: image, width=size[0], height=size[1]
        return: upper left 8x8 block of DCTMatrix
    """
    DCTMatrix = [[0 for x in range(size[0])] for y in range(size[1])]
    for u in range(size[0]):
        for v in range(size[1]):
            for i in range(size[0]):
                for j in range(size[1]):
                    r, g, b = img.getpixel((i, j))
                    S = (r + g + b) // 3
                    val1 = math.pi/size[0]*(i+1./2.)*u
                    val2 = math.pi/size[1]*(j+1./2.)*v
                    DCTMatrix[u][v] += S * math.cos(val1) * math.cos(val2)
    matrix = [[0 for x in range(8)] for y in range(8)]
    for i in range(8):
        for j in range(8):
            matrix[i][j] = DCTMatrix[i][j]
    return matrix

# pHash https://habrahabr.ru/post/120562/
def getImageHash(img):
    """ Get image pHash
        return: 64-bit hash string
    """
    size = 32, 32
    img = img.resize(size, Image.ANTIALIAS)
    matrix = DCT(img, size)
    average = 0
    for i in range(8):
        for j in range(8):
            if i == 0 and j == 0:
                continue
            average += matrix[i][j]
    average = average / 63

    hashString = ''
    for i in range(8):
        for j in range(8):
            if matrix[i][j] >= average:
                hashString += '1'
            else:
                hashString += '0'
    return hashString

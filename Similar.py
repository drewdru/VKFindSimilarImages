from PIL import Image
import os
import math

def getThumbnail(imgDir, size):
    imageList = os.listdir(imgDir)
    for inImage in imageList:
        img = Image.open(imgDir + inImage)
        img.thumbnail(size)
        img = img.convert(mode='L')
        img.save('./thumb/' + inImage, "JPEG")

def rmsDifference(img1, img2, size):
    '''
    images root mean square difference
    '''
    res = [0, 0, 0]    
    for i in range(size[0]):
        for j in range(size[1]):
            try:
                for k in range(3):
                    res[k] += (img1[i,j][k] - img2[i,j][k]) ** 2
            except IndexError:
                break              
    for k in range(3):
        res[k] = math.sqrt( res[k] ) / 256
    return res

def findSimilarImages(imgDir, size):
    imageList = os.listdir(imgDir)
    for index, inImage1 in enumerate(imageList):
        img1 = Image.open(imgDir + inImage1)
        startINDX = index+1
        for index2, inImage2 in enumerate(imageList[startINDX:]):
            img2 = Image.open(imgDir + inImage2)
            rmsDiff = rmsDifference(img1.load(), img2.load(), img1.size)
            if rmsDiff[0] < 8 and rmsDiff[1] < 8 and rmsDiff[2] < 8:
                saveURLtoSimilarImages
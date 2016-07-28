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
    # res = [0, 0, 0]   
    res = 0 
    for i in range(size[0]):
        for j in range(size[1]):
            try:
                dif = img1[i,j] - img2[i,j]
                res += pow(dif, 2)
                # for k in range(3):
                #     dif = img1[i,j][k] - img2[i,j][k]
                #     res[k] += pow(dif, 2)
            except IndexError:
                break      
    res = math.sqrt( res ) / 256
    # for k in range(3):
    #     res[k] = math.sqrt( res[k] ) / 256
    return res

def findSimilarImages(imgDir):
    imageList = os.listdir(imgDir)
    for index, inImage1 in enumerate(imageList):
        img1 = Image.open(imgDir + inImage1)
        startINDX = index+1
        for index2, inImage2 in enumerate(imageList[startINDX:]):
            img2 = Image.open(imgDir + inImage2)
            rmsDiff = rmsDifference(img1.load(), img2.load(), img1.size)
            if rmsDiff < 1:
                print(rmsDiff)
                print(inImage1, inImage2)
                # pass
                # saveURLtoSimilarImages
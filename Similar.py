import json
import math
import os

from PIL import Image
from vkBase.views.images import ImagesView


def saveURLtoSimilarImages(ownerID, imgId1, imgId2):
    ''' Save similar images to similarImages.txt '''
    img1 = '{}_{}'.format(ownerID, imgId1)
    img2 = '{}_{}'.format(ownerID, imgId2)

    print('https://vk.com/photo{}'.format(img1))
    print('https://vk.com/photo{}'.format(img2))
    
    f = open('similarImages.txt','a+')
    f.write(img1 + ',' + img2 + ',\n')
    f.close()

def getThumbnails(imgDir, thumbDir, size):
    ''' Getting thumbnails  '''
    imageList = os.listdir(imgDir)
    for inImage in imageList:
        img = Image.open(imgDir + inImage)
        img.thumbnail(size)
        img = img.convert(mode='L')
        img.save(thumbDir + inImage, "JPEG")

def rmsDifference(img1, img2, size):
    ''' Return a root mean square difference of two images '''
    res = 0 
    for i in range(size[0]):
        for j in range(size[1]):
            try:
                dif = img1[i,j] - img2[i,j]
                res += pow(dif, 2)
            except IndexError:
                break      
    res = math.sqrt( res ) / 256
    return res

def findSimilarImages(imgDir, ownerID):
    ''' findSimilarImages '''
    imageList = os.listdir(imgDir)
    for index, inImage1 in enumerate(imageList):
        img1 = Image.open(imgDir + inImage1)
        startINDX = index+1
        for index2, inImage2 in enumerate(imageList[startINDX:]):
            img2 = Image.open(imgDir + inImage2)
            rmsDiff = rmsDifference(img1.load(), img2.load(), img1.size)
            if rmsDiff < 1:
                imgIndx1 = inImage1.split('.')[0]
                imgIndx2 = inImage2.split('.')[0]                
                imgInfoFile = open('imgInfo.json', 'r')
                imgInfo = json.load(imgInfoFile)
                imgInfoFile.close()
                saveURLtoSimilarImages(ownerID, imgInfo['img'][imgIndx1]['id'],
                    imgInfo['img'][imgIndx2]['id'])


# may be optimized: https://habrahabr.ru/post/211264/
def checkHammingDistance(hashString1, hashString2, hashLength, HammingDistance):
    """
        Check difference of hashes

        @param hashString1 The hash string
        @param hashString2 The hash string
        @return Return True if count of hashes difference < hashLength
    """
    if (len(hashString1) != hashLength) or (len(hashString2) != hashLength):
        raise Exception('One of two strings not a 64-bit hash')
    differenceSum = 0
    for indx in range(hashLength):
        if hashString1[indx] != hashString2[indx]:
            differenceSum += 1
        if differenceSum > HammingDistance:
            return False
    return True

def findSimilarImagesByPHash(ownerId, album):
    records = ImagesView().getImagesByAlbumID(album.album_id)
    for indx, imgInfo1 in enumerate(records):
        startINDX = indx + 1
        for imgInfo2 in records[startINDX:]:
            if checkHammingDistance(imgInfo1.image_hash,
                    imgInfo2.image_hash, 64, 5):
                saveURLtoSimilarImages(ownerId, imgInfo1.image_id,
                    imgInfo2.image_id)

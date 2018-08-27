
import json
import os
import sys
import time

import vk

import settings
from VKDownloadImage import downloadImage
from vkBase.models.images import Images


def clearTempData(imgDir, deleteImgDir, thumbDir, imgInfoFile,
                  deleteImgInfoFile): # clear directory with images
    try:
        imageList = os.listdir(imgDir)
        for inImage in imageList:
            os.remove(imgDir + inImage)
    except FileNotFoundError:
        pass
    # clear directory with deleteImages
    try:
        imageList = os.listdir(deleteImgDir)
        for inImage in imageList:
            os.remove(deleteImgDir + inImage)
    except FileNotFoundError:
        pass
    # clear directory with Thumbnails
    try:
        imageList = os.listdir(thumbDir)
        for inImage in imageList:
            os.remove(thumbDir + inImage)
    except FileNotFoundError:
        pass
    # remove file with information about the downloaded images
    try:
        os.remove(imgInfoFile)
    except FileNotFoundError:
        pass
    # remove file with information about the downloaded images to remove
    try:
        os.remove(deleteImgInfoFile)
    except FileNotFoundError:
        pass
    # remove file with similar images list
    try:
        os.remove('./similarImages.txt')
    except FileNotFoundError:
        pass
    # remove file with images to delete
    try:
        os.remove('./delete.txt')
    except FileNotFoundError:
        pass
    print('old files are removed')

def getAccessToken():
    # uri example "https://oauth.vk.com/authorize?client_id=4916113&scope=photos,wall,groups,offline&redirect_uri=https://oauth.vk.com/blank.html&display=mobile&v=5.53&response_type=token"
    uri = '{}?v={}&client_id={}&scope={}&redirect_uri={}&{}'.format(
        'https://oauth.vk.com/authorize', 
        settings.VK['api_v'], 
        settings.VK['app_id'],
        settings.VK['scope'],
        'https://oauth.vk.com/blank.html',
        'display=mobile&response_type=token'
    )
    print('pls get acces_tocken here:')
    print(uri)
    return input('access_token: ')

def getVkApi():
    """ Get vk api with access_token """
    if settings.VK['isTwoFactor']:
        # get access_token to vk api
        access_token = getAccessToken()
        vkSession = vk.Session(access_token=access_token)
    else:
        # get access_token to vk api
        vkSession = vk.AuthSession(app_id=settings.VK['app_id'],
            user_login=settings.VK['user_login'],
            user_password=settings.VK['user_password'],
            scope=settings.VK['scope'])

    print('Connection with vk. Stand by ...')
    vkApi = vk.API(vkSession, v=settings.VK['api_v'], timeout=999999999)
    print('VK api is connected')
    return vkApi

def deleteLostImages(vkApi, OWNER_ID, error404List):
    count = 0
    textCode = ''
    for error404Image in error404List:
        count += 1
        print('delete 404IMAGE id = ' + str(error404Image))
        # api.photos.delete(owner_id = OWNER_ID, photo_id = error404Image)
        textCode += ('API.photos.delete({"owner_id": "'
            + OWNER_ID
            + '", "photo_id": "'
            + error404Image
            + '"}); ')
        if count%24 == 0:
            vkApi.execute(code=textCode) 
            count = 0
            textCode = ''
            time.sleep(10) 
    if count != 0:
        vkApi.execute(code=textCode) 
        time.sleep(10)

def sortByID(inputStr):
    return int(inputStr.split('.')[0])

def compareImagesSize(deleteImgDir, imgPath1, imgPath2):
    if os.path.getsize(deleteImgDir + imgPath1) >=\
            os.path.getsize(deleteImgDir + imgPath2):
        biggerImage = imgPath1.split('.')[0]
        smallerImage = imgPath2.split('.')[0]
    else:
        biggerImage = imgPath1.split('.')[0]
        smallerImage = imgPath2.split('.')[0]
    return biggerImage, smallerImage

def saveImageCaption(vkApi, OWNER_ID, deleteImgDir, deleteImgInfoFile):
    deleteImageList = os.listdir(deleteImgDir)
    deleteImageList.sort(key=sortByID)
    count = 0
    textCode = ''
    imgID = ''
    try:
        dImgInfoFile = open(deleteImgInfoFile, 'r')
        imgInfo = json.load(dImgInfoFile)
        dImgInfoFile.close()
        i = 0
        while i < len(deleteImageList) - 1:
            originImage, deleteImage = compareImagesSize(deleteImgDir,
                deleteImageList[i], deleteImageList[i + 1])
            # Save deleteImage id
            f = open('delete.txt', 'a+')
            f.write('{}\n'.format(imgInfo['img'][deleteImage]['id']))
            f.close()
            # Save caption
            originText = imgInfo['img'][originImage]['text']
            deleteText = imgInfo['img'][deleteImage]['text']
            print('image ' + originImage + ': ' + originText)
            print('image ' + deleteImage + ': ' + deleteText)
            text = ''
            imgID = str(imgInfo['img'][originImage]['id'])
            if originText == '' and deleteText != '':
                text = deleteText
            elif originText != '' and deleteText != ''\
                    and originText.lower() != deleteText.lower():
                text = originText
                text += '\n_________\n'
                text += deleteText
            if text != '': # TODO: use exec method (not used due to error)
                vkApi.photos.edit(owner_id=OWNER_ID,
                    photo_id=imgInfo['img'][originImage]['id'],
                    caption=text)
                time.sleep(2)
            i += 2
    except FileNotFoundError:
        pass

def deleteVkImages(vkApi, OWNER_ID, deleteImgDir, deleteImgInfoFile):
    try:
        f = open('similarImages.txt', 'r')
        photoIds = f.read()
        f.close()
        photoList = vkApi.photos.getById(photos=photoIds, photo_sizes=1)
        error404List = downloadImage(photoList,
            deleteImgDir,
            deleteImgInfoFile,
            isBig=True)
    except FileNotFoundError:
        pass
    saveImageCaption(vkApi, OWNER_ID, deleteImgDir, deleteImgInfoFile)
    try:
        deletePhotosFile = open('delete.txt', 'r')
        count = 0
        textCode = ''
        for deletePhoto in deletePhotosFile:
            count += 1
            deletePhoto = deletePhoto.rstrip('\n')
            print('https://vk.com/photo{}_{}'.format(OWNER_ID, deletePhoto))
            textCode += ('API.photos.delete({"owner_id": "'
                + OWNER_ID
                + '", "photo_id": "'
                + deletePhoto
                + '"}); ')
            with Images() as imagesModel:
                imagesModel.delete(deletePhoto)
            if count%24 == 0:
                vkApi.execute(code=textCode)
                count = 0
                textCode = ''
                time.sleep(10)
        if count != 0:
            vkApi.execute(code=textCode)
        deletePhotosFile.close()
        time.sleep(30)
    except FileNotFoundError:
        pass

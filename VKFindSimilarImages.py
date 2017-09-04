import vk
import json
import os
import time
import sys
import settings
from VKDownloadImage import downloadImage
from Similar import getThumbnails, findSimilarImages

def getVkApi():
    """ Get vk api with access_token """
    # get access_token to vk api
    vkSession = vk.AuthSession(app_id=settings.VK['app_id'],
        user_login=settings.VK['user_login'],
        user_password=settings.VK['user_password'],
        scope=settings.VK['scope'])
    print('Connection with vk. Stand by ...')
    vkApi = vk.API(vkSession, v='5.53', timeout=999999999)
    print('VK api is connected')
    return vkApi

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

def deleteSimilarImages(vkApi, deleteImgDir, deleteImgInfoFile):
    print('\nDELETE SIMILAR IMAGES!\n')
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
            originImage = '-1'
            deleteImage = '-1'
            if os.path.getsize(deleteImgDir + deleteImageList[i]) >=\
                    os.path.getsize(deleteImgDir + deleteImageList[i + 1]):
                originImage = deleteImageList[i].split('.')[0]
                deleteImage = deleteImageList[i + 1].split('.')[0]
            else:
                originImage = deleteImageList[i + 1].split('.')[0]
                deleteImage = deleteImageList[i].split('.')[0]

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
            # Save deleteImage id
            img1 = str(imgInfo['img'][deleteImage]['id'])
            f = open('delete.txt', 'a+')
            f.write(img1 + '\n')
            f.close()
            i += 2
    except FileNotFoundError:
        pass

def deleteVkImages(vkApi, OWNER_ID):
    try:
        deletePhotosFile = open('delete.txt', 'r')
        count = 0
        textCode = ''
        for deletePhoto in deletePhotosFile:
            count += 1
            deletePhoto = deletePhoto.rstrip('\n')
            print('https://vk.com/photo'
                + OWNER_ID
                + '_'
                + deletePhoto)
            textCode += ('API.photos.delete({"owner_id": "'
                + OWNER_ID
                + '", "photo_id": "'
                + deletePhoto
                + '"}); ')
            #api.photos.delete(owner_id = OWNER_ID, photo_id = deletePhoto)
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

def main():
    """ Main entry point for the script """
    OWNER_ID = settings.VK['owner_id']
    isResume = settings.VK['isResume']
    albumBlackList = settings.VK['albumBlackList']
    resumeAlbumID = settings.VK['resumeAlbumID']

    vkApi = getVkApi()
    albums = vkApi.photos.getAlbums(owner_id=OWNER_ID)

    imgDir = './img/'
    thumbDir = './thumb/'
    thumbnailsSize = 32, 32
    imgInfoFile = './imgInfo.json'
    deleteImgDir = './deleteImg/'
    deleteImgInfoFile = './deleteImgInfo.json'

    for index, album in enumerate(albums['items']):
        if isResume and album['id'] != resumeAlbumID:
            continue
        else:
            isResume = False
        if album['id'] in albumBlackList:
            continue

        clearTempData(imgDir, deleteImgDir, thumbDir, imgInfoFile, deleteImgInfoFile)

        print(album['id'])
        # get photos list from album['id']
        photos = vkApi.photos.get(owner_id=OWNER_ID,
            album_id=album['id'],
            photo_sizes='1')

        error404List = downloadImage(photos['items'], imgDir,\
            imgInfoFile, isBig=False)
        deleteLostImages(vkApi, OWNER_ID, error404List)

        getThumbnails(imgDir, thumbDir, thumbnailsSize)
        findSimilarImages(thumbDir)

        deleteSimilarImages(vkApi, deleteImgDir, deleteImgInfoFile)
        deleteVkImages(vkApi, OWNER_ID)

def sortByID(inputStr):
    return int(inputStr.split('.')[0])

if __name__ == '__main__':
    sys.exit(main())

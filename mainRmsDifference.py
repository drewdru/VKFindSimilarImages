import os
import sys

import settings
import vkApiHelper
from Similar import findSimilarImages, getThumbnails
from VKDownloadImage import downloadImage



def main():
    """ Main entry point for the script """
    OWNER_ID = settings.VK['owner_id']
    isResume = settings.VK['isResume']
    albumBlackList = settings.VK['albumBlackList']
    resumeAlbumID = settings.VK['resumeAlbumID']

    vkApi = vkApiHelper.getVkApi()
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

        vkApiHelper.clearTempData(imgDir, deleteImgDir, thumbDir,
            imgInfoFile, deleteImgInfoFile)

        print(album['id'])
        # get photos list from album['id']
        photos = vkApi.photos.get(owner_id=OWNER_ID,
            album_id=album['id'],
            photo_sizes='1')

        error404List = downloadImage(photos['items'], imgDir,\
            imgInfoFile, isBig=False)
        vkApiHelper.deleteLostImages(vkApi, OWNER_ID, error404List)

        getThumbnails(imgDir, thumbDir, thumbnailsSize)
        findSimilarImages(thumbDir, OWNER_ID)

        print('\nDELETE SIMILAR IMAGES!\n')
        vkApiHelper.deleteVkImages(vkApi, OWNER_ID, deleteImgDir, deleteImgInfoFile)

if __name__ == '__main__':
    sys.exit(main())

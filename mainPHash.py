import json
import os
import sys
import time

import vk

import settings
import vkApiHelper
from vkBase import vkDbHelper
from Similar import findSimilarImagesByPHash
from vkBase.views.albums import AlbumsView

def main():
    """ Main entry point for the script """
    OWNER_ID = settings.VK['owner_id']
    isResume = settings.VK['isResume']
    resumeAlbumID = settings.VK['resumeAlbumID']

    imgDir = './img/'
    thumbDir = './thumb/'
    imgInfoFile = './imgInfo.json'
    deleteImgDir = './deleteImg/'
    deleteImgInfoFile = './deleteImgInfo.json'

    vkApi = vkApiHelper.getVkApi()
    albums = vkApi.photos.getAlbums(owner_id=OWNER_ID)

    vkDbHelper.findNewAlbums(albums['items'])
    vkDbHelper.addAlbumsToDB(albums['items'])
    print('Find new images and generate hash')
    vkDbHelper.getVkImages(vkApi, albums['items'], OWNER_ID,
        isResume=isResume, resumeAlbumID=resumeAlbumID)

    albums = AlbumsView().getAlbumsWithoutBlacklist()
    for album in albums:
        print('Album id: {}'.format(album.album_id))
        vkApiHelper.clearTempData(imgDir, deleteImgDir, thumbDir,
            imgInfoFile, deleteImgInfoFile)
        findSimilarImagesByPHash(OWNER_ID, album)
        print('\nDELETE SIMILAR IMAGES!\n')
        vkApiHelper.deleteVkImages(vkApi, OWNER_ID, deleteImgDir, deleteImgInfoFile)
        time.sleep(30)



if __name__ == '__main__':
    sys.exit(main())

# -*- coding: utf-8 -*-
import os
import sys

from .vkImageSaver import savePhotosToDB
from .models.albums import Albums

def findNewAlbums(albums):
    """ Find new albums
        :param dict albums: All owners albums
    """
    allAlbums = []
    albumsTypeDir = './vkBase/albums_type/'
    albumsTypeList = os.listdir(albumsTypeDir)
    for albumsType in albumsTypeList:
        with open(albumsTypeDir + albumsType) as f:
            for line in f:
                allAlbums.append(int(line))
    isFindedNewAlbums = False
    for album in albums:
        if album['id'] not in allAlbums:
            isFindedNewAlbums = True
            print(album['id'])
    if isFindedNewAlbums:
        # TODO: auto add new albums and update them with GUI dialog
        print('New albums are found, please add them to the database')
        programPause = input('And press <ENTER> to continue...')

def getAlbumTypeIndxByFileName(fileName):
    if fileName == 'admin_albums.txt': return 1
    if fileName == 'special_albums.txt': return 2
    if fileName == 'theme_albums.txt': return 3
    if fileName == 'games_and_another_worlds_albums.txt': return 4
    if fileName == 'artist_albums.txt': return 5
    return 0

def addAlbumsToDB(albums):
    """ Add albums to data base """
    albumsTypeDir = './vkBase/albums_type/'
    albumsTypeList = os.listdir(albumsTypeDir)
    for albumsType in albumsTypeList:
        albumTypeIndx = getAlbumTypeIndxByFileName(albumsType)
        with open(albumsTypeDir + albumsType) as f:
            for line in f:
                for item in albums:
                    if item['id'] == int(line):
                        with Albums() as albumsModel:
                            if albumsModel.checkAlbumId(item['id']):
                                albumsModel.update(item['id'], albumTypeIndx,
                                    item['title'], item['description'])
                            else: 
                                albumsModel.insert(item, albumTypeIndx)

def getVkImages(vkApi, albums, OWNER_ID, isResume=False, resumeAlbumID=0):
    for album in albums:
        if isResume and album['id'] != resumeAlbumID:
            continue
        else:
            isResume = False
        # get photos list from album['id']
        photos = vkApi.photos.get(owner_id=OWNER_ID,
            album_id=album['id'],
            photo_sizes='1')
        savePhotosToDB(photos['items'], isBig=False)

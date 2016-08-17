import vk
import json
import os
import time
import sys
from VKDownloadImage import downloadImage
from Similar import getThumbnails, findSimilarImages

def main():
    """Main entry point for the script."""
    
    # get access_token to vk api
    session = vk.AuthSession(app_id = 'APP_ID',
        user_login = 'USER_LOGIN', 
        user_password = 'USER_PASS', 
        scope = 'photos, wall, groups, offline')

    api = vk.API(session, v='5.53', timeout=10)
    print('api is connected')  

    # get albums list
    OWNER_ID = 'OWNER_ID'
    albums = api.photos.getAlbums(owner_id = OWNER_ID)

    isResume = True
    resumeAlbumID = ALBUM_ID

    imgDir = './img/'
    thumbDir = './thumb/'
    thumbnailsSize = 32,32

    for index, album in enumerate(albums['items']):    
        if isResume and album['id'] != resumeAlbumID:
            continue
        else:
            isResume = False    
        
        successful = False
        while not successful:
            #clear directory with images
            try:
                imageList = os.listdir(imgDir)
                for inImage in imageList:
                    os.remove(imgDir + inImage)
            except FileNotFoundError:
                pass
            #clear directory with Thumbnails
            try:
                imageList = os.listdir(thumbDir)
                for inImage in imageList:
                    os.remove(thumbDir + inImage)
            except FileNotFoundError:
                pass
            #remove file with information about the downloaded images
            try:
                os.remove('./imgInfo.json')
            except FileNotFoundError:
                pass
            
            print(album['id'])
            # get photos list from album['id']
            photos = api.photos.get(owner_id = OWNER_ID, 
                album_id = album['id'], 
                photo_sizes='1')
            
            error404List = downloadImage(photos['items'], isBig = False)
            if len(error404List) > 0:
                #deleteImages(error404List);
                print(error404List)
                successful = False
                continue
                            
            getThumbnails(imgDir, thumbDir, thumbnailsSize)
            findSimilarImages(thumbDir)
            successful = True
            time.sleep(200)

if __name__ == '__main__':
    sys.exit(main())






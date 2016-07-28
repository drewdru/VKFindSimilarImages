import vk
import json

from VKDownloadImage import downloadImage
from Similar import getThumbnail, findSimilarImages

session = vk.AuthSession(app_id = 'APP_ID',
    user_login = 'USER_LOGIN', 
    user_password = 'USER_PASS', 
    scope = 'photos, wall, groups, offline')

api = vk.API(session, v='5.53', timeout=10)
print('api is connected')

OWNER_ID = 'OWNER_ID'
albums = api.photos.getAlbums(owner_id = OWNER_ID)

imgDir = './img/'
thumbDir = './thumb/'
for album in albums['items']:
    imageList = os.listdir(imgDir)
    for inImage in imageList:
        os.remove(imgDir + inImage)

    imageList = os.listdir(thumbDir)
    for inImage in imageList:
        os.remove(thumbDir + inImage)
    
    os.remove('./imgInfo.json')

    photos = api.photos.get(owner_id = OWNER_ID, 
        album_id = album['id'], 
        photo_sizes='1')

    downloadImage(photos['items'], isBig = False)

    size = 32,32
    getThumbnail(imgDir, size)
    findSimilarImages(thumbDir)

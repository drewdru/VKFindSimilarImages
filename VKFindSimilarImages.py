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

photos = api.photos.get(owner_id = 'ALBUM_OWNER', 
    album_id = 'ALBUM_ID', 
    photo_sizes='1')

downloadImage(photos['items'], isBig = False)

size = 32,32
getThumbnail('./img/', size)
findSimilarImages('./thumb/')

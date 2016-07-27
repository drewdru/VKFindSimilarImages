import vk
import json
import urllib

session = vk.AuthSession(app_id = 'APP_ID', user_login = 'USER_LOGIN', user_password = 'USER_PASS', scope = 'photos, wall, groups, offline')
api = vk.API(session, v='5.53', timeout=10)
print('api is connected')

photos = api.photos.get(owner_id = 'ALBUM_OWNER', album_id = 'ALBUM_ID', photo_sizes='1')

for image in photos['items']:
	print(image['sizes'][-1])




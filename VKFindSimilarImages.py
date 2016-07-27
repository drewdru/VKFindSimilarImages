import vk
import json
import urllib

session = vk.AuthSession(app_id = 'APP_ID', 
	user_login = 'USER_LOGIN', 
	user_password = 'USER_PASS', 
	scope = 'photos, wall, groups, offline')

api = vk.API(session, v='5.53', timeout=10)
print('api is connected')

photos = api.photos.get(owner_id = 'ALBUM_OWNER', 
	album_id = 'ALBUM_ID', 
	photo_sizes='1')

textFile = open('./textFile.txt','w+')
for index, image in enumerate(photos['items']):
    try:
        print(image['sizes'][0]['src'])
        u = urllib.request.urlopen(image['sizes'][0]['src'])
        raw_data = u.read()
        u.close()
        f = open('./img/' + str(index) + '.jpg','wb+')
        f.write(raw_data)
        f.close()
        text = str(index)+ ': ' + json.dumps(image['sizes'][0]['src'])
        print(text)
        textFile.write(text+'\n')
    except Exception as inst:
        print(inst)
        print('error:' + json.dumps(image['sizes'][0]['src']))
textFile.close()



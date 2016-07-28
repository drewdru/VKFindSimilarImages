import json
import urllib

def downloadImage(images, isBig = True):
    '''
    Download images from vk.com
    '''
    
    size = -1 if isBig else 0
    imgInfo = {
        'img': [
        ]
    }
    for index, image in enumerate(images):
        try:
            u = urllib.request.urlopen(image['sizes'][size]['src'])
            raw_data = u.read()
            u.close()
            f = open('./img/' + str(index) + '.jpg','wb+')
            f.write(raw_data)
            f.close()
            imgInfo['img'].append({
                'index': index,
                'id': image['id'],
                'owner_id': image['owner_id'],
                'album_id': image['album_id'],
                'text': image['text']
            })
        except Exception as inst:
            print(inst)
            print('error:' + json.dumps(image['sizes'][0]['src']))
    with open('imgInfo.json', 'w+') as outfile:
        json.dump(imgInfo, outfile, ensure_ascii=False)
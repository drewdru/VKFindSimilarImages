import json
import urllib
import sys
def downloadImage(images, isBig = True):
    ''' Download images from vk.com '''    
    size = -1 if isBig else 0
    imgInfo = {
        'img': [
        ]
    }
    error404List = []
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
        except urllib.error.HTTPError as err:
            if err.code == 404:
                error404List.append(json.dumps(image['sizes'][0]['src']))
            else:
                print(err)
                print('error:' + json.dumps(image['sizes'][0]['src']))
                sys.exit(1)
        except Exception as inst:
            print(inst)
            print('error:' + json.dumps(image['sizes'][0]['src']))
            sys.exit(2);
    if len(error404List) > 0:
        return error404List

    with open('imgInfo.json', 'w+') as outfile:
        json.dump(imgInfo, outfile, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    
    return error404List
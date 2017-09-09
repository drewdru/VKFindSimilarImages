import json
import urllib
import sys

from PIL import Image
import requests
from io import BytesIO

try:
    from vkBase import pHash
    from vkBase.models.images import Images
except Exception as error:
    import pHash
    from vkBase.models.images import Images

def savePhotosToDB(imagesInfo, isBig=True):
    """ Download images from vk.com 
        :return: images which not found in vk servers
    """
    size = -1 if isBig else 0
    error404List = []
    for imageInfo in imagesInfo:
        try:
            with Images() as imagesModel:
                if imagesModel.checkImgId(imageInfo['id']):
                    imagesModel.update(imageInfo)
                else:
                    response = requests.get(imageInfo['sizes'][size]['src'])
                    img = Image.open(BytesIO(response.content))
                    img = img.convert(mode='RGB')
                    img_hash = pHash.getImageHash(img)
                    imagesModel.insert(imageInfo, img_hash)
        except urllib.error.HTTPError as err:
            print(err)
            print('https://vk.com/photo-2481783_' + str(imageInfo['id']))
        except Exception as err:
            print(err)
            print('https://vk.com/photo-2481783_' + str(imageInfo['id']))

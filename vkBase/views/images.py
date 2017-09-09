
from vkBase.models.images import Images

class ImagesView:
    def getImagesByAlbumID(self, albumID):
        with Images() as imagesModel:
            return imagesModel.getQuery()\
            .filter(Images.album_id == albumID).all()

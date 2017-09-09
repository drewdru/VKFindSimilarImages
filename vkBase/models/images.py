from sqlalchemy import Column, Integer, String
from . import modelsHelper

class Images(modelsHelper.Base):
    __tablename__ = 'images'
    image_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, nullable=False)
    album_id = Column(Integer, nullable=False)
    image_caption = Column(String, nullable=True)
    image_hash = Column(String, nullable=True)

    def __init__(self):
        super().open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().close()

    def getQuery(self):
        return self.session.query(Images)

    def checkImgId(self, image_id):
        query = self.getQuery().filter(Images.image_id == image_id)
        value = query.first()
        return value

    def insert(self, imagesInfo, image_hash):
        try:
            with Images() as imagesModel:
                imagesModel
                imagesModel.image_id = imagesInfo['id']
                imagesModel.owner_id = imagesInfo['owner_id']
                imagesModel.album_id = imagesInfo['album_id']
                imagesModel.image_caption = imagesInfo['text']
                imagesModel.image_hash = image_hash
                self.session.add(imagesModel)
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)

    def update(self, imagesInfo):
        try:
            self.getQuery().filter(Images.image_id == imagesInfo['id'])\
            .update({
                'album_id': imagesInfo['album_id'],
                'image_caption': imagesInfo['text']
            })
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)

    def delete(self, image_id):
        try:
            img = self.getQuery().filter(Images.image_id == image_id).first()
            self.session.delete(img)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)

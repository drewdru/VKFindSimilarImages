from sqlalchemy import Column, Integer, String
from . import modelsHelper

class Albums(modelsHelper.Base):
    __tablename__ = 'albums'
    album_id = Column(Integer, primary_key=True)
    album_type = Column(Integer, nullable=False, default=0)
    album_title = Column(String, nullable=False)
    album_description = Column(String, nullable=False)

    def __init__(self):
        super().open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().close()

    def getQuery(self):
        return self.session.query(Albums)

    def checkAlbumId(self, albumId):
        with Albums() as albumsModel:
            query = self.getQuery().filter(Albums.album_id == albumId)
            value = query.first()
        return value

    def insert(self, albumInfo, albumTypeIndx):
        with Albums() as albumsModel:
            try:
                albumsModel.album_id = albumInfo['id']
                albumsModel.album_type = albumTypeIndx
                albumsModel.album_title = albumInfo['title']
                albumsModel.album_description = albumInfo['description']
                self.session.add(albumsModel)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                print(e)

    def update(self, album_id, album_type, album_title, album_description):
        try:
            self.getQuery().filter(Albums.album_id == album_id)\
            .update({
                'album_type': album_type,
                'album_title': album_title,
                'album_description': album_description,
            })
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)


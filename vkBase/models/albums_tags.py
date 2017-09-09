from sqlalchemy import Column, Integer, String, ForeignKey
from . import modelsHelper

class AlbumsTags(modelsHelper.Base):
    __tablename__ = 'albums_tags'
    albums_tags_id = Column(Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey('albums.album_id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.tags_id'), nullable=False)
    
    def __init__(self):
        super().open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().close()

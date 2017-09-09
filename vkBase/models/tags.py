from sqlalchemy import Column, Integer, String
from . import modelsHelper

class Tags(modelsHelper.Base):
    __tablename__ = 'tags'
    tags_id = Column(Integer, primary_key=True)
    tag_name = Column(String, nullable=False)

    def __init__(self):
        super().open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().close()

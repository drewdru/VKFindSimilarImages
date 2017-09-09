
from vkBase.models.albums import Albums

class AlbumsView:
    def getAlbumsWithoutBlacklist(self):
        with Albums() as albumsModel:
            return albumsModel.getQuery().filter(Albums.album_type != 1).all()


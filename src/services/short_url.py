from models.short_url import ShortUrl as ShortUrlModel
from schemas.short_url import ShortUrlCreate, ShortUrlUpdate
from .base import RepositoryDB, ShortUrlRepositoryDB


class RepositoryShortUrl(ShortUrlRepositoryDB[ShortUrlModel, ShortUrlCreate, ShortUrlUpdate]):
    pass

short_url_crud = RepositoryShortUrl(ShortUrlModel)

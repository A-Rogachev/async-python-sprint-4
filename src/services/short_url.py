from models.short_url import ShortUrl as ShortUrlModel
from schemas.short_url import ShortUrlCreate, ShortUrlDelete

from .base import ShortUrlRepositoryDB


class RepositoryShortUrl(ShortUrlRepositoryDB[ShortUrlModel, ShortUrlCreate, ShortUrlDelete]):
    """
    Бизнес логика для модели ShortUrl.
    """
    pass

short_url_crud = RepositoryShortUrl(ShortUrlModel)

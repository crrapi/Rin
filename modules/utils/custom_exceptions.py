class Error(Exception):
    pass


class ImageNotFound(Error):
    pass


class NSFWException(Error):
    pass


class TagsNotFound(Error):
    pass


class PoolNotFound(Error):
    pass


class InfoNotFound(Error):
    pass

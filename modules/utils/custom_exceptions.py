class Error(Exception):
    pass


class ResourceNotFound(Error):
    pass


class NSFWException(Error):
    pass

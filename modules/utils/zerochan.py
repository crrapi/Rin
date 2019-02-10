from . import scrap

async def _search(query: str, page: int):
    search = scrap.search(query, p=page)
    images = [await search.__anext__() for i in range(scrap.IMAGES_PER_TAG)]
    return images

async def _image(id: str):
    search = await scrap.image(id)
    return search

async def _info(query: str):
    search = await scrap.info(query)
    return search

async def _meta(query: str, page: int):
    search = scrap.meta(query, p=page)
    tags = [await search.__anext__() for i in range(scrap.TAGS_PER_META)]
    return tags
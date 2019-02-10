from . import scrap



async def search(query: str, page: int):
    results = scrap.search(query, p=page)
    images = [await results.__anext__() for i in range(scrap.IMAGES_PER_TAG)]
    return images


async def image(image_id: str):
    images: dict = await scrap.image(image_id)
    return images


async def info(query: str):
    information = await scrap.info(query)
    return information


async def meta(query: str, page: int):
    meta_tags = scrap.meta(query, p=page)
    tags = [await meta_tags.__anext__() for i in range(scrap.TAGS_PER_META)]
    return tags

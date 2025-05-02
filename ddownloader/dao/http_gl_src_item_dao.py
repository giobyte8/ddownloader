from ddownloader.models import HttpGallerySourceItem
from .tortoise.models import DBHttpGallerySourceItem


async def upsert(item: HttpGallerySourceItem) -> HttpGallerySourceItem:
    """
    Upsert an HTTP source item in the database.

    Args:
        item (HttpGallerySourceItem): The HTTP source item to upsert.

    Returns:
        HttpGallerySourceItem: The upserted HTTP source item.
    """
    db_item, is_new = await DBHttpGallerySourceItem.get_or_create(
        source_id=item.source_id,
        filename=item.filename,
        defaults={
            "remote_status": item.remote_status
        }
    )
    item.id = db_item.id

    # Update the item if it already exists
    if not is_new:
        await db_item.\
            update_from_dict({
                "remote_status": item.remote_status
            }).\
            save()

    return item

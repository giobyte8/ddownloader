from uuid import UUID
from ddownloader.models import HttpGallerySourceItem, SrcItemRemoteStatus
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


async def update_status_by_src_id(
        src_id: UUID,
        status: SrcItemRemoteStatus
) -> int:
    """Updates the remote status for all items of a given source.

    Args:
        src_id (UUID): Source's unique identifier.
        status (SrcItemRemoteStatus): Target remote status for items.

    Returns:
        int: Number of rows updated.
    """
    return await DBHttpGallerySourceItem.\
        filter(source_id=src_id).\
        update(remote_status=status)


async def update_status_by_src_id_and_status(
        src_id: UUID,
        old_status: SrcItemRemoteStatus,
        new_status: SrcItemRemoteStatus
) -> int:
    """Updates the remote status for all items of a given source.

    Args:
        src_id (UUID): Source's unique identifier.
        old_status (SrcItemRemoteStatus): Current remote status for items.
        new_status (SrcItemRemoteStatus): Target remote status for items.

    Returns:
        int: Number of rows updated.
    """
    return await DBHttpGallerySourceItem.\
        filter(source_id=src_id, remote_status=old_status).\
        update(remote_status=new_status)


async def update_status_by_src_id_and_filename(
        src_id: UUID,
        filename: str,
        status: SrcItemRemoteStatus
) -> int:
    """Updates the remote status for a specific item of a given source.

    Args:
        src_id (UUID): Source's unique identifier.
        filename (str): Filename of the item.
        status (SrcItemRemoteStatus): Target remote status for the item.

    Returns:
        int: Number of rows updated.
    """
    return await DBHttpGallerySourceItem.\
        filter(source_id=src_id, filename=filename).\
        update(remote_status=status)

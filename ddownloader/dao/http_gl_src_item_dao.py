from opentelemetry import trace
from uuid import UUID
from ddownloader import config as cfg
from ddownloader.models import HttpGallerySourceItem, SrcItemRemoteStatus
from .tortoise.models import DBHttpGallerySourceItem


tracer = trace.get_tracer(cfg.otel_svc_name())


@tracer.start_as_current_span("item_dao.find_by_src_id_and_status")
async def find_by_src_id_and_status(
        src_id: UUID,
        status: SrcItemRemoteStatus
) -> list[HttpGallerySourceItem]:
    """Finds all items of a given source with a specific remote status.

    Args:
        src_id (UUID): Source's unique identifier.
        status (SrcItemRemoteStatus): Remote status to filter items.

    Returns:
        list[HttpGallerySourceItem]: List of items matching the criteria.
    """
    db_items = await DBHttpGallerySourceItem.\
        filter(source_id=src_id, remote_status=status).\
        all()

    items = []
    for db_item in db_items:
        items.append(HttpGallerySourceItem(
            id=db_item.id,
            source_id=db_item.source_id,
            filename=db_item.filename,
            remote_status=db_item.remote_status
        ))

    return items


@tracer.start_as_current_span("item_dao.upsert")
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


@tracer.start_as_current_span("item_dao.update_status_by_src_id")
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


@tracer.start_as_current_span("item_dao.update_status_by_src_id_and_status")
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


@tracer.start_as_current_span("item_dao.update_status_by_src_id_and_filename")
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


@tracer.start_as_current_span("item_dao.delete")
async def delete(item: HttpGallerySourceItem) -> None:
    """Deletes an HTTP source item from the database.

    Args:
        item (HttpGallerySourceItem): The HTTP source item to delete.
    """
    await DBHttpGallerySourceItem.\
        filter(id=item.id).\
        delete()


@tracer.start_as_current_span("item_dao.delete_by_src_id_and_status")
async def delete_by_src_id_and_status(
        src_id: UUID,
        status: SrcItemRemoteStatus
) -> int:
    """Deletes all items of a given source with a specific remote status.

    Args:
        src_id (UUID): Source's unique identifier.
        status (SrcItemRemoteStatus): Remote status to filter items.

    Returns:
        int: Number of rows deleted.
    """
    return await DBHttpGallerySourceItem.\
        filter(source_id=src_id, remote_status=status).\
        delete()

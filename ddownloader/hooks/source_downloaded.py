from ddownloader.dao import http_gl_src_item_dao as item_dao
from ddownloader.models import HttpGallerySource, SrcItemRemoteStatus
from ddownloader.services import file_svc


async def on_source_downloaded(src: HttpGallerySource) -> None:

    # Delete physical files and remove items from DB
    if src.sync_remote_deletes:
        items = await item_dao.find_by_src_id_and_status(
            src.id,
            SrcItemRemoteStatus.UNKNOWN
        )

        for item in items:
            await file_svc.delete_file(item)

        # Delete items from DB
        await item_dao.delete_by_src_id_and_status(
            src.id,
            SrcItemRemoteStatus.UNKNOWN
        )

    # Mark items as NOT_FOUND
    else:
        await item_dao.update_status_by_src_id_and_status(
            src.id,
            SrcItemRemoteStatus.UNKNOWN,
            SrcItemRemoteStatus.NOT_FOUND
        )

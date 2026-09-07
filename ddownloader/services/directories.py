from ..dao import http_gallery_source_dao as src_dao
from ..models import Directory


async def all() -> list[Directory]:
    dirs = []

    sources = await src_dao.all(order_by='content_path')
    current_dir = None
    for src in sources:
        if not current_dir or current_dir.path != src.content_path:
            current_dir = Directory(path=src.content_path)
            dirs.append(current_dir)

        current_dir.sources.append(src)

    return dirs

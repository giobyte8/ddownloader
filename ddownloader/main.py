import asyncio
import os
import sys
from hypercorn.config import Config
from hypercorn.asyncio import serve

# If package was not imported from other module
# and package has not been yet installed
if not __package__ and not hasattr(sys, "frozen"):
    central_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    sys.path.insert(0, os.path.realpath(central_root))

from ddownloader.dao import http_gallery_source_dao as gallery_src_dao
from ddownloader.download import download_svc
from ddownloader.web.app import app as downloader_app


__bg_tasks = set()


@downloader_app.before_serving
async def before_serving():
    gl_sources = await gallery_src_dao.all()

    dl_task = asyncio.create_task(download_svc.start(gl_sources))
    __bg_tasks.add(dl_task)


@downloader_app.after_serving
async def shutdown():
    for task in __bg_tasks:
        task.cancel()


if __name__ == "__main__":
    downloader_app.run(host='0.0.0.0', port=5001)

import asyncio
import logging
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

import ddownloader.config as cfg
from ddownloader.dao import database
from ddownloader.download import download_svc
from ddownloader.metrics import tracker as metrics_tracker
from ddownloader.web.app import app as downloader_app


log = logging.getLogger("ddownloader.quart.app")
__bg_tasks = set()


@downloader_app.before_serving
async def before_serving():
    await database.init()

    dl_task = asyncio.create_task(download_svc.start())
    __bg_tasks.add(dl_task)


@downloader_app.after_serving
async def shutdown():
    for task in __bg_tasks:
        task.cancel()

    await metrics_tracker.cleanup()


if __name__ == "__main__":
    if cfg.app_env() in ["prod", "production"]:
        hypercorn_cfg = Config()
        hypercorn_cfg.accesslog = log
        hypercorn_cfg.errorlog  = log
        hypercorn_cfg.bind = [f"0.0.0.0:{ cfg.app_port() }"]

        asyncio.run(serve(downloader_app, hypercorn_cfg))
    else:
        downloader_app.run(
            host='0.0.0.0',
            port=cfg.app_port())

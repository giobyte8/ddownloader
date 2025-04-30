#!/usr/bin/env python3
# This script should be executed as an entrypoint by 'download tools'
# to let ddownloader know that a file has been downloaded.
#
# It is designed to be executed from project root directory.

import aiohttp
import asyncio
import os
import sys

# Add project root to sys.path
if __name__ == '__main__':
    dl_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dl_root = os.path.dirname(dl_root)
    sys.path.insert(0, os.path.realpath(dl_root))

import ddownloader.config as cfg


source_id = sys.argv[1]
filename = sys.argv[2]
url = (
    f"http://localhost:{ cfg.app_port() }/"
    f"api/hooks/source/{ source_id }/downloaded"
)

async def post_file_downloaded():
    """Post to ddownloader API that a file has been downloaded."""

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"filename": filename}) as resp:
            if resp.status != 201:
                print('Failed to notify ddownloader about downloaded file')
                sys.exit(1)

asyncio.run(post_file_downloaded())

#!/usr/bin/env python3
# This script should be executed as an entrypoint by 'download tools'
# to let ddownloader know that a file has been downloaded.
#
# It is designed to be executed from project root directory.

import logging
import os
import sys

# Add project root to sys.path
if __name__ == '__main__':
    dl_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dl_root = os.path.dirname(dl_root)
    sys.path.insert(0, os.path.realpath(dl_root))

#from http_downloader.messaging import producer


logger = logging.getLogger(__name__)
source_id = sys.argv[1]
filename = sys.argv[2]


print(f"Running 'file downloaded' hook for: {filename}")
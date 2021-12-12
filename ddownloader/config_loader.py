"""
Utilities to read and process env config
"""
import os
from dotenv import load_dotenv


load_dotenv()


def get_db_path():
    return os.getenv('DB_PATH')

def downloads_dir():
    return os.getenv('DOWNLOADS_PATH')

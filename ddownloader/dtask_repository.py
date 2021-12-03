import contextlib
import sqlite3
import ddownloader.config_loader as dconfig
from ddownloader.downloader import DownloadTask
from ddownloader.log_utils import logger


CREATE_TABLE_IF_NOT_EXISTS = """
    CREATE TABLE IF NOT EXISTS download_task(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url VARCHAR(5000) NOT NULL,
        target_path VARCHAR(5000) NOT NULL,
        
        total_size REAL DEFAULT 0,
        downloaded_size REAL DEFAULT 0,
        status VARCHAR(50),
        file_hash VARCHAR(1000),
        err_message VARCHAR(5000)
    )
"""

FIND_BY_ID = """
    SELECT * FROM download_task
    WHERE id = :id
"""

INSERT_DTASK = """
    INSERT INTO download_task VALUES(
        null,
        :url,
        :target_path,
        :total_size,
        :downloaded_size,
        :status,
        :file_hash,
        null)
"""

UPDATE_DTASK = """
    UPDATE download_task
    SET
        total_size=:total_size,
        downloaded_size=:downloaded_size,
        status=:status,
        err_message=:err_message
    WHERE id = :id
"""

_db_path = dconfig.get_db_path()


class DBError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__("DB Error: {}".format(message))


@contextlib.contextmanager
def _db_con():
    """Context manager to wrap db connections and
    query exceptions.

    Yields:
        [sqlite3.Connection]: SQLite database connection
    """
    try:
        con = sqlite3.connect(_db_path)

        with con:
            con.row_factory = sqlite3.Row
            yield con
        con.close()
    except Exception as e:
        raise(DBError(e))


def init():
    """Initializes database
    """
    logger.info('Database path: %s', _db_path)

    with _db_con() as con:
        con.execute(CREATE_TABLE_IF_NOT_EXISTS)

def save(dtask: DownloadTask):
    """Upserts a download task into database. If id is greater than 0,
    then task will be updated, otherwise will be inserted.

    In case of insertion, the id will be automatically updated in
    given object as a side effect.

    Args:
        dtask (DownloadTask): Task to upsert into database
    """
    with _db_con() as con:
        if dtask.id > 0:
            con.execute(UPDATE_DTASK, {
                "total_size": dtask.total_size,
                "downloaded_size": dtask.downloaded_size,
                "status": dtask.status.value,
                "err_message": dtask.error_message,
                "id": dtask.id
            })
        else:
            cur = con.execute(INSERT_DTASK, {
                "url": dtask.url,
                "target_path": dtask.target_path,
                "total_size": dtask.total_size,
                "downloaded_size": dtask.downloaded_size,
                "status": dtask.status.value,
                "file_hash": dtask.file_hash
            })

            dtask.id = cur.lastrowid

def paginate(page_size: int = 30, page: int = 0):
    pass

def find_by_id(id: int) -> DownloadTask:
    with _db_con() as con:
        cur = con.execute(FIND_BY_ID, {'id': id})
        
        row = cur.fetchone()
        if not row:
            return None

        dtask = DownloadTask(row['url'], row['target_path'])
        dtask.id = row['id']
        dtask.total_size = row['total_size']
        dtask.downloaded_size = row['downloaded_size']
        dtask.file_hash = row['file_hash']
        dtask.err_message = row['err_message']
        return dtask

def delete_by_id(id: int):
    pass


## Initialize database upon module first execution
init()
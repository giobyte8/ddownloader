from huey import SqliteHuey
import huey

import ddownloader.dtask_repository as dtask_repo
from ddownloader.config_loader import get_db_path
from ddownloader.log_utils import logger
from ddownloader import downloader


_db_path = get_db_path()
logger.info('Huey database: %s', _db_path)
huey = SqliteHuey(_db_path)


@huey.task()
def download(dtask_id: int):
    dtask = dtask_repo.find_by_id(dtask_id)

    def _reload_status():
        db_task = dtask_repo.find_by_id(dtask_id)
        dtask.status = db_task.status

    downloader.download(
        dtask,
        on_update=lambda: dtask_repo.save(dtask),
        reload_status=_reload_status
    )

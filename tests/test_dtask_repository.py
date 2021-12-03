from ddownloader.downloader import DownloadTask
import os
import pytest
import ddownloader.dtask_repository as dtask_repo

@pytest.fixture(scope='module')
def test_database():
    """Takes care of removing test database file
    upon tests completion.
    """
    db_path = os.getenv('DB_PATH')
    print('Test database path: {}'.format(db_path))

    # Yield to execute tests
    yield

    # Teardown after tests execution
    os.remove(db_path)
    

def test_init(test_database):
    """DB should be automatically initialized
    during first dtask_repository module import
    """
    DTASK_TABLE_NAME = 'download_task'
    GET_TABLE_BY_NAME = """
        SELECT * FROM sqlite_master
        WHERE type = 'table'
        AND name = :table_name
    """

    with dtask_repo._db_con() as con:
        cur = con.execute(GET_TABLE_BY_NAME, {
            'table_name': DTASK_TABLE_NAME
        })

        row = cur.fetchone()
        assert row is not None
        assert row['name'] == DTASK_TABLE_NAME


def test_save_insert(test_database):
    dtask = DownloadTask('fake_url.com', 'fake_destination')
    dtask_repo.save(dtask)

    # Id must have been autogenerated on record insertion
    assert dtask.id == 1


def test_find_by_id(test_database):
    dtask = DownloadTask('fake_saved_url.com', 'fake_saved_destination')
    dtask_repo.save(dtask)

    db_dtask = dtask_repo.find_by_id(dtask.id)
    assert db_dtask.id == dtask.id
    assert db_dtask.url == dtask.url
    assert db_dtask.target_path == dtask.target_path
import logging
from aiohttp import ClientSession
from aiohttp import client_exceptions as aiohttp_ex
from ddownloader import config as cfg


log = logging.getLogger(__name__)
_aiohttp_session: ClientSession | None = None
_NOTIF_URL = f"{ cfg.ct_api_url() }/notifications"


def _http() -> ClientSession:
    """Retrieves the shared http session for all Central requests
    Note: A session contains a cookie storage and connection pool,
    hence, cookies and connections are shared between HTTP requests.

    Returns:
        ClientSession: Singleton aiohttp client session
    """
    global _aiohttp_session

    if not _aiohttp_session or _aiohttp_session.closed:
        log.debug('Creating new aiohttp client session for Central')

        headers = {'Authorization': f'Bearer { cfg.ct_api_key() }'}
        _aiohttp_session = ClientSession(headers=headers)
    return _aiohttp_session


async def cleanup():
    global _aiohttp_session
    if _aiohttp_session and not _aiohttp_session.closed:
        await _aiohttp_session.close()


async def notify(msg: str) -> None:
    """Posts a notification to Central

    Args:
        msg (str): Notification content
    """
    req_body = { "title": "ddownloader", "content": msg }

    try:
        async with _http().post(_NOTIF_URL, json=req_body) as res:
            if res.status == 201:
                log.debug('Notification sent to Central')
            else:
                log.error(
                    'Failed to send notification to Central: %s: %s',
                    res.status,
                    await res.text()
                )
    except aiohttp_ex.ClientOSError as e:
        log.error('aiohttp error: %s', e)
    except Exception as e:
        log.error('Error while posting notification to Central: %s', e)



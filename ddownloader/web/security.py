from functools import wraps
from quart import (
    has_request_context,
    request
)
from typing import Any, Callable
from werkzeug.exceptions import Unauthorized
from ddownloader import config as cfg


def api_key_hooks_required() -> Callable:
    """A decorator to restrict route access to requests with an API key.

    The API key should be provided in the 'Authorization' header with the value
    'Bearer <api_key>'. If the API key is invalid or missing, a 401 Unauthorized
    response is returned.

    Note that it is important that this decorator be
    wrapped by the route decorator and not vice versa, as below.

    .. code-block:: python

        @app.route('/')
        @api_key_hooks_required()
        async def index():
            ...

    Returns:
        Callable: The decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if has_request_context():
                if 'Authorization' not in request.headers:
                    raise Unauthorized('API key is missing.')

                auth_header = request.headers['Authorization']
                if not auth_header.startswith('Bearer '):
                    raise Unauthorized('API key is missing.')

                api_key = auth_header.split(' ')[1]
                if await _validate_api_key(api_key):
                    return await func(*args, **kwargs)
                else:
                    raise Unauthorized('API key is invalid.')
            else:
                raise RuntimeError(
                    'Decorator must be used within a request context.'
                )

        return wrapper
    return decorator


async def _validate_api_key(key: str) -> bool:
    """Validate the provided API key.

    Args:
        key (str): The API key to validate.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    return cfg.api_key_hooks() == key

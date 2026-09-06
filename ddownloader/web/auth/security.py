import logging
from functools import wraps
from quart import (
    has_request_context,
    redirect,
    request,
    session,
    url_for
)
from typing import Any, Callable
from werkzeug.exceptions import Unauthorized
from werkzeug.security import check_password_hash
from ddownloader import config as cfg

logger = logging.getLogger(__name__)

SESSION_KEY = "authenticated"


def verify_credentials(username: str, password: str) -> bool:
    """Validate the provided username/password against the configured
    single shared admin account.

    Args:
        username (str): Submitted username.
        password (str): Submitted plaintext password.

    Returns:
        bool: True if credentials match the configured account.
    """
    expected_username = cfg.web_auth_username()
    expected_hash = cfg.web_auth_password_hash()
    if not expected_username or not expected_hash:
        return False

    if username != expected_username:
        return False

    return check_password_hash(expected_hash, password)


async def require_login():
    """Blueprint ``before_request`` guard.

    Redirects unauthenticated requests to the login page, preserving the
    originally requested path in the ``next`` query parameter so the user
    is sent back to where they intended to go after logging in.

    Intended usage:

    .. code-block:: python

        sources_app.before_request(require_login)

    Returns:
        Response | None: A redirect response when not authenticated,
        otherwise None to let the request continue.
    """
    if session.get(SESSION_KEY):
        return None

    return redirect(url_for("auth.login", next=request.path))


def ensure_web_auth_configured() -> None:
    """Fail fast at startup if web auth is not fully configured.

    Raises:
        RuntimeError: If any required web auth setting is missing.
    """
    missing = [
        name for name, value in (
            ("SECRET_KEY", cfg.secret_key()),
            ("WEB_AUTH_USERNAME", cfg.web_auth_username()),
            ("WEB_AUTH_PASSWORD_HASH", cfg.web_auth_password_hash()),
        )
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing required web auth configuration: "
            f"{', '.join(missing)}. Set them in your environment/.env file. "
            "Generate a password hash with scripts/gen_password_hash.py."
        )


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


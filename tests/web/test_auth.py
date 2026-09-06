import asyncio
import os
from functools import wraps
from unittest.mock import AsyncMock, patch
from werkzeug.security import generate_password_hash

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("WEB_AUTH_USERNAME", "admin")
os.environ.setdefault("WEB_AUTH_PASSWORD_HASH", generate_password_hash("s3cr3t"))

from ddownloader.web.app import app as downloader_app  # noqa: E402


def async_test(fn):
    """Run an async test function to completion with asyncio.run.

    The project's test stack does not include pytest-asyncio, so plain
    ``async def`` test functions are never awaited by pytest.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return asyncio.run(fn(*args, **kwargs))

    return wrapper


def _test_client():
    downloader_app.config["TESTING"] = True
    return downloader_app.test_client()


@async_test
async def test_protected_route_redirects_to_login_when_unauthenticated():
    client = _test_client()

    response = await client.get("/sources/")

    assert response.status_code == 302
    assert response.headers["Location"].startswith("/login")


@async_test
async def test_login_with_invalid_credentials_is_rejected():
    client = _test_client()

    response = await client.post("/login", form={
        "username": "admin",
        "password": "wrong-password",
    })

    assert response.status_code == 401


@async_test
async def test_login_grants_access_to_protected_route():
    client = _test_client()

    with patch(
        "ddownloader.web.app_sources.src_dao.all",
        new=AsyncMock(return_value=[]),
    ):
        login_response = await client.post("/login", form={
            "username": "admin",
            "password": "s3cr3t",
            "next": "/sources/",
        })
        assert login_response.status_code == 302
        assert login_response.headers["Location"] == "/sources/"

        protected_response = await client.get("/sources/")
        assert protected_response.status_code == 200


@async_test
async def test_logout_revokes_access():
    client = _test_client()

    with patch(
        "ddownloader.web.app_sources.src_dao.all",
        new=AsyncMock(return_value=[]),
    ):
        await client.post("/login", form={
            "username": "admin",
            "password": "s3cr3t",
        })

        logout_response = await client.get("/logout")
        assert logout_response.status_code == 302
        assert logout_response.headers["Location"] == "/login"

        protected_response = await client.get("/sources/")
        assert protected_response.status_code == 302
        assert protected_response.headers["Location"].startswith("/login")

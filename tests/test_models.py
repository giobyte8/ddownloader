import pytest

from ddownloader.models import HttpGallerySource


@pytest.mark.parametrize(
    "content_path,expected",
    [
        ("photos/old_gallery-2020", "Old gallery 2020"),
        ("pics/my_gallery_Name",    "my gallery Name"),
        ("leading/slash_name/",     "Slash name"),
        ("",                        ""),
        ("weird/---__",             "---__"),
    ],
)
def test_http_gallery_source_name(content_path, expected):
    src = HttpGallerySource(
        content_path=content_path,
        url="http://example.com",
        sync_remote_deletes=False,
        download_schedule="0 0 * * *",
        download_enabled=False,
    )

    assert src.name == expected

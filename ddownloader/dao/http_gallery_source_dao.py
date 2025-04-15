from ddownloader.models import HttpGallerySource


async def all() -> list[HttpGallerySource]:
    """Get all HTTP gallery sources from the database.
    """

    return [
        HttpGallerySource(
            url="https://example.com",
            content_path="/path/to/content",
            sync_remote_deletes=True,
        ),
        HttpGallerySource(
            url="https://example2.com",
            content_path="/path/to/content2",
            sync_remote_deletes=False,
        ),
    ]
import logging
from tortoise.models import Model
from tortoise import fields


logger = logging.getLogger(__name__)


class DBHttpGallerySource(Model):
    """Database Tortoise model for HTTP sources."""

    id = fields.UUIDField(primary_key=True)
    url = fields.CharField(max_length=5000)
    content_path = fields.CharField(max_length=5000)
    sync_remote_deletes = fields.BooleanField(default=True)

    class Meta:
        table = "http_gallery_source"

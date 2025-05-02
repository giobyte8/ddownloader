from tortoise.models import Model
from tortoise import fields
from ddownloader.models import SrcItemRemoteStatus


class DBHttpGallerySource(Model):
    """Database Tortoise model for HTTP sources."""

    id = fields.UUIDField(primary_key=True)
    url = fields.CharField(max_length=5000)
    content_path = fields.CharField(max_length=5000)
    sync_remote_deletes = fields.BooleanField(default=True)

    class Meta:
        table = "http_gallery_source"


class DBHttpGallerySourceItem(Model):
    """Database Tortoise model for HTTP source items."""

    id = fields.UUIDField(primary_key=True)
    filename = fields.CharField(max_length=5000)
    remote_status: SrcItemRemoteStatus = fields.CharEnumField(
        SrcItemRemoteStatus,
        default=SrcItemRemoteStatus.FOUND,
        max_length=255
    )
    source = fields.ForeignKeyField(
        "models.DBHttpGallerySource",
        related_name="items",
        on_delete=fields.CASCADE
    )

    class Meta:
        table = "http_gallery_source_item"

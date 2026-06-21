from datetime import datetime
from tortoise.models import Model
from tortoise import fields
from ddownloader.models import SrcItemRemoteStatus


class DBHttpGallerySource(Model):
    """Database Tortoise model for HTTP sources."""

    id = fields.UUIDField(primary_key=True)
    url = fields.CharField(max_length=5000)
    content_path = fields.CharField(max_length=5000)
    sync_remote_deletes = fields.BooleanField(default=True)

    # Cron string defining the download schedule for this source,
    # e.g. "0 0 * * SUN" for weekly on Sundays at midnight.
    # Nullable — a source without a schedule can only be downloaded manually.
    download_schedule = fields.CharField(max_length=255, null=True, default=None)

    download_enabled = fields.BooleanField()

    # Not persisted in database. Used to store aggregated value retrieved
    # during queries that join with APScheduler jobs.
    job_next_run_time: float | None

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


class DBGallerySrcDownloadJob(Model):
    """Database Tortoise model for gallery source download jobs."""

    id = fields.UUIDField(primary_key=True)
    source = fields.ForeignKeyField(
        "models.DBHttpGallerySource",
        related_name="download_jobs",
        on_delete=fields.CASCADE
    )
    started_at = fields.DatetimeField(auto_now_add=True)
    completed_at = fields.DatetimeField(null=True)

    class Meta:
        table = "gallery_src_download_job"


class DBDownloadJobDownloadedFile(Model):
    """Database Tortoise model for files downloaded by a job."""

    id = fields.UUIDField(primary_key=True)
    job = fields.ForeignKeyField(
        "models.DBGallerySrcDownloadJob",
        related_name="downloaded_files",
        on_delete=fields.CASCADE
    )
    src_item = fields.ForeignKeyField(
        "models.DBHttpGallerySourceItem",
        related_name="downloaded_files",
        on_delete=fields.CASCADE
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "download_job_downloaded_file"


class DBDownloadJobSkippedFile(Model):
    """Database Tortoise model for files skipped by a job."""

    id = fields.UUIDField(primary_key=True)
    job = fields.ForeignKeyField(
        "models.DBGallerySrcDownloadJob",
        related_name="skipped_files",
        on_delete=fields.CASCADE
    )
    src_item = fields.ForeignKeyField(
        "models.DBHttpGallerySourceItem",
        related_name="skipped_files",
        on_delete=fields.CASCADE
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "download_job_skipped_file"


class DBAPSchedulerJob(Model):
    """Database Tortoise model for APScheduler jobs."""

    id = fields.CharField(max_length=255, primary_key=True)
    next_run_time = fields.FloatField(null=True)

    class Meta:
        table = "apscheduler_jobs"

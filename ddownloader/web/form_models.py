from cron_descriptor import get_description
from apscheduler.triggers.cron import CronTrigger
from pydantic import BaseModel, HttpUrl, field_validator


class CreateSourceForm(BaseModel):
    url: HttpUrl
    content_path: str
    download_schedule: str | None = None
    sync_remote_deletes: bool = False
    download_enabled: bool = False

    @field_validator("content_path", mode="after")
    @classmethod
    def no_path_traversal(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Content path is required")
        if v.startswith("/"):
            raise ValueError("Path must be relative, not absolute")
        if ".." in v:
            raise ValueError("Path must not contain '..'")
        return v

    @field_validator("download_schedule", mode="before")
    @classmethod
    def valid_cron(cls, v: str | None) -> str | None:
        if not v or not v.strip():
            return None
        try:
            CronTrigger.from_crontab(v)
        except Exception:
            raise ValueError("Must be a valid cron expression (e.g. '0 0 * * SUN')")
        return v

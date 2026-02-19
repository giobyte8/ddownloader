from opentelemetry import trace
from uuid import UUID
from ddownloader import config as cfg
from ddownloader.models import DownloadJobSkippedFile
from .tortoise.models import DBDownloadJobSkippedFile


tracer = trace.get_tracer(cfg.otel_svc_name())


@tracer.start_as_current_span("download_job_skipped_file_dao.find_by_job_id")
async def find_by_job_id(job_id: UUID) -> list[DownloadJobSkippedFile]:
    db_rows = await DBDownloadJobSkippedFile.filter(job_id=job_id).all()

    rows: list[DownloadJobSkippedFile] = []
    for db_row in db_rows:
        rows.append(DownloadJobSkippedFile(
            id=db_row.id,
            job_id=db_row.job_id,
            src_item_id=db_row.src_item_id,
            created_at=db_row.created_at,
        ))

    return rows


@tracer.start_as_current_span("download_job_skipped_file_dao.find_by_src_item_id")
async def find_by_src_item_id(src_item_id: UUID) -> list[DownloadJobSkippedFile]:
    db_rows = await DBDownloadJobSkippedFile.filter(src_item_id=src_item_id).all()

    rows: list[DownloadJobSkippedFile] = []
    for db_row in db_rows:
        rows.append(DownloadJobSkippedFile(
            id=db_row.id,
            job_id=db_row.job_id,
            src_item_id=db_row.src_item_id,
            created_at=db_row.created_at,
        ))

    return rows


@tracer.start_as_current_span("download_job_skipped_file_dao.insert")
async def insert(row: DownloadJobSkippedFile) -> DownloadJobSkippedFile:
    db_row = await DBDownloadJobSkippedFile.create(
        job_id=row.job_id,
        src_item_id=row.src_item_id,
    )
    row.id = db_row.id
    row.created_at = db_row.created_at
    return row

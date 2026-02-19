from opentelemetry import trace
from uuid import UUID
from ddownloader import config as cfg
from ddownloader.models import DownloadJobDownloadedFile
from .tortoise.models import DBDownloadJobDownloadedFile


tracer = trace.get_tracer(cfg.otel_svc_name())


@tracer.start_as_current_span("download_job_downloaded_file_dao.find_by_job_id")
async def find_by_job_id(job_id: UUID) -> list[DownloadJobDownloadedFile]:
    db_rows = await DBDownloadJobDownloadedFile.filter(job_id=job_id).all()

    rows: list[DownloadJobDownloadedFile] = []
    for db_row in db_rows:
        rows.append(DownloadJobDownloadedFile(
            id=db_row.id,
            job_id=db_row.job_id,
            src_item_id=db_row.src_item_id,
            created_at=db_row.created_at,
        ))

    return rows


@tracer.start_as_current_span("download_job_downloaded_file_dao.find_by_src_item_id")
async def find_by_src_item_id(src_item_id: UUID) -> list[DownloadJobDownloadedFile]:
    db_rows = await DBDownloadJobDownloadedFile.filter(src_item_id=src_item_id).all()

    rows: list[DownloadJobDownloadedFile] = []
    for db_row in db_rows:
        rows.append(DownloadJobDownloadedFile(
            id=db_row.id,
            job_id=db_row.job_id,
            src_item_id=db_row.src_item_id,
            created_at=db_row.created_at,
        ))

    return rows


@tracer.start_as_current_span("download_job_downloaded_file_dao.insert")
async def insert(row: DownloadJobDownloadedFile) -> DownloadJobDownloadedFile:
    db_row = await DBDownloadJobDownloadedFile.create(
        job_id=row.job_id,
        src_item_id=row.src_item_id,
    )
    row.id = db_row.id
    row.created_at = db_row.created_at
    return row

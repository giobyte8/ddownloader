from opentelemetry import trace
from uuid import UUID
from ddownloader import config as cfg
from ddownloader.models import DownloadJobDownloadedFile, HttpGallerySourceItem
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


@tracer.start_as_current_span("download_job_downloaded_file_dao.count")
async def count(job_id: UUID) -> int:
    return await DBDownloadJobDownloadedFile.filter(job_id=job_id).count()


@tracer.start_as_current_span("download_job_downloaded_file_dao.page")
async def page(
    job_id: UUID,
    page_number: int,
    page_size: int = 30,
) -> list[DownloadJobDownloadedFile]:
    if page_number < 1:
        page_number = 1
    if page_size < 1:
        page_size = 30

    offset = (page_number - 1) * page_size

    db_rows = await (
        DBDownloadJobDownloadedFile
        .filter(job_id=job_id)
        .prefetch_related("src_item")
        .order_by("-created_at")
        .offset(offset)
        .limit(page_size)
        .all()
    )

    rows: list[DownloadJobDownloadedFile] = []
    for db_row in db_rows:
        src_item = None
        if getattr(db_row, "src_item", None) is not None:
            src_item = HttpGallerySourceItem(
                id=db_row.src_item.id,
                source_id=db_row.src_item.source_id,
                filename=db_row.src_item.filename,
                remote_status=db_row.src_item.remote_status,
            )

        rows.append(DownloadJobDownloadedFile(
            id=db_row.id,
            job_id=db_row.job_id,
            src_item_id=db_row.src_item_id,
            created_at=db_row.created_at,
            src_item=src_item,
        ))

    return rows

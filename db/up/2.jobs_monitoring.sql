CREATE TABLE IF NOT EXISTS gallery_src_download_job(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,

    FOREIGN KEY (source_id) REFERENCES http_gallery_source(id)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS download_job_downloaded_file(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL,
    src_item_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    FOREIGN KEY (job_id) REFERENCES gallery_src_download_job(id)
      ON DELETE CASCADE,
    FOREIGN KEY (src_item_id) REFERENCES http_gallery_source_item(id)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS download_job_skipped_file(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL,
    src_item_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    FOREIGN KEY (job_id) REFERENCES gallery_src_download_job(id)
      ON DELETE CASCADE,
    FOREIGN KEY (src_item_id) REFERENCES http_gallery_source_item(id)
      ON DELETE CASCADE
);

ALTER TABLE http_gallery_source_item
    ADD COLUMN created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ADD COLUMN updated_at TIMESTAMPTZ;

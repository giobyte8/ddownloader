CREATE TABLE IF NOT EXISTS http_gallery_source(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url VARCHAR(5000) NOT NULL,
    content_path VARCHAR(5000) NOT NULL,
    sync_remote_deletes BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS http_single_file_source(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url VARCHAR(5000) NOT NULL,
    dst_path VARCHAR(5000) NOT NULL
);

CREATE TABLE IF NOT EXISTS http_gallery_source_item(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL,
    filename VARCHAR(5000) NOT NULL,
    remote_status VARCHAR(255) NOT NULL,

    FOREIGN KEY (source_id) REFERENCES http_gallery_source(id)
      ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_http_gallery_source_item_remote_status
  ON http_gallery_source_item(remote_status);

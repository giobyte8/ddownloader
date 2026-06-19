ALTER TABLE http_gallery_source
  ALTER COLUMN download_schedule DROP NOT NULL,
  ALTER COLUMN download_schedule DROP DEFAULT;

import json
import logging
import uuid
import os
import subprocess
import ddownloader.config as cfg
from ddownloader import futils
from ddownloader.models import HttpGallerySource


async def download(src: HttpGallerySource) -> None:
    gl_content_path = os.path.join(cfg.galleries_path(), src.content_path)
    futils.assert_dir_exists(gl_content_path)

    cmd_file_skipped = [
        'python',
        'ddownloader/hooks/file_skipped.py',
        str(src.id),
        '{_filename}']

    cmd_file_downloaded = [
        'python',
        'ddownloader/hooks/file_downloaded.py',
        str(src.id),
        '{_filename}']

    gdl_cfg_file_path = GDLCfgFileBuilder() \
        .hook('skip', cmd_file_skipped) \
        .hook('after', cmd_file_downloaded) \
        .build()

    # REMOVE -q param for more verbose output from gallery-dl subprocess
    p = subprocess.run([
        'gallery-dl',
        '-q',
        '-D', gl_content_path,
        '-c', gdl_cfg_file_path,
        str(src.url)
    ])

    # Comment remove file step for debugging purposes
    os.remove(gdl_cfg_file_path)


class GDLCfgFileBuilder:
    """Builder for 'gallery-dl' JSON config file."""

    def __init__(self):
        cfg_template_path = os.path.join(cfg.config_path(), "gdl-base.json")
        futils.assert_file_exists(cfg_template_path)
        futils.assert_dir_exists(cfg.runtime_path())

        # Load config template as a dict
        with open(cfg_template_path, 'r') as cfg_template:
            self.j_config = json.loads(cfg_template.read())

    def build(self) -> str:
        cfg_file_path = os.path.join(
            cfg.runtime_path(),
            f'{ str(uuid.uuid4()) }.json'
        )

        with open(cfg_file_path, 'w') as cfg_file:
            cfg_file.write(json.dumps(self.j_config))
        return cfg_file_path

    def hook(self, event: str, command: list[str]) -> 'GDLCfgFileBuilder':
        postprocessors = self.j_config['extractor']['postprocessors']

        for postprocessor in postprocessors:
            if postprocessor['event'] == event:
                postprocessor['command'] = command
                break

        return self

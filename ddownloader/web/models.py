from dataclasses import dataclass
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from ddownloader.downloader import DownloadTask

from ddownloader.web.validators import safe_target_path


dtask_schema = {
    'type': 'object',
    'required': ['url', 'target_path'],
    'properties': {
        'url': {
            'type': 'string',
            'format': 'uri',
            'pattern': '^(https?|http)://'
        },
        'target_path': {
            'type': 'string'
        },
        'file_hash': {
            'type': 'string'
        }
    }
}

class PostDownloadTaskRequest(Inputs):
    json = [JsonSchema(schema=dtask_schema), safe_target_path]

@dataclass
class DownloadTasksPage():
    page: int
    page_size: int
    total_count: int
    dtasks: list[DownloadTask]

    def to_dict(self) -> dict:
        return {
            'page': self.page,
            'page_size': self.page_size,
            'total_count': self.total_count,
            'dtasks': [dtask.to_dict() for dtask in self.dtasks]
        }

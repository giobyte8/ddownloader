from dataclasses import dataclass
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from ddownloader.downloader import DownloadTask

from ddownloader.web.validators import (
    dtask_exists,
    safe_target_path,
    target_path_not_exists
)


dtask_schema = {
    'type': 'object',
    'required': ['url', 'relative_target_path'],
    'properties': {
        'url': {
            'type': 'string',
            'format': 'uri',
            'pattern': '^(https?|http)://'
        },
        'relative_target_path': {
            'type': 'string'
        },
        'file_hash': {
            'type': 'string'
        }
    }
}

dtask_update_schema = {
    'type': 'object',
    'required': ['status'],
    'properties': {
        'status': {
            'type': 'string',
            'enum': [
                'Queued',
                'Paused'
            ]
        }
    }
}

class PostDownloadTaskRequest(Inputs):
    json = [
        JsonSchema(schema=dtask_schema),
        safe_target_path,
        target_path_not_exists
    ]

class PutDownloadTaskRequest(Inputs):
    json = [JsonSchema(schema=dtask_update_schema)]
    rule = {
        'dtask_id': [dtask_exists]
    }


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

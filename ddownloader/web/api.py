from flask import request
from flask.json import jsonify
from ddownloader.downloader import DownloadTask

import ddownloader.dtask_repository as dtask_repo
from ddownloader.web.app import app
from ddownloader.web.errors import DTaskValidationError
from ddownloader.web.models import (
    DownloadTasksPage,
    PostDownloadTaskRequest
)


@app.errorhandler(DTaskValidationError)
def on_dtask_validation_error(err: DTaskValidationError):
    res = jsonify(err.to_dict())
    res.status_code = err.status_code
    return res


@app.route('/tasks', methods=['GET'])
def get_tasks():
    page = request.args.get('page', 1)
    page_size = request.args.get('page_size', 30)

    dtasks = dtask_repo.paginate(page_size, page)
    count = dtask_repo.count()

    dtasks_page = DownloadTasksPage(
        page,
        page_size,
        count,
        dtasks
    )
    return jsonify(dtasks_page.to_dict())


@app.route('/tasks', methods=['POST'])
def post_task():
    inputs = PostDownloadTaskRequest(request)
    if not inputs.validate():
        raise DTaskValidationError(inputs.errors[0])

    dtask = DownloadTask(
        url=request.json.get('url'),
        target_path=request.json.get('target_path'),
        file_hash=request.json.get('file_hash', None)
    )

    dtask_repo.save(dtask)
    return jsonify(dtask.to_dict())

from flask import request
from flask.json import jsonify

from ddownloader.web import dtask_service
from ddownloader.web.app import app
from ddownloader.web.errors import DTaskValidationError
from ddownloader.web.models import PostDownloadTaskRequest


@app.errorhandler(DTaskValidationError)
def on_dtask_validation_error(err: DTaskValidationError):
    res = jsonify(err.to_dict())
    res.status_code = err.status_code
    return res


@app.route('/tasks', methods=['GET'])
def get_tasks():
    page = request.args.get('page', 1)
    page_size = request.args.get('page_size', 30)

    dtasks_page = dtask_service.get_page(page, page_size)
    return jsonify(dtasks_page.to_dict())


@app.route('/tasks', methods=['POST'])
def post_task():
    inputs = PostDownloadTaskRequest(request)
    if not inputs.validate():
        raise DTaskValidationError(inputs.errors[0])

    dtask = dtask_service.create_and_queue(
        url=request.json.get('url'),
        relative_target_path=request
            .json
            .get('relative_target_path'),
        file_hash=request.json.get('file_hash', None)
    )
    
    return jsonify(dtask.to_dict())

from flask import request
from flask.json import jsonify
from ddownloader import downloader
from ddownloader.downloader import DownloadStatus

from ddownloader.errors import (
    InvalidStatusTransitionError,
    MetadataReqError
)
from ddownloader.web import dtask_service
from ddownloader.web.app import app
from ddownloader.web.errors import (
    DDownloaderApiError,
    DTaskValidationError,
    UrlMetadataRequestValidationError
)
from ddownloader.web.models import (
    PostDownloadTaskRequest,
    PutDownloadTaskRequest,
    UrlMetadataRequest
)


@app.errorhandler(DDownloaderApiError)
def on_dtask_validation_error(err: DDownloaderApiError):
    res = jsonify(err.to_dict())
    res.status_code = err.status_code
    return res

@app.errorhandler(MetadataReqError)
def on_metadata_req_error(err: MetadataReqError):
    res = jsonify({ 'message': err.message })
    res.status_code = 500
    return res

@app.errorhandler(InvalidStatusTransitionError)
def on_invalid_status_transition_error(err: InvalidStatusTransitionError):
    res = jsonify({
        'status_code': 409,
        'message': err.message
    })
    res.status_code = 409
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


@app.route('/tasks/<int:dtask_id>', methods=['PUT'])
def put_task(dtask_id):
    inputs = PutDownloadTaskRequest(request)
    if not inputs.validate():
        raise DTaskValidationError(inputs.errors[0])

    new_status_raw = request.json.get('status')
    new_status = DownloadStatus(new_status_raw)
    dtask = dtask_service.update_status(dtask_id, new_status)

    return jsonify(dtask.to_dict())


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    dtask_service.remove(id)
    return '', 204

@app.route('/url/metadata', methods=['GET'])
def fetch_metadata():
    inputs = UrlMetadataRequest(request)
    if not inputs.validate():
        raise UrlMetadataRequestValidationError(inputs.errors[0])

    url_meta = downloader.metadata(request.args.get('url'))
    return jsonify(url_meta.to_dict())

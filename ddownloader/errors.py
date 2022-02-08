
class InvalidStatusTransitionError(Exception):

    def __init__(
        self,
        source_status: "DownloadStatus",
        target_status: "DownloadStatus"
    ) -> None:
        Exception.__init__(self)
        self.message = (
            f'Download task can not change its status from'
            f'{source_status.value} to {target_status.value}'
        )

class MetadataReqError(Exception):
    def __init__(self, message) -> None:
        Exception.__init__(self)
        self.message = f'Metadata request failed: {message}'

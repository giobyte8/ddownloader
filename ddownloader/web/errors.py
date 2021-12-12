
class DTaskValidationError(Exception):
    status_code = 400;

    def __init__(self, message, status_code=400) -> None:
        Exception.__init__(self)
        self.status_code = status_code
        self.message = message
    
    def to_dict(self):
        return { 'message': self.message }

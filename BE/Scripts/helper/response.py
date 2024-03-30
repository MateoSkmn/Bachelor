class Response:
    def __init__(self, success, error_code=None, message=None):
        self.success = success
        self.error_code = error_code
        self.message = message
class JelasticClientException(Exception):
    def __init__(self, message: str, response=None):
        super().__init__(message)
        if response is None:
            response = {}
        self.response = response

class ExceptionHandler(Exception):
    def __init__(self, message):
        self._message = f"Request failed: {message}"
        super().__init__(message)

    def __str__(self):
        return self._message

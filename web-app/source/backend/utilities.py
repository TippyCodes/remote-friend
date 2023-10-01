class APIResponse:
    success = True
    message = "success"

    def __init__(self, success, message):
        self.success = success
        self.message = message
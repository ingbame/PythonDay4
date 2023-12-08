class ResultModel:
    def __init__(self, model = {}, message = "", success = True):
        self.model = model
        self.message = message
        self.success = success

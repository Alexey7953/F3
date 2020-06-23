class OperationError(Exception):
    service = 'operation'

    def __init__(self, *args):
        super().__init__(self.service, *args)


class OperationNotFound(OperationError):
    pass
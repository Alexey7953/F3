class UsersError(Exception):
    service = 'users'

    def __init__(self, *args):
        super().__init__(self.service, *args)


class UserNotFound(UsersError):
    pass

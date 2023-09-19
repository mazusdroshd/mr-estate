class TooEarly(Exception):
    def __init__(self, msg: str, remaining_seconds: int):
        self.msg = msg
        self.remaining_seconds = remaining_seconds


class UserExists(Exception):
    pass

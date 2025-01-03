class ReplyButtonException(BaseException):
    def __init__(
        self, salary: str, message="REPLY Exception: No create btn"
    ) -> None:  # noqa
        self.salary = salary
        self.message = message
        super().__init__(self.message)

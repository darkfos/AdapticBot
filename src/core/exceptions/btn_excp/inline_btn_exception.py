class InlineButtonException(BaseException):
    def __init__(
        self, salary: str, message: str = "INLINE Exception: No create btn"
    ) -> None:  # noqa
        self.salary = salary
        self.message = "INLINE Exception: No create btn"
        super().__init__(self.message)

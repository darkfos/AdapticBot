class InlineButtonException(BaseException):
    def __init__(
            self,
            salary,
            message = "INLINE Exception: No create btn"
    ) -> None:
        self.salary = salary
        self.message = "INLINE Exception: No create btn"
        super().__init__(self.message)
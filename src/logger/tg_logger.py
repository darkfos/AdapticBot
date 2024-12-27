import logging
from logging import Logger


class TGLogger:
    __logger: Logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="logs.log",
        level=logging.INFO,
    )

    @classmethod
    def get_logger(cls) -> Logger:
        return cls.__logger
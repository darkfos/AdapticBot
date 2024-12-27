import logging
from logging import Logger
from typing import Dict


class TGLogger:
    __logger: Logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="logs.log",
        level=logging.INFO,
    )

    @classmethod
    def get_logger(cls) -> Logger:
        return cls.__logger

    @classmethod
    def get_config(cls) -> Dict[str, str]:
        return {"tg_id": "<TG-ID>"}

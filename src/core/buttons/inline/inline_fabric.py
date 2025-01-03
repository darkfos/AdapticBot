from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Literal

from src.core.buttons.inline import GeneralInlineButton
from src.core.exceptions.btn_excp.inline_btn_exception import (
    InlineButtonException,
)  # noqa


class InlineButtonFabric:

    @staticmethod
    async def build_buttons(
        btn_arg: Literal["general", "back"]
    ) -> InlineKeyboardBuilder:
        match btn_arg:
            case "general":
                return await GeneralInlineButton.start_btn_command()
            case "back":
                return await GeneralInlineButton.back_btn_command()
            case _:
                raise InlineButtonException(
                    "not found arg for create inline btn"
                )  # noqa

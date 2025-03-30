from aiogram.utils.keyboard import ReplyKeyboardBuilder


from src.core.exceptions.btn_excp.reply_btn_exception import (
    ReplyButtonException,
)  # noqa
from src.core.buttons.reply import ReplyGeneralButton


class ReplyButtonFabric:
    @staticmethod
    async def build_buttons(btn_name: str) -> ReplyKeyboardBuilder:
        match btn_name:
            case "general_tests":
                return await ReplyGeneralButton.general_buttons()
            case "contact":
                return await ReplyGeneralButton.get_contacts()
            case _:
                raise ReplyButtonException("No create reply btn")

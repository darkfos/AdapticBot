from aiogram.utils.keyboard import ReplyKeyboardBuilder


from src.core.exceptions.btn_excp.reply_btn_exceotion import ReplyButtonException # noqa
from src.core.buttons.reply import ReplyGeneralButton

class ReplyButtonFabric:
    @staticmethod
    async def build_buttons(btn_name: str) -> ReplyKeyboardBuilder:
        match btn_name:
            case "general":
                return await ReplyGeneralButton.general_buttons()
            case _:
                raise ReplyButtonException("No create reply btn")

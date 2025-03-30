from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


class ReplyGeneralButton:

    @classmethod
    async def general_buttons(cls) -> ReplyKeyboardMarkup:
        rk_builder: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
            keyboard=[
                [KeyboardButton(text="🆘 Помощь")],
                [KeyboardButton(text="ℹ️ Краткая информация")],
                [KeyboardButton(text="📙 Памятка")],
            ],
        )

        return rk_builder

    @classmethod
    async def get_contacts(cls) -> ReplyKeyboardMarkup:
        rk_builder: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
            keyboard=[
                [KeyboardButton(text="Отправить контакт", request_contact=True)],
            ],
        )

        return rk_builder
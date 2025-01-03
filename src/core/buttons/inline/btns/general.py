from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


class GeneralInlineButton:

    @classmethod
    async def start_btn_command(cls) -> InlineKeyboardBuilder:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="🆘 Помощь", callback_data="/help"),
        )
        builder.row(
            InlineKeyboardButton(
                text="ℹ️ Краткая информация", callback_data="/info"
            ),  # noqa
        )
        builder.row(
            InlineKeyboardButton(text="📙 Памятка", callback_data="/memo"),
        )
        return builder.as_markup()

    @classmethod
    async def back_btn_command(cls) -> InlineKeyboardBuilder:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text="🔙 Обратно", callback_data="/back")
        )  # noqa
        return builder.as_markup()

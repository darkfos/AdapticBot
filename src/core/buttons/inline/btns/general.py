import emoji
from aiogram.types import InlineKeyboardMarkup
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

    @classmethod
    async def admin_panel_command(cls) -> InlineKeyboardBuilder:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text=emoji.emojize(":calendar: Запланированные встречи"), callback_data="admin_panel_meets"),
            InlineKeyboardButton(text=emoji.emojize("➕:calendar: Назначить встречу"), callback_data="admin_panel_create_meets"),
        )
        builder.row(
            InlineKeyboardButton(text=emoji.emojize(":cross_mark::calendar: Удалить встречу"), callback_data="admin_panel_delete_meets"),
            InlineKeyboardButton(text=emoji.emojize(":pencil::calendar: Изменить данные о встрече"), callback_data="admin_panel_change_meets"),
        )
        builder.row(
            InlineKeyboardButton(text=emoji.emojize("👤 Добавить сотрудника"), callback_data="admin_panel_add_persona")
        )
        builder.row(
            InlineKeyboardButton(text=emoji.emojize("👤 Сотрудники"), callback_data="admin_panel_all_personal")
        )

        return builder.as_markup()

    @classmethod
    async def skip_button(cls) -> InlineKeyboardBuilder:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="Пропустить", callback_data="skip"
            )
        )

        return builder.as_markup()

    @classmethod
    async def profile_button(cls) -> InlineKeyboardBuilder:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="Обновить номер телефона", callback_data="profile_update_phone",
            )
        )
        builder.row(
            InlineKeyboardButton(
                text="Запланированные встречи", callback_data="profile_meets"
            )
        )

        return builder.as_markup()
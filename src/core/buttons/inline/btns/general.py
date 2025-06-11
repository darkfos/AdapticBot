import emoji
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


class GeneralInlineButton:

    @classmethod
    async def start_btn_command(cls) -> InlineKeyboardBuilder:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
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
            InlineKeyboardButton(
                text=emoji.emojize(":calendar: Запланированные встречи"),
                callback_data="admin_panel_meets",
            ),
            InlineKeyboardButton(
                text=emoji.emojize("➕:calendar: Назначить встречу"),
                callback_data="admin_panel_create_meets",
            ),
        )
        builder.row(
            InlineKeyboardButton(
                text=emoji.emojize(":cross_mark::calendar: Удалить встречу"),
                callback_data="admin_panel_delete_meets",
            ),
            InlineKeyboardButton(
                text=emoji.emojize(":pencil::calendar: Изменить данные о встрече"),
                callback_data="admin_panel_change_meets",
            ),
        )
        builder.row(
            InlineKeyboardButton(
                text=emoji.emojize("👤 Добавить сотрудника"),
                callback_data="admin_panel_add_persona",
            )
        )
        builder.row(
            InlineKeyboardButton(
                text=emoji.emojize("👤 Добавить администратора"),
                callback_data="admin_panel_add_admin_persona",
            )
        )
        builder.row(
            InlineKeyboardButton(
                text="👤 Удалить сотрудника", callback_data="admin_panel_delete_persona"
            )
        )
        builder.row(
            InlineKeyboardButton(
                text=emoji.emojize("👤 Сотрудники"),
                callback_data="admin_panel_all_personal",
            )
        )
        builder.row(
            InlineKeyboardButton(
                text="💌 Отослать уведомления", callback_data="send_notifications"
            )
        )

        return builder.as_markup()

    @classmethod
    async def skip_button(cls) -> InlineKeyboardBuilder:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="Пропустить", callback_data="skip"))

        return builder.as_markup()

    @classmethod
    async def profile_button(cls) -> InlineKeyboardBuilder:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="📞 Обновить номер телефона",
                callback_data="profile_update_phone",
            )
        )
        builder.row(
            InlineKeyboardButton(
                text="📝 Запланированные встречи", callback_data="profile_meets"
            )
        )

        return builder.as_markup()

    @classmethod
    async def notification_button(cls) -> InlineKeyboardBuilder:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="Каждый день в 9-00",
                callback_data="notification_btn_every_1",
            )
        )

        builder.row(
            InlineKeyboardButton(
                text="Каждые 3 дня в 9-00", callback_data="notification_btn_every_3"
            )
        )

        builder.row(
            InlineKeyboardButton(
                text="Каждую неделю в 9-00", callback_data="notification_btn_every_7"
            )
        )

        builder.row(
            InlineKeyboardButton(
                text="Каждый месяц в 9-00", callback_data="notification_btn_every_30"
            )
        )

        return builder.as_markup()

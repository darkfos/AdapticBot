from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


from src.database.sqlite.repository.meet_repository import MeetModelRepository


class Pagination:
    def __init__(self, tg_id: int = None) -> None:
        self.tg_id = tg_id
        self.page: int = 0
        self.meets = None

    async def get_meets(self):
        all_meets = await MeetModelRepository.get_all_by_user(self.tg_id) if self.tg_id else await MeetModelRepository.get_all()
        self.meets = all_meets

        inline_builder = InlineKeyboardBuilder()

        if (self.page < len(self.meets)):
            inline_builder.add(
                InlineKeyboardButton(
                    text="Дальше ->",
                    callback_data="profile_page_next_" + str(self.page+1)
                )
            )

        inline_builder.row(
            InlineKeyboardButton(
                text="Подробнее",
                callback_data="profile_page_description_" + str(self.meets[self.page].id)
            )
        )

        return (all_meets[self.page], inline_builder.as_markup(), self.page+1)

    async def get_next(self, page):
        all_meets = await MeetModelRepository.get_all_by_user(self.tg_id) if self.tg_id else await MeetModelRepository.get_all()
        self.meets = all_meets
        inline_builder = InlineKeyboardBuilder()

        if (page < len(self.meets)-1):
            inline_builder.add(
                InlineKeyboardButton(
                    text="Дальше ->",
                    callback_data="profile_page_next_" + str(page+1)
                )
            )

        if (page > 0):
            inline_builder.add(
                InlineKeyboardButton(
                    text="<- Обратно",
                    callback_data="profile_page_back_" + str(page-1)
                )
            )

        inline_builder.row(
            InlineKeyboardButton(
                text="Подробнее",
                callback_data="profile_page_description_" + str(self.meets[page].id)
            )
        )

        return (self.meets[page], inline_builder.as_markup(), page+1)

    async def get_previously(self, page):
        all_meets = await MeetModelRepository.get_all_by_user(self.tg_id) if self.tg_id else await MeetModelRepository.get_all()
        self.meets = all_meets
        inline_builder = InlineKeyboardBuilder()

        if (page < len(self.meets)-1):
            inline_builder.add(
                InlineKeyboardButton(
                    text="Дальше ->",
                    callback_data="profile_page_next_" + str(page+1)
                )
            )

        if (page > 0):
            inline_builder.add(
                InlineKeyboardButton(
                    text="<- Обратно",
                    callback_data="profile_page_back_" + str(page-1)
                )
            )

        inline_builder.row(
            InlineKeyboardButton(
                text="Подробнее",
                callback_data="profile_page_description_" + str(self.meets[page].id)
            )
        )

        return (self.meets[page], inline_builder.as_markup(), page+1)
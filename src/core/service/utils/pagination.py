from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


from src.database.sqlite.repository.meet_repository import MeetModelRepository


class Pagination:
    def __init__(self, tg_id: int = None) -> None:
        self.tg_id = tg_id
        self.page: int = 0
        self.page_end: int = self.page + 1
        self.meets = None

    async def get_meets(self):
        all_meets = await MeetModelRepository.get_all_by_user(self.tg_id) if self.tg_id else await MeetModelRepository.get_all()
        self.meets = all_meets

        for meet in self.meets[self.page:self.page_end]:
            inline_builder = InlineKeyboardBuilder()

            if (self.page_end == len(all_meets) or self.page == len(all_meets)):
                inline_builder.row(
                    InlineKeyboardButton(
                        text="<- Обратно",
                        callback_data=str(self.page-1)
                    )
                )

            else:
                inline_builder.add(
                    InlineKeyboardButton(
                        text="Дальше ->",
                        callback_data=str(self.page+1)
                    )
                )

            return (meet, inline_builder, self.page)
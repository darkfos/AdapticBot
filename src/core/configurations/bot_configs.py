from aiogram.methods import SetMyDescription, SetMyShortDescription
from aiogram import Bot


from src.enums import ConfigurationTextEnum


async def set_description_on_bot(bot: Bot) -> None:
    """
    Set description
    :return:
    """

    await bot(
        SetMyDescription(description=ConfigurationTextEnum.BOT_DESC.value)
    )  # noqa


async def set_my_short_description_on_bot(bot: Bot) -> None:
    """
    Set shor description
    :param bot:
    :return:
    """

    await bot(
        SetMyShortDescription(
            short_description=ConfigurationTextEnum.BOT_SHORT_DESC.value
        )
    )

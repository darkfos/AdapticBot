from aiogram.methods import (
    SetMyDescription,
    SetMyShortDescription,
    SetMyCommands,
    SetChatMenuButton,
    SetMyName,
)
from aiogram.types import MenuButtonCommands
from aiogram.types.bot_command import BotCommand
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
    Set short description
    :param bot:
    :return:
    """

    await bot(
        SetMyShortDescription(
            short_description=ConfigurationTextEnum.BOT_SHORT_DESC.value
        )
    )


async def set_my_commands(bot: Bot) -> None:
    """
    Set commands
    :param bot:
    :return:
    """

    await bot(
        SetMyCommands(
            commands=[
                BotCommand(
                    command=command_desc.split(" - ")[0],
                    description=command_desc.split(" - ")[1],
                )
                for command_desc in ConfigurationTextEnum.COMMANDS_LIST.value
            ]
        )
    )


async def set_chat_menu_buttons(bot: Bot) -> None:
    """
    Set chat menu btn's
    :param bot:
    :return:
    """

    await bot(
        SetChatMenuButton(
            chat_id=None, menu_button=MenuButtonCommands(text="Начать")
        )  # noqa
    )


async def set_bot_name(bot: Bot) -> None:
    """
    Set bot name
    :param bot:
    :return:
    """

    await bot(SetMyName(name=ConfigurationTextEnum.BOT_NAME.value))

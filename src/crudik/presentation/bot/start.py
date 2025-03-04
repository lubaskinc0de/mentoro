from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Back, Select
from aiogram_dialog.widgets.text import Const, Format

from crudik.presentation.bot.states import (
    MentorSignInStates,
    MentorSignUpStates,
    StartStates,
    StudentSignInStates,
    StudentSignUpStates,
)

router = Router(name=__name__)


@router.message(CommandStart())
async def start_handler(
    event: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=StartStates.select_entity,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def select_entity(event: CallbackQuery, widget: Select[str], dialog_manager: DialogManager, value: str) -> None:
    dialog_manager.dialog_data["entity_type"] = value
    await dialog_manager.switch_to(
        show_mode=ShowMode.EDIT,
        state=StartStates.select_auth,
    )


_state_map = {
    ("sign_up", "student"): StudentSignUpStates.main,
    ("sign_up", "mentor"): MentorSignUpStates.enter_full_name,
    ("sign_in", "student"): StudentSignInStates.main,
    ("sign_in", "mentor"): MentorSignInStates.main,
}


async def select_way_auth(event: CallbackQuery, widget: Select[str], dialog_manager: DialogManager, value: str) -> None:
    dialog_data = dialog_manager.dialog_data
    await dialog_manager.start(
        state=_state_map[(value, dialog_data["entity_type"])],
    )


dialog = Dialog(
    Window(
        Const("Привет! Кто ты?"),
        Select(
            Format("{item[0]}"),
            id="select_auth",
            item_id_getter=lambda item: item[1],
            items=[
                ("Я студент", "student"),
                ("Я ментор", "mentor"),
            ],
            on_click=select_entity,
        ),
        state=StartStates.select_entity,
    ),
    Window(
        Const("Выбери способ авторизации"),
        Select(
            Format("{item[0]}"),
            id="select_auth",
            item_id_getter=lambda item: item[1],
            items=[
                ("Регистрация", "sign_up"),
                ("Авторизация", "sign in"),
            ],
            on_click=select_way_auth,
        ),
        Back(Const("Назад")),
        state=StartStates.select_auth,
    ),
)

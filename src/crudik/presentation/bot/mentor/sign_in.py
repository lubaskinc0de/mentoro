from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.mentor.sign_in import SignInMentorRequest
from crudik.presentation.bot.states import MentorProfileStates, MentorSignInStates


@inject
async def input_message(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    api_gateway: FromDishka[TestApiGateway],
) -> None:
    if event.text:
        token = await api_gateway.sign_in_mentor(SignInMentorRequest(full_name=event.text))
        if token.status_code == 401 or token.model is None:
            await event.reply("Такого ментора нет в системе. Попробуйте еще раз")
            return

        await dialog_manager.start(
            state=MentorProfileStates.profile,
            show_mode=ShowMode.EDIT,
            data={"token": token.model.access_token},
        )
    await event.delete()


dialog = Dialog(
    Window(
        Const("Для авторизации как ментор нужно ввести полное имя"),
        MessageInput(input_message),
        state=MentorSignInStates.enter_name,
    ),
)

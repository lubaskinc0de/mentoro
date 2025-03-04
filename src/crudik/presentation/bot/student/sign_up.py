from collections.abc import Callable, Coroutine
from typing import Any

from aiogram import Bot, F
from aiogram.enums import ContentType, ParseMode
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.common.scroll import ManagedScroll
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Group, Next, NumberedPager, Row, StubScroll
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Case, Const, Format, List, Multi
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.student.sign_up import SignUpStudentRequest
from crudik.presentation.bot.states import StudentProfileStates, StudentSignUpStates


def input_message(
    key: str,
    next_state: State,
) -> Callable[[Message, MessageInput, DialogManager], Coroutine[Any, Any, None]]:
    async def wrappper(
        event: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
    ) -> None:
        if event.text:
            dialog_manager.dialog_data[key] = event.text
            await dialog_manager.switch_to(
                state=next_state,
                show_mode=ShowMode.EDIT,
            )
        await event.delete()

    return wrappper


async def enter_profile_media(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    if event.photo:
        dialog_manager.dialog_data["file_id"] = event.photo[-1].file_id
        await dialog_manager.switch_to(
            show_mode=ShowMode.EDIT,
            state=StudentSignUpStates.sign_in,
        )
    await event.delete()


async def sign_in_getter(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    dialog_data = dialog_manager.dialog_data
    if dialog_data.get("file_id"):
        media = MediaAttachment(
            file_id=MediaId(dialog_data["file_id"]),
            type=ContentType.PHOTO,
        )
    else:
        media = None

    return {
        "interests": dialog_data["interests"],
        "media": media,
        "full_name": dialog_data["full_name"],
        "about_us": dialog_data.get("about_us") or "отсутствует",
    }


async def input_interest(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    if event.text:
        dialog_manager.dialog_data.setdefault("interests", []).append(event.text)


async def interests_getter(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    scroll: ManagedScroll | None = dialog_manager.find("stub_scroll")
    if scroll is None:
        raise ValueError("stub_scroll not found")

    interests = dialog_manager.dialog_data.get("interests", [])
    current_page = (await scroll.get_page()) + 1
    return {
        "pages": len(interests),
        "ready_for_next": bool(interests),
        "selected_skill_pos": current_page,
        "skills": interests,
    }


async def delete_interest(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    scroll: ManagedScroll | None = dialog_manager.find("stub_scroll")
    if scroll is None:
        raise ValueError("stub_scroll not found")

    current_page = await scroll.get_page()
    if dialog_manager.dialog_data.get("interests"):
        dialog_manager.dialog_data["interests"].pop(current_page)


@inject
async def sign_in_handler(
    event: CallbackQuery, widget: Button, dialog_manager: DialogManager, api_gateway: FromDishka[TestApiGateway]
) -> None:
    middleware_data = dialog_manager.middleware_data
    dialog_data = dialog_manager.dialog_data
    token = await api_gateway.sign_up_student(
        SignUpStudentRequest(
            full_name=dialog_data["full_name"],
            interests=dialog_data["interests"],
            age=dialog_data.get("age"),
            description=dialog_data.get("about_us"),
        ),
    )

    if token.model is None:
        raise ValueError(token)

    if dialog_data.get("file_id"):
        bot: Bot = middleware_data["bot"]
        file = await bot.download(dialog_data["file_id"])
        if file:
            await api_gateway.mentor_update_avatar(token=token.model.access_token, file=file)
    await dialog_manager.start(
        state=StudentProfileStates.profile,
        show_mode=ShowMode.DELETE_AND_SEND,
        data={
            "token": token.model.access_token,
        },
    )


dialog = Dialog(
    Window(
        Const("Введи полное имя"),
        MessageInput(
            input_message(
                key="full_name",
                next_state=StudentSignUpStates.enter_about_us,
            ),
            content_types=ContentType.TEXT,
        ),
        Cancel(Const("Назад"), show_mode=ShowMode.EDIT),
        state=StudentSignUpStates.enter_full_name,
    ),
    Window(
        Const("Введи текст о себе"),
        MessageInput(
            input_message(
                key="about_us",
                next_state=StudentSignUpStates.enter_interests,
            ),
            content_types=ContentType.TEXT,
        ),
        Row(
            Next(Const("Далее"), show_mode=ShowMode.EDIT),
            Back(Const("Назад"), show_mode=ShowMode.EDIT),
        ),
        state=StudentSignUpStates.enter_about_us,
    ),
    Window(
        Multi(
            Const("Поделись чем увлекаешься:\n"),
            List(
                Case(
                    {True: Format("[{pos}]. {item}"), ...: Format("{pos}. {item}")},
                    selector=F["data"]["selected_skill_pos"] == F["pos"],
                ),
                items="skills",
            ),
        ),
        StubScroll(id="stub_scroll", pages="pages"),
        Group(
            NumberedPager(scroll="stub_scroll", id="numbered_pager"),
            width=8,
        ),
        MessageInput(
            input_interest,
            content_types=ContentType.TEXT,
        ),
        Button(
            Const("Удалить увлечение"),
            id="delete_interest",
            on_click=delete_interest,
            when=F["pages"],
        ),
        Row(
            Next(Const("Далее"), show_mode=ShowMode.EDIT, when="ready_for_next"),
            Back(Const("Назад"), show_mode=ShowMode.EDIT),
        ),
        getter=interests_getter,
        state=StudentSignUpStates.enter_interests,
    ),
    Window(
        Const("Отправь фотографию для профиля"),
        MessageInput(
            enter_profile_media,
            content_types=ContentType.PHOTO,
        ),
        Row(
            Next(Const("Далее"), show_mode=ShowMode.EDIT),
            Back(Const("Назад"), show_mode=ShowMode.EDIT),
        ),
        state=StudentSignUpStates.enter_photo,
    ),
    Window(
        DynamicMedia("media", when=F["media"]),
        Multi(
            Format("Введенные данные\n\n<b>Полное имя:</b> {full_name}\n<b>О себе:</b> {about_us}\n<b>Навыки:</b>"),
            List(
                Format("{pos}. {item}"),
                items="skills",
            ),
        ),
        Button(
            Const("Завершить регистрацию"),
            id="sign_in",
            on_click=sign_in_handler,
        ),
        Back(Const("Назад"), show_mode=ShowMode.EDIT),
        getter=sign_in_getter,
        parse_mode=ParseMode.HTML,
        state=StudentSignUpStates.sign_in,
    ),
)

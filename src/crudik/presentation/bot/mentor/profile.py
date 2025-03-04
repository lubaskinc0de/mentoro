from typing import Any

from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import Back, Next, NextPage, PrevPage, Row, StubScroll
from aiogram_dialog.widgets.media.static import StaticMedia
from aiogram_dialog.widgets.text import Const, Format, List, Multi
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.models.mentoring_request import MentoringRequestType
from crudik.presentation.bot.common import set_on_start_data
from crudik.presentation.bot.states import MentorProfileStates


@inject
async def profile_getter(
    dialog_manager: DialogManager,
    api_gateway: FromDishka[TestApiGateway],
    **kwargs: Any,
) -> dict[str, Any]:
    me = await api_gateway.read_mentor(
        dialog_manager.dialog_data["token"],
    )

    assert me.model is not None

    return {
        "photo_url": me.model.photo_url,
        "full_name": me.model.full_name,
        "description": me.model.description,
        "skills": me.model.skills,
        "contacts": me.model.contacts,
    }


@inject
async def requests_getter(
    dialog_manager: DialogManager,
    api_gateway: FromDishka[TestApiGateway],
    **kwargs: Any,
) -> dict[str, Any]:
    data = await api_gateway.read_mentors_requests(
        dialog_manager.dialog_data["token"],
    )

    assert data.model is not None

    if not data.model:
        return {
            "pages": 0,
            "exists_data": False,
        }

    scroll: ManagedScroll | None = dialog_manager.find("stub_scroll")
    assert scroll is not None

    page = await scroll.get_page()
    res = data.model[page]

    if res.type == MentoringRequestType.ACCEPTED:
        type_present = "Принят"
    elif res.type == MentoringRequestType.REVIEW:
        type_present = "На рассмотрении"
    else:
        type_present = "Отклонено"

    return {
        "exists_data": True,
        "pages": len(data.model),
        "type": type_present,
        "created_at": res.created_at.strftime("%d.%m.%Y %H:%M"),
        "full_name": res.student.full_name,
        "description": res.student.description or "отсутствует",
        "photo_url": res.student.avatar_url,
        "interests": res.student.interests,
        "age": res.student.age or "отсутствует",
    }


dialog = Dialog(
    Window(
        StaticMedia(url=Format("{photo_url}"), when=F["photo_url"]),
        Multi(
            Format(
                "<b>Данные об аккаунте:</b>\n"
                "<b>Полное имя: </b>{full_name}\n"
                "<b>О себе: </b>{description}\n"
                "<b>Скиллы: </b>"
            ),
            List(
                Format(" {pos}. {item}"),
                items="skills",
            ),
            Const("\n<b>Контакты:</b>"),
            List(
                Format(" {pos}. {item.social_network}: {item.url}"),
                items="contacts",
            ),
        ),
        Next(
            Const("Заявки на ментерство"),
            show_mode=ShowMode.EDIT,
        ),
        getter=profile_getter,
        parse_mode=ParseMode.HTML,
        state=MentorProfileStates.profile,
    ),
    Window(
        StaticMedia(url=Format("{photo_url}"), when=F["photo_url"] & F["exists_data"]),
        Multi(
            Format(
                "<b>Данные об заявке:</b>\n"
                " <b>Тип заявки: </b>{type}\n"
                " <b>Дата создания: </b>{created_at}\n\n"
                "<b>Данные об аккаунте студента:</b>\n"
                " <b>Полное имя: </b>{full_name}\n"
                " <b>Возраст: </b>{age}\n"
                " <b>Интересы: </b>"
            ),
            List(
                Format(" {pos}. {item}"),
                items="interests",
            ),
            Format(" <b>О себе: </b>{description}"),
            when=F["exists_data"],
        )
        | Const("Заявок на ментерство нет"),
        StubScroll("stub_scroll", "pages"),
        Row(
            PrevPage("stub_scroll", "prev_page", when=F["exists_data"]),
            Back(
                Const("В профиль"),
                show_mode=ShowMode.EDIT,
            ),
            NextPage("stub_scroll", "next_page", when=F["exists_data"]),
        ),
        getter=requests_getter,
        state=MentorProfileStates.requests,
        parse_mode=ParseMode.HTML,
    ),
    on_start=set_on_start_data,
)

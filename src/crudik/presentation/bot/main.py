from aiogram import Dispatcher

from .mentor.profile import dialog as dialog_mentor_profile
from .mentor.sign_up import dialog as mentor_sign_up_dialog
from .start import dialog as start_dialog
from .start import router as start_router


def include_handlers(dp: Dispatcher) -> None:
    dp.include_router(start_router)

    dp.include_router(mentor_sign_up_dialog)
    dp.include_router(start_dialog)
    dp.include_router(dialog_mentor_profile)

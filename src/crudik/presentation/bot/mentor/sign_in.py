# from aiogram import Router
# from aiogram.filters import Command
# from aiogram.types import Message
# from aiogram_dialog import Dialog, DialogManager, Window
#
# from crudik.presentation.bot.states import MentorSignInStates
#
# router = Router(name=__name__)
#
# @router.message(Command("sign_in"))
# async def sign_in_handler(
#     event: Message,
#     dialog_manager: DialogManager,
# ) -> None:
#     await dialog_manager.start(state=MentorSignInStates)
#
#
# dialog = Dialog(
#     Window(
#         state=MentorSignInStates,
#     ),
# )

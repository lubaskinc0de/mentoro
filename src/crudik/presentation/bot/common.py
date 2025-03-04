from typing import Any

from aiogram_dialog import DialogManager


async def set_on_start_data(
    start_data: dict[str, Any],
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data.update(start_data)

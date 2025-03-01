import asyncio
import sys

from filler.fill_data import fill_data


async def main() -> None:
    argv = sys.argv[1:]

    if not argv:
        return

    try:
        module = argv[0]
        option = argv[1]
    except IndexError:
        return

    modules = {
        "run": {
            "fill": fill_data,
        },
    }

    if module not in modules:
        return

    if option not in modules[module]:
        return

    command = modules[module][option]
    await command()


asyncio.run(main())

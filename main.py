import asyncio
from mailing import mailing
from CardRefresh import start_refresh
from handlers.start_handler import start_handler_main
from handlers.other_handlers import handle_all_events


async def main():
    await start_handler_main()
    await mailing()
    await start_refresh()
    await handle_all_events()

if __name__ == '__main__':
    from asyncio import run
    run(main())

import asyncio
from mailing import main as mailing_main
from CardRefresh import card_refresh_main
from handlers.start_handler import start_handler_main
from handlers.other_handlers import handle_all_events


async def main():
    await start_handler_main()
    await mailing_main()
    await card_refresh_main()
    await handle_all_events()

if __name__ == '__main__':
    from asyncio import run
    run(main())

from trello import TrelloClient
from aiogram import Bot, Dispatcher


TOKEN = '6757291411:AAE66i_EJvp0FPFIzMRmvGIIOMRImYFQWCg'
ADMIN = 851766492


FAQ_URL_1 = "facebook.com"
FAQ_URL_2 = "trello.com"
FAQ_URL_3 = "instagram.com"
FAQ_URL_4 = ""
FAQ_URL_5 = ""
FAQ_URL_6 = ""
FAQ_URL_7 = ""
FAQ_URL_8 = ""
FAQ_URL_9 = ""


TRELLO_API_KEY = '7becfc205a732ce29804b66f6c0d0493'
TRELLO_TOKEN = 'ATTA6144f2c536973c50aa8ba2a183c1fdf6180fff0b352866c3d27fdbc6d7b6a2220A3829BF'
TRELLO_BOARD_ID = 'KGj8jeNn'
YOUR_TRELLO_LIST_NAME = "Актуальные Вакансии"


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


trello = TrelloClient(
    api_key=TRELLO_API_KEY,
    api_secret=TRELLO_TOKEN,
)

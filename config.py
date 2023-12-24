from trello import TrelloClient
from aiogram import Bot, Dispatcher


TOKEN = ''
ADMIN =


FAQ_URL_1 = "facebook.com"
FAQ_URL_2 = "trello.com"
FAQ_URL_3 = "instagram.com"
FAQ_URL_4 = ""
FAQ_URL_5 = ""
FAQ_URL_6 = ""
FAQ_URL_7 = ""
FAQ_URL_8 = ""
FAQ_URL_9 = ""


TRELLO_API_KEY = ''
TRELLO_TOKEN = ''
TRELLO_BOARD_ID = ''
YOUR_TRELLO_LIST_NAME = "Актуальные Вакансии"


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


trello = TrelloClient(
    api_key=TRELLO_API_KEY,
    api_secret=TRELLO_TOKEN,
)

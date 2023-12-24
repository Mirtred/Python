from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard(show_respond_button=True, show_unsubscribe_button=True):
    keyboard = InlineKeyboardMarkup()

    if show_respond_button:
        keyboard.add(InlineKeyboardButton(text="Откликнуться на последнюю вакансию", callback_data="respond"))

    keyboard.add(InlineKeyboardButton(text="Показать доступные вакансии", callback_data="vacancies"))

    keyboard.add(InlineKeyboardButton(text="Указать номер телефона", callback_data="phone"))

    keyboard.add(InlineKeyboardButton(text="Полезные ссылки", callback_data="faq"))

    if show_unsubscribe_button:
        keyboard.add(InlineKeyboardButton(text="Отписаться", callback_data="unsubscribe"))

    return keyboard

from aiogram import types

from config import (dp, bot, ADMIN,
                    FAQ_URL_1, FAQ_URL_2, FAQ_URL_3, FAQ_URL_4, FAQ_URL_5, FAQ_URL_6, FAQ_URL_7, FAQ_URL_8, FAQ_URL_9)
from utils.database import cursor, conn
from utils.database import manage_user, get_user_phone
from keyboards.keyboard import create_keyboard
from mailing import send_vacancies_to_users


main_keyboard = create_keyboard(show_respond_button=False)
secondary_keyboard = create_keyboard(show_unsubscribe_button=False)


# Команды админа
@dp.message_handler(commands=["m"])
async def send_message(message: types.Message):
    text_a = message.text.replace("/m ", "")
    user_id = message.from_user.id
    if user_id != ADMIN:
        await message.answer("Ошибка.")
        return

    cursor.execute("SELECT id, name FROM Forms")
    users = cursor

    for user in users:
        await bot.send_message(user[0], text_a)
    await message.answer("Сообщение успешно отправлено всем пользователям.")


# Обрабатываем коллбэк-запросы от кнопок
@dp.callback_query_handler()
async def callback(query: types.CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    user_name = query.from_user.first_name

    if data == "unsubscribe":
        manage_user(user_id, remove=True)
        await query.answer("Вы успешно отписаны от бота.")

    elif data == "vacancies":
        await query.answer()
        await send_vacancies_to_users(user_id, reply_markup=main_keyboard)

    elif data == "phone":
        await query.answer()
        phone = get_user_phone(user_id)
        if phone:
            await query.message.answer(f"Ваш номер телефона: {phone}"
                                       f"\nЕсли вы хотите изменить его, напишите новый номер в сообщении боту в"
                                       f"формате код страны и девяти цифр номера мобильного телефона"
                                       f" без дополнительных символов и пробелов, например 48ХХХХХХХХХ.")
        else:
            await query.message.answer("Пожалуйста, укажите ваш номер телефона в сообщении боту в"
                                       "формате кода страны и девяти цифр номера мобильного телефона"
                                       " без дополнительных символов и пробелов, например 48ХХХХХХХХХ.")

    elif data == "faq":
        await query.answer()

        faq_urls = [
            FAQ_URL_1, FAQ_URL_2, FAQ_URL_3, FAQ_URL_4, FAQ_URL_5, FAQ_URL_6, FAQ_URL_7, FAQ_URL_8, FAQ_URL_9
        ]

        faq_message = "Вот некоторые полезные ссылки:\n"

        for i, url in enumerate(faq_urls, start=1):
            if url:
                faq_message += f"Сылка {i}: {url}\n"

        await query.message.answer(faq_message, reply_markup=main_keyboard)


    elif data == "respond":
        result = cursor.execute("SELECT last_sent_card FROM Forms WHERE id = ?", (user_id,)).fetchone()
        last_sent_card_id = result[0] if result else None

        # Проверяем, чтобы ID карточки не добавлялись повторно

        if last_sent_card_id not in cursor.execute("SELECT card FROM Forms WHERE id = ?", (user_id,)).fetchone()[0]:
            # Если ID карточки еще не добавлен, обновляем колонку "card"

            cursor.execute("UPDATE Forms SET last_sent_card = COALESCE(card || ', ' || ?, ?) WHERE id = ?",

                           (last_sent_card_id, last_sent_card_id, user_id))

            conn.commit()

        count_responded_users = \
            cursor.execute("SELECT COUNT(*) FROM Forms WHERE last_sent_card LIKE ?",
                           ('%' + last_sent_card_id + '%',)).fetchone()[0]

        await query.answer(
            f"Вы успешно откликнулись на последнюю вакансию.\nНа данную вакансию откликнулись: {count_responded_users}")


# Текстовые сообщения
@dp.message_handler(content_types=["text"])
async def text(message: types.Message):
    # Получаем текст сообщения
    text_p = message.text
    # Получаем идентификатор и имя пользователя
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    # Проверяем, является ли текст номером телефона
    if text_p.isdigit():
        # Добавляем или обновляем пользователя в базе данных с номером телефона
        manage_user(user_id, user_name, text_p)
        # Отправляем сообщение с подтверждением и предложением выбрать вариант взаимодействия
        await message.answer(f"Ваш номер телефона {text_p} успешно сохранен в базе данных."
                             f"\nВыберите вариант взаимодействия:", reply_markup=main_keyboard)
    else:
        # Отправляем сообщение с предупреждением и предложением выбрать вариант взаимодействия
        await message.answer("Это не похоже на номер телефона.\nВыберите вариант взаимодействия:",
                             reply_markup=main_keyboard)


async def handle_all_events():
    message = types.Message(chat=types.Chat(id=123, type="private"), message_id=456, text="/start")
    await send_message(message)

    query = types.CallbackQuery.from_user(user_id=123, first_name="John", data="vacancies")
    await callback(query)

    text_message = types.Message(chat=types.Chat(id=123, type="private"), message_id=457, text="Some text")
    await text(text_message)


async def other_handlers_main():
    await handle_all_events()

if __name__ == '__main__':
    from asyncio import run
    run(other_handlers_main())

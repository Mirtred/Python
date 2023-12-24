from config import bot, dp, TRELLO_BOARD_ID, YOUR_TRELLO_LIST_NAME, trello

from utils.database import conn, cursor, get_existing_forms
from keyboards.keyboard import create_keyboard

secondary_keyboard = create_keyboard(show_unsubscribe_button=False)

# Получаем объект доски
board = trello.get_board(TRELLO_BOARD_ID)
last_sent_card_index_dict = {}


# Отправка сообщений при нажатии на кнопку "Показать актуальные вакансии"
async def send_vacancies_to_users(user_id, reply_markup):
    # Получаем объект листа по его имени
    your_trello_list = next((lst for lst in board.list_lists() if lst.name == YOUR_TRELLO_LIST_NAME), None)

    # Проверяем, найден ли лист
    if not your_trello_list:
        print(f"Лист с именем '{YOUR_TRELLO_LIST_NAME}' не найден.")
        return

    # Извлекаем все карточки из листа
    cards = your_trello_list.list_cards()

    # Извлекаем пользователя из базы данных
    user = cursor.execute("SELECT id FROM Forms WHERE id = ?", (user_id,)).fetchone()

    # Извлекаем из словаря последний отправленный индекс карточки для пользователя
    last_sent_card_index = last_sent_card_index_dict.get(user_id, 0)

    # Если индекс больше или равен количеству карточек, отправляем сообщение о завершении
    if last_sent_card_index >= len(cards):
        await bot.send_message(user[0], "Это все актуальные вакансии на данный момент.")

        # Сбрасываем индекс на 0 для повторного цикла
        last_sent_card_index_dict[user_id] = 0
        return

    # Отправляем по одной карточке по запросу пользователя
    card = cards[last_sent_card_index]
    message_text = f"Вакансия: {card.name}\nОписание: {card.description}"
    await bot.send_message(user[0], message_text, reply_markup=secondary_keyboard)

    # Сохраняем ID последней отправленной карточки в базе данных
    last_sent_card_id = card.id  # Получаем ID карточки Trello
    cursor.execute("UPDATE Forms SET last_sent_card = ? WHERE id = ?", (last_sent_card_id, user_id))
    conn.commit()  # Фиксируем изменения в базе данных

    # Обновляем информацию о последнем отправленном индексе карточки в словаре
    last_sent_card_index_dict[user_id] = last_sent_card_index + 1


async def mailing():
    get_existing_forms()
    await dp.start_polling()

if __name__ == '__main__':
    from asyncio import run
    run(mailing())

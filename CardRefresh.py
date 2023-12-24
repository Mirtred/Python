import asyncio
import aiohttp
import time

from utils.database import conn
from config import YOUR_TRELLO_LIST_NAME, TRELLO_BOARD_ID, TRELLO_API_KEY, TRELLO_TOKEN, dp
from keyboards.keyboard import create_keyboard

secondary_keyboard = create_keyboard(show_unsubscribe_button=False)


async def get_existing_trello_cards():
    cursor = conn.cursor()
    cursor.execute('SELECT card_id, card_name, card_desc, user_count FROM TrelloCards')
    rows = cursor.fetchall()
    existing_cards = {row[0]: {'card_name': row[1], 'card_desc': row[2], 'user_count': row[3]} for row in rows}
    return existing_cards


async def update_database(new_cards, existing_cards):
    cursor = conn.cursor()
    changes_occurred = False

    for card in new_cards:
        card_id = card['id']
        card_name = card['name']
        card_desc = card['desc']

        if card_id not in existing_cards:
            cursor.execute('''
                INSERT INTO TrelloCards (card_id, card_name, card_desc, user_count)
                VALUES (?, ?, ?, 0)
            ''', (card_id, card_name, card_desc))
            changes_occurred = True
        else:
            if card_name != existing_cards[card_id]['card_name'] or card_desc != existing_cards[card_id]['card_desc']:
                cursor.execute('''
                    UPDATE TrelloCards
                    SET card_name = ?, card_desc = ?
                    WHERE card_id = ?
                ''', (card_name, card_desc, card_id))
                changes_occurred = True

    deleted_cards = set(existing_cards.keys()) - set(card['id'] for card in new_cards)
    for card_id in deleted_cards:
        cursor.execute('DELETE FROM TrelloCards WHERE card_id = ?', (card_id,))
        changes_occurred = True

    conn.commit()

    return changes_occurred


async def get_trello_cards():
    url = f'https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists'
    params = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            lists = await response.json()

    for trello_list in lists:
        if trello_list['name'] == YOUR_TRELLO_LIST_NAME:
            cards_url = f'https://api.trello.com/1/lists/{trello_list["id"]}/cards'

            async with aiohttp.ClientSession() as session:
                async with session.get(cards_url, params=params) as cards_response:
                    return await cards_response.json()

    return []


async def refresh_trello_cards():
    while not asyncio.get_event_loop().is_closed():
        try:
            existing_cards = await get_existing_trello_cards()
            trello_cards = await get_trello_cards()
            changes_occurred = await update_database(trello_cards, existing_cards)

            if changes_occurred:
                await handle_new_card_addition(None)

            await asyncio.sleep(15)
            await asyncio.sleep(0)

        except Exception as e:
            print(f"An error occurred: {e}")


async def handle_new_card_addition(reply_markup=None):
    existing_forms = await get_forms_data()
    new_card = await get_latest_card()

    if existing_forms and new_card and new_card['card_desc']:
        message_text = f"Новая карточка!\nНазвание: {new_card['card_name']}\nОписание: {new_card['card_desc']}"

        for user_id in existing_forms:
            try:
                print(f'Sending message to user {user_id}')
                await send_message_to_user(user_id, message_text)
                print(f'Message sent to user {user_id}')
            except Exception as e:
                print(f"An error occurred while sending message to user {user_id}: {e}")


async def get_forms_data():
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM Forms')
    existing_forms = [row[0] for row in cursor.fetchall()]
    return existing_forms


async def get_latest_card():
    cursor = conn.cursor()
    cursor.execute('SELECT card_name, card_desc FROM TrelloCards ORDER BY ROWID DESC LIMIT 1')
    latest_card = cursor.fetchone()
    return {'card_name': latest_card[0], 'card_desc': latest_card[1]} if latest_card else None


async def send_message_to_user(user_id, text):
    await dp.bot.send_message(chat_id=user_id, text=text)


async def start_refresh():
    while True:
        try:
            await refresh_trello_cards()
        except Exception as e:
            print(f"An error occurred during Trello card refresh: {e}")

if __name__ == "__main__":
    asyncio.run(start_refresh())

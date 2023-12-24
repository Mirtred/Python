import sqlite3


DB_NAME = 'data.db'
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()


def get_existing_forms():
    cursor.execute('SELECT id, name, phone, last_sent_card FROM Forms')
    rows = cursor.fetchall()

    existing_forms = {}
    for row in rows:
        if len(row) >= 5:
            existing_forms[row[0]] = {'id': row[1], 'name': row[2], 'phone': row[3], 'last_sent_card': row[4]}
        else:
            print(f"Invalid row: {row}")

    return existing_forms


def get_existing_trello_cards():
    cursor.execute('SELECT card_id, card_name, card_desc, user_count FROM TrelloCards')
    existing_cards = {row[0]: {'card_name': row[1], 'card_desc': row[2], 'user_count':
        row[3]} for row in cursor.fetchall()}
    return existing_cards


def get_existing_cards():
    cursor.execute('SELECT id, id_card_1 FROM Cards')
    existing_cards = {row[0]: {'id_card_1': row[1]} for row in cursor.fetchall()}
    return existing_cards


# Функция для добавления, обновления или удаления пользователя в базе данных
def manage_user(user_id, name=None, phone=None, remove=False):
    if remove:
        cursor.execute("DELETE FROM Forms WHERE id=?", (user_id,))
    else:
        cursor.execute("SELECT * FROM Forms WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE Forms SET phone = ? WHERE id = ?", (phone, user_id))
        else:
            cursor.execute("INSERT INTO Forms (id, name, phone) VALUES (?, ?, ?)", (user_id, name, phone))
    conn.commit()


# Создаем функцию для получения номера телефона пользователя из базы данных
def get_user_phone(user_id):
    # Проверяем, есть ли пользователь в базе данных
    cursor.execute("SELECT phone FROM Forms WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


# Создаем функцию для получения номера телефона пользователя из базы данных
def get_user_phone(user_id):
    # Проверяем, есть ли пользователь в базе данных
    cursor.execute("SELECT phone FROM Forms WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

from aiogram import types
from config import dp

from utils.database import manage_user
from keyboards.keyboard import create_keyboard

main_keyboard = create_keyboard(show_respond_button=False)


@dp.message_handler(commands=["start", "unsubscribe"])
async def handle_start_or_unsubscribe(message: types.Message):
    user_id = message.from_user.id

    if message.get_command() == "/start":
        print("Received /start command")
        await message.answer(f"Привет, {message.from_user.first_name}!"
                             f"\nЯ бот, который может помочь вам с вакансиями и другими вопросами."
                             f"\nВыберите вариант взаимодействия:", reply_markup=main_keyboard)
        manage_user(user_id, message.from_user.first_name, None)

    elif message.get_command() == "/unsubscribe":
        print("Received /unsubscribe command")
        manage_user(user_id, remove=True)
        await message.answer("Вы успешно отписаны от бота.")


async def start_handler_main():
    await handle_start_or_unsubscribe()

if __name__ == '__main__':
    from asyncio import run
    run(start_handler_main())

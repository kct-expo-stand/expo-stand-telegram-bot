from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_contact_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить мой номер из Telegram", request_contact=True)],
            [KeyboardButton(text="У меня другой номер")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_skip_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пропустить")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_contact_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить мой номер из Telegram", request_contact=True)],
            [KeyboardButton(text="У меня другой номер")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_program_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="FrontEnd", callback_data="program_frontend")],
            [InlineKeyboardButton(text="BackEnd", callback_data="program_backend")],
            [InlineKeyboardButton(text="Design", callback_data="program_design")],
            [InlineKeyboardButton(text="GameDev", callback_data="program_gamedev")],
            [InlineKeyboardButton(text="Project Manager", callback_data="program_pm")],
            [InlineKeyboardButton(text="Пропустить", callback_data="program_skip")]
        ]
    )

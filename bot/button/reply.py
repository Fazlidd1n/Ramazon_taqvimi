from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def menu_buttons():
    calendar = KeyboardButton(text="Taqvim 💫")
    s = KeyboardButton(text="Iftorlik duosi ✨")
    i = KeyboardButton(text="Saharlik duosi ✨")
    info = KeyboardButton(text="Ma'lumot 📋")
    design = [
        [calendar],
        [s, i],
        [info]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True, one_time_keyboard=True)


def calendar_buttons():
    today = KeyboardButton(text="Bugungi Vaqt ⏰")
    month = KeyboardButton(text="Oylik Vaqtlar 📆")
    back = KeyboardButton(text="🔙 Menu")
    design = [
        [today, month],
        [back]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True, one_time_keyboard=True)

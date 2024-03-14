import datetime

import pytz
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, BotCommand

from bot.button.reply import menu_buttons, calendar_buttons
from bot.state import Menu
from bot.text import start_text, i_duosi, s_duosi, today_time_text, info_creator
from db.config import Base, session
from db.model import BotUser, RamadanCalendar
from dispatcher import dp, bot


@dp.message(Command('start', 'restart'))
async def start_handler(msg: Message, state: FSMContext):
    start = BotCommand(command='start', description='Botga start berish')
    restart = BotCommand(command='restart', description='Botga qayta start berish')
    reklama = BotCommand(command='reklama', description="Foydalanuvchilarga reklama yuborish (Admin uchun ❗️)")
    await msg.bot.set_my_commands(commands=[start, restart, reklama])

    await bot.send_message(2045036931,
                           f"🟢 Yangi foydalanuvchi\n fullname : {msg.from_user.full_name}\n username : {msg.from_user.username}")
    BotUser.insert_user(Base, msg.from_user.id, msg.from_user.full_name, msg.from_user.username)
    await msg.answer(start_text.format(msg.from_user.full_name), reply_markup=menu_buttons())
    print(f"👤 - {msg.from_user.full_name}")
    await state.set_state(Menu.menu)


@dp.message(Command("reklama"))
async def reklama_handler(msg: Message, state: FSMContext):
    if msg.from_user.id == 2045036931:
        await msg.answer("Reklama xabarini yuboring ⤵️")
        await state.set_state(Menu.reklama)
    else:
        await msg.answer("Siz admin emassiz ❗️", reply_markup=menu_buttons())
        await state.set_state(Menu.menu)


@dp.message(Menu.reklama)
async def reklama_handler(msg: Message, state: FSMContext):
    users = session.query(BotUser)
    for user in users:
        if user.user_id == 2045036931:
            continue
        await msg.copy_to(user.user_id)
    await msg.answer("Xabar yuborildi ✅", reply_markup=menu_buttons())
    await state.set_state(Menu.menu)


@dp.message(Menu.menu)
async def menu_handler(msg: Message, state: FSMContext):
    if msg.text == 'Taqvim 💫':
        await msg.answer("Tugmalardan birini tanlang ⤵️", reply_markup=calendar_buttons())
        await state.set_state(Menu.calendar)
    elif msg.text == "Iftorlik duosi ✨":
        photo = FSInputFile('images/ogiz_ochish.jpeg')
        await msg.answer_photo(photo, i_duosi, reply_markup=menu_buttons())
    elif msg.text == "Saharlik duosi ✨":
        photo = FSInputFile('images/ogiz_yopish.jpeg')
        await msg.answer_photo(photo, s_duosi, reply_markup=menu_buttons())
    elif msg.text == "Ma'lumot 📋":
        await msg.answer(info_creator, reply_markup=menu_buttons())
    else:
        await msg.answer("Menudagi tugmalardan birini tanlang ❗", reply_markup=menu_buttons())
        await state.set_state(Menu.menu)


@dp.message(Menu.calendar)
async def calendar_menu(msg: Message, state: FSMContext):
    if msg.text == "Bugungi Vaqt ⏰":
        tz = pytz.timezone('Asia/Tashkent')
        d = datetime.datetime.now(tz=tz).strftime('%d').strip('0')
        m = datetime.datetime.now(tz=tz).strftime('%m').strip('0')
        y = datetime.datetime.now(tz=tz).strftime('%Y')
        if m == '3':
            m = 'Mart'
        elif m == '4':
            m = 'Aprel'
        x = f"{d} {m} {y}"
        if RamadanCalendar.select_data(Base, x):
            data = RamadanCalendar.select_data(Base, x)[0]
            # day_name = ''
            if data.day_name == 'Du':
                day_name = 'Dushanba'
            elif data.day_name == 'Se':
                day_name = 'Seshanba'
            elif data.day_name == 'Cho':
                day_name = 'Chorshanba'
            elif data.day_name == 'Pa':
                day_name = 'Payshanba'
            elif data.day_name == 'Ju':
                day_name = 'Juma'
            elif data.day_name == 'Sha':
                day_name = 'Shanba'
            else:
                day_name = 'Yakshanba'
            photo = FSInputFile('images/tabrik.jpg')
            await msg.answer_photo(photo,
                                   today_time_text.format(data.day, day_name, data.date, data.s_time, data.i_time),
                                   reply_markup=calendar_buttons())
        else:
            await msg.answer("Bugun Ramazon kuni emas ❗", reply_markup=calendar_buttons())

    elif msg.text == "Oylik Vaqtlar 📆":
        photo = FSInputFile('images/oylik_taqvim.jpeg')
        await msg.answer_photo(photo, "Toshkent shahrining\nRamazon oyi taqvimi 🌙", reply_markup=calendar_buttons())

    elif msg.text == "🔙 Menu":
        await msg.answer('Menu 📋\nTugmalardan birini tanlang ⤵️', reply_markup=menu_buttons())
        await state.set_state(Menu.menu)

    else:
        await msg.answer("❌ Tugmalardan birini tanlang ⤵️", reply_markup=calendar_buttons())
        await state.set_state(Menu.calendar)

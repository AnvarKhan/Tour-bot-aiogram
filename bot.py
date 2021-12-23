import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.builtin import CommandStart

import threading
import requests

from mysql import connector
from datetime import date

from buttons.buttons import *
from config.config import *

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

conn = connector.connect(host=host, user=user, password=password, database=db_name)
cursor = conn.cursor(buffered=True)

def sql(chat, id):
    user_id_chat = f"UPDATE users SET chat_id = {str(chat)} WHERE id = {id}" 
    cursor.execute(user_id_chat)
    return conn.commit()

@dp.message_handler(CommandStart())
async def command_start(message: types.Message):
    user_fullname = message.from_user.full_name
    await message.answer(f"""Здравствуйте <b><i>{user_fullname}</i></b>. 
Это официальный бот "Safar.guru"
""", parse_mode='HTML')
    await message.answer(f"""Пришлите свой номер🔽""", reply_markup=kontakt_btn1)


@dp.message_handler(content_types=['contact'])
async def phone(message: types.Message):
    user_id = message.from_user.id
    selectquery = f"SELECT * from users Where number = {message.contact.phone_number}" 
    cursor.execute(selectquery)
    user = cursor.fetchone()
    print(user)
    if user:
        await message.answer("🔽Выберите одну из следующих кнопок:🔽", reply_markup=menu)
        await message.answer(f"""       Safar.guru 
Логин: {user[1]}
Парол: {user[6]}""")

        sql(message.from_user.id, user[0])

    else:
        await message.answer("""Вы не зарегистрированы❗️
Зарегистрируйтесь на нашем сайте Safar.guru!""")


@dp.message_handler(text='📕Бронь Лист Гостиницы')
async def hotel_brons(message: types.Message):
    user_id = message.from_user.id
    selectquery = """
SELECT chat_id,start,end,sum,hotel_brons.hotel_id,room_id,
hotels.id,hotels.name,region_ru,
hotel_rooms.id,hotel_rooms.type 
from hotel_brons,hotels,hotel_rooms"""
    cursor.execute(selectquery)
    hotel_all = cursor.fetchall()
    for mexmon in hotel_all:
        if user_id in mexmon and mexmon[4] == mexmon[6] and mexmon[5] == mexmon[9]:
            await message.answer(f"""Вы в городе "<b><i>{mexmon[8]}</i></b>" 
"<b><i>{mexmon[7]} Hotel</i></b>"забронировали отель!
<b>Номер брона:</b> 1231231 || <i>{mexmon[1]}</i> - <i>{mexmon[2]}</i>
<b>Комната:</b> {mexmon[10]} || <b>Итого:</b> {mexmon[3]}""", parse_mode='HTML')


@dp.message_handler(text='📕Бронь Лист Туров')
async def hotel_brons(message: types.Message):
    user_id = message.from_user.id
    selectquery = """
SELECT chat_id,date,tour_id,tourfirm_id,
tours.id,tours.title_ru,tours.price,tours.region_ru,
tourfirm_infos.id,tourfirm_infos.name,tourfirm_infos.number 
from tour_brons,tours,tourfirm_infos"""
    cursor.execute(selectquery)
    tour_all = cursor.fetchall()
    for tour in tour_all:
        if user_id in tour and tour[2] == tour[4] and tour[3] == tour[8]:
            await message.answer(f"""<b>Город зарегистрированного вида:</b>"<i>{tour[7]}</i>",
<b>Название тура:</b><i>{tour[5]}</i>",
<b>Номер брона:</b> 1231231 || <i>{tour[1]}</i>,
<b>Итого:</b> {tour[6]} so'm,
<b>Тур ферма:</b>{tour[9]}
<b>Номер телефона:</b>{tour[10]}""", parse_mode='HTML')


@dp.message_handler(text='📕Бронь Лист Гидов')
async def hotel_brons(message: types.Message):
    user_id = message.from_user.id
    selectquery = """
SELECT chat_id,guide_id,
guide_infos.id,guide_infos.name,guide_infos.number,guide_infos.region_ru
from guide_brons,guide_infos"""
    cursor.execute(selectquery)
    guide_all = cursor.fetchall()
    for guide in guide_all:
        if user_id in guide and guide[1] == guide[2]:
            await message.answer(f"""Вы в городе <b><i>{guide[5]}</i></b>
Забронировали <b><i>{guide[3]}</i></b>!
<b>Номер брона:</b> 1231231
<b>Номер телефона:</b>{guide[4]}""", parse_mode='HTML')


@dp.message_handler(text='💬Отзывы')
async def Otziv(message: types.Message):
    """here is way to otziv button"""
    await message.answer("Оставить отзыв!", reply_markup=back)

    @dp.message_handler()
    async def comment(message: types.Message):
        """get Comments to safar"""
        user_id = message.from_user.id
        today = str(date.today())
        comments = f"""INSERT INTO comment_user (chat_id,comments,Date_of_comment) VALUES {user_id, message.text, today}"""
        cursor.execute(comments)
        conn.commit()
        await message.answer("Ваш отзыв был принят")


@dp.message_handler(text='⬅️Назад')
async def hotel_brons(message: types.Message):
    """Back button"""
    await message.answer("🔽Выберите одну из следующих кнопок::🔽", reply_markup=menu)


def set_interval(func, sec):
    """Interval of threading"""
    def func_wrapper():
        """get func for thread"""
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def grup():

    """After 3 days it sends msgs"""

    msg = """Здравствуйте
Хорошо отдохнул?
Оставьте комментарий с помощью кнопки 💬отзыва! """
    selectquery = """
    SELECT chat_id,day3_after
    from hotel_brons"""
    cursor.execute(selectquery)
    guide_all = cursor.fetchall()
    today = str(date.today())
    for gruxlar in guide_all:
        if today == gruxlar[1]:
            TO_URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=HTML'.format(TOKEN,
                                                                                                            gruxlar[0],
                                                                                                            msg)
            resp = requests.get(TO_URL)


set_interval(grup, 60*60*24)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

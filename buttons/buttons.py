from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📕Бронь Лист Гостиницы"),
        ],
        [
            KeyboardButton(text="📕Бронь Лист Туров"),
        ],
        [
            KeyboardButton(text="📕Бронь Лист Гидов"),
        ],
        [
            KeyboardButton(text="💬Отзывы"),
        ],
    ],
    resize_keyboard=True
)


back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⬅️Назад')
        ],
    ],
    resize_keyboard=True
)

# KONTAKT Knopkasi
kontakt_btn1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Mening raqamim', request_contact=True)
        ],
    ],
    resize_keyboard=True
)



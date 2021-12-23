from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters.builtin import CommandStart


@dp.message_handler(CommandStart())
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Assalamualaykum')
        await message.delete()
    except:
        await message.reply('Hush kelibsiz')



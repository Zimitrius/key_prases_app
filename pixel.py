
from aiogram.dispatcher import FSMContext
from aiogram import executor
from loader import dp, bot
from game_engein import Pixelway
from log_info import log_for_mess_handlers


game = Pixelway(12,12)


async def welcome(message):
    await log_for_mess_handlers((message))
    await message.answer( game.text, reply_markup=game._keys)


@dp.message_handler(commands=['start'])
async def start(message, state: FSMContext):
    user_id = message.chat.id
    game.gen()
    game.keys()
    async with state.proxy() as data:
        data[user_id] = {}
        data[user_id]['box'] = game.img
        data[user_id]['xy'] = (game.x, game.y)
    await welcome(message)


@dp.callback_query_handler()
async def callback_inline(call, state: FSMContext):
    user_id = call.message.chat.id
    async with state.proxy() as data:
        game.img = data[user_id]['box']
        game.x, game.y =data[user_id]['xy']

    await joystick(call.data)
    async with state.proxy() as data:
        data[user_id]['box'] = game.img
        data[user_id]['xy'] = (game.x, game.y)
    text = game.text
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=game._keys )


async def joystick(data):
    if data in game.kdoc.values() or data == 'refr':
        getattr(game, data)()
    else:
        pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

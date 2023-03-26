from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot("BOT TOKEN")
dp = Dispatcher(bot)
all_t = ["1891-1916", "1917-1940", "1941-1965", "1966-1985", "1986-1992", "1993-2014"]


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
  inline_btn1=InlineKeyboardButton("Пример работы", callback_data="example")
  inline_btn2 = InlineKeyboardButton("Собственный запрос", callback_data="do")
  inline_kb = InlineKeyboardMarkup().add(inline_btn1).add(inline_btn2)
  await message.reply(text=f"Привет, {message.from_user.first_name}!\nЯ бот, написанный командой \"Тяжело\" на хакатоне ВШЭ\nЗдесь можно получить портрет эпохи прислав дату и место\nВыбирай что ты хочешь:", reply_markup=inline_kb)


@dp.callback_query_handler(text="example")
async def call_example(callback: types.CallbackQuery):
    await callback.answer("Код выполняется")
    await callback.message.answer_photo(photo="https://replit.com/@dvervevre/tagelo#%D0%91%D0%B5%D0%B7%20%D0%BD%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F.png", caption="1941-1945, Cанкт-Петербург")

@dp.callback_query_handler(text="do")
async def call_another(callback: types.CallbackQuery):
    await callback.message.answer("Пришлите запрос форматом гггг-гггг, место:")



@dp.message_handler()
async def all(message: types.Message):
    if message.text.count("-") & message.text.count(","):
        global all_t
        start = end = 0
        place = ""
        t=message.text[:message.text.find(",")]
        if t in all_t:
            start = message.text[:message.text.find("-")]
            t = message.text[message.text.find("-") + 1:]
            end = t[:t.find(",")]
            place = t[t.find(",") + 2:]
        else:
            await message.answer("Вы ввели неправильную дату\nМожно вводить только:\n1891-1916\n1917-1940\n1941-1965\n1966-1985\n1986-1992\n1993-2014")
        if end != start:
            pipeline(start, end, place)
            await message.answer_photo("/kaggle/working/images/1.png",caption=message.text)
            await message.answer_photo("/kaggle/working/images/2.png",caption=message.text)
            await message.answer_photo("/kaggle/working/images/3.png",caption=message.text)
            await message.answer_photo("/kaggle/working/images/4.png",caption=message.text)
            await message.answer_photo("/kaggle/working/images/5.png",caption=message.text)
            await message.answer_photo("/kaggle/working/images/6.png",caption=message.text)
            await message.answer_photo("/kaggle/working/images/7.png",caption=message.text)
            await message.answer_photo("/kaggle/working/images/8.png",caption=message.text)
    else:
        await message.reply("Я вас не понял(")



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
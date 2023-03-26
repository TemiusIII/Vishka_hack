from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot("5864672896:AAGN9RkSx5HFguOPt96wdCffRFH-ykHbeDc")
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
  inline_btn1=InlineKeyboardButton("Пример работы", callback_data="example")
  inline_btn2 = InlineKeyboardButton("Собственный запрос", callback_data="do")
  inline_kb = InlineKeyboardMarkup().add(inline_btn1).add(inline_btn2)
  await message.reply(text=f"Привет, {message.from_user.first_name}!\nЯ бот, написанный командой \"Тяжело\" на хакатоне ВШЭ\nЗдесь можно получить портрет эпохи прислав дату и место\nВыбирай что ты хочешь:", reply_markup=inline_kb)

@dp.message_handler()
async def all(message: types.Message):
    await message.reply("Я вас не понял(")

@dp.callback_query_handler(text="example")
async def call_example(callback: types.CallbackQuery):
    await callback.answer("Код выполняется")
    await callback.message.answer_photo(photo="https://replit.com/@dvervevre/tagelo#%D0%91%D0%B5%D0%B7%20%D0%BD%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F.png", caption="1941-1945, Cанкт-Петербург")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

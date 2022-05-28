import logging
import wikipedia
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.ERROR)

bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


def getwiki(word: str):
    wikipedia.set_lang("ru")
    try:
        p_wiki = wikipedia.page(word)
        p_wiki_summary = p_wiki.summary
        p_wiki_title = p_wiki_summary.split('—')
        return f'<b>{str(p_wiki_title[0])}</b>' + '—' + str(''.join(p_wiki_title[1:]))
    except wikipedia.exceptions.PageError:
        return f'<i>Такого слова нет в словаре Википедии!</i>'


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        f'<b>Привет {message.from_user.first_name}</b>\n\nВведи слово для поиска в Википедии:')


@dp.message_handler()
async def wikitext(message: types.Message):
    await message.answer(getwiki(message.text))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

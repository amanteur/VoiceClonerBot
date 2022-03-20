import logging
import os
from pathlib import Path

from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, File, Message, CallbackQuery, input_file
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiofiles.os

import config
from bot import keyboard as kb
from bot.settings import *
from bot import utils

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'], state='*')
async def send_welcome(message: Message):
    """
    Starting command.
    """
    username = message.from_user.username
    msg = START_MESSAGE.format(username)
    await message.reply(msg,
                        reply_markup=kb.kb_start)
    await States.INIT_STATE.set()


@dp.callback_query_handler(lambda c: c.data in ['get_help'])
@dp.message_handler(commands=['help'], state='*')
async def send_help(message: Message):
    """
    Help command to show all bot functions.
    """

    await message.reply(HELPER_MESSAGE)


@dp.message_handler(commands=['add_voice'], state='*')
@dp.callback_query_handler(
    lambda c: c.data == 'add_voice',
    state='*'
)
async def process_callback_add_voice(callback_query: CallbackQuery):
    """
    Function to add (or not to add) a new voice to database.
    :param callback_query:
    :return:
    """
    await bot.answer_callback_query(callback_query.id)

    if utils.check_user_existence(callback_query.message.chat.id):
        msg = "I already have your voice.\n" \
              "Do you want to re-record it?"
        markup = kb.kb_binary_answer
        await States.USER_EXIST.set()
    else:
        utils.add_user(callback_query.message.chat.id)
        msg = LANGUAGE_MESSAGE
        markup = kb.kb_languages
        await States.USER_NOT_EXIST.set()

    await bot.send_message(
        callback_query.message.chat.id,
        msg,
        reply_markup=markup
    )


@dp.callback_query_handler(
    lambda c: c.data in ['add_voice_yes', 'add_voice_no'],
    state=States.USER_EXIST
)
async def process_callback_add_voice_yes_no(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data == 'add_voice_yes':
        msg = LANGUAGE_MESSAGE
        markup = kb.kb_languages
        await States.USER_NOT_EXIST.set()
        await bot.send_message(
            callback_query.message.chat.id,
            msg,
            reply_markup=markup
        )
    else:
        await States.INIT_STATE.set()
        await bot.send_message(
            callback_query.message.chat.id,
            RESTART_MESSAGE
        )


@dp.callback_query_handler(
    lambda c: c.data in ['select_english', 'select_russian'],
    state=States.USER_NOT_EXIST,
)
async def process_callback_add_voice_lang(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data == 'select_english':
        msg = TRAIN_MESSAGE.format(TRAIN_LINES_ENG)
        await States.USER_ADD_ENGLISH.set()
    else:
        msg = TRAIN_MESSAGE.format(TRAIN_LINES_RUS)
        await States.USER_ADD_RUSSIAN.set()
    await bot.send_message(
        callback_query.message.chat.id,
        msg
    )


async def handle_voice_msg(
        file: File,
        file_name: str,
        path: str):
    Path(f"{path}").mkdir(
        parents=True, exist_ok=True
    )
    await bot.download_file(
        file_path=file.file_path, destination=f"{path}/{file_name}"
    )


@dp.message_handler(
    content_types=[ContentType.VOICE],
    state=[States.USER_ADD_RUSSIAN, States.USER_ADD_ENGLISH]
)
async def voice_message_handler(message: Message, state: FSMContext):
    voice = await message.voice.get_file()
    current_state = await state.get_state()
    if current_state == States.USER_ADD_RUSSIAN.state:
        filename = f"{message.from_user.id}_rus.ogg"
    else:
        filename = f"{message.from_user.id}_eng.ogg"

    utils.update_user(message.from_user.id, filename)
    await handle_voice_msg(file=voice, file_name=filename, path=VOICE_SAVE_PATH)
    await message.reply(SAVE_VOICE_MESSAGE, reply_markup=kb.kb_languages)
    await States.USER_NOT_EXIST.set()


async def handle_synth_message(
        message,
        text: str,
        user_id: int,
        language: str):
    data = utils.find_user(user_id)
    if language == '__label__en' and data[3] is not None:
        voice_path = data[3]
    elif language == '__label__ru' and data[1] is not None:
        voice_path = data[1]
    else:
        voice_path = ''
    full_voice_path = os.path.join(VOICE_SAVE_PATH, voice_path)
    lang = 'russian' if language == '__label__ru' else 'english'
    if not os.path.isfile(full_voice_path) or not voice_path:
        await message.reply(
            NO_LANGUAGE_MESSAGE.format(lang), reply_markup=kb.kb_languages
        )
        await States.USER_NOT_EXIST.set()
    else:
        synth_path_wav, synth_path_ogg = utils.synth_voice(text, full_voice_path, user_id, lang)
        file = input_file.InputFile(synth_path_ogg)
        await message.answer_voice(file, caption="Synthesized")
        await aiofiles.os.remove(synth_path_wav)
        await aiofiles.os.remove(synth_path_ogg)


@dp.message_handler(commands=['synth'], state='*')
@dp.message_handler(
    is_reply=True,
    text_contains=BOT_MENTION_NAME,
    chat_type='group',
    state='*'
)
@dp.message_handler(
    is_forwarded=True,
    chat_type='private',
    state='*'
)
async def synth_handle(message: Message):
    user_id = message.from_user.id
    if message.text.startswith('/synth'):
        text = message.text.lstrip('/synth')
    elif "reply_to_message" in message:
        text = message.reply_to_message.text
    else:
        text = message.text
    language = utils.get_language(text)
    await message.reply(SYNTH_MESSAGE)
    await handle_synth_message(message, text, user_id, language)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

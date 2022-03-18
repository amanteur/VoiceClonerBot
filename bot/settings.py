from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    INIT_STATE = State()
    USER_EXIST = State()
    USER_NOT_EXIST = State()
    USER_ADD_RUSSIAN = State()
    USER_ADD_ENGLISH = State()


VOICE_SAVE_PATH = 'bot/files/voice'
EMB_SAVE_PATH = 'bot/files/emb'
VOICE_OUT_PATH = 'bot/files/temp_transformed_voice'

BOT_TOKEN = ""
BOT_NAME = 'Voice Cloner'
BOT_MENTION_NAME = '@VoiceClonerBot'

START_MESSAGE = "Hi, {}!\n" \
                f"I'm {BOT_NAME} and I can clone your voice.\n" \
                "Enter /help to see all functionality."

HELPER_MESSAGE = "It is a help command.\n" \
                 "You can synthesize your voice based on some text via this bot.\n\n" \
                 "Available functions:\n\n" \
                 "/start: \n" \
                 "Start the bot and follow the guidance to add your voice.\n\n" \
                 "/synth 'YOUR TEXT': \n" \
                 "Synthesize 'YOUR TEXT' with your voice.\n\n" \
                 "@VoiceClonerBot with reply to some text: \n" \
                 "Synthesize text from replied message with your voice " \
                 "(Available only in group chats).\n\n" \
                 "Forward message to bot: \n" \
                 "Synthesize text from forwarded message" \
                 "(Available only in private chats)"

LANGUAGE_MESSAGE = "Please select the language " \
                   "of your preferred speech."

RESTART_MESSAGE = 'Ok, if you want to start again ' \
                  'just type /start.'

SAVE_VOICE_MESSAGE = "Ok, I've got your voice " \
                     "and saved you in my database!\n" \
                     "You can add another language too!\n" \
                     "Or just ignore it."

TRAIN_MESSAGE = """
Start recording your voice and read these lines:
{}
"""

TRAIN_LINES_RUS = """
Что вершит судьбу человека в этом мире?
Некое незримое существо или закон?
Подобно длани господней парящей над миром.
По крайней мере, истина - то, что человек не властен даже над своей волей.
"""

TRAIN_LINES_ENG = """
We're no strangers to love
You know the rules and so do I
A full commitment's what I'm thinking of
You wouldn't get this from any other guy.
"""

SYNTH_MESSAGE = "Wait a bit, I synthesize your {} message..."


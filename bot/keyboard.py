from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# initial keyboard
btn_add_voice = InlineKeyboardButton('Add my voice!', callback_data='add_voice')

kb_start = InlineKeyboardMarkup(row_width=1)
kb_start.add(btn_add_voice)


# binary answer
btn_yes = InlineKeyboardButton('Yes!', callback_data='add_voice_yes')
btn_no = InlineKeyboardButton('Nope.', callback_data='add_voice_no')

kb_binary_answer = InlineKeyboardMarkup(row_width=2)
kb_binary_answer.insert(btn_yes)
kb_binary_answer.insert(btn_no)

# which language to record

btn_eng = InlineKeyboardButton('English', callback_data='select_english')
btn_rus = InlineKeyboardButton('Russian', callback_data='select_russian')

kb_languages = InlineKeyboardMarkup(row_width=2)
kb_languages.insert(btn_eng)
kb_languages.insert(btn_rus)

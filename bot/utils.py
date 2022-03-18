from bot.database import DB, User
from typing import Tuple


def check_user_existence(user_id: int) -> bool:
    db = DB()
    db.setup_users()
    row = db.get_user(user_id)
    if row is None:
        return False
    else:
        return True


def add_user(user_id: int) -> None:
    db = DB()
    user = User(user_id)
    db.add_user(user)


def update_path(path: str) -> Tuple[str, str]:
    path_tuple = ()
    if path.endswith('ogg'):
        # it is a voice file
        if path.split('.')[0].endswith('eng'):
            path_tuple = ('eng_path_voice', path)
        elif path.split('.')[0].endswith('rus'):
            path_tuple = ('rus_path_voice', path)
    # using numpy at this moment
    elif path.endswith('npy'):
        # it is an embedding
        if path.split('.')[0].endswith('eng'):
            path_tuple = ('eng_path_emb', path)
        elif path.split('.')[0].endswith('rus'):
            path_tuple = ('rus_path_emb', path)
    return path_tuple


def update_user(user_id: int, path: str = None) -> None:
    path = update_path(path)
    db = DB()
    db.update_user(user_id, path)


def find_user(user_id: int) -> Tuple:
    db = DB()
    data = db.get_user(user_id)
    return data

def synth_voice(text, voice_path, voice_out_dir):
    # PUT YOUR MODEL HERE
    # synth_voice = model(text, voice_path)
    # voice_out_path = os.path.join(voice_out_dir, voice_path)

    # SAVE synth_voice TO voice_out_path

    return "bot/files/voice/604592193_eng.ogg"



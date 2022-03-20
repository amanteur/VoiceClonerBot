from bot.database import DB, User
from typing import Tuple
import os
import soundfile as sf
import numpy as np
import fasttext
from model import synth_waveform
from bot.settings import *
import subprocess


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


def get_language(text) -> str:
    model = fasttext.load_model('model/lang_classification/saved_models/lid.176.ftz')
    label, _ = model.predict(text, k=1)
    return label[0]


def synth_voice(text, voice_path, user_id, language):
    waveform, sample_rate = synth_waveform(text, voice_path)
    file_name_wav = f'{user_id}_{language}.wav'
    file_name_ogg = f'{user_id}_{language}.ogg'
    fpath_wav = os.path.join(VOICE_OUT_PATH, file_name_wav)
    fpath_ogg = os.path.join(VOICE_OUT_PATH, file_name_ogg)
    sf.write(fpath_wav, waveform.astype(np.float32), sample_rate)
    subprocess.run(["ffmpeg", '-i', fpath_wav, '-acodec', 'libopus', fpath_ogg, '-y'])
    print(fpath_wav, fpath_ogg)
    return fpath_wav, fpath_ogg



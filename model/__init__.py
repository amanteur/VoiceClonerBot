import warnings
warnings.filterwarnings(action="ignore")
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from encoder.params_model import model_embedding_size as speaker_embedding_size
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from g2p.train import g2p
from pathlib import Path
import soundfile as sf
import numpy as np

_current_dir = Path(__file__).parent.resolve()
_enc_model_fpath = _current_dir.joinpath(Path("encoder/saved_models/pretrained.pt"))
_syn_model_dir = _current_dir.joinpath("synthesizer/saved_models/logs-pretrained/taco_pretrained")
_voc_model_fpath = _current_dir.joinpath("vocoder/saved_models/pretrained/pretrained.pt")

encoder.load_model(_enc_model_fpath)
synthesizer = Synthesizer(_syn_model_dir)
vocoder.load_model(_voc_model_fpath)

from inference import synth

def synth_waveform(text, voice_path):
    generated_voice = synth(text, voice_path, synthesizer)
    
    return generated_voice, synthesizer.sample_rate
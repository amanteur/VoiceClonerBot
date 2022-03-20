from encoder import inference as encoder
from vocoder import inference as vocoder
from g2p.train import g2p
import numpy as np
import librosa
import soundfile as sf

def synth(text, voice_path, synthesizer):
    preprocessed_wav = encoder.preprocess_wav(voice_path)
    original_wav, sampling_rate = librosa.load(voice_path)
    preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
    embed = encoder.embed_utterance(preprocessed_wav)
    texts = [text]
    texts = g2p(texts)
    embeds = [embed]
    specs = synthesizer.synthesize_spectrograms(texts, embeds)
    spec = specs[0]
    generated_wav = vocoder.infer_waveform(spec)
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

    return generated_wav
    
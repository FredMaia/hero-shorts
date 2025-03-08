import torch
from TTS.api import TTS

model='tts_models/en/ljspeech/fast_pitch'

device = "cuda" if torch.cuda.is_available() else "cpu"

def generate_audio(text="A journey of a thousand miles begins with a little single step"):
    tts = TTS(model_name=model).to(device)
    tts.tts_to_file(text=text, file_path='outputs/output.wav')
    return "outputs/output.wav"

def get_models():
    return 'tts models'

print(generate_audio())
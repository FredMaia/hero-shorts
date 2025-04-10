from TTS.api import TTS

audio_referencia = "audio2.ogg"

texto = "Testando a voz do personagem. Gostaria de entender como esse processo é feito."

# tts_models/multilingual/multi-dataset/your_tts
# tts_models/pt/cv/your_tts
# tts_models/multilingual/multi-dataset/xtts_v2 - licença enjoada
# tts_models/en/multi-dataset/tortoise-v2
# pt-br

modelo = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

modelo.tts_to_file(
    text=texto, 
    speaker_wav=audio_referencia, 
    file_path="voz_gerada.wav", 
    language="pt-br"
)
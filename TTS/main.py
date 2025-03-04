# import os
# import torch
# from TTS.api import TTS

# class TextToSpeechGenerator:
#     def __init__(self, language='pt', model_name=None):
#         # Verificar disponibilidade de GPU
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         print(f"Usando dispositivo: {self.device}")

#         # Configurações de modelos para português
#         self.pt_models = {
#             'vits': 'tts_models/pt/css10/vits',
#             'fakquer': 'tts_models/pt/extra/male-fakquer'
#         }
        
#         # Selecionar modelo padrão se não especificado
#         if not model_name:
#             model_name = self.pt_models['vits']
        
#         # Inicializar TTS
#         print(f"Carregando modelo: {model_name}")
#         self.tts = TTS(model_name=model_name).to(self.device)
    
#     def generate_audio(self, text, output_dir='audio_outputs', filename=None):
#         """
#         Gerar áudio a partir de texto
        
#         :param text: Texto para conversão
#         :param output_dir: Diretório para salvar áudios
#         :param filename: Nome personalizado do arquivo
#         :return: Caminho completo do arquivo de áudio
#         """
#         # Criar diretório se não existir
#         os.makedirs(output_dir, exist_ok=True)
        
#         # Gerar nome de arquivo
#         if not filename:
#             filename = f"audio_{abs(hash(text))}.wav"
        
#         # Caminho completo do arquivo
#         output_path = os.path.join(output_dir, filename)
        
#         try:
#             # Gerar áudio
#             self.tts.tts_to_file(
#                 text=text, 
#                 file_path=output_path
#             )
            
#             print(f"Áudio gerado: {output_path}")
#             return output_path
        
#         except Exception as e:
#             print(f"Erro na geração de áudio: {e}")
#             return None
    
#     def list_portuguese_models(self):
#         """Listar modelos disponíveis para português"""
#         return list(self.pt_models.values())

# def main():
#     # Inicializar gerador de áudio
#     try:
#         tts_generator = TextToSpeechGenerator()
        
#         # Textos para teste
#         textos = [
#             "Olá, este é um teste de geração de voz com Coqui TTS no Windows",
#             "Criando conteúdo viral com tecnologia de ponta",
#             "Inteligência artificial transformando a criação de mídia"
#         ]
        
#         # Gerar áudios para cada texto
#         for texto in textos:
#             tts_generator.generate_audio(texto)
        
#         # Mostrar modelos disponíveis
#         print("\nModelos de Português:")
#         for modelo in tts_generator.list_portuguese_models():
#             print(modelo)
    
#     except Exception as e:
#         print(f"Erro durante a execução: {e}")
#         print("Possíveis causas:")
#         print("1. Dependências não instaladas corretamente")
#         print("2. Problemas com instalação do PyTorch")
#         print("3. Modelo de TTS não baixado")

# if __name__ == "__main__":
#     main()

import torch
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"

def generate_audio(text="A journey of a thousand miles begins with a single"):
    tts = TTS(model_name='tts_models/en/ljspeech/fast_pitch').to(device)
    tts.tts_to_file(text=text, file_path='outputs/output.wav')
    return "outputs/output.wav"

print(generate_audio())
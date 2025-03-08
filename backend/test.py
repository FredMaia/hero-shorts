from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip

from PIL import ImageFont
import math

def create_animated_caption(word_clips, duration):
    """Anima as palavras aparecendo sequencialmente com fade-in."""
    word_animations = []
    current_time = 0
    
    for word, word_duration in word_clips:
        txt_clip = TextClip(word, fontsize=80, color='white', 
                          font='Arial-Bold', stroke_color='black', stroke_width=2)
        txt_clip = txt_clip.set_start(current_time).set_duration(duration)
        txt_clip = txt_clip.crossfadein(0.5).set_position(('center', 0.7), relative=True)
        word_animations.append(txt_clip)
        current_time += word_duration
    
    return CompositeVideoClip(word_animations)

def process_segment(segment):
    """Processa um segmento de vídeo com legendas animadas."""
    # Carrega o vídeo e áudio
    video = VideoFileClip(segment['video_path'])
    audio = AudioFileClip(segment['audio_path'])
    video = video.set_audio(audio)
    
    # Configurações de legenda
    script = segment['script_part']
    words = script.split()
    n_words = len(words)
    word_duration = segment['duration'] / n_words
    
    # Divide o texto em palavras com durações
    word_clips = []
    cumulative_text = []
    
    # Calcula o tamanho da fonte dinâmico (ajuste para shorts)
    base_font_size = int(video.size[1] * 0.09)  # 9% da altura do vídeo
    
    for idx, word in enumerate(words):
        cumulative_text.append(word)
        txt_clip = TextClip(' '.join(cumulative_text), fontsize=base_font_size, 
                          color='white', font='Impact', method='label',
                          align='center', size=video.size)
        txt_clip = txt_clip.set_start(idx * word_duration).set_duration(word_duration)
        txt_clip = txt_clip.fadein(0.2).fadeout(0.2)
        word_clips.append(txt_clip)
    
    # Combina todas as legendas
    final_text = CompositeVideoClip(word_clips).set_position('center')
    
    # Combina vídeo e legendas
    final_video = CompositeVideoClip([video, final_text])
    
    return final_video

# Processa todos os segmentos
final_clips = []
segments = [{'script_part': 'Technology has significantly impacted the modern world, connecting us in ways previously unimaginable.', 'video_path': './temp_video_afcb4c7f-0013-4f94-b55f-d8612658b314.mp4', 'audio_path': './audio_part_0.wav', 'duration': 6.98}, {'script_part': 'From smartphones to virtual reality, technology has revolutionized how we learn, work, and communicate.', 'video_path': './temp_video_590d0391-e9f6-4b54-b685-d062db016147.mp4', 'audio_path': './audio_part_1.wav', 'duration': 7.21}, {'script_part': 'In the traditional classroom, technology has transformed teaching methods, making learning more interactive and engaging.', 'video_path': './temp_video_41b43512-714f-48b9-ace6-23aff5c46dd8.mp4', 'audio_path': './audio_part_2.wav', 'duration': 7.34}, {'script_part': 'Educators can now use digital tools to track student progress, personalize learning, and connect with students remotely.', 'video_path': './temp_video_a5a773a5-1f16-4103-956c-e5e510fa2b3e.mp4', 'audio_path': './audio_part_3.wav', 'duration': 8.26}, {'script_part': 'As technology continues to advance, its impact on education will only become more profound, shaping the future of learning.', 'video_path': './temp_video_50e8c354-09ef-4639-9b7e-d587f9977d3f.mp4', 'audio_path': './audio_part_4.wav', 'duration': 7.83}]

for segment in segments:  # Substituir 'segments' por sua variável
    processed = process_segment(segment)
    final_clips.append(processed)

# Concatena todos os segmentos
final_video = concatenate_videoclips(final_clips)

# Para vídeos verticais (shorts)
final_video = final_video.resize(height=1920).crop( 
    x1=((final_video.size[0] - 1080)/2), 
    y1=0, 
    width=1080, 
    height=1920
)

# Salva o resultado
final_video.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
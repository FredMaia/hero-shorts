import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import httpx
import json
import uuid

import torch
from groq import Groq
from TTS.api import TTS

from moviepy.editor import AudioFileClip, TextClip, VideoFileClip, ColorClip, concatenate_videoclips, CompositeVideoClip
from pydantic import BaseModel
from moviepy.video.fx.resize import resize
from PIL import Image

model='tts_models/en/ljspeech/fast_pitch'

device = "cuda" if torch.cuda.is_available() else "cpu"

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    prompt: str

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# OUTPUT_DIR = "outputs"
OUTPUT_DIR = "./"
# AUDIO_DIR = "outputs_audio"
AUDIO_DIR = "./"


os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

groq_client = Groq(api_key=GROQ_API_KEY)

def make_movie_py_compatible_with_pillow():
    try:
        if not hasattr(Image, 'ANTIALIAS'):
            if hasattr(Image, 'LANCZOS'):
                Image.ANTIALIAS = Image.LANCZOS
                print("Correção aplicada: PIL.Image.ANTIALIAS -> PIL.Image.LANCZOS")
            else:
                try:
                    from PIL import Image
                    Image.ANTIALIAS = Image.Resampling.LANCZOS
                    print("Correção aplicada: PIL.Image.ANTIALIAS -> PIL.Image.Resampling.LANCZOS")
                except (ImportError, AttributeError):
                    print("AVISO: Não foi possível aplicar a correção para PIL.Image.ANTIALIAS")
    except ImportError:
        print("AVISO: Não foi possível importar os módulos necessários para a correção do PIL")

def prepare_video_for_shorts(video_path, audio_path):
    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        target_width = 1080
        target_height = 1920
        
        if video.w/video.h > target_width/target_height:
            new_height = target_height
            new_width = int(video.w * new_height / video.h)
            resized_video = video.resize(height=new_height, width=new_width)
            
            x_offset = (new_width - target_width) // 2
            cropped_video = resized_video.crop(x1=x_offset, y1=0, 
                                               x2=x_offset + target_width, 
                                               y2=target_height)
        else:
            new_width = target_width
            new_height = int(video.h * new_width / video.w)
            resized_video = video.resize(width=new_width, height=new_height)
            
            y_offset = (new_height - target_height) // 2 if new_height > target_height else 0
            height_to_use = min(new_height, target_height)
            
            cropped_video = resized_video.crop(x1=0, y1=y_offset, 
                                              x2=target_width, 
                                              y2=y_offset + height_to_use)
            
            if new_height < target_height:
                black_clip = ColorClip(size=(target_width, target_height), color=(0, 0, 0))
                black_clip = black_clip.set_duration(video.duration)
                
                y_position = (target_height - new_height) // 2
                cropped_video = cropped_video.set_position(("center", y_position))
                cropped_video = CompositeVideoClip([black_clip, cropped_video])
        
        if cropped_video.duration < audio.duration:
            cropped_video = cropped_video.loop(duration=audio.duration)
        else:
            cropped_video = cropped_video.subclip(0, audio.duration)
        
        cropped_video = cropped_video.set_audio(audio)
        
        return cropped_video
    
    except Exception as e:
        raise Exception(f"Erro ao preparar vídeo: {str(e)}")

def generate_audio(text, file_path):
    try:
        tts = TTS(model_name=model).to(device)
        tts.tts_to_file(text=text, file_path=file_path)
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar áudio: {str(e)}")


def generate_script(prompt: str) -> dict:
    try:
        chat_completion = groq_client.chat.completions.create(
             messages=[{
                "role": "user",
                "content": f"""
                Generate a short video script (30-60 seconds) divided into 5 parts and 5 stock video keywords.
                Each part should be a short sentence or paragraph that will be narrated separately.
                
                JSON format: {{
                    "parts": [
                        "part 1 of the script",
                        "part 2 of the script",
                        "part 3 of the script",
                        "part 4 of the script",
                        "part 5 of the script"
                    ],
                    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
                }}
                
                Topic: {prompt}
                """
            }],
            model="mixtral-8x7b-32768",
            response_format={"type": "json_object"}
        )
        
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no Groq: {str(e)}")


def get_stock_video(keyword: str) -> str:
    try:
        url = f"https://api.pexels.com/videos/search?query={keyword} vertical&per_page=15&orientation=portrait"
        headers = {"Authorization": PEXELS_API_KEY}
        
        response = requests.get(url, headers=headers)
        video_data = response.json()

        if video_data.get('videos'):
            for video in video_data['videos']:
                for video_file in video['video_files']:
                    width = video_file.get('width', 0)
                    height = video_file.get('height', 0)
                    
                    if height > width:
                        return download_video(video_file['link'])
            
            video_file = video_data['videos'][0]['video_files'][0]['link']
            return download_video(video_file)
        
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no Pexels: {str(e)}")


def download_video(url: str) -> str:
    try:
        local_path = os.path.join(OUTPUT_DIR, f"temp_video_{uuid.uuid4()}.mp4")
        with httpx.stream("GET", url) as response:
            with open(local_path, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
        return local_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao baixar vídeo: {str(e)}")


def generate_video_segments(script_parts: list[str], video_paths: list[str]) -> list[dict]:
    segments = []
    
    for i, (part, video_path) in enumerate(zip(script_parts, video_paths)):
        try:
            print(f"Processando segmento {i+1}/{len(script_parts)}")
            print(f"Texto: {part[:50]}...")  
            
            audio_path = os.path.join(AUDIO_DIR, f"audio_part_{i}.wav")
            generate_audio(part, audio_path)
            
            if not os.path.exists(audio_path):
                raise Exception(f"Falha ao gerar arquivo de áudio para o segmento {i}")
                
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration
            audio_clip.close() 
            
            print(f"Áudio gerado: {audio_path}, duração: {audio_duration}s")
            
            segments.append({
                "script_part": part,
                "video_path": video_path,
                "audio_path": audio_path,
                "duration": audio_duration
            })
            
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"ERRO ao gerar segmento de vídeo {i}: {str(e)}")
            print(error_trace)
            continue
    
    if not segments:
        raise HTTPException(status_code=500, detail="Nenhum segmento de vídeo pôde ser gerado")
    
    print(f"Total de segmentos gerados: {len(segments)}/{len(script_parts)}")
    print(segments)
    return segments

def create_final_video(segments: list[dict]) -> str:
    clips = []
    max_clip_duration = 10  
    
    try:
        make_movie_py_compatible_with_pillow()
        
        for segment in segments:
            try:
                print(f"Processando vídeo: {segment['video_path']}")
                print(f"Processando áudio: {segment['audio_path']}")
                
                try:
                    clip = VideoFileClip(segment["video_path"])
                except Exception as e:
                    print(f"Erro ao carregar vídeo: {str(e)}")
                    continue
                    
                try:
                    audio = AudioFileClip(segment["audio_path"])
                except Exception as e:
                    print(f"Erro ao carregar áudio: {str(e)}")
                    clip.close()
                    continue
                
                print(f"Dimensões originais do vídeo: {clip.w}x{clip.h}")
                
                try:
                    aspect_ratio = round((clip.w/clip.h), 4)
                    target_ratio = 9/16 
                    
                    if aspect_ratio < target_ratio:
                        new_height = int(clip.w / target_ratio)
                        y1 = max(0, int((clip.h - new_height) / 2))
                        y2 = min(clip.h, y1 + new_height)
                        clip = clip.crop(x1=0, y1=y1, x2=clip.w, y2=y2)
                    else:
                        new_width = int(clip.h * target_ratio)
                        x1 = max(0, int((clip.w - new_width) / 2))
                        x2 = min(clip.w, x1 + new_width)
                        clip = clip.crop(x1=x1, y1=0, x2=x2, y2=clip.h)
                    
                    clip = clip.resize(newsize=(1080, 1920))
                    
                    print(f"Vídeo redimensionado para: 1080x1920")
                except Exception as crop_error:
                    print(f"Erro durante o redimensionamento: {str(crop_error)}")
                    try:
                        clip = clip.resize(width=1080)
                        print(f"Fallback: redimensionado apenas pela largura: 1080x{clip.h}")
                    except:
                        print("Não foi possível redimensionar nem mesmo pelo método fallback")
                        clip.close()
                        audio.close()
                        continue
                
                try:
                    if clip.duration < audio.duration:
                        print(f"Vídeo mais curto que áudio, usando loop: {clip.duration}s < {audio.duration}s")
                        clip = clip.loop(duration=audio.duration)
                    else:
                        print(f"Cortando vídeo para duração do áudio: {audio.duration}s")
                        clip = clip.subclip(0, audio.duration)
                    
                    clip = clip.set_audio(audio)
                    
                    print("Áudio aplicado com sucesso")
                except Exception as duration_error:
                    print(f"Erro ao ajustar duração ou áudio: {str(duration_error)}")
                    clip.close()
                    audio.close()
                    continue
                
                try:
                    txt_clip = TextClip(
                        txt=segment["script_part"], 
                        fontsize=36,  
                        color='white', 
                        bg_color='rgba(0,0,0,0.5)',
                        size=(1000, None), 
                        method='caption'
                    )
                    txt_clip = txt_clip.set_duration(clip.duration)
                    txt_clip = txt_clip.set_position(('center', 'bottom'))
                    
                    final_clip = CompositeVideoClip([clip, txt_clip], size=(1080, 1920))
                    
                    print("Legenda adicionada com sucesso")
                except Exception as text_error:
                    print(f"Erro ao adicionar legenda: {str(text_error)}")
                    final_clip = clip
                
                clips.append(final_clip)
                print(f"Segmento processado com sucesso, duração: {final_clip.duration}s")
                
            except Exception as segment_error:
                import traceback
                error_trace = traceback.format_exc()
                print(f"ERRO ao processar segmento: {str(segment_error)}")
                print(error_trace)
                continue
        
        if not clips:
            raise Exception("Nenhum clip foi processado com sucesso")
        
        print(f"Total de clips processados: {len(clips)}")
        
        print("Iniciando concatenação dos clips...")
        final_video = concatenate_videoclips(clips, method="compose")
        print(f"Concatenação concluída, duração total: {final_video.duration}s")

        output_path = os.path.join(OUTPUT_DIR, f"shorts_{uuid.uuid4()}.mp4")
        
        print(f"Iniciando exportação do vídeo para: {output_path}")
        
        final_video.write_videofile(
            output_path, 
            fps=30,
            audio_codec='aac', 
            audio_bitrate='128k',
            bitrate='8000k',
            threads=4
        )
        
        print(f"Exportação concluída com sucesso")
        
        for clip in clips:
            clip.close()
        final_video.close()
        
        return output_path
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERRO CRÍTICO na geração do vídeo: {str(e)}")
        print(error_trace)
        
        for clip in clips if 'clips' in locals() else []:
            try:
                clip.close()
            except Exception as close_error:
                print(f"Erro ao fechar clip: {str(close_error)}")
                
        raise HTTPException(status_code=500, detail=f"Erro na geração do vídeo: {str(e)}")
    
@app.post("/generate-audio")
async def create_audio(request: dict):
    file_path = os.path.join(AUDIO_DIR, "output.wav")
    generate_audio(request["text"], file_path)
    return {"message": "Áudio criado com sucesso", "file_path": file_path}


@app.post("/generate-video")
async def create_video(request: VideoRequest):
    try:
        generated_data = generate_script(request.prompt)
        print("Dados gerados:", generated_data)
        
        video_paths = []
        for keyword in generated_data["keywords"]:
            try:
                video_path = get_stock_video(keyword)
                if video_path:
                    video_paths.append(video_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erro ao buscar vídeo para a palavra-chave '{keyword}': {str(e)}")
        
        min_length = min(len(video_paths), len(generated_data["parts"]))
        video_paths = video_paths[:min_length]
        script_parts = generated_data["parts"][:min_length]
        
        segments = generate_video_segments(script_parts, video_paths)
        
        final_video_path = create_final_video(segments)
        
        return {
            "message": "Vídeo criado com sucesso",
            "video_url": final_video_path,
            "segments": [
                {
                    "script": segment["script_part"],
                    "audio": segment["audio_path"],
                    "duration": segment["duration"]
                } for segment in segments
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a requisição: {str(e)}")

screen_width = 1080
screen_height = 1920

def get_transcribed_text(filename):
    audio = whisper.load_audio(filename)
    model = whisper.load_model("small", device="cpu")
    results = whisper.transcribe(model, audio, language="en")

    return results["segments"]

def get_text_clips(text, fontsize):
    text_clips = []
    for segment in text:
        for word in segment["words"]:
            text_clips.append(
                TextClip(word["text"],
                    fontsize=fontsize,
                    method='caption',
                    stroke_width=5, 
                    stroke_color="white", 
                    font="Arial-Bold",
                      color="white")
                .set_start(word["start"])
                .set_end(word["end"])   
                .set_position("center")
            )
    return text_clips

import whisper_timestamped as whisper

@app.get("/legenda")
async def create_captions():
    filename = "./short.mp4"
    # Loading the video as a VideoFileClip
    original_clip = VideoFileClip(filename)

    # Load the audio in the video to transcribe it and get transcribed text
    transcribed_text = get_transcribed_text(filename)
    # Generate text elements for video using transcribed text
    text_clip_list = get_text_clips(text=transcribed_text, fontsize=90)
    # Create a CompositeVideoClip that we write to a file
    final_clip = CompositeVideoClip([original_clip] + text_clip_list)

    final_clip.write_videofile("final.mp4")
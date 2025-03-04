from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import openai
import base64
import os

app = FastAPI()

class VideoPrompt(BaseModel):
    prompt: str
    style: Optional[str] = None

class VideoResponse(BaseModel):
    script: str
    video_url: Optional[str] = None
    error: Optional[str] = None

@app.post("/generate-video", response_model=VideoResponse)
async def generate_video(prompt: VideoPrompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um roteirista criativo de vídeos virais para redes sociais."},
                {"role": "user", "content": f"Crie um roteiro curto e viral para um vídeo sobre: {prompt.prompt}. " + 
                 "O roteiro deve ser conciso, com no máximo 30 segundos, e ter um gancho interessante."}
            ],
            max_tokens=300
        )
        
        script = response.choices[0].message.content.strip()
        
        return VideoResponse(
            script=script,
            video_url=None  
        )
    
    except Exception as e:
        return VideoResponse(
            script="",
            error=str(e)
        )
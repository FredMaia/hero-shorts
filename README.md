# 🚀 Hero shorts: **Transforme Texto em Vídeos Viralizáveis para TikTok, Reels e Shorts**  
*Crie conteúdo impactante em segundos com IA — 100% Gratuito!*

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/React-18%2B-61DAFB?logo=react" alt="React">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
</div>

---

## **Recursos disponíveis**  
- **🎥 Texto para Vídeo com IA**: Gere vídeos dinâmicos usando modelos do **Hugging Face** (Stable Video Diffusion) e **Coqui TTS** para voz realista.  
- **🖼️ Banco de Vídeos Grátis**: Integração com a API do **Pexels** para adicionar cenas profissionais ao seu conteúdo.  
- **📱 Templates Prontos**: Formatos otimizados para TikTok (9:16), Reels (1080x1920) e Shorts (YouTube).  
- **🎵 Trilhas Sonoras Automáticas**: Adicione músicas royalty-free com sincronização perfeita.  
- **⚡ Exporte em 1 Clique**: Vídeos em MP4 ou GIF, prontos para postar!  

---

## 🛠️ **Tecnologias Utilizadas**  
| **Frontend** (React)          | **Backend** (Python)           |  
|-------------------------------|---------------------------------|  
| ▶️ React + Typescript               | 🐍 FastAPI                     |  
| 🎨 Tailwind CSS               | 🤗 Hugging Face Transformers   |  
| 🎬 FFmpeg.wasm (Edição no Navegador) | 🐸 Coqui TTS (Text-to-Speech) |  
| 📱 PWA (App Offline)          | 🎞️ MoviePy (Processamento de Vídeo) |  
| 🌐 Axios (API Calls)          | 📸 Pexels API (Stock Videos)   |  

---

## 🎥 **Como Funciona?**  
1. **Digite um Prompt**: Ex: *"Um astronauta dançando numa galáxia neon, estilo cyberpunk"*.  
2. **Escolha um Template**: Para TikTok, Reels ou Shorts.  
3. **Personalize**: Adicione textos, músicas, ajuste a duração e os vídeos de fundo.
4. **Renderize**: A IA gera o vídeo em minutos usando modelos open-source!  

Demonstração: 

---

## 🚀 **Como rodar localmente:**  

### **Pré-requisitos**  
- Python 3.10+  
- Node.js 18+  
- API Keys (Grátis): [Hugging Face](https://huggingface.co/settings/tokens) e [Pexels](https://www.pexels.com/api/)
- ffmpeg
- image magick
- MSVC Compiler for C++

### **Passo a Passo**  
```bash
# Instale o Frontend
cd frontend
npm install
npm start

# Instale o Backend
cd ../backend

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

docker build -t video-generator .
docker run -p 8000:8000 --env-file .env video-generator
```

## 🏛️ Arquitetura do back-end

- 📜 Geração de roteiro (Groq API) → O sistema recebe um prompt e utiliza a Groq API para criar um roteiro estruturado.
- 🎬 Seleção de clipes (Pexels API) → Com base no roteiro gerado, a API do Pexels é usada para buscar vídeos relevantes.
- 🗣️ Conversão de texto em fala (Coqui TTS ou Kokoro) → O roteiro é transformado em áudio utilizando a API Coqui TTS ou Kokoro82M, ambos **open source**.
- 🎞️ Edição e legendagem (PyMovie & Whisper Timestamped) → O vídeo final é montado, sincronizando os clipes com o áudio gerado e adicionando legendas automáticas.

![App architecture](/backend/assets/arq.png)
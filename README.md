# 🚀 Text2Clip: **Transforme Texto em Vídeos Viralizáveis para TikTok, Reels e Shorts**  
*Crie conteúdo impactante em segundos com IA — 100% Gratuito!*

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/React-18%2B-61DAFB?logo=react" alt="React">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
</div>

---

## ✨ **Recursos Incríveis**  
- **🎥 Texto para Vídeo com IA**: Gere vídeos dinâmicos usando modelos do **Hugging Face** (Stable Video Diffusion) e **Coqui TTS** para voz realista.  
- **🖼️ Banco de Vídeos Grátis**: Integração com a API do **Pexels** para adicionar cenas profissionais ao seu conteúdo.  
- **📱 Templates Prontos**: Formatos otimizados para TikTok (9:16), Reels (1080x1920) e Shorts (YouTube).  
- **🎵 Trilhas Sonoras Automáticas**: Adicione músicas royalty-free com sincronização perfeita.  
- **⚡ Exporte em 1 Clique**: Vídeos em MP4 ou GIF, prontos para postar!  

---

## 🛠️ **Tecnologias Utilizadas**  
| **Frontend** (React)          | **Backend** (Python)           |  
|-------------------------------|---------------------------------|  
| ▶️ React + Vite               | 🐍 FastAPI                     |  
| 🎨 Tailwind CSS               | 🤗 Hugging Face Transformers   |  
| 🎬 FFmpeg.wasm (Edição no Navegador) | 🐸 Coqui TTS (Text-to-Speech) |  
| 📱 PWA (App Offline)          | 🎞️ MoviePy (Processamento de Vídeo) |  
| 🌐 Axios (API Calls)          | 📸 Pexels API (Stock Videos)   |  

---

## 🎥 **Como Funciona?**  
1. **Digite um Prompt**: Ex: *"Um astronauta dançando numa galáxia neon, estilo cyberpunk"*.  
2. **Escolha um Template**: Para TikTok, Reels ou Shorts.  
3. **Personalize**: Adicione textos, músicas e ajuste a duração.  
4. **Renderize**: A IA gera o vídeo em minutos usando modelos open-source!  

![Demo](https://via.placeholder.com/800x400.png?text=Demo+Text2Reels+-+Adicione+um+GIF+Impactante)  

---

## 🚀 **Comece Agora (Instalação em 2 Minutos)**  

### **Pré-requisitos**  
- Python 3.10+  
- Node.js 18+  
- API Keys (Grátis): [Hugging Face](https://huggingface.co/settings/tokens) e [Pexels](https://www.pexels.com/api/)  

### **Passo a Passo**  
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/text2reels.git
cd text2reels

# Instale o Frontend
cd frontend
npm install
npm run dev

# Instale o Backend
cd ../backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
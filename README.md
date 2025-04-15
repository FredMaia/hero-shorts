# 🚀 Hero shorts: **Transforme texto em vídeos curtos viralizáveis**  
*Crie conteúdo impactante em segundos com IA — 100% Gratuito!*

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/React-18%2B-61DAFB?logo=react" alt="React">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
</div>

---

![App frontend](/backend/assets/front.png)


## **Recursos disponíveis**  
- **Texto para vídeo com IA**: Gere vídeos dinâmicos usando modelos do **Hugging Face** (Stable Video Diffusion) e **Coqui TTS** para voz realista.  
- **Banco de Vídeos Grátis**: Integração com a API do **Pexels** para adicionar cenas profissionais ao seu conteúdo.  
- **Templates Prontos**: Formatos otimizados para TikTok, Reels e Shorts.  

---

## 🛠️ **Tecnologias Utilizadas**  
| **Backend** (Python)           |  
|-------------------------------|
|  FastAPI                     |  
|  Hugging Face Transformers   |  
|  Coqui TTS (Text-to-Speech) |  
|  MoviePy (Processamento de Vídeo) |  
|  Pexels API (Stock Videos)   |  

---

## 🎥 **Como Funciona?**  
1. **Digite um Prompt**: Ex: *"Um astronauta dançando numa galáxia neon, estilo cyberpunk"*.  
2. **Escolha um Template**: Para TikTok, Reels ou Shorts.  
3. **Personalize**: Adicione textos, músicas, ajuste a duração e os vídeos de fundo.
4. **Renderize**: A IA gera o vídeo em minutos usando modelos open-source!  

---

## 🚀 **Como rodar localmente:**  

### **Pré-requisitos**  
- Python 3.10+  
- Node.js 18+  
- API Keys (Grátis): [Hugging Face](https://huggingface.co/settings/tokens) e [Pexels](https://www.pexels.com/api/)
- ffmpeg
- image magick
- MSVC Compiler for C++



## 🏛️ Arquitetura do back-end

- 📜 Geração de roteiro (Groq API) → O sistema recebe um prompt e utiliza a Groq API para criar um roteiro estruturado.
- 🎬 Seleção de clipes (Pexels API) → Com base no roteiro gerado, a API do Pexels é usada para buscar vídeos relevantes.
- 🗣️ Conversão de texto em fala (Coqui TTS ou Kokoro) → O roteiro é transformado em áudio utilizando a API Coqui TTS ou Kokoro82M, ambos **open source**.
- 🎞️ Edição e legendagem (PyMovie & Whisper Timestamped) → O vídeo final é montado, sincronizando os clipes com o áudio gerado e adicionando legendas automáticas.

![App architecture](/backend/assets/arq.png)



## Considerações importantes

- 💡 O setup seria bem mais fácil com Docker, mas minha máquina quase virou uma torradeira tentando rodar os modelos no container

- 🕒 Talvez o vídeo demore para rodar, inicialize o backend com a flag `--timeout-keep-alive` para evitar timeouts
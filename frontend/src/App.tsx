import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

interface VideoResponse {
  videoUrl: string;
  message: string;
}

const App: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  // const [result, setResult] = useState<VideoResponse | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!prompt.trim()) {
      setError('Por favor, digite uma ideia para o vídeo');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/generate-video', 
        { prompt },  
        { responseType: 'blob' }  
    );

      const videoUrl = URL.createObjectURL(response.data);
      setResult(videoUrl);
    } catch (err) {
      setError('Erro ao gerar o vídeo. Verifique se o servidor está rodando.');
      console.error('Erro:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="stars"></div>
      <div className="glow"></div>
      
      <header>
        <h1>Hero<span>Shorts</span></h1>
        <p className="subtitle">Gerador de vídeos com IA</p>
      </header>

      <main>
        <div className="card">
          <h2>📝 Crie seu vídeo</h2>
          <p>Digite uma ideia e nosso sistema irá gerar um vídeo completo automaticamente!</p>
          
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Ex: Uma explicação sobre como a energia solar funciona"
                rows={4}
              />
              <div className="input-border"></div>
            </div>
            
            <button 
              type="submit" 
              disabled={loading}
              className={loading ? 'loading' : ''}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Gerando vídeo...
                </>
              ) : 'Gerar vídeo'}
            </button>
          </form>

          {error && <div className="error-message">{error}</div>}

          {loading && (
            <div className="process-container">
              <div className="process">
                <div className="step active">Gerando roteiro</div>
                <div className="step">Criando narração</div>
                <div className="step">Adicionando clipes</div>
                <div className="step">Sincronizando legendas</div>
                <div className="step">Finalizando vídeo</div>
              </div>
            </div>
          )}

          {result && (
            <div className="result-container">
              <h3>🎬 Seu vídeo está pronto!</h3>
              <div className="video-player">
                <video controls src={result}>
                  Seu navegador não suporta o elemento de vídeo.
                </video>
              </div>
              <div className="action-buttons">
                <a href={result} download className="download-btn">
                  Baixar vídeo
                </a>
                <button className="share-btn">
                  Compartilhar
                </button>
              </div>
            </div>
          )}
        </div>
        
        <div className="features">
          <div className="feature">
            <div className="icon">🤖</div>
            <h3>IA Avançada</h3>
            <p>Roteiros otimizados com Qwen 2.5</p>
          </div>
          <div className="feature">
            <div className="icon">🎙️</div>
            <h3>Voz Realista</h3>
            <p>Narração com Coqui TTS</p>
          </div>
          <div className="feature">
            <div className="icon">💬</div>
            <h3>Legendas Sincronizadas</h3>
            <p>Whisper Timestamped</p>
          </div>
        </div>
      </main>

      <footer>
        <p>Desenvolvido por FredMaia, utilizando tecnologias Open Source</p>
        <p>Nenhum limite de uso - 100% gratuito</p>
      </footer>
    </div>
  );
};

export default App;

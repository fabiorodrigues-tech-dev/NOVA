  #!/usr/bin/env python3
"""
NOVA Voice Studio — Interface Visual Interativa de Vozes Neurais
Servidor Web local com interface moderna (Dark Mode) para audição, teste e configuração de vozes.
"""

import os
import sys
import json
import asyncio
import tempfile
import subprocess
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

try:
    import edge_tts
except ImportError:
    print("❌ Erro: 'edge-tts' não encontrado. Execute: pip3 install edge-tts")
    sys.exit(1)

PORT = 5050
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config_voz.json"))

VOZES_CATALOGO = [
    {
        "id": "pt-BR-AntonioNeural",
        "nome": "Antônio",
        "idioma": "pt-BR",
        "genero": "Masculino",
        "tag": "Executiva / Natural",
        "descricao": "Voz padrão do NOVA. Tom sério, articulado e altamente profissional.",
        "icone": "👨‍💼",
        "frase_demo": "Olá, Fábio! Eu sou o Antônio, sua voz padrão no ecossistema NOVA. Todos os microsserviços estão operacionais."
    },
    {
        "id": "pt-BR-FranciscaNeural",
        "nome": "Francisca",
        "idioma": "pt-BR",
        "genero": "Feminino",
        "tag": "Acolhedora / Fluida",
        "descricao": "Voz executiva feminina. Dicção impecável, tom caloroso e natural.",
        "icone": "👩‍💼",
        "frase_demo": "Olá, Fábio! Sou a Francisca. Seus relatórios financeiros e candidaturas estão prontos para envio."
    },
    {
        "id": "pt-BR-FabioNeural",
        "nome": "Fábio",
        "idioma": "pt-BR",
        "genero": "Masculino",
        "tag": "Direta / Ágil",
        "descricao": "Voz masculina jovem e dinâmica. Ideal para respostas rápidas de terminal.",
        "icone": "👨‍💻",
        "frase_demo": "Fala, Fábio! Sou o Fábio Neural. Construímos uma arquitetura sólida em Java 21 e Spring Boot 3."
    },
    {
        "id": "pt-BR-ThalitaNeural",
        "nome": "Thalita",
        "idioma": "pt-BR",
        "genero": "Feminino",
        "tag": "Jovem / Expressiva",
        "descricao": "Tom conversacional e enérgico, com entonação espontânea.",
        "icone": "👩‍🎨",
        "frase_demo": "Oi, Fábio! Sou a Thalita. Seus estudos da Trilha Santander 2026 estão avançando com força total!"
    },
    {
        "id": "en-US-GuyNeural",
        "nome": "Guy (English)",
        "idioma": "en-US",
        "genero": "Masculino",
        "tag": "International Tech Lead",
        "descricao": "Voz americana executiva de alta credibilidade para entrevistas e clientes globais.",
        "icone": "🌐",
        "frase_demo": "Hello, Fabio! Guy speaking. Your international portfolio and FullStack Connect applications look solid."
    },
    {
        "id": "en-US-JennyNeural",
        "nome": "Jenny (English)",
        "idioma": "en-US",
        "genero": "Feminino",
        "tag": "Silicon Valley Native",
        "descricao": "Voz executiva americana fluida e polida para reuniões internacionais.",
        "icone": "✨",
        "frase_demo": "Hi, Fabio! Jenny here. Your Clean Architecture backend and Spring AI modules are fully verified."
    }
]

def carregar_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"voz_padrao": "pt-BR-AntonioNeural", "velocidade": "+0%", "tom": "+0Hz"}

def salvar_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

async def gerar_audio_bytes(texto: str, voz_id: str, taxa: str = "+0%") -> bytes:
    comunicador = edge_tts.Communicate(text=texto, voice=voz_id, rate=taxa)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        await comunicador.save(temp_path)
        with open(temp_path, "rb") as f:
            audio_data = f.read()
        return audio_data
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

HTML_PAGE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NOVA Voice Studio — Neural Voice Interface</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #0B0F17;
      --bg-surface: rgba(22, 30, 46, 0.7);
      --bg-card: rgba(30, 41, 59, 0.6);
      --bg-card-active: rgba(37, 99, 235, 0.15);
      --primary: #3B82F6;
      --primary-glow: rgba(59, 130, 246, 0.4);
      --accent: #10B981;
      --accent-glow: rgba(16, 185, 129, 0.3);
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
      --border: rgba(148, 163, 184, 0.12);
      --border-active: #3B82F6;
      --radius: 16px;
      --transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Outfit', -apple-system, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background-image: 
        radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%);
      background-attachment: fixed;
      padding: 32px 20px;
    }

    .container {
      max-width: 1180px;
      margin: 0 auto;
      width: 100%;
    }

    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 36px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .brand-logo {
      width: 46px;
      height: 46px;
      background: linear-gradient(135deg, #3B82F6, #10B981);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      box-shadow: 0 0 24px var(--primary-glow);
    }

    .brand-title h1 {
      font-size: 24px;
      font-weight: 700;
      letter-spacing: -0.5px;
      background: linear-gradient(to right, #FFFFFF, #94A3B8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-title p {
      font-size: 13px;
      color: var(--text-muted);
      font-weight: 400;
    }

    .status-badge {
      display: flex;
      align-items: center;
      gap: 10px;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      padding: 8px 16px;
      border-radius: 999px;
      backdrop-filter: blur(12px);
      font-size: 13px;
      font-weight: 500;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      background-color: var(--accent);
      border-radius: 50%;
      box-shadow: 0 0 10px var(--accent);
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.85); }
    }

    /* Live Studio Control Box */
    .studio-controls {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      margin-bottom: 36px;
      backdrop-filter: blur(16px);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .controls-grid {
      display: grid;
      grid-template-columns: 1fr 280px auto;
      gap: 20px;
      align-items: flex-end;
    }

    @media (max-width: 850px) {
      .controls-grid {
        grid-template-columns: 1fr;
      }
    }

    .input-group label {
      display: block;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .custom-input {
      width: 100%;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 14px 18px;
      border-radius: 12px;
      font-size: 15px;
      font-family: inherit;
      outline: none;
      transition: var(--transition);
    }

    .custom-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-glow);
    }

    .speed-control {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
    }

    .slider-val {
      color: var(--primary);
      font-family: 'JetBrains Mono', monospace;
    }

    input[type="range"] {
      -webkit-appearance: none;
      width: 100%;
      height: 6px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 4px;
      outline: none;
    }

    input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--primary);
      cursor: pointer;
      box-shadow: 0 0 10px var(--primary-glow);
      transition: transform 0.1s;
    }

    input[type="range"]::-webkit-slider-thumb:hover {
      transform: scale(1.2);
    }

    .btn-test-all {
      background: linear-gradient(135deg, #3B82F6, #2563EB);
      color: white;
      border: none;
      padding: 14px 24px;
      border-radius: 12px;
      font-size: 15px;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition);
      box-shadow: 0 4px 16px var(--primary-glow);
      white-space: nowrap;
    }

    .btn-test-all:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    }

    /* Voice Grid */
    .section-title {
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-main);
    }

    .voice-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }

    .voice-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backdrop-filter: blur(12px);
      transition: var(--transition);
      position: relative;
      overflow: hidden;
    }

    .voice-card:hover {
      border-color: rgba(148, 163, 184, 0.3);
      transform: translateY(-4px);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4);
    }

    .voice-card.active {
      background: var(--bg-card-active);
      border-color: var(--border-active);
      box-shadow: 0 0 30px rgba(59, 130, 246, 0.25);
    }

    .active-badge {
      position: absolute;
      top: 16px;
      right: 16px;
      background: var(--primary);
      color: white;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      box-shadow: 0 0 12px var(--primary-glow);
      display: none;
    }

    .voice-card.active .active-badge {
      display: block;
    }

    .card-header {
      display: flex;
      align-items: flex-start;
      gap: 14px;
      margin-bottom: 12px;
    }

    .voice-icon {
      font-size: 32px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 12px;
      width: 52px;
      height: 52px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .voice-info h3 {
      font-size: 18px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 2px;
    }

    .voice-tag {
      display: inline-block;
      font-size: 12px;
      font-weight: 600;
      color: var(--primary);
      background: rgba(59, 130, 246, 0.12);
      padding: 2px 8px;
      border-radius: 6px;
      margin-bottom: 6px;
    }

    .voice-desc {
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 18px;
    }

    .voice-id-code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11.5px;
      color: #64748B;
      background: rgba(0, 0, 0, 0.3);
      padding: 6px 10px;
      border-radius: 8px;
      margin-bottom: 18px;
      display: block;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .card-actions {
      display: flex;
      gap: 10px;
      margin-top: auto;
    }

    .btn-action {
      flex: 1;
      padding: 10px 14px;
      border-radius: 10px;
      font-size: 13.5px;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: var(--transition);
      border: 1px solid transparent;
    }

    .btn-play {
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-main);
      border-color: rgba(255, 255, 255, 0.1);
    }

    .btn-play:hover {
      background: rgba(255, 255, 255, 0.16);
      transform: translateY(-1px);
    }

    .btn-play.playing {
      background: var(--accent);
      color: white;
      box-shadow: 0 0 16px var(--accent-glow);
    }

    .btn-set-default {
      background: rgba(59, 130, 246, 0.12);
      color: var(--primary);
      border-color: rgba(59, 130, 246, 0.3);
    }

    .btn-set-default:hover {
      background: var(--primary);
      color: white;
      box-shadow: 0 0 16px var(--primary-glow);
    }

    .voice-card.active .btn-set-default {
      background: rgba(16, 185, 129, 0.15);
      color: var(--accent);
      border-color: rgba(16, 185, 129, 0.4);
      pointer-events: none;
    }

    /* Toast Notification */
    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid var(--accent);
      color: var(--text-main);
      padding: 14px 22px;
      border-radius: 12px;
      font-size: 14px;
      font-weight: 600;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      gap: 10px;
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      z-index: 1000;
    }

    .toast.show {
      transform: translateY(0);
      opacity: 1;
    }

    footer {
      margin-top: auto;
      text-align: center;
      padding: 24px 0;
      border-top: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 13px;
    }
  </style>
</head>
<body>

  <div class="container">
    
    <!-- Top Header -->
    <header>
      <div class="brand">
        <div class="brand-logo">🎙️</div>
        <div class="brand-title">
          <h1>NOVA Voice Studio</h1>
          <p>Neural Voice Interface & Acoustic Tuning • Ecossistema NOVA</p>
        </div>
      </div>
      <div class="status-badge" id="activeStatusBadge">
        <div class="status-dot"></div>
        <span>Voz Ativa: <strong id="activeVoiceNameDisplay">Antônio</strong></span>
      </div>
    </header>

    <!-- Studio Interactive Controls -->
    <section class="studio-controls">
      <div class="controls-grid">
        <div class="input-group">
          <label for="customTextInput">💬 Frase Customizada para Teste</label>
          <input type="text" id="customTextInput" class="custom-input" placeholder="Digite qualquer texto para o NOVA falar em tempo real..." value="Olá, Fábio! Todos os módulos do ecossistema NOVA estão operando com 100% de estabilidade.">
        </div>

        <div class="speed-control">
          <div class="slider-header">
            <label>⚡ Velocidade da Fala</label>
            <span class="slider-val" id="speedDisplay">+0%</span>
          </div>
          <input type="range" id="speedSlider" min="-50" max="50" value="0" step="5">
        </div>

        <button class="btn-test-all" id="btnTestActiveVoice">
          <span>▶️ Testar Frase</span>
        </button>
      </div>
    </section>

    <!-- Voice Cards Grid -->
    <div class="section-title">
      <span>🎭 Catálogo de Vozes Neurais Disponíveis</span>
    </div>

    <div class="voice-grid" id="voiceGridContainer">
      <!-- Cards serão injetados dinamicamente via JS -->
    </div>

    <footer>
      Ecossistema NOVA • Java 21 • Spring Boot 3.3 • Spring AI MCP • edge-tts • macOS
    </footer>

  </div>

  <div class="toast" id="toastNotification">
    <span>✅ Configuração salva com sucesso!</span>
  </div>

  <audio id="audioPlayer"></audio>

  <script>
    const VOZES = __VOZES_JSON__;
    let configAtual = __CONFIG_JSON__;
    const audioPlayer = document.getElementById('audioPlayer');

    function renderGrid() {
      const container = document.getElementById('voiceGridContainer');
      container.innerHTML = '';

      VOZES.forEach(voz => {
        const isActive = voz.id === configAtual.voz_padrao;
        const card = document.createElement('div');
        card.className = `voice-card ${isActive ? 'active' : ''}`;
        card.id = `card-${voz.id}`;

        card.innerHTML = `
          <div class="active-badge">⭐ Ativa</div>
          <div>
            <div class="card-header">
              <div class="voice-icon">${voz.icone}</div>
              <div class="voice-info">
                <h3>${voz.nome}</h3>
                <span class="voice-tag">${voz.tag}</span>
              </div>
            </div>
            <p class="voice-desc">${voz.descricao}</p>
            <code class="voice-id-code">${voz.id}</code>
          </div>

          <div class="card-actions">
            <button class="btn-action btn-play" id="btn-play-${voz.id}" onclick="ouvirDemonstracao('${voz.id}')">
              <span>▶️ Ouvir</span>
            </button>
            <button class="btn-action btn-set-default" onclick="definirComoPadrao('${voz.id}', '${voz.nome}')">
              <span>${isActive ? '✓ Padrão' : '⭐ Definir'}</span>
            </button>
          </div>
        `;
        container.appendChild(card);
      });

      atualizarBadgeAtivo();
    }

    function atualizarBadgeAtivo() {
      const vozEncontrada = VOZES.find(v => v.id === configAtual.voz_padrao);
      const nome = vozEncontrada ? vozEncontrada.nome : configAtual.voz_padrao;
      document.getElementById('activeVoiceNameDisplay').innerText = nome;
      
      const speedVal = parseInt(configAtual.velocidade || "+0");
      document.getElementById('speedSlider').value = isNaN(speedVal) ? 0 : speedVal;
      document.getElementById('speedDisplay').innerText = (speedVal >= 0 ? '+' : '') + speedVal + '%';
    }

    // Slider de velocidade
    const speedSlider = document.getElementById('speedSlider');
    const speedDisplay = document.getElementById('speedDisplay');

    speedSlider.addEventListener('input', (e) => {
      const val = parseInt(e.target.value);
      const strVal = (val >= 0 ? '+' : '') + val + '%';
      speedDisplay.innerText = strVal;
      configAtual.velocidade = strVal;
    });

    speedSlider.addEventListener('change', () => {
      salvarConfiguracoesBackend();
    });

    async function ouvirDemonstracao(vozId) {
      const customText = document.getElementById('customTextInput').value.trim();
      const vozObj = VOZES.find(v => v.id === vozId);
      const texto = customText || (vozObj ? vozObj.frase_demo : "Teste de voz do NOVA.");
      const taxa = configAtual.velocidade || "+0%";

      const playBtn = document.getElementById(`btn-play-${vozId}`);
      if (playBtn) playBtn.classList.add('playing');

      try {
        const res = await fetch('/api/synthesize', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ texto, voz: vozId, taxa })
        });

        if (!res.ok) throw new Error("Erro na síntese de áudio");

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        audioPlayer.src = url;
        audioPlayer.play();

        audioPlayer.onended = () => {
          if (playBtn) playBtn.classList.remove('playing');
        };
      } catch (err) {
        console.error(err);
        if (playBtn) playBtn.classList.remove('playing');
        showToast("⚠️ Falha ao reproduzir áudio.");
      }
    }

    // Botão testar voz ativa com a frase do input
    document.getElementById('btnTestActiveVoice').addEventListener('click', () => {
      ouvirDemonstracao(configAtual.voz_padrao);
    });

    async function definirComoPadrao(vozId, nome) {
      configAtual.voz_padrao = vozId;
      await salvarConfiguracoesBackend();
      renderGrid();
      showToast(`⭐ Voz padrão alterada para: ${nome}!`);
    }

    async function salvarConfiguracoesBackend() {
      try {
        await fetch('/api/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(configAtual)
        });
      } catch (err) {
        console.error("Erro ao salvar config:", err);
      }
    }

    function showToast(msg) {
      const toast = document.getElementById('toastNotification');
      toast.querySelector('span').innerText = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 3000);
    }

    // Inicialização
    renderGrid();
  </script>
</body>
</html>
"""

class VoiceStudioHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/" or parsed.path == "/index.html":
            config = carregar_config()
            page_content = HTML_PAGE.replace("__VOZES_JSON__", json.dumps(VOZES_CATALOGO, ensure_ascii=False))
            page_content = page_content.replace("__CONFIG_JSON__", json.dumps(config, ensure_ascii=False))

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(page_content.encode("utf-8"))

        elif parsed.path == "/api/config":
            config = carregar_config()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(config).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/config":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
                salvar_config(data)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "OK"}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

        elif parsed.path == "/api/synthesize":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
                texto = data.get("texto", "Teste de áudio do NOVA.")
                voz_id = data.get("voz", "pt-BR-AntonioNeural")
                taxa = data.get("taxa", "+0%")

                audio_bytes = asyncio.run(gerar_audio_bytes(texto, voz_id, taxa))

                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Content-Length", str(len(audio_bytes)))
                self.end_headers()
                self.wfile.write(audio_bytes)

            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suprime logs de requisições individuais para manter o terminal limpo
        pass

def iniciar_servidor():
    server = HTTPServer(('127.0.0.1', PORT), VoiceStudioHandler)
    url = f"http://localhost:{PORT}"
    print("=" * 65)
    print(f"🎙️ NOVA VOICE STUDIO INICIADO COM SUCESSO!")
    print(f"🌐 Acesse a interface visual em: {url}")
    print(f"Pressione Ctrl+C no terminal para encerrar o servidor.")
    print("=" * 65)

    # Abre o navegador padrão do usuário no Mac
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Voice Studio encerrado. Até logo!")
        server.server_close()

if __name__ == "__main__":
    iniciar_servidor()

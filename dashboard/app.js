/**
 * NOVA Control Center — Front-End Logic (Voice Assistant & Figma Dabang)
 * Integração com webkitSpeechRecognition, síntese Base64 e Chart.js.
 */

let chartEvolucao = null;
let chartCategorias = null;
let chartTargetReality = null;
let chartMatch = null;
let dadosGlobais = null;
let pitchTextoAtual = "";

// Voice Recognition & Audio Player
let recognition = null;
let isRecording = false;
let currentAudioPlayer = null;

document.addEventListener('DOMContentLoaded', () => {
  carregarDashboard();
  configurarBuscaGlobal();
  inicializarSpeechRecognition();
  carregarConfiguracaoVoz();
});

async function carregarDashboard() {
  try {
    const res = await fetch('/api/status');
    if (!res.ok) throw new Error("Falha ao carregar API /api/status");
    const data = await res.json();
    dadosGlobais = data;

    renderizarTopKPIs(data.financas, data.estudos);
    renderizarGraficoEvolucao(data.financas);
    renderizarGraficoCategorias(data.financas);
    renderizarGraficoTargetReality(data.financas);
    renderizarGraficoMatchCarreira(data.candidaturas);
    renderizarTabelaCandidaturas(data.candidaturas);

    if (window.lucide) {
      lucide.createIcons();
    }

  } catch (err) {
    console.error("Erro no dashboard:", err);
    showToast("⚠️ Conectado com cache local.");
    if (window.lucide) lucide.createIcons();
  }
}

function recarregarDashboard() {
  carregarDashboard();
  showToast("↻ Painel sincronizado com sucesso!");
}

/* ==========================================================================
   1. VOICE ASSISTANT (MICROFONE & SÍNTESE BASE64)
   ========================================================================== */

function inicializarSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    console.warn("SpeechRecognition não suportado neste navegador.");
    return;
  }

  recognition = new SpeechRecognition();
  recognition.lang = 'pt-BR';
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => {
    isRecording = true;
    atualizarEstadoVoz('listening', 'Ouvindo sua voz...');
    document.getElementById('btnMicToggle').classList.add('active');
    document.getElementById('btnMicLabel').innerText = 'Gravando...';
  };

  recognition.onresult = async (event) => {
    const transcricao = event.results[0][0].transcript;
    if (transcricao) {
      adicionarMensagemChat('user', transcricao);
      atualizarEstadoVoz('processing', 'Processando resposta...');
      await enviarComandoParaBackend(transcricao);
    }
  };

  recognition.onerror = (event) => {
    console.warn("Erro no reconhecimento de fala:", event.error);
    atualizarEstadoVoz('ready', 'Pronto para ouvir');
    document.getElementById('btnMicToggle').classList.remove('active');
    document.getElementById('btnMicLabel').innerText = 'Pressione para Falar';
    isRecording = false;
  };

  recognition.onend = () => {
    isRecording = false;
    document.getElementById('btnMicToggle').classList.remove('active');
    document.getElementById('btnMicLabel').innerText = 'Pressione para Falar';
  };
}

function toggleGravacaoVoz() {
  if (!recognition) {
    showToast("⚠️ Microfone não suportado no navegador. Digite no campo de texto.");
    return;
  }

  if (isRecording) {
    recognition.stop();
  } else {
    try {
      recognition.start();
    } catch (e) {
      console.warn("Reconhecimento já estava ativo ou ocupado:", e);
    }
  }
}

async function enviarTextoDigitado() {
  const input = document.getElementById('vaTextInput');
  const texto = input.value.trim();
  if (!texto) return;

  adicionarMensagemChat('user', texto);
  atualizarEstadoVoz('processing', 'Processando resposta...');
  input.value = '';

  await enviarComandoParaBackend(texto);
}

function executarPromptRapido(prompt) {
  document.getElementById('vaTextInput').value = prompt;
  enviarTextoDigitado();
}

async function enviarComandoParaBackend(comando) {
  const selectVoz = document.getElementById('selectVoiceModel');
  const vozEscolhida = selectVoz ? selectVoz.value : 'pt-BR-FranciscaNeural';

  try {
    const res = await fetch('/api/voice/interact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comando, voz: vozEscolhida })
    });

    if (!res.ok) throw new Error("Erro na resposta do servidor");
    const data = await res.json();

    // Adiciona resposta do assistente no diálogo
    adicionarMensagemChat('assistant', data.texto);

    // Reproduz o áudio retornado em Base64
    if (data.audio_base64) {
      reproduzirAudioBase64(data.audio_base64);
    } else {
      atualizarEstadoVoz('ready', 'Pronto para ouvir');
    }

  } catch (err) {
    console.error("Erro na interação de voz:", err);
    adicionarMensagemChat('assistant', "Desculpe, ocorreu uma instabilidade ao conectar com o serviço de voz.");
    atualizarEstadoVoz('ready', 'Pronto para ouvir');
  }
}

function reproduzirAudioBase64(base64Data) {
  if (currentAudioPlayer) {
    currentAudioPlayer.pause();
    currentAudioPlayer = null;
  }

  const audioSrc = "data:audio/mp3;base64," + base64Data;
  currentAudioPlayer = new Audio(audioSrc);

  currentAudioPlayer.onplay = () => {
    atualizarEstadoVoz('speaking', 'NOVA Falando...');
  };

  currentAudioPlayer.onended = () => {
    atualizarEstadoVoz('ready', 'Pronto para ouvir');
    currentAudioPlayer = null;
  };

  currentAudioPlayer.onerror = () => {
    console.error("Erro ao tocar áudio");
    atualizarEstadoVoz('ready', 'Pronto para ouvir');
  };

  currentAudioPlayer.play().catch(e => {
    console.warn("Autoplay bloqueado pelo navegador:", e);
    atualizarEstadoVoz('ready', 'Pronto para ouvir');
  });
}

function atualizarEstadoVoz(estado, textoStatus) {
  const orb = document.getElementById('orbAppleSphere');
  const stateDot = document.getElementById('vaStateDot');
  const stateText = document.getElementById('vaStateText');

  stateText.innerText = textoStatus;

  orb.className = 'orb-apple-sphere';
  stateDot.className = 'state-dot';

  if (estado === 'listening') {
    orb.classList.add('listening');
    stateDot.classList.add('listening');
  } else if (estado === 'speaking') {
    orb.classList.add('speaking');
    stateDot.classList.add('speaking');
  }
}

function adicionarMensagemChat(remetente, texto) {
  const dialogBox = document.getElementById('vaDialogBox');
  const msg = document.createElement('div');
  msg.className = `va-message ${remetente}`;

  const avatar = remetente === 'user' ? '👤' : '🌌';
  const author = remetente === 'user' ? 'Você' : 'NOVA';

  msg.innerHTML = `
    <div class="msg-avatar">${avatar}</div>
    <div class="msg-content">
      <span class="msg-author">${author}</span>
      <p>${texto}</p>
    </div>
  `;

  dialogBox.appendChild(msg);
  dialogBox.scrollTop = dialogBox.scrollHeight;
}

async function trocarVozAtiva(novaVoz) {
  try {
    await fetch('/api/voice/set-voice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ voz: novaVoz })
    });

    const nomeFormatado = novaVoz.replace("pt-BR-", "").replace("en-US-", "").replace("Neural", "");
    document.getElementById('headerVoiceName').innerText = `Voz: ${nomeFormatado}`;
    document.getElementById('sidebarVoicePill').innerText = nomeFormatado;
    showToast(`🎙️ Voz padrão alterada para: ${nomeFormatado}`);

  } catch (err) {
    console.error("Erro ao alterar voz:", err);
  }
}

async function carregarConfiguracaoVoz() {
  try {
    const res = await fetch('/api/voice/config');
    if (!res.ok) return;
    const cfg = await res.json();
    const vozPadrao = cfg.voz_padrao || 'pt-BR-FranciscaNeural';

    const select = document.getElementById('selectVoiceModel');
    if (select) select.value = vozPadrao;

    const nome = vozPadrao.replace("pt-BR-", "").replace("en-US-", "").replace("Neural", "");
    document.getElementById('headerVoiceName').innerText = `Voz: ${nome}`;
    document.getElementById('sidebarVoicePill').innerText = nome;

  } catch (e) {
    // Silencioso
  }
}

function focarNoAssistenteVoz() {
  const section = document.getElementById('voice-assistant-section');
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' });
    document.getElementById('vaTextInput').focus();
  }
}

/* ==========================================================================
   2. TOP 4 SUMMARY CARDS
   ========================================================================== */

function renderizarTopKPIs(fin, estudos) {
  const fmtBRL = (val) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);

  if (fin) {
    document.getElementById('kpiSaldo').innerText = (fin.saldo >= 0 ? '+ ' : '') + fmtBRL(fin.saldo);
    document.getElementById('kpiReceitas').innerText = fmtBRL(fin.totalReceitas);
    document.getElementById('kpiDespesas').innerText = fmtBRL(fin.totalGasto);
  }

  if (estudos) {
    document.getElementById('kpiDio').innerText = `${estudos.progresso_percentual}% Concluído`;
    document.getElementById('kpiDioBar').style.width = `${estudos.progresso_percentual}%`;
  }
}

/* ==========================================================================
   3. GRÁFICO 1: EVOLUÇÃO FINANCEIRA
   ========================================================================== */

function renderizarGraficoEvolucao(fin) {
  const ctx = document.getElementById('chartEvolucaoFinanceira').getContext('2d');
  const semanas = ['Semana 1 (01-07)', 'Semana 2 (08-14)', 'Semana 3 (15-21)', 'Semana 4 (22-31)'];
  const receitas = [500.00, 500.00, 1200.00, 99.00];
  const despesas = [320.50, 412.10, 568.30, 408.87];

  if (chartEvolucao) chartEvolucao.destroy();

  chartEvolucao = new Chart(ctx, {
    type: 'line',
    data: {
      labels: semanas,
      datasets: [
        {
          label: 'Receitas (R$)',
          data: receitas,
          borderColor: '#3B82F6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#3B82F6',
          pointRadius: 4,
          borderWidth: 3
        },
        {
          label: 'Despesas (R$)',
          data: despesas,
          borderColor: '#F43F5E',
          backgroundColor: 'rgba(244, 63, 94, 0.08)',
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#F43F5E',
          pointRadius: 4,
          borderWidth: 3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          align: 'end',
          labels: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 12, weight: '600' }, usePointStyle: true }
        },
        tooltip: {
          backgroundColor: '#0F172A',
          titleColor: '#F8FAFC',
          bodyColor: '#94A3B8',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          padding: 10,
          callbacks: {
            label: (c) => ` ${c.dataset.label}: R$ ${c.parsed.y.toFixed(2)}`
          }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#64748B', font: { family: 'Plus Jakarta Sans', size: 11 } } },
        y: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748B', font: { family: 'JetBrains Mono', size: 11 }, callback: (v) => `R$ ${v}` }
        }
      }
    }
  });
}

/* ==========================================================================
   4. GRÁFICO 2: GASTOS POR CATEGORIA
   ========================================================================== */

function renderizarGraficoCategorias(fin) {
  const ctx = document.getElementById('chartGastosCategoria').getContext('2d');
  const categorias = fin && fin.totalPorCategoria ? fin.totalPorCategoria : {
    "Alimentação": 728.38,
    "Transporte": 151.87,
    "Compras": 318.52,
    "Transferências": 511.00
  };

  const labels = Object.keys(categorias);
  const valores = Object.values(categorias);
  const cores = ['#F43F5E', '#F59E0B', '#3B82F6', '#8B5CF6'];

  if (chartCategorias) chartCategorias.destroy();

  chartCategorias = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Gasto Total (R$)',
        data: valores,
        backgroundColor: cores,
        borderRadius: 8,
        barPercentage: 0.55
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#0F172A',
          titleColor: '#F8FAFC',
          bodyColor: '#94A3B8',
          callbacks: { label: (c) => ` R$ ${c.parsed.y.toFixed(2)}` }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 11 } } },
        y: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748B', font: { family: 'JetBrains Mono', size: 11 }, callback: (v) => `R$ ${v}` }
        }
      }
    }
  });
}

/* ==========================================================================
   5. GRÁFICO 3: TARGET VS REALITY
   ========================================================================== */

function renderizarGraficoTargetReality(fin) {
  const ctx = document.getElementById('chartTargetVsReality').getContext('2d');
  if (chartTargetReality) chartTargetReality.destroy();

  chartTargetReality = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Meta Teto', 'Gasto Real', 'Economia Gerada'],
      datasets: [{
        label: 'Valor (R$)',
        data: [2000.00, 1709.77, 589.23],
        backgroundColor: ['rgba(59, 130, 246, 0.6)', '#F43F5E', '#10B981'],
        borderRadius: 8,
        barPercentage: 0.5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#0F172A',
          callbacks: { label: (c) => ` R$ ${c.parsed.y.toFixed(2)}` }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 11 } } },
        y: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748B', font: { family: 'JetBrains Mono', size: 11 }, callback: (v) => `R$ ${v}` }
        }
      }
    }
  });
}

/* ==========================================================================
   6. GRÁFICO 4: MATCH DE CARREIRA
   ========================================================================== */

function renderizarGraficoMatchCarreira(jobs) {
  const ctx = document.getElementById('chartMatchCarreira').getContext('2d');
  const nomes = (jobs || []).map(j => j.nome);
  const scores = (jobs || []).map(j => j.match);

  if (chartMatch) chartMatch.destroy();

  chartMatch = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: nomes,
      datasets: [{
        axis: 'y',
        label: 'Aderência Técnica (%)',
        data: scores,
        backgroundColor: ['#10B981', '#3B82F6', '#60A5FA', '#F59E0B'],
        borderRadius: 6,
        barPercentage: 0.5
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#0F172A',
          callbacks: { label: (c) => ` Match: ${c.parsed.x}%` }
        }
      },
      scales: {
        x: {
          min: 0,
          max: 100,
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748B', font: { family: 'JetBrains Mono', size: 11 }, callback: (v) => `${v}%` }
        },
        y: { grid: { display: false }, ticks: { color: '#F1F5F9', font: { family: 'Plus Jakarta Sans', size: 12, weight: '700' } } }
      }
    }
  });
}

/* ==========================================================================
   7. TABELA DE CANDIDATURAS 360°
   ========================================================================== */

function renderizarTabelaCandidaturas(jobs) {
  const tbody = document.getElementById('candidatesTableBody');
  if (!tbody || !jobs) return;

  tbody.innerHTML = '';

  jobs.forEach((job, idx) => {
    const tr = document.createElement('tr');

    let badgeClass = 'high';
    if (job.match < 75) badgeClass = 'eval';
    else if (job.match < 90) badgeClass = 'mid';

    tr.innerHTML = `
      <td style="color: #64748B; font-weight: 700; font-family: 'JetBrains Mono', monospace;">0${idx + 1}</td>
      <td>
        <div class="company-cell">
          <div class="company-avatar-box">${job.nome.substring(0, 2).toUpperCase()}</div>
          <div class="company-title-wrap">
            <strong>${job.nome}</strong>
            <span>${job.modelo}</span>
          </div>
        </div>
      </td>
      <td>
        <strong style="color: #F8FAFC; display: block;">${job.cargo}</strong>
        <span style="color: #64748B; font-size: 11.5px;"><i data-lucide="map-pin" style="width: 12px; height: 12px; vertical-align: middle;"></i> ${job.local}</span>
      </td>
      <td>
        <div class="match-bar-cell">
          <span class="match-pct-badge ${badgeClass}">${job.match}%</span>
        </div>
      </td>
      <td>
        <span class="table-salary-tag">${job.salario_min} - ${job.salario_max}</span>
      </td>
      <td>
        <div class="action-buttons-flex">
          <a href="/download${job.cv_pdf}" target="_blank" class="btn-tbl-action" title="Baixar Currículo PDF">
            <i data-lucide="file-text"></i>
            <span>CV PDF</span>
          </a>
          <a href="/download${job.cover_docx}" target="_blank" class="btn-tbl-action" title="Baixar Cover Letter DOCX">
            <i data-lucide="file-code"></i>
            <span>DOCX</span>
          </a>
          <a href="/download${job.relatorio_pdf}" target="_blank" class="btn-tbl-action" title="Baixar Relatório Visual Match">
            <i data-lucide="bar-chart-2"></i>
            <span>Relatório</span>
          </a>
        </div>
      </td>
      <td>
        <button class="btn-tbl-action btn-tbl-pitch" onclick="abrirModalPitch('${job.id}')">
          <i data-lucide="message-square"></i>
          <span>Copiar Pitch</span>
        </button>
      </td>
    `;

    tbody.appendChild(tr);
  });

  if (window.lucide) {
    lucide.createIcons();
  }
}

/* ==========================================================================
   8. MODAL & TOAST & BUSCA
   ========================================================================== */

function abrirModalPitch(jobId) {
  const job = (dadosGlobais.candidaturas || []).find(j => j.id === jobId);
  if (!job) return;

  pitchTextoAtual = job.pitch_texto || "Pitch não encontrado.";
  document.getElementById('modalCompanyHeader').innerText = `Pitch LinkedIn — ${job.nome}`;
  document.getElementById('modalCompanySub').innerText = `Roteiro para ${job.cargo} (${job.local})`;
  document.getElementById('modalPitchBody').innerText = pitchTextoAtual;

  document.getElementById('pitchModal').classList.add('show');
}

function fecharModalPitch() {
  document.getElementById('pitchModal').classList.remove('show');
}

function copiarPitchClipboard() {
  if (!pitchTextoAtual) return;
  navigator.clipboard.writeText(pitchTextoAtual).then(() => {
    showToast("📋 Pitch copiado para a área de transferência!");
    fecharModalPitch();
  }).catch(() => {
    showToast("⚠️ Falha ao copiar.");
  });
}

function selecionarMenu(elem) {
  document.querySelectorAll('.menu-link').forEach(l => l.classList.remove('active'));
  elem.classList.add('active');
}

function showToast(msg) {
  const toast = document.getElementById('toastBox');
  document.getElementById('toastText').innerText = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3500);
}

function configurarBuscaGlobal() {
  const searchInput = document.getElementById('globalSearchInput');
  searchInput.addEventListener('keyup', (e) => {
    const termo = e.target.value.toLowerCase().trim();
    if (!termo) {
      renderizarTabelaCandidaturas(dadosGlobais.candidaturas);
      return;
    }
    const filtrados = (dadosGlobais.candidaturas || []).filter(j => 
      j.nome.toLowerCase().includes(termo) || 
      j.cargo.toLowerCase().includes(termo) ||
      j.local.toLowerCase().includes(termo)
    );
    renderizarTabelaCandidaturas(filtrados);
  });
}

window.addEventListener('click', (e) => {
  const modal = document.getElementById('pitchModal');
  if (e.target === modal) fecharModalPitch();
});

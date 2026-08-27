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

// Voice Recognition & Audio Player & Living Shader Engine
let recognition = null;
let isRecording = false;
let currentAudioPlayer = null;
let estadoAtualDashboard = 'normal';
let novaLivingShaderEngine = null;

document.addEventListener('DOMContentLoaded', () => {
  inicializarTemaM3();
  executarSplash3D();

  // Inicializa o Motor de Shader Vivo da NOVA IA Voice
  try {
    novaLivingShaderEngine = new NovaLivingShaderEngine();
  } catch (err) {
    console.warn("Living Shader Engine init warning:", err);
  }

  const urlParams = new URLSearchParams(window.location.search);
  const estadoUrl = urlParams.get('state');

  carregarDashboard().then(() => {
    if (estadoUrl && ['loading', 'empty', 'error', 'normal'].includes(estadoUrl)) {
      alternarEstadoDashboard(estadoUrl);
    }
  });

  configurarBuscaGlobal();
  inicializarSpeechRecognition();
  carregarConfiguracaoVoz();

  if (window.location.hash.includes('voice-studio') || new URLSearchParams(window.location.search).get('view') === 'voice-studio') {
    navegarParaSecao('voice-studio');
  }
});

/* ==========================================================================
   SPLASH SCREEN 3D (STORYBOARD ~2.2s COM SESSIONSTORAGE E A11Y)
   ========================================================================== */

function executarSplash3D() {
  const splash = document.getElementById('nova3dSplashScreen');
  if (!splash) return;

  // Requisito 2: prefers-reduced-motion
  const prefereReducaoMovimento = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const tempoExibicaoMs = prefereReducaoMovimento ? 400 : 2200;

  setTimeout(() => {
    splash.classList.add('splash-hidden');
    sessionStorage.setItem('nova_splash_shown', 'true');
    setTimeout(() => {
      if (splash && splash.parentNode) {
        splash.parentNode.removeChild(splash);
      }
    }, 500);
  }, tempoExibicaoMs);
}

/* ==========================================================================
   MATERIAL DESIGN 3 THEME SYSTEM (LIGHT / DARK)
   ========================================================================== */

function inicializarTemaM3() {
  const urlParams = new URLSearchParams(window.location.search);
  const themeParam = urlParams.get('theme');
  const salvo = localStorage.getItem('nova-theme');
  let temaInicial = 'dark';

  if (themeParam && ['light', 'dark'].includes(themeParam)) {
    temaInicial = themeParam;
  } else if (salvo) {
    temaInicial = salvo;
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
    temaInicial = 'light';
  }
  document.documentElement.setAttribute('data-theme', temaInicial);
  document.body.setAttribute('data-theme', temaInicial);
}

function alternarTemaM3() {
  const temaAtual = document.documentElement.getAttribute('data-theme') || 'dark';
  const novoTema = temaAtual === 'dark' ? 'light' : 'dark';

  document.documentElement.setAttribute('data-theme', novoTema);
  document.body.setAttribute('data-theme', novoTema);
  localStorage.setItem('nova-theme', novoTema);

  if (dadosGlobais) {
    renderizarDadosNormal(dadosGlobais);
  }

  if (window.lucide) lucide.createIcons();
  showToast(`☀️ Tema alterado para: ${novoTema === 'dark' ? 'Modo Escuro (M3)' : 'Modo Claro (M3)'}`);
}

function obterTokensM3() {
  const isLight = document.documentElement.getAttribute('data-theme') === 'light';
  return {
    isLight,
    primary: isLight ? '#4A6FA5' : '#A9C7FF',
    primaryContainer: isLight ? '#D9E3F5' : '#2C4A7C',
    onPrimaryContainer: isLight ? '#0F2C4E' : '#D9E3F5',
    secondary: isLight ? '#5B8A72' : '#9FD3B3',
    secondaryContainer: isLight ? '#D9EFE0' : '#2C4F3B',
    onSecondaryContainer: isLight ? '#0F2E1C' : '#D9EFE0',
    tertiary: isLight ? '#8A6D1A' : '#E4C46E',
    tertiaryContainer: isLight ? '#F5E7C4' : '#5C4900',
    onTertiaryContainer: isLight ? '#3D2F00' : '#F5E7C4',
    error: isLight ? '#B3261E' : '#F2B8B5',
    errorContainer: isLight ? '#F9DEDC' : '#8C1D18',
    surface: isLight ? '#FFFFFF' : '#1B1C22',
    onSurface: isLight ? '#1B1C1E' : '#E3E2E6',
    onSurfaceVariant: isLight ? '#45464F' : '#C6C6D0',
    outline: isLight ? '#767680' : '#909099',
    gridLines: isLight ? 'rgba(0, 0, 0, 0.07)' : 'rgba(255, 255, 255, 0.07)',
    tooltipBg: isLight ? '#1B1C1E' : '#121317',
    tooltipText: isLight ? '#FBFBFE' : '#E3E2E6'
  };
}

function ocultarSplashScreen() {
  const splash = document.getElementById('novaSplashScreen');
  if (splash) {
    setTimeout(() => {
      splash.classList.add('hidden');
    }, 450);
  }
}

async function carregarDashboard() {
  try {
    const res = await fetch('/api/status');
    if (!res.ok) throw new Error("Falha ao carregar API /api/status");
    const data = await res.json();
    dadosGlobais = data;

    renderizarDadosNormal(data);
    ocultarSplashScreen();

  } catch (err) {
    console.error("Erro no dashboard:", err);
    ocultarSplashScreen();
    renderizarEstadoError();
    showToast("⚠️ Conectado em modo offline com dados seguros.");
    if (window.lucide) lucide.createIcons();
  }
}

function recarregarDashboard() {
  alternarEstadoDashboard('normal');
  showToast("↻ Painel sincronizado com sucesso!");
}

/* ==========================================================================
   CONTROLE DE ESTADOS DO DASHBOARD (NORMAL, LOADING, EMPTY, ERROR)
   ========================================================================== */

function alternarEstadoDashboard(estado) {
  estadoAtualDashboard = estado;
  const select = document.getElementById('selectDashboardState');
  if (select && select.value !== estado) select.value = estado;

  if (estado === 'loading') {
    renderizarEstadoLoading();
  } else if (estado === 'empty') {
    renderizarEstadoEmpty();
  } else if (estado === 'error') {
    renderizarEstadoError();
  } else {
    if (dadosGlobais) {
      renderizarDadosNormal(dadosGlobais);
    } else {
      carregarDashboard();
    }
  }

  if (window.lucide) lucide.createIcons();
  showToast(`Visualizando Estado: ${estado.toUpperCase()}`);
}

function renderizarDadosNormal(data) {
  renderizarTopKPIs(data.financas, data.estudos);
  renderizarProjecaoFinanceira(data.projecao || data.financas);
  renderizarCaixinhas(data.caixinhas);
  renderizarGraficoEvolucao(data.financas);
  renderizarGraficoCategorias(data.financas);
  renderizarGraficoTargetReality(data.financas);
  renderizarGraficoMatchCarreira(data.candidaturas);
  renderizarTabelaCandidaturas(data.candidaturas);
  if (window.lucide) lucide.createIcons();
}

function renderizarCaixinhas(caixinhasData) {
  if (!caixinhasData) return;
  const patTotalEl = document.getElementById('kpiPatrimonioTotal');
  const resEl = document.getElementById('valReservaEmergencia');
  const casalEl = document.getElementById('valFundoCasal');
  const contaEl = document.getElementById('valSaldoConta');

  if (patTotalEl) {
    patTotalEl.textContent = `Patrimônio: R$ ${Number(caixinhasData.patrimonioLiquidoTotal || 607500.00).toFixed(2).replace('.', ',')}`;
  }
  if (contaEl) {
    contaEl.textContent = `R$ ${Number(caixinhasData.saldoContaCorrente || 107500.00).toFixed(2).replace('.', ',')}`;
  }

  if (caixinhasData.caixinhas && Array.isArray(caixinhasData.caixinhas)) {
    caixinhasData.caixinhas.forEach(c => {
      const nome = (c.nome || '').toLowerCase();
      if (nome.includes('reserva') || c.tipo === 'RESERVA_EMERGENCIA') {
        if (resEl) resEl.textContent = `R$ ${Number(c.saldo || 350000.00).toFixed(2).replace('.', ',')}`;
      } else if (nome.includes('casal') || nome.includes('expansão') || c.tipo === 'FUNDO_CASAL') {
        if (casalEl) casalEl.textContent = `R$ ${Number(c.saldo || 150000.00).toFixed(2).replace('.', ',')}`;
      }
    });
  }
}

function renderizarProjecaoFinanceira(proj) {
  if (!proj) return;
  const burnEl = document.getElementById('projBurnRate');
  const diasEl = document.getElementById('projDiasInfo');
  const gastoAdicEl = document.getElementById('projGastoAdicional');
  const gastoTotEl = document.getElementById('projGastoTotal');
  const saldoFinEl = document.getElementById('projSaldoFinal');
  const statusBadge = document.getElementById('projecaoStatusBadge');
  const recTxt = document.getElementById('projRecomendacaoTxt');

  if (burnEl) burnEl.textContent = `R$ ${Number(proj.burnRateDiario || 1574.07).toFixed(2).replace('.', ',')} / dia`;
  if (diasEl) diasEl.textContent = `${proj.diasDecorridos || 27} dias decorridos • ${proj.diasRestantes || 4} restantes`;
  if (gastoAdicEl) gastoAdicEl.textContent = `R$ ${Number(proj.gastoAdicionalProjetado || 6296.28).toFixed(2).replace('.', ',')}`;
  if (gastoTotEl) gastoTotEl.textContent = `R$ ${Number(proj.gastoTotalProjetado || 48796.28).toFixed(2).replace('.', ',')}`;
  
  if (saldoFinEl) {
    const val = Number(proj.saldoFinalProjetado || 101203.72);
    saldoFinEl.textContent = `${val >= 0 ? '+ ' : '- '}R$ ${Math.abs(val).toFixed(2).replace('.', ',')}`;
    saldoFinEl.className = `p-metric-val ${val >= 0 ? 'positive' : 'negative'}`;
  }

  if (statusBadge) {
    if (proj.statusOrcamentario === 'CRITICO') {
      statusBadge.innerHTML = '<span class="md3-badge md3-badge--error">CRÍTICO (DÉFICIT)</span>';
    } else if (proj.statusOrcamentario === 'ALERTA') {
      statusBadge.innerHTML = '<span class="md3-badge md3-badge--warning">ALERTA (MARGEM BAIXA)</span>';
    } else {
      statusBadge.innerHTML = '<span class="md3-badge md3-badge--success">SAUDÁVEL (SUPERÁVIT)</span>';
    }
  }

  if (recTxt && proj.recomendacaoEstrategica) {
    recTxt.textContent = proj.recomendacaoEstrategica;
  }
}

function garantirCanvas(idHolder, idCanvas) {
  let canvas = document.getElementById(idCanvas);
  if (!canvas) {
    const parent = document.getElementById(idHolder);
    if (parent) {
      parent.innerHTML = `<canvas id="${idCanvas}"></canvas>`;
      canvas = document.getElementById(idCanvas);
    }
  }
  return canvas;
}

function destruirTodosGraficos() {
  if (chartEvolucao) { chartEvolucao.destroy(); chartEvolucao = null; }
  if (chartCategorias) { chartCategorias.destroy(); chartCategorias = null; }
  if (chartTargetReality) { chartTargetReality.destroy(); chartTargetReality = null; }
  if (chartMatch) { chartMatch.destroy(); chartMatch = null; }
}

function renderizarEstadoLoading() {
  // 1. KPIs em modo Skeleton
  document.getElementById('kpiSaldo').innerHTML = '<span class="skeleton-shimmer skeleton-num"></span>';
  document.getElementById('kpiReceitas').innerHTML = '<span class="skeleton-shimmer skeleton-num"></span>';
  document.getElementById('kpiDespesas').innerHTML = '<span class="skeleton-shimmer skeleton-num"></span>';
  document.getElementById('kpiDio').innerHTML = '<span class="skeleton-shimmer skeleton-num" style="width:60%"></span>';

  // 2. Destrói gráficos e exibe skeleton shimmer boxes
  destruirTodosGraficos();

  const elEvolucao = document.getElementById('holderEvolucao');
  if (elEvolucao) {
    elEvolucao.innerHTML = `
      <div class="skeleton-chart-box">
        <div class="skeleton-chart-bars">
          <div class="skeleton-shimmer skeleton-bar-item" style="height: 40%"></div>
          <div class="skeleton-shimmer skeleton-bar-item" style="height: 70%"></div>
          <div class="skeleton-shimmer skeleton-bar-item" style="height: 100%"></div>
          <div class="skeleton-shimmer skeleton-bar-item" style="height: 55%"></div>
        </div>
        <span class="skeleton-shimmer skeleton-text" style="width: 40%"></span>
      </div>`;
  }

  const elCategorias = document.getElementById('holderCategorias');
  if (elCategorias) {
    elCategorias.innerHTML = `
      <div class="skeleton-chart-box">
        <div class="skeleton-shimmer skeleton-chart-circle"></div>
        <span class="skeleton-shimmer skeleton-text" style="width: 50%"></span>
      </div>`;
  }

  const elTarget = document.getElementById('holderTarget');
  if (elTarget) {
    elTarget.innerHTML = `
      <div class="skeleton-chart-box">
        <div class="skeleton-chart-bars">
          <div class="skeleton-shimmer skeleton-bar-item" style="height: 80%"></div>
          <div class="skeleton-shimmer skeleton-bar-item" style="height: 60%"></div>
        </div>
        <span class="skeleton-shimmer skeleton-text" style="width: 45%"></span>
      </div>`;
  }

  const elMatch = document.getElementById('holderMatch');
  if (elMatch) {
    elMatch.innerHTML = `
      <div class="skeleton-chart-box" style="padding: 20px;">
        <div class="skeleton-shimmer skeleton-bar-row"></div>
        <div class="skeleton-shimmer skeleton-bar-row" style="width: 85%"></div>
        <div class="skeleton-shimmer skeleton-bar-row" style="width: 75%"></div>
        <span class="skeleton-shimmer skeleton-text" style="width: 35%"></span>
      </div>`;
  }

  // 3. Tabela em modo Skeleton
  const tbody = document.getElementById('candidatesTableBody');
  if (tbody) {
    tbody.innerHTML = `
      <tr><td colspan="7"><div class="skeleton-shimmer skeleton-table-row"></div></td></tr>
      <tr><td colspan="7"><div class="skeleton-shimmer skeleton-table-row"></div></td></tr>
      <tr><td colspan="7"><div class="skeleton-shimmer skeleton-table-row"></div></td></tr>
    `;
  }
}

function renderizarEstadoEmpty() {
  destruirTodosGraficos();

  // KPIs Zerados
  document.getElementById('kpiSaldo').innerText = 'R$ 0,00';
  document.getElementById('kpiReceitas').innerText = 'R$ 0,00';
  document.getElementById('kpiDespesas').innerText = 'R$ 0,00';
  document.getElementById('kpiDio').innerText = '0% Concluído';
  document.getElementById('kpiDioBar').style.width = '0%';

  // Gráficos Vazios
  ['holderEvolucao', 'holderCategorias', 'holderTarget', 'holderMatch'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.innerHTML = `
        <div class="empty-state-card">
          <div class="empty-icon-circle"><i data-lucide="bar-chart-2"></i></div>
          <h4 class="empty-title">Sem movimentações no período</h4>
          <p class="empty-desc">Nenhum lançamento foi registrado para este filtro orçamentário.</p>
        </div>`;
    }
  });

  // Tabela Vazia Propositiva
  const tbody = document.getElementById('candidatesTableBody');
  if (tbody) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7">
          <div class="empty-state-card">
            <div class="empty-icon-circle"><i data-lucide="inbox"></i></div>
            <h4 class="empty-title">Nenhuma candidatura ativa no momento</h4>
            <p class="empty-desc">Você ainda não mapeou vagas para este ciclo. Que tal analisar uma nova oportunidade com o NOVA?</p>
            <button class="btn-empty-action" onclick="alternarEstadoDashboard('normal')">
              <i data-lucide="plus-circle"></i>
              <span>Carregar Candidaturas Ativas</span>
            </button>
          </div>
        </td>
      </tr>
    `;
  }
}

function renderizarEstadoError() {
  destruirTodosGraficos();

  // Mensagem amigável na voz do NOVA
  ['holderEvolucao', 'holderCategorias', 'holderTarget', 'holderMatch'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.innerHTML = `
        <div class="card-error-state">
          <div class="error-icon-box"><i data-lucide="wifi-off"></i></div>
          <h4 class="error-msg-title">Sincronização Temporariamente Indisponível</h4>
          <p class="error-msg-body">Não foi possível conectar ao banco H2 local neste momento. Seus dados estão seguros e o NOVA continuará tentando em segundo plano.</p>
          <button class="btn-retry-action" onclick="alternarEstadoDashboard('normal')">
            <i data-lucide="rotate-cw"></i>
            <span>Tentar Reconectar Agora</span>
          </button>
        </div>`;
    }
  });

  const tbody = document.getElementById('candidatesTableBody');
  if (tbody) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7">
          <div class="card-error-state">
            <div class="error-icon-box"><i data-lucide="alert-circle"></i></div>
            <h4 class="error-msg-title">Não foi possível carregar a esteira de vagas</h4>
            <p class="error-msg-body">O arquivo de candidaturas não respondeu. Clique abaixo para restabelecer a conexão com a base local.</p>
            <button class="btn-retry-action" onclick="alternarEstadoDashboard('normal')">
              <i data-lucide="rotate-cw"></i>
              <span>Reconectar Base de Vagas</span>
            </button>
          </div>
        </td>
      </tr>
    `;
  }
}

/* ==========================================================================
   1. NOVA LIVING SHADER ENGINE & AUDIO REACTIVE ORB
   ========================================================================== */

let audioCtx = null;
let analyserNode = null;
let audioSourceMap = new WeakMap();

class NovaLivingShaderEngine {
  constructor() {
    this.mainCanvas = document.getElementById('novaShaderOrbCanvas');
    this.miniCanvas = document.getElementById('novaMiniShaderCanvas');
    this.wrapper = document.getElementById('orbVisualWrapper');
    this.centerIcon = document.getElementById('orbCenterIcon');
    this.centerIconWrap = document.getElementById('orbCenterIconWrap');

    this.mainCtx = this.mainCanvas ? this.mainCanvas.getContext('2d') : null;
    this.miniCtx = this.miniCanvas ? this.miniCanvas.getContext('2d') : null;

    this.time = 0;
    this.state = 'idle'; // 'idle' | 'listening' | 'thinking' | 'speaking'
    this.audioEnergy = 0;
    this.targetEnergy = 0;
    this.audioFrequencies = new Uint8Array(16);
    this.analyser = null;

    // Pointer interaction
    this.pointer = { x: 0.5, y: 0.5, targetX: 0.5, targetY: 0.5, isHover: false };

    this.init();
  }

  init() {
    if (!this.mainCanvas || !this.mainCtx) return;

    // High DPI Support
    const dpr = window.devicePixelRatio || 1;
    this.width = 280;
    this.height = 280;
    this.mainCanvas.width = this.width * dpr;
    this.mainCanvas.height = this.height * dpr;
    this.mainCtx.scale(dpr, dpr);

    if (this.miniCanvas && this.miniCtx) {
      this.miniCanvas.width = 88 * dpr;
      this.miniCanvas.height = 88 * dpr;
      this.miniCtx.scale(dpr, dpr);
    }

    // Pointer tracking
    if (this.wrapper) {
      this.wrapper.addEventListener('pointermove', (e) => {
        const rect = this.wrapper.getBoundingClientRect();
        this.pointer.targetX = (e.clientX - rect.left) / rect.width;
        this.pointer.targetY = (e.clientY - rect.top) / rect.height;
        this.pointer.isHover = true;
      });

      this.wrapper.addEventListener('pointerleave', () => {
        this.pointer.targetX = 0.5;
        this.pointer.targetY = 0.5;
        this.pointer.isHover = false;
      });
    }

    this.animate();
  }

  setState(newState, label) {
    this.state = newState;
    if (this.wrapper) {
      this.wrapper.classList.remove('listening', 'speaking', 'thinking');
      if (newState === 'listening') this.wrapper.classList.add('listening');
      if (newState === 'speaking') this.wrapper.classList.add('speaking');
      if (newState === 'thinking') this.wrapper.classList.add('thinking');
    }

    // Center Icon Morph
    if (this.centerIcon) {
      if (newState === 'listening') {
        this.centerIcon.innerText = 'hearing';
      } else if (newState === 'thinking') {
        this.centerIcon.innerText = 'psychology';
      } else if (newState === 'speaking') {
        this.centerIcon.innerText = 'graphic_eq';
      } else {
        this.centerIcon.innerText = 'mic';
      }
    }
  }

  setAudioAnalyser(analyser) {
    this.analyser = analyser;
  }

  renderShader(ctx, w, h, isMini = false) {
    const cx = w / 2;
    const cy = h / 2;
    const radius = w * 0.46;

    // Smooth pointer lerp
    this.pointer.x += (this.pointer.targetX - this.pointer.x) * 0.12;
    this.pointer.y += (this.pointer.targetY - this.pointer.y) * 0.12;

    // Time speed based on state
    let speed = 0.024;
    if (this.state === 'listening') speed = 0.065;
    else if (this.state === 'thinking') speed = 0.085;
    else if (this.state === 'speaking') speed = 0.045 + (this.audioEnergy * 0.06);

    this.time += speed;

    // Clear
    ctx.clearRect(0, 0, w, h);

    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.clip();

    // 1. Deep Core Base Gradient
    const bgGrad = ctx.createRadialGradient(cx, cy, radius * 0.1, cx, cy, radius);
    if (this.state === 'listening') {
      bgGrad.addColorStop(0, '#7A1C20');
      bgGrad.addColorStop(0.6, '#3D0005');
      bgGrad.addColorStop(1, '#110507');
    } else {
      bgGrad.addColorStop(0, '#192C4E');
      bgGrad.addColorStop(0.5, '#0F1E36');
      bgGrad.addColorStop(1, '#080C14');
    }
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // 2. Harmonic Fluid Blobs with Chromatic Vortices
    const blobCount = 6;
    const px = (this.pointer.x - 0.5) * 35;
    const py = (this.pointer.y - 0.5) * 35;

    for (let i = 0; i < blobCount; i++) {
      const angle = (i / blobCount) * Math.PI * 2 + this.time * 0.8;
      const freqMultiplier = this.audioFrequencies[i % this.audioFrequencies.length] || 0;
      const energyMod = (this.audioEnergy * 25) + (freqMultiplier / 255 * 30);

      const distance = radius * 0.45 + Math.sin(this.time * 1.5 + i * 1.8) * (18 + energyMod);
      const bx = cx + Math.cos(angle) * distance + px * 0.6;
      const by = cy + Math.sin(angle) * distance + py * 0.6;
      const bRad = radius * (0.45 + Math.cos(this.time * 2.2 + i) * 0.12) + energyMod * 0.5;

      const grad = ctx.createRadialGradient(bx, by, 0, bx, by, Math.max(bRad, 5));

      // Chromatic Palette selection
      if (this.state === 'listening') {
        grad.addColorStop(0, 'rgba(255, 180, 171, 0.95)');
        grad.addColorStop(0.4, 'rgba(186, 26, 26, 0.8)');
        grad.addColorStop(0.8, 'rgba(147, 0, 10, 0.4)');
        grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
      } else {
        if (i % 4 === 0) {
          // Cobalt Primary
          grad.addColorStop(0, 'rgba(169, 199, 255, 0.95)');
          grad.addColorStop(0.4, 'rgba(74, 111, 165, 0.8)');
          grad.addColorStop(1, 'rgba(0, 48, 98, 0)');
        } else if (i % 4 === 1) {
          // Emerald Secondary
          grad.addColorStop(0, 'rgba(162, 244, 196, 0.95)');
          grad.addColorStop(0.4, 'rgba(91, 138, 114, 0.8)');
          grad.addColorStop(1, 'rgba(0, 57, 32, 0)');
        } else if (i % 4 === 2) {
          // Warm Gold Tertiary
          grad.addColorStop(0, 'rgba(255, 224, 139, 0.95)');
          grad.addColorStop(0.4, 'rgba(184, 134, 11, 0.75)');
          grad.addColorStop(1, 'rgba(92, 67, 0, 0)');
        } else {
          // Electric Violet
          grad.addColorStop(0, 'rgba(217, 70, 239, 0.9)');
          grad.addColorStop(0.4, 'rgba(142, 111, 165, 0.75)');
          grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        }
      }

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(bx, by, Math.max(bRad, 1), 0, Math.PI * 2);
      ctx.fill();
    }

    // 3. Central Luminous Core
    const coreGrad = ctx.createRadialGradient(cx + px * 0.3, cy + py * 0.3, 0, cx, cy, radius * 0.65);
    if (this.state === 'listening') {
      coreGrad.addColorStop(0, 'rgba(255, 255, 255, 0.95)');
      coreGrad.addColorStop(0.3, 'rgba(255, 180, 171, 0.7)');
      coreGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    } else {
      coreGrad.addColorStop(0, 'rgba(255, 255, 255, 0.95)');
      coreGrad.addColorStop(0.3, 'rgba(169, 199, 255, 0.65)');
      coreGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    }
    ctx.fillStyle = coreGrad;
    ctx.beginPath();
    ctx.arc(cx + px * 0.3, cy + py * 0.3, radius * 0.65, 0, Math.PI * 2);
    ctx.fill();

    // 4. Specular Glass Rim Refraction
    const rimGrad = ctx.createLinearGradient(0, 0, w, h);
    rimGrad.addColorStop(0, 'rgba(255, 255, 255, 0.65)');
    rimGrad.addColorStop(0.5, 'rgba(255, 255, 255, 0.05)');
    rimGrad.addColorStop(1, 'rgba(255, 255, 255, 0.35)');
    ctx.lineWidth = isMini ? 2 : 3.5;
    ctx.strokeStyle = rimGrad;
    ctx.stroke();

    ctx.restore();
  }

  animate() {
    // 1. Fetch audio FFT data if connected
    if (this.analyser) {
      const buffer = new Uint8Array(this.analyser.frequencyBinCount);
      this.analyser.getByteFrequencyData(buffer);
      this.audioFrequencies = buffer.slice(0, 16);

      let sum = 0;
      for (let i = 0; i < 16; i++) {
        sum += buffer[i];
      }
      this.targetEnergy = sum / (16 * 255); // 0.0 to 1.0
    } else {
      this.targetEnergy = 0;
    }

    this.audioEnergy += (this.targetEnergy - this.audioEnergy) * 0.25;

    // 2. Render Main Shader Canvas
    if (this.mainCtx) {
      this.renderShader(this.mainCtx, this.width, this.height, false);
    }

    // 3. Render Mini Squircle Canvas
    if (this.miniCtx) {
      this.renderShader(this.miniCtx, 88, 88, true);
    }

    requestAnimationFrame(() => this.animate());
  }
}

function conectarOrbAoAudio(audioElem) {
  try {
    if (!audioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) {
        audioCtx = new AudioContextClass();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    if (audioCtx && !analyserNode) {
      analyserNode = audioCtx.createAnalyser();
      analyserNode.fftSize = 128;
      analyserNode.smoothingTimeConstant = 0.75;
    }

    if (audioCtx && analyserNode && !audioSourceMap.has(audioElem)) {
      const source = audioCtx.createMediaElementSource(audioElem);
      source.connect(analyserNode);
      analyserNode.connect(audioCtx.destination);
      audioSourceMap.set(audioElem, source);
    }

    if (novaLivingShaderEngine && analyserNode) {
      novaLivingShaderEngine.setAudioAnalyser(analyserNode);
    }

  } catch (err) {
    console.warn("Web Audio API fallbacked para animação padrão:", err);
  }
}

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
      atualizarEstadoVoz('thinking', 'Processando resposta...');
      await enviarComandoParaBackend(transcricao);
    }
  };

  recognition.onerror = (event) => {
    console.warn("Erro no reconhecimento de fala:", event.error);
    atualizarEstadoVoz('idle', 'Pronto para ouvir');
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
    showToast("⚠️ Reconhecimento de voz não suportado neste navegador.");
    return;
  }

  if (isRecording) {
    recognition.stop();
  } else {
    try {
      recognition.start();
    } catch (e) {
      console.warn(e);
    }
  }
}

function enviarTextoDigitado() {
  const input = document.getElementById('vaTextInput');
  const texto = input.value.trim();
  if (!texto) return;

  adicionarMensagemChat('user', texto);
  atualizarEstadoVoz('thinking', 'Processando resposta...');
  input.value = '';
  enviarComandoParaBackend(texto);
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
      atualizarEstadoVoz('idle', 'Pronto para ouvir');
    }

  } catch (err) {
    console.error("Erro na interação de voz:", err);
    adicionarMensagemChat('assistant', "Desculpe, ocorreu uma instabilidade ao conectar com o serviço de voz.");
    atualizarEstadoVoz('idle', 'Pronto para ouvir');
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
    conectarOrbAoAudio(currentAudioPlayer);
  };

  currentAudioPlayer.onended = () => {
    atualizarEstadoVoz('idle', 'Pronto para ouvir');
    currentAudioPlayer = null;
  };

  currentAudioPlayer.onerror = () => {
    console.error("Erro ao tocar áudio");
    atualizarEstadoVoz('idle', 'Pronto para ouvir');
  };

  currentAudioPlayer.play().catch(e => {
    console.warn("Autoplay bloqueado pelo navegador:", e);
    atualizarEstadoVoz('idle', 'Pronto para ouvir');
  });
}

function atualizarEstadoVoz(estado, textoStatus) {
  const stateDot = document.getElementById('vaStateDot');
  const stateText = document.getElementById('vaStateText');

  if (stateText) stateText.innerText = textoStatus;
  if (stateDot) {
    stateDot.className = 'state-dot';
    if (estado === 'listening') stateDot.classList.add('listening');
    else if (estado === 'speaking') stateDot.classList.add('speaking');
  }

  if (novaLivingShaderEngine) {
    novaLivingShaderEngine.setState(estado, textoStatus);
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
   2. TOP 4 SUMMARY CARDS COM ANIMAÇÃO DE CONTAGEM
   ========================================================================== */

function animarContagem(elementId, valorFinal, prefixo = "", sufixo = "", duracaoMs = 850, casasDecimais = 2) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const inicio = 0;
  const startTime = performance.now();

  function step(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duracaoMs, 1);
    const easeOut = 1 - Math.pow(1 - progress, 3);
    const valorAtual = inicio + (valorFinal - inicio) * easeOut;

    const fmtValor = new Intl.NumberFormat('pt-BR', {
      minimumFractionDigits: casasDecimais,
      maximumFractionDigits: casasDecimais
    }).format(valorAtual);

    el.innerText = `${prefixo}${fmtValor}${sufixo}`;

    if (progress < 1) {
      requestAnimationFrame(step);
    } else {
      const finalFmt = new Intl.NumberFormat('pt-BR', {
        minimumFractionDigits: casasDecimais,
        maximumFractionDigits: casasDecimais
      }).format(valorFinal);
      el.innerText = `${prefixo}${finalFmt}${sufixo}`;
    }
  }

  requestAnimationFrame(step);
}

function renderizarTopKPIs(fin, estudos) {
  if (fin) {
    animarContagem('kpiSaldo', fin.saldo, fin.saldo >= 0 ? '+ R$ ' : '- R$ ', '', 850, 2);
    animarContagem('kpiReceitas', fin.totalReceitas, 'R$ ', '', 850, 2);
    animarContagem('kpiDespesas', fin.totalGasto, 'R$ ', '', 850, 2);
  }

  if (estudos) {
    animarContagem('kpiDio', estudos.progresso_percentual, '', '% Concluído', 850, 1);
    const bar = document.getElementById('kpiDioBar');
    if (bar) bar.style.width = `${estudos.progresso_percentual}%`;
  }
}

/* ==========================================================================
   3. GRÁFICO 1: EVOLUÇÃO FINANCEIRA (M3 TOKENS)
   ========================================================================== */

function renderizarGraficoEvolucao(fin) {
  const canvas = garantirCanvas('holderEvolucao', 'chartEvolucaoFinanceira');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const m3 = obterTokensM3();
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
          borderColor: m3.secondary,
          backgroundColor: m3.isLight ? 'rgba(91, 138, 114, 0.12)' : 'rgba(159, 211, 179, 0.15)',
          tension: 0.4,
          fill: true,
          pointBackgroundColor: m3.secondary,
          pointRadius: 4,
          borderWidth: 3
        },
        {
          label: 'Despesas (R$)',
          data: despesas,
          borderColor: m3.primary,
          backgroundColor: m3.isLight ? 'rgba(74, 111, 165, 0.08)' : 'rgba(169, 199, 255, 0.12)',
          tension: 0.4,
          fill: true,
          pointBackgroundColor: m3.primary,
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
          labels: { color: m3.onSurfaceVariant, font: { family: 'Plus Jakarta Sans', size: 12, weight: '600' }, usePointStyle: true }
        },
        tooltip: {
          backgroundColor: m3.tooltipBg,
          titleColor: m3.tooltipText,
          bodyColor: m3.tooltipText,
          borderColor: m3.outline,
          borderWidth: 1,
          padding: 10,
          callbacks: {
            label: (c) => ` ${c.dataset.label}: R$ ${c.parsed.y.toFixed(2)}`
          }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: m3.onSurfaceVariant, font: { family: 'Plus Jakarta Sans', size: 11 } } },
        y: {
          grid: { color: m3.gridLines },
          ticks: { color: m3.onSurfaceVariant, font: { family: 'JetBrains Mono', size: 11 }, callback: (v) => `R$ ${v}` }
        }
      }
    }
  });
}

/* ==========================================================================
   4. GRÁFICO 2: GASTOS POR CATEGORIA (M3 TOKENS)
   ========================================================================== */

function renderizarGraficoCategorias(fin) {
  const canvas = garantirCanvas('holderCategorias', 'chartGastosCategoria');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const m3 = obterTokensM3();
  const categorias = fin && fin.totalPorCategoria ? fin.totalPorCategoria : {
    "Alimentação": 728.38,
    "Transporte": 151.87,
    "Compras": 318.52,
    "Transferências": 511.00
  };

  const labels = Object.keys(categorias);
  const valores = Object.values(categorias);
  const cores = [m3.primary, m3.secondary, m3.tertiary, m3.isLight ? '#6B5B95' : '#C4B5FD'];

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
          backgroundColor: m3.tooltipBg,
          titleColor: m3.tooltipText,
          bodyColor: m3.tooltipText,
          callbacks: { label: (c) => ` R$ ${c.parsed.y.toFixed(2)}` }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: m3.onSurfaceVariant, font: { family: 'Plus Jakarta Sans', size: 11 } } },
        y: {
          grid: { color: m3.gridLines },
          ticks: { color: m3.onSurfaceVariant, font: { family: 'JetBrains Mono', size: 11 }, callback: (v) => `R$ ${v}` }
        }
      }
    }
  });
}

/* ==========================================================================
   5. GRÁFICO 3: TARGET VS REALITY (M3 TOKENS)
   ========================================================================== */

function renderizarGraficoTargetReality(fin) {
  const canvas = garantirCanvas('holderTarget', 'chartTargetVsReality');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const m3 = obterTokensM3();
  if (chartTargetReality) chartTargetReality.destroy();

  chartTargetReality = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Meta Teto', 'Gasto Real', 'Economia Gerada'],
      datasets: [{
        label: 'Valor (R$)',
        data: [2000.00, 1709.77, 589.23],
        backgroundColor: [m3.primary, m3.error, m3.secondary],
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
          backgroundColor: m3.tooltipBg,
          titleColor: m3.tooltipText,
          bodyColor: m3.tooltipText,
          callbacks: { label: (c) => ` R$ ${c.parsed.y.toFixed(2)}` }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: m3.onSurfaceVariant, font: { family: 'Plus Jakarta Sans', size: 11 } } },
        y: {
          grid: { color: m3.gridLines },
          ticks: { color: m3.onSurfaceVariant, font: { family: 'JetBrains Mono', size: 11 }, callback: (v) => `R$ ${v}` }
        }
      }
    }
  });
}

/* ==========================================================================
   6. GRÁFICO 4: MATCH DE CARREIRA (M3 TOKENS)
   ========================================================================== */

function renderizarGraficoMatchCarreira(jobs) {
  const canvas = garantirCanvas('holderMatch', 'chartMatchCarreira');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const m3 = obterTokensM3();
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
        backgroundColor: [m3.secondary, m3.primary, m3.tertiary, m3.isLight ? '#7C6F93' : '#B8A6CE'],
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
          backgroundColor: m3.tooltipBg,
          titleColor: m3.tooltipText,
          bodyColor: m3.tooltipText,
          callbacks: { label: (c) => ` Match: ${c.parsed.x}%` }
        }
      },
      scales: {
        x: {
          min: 0,
          max: 100,
          grid: { color: m3.gridLines },
          ticks: { color: m3.onSurfaceVariant, font: { family: 'JetBrains Mono', size: 11 }, callback: (v) => `${v}%` }
        },
        y: { grid: { display: false }, ticks: { color: m3.onSurface, font: { family: 'Plus Jakarta Sans', size: 12, weight: '700' } } }
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
        <strong style="color: var(--nova-on-surface); display: block;">${job.cargo}</strong>
        <span style="color: var(--nova-outline); font-size: 11.5px; display: inline-flex; align-items: center; gap: 3px;"><span class="material-symbols-rounded" style="font-size: 13px;">location_on</span> ${job.local}</span>
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
            <span class="material-symbols-rounded">description</span>
            <span>CV PDF</span>
          </a>
          <a href="/download${job.cover_docx}" target="_blank" class="btn-tbl-action" title="Baixar Cover Letter DOCX">
            <span class="material-symbols-rounded">article</span>
            <span>DOCX</span>
          </a>
          <a href="/download${job.relatorio_pdf}" target="_blank" class="btn-tbl-action" title="Baixar Relatório Visual Match">
            <span class="material-symbols-rounded">analytics</span>
            <span>Relatório</span>
          </a>
        </div>
      </td>
      <td>
        <button class="btn-tbl-action btn-tbl-pitch" onclick="abrirModalPitch('${job.id}')">
          <span class="material-symbols-rounded">chat</span>
          <span>Copiar Pitch</span>
        </button>
      </td>
    `;

    tbody.appendChild(tr);
  });
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

/* ==========================================================================
   9. SPA NAVIGATION & SEÇÃO VOICE STUDIO UNIFICADA
   ========================================================================== */

let catalogoVozesCache = null;
let configVozStudioCache = null;
let vsAudioPlayerInstance = null;

function navegarParaSecao(secaoId, scrollTargetId) {
  const dashboardView = document.getElementById('dashboard-view');
  const voiceStudioView = document.getElementById('voice-studio-view');

  if (secaoId === 'voice-studio') {
    if (dashboardView) dashboardView.style.display = 'none';
    if (voiceStudioView) voiceStudioView.style.display = 'flex';
    carregarVoiceStudio();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } else {
    if (voiceStudioView) voiceStudioView.style.display = 'none';
    if (dashboardView) dashboardView.style.display = 'flex';

    if (secaoId === 'assistant') {
      const vaElem = document.getElementById('voice-assistant-section');
      if (vaElem) {
        vaElem.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    } else if (scrollTargetId) {
      const targetElem = document.getElementById(scrollTargetId);
      if (targetElem) {
        targetElem.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  if (window.lucide) {
    lucide.createIcons();
  }
}

async function carregarVoiceStudio() {
  try {
    // 1. Busca catálogo de vozes através do proxy reverso
    const [resVoices, resConfig] = await Promise.all([
      fetch('/voice-studio/api/voices'),
      fetch('/voice-studio/api/config')
    ]);

    if (!resVoices.ok || !resConfig.ok) {
      throw new Error("Falha ao comunicar com proxy do Voice Studio");
    }

    catalogoVozesCache = await resVoices.json();
    configVozStudioCache = await resConfig.json();

    renderizarCatalogoVoiceStudio(catalogoVozesCache, configVozStudioCache);
  } catch (err) {
    console.error("Erro ao carregar Voice Studio:", err);
    showToast("⚠️ Conectando com catálogo local...");
    
    // Fallback com catálogo padrão se backend 5050 estiver subindo
    const fallbackVozes = [
      { id: "pt-BR-AntonioNeural", nome: "Antônio", genero: "Masculino", tag: "Executiva / Natural", descricao: "Voz padrão do NOVA. Tom sério, articulado e altamente profissional.", icone: "👨‍💼", frase_demo: "Olá, Fábio! Eu sou o Antônio, sua voz padrão no ecossistema NOVA." },
      { id: "pt-BR-FranciscaNeural", nome: "Francisca", genero: "Feminino", tag: "Acolhedora / Fluida", descricao: "Voz executiva feminina. Dicção impecável, tom caloroso e natural.", icone: "👩‍💼", frase_demo: "Olá, Fábio! Sou a Francisca. Seus relatórios financeiros e candidaturas estão prontos." },
      { id: "pt-BR-FabioNeural", nome: "Fábio", genero: "Masculino", tag: "Direta / Ágil", descricao: "Voz masculina jovem e dinâmica. Ideal para respostas rápidas de terminal.", icone: "👨‍💻", frase_demo: "Fala, Fábio! Sou o Fábio Neural. Construímos uma arquitetura sólida em Java 21." },
      { id: "pt-BR-ThalitaNeural", nome: "Thalita", genero: "Feminino", tag: "Jovem / Expressiva", descricao: "Tom conversacional e enérgico, com entonação espontânea.", icone: "👩‍🎨", frase_demo: "Oi, Fábio! Sou a Thalita. Seus estudos da Trilha Santander 2026 estão avançando." },
      { id: "en-US-GuyNeural", nome: "Guy (English)", genero: "Masculino", tag: "International Tech Lead", descricao: "Voz americana executiva de alta credibilidade para entrevistas e clientes globais.", icone: "🌐", frase_demo: "Hello, Fabio! Guy speaking. Your international portfolio looks solid." },
      { id: "en-US-JennyNeural", nome: "Jenny (English)", genero: "Feminino", tag: "Silicon Valley Native", descricao: "Voz executiva americana fluida e polida para reuniões internacionais.", icone: "✨", frase_demo: "Hi, Fabio! Jenny here. Your Clean Architecture backend is fully verified." }
    ];
    configVozStudioCache = configVozStudioCache || { voz_padrao: "pt-BR-FranciscaNeural", velocidade: "+0%" };
    renderizarCatalogoVoiceStudio(fallbackVozes, configVozStudioCache);
  }
}

let filtroVozAtivo = 'todos';
let buscaVozTermo = '';

function renderizarCatalogoVoiceStudio(vozes, config) {
  const container = document.getElementById('vsVoiceGrid');
  if (!container) return;
  container.innerHTML = '';

  const vozAtivaId = (config && config.voz_padrao) ? config.voz_padrao : 'pt-BR-FranciscaNeural';
  const vozAtivaObj = vozes.find(v => v.id === vozAtivaId) || vozes[0] || {
    id: "pt-BR-FranciscaNeural",
    nome: "Francisca",
    tag: "Acolhedora / Fluida",
    icone: "👩‍💼"
  };

  // 1. Atualiza Showcase Bento Header com a Voz Ativa
  const avatarElem = document.getElementById('vsActiveAvatar');
  const titleElem = document.getElementById('vsActiveVoiceTitle');
  const idElem = document.getElementById('vsActiveVoiceId');
  const tagElem = document.getElementById('vsActiveVoiceTag');

  if (avatarElem) avatarElem.innerText = vozAtivaObj.icone || '🎙️';
  if (titleElem) titleElem.innerText = vozAtivaObj.nome;
  if (idElem) idElem.innerText = vozAtivaObj.id;
  if (tagElem) tagElem.innerText = `${vozAtivaObj.tag || vozAtivaObj.genero} • ${vozAtivaObj.id.startsWith('pt-BR') ? '🇧🇷 Brasil' : '🇺🇸 Estados Unidos'}`;

  // 2. Atualiza slider de velocidade
  const speedVal = parseInt((config && config.velocidade) ? config.velocidade : "+0");
  const speedSlider = document.getElementById('vsSpeedSlider');
  const speedDisplay = document.getElementById('vsSpeedDisplay');
  if (speedSlider) speedSlider.value = isNaN(speedVal) ? 0 : speedVal;
  if (speedDisplay) speedDisplay.innerText = (speedVal >= 0 ? '+' : '') + (isNaN(speedVal) ? 0 : speedVal) + '%';

  // 3. Aplica filtros ativos e busca
  let vozesFiltradas = vozes.filter(v => {
    // Filtro por Categoria
    if (filtroVozAtivo === 'pt-br' && !v.id.startsWith('pt-BR')) return false;
    if (filtroVozAtivo === 'en-us' && !v.id.startsWith('en-US')) return false;
    if (filtroVozAtivo === 'feminino' && (v.genero || '').toLowerCase() !== 'feminino') return false;
    if (filtroVozAtivo === 'masculino' && (v.genero || '').toLowerCase() !== 'masculino') return false;
    if (filtroVozAtivo === 'executiva' && !(v.tag || '').toLowerCase().includes('executiv')) return false;

    // Filtro por Termo de Busca
    if (buscaVozTermo) {
      const matchNome = (v.nome || '').toLowerCase().includes(buscaVozTermo);
      const matchTag = (v.tag || '').toLowerCase().includes(buscaVozTermo);
      const matchDesc = (v.descricao || '').toLowerCase().includes(buscaVozTermo);
      const matchId = (v.id || '').toLowerCase().includes(buscaVozTermo);
      if (!matchNome && !matchTag && !matchDesc && !matchId) return false;
    }

    return true;
  });

  // Atualiza contador de vozes no toolbar
  const allFilterBtn = document.querySelector('.vs-filter-btn:first-child span:last-child');
  if (allFilterBtn) allFilterBtn.innerText = `Todas as Vozes (${vozes.length})`;

  if (vozesFiltradas.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 48px; background: var(--nova-surface); border: 1px dashed var(--nova-outline-variant); border-radius: 20px;">
        <span class="material-symbols-rounded" style="font-size: 36px; color: var(--nova-outline); margin-bottom: 8px;">search_off</span>
        <h4 style="color: var(--nova-on-surface); font-size: 16px; margin-bottom: 4px;">Nenhuma voz encontrada</h4>
        <p style="color: var(--nova-on-surface-variant); font-size: 13px;">Tente ajustar o termo de busca ou selecionar outra categoria acima.</p>
      </div>
    `;
    return;
  }

  // 4. Renderiza Cards com Anatomia Material 3 Design Kit
  vozesFiltradas.forEach(voz => {
    const isActive = voz.id === vozAtivaId;
    const isPT = voz.id.startsWith('pt-BR');
    const card = document.createElement('div');
    card.className = `vs-card md3-card ${isActive ? 'active' : ''}`;
    card.id = `vs-card-${voz.id}`;

    card.innerHTML = `
      <div class="vs-card-top-group md3-card__content-slot" data-slot="content">
        <!-- Header Slot -->
        <div class="vs-card-header md3-card__header-slot" data-slot="header">
          <div class="vs-avatar-squircle">${voz.icone || '🎙️'}</div>
          <div class="vs-card-name-group">
            <h4>${voz.nome}</h4>
            <div class="vs-badges-row">
              <span class="vs-lang-badge md3-badge">${isPT ? '🇧🇷 pt-BR' : '🇺🇸 en-US'}</span>
              <span class="vs-tag-badge md3-badge">${voz.tag || voz.genero}</span>
            </div>
          </div>
        </div>

        <!-- Descrição -->
        <p class="vs-card-desc">${voz.descricao}</p>

        <!-- Sample Quote Box -->
        <div class="vs-sample-box">
          <span class="vs-sample-quote-txt">“${voz.frase_demo}”</span>
        </div>

        <!-- Metadata Footer -->
        <div class="vs-meta-footer">
          <span class="vs-id-code">${voz.id}</span>
          <span class="vs-engine-tag">Neural 24kHz</span>
        </div>
      </div>

      <!-- Actions Slot -->
      <div class="vs-card-actions md3-card__actions-slot" data-slot="actions">
        <button class="btn-vs-action btn-vs-play md3-button md3-button--tonal" id="btn-vs-play-${voz.id}" onclick="ouvirVozStudio('${voz.id}')" title="Ouvir Demonstração">
          <span class="material-symbols-rounded">play_arrow</span>
          <span>Ouvir</span>
        </button>
        <button class="btn-vs-action btn-vs-set md3-button ${isActive ? 'md3-button--filled' : 'md3-button--outlined'}" onclick="definirVozPadraoStudio('${voz.id}', '${voz.nome}')" title="${isActive ? 'Voz padrão ativa' : 'Definir como voz padrão'}">
          <span class="material-symbols-rounded">${isActive ? 'check_circle' : 'star'}</span>
          <span>${isActive ? 'Padrão' : 'Definir'}</span>
        </button>
      </div>
    `;

    container.appendChild(card);
  });
}

function filtrarCatalogoVozes(filtro, btn) {
  filtroVozAtivo = filtro;
  document.querySelectorAll('.vs-filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  renderizarCatalogoVoiceStudio(catalogoVozesCache, configVozStudioCache);
}

function buscarVozesCatalogo(termo) {
  buscaVozTermo = (termo || '').toLowerCase().trim();
  renderizarCatalogoVoiceStudio(catalogoVozesCache, configVozStudioCache);
}

function alternarEstadoUI(estado) {
  alternarEstadoDashboard(estado);
}

function atualizarLabelVelocidade(val) {
  const num = parseInt(val);
  const strVal = (num >= 0 ? '+' : '') + num + '%';
  const display = document.getElementById('vsSpeedDisplay');
  if (display) display.innerText = strVal;
  if (configVozStudioCache) configVozStudioCache.velocidade = strVal;
}

async function salvarVelocidadeStudio(val) {
  atualizarLabelVelocidade(val);
  try {
    await fetch('/voice-studio/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(configVozStudioCache)
    });
    showToast(`⚡ Velocidade ajustada para ${configVozStudioCache.velocidade}`);
  } catch (err) {
    console.error("Erro ao salvar velocidade:", err);
  }
}

function definirFraseTeste(texto) {
  const input = document.getElementById('vsTextInput');
  if (input) {
    input.value = texto;
    input.focus();
  }
}

async function testarVozAtivaStudio() {
  const vozAtiva = (configVozStudioCache && configVozStudioCache.voz_padrao) ? configVozStudioCache.voz_padrao : 'pt-BR-FranciscaNeural';
  await ouvirVozStudio(vozAtiva, true);
}

async function ouvirVozStudio(vozId, isTestingActive = false) {
  const customText = document.getElementById('vsTextInput') ? document.getElementById('vsTextInput').value.trim() : '';
  const vozObj = (catalogoVozesCache || []).find(v => v.id === vozId);
  const texto = customText || (vozObj ? vozObj.frase_demo : "Teste de voz do NOVA.");
  const taxa = (configVozStudioCache && configVozStudioCache.velocidade) ? configVozStudioCache.velocidade : "+0%";

  const playBtn = isTestingActive ? document.getElementById('btnVsTestActive') : document.getElementById(`btn-vs-play-${vozId}`);
  if (playBtn) {
    playBtn.classList.add(isTestingActive ? 'loading' : 'playing');
  }

  try {
    const res = await fetch('/voice-studio/api/synthesize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texto, voz: vozId, taxa })
    });

    if (!res.ok) throw new Error("Erro na síntese via proxy /voice-studio/api/synthesize");

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    
    if (!vsAudioPlayerInstance) {
      vsAudioPlayerInstance = document.getElementById('vsAudioPlayer') || new Audio();
    }
    vsAudioPlayerInstance.src = url;
    conectarOrbAoAudio(vsAudioPlayerInstance);
    await vsAudioPlayerInstance.play();

    vsAudioPlayerInstance.onended = () => {
      if (playBtn) playBtn.classList.remove(isTestingActive ? 'loading' : 'playing');
    };
  } catch (err) {
    console.error(err);
    if (playBtn) playBtn.classList.remove(isTestingActive ? 'loading' : 'playing');
    showToast("⚠️ Falha ao sintetizar áudio no Voice Studio.");
  }
}

async function definirVozPadraoStudio(vozId, nome) {
  if (!configVozStudioCache) configVozStudioCache = {};
  configVozStudioCache.voz_padrao = vozId;

  try {
    await fetch('/voice-studio/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(configVozStudioCache)
    });

    // Atualiza Voice Assistant dropdown e header chip
    const select = document.getElementById('selectVoiceModel');
    if (select) select.value = vozId;
    
    const headerChip = document.getElementById('headerVoiceName');
    if (headerChip) headerChip.innerText = `Voz: ${nome}`;

    renderizarCatalogoVoiceStudio(catalogoVozesCache, configVozStudioCache);
    showToast(`⭐ Voz padrão alterada para: ${nome}!`);
  } catch (err) {
    console.error("Erro ao salvar voz:", err);
    showToast("⚠️ Erro ao salvar voz padrão.");
  }
}



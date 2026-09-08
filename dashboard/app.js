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
let isProcessingVoice = false;
let currentAudioPlayer = null;
let estadoAtualDashboard = 'normal';
let novaLivingShaderEngine = null;

const MENSAGEM_BOAS_VINDAS_RECRUITERS = "Olá! Bem-vindo ao NOVA Control Center, o ecossistema autônomo desenvolvido por Fábio Rodrigues. Sou a interface de voz neural conectada a microsserviços em Java 21, Clean Architecture e Spring AI (MCP). Você pode falar pelo microfone ou testar comandos como /status, /vagas ou /financeiro.";

// LGPD Safe: Por padrão, todo visitante público inicia SEMPRE em Modo Demonstração (LGPD Safe)
function obterPinAutenticado() {
  return sessionStorage.getItem('nova_auth_pin') || sessionStorage.getItem('nova_admin_pin') || '';
}

function obterAuthHeaders() {
  const pin = obterPinAutenticado();
  const headers = {};
  if (pin) {
    headers['Authorization'] = `Bearer ${pin}`;
    headers['X-Admin-PIN'] = pin;
  }
  return headers;
}

const salvoModoPrivacidade = localStorage.getItem('nova_privacy_mode');
let modoPrivacidade = (salvoModoPrivacidade === 'real' && Boolean(obterPinAutenticado())) ? 'real' : 'demo';

// Helper global para estado de demonstração (isDemoMode)
function isDemoMode() {
  return modoPrivacidade === 'demo';
}
window.isDemoMode = isDemoMode;
window.obterPinAutenticado = obterPinAutenticado;

document.addEventListener('DOMContentLoaded', () => {
  inicializarTemaM3();
  inicializarModoPrivacidade();
  executarSplash3D();

  // Garante a mensagem inicial oficial para Tech Recruiters
  const welcomeMsg = document.getElementById('assistantWelcomeMsg');
  if (welcomeMsg) {
    welcomeMsg.textContent = MENSAGEM_BOAS_VINDAS_RECRUITERS;
  }

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

  const hash = (window.location.hash || '').toLowerCase();
  const viewParam = new URLSearchParams(window.location.search).get('view');

  if (hash.includes('voice-studio') || viewParam === 'voice-studio') {
    alternarAbaDedicada('view-voice-studio', document.getElementById('menu-voice-studio'));
  } else if (hash.includes('financas') || viewParam === 'financas') {
    alternarAbaDedicada('view-financas', document.getElementById('menu-financas'));
  } else if (hash.includes('candidaturas') || viewParam === 'candidaturas') {
    alternarAbaDedicada('view-candidaturas', document.getElementById('menu-candidaturas'));
  } else if (hash.includes('estudos') || viewParam === 'estudos') {
    alternarAbaDedicada('view-estudos', document.getElementById('menu-estudos'));
  } else if (hash.includes('engenharia') || viewParam === 'engenharia') {
    alternarAbaDedicada('view-engenharia', document.getElementById('menu-engenharia'));
  } else if (hash.includes('api-docs') || viewParam === 'api-docs' || hash.includes('swagger')) {
    alternarAbaDedicada('view-api-docs', document.getElementById('menu-api-docs'));
  }
});

/* ==========================================================================
   PRIVACY & DEMO PRESENTATION MODE (LGPD, PIN SECURITY & SCREEN RECORDING)
   ========================================================================== */

function inicializarModoPrivacidade() {
  const urlParams = new URLSearchParams(window.location.search);
  const pinAutenticado = Boolean(obterPinAutenticado());

  if (urlParams.get('demo') === 'true' || urlParams.get('mode') === 'demo') {
    modoPrivacidade = 'demo';
  } else if (urlParams.get('demo') === 'false' || urlParams.get('mode') === 'real') {
    // Só entra em modo real se houver PIN autenticado na sessão
    modoPrivacidade = pinAutenticado ? 'real' : 'demo';
  } else {
    // Garantia LGPD: Se não houver PIN na sessão atual, o padrão é SEMPRE 'demo'
    const salvo = localStorage.getItem('nova_privacy_mode');
    modoPrivacidade = (salvo === 'real' && pinAutenticado) ? 'real' : 'demo';
  }
  atualizarBotoesPrivacidade();
}

function solicitarAlternanciaPrivacidade() {
  if (modoPrivacidade === 'real') {
    bloquearVoltarModoDemo();
  } else {
    const pin = obterPinAutenticado();
    if (pin) {
      modoPrivacidade = 'real';
      localStorage.setItem('nova_privacy_mode', 'real');
      document.cookie = `nova_privacy_mode=real; path=/; max-age=31536000; SameSite=Lax`;
      atualizarBotoesPrivacidade();
      carregarDashboard();
      showToast("👁️ Modo Real Ativo: Dados Locais H2 Conectados");
    } else {
      abrirModalPin();
    }
  }
}
window.solicitarAlternanciaPrivacidade = solicitarAlternanciaPrivacidade;
window.alternarModoPrivacidade = solicitarAlternanciaPrivacidade;

function abrirModalPin() {
  const modal = document.getElementById('pinSecurityModal') || document.getElementById('pin-modal');
  const input = document.getElementById('adminPinInput');
  const errBox = document.getElementById('pinErrorMessage');
  
  if (errBox) errBox.style.display = 'none';
  if (input) {
    input.value = '';
    input.classList.remove('input-error');
  }
  if (modal) {
    modal.classList.add('show');
    setTimeout(() => { if (input) input.focus(); }, 120);
  }
}
window.abrirModalPin = abrirModalPin;

function fecharModalPin() {
  const modal = document.getElementById('pinSecurityModal') || document.getElementById('pin-modal');
  if (modal) modal.classList.remove('show');
}
window.fecharModalPin = fecharModalPin;

function alternarVisibilidadePin() {
  const input = document.getElementById('adminPinInput');
  const icon = document.getElementById('pinVisibilityIcon');
  if (input) {
    const isPass = input.type === 'password';
    input.type = isPass ? 'text' : 'password';
    if (icon) icon.textContent = isPass ? 'visibility_off' : 'visibility';
  }
}
window.alternarVisibilidadePin = alternarVisibilidadePin;

async function submeterPinAutenticacao() {
  const input = document.getElementById('adminPinInput');
  const errBox = document.getElementById('pinErrorMessage');
  const errText = document.getElementById('pinErrorText');
  const btn = document.getElementById('btnConfirmPin');
  const pin = input ? input.value.trim() : '';

  if (!pin) {
    if (errBox && errText) {
      errText.textContent = "Por favor, digite o PIN de administrador.";
      errBox.style.display = 'flex';
    }
    if (input) input.classList.add('input-error');
    return;
  }

  if (btn) btn.disabled = true;

  try {
    const res = await fetch('/api/auth/verify-pin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pin })
    });

    const data = await res.json().catch(() => ({ authenticated: false }));

    if (res.ok && data.authenticated) {
      sessionStorage.setItem('nova_auth_pin', pin);
      sessionStorage.setItem('nova_admin_pin', pin);
      modoPrivacidade = 'real';
      localStorage.setItem('nova_privacy_mode', 'real');
      document.cookie = `nova_privacy_mode=real; path=/; max-age=31536000; SameSite=Lax`;

      fecharModalPin();
      atualizarBotoesPrivacidade();
      await carregarDashboard();
      showToast("🔓 Acesso Concedido: Dados Reais Conectados!");
    } else {
      if (input) {
        input.classList.add('input-error');
        input.select();
      }
      if (errBox && errText) {
        errText.textContent = data.message || "PIN incorreto. Tente novamente.";
        errBox.style.display = 'flex';
      }
      modoPrivacidade = 'demo';
      atualizarBotoesPrivacidade();
    }
  } catch (err) {
    console.error("Erro na validação do PIN:", err);
    if (errBox && errText) {
      errText.textContent = "Falha de conexão com o servidor ao validar PIN.";
      errBox.style.display = 'flex';
    }
  } finally {
    if (btn) btn.disabled = false;
  }
}
window.submeterPinAutenticacao = submeterPinAutenticacao;

function bloquearVoltarModoDemo() {
  sessionStorage.removeItem('nova_auth_pin');
  sessionStorage.removeItem('nova_admin_pin');
  modoPrivacidade = 'demo';
  localStorage.setItem('nova_privacy_mode', 'demo');
  document.cookie = `nova_privacy_mode=demo; path=/; max-age=31536000; SameSite=Lax`;
  atualizarBotoesPrivacidade();
  carregarDashboard();
  showToast("🔒 Dados Reais Trancados: Modo Demonstração (LGPD Safe) ativo.");
}
window.bloquearVoltarModoDemo = bloquearVoltarModoDemo;

function atualizarBotoesPrivacidade() {
  const btn = document.getElementById('btnPrivacyToggle');
  const icon = document.getElementById('privacyModeIcon');
  const label = document.getElementById('privacyModeLabel');
  const banner = document.getElementById('demoModeBanner');
  const btnLock = document.getElementById('btnLockRealData');

  const isReal = modoPrivacidade === 'real' && Boolean(obterPinAutenticado());

  if (btn) {
    if (isReal) {
      btn.classList.remove('demo-active');
      btn.classList.add('real-active');
    } else {
      btn.classList.add('demo-active');
      btn.classList.remove('real-active');
    }
  }
  if (icon) {
    icon.textContent = isReal ? 'lock_open' : 'shield';
  }
  if (label) {
    label.textContent = isReal ? 'Dados Reais Conectados' : 'Modo Demo (LGPD)';
  }
  if (banner) {
    banner.style.display = isReal ? 'none' : 'flex';
  }
  if (btnLock) {
    btnLock.style.display = isReal ? 'inline-flex' : 'none';
  }
}
window.atualizarBotoesPrivacidade = atualizarBotoesPrivacidade;

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
    const pin = obterPinAutenticado();
    const isReal = modoPrivacidade === 'real' && Boolean(pin);
    const queryParam = isReal ? '?demo=false' : '?demo=true';
    
    const headers = {
      'X-NOVA-Demo': isReal ? 'false' : 'true',
      ...obterAuthHeaders()
    };

    const res = await fetch(`/api/status${queryParam}`, { headers });
    if (!res.ok) throw new Error("Falha ao carregar API /api/status");
    const data = await res.json();
    dadosGlobais = data;

    if (data.demo_mode) {
      modoPrivacidade = 'demo';
    } else if (data.authenticated) {
      modoPrivacidade = 'real';
    }
    atualizarBotoesPrivacidade();

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
  carregarDashboard();
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
  renderizarExtratoFinanceiro(isDemoMode());
  renderizarAbaEstudos(isDemoMode(), data.estudos);
  if (window.lucide) lucide.createIcons();
}

function renderizarExtratoFinanceiro(isDemo) {
  const tbody = document.getElementById('extratoTableBody');
  if (!tbody) return;

  const transacoesDemo = [
    { data: '28/08/2026', desc: 'Tech Enterprise S/A - Honorários Consultoria', cat: 'Receita Dev', tipo: 'CRÉDITO', valor: 18500.00, isReceita: true },
    { data: '25/08/2026', desc: 'AWS Cloud Services - Cloud Architecture', cat: 'Infra / DevOps', tipo: 'DÉBITO', valor: -3250.00, isReceita: false },
    { data: '22/08/2026', desc: 'Apple Developer Program - Licença Anual', cat: 'Licenças Dev', tipo: 'DÉBITO', valor: -699.00, isReceita: false },
    { data: '20/08/2026', desc: 'Aporte Automático - Caixinha Reserva CDI', cat: 'Investimentos', tipo: 'APLICAÇÃO', valor: -5000.00, isReceita: false },
    { data: '18/08/2026', desc: 'Coworking Hub Recife - Espaço Executivo', cat: 'Operações', tipo: 'DÉBITO', valor: -1800.00, isReceita: false },
    { data: '15/08/2026', desc: 'Certificação Spring Professional & AI Lab', cat: 'Educação / DIO', tipo: 'DÉBITO', valor: -1200.00, isReceita: false },
    { data: '12/08/2026', desc: 'Transferência Pix Recebida - Mentoria Java', cat: 'Consultoria', tipo: 'CRÉDITO', valor: 2500.00, isReceita: true },
    { data: '08/08/2026', desc: 'Supermercado Gourmet - Suprimentos Home Office', cat: 'Alimentação', tipo: 'DÉBITO', valor: -850.40, isReceita: false }
  ];

  const transacoesReais = [
    { data: '28/08/2026', desc: 'Transferência Pix Recebida - Ramon', cat: 'Receita', tipo: 'CRÉDITO', valor: 1500.00, isReceita: true },
    { data: '26/08/2026', desc: 'Supermercado Extra - Compras do Mês', cat: 'Alimentação', tipo: 'DÉBITO', valor: -245.60, isReceita: false },
    { data: '24/08/2026', desc: 'Posto Shell - Combustível', cat: 'Transporte', tipo: 'DÉBITO', valor: -151.87, isReceita: false },
    { data: '22/08/2026', desc: 'Transferência Pix Recebida - Gildeth', cat: 'Receita', tipo: 'CRÉDITO', valor: 500.00, isReceita: true },
    { data: '20/08/2026', desc: 'Amazon Marketplace - Equipamento e Livros', cat: 'Compras', tipo: 'DÉBITO', valor: -318.52, isReceita: false },
    { data: '18/08/2026', desc: 'Transferência Pix Recebida - Sheila', cat: 'Receita', tipo: 'CRÉDITO', valor: 299.00, isReceita: true },
    { data: '15/08/2026', desc: 'Alimentação e Refeições Diversas', cat: 'Alimentação', tipo: 'DÉBITO', valor: -482.78, isReceita: false },
    { data: '10/08/2026', desc: 'Transferência entre Contas', cat: 'Transferências', tipo: 'DÉBITO', valor: -511.00, isReceita: false }
  ];

  const lista = isDemo ? transacoesDemo : transacoesReais;
  tbody.innerHTML = lista.map(t => `
    <tr>
      <td style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--nova-outline);">${t.data}</td>
      <td style="font-weight: 600; color: var(--nova-on-surface);">${t.desc}</td>
      <td><span class="md3-badge" style="font-size: 11px;">${t.cat}</span></td>
      <td><span class="md3-badge ${t.isReceita ? 'md3-badge--success' : ''}" style="font-size: 11px;">${t.tipo}</span></td>
      <td style="text-align: right; font-family: 'JetBrains Mono', monospace; font-weight: 700; padding-right: 24px; color: ${t.isReceita ? 'var(--nova-secondary)' : 'var(--nova-on-surface)'};">
        ${t.isReceita ? '+ ' : '- '}R$ ${Math.abs(t.valor).toFixed(2).replace('.', ',')}
      </td>
    </tr>
  `).join('');

  const pill = document.getElementById('extratoCounterPill');
  if (pill) {
    pill.textContent = `${lista.length} Lançamentos Conciliados`;
  }
}
window.renderizarExtratoFinanceiro = renderizarExtratoFinanceiro;

/* ==========================================================================
   RENDERIZAÇÃO DA ABA ESTUDOS (100% CONCLUÍDO • TRILHA 1 DIO & TRILHA 2 FULL STACK)
   ========================================================================== */
function renderizarAbaEstudos(isDemo, dadosEstudos) {
  const headerTitle = document.getElementById('estudosHeaderTitle');
  const headerSub = document.getElementById('estudosHeaderSub');
  const widgetTitle = document.getElementById('estudosWidgetTitle');
  const widgetSub = document.getElementById('estudosWidgetSub');
  const barLabel = document.getElementById('estudosBarLabel');
  const progressNum = document.getElementById('estudosProgressNum');
  const progressBar = document.getElementById('estudosProgressBar');
  const modAtual = document.getElementById('estudosModAtual');
  const testesVal = document.getElementById('estudosTestesVal');
  const persistVal = document.getElementById('estudosPersistVal');
  const mcpVal = document.getElementById('estudosMcpVal');
  const modulesGrid = document.getElementById('estudosModulesGrid');
  const trilha2Grid = document.getElementById('estudosTrilha2Grid');

  if (headerTitle) headerTitle.textContent = "Trilha Santander 2026 & Mentoria Técnica Back-end";
  if (headerSub) headerSub.textContent = "Bootcamp Santander 2026 - AI Java Back-end (DIO) • Especialização Full Stack Cloud • Metodologias Ativas";
  if (widgetTitle) widgetTitle.textContent = "Trilha Santander 2026 & Engenharia Back-end";
  if (widgetSub) widgetSub.textContent = "DIO AI Java Back-end • Clean Architecture • Spring AI MCP";
  if (barLabel) barLabel.textContent = "Progresso da Trilha Santander";
  if (progressNum) {
    progressNum.textContent = "26 de 26 Atividades (100% Concluído)";
    progressNum.className = "text-green";
  }
  if (progressBar) {
    progressBar.style.width = "100%";
    progressBar.classList.add("bar-emerald-100");
  }
  if (modAtual) modAtual.textContent = "26/26 Concluídas";
  if (testesVal) testesVal.textContent = "40/40 Passando (100%)";
  if (persistVal) persistVal.textContent = "H2 ACID em Arquivo";
  if (mcpVal) mcpVal.textContent = "Spring AI Model Context";

  if (modulesGrid) {
    modulesGrid.innerHTML = `
      <div class="estudo-module-card">
        <div class="module-card-top">
          <span class="module-number-badge">MÓDULO 01</span>
          <span class="md3-badge md3-badge--success card-badge metric-pill">CONCLUÍDO</span>
        </div>
        <h4 class="module-card-title">Fundamentos de Java 21 & POO</h4>
        <p class="module-card-desc">Sintaxe moderna, orientação a objetos profunda, tipos primitivos, wrappers e boas práticas.</p>
        <ul class="module-topics-list">
          <li><span class="material-symbols-rounded text-green">check_circle</span> Classes, Objetos e Encapsulamento</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Herança, Polimorfismo e Interfaces</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Tratamento de Exceções & Collections API</li>
        </ul>
      </div>

      <div class="estudo-module-card">
        <div class="module-card-top">
          <span class="module-number-badge">MÓDULO 02</span>
          <span class="md3-badge md3-badge--success card-badge metric-pill">CONCLUÍDO</span>
        </div>
        <h4 class="module-card-title">Dominando Java 21 & Features Modernas</h4>
        <p class="module-card-desc">Records imutáveis, Pattern Matching avançado, Sealed Classes, Sequenced Collections e Virtual Threads.</p>
        <ul class="module-topics-list">
          <li><span class="material-symbols-rounded text-green">check_circle</span> Records & Imutabilidade de Domínio</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Pattern Matching for switch</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Virtual Threads (Project Loom)</li>
        </ul>
      </div>

      <div class="estudo-module-card">
        <div class="module-card-top">
          <span class="module-number-badge">MÓDULO 03</span>
          <span class="md3-badge md3-badge--success card-badge metric-pill">CONCLUÍDO</span>
        </div>
        <h4 class="module-card-title">Ecossistema Spring Boot 3.3</h4>
        <p class="module-card-desc">Construção de APIs RESTful robustas, Spring Data JPA, H2 Database e validação Bean Validation.</p>
        <ul class="module-topics-list">
          <li><span class="material-symbols-rounded text-green">check_circle</span> Spring Web & Controladores REST</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Spring Data JPA & Transações ACID</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Tratamento Centralizado de Erros (RFC 7807)</li>
        </ul>
      </div>

      <div class="estudo-module-card">
        <div class="module-card-top">
          <span class="module-number-badge">MÓDULO 04</span>
          <span class="md3-badge md3-badge--success card-badge metric-pill">CONCLUÍDO</span>
        </div>
        <h4 class="module-card-title">Clean Architecture & SOLID</h4>
        <p class="module-card-desc">Segregação estrita em camadas de Domínio, Aplicação, Infraestrutura e Apresentação sem acoplamento.</p>
        <ul class="module-topics-list">
          <li><span class="material-symbols-rounded text-green">check_circle</span> Princípios SOLID na Prática</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Use Cases Independentes de Framework</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Inversão de Dependências (DIP)</li>
        </ul>
      </div>

      <div class="estudo-module-card">
        <div class="module-card-top">
          <span class="module-number-badge">MÓDULO 05</span>
          <span class="md3-badge md3-badge--success card-badge metric-pill">CONCLUÍDO</span>
        </div>
        <h4 class="module-card-title">Spring AI & Model Context Protocol</h4>
        <p class="module-card-desc">Integração do ecossistema Java com LLMs (Gemini), servidor de ferramentas MCP e engenharia de contexto.</p>
        <ul class="module-topics-list">
          <li><span class="material-symbols-rounded text-green">check_circle</span> Spring AI MCP Server (@Tool)</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Tool Calling & Function Execution</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Pipelines Autônomos de IA & Fallback</li>
        </ul>
      </div>

      <div class="estudo-module-card">
        <div class="module-card-top">
          <span class="module-number-badge">MÓDULO 06</span>
          <span class="md3-badge md3-badge--success card-badge metric-pill">CONCLUÍDO</span>
        </div>
        <h4 class="module-card-title">Testes Automatizados com JUnit 5</h4>
        <p class="module-card-desc">Estratégias completas de TDD, mocks com Mockito, testes de integração de Use Cases e validação de regressão.</p>
        <ul class="module-topics-list">
          <li><span class="material-symbols-rounded text-green">check_circle</span> Testes Unitários de Regras de Negócio</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Mocking de Portas e Repositórios</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Cobertura de Código & AssertJ (40/40)</li>
        </ul>
      </div>
    `;
  }

  if (trilha2Grid) {
    trilha2Grid.innerHTML = `
      <div class="estudo-module-card">
        <div class="module-card-top">
          <span class="module-number-badge">MÓDULO 01</span>
          <span class="md3-badge md3-badge--success card-badge metric-pill">CONCLUÍDO</span>
        </div>
        <h4 class="module-card-title">TypeScript Avançado & React Reativo</h4>
        <p class="module-card-desc">Desenvolvimento frontend moderno e tipado com SPA reativo, hooks customizados e consumo de APIs.</p>
        <ul class="module-topics-list">
          <li><span class="material-symbols-rounded text-green">check_circle</span> Tipagem Estrita, Generics e Utility Types</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Hooks Avançados & Gestão de Estado Imutável</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Integração com REST APIs e WebSockets</li>
        </ul>
      </div>

      <div class="estudo-module-card">
        <div class="module-card-top">
          <span class="module-number-badge">MÓDULO 02</span>
          <span class="md3-badge md3-badge--success card-badge metric-pill">CONCLUÍDO</span>
        </div>
        <h4 class="module-card-title">Design Systems no Figma & Material Design 3</h4>
        <p class="module-card-desc">Criação de interfaces elegantes no padrão Apple com Glassmorphism profundo, acessibilidade e Bento Grid.</p>
        <ul class="module-topics-list">
          <li><span class="material-symbols-rounded text-green">check_circle</span> Design Tokens, Variáveis e Tipografia Expressiva</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Glassmorphism & Micro-interações Apple Standard</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Componentes Reutilizáveis & Acessibilidade WCAG 2.1</li>
        </ul>
      </div>

      <div class="estudo-module-card">
        <div class="module-card-top">
          <span class="module-number-badge">MÓDULO 03</span>
          <span class="md3-badge md3-badge--success card-badge metric-pill">CONCLUÍDO</span>
        </div>
        <h4 class="module-card-title">Containerização com Docker & Multi-stage</h4>
        <p class="module-card-desc">Padronização de ambientes de execução, empacotamento enxuto de microsserviços e isolamento de dependências.</p>
        <ul class="module-topics-list">
          <li><span class="material-symbols-rounded text-green">check_circle</span> Dockerfiles Otimizados com Multi-stage Build</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Minimização de Imagens com Distroless e Alpine</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Docker Compose para Orquestração Multi-serviço</li>
        </ul>
      </div>

      <div class="estudo-module-card">
        <div class="module-card-top">
          <span class="module-number-badge">MÓDULO 04</span>
          <span class="md3-badge md3-badge--success card-badge metric-pill">CONCLUÍDO</span>
        </div>
        <h4 class="module-card-title">CI/CD com GitHub Actions & Testes</h4>
        <p class="module-card-desc">Esteiras de entrega contínua com execução automática de testes JUnit 5, linter e validações a cada push.</p>
        <ul class="module-topics-list">
          <li><span class="material-symbols-rounded text-green">check_circle</span> Pipelines de Integração Contínua Automatizados</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Execução de Testes JUnit 5 e Linters no Push</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Build e Validação de Artefatos em Pipeline</li>
        </ul>
      </div>

      <div class="estudo-module-card">
        <div class="module-card-top">
          <span class="module-number-badge">MÓDULO 05</span>
          <span class="md3-badge md3-badge--success card-badge metric-pill">CONCLUÍDO</span>
        </div>
        <h4 class="module-card-title">Deploy em Nuvem & Infraestrutura Cloud (Render)</h4>
        <p class="module-card-desc">Publicação produtiva em nuvem pública com SSL automático, variáveis de ambiente seguras e zero downtime.</p>
        <ul class="module-topics-list">
          <li><span class="material-symbols-rounded text-green">check_circle</span> Deploy Contínuo de Microsserviços e Web SPAs</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Configuração de Variáveis de Ambiente e Secrets</li>
          <li><span class="material-symbols-rounded text-green">check_circle</span> Health Checks, Monitoramento de Uptime e SSL</li>
        </ul>
      </div>
    `;
  }
}
window.renderizarAbaEstudos = renderizarAbaEstudos;

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
    const btnMic = document.getElementById('btnMicToggle');
    if (btnMic) btnMic.classList.add('active');
    const btnLbl = document.getElementById('btnMicLabel');
    if (btnLbl) btnLbl.innerText = 'Gravando...';
  };

  recognition.onresult = async (event) => {
    // 1. Anti-Loop Acústico: Se já estiver processando requisição ou reproduzindo áudio, ignora captura
    if (isProcessingVoice) {
      return;
    }

    // 2. Só envia requisição quando isFinal for true, evitando múltiplos envios em loop
    if (!event.results || !event.results[0] || event.results[0].isFinal !== true) {
      return;
    }

    const transcricao = (event.results[0][0].transcript || "").trim();
    if (!transcricao) return;

    // 3. Bloqueia novas capturas e interrompe o microfone temporariamente
    isProcessingVoice = true;
    try {
      recognition.abort();
    } catch (e) {}

    adicionarMensagemChat('user', transcricao, transcricao);
    atualizarEstadoVoz('thinking', 'Processando resposta...');
    await enviarComandoParaBackend(transcricao);
  };

  recognition.onerror = (event) => {
    console.warn("Erro no reconhecimento de fala:", event.error);
    if (!isProcessingVoice) {
      atualizarEstadoVoz('idle', 'Pronto para ouvir');
    }
    const btnMic = document.getElementById('btnMicToggle');
    if (btnMic) btnMic.classList.remove('active');
    const btnLbl = document.getElementById('btnMicLabel');
    if (btnLbl) btnLbl.innerText = 'Pressione para Falar';
    isRecording = false;
  };

  recognition.onend = () => {
    isRecording = false;
    const btnMic = document.getElementById('btnMicToggle');
    if (btnMic) btnMic.classList.remove('active');
    const btnLbl = document.getElementById('btnMicLabel');
    if (btnLbl) btnLbl.innerText = 'Pressione para Falar';
  };
}

function toggleGravacaoVoz() {
  if (!recognition) {
    showToast("⚠️ Reconhecimento de voz não suportado neste navegador.");
    return;
  }

  // Previne acionamento durante processamento ou reprodução
  if (isProcessingVoice) {
    showToast("Aguarde a resposta atual terminar antes de falar.");
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
  const texto = input ? input.value.trim() : '';
  if (!texto) return;

  // Interrompe áudio anterior se estiver tocando
  if (isProcessingVoice && currentAudioPlayer) {
    try { currentAudioPlayer.pause(); } catch (e) {}
    currentAudioPlayer = null;
  }

  isProcessingVoice = true;
  if (recognition) {
    try { recognition.abort(); } catch (e) {}
  }

  adicionarMensagemChat('user', texto, texto);
  atualizarEstadoVoz('thinking', 'Processando resposta...');
  if (input) input.value = '';
  enviarComandoParaBackend(texto);
}

function executarPromptRapido(prompt) {
  const input = document.getElementById('vaTextInput');
  if (input) input.value = prompt;
  enviarTextoDigitado();
}

async function enviarComandoParaBackend(comando) {
  const selectVoz = document.getElementById('selectVoiceModel');
  const vozEscolhida = selectVoz ? selectVoz.value : 'pt-BR-FranciscaNeural';
  const pinAutenticado = sessionStorage.getItem('nova_auth_pin') || sessionStorage.getItem('nova_admin_pin') || '';
  const isDemo = modoPrivacidade === 'demo' || !pinAutenticado;

  try {
    const res = await fetch('/api/voice/interact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-NOVA-PIN': pinAutenticado,
        'X-NOVA-Demo': isDemo ? 'true' : 'false',
        ...obterAuthHeaders()
      },
      body: JSON.stringify({
        comando,
        voz: vozEscolhida,
        is_demo: isDemo,
        pin: pinAutenticado
      })
    });

    if (!res.ok) throw new Error("Erro na resposta do servidor");
    const data = await res.json();

    // Adiciona resposta do assistente no diálogo passando comando para checagem de apresentação
    adicionarMensagemChat('assistant', data.texto, comando);

    // Reproduz o áudio neural retornado em Base64
    if (data.audio_base64) {
      reproduzirAudioBase64(data.audio_base64);
    } else {
      atualizarEstadoVoz('idle', 'Pronto para ouvir');
      isProcessingVoice = false;
    }

  } catch (err) {
    console.error("Erro na interação de voz:", err);
    adicionarMensagemChat('assistant', "Desculpe, ocorreu uma instabilidade ao conectar com o serviço de voz.", comando);
    atualizarEstadoVoz('idle', 'Pronto para ouvir');
    isProcessingVoice = false;
  }
}

function reproduzirAudioBase64(base64Data) {
  if (currentAudioPlayer) {
    try { currentAudioPlayer.pause(); } catch (e) {}
    currentAudioPlayer = null;
  }

  // Interrompe o microfone temporariamente para evitar loop acústico
  if (recognition) {
    try { recognition.abort(); } catch (e) {}
  }
  isProcessingVoice = true;

  const audioSrc = "data:audio/mp3;base64," + base64Data;
  currentAudioPlayer = new Audio(audioSrc);

  currentAudioPlayer.onplay = () => {
    atualizarEstadoVoz('speaking', 'NOVA Falando...');
    conectarOrbAoAudio(currentAudioPlayer);
  };

  currentAudioPlayer.onended = () => {
    atualizarEstadoVoz('idle', 'Pronto para ouvir');
    currentAudioPlayer = null;
    isProcessingVoice = false; // Libera o microfone novamente
  };

  currentAudioPlayer.onerror = () => {
    console.error("Erro ao tocar áudio");
    atualizarEstadoVoz('idle', 'Pronto para ouvir');
    currentAudioPlayer = null;
    isProcessingVoice = false; // Libera o microfone
  };

  currentAudioPlayer.play().catch(e => {
    console.warn("Autoplay bloqueado pelo navegador:", e);
    atualizarEstadoVoz('idle', 'Pronto para ouvir');
    currentAudioPlayer = null;
    isProcessingVoice = false;
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

function adicionarMensagemChat(remetente, texto, comandoOrigem = '') {
  const dialogBox = document.getElementById('vaDialogBox');
  if (!dialogBox) return;
  const msg = document.createElement('div');
  msg.className = `va-message ${remetente}`;

  const avatar = remetente === 'user' ? '👤' : '🌌';
  const author = remetente === 'user' ? 'Você' : 'NOVA';

  // Identifica intenção de apresentação para renderizar os 4 botões de atalho rápido
  const cmdNorm = (comandoOrigem || "").toLowerCase();
  const txtNorm = (texto || "").toLowerCase();
  const termosApresentacao = [
    "o que você pode fazer", "o que voce pode fazer",
    "o que você faz", "o que voce faz",
    "quais suas funcoes", "quais suas funções",
    "quais seus comandos", "quais os comandos",
    "como pode me ajudar", "o que você sabe fazer",
    "o que voce sabe fazer", "o que pode fazer"
  ];
  const ehApresentacao = remetente === 'assistant' && (
    termosApresentacao.some(t => cmdNorm.includes(t)) ||
    txtNorm.includes("sou o nova, seu assistente") ||
    txtNorm.includes("posso consultar seu saldo") ||
    cmdNorm.includes("ajuda") ||
    cmdNorm.includes("comandos")
  );

  let botoesApresentacaoHtml = '';
  if (ehApresentacao) {
    botoesApresentacaoHtml = `
      <div class="va-quick-actions-bar" role="group" aria-label="Atalhos rápidos de navegação">
        <button type="button" class="btn-va-action" onclick="executarPromptRapido('NOVA, qual é o meu saldo atual?')">
          <span class="btn-va-icon">💰</span>
          <span>Saldo</span>
        </button>
        <button type="button" class="btn-va-action" onclick="executarPromptRapido('quais são as minhas candidaturas ativas?')">
          <span class="btn-va-icon">💼</span>
          <span>Vagas</span>
        </button>
        <button type="button" class="btn-va-action" onclick="executarPromptRapido('como estão os meus estudos?')">
          <span class="btn-va-icon">📚</span>
          <span>Estudos</span>
        </button>
        <button type="button" class="btn-va-action" onclick="executarPromptRapido('status da engenharia e microsserviços')">
          <span class="btn-va-icon">⚡</span>
          <span>Engenharia</span>
        </button>
      </div>
    `;
  }

  msg.innerHTML = `
    <div class="msg-avatar">${avatar}</div>
    <div class="msg-content">
      <span class="msg-author">${author}</span>
      <p>${texto}</p>
      ${botoesApresentacaoHtml}
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
    const percentual = 100.0;
    animarContagem('kpiDio', percentual, '', '% Concluído', 850, 1);
    const bar = document.getElementById('kpiDioBar');
    if (bar) {
      bar.style.width = '100%';
      bar.style.background = 'linear-gradient(90deg, #10b981, #059669)';
    }
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

  const counterPill = document.getElementById('tableCounterPill');
  if (counterPill) {
    counterPill.textContent = `${jobs.length} ${jobs.length === 1 ? 'Empresa Ativa' : 'Empresas Ativas'}`;
  }
  const sideCounter = document.getElementById('sidebarJobCounter');
  if (sideCounter && (!window.filtroTrilhaAtual || window.filtroTrilhaAtual === 'todas')) {
    sideCounter.textContent = jobs.length;
  }

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
      <td class="col-faixa-salarial">
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

let filtroTrilhaAtual = 'todas';
window.filtroTrilhaAtual = filtroTrilhaAtual;

function filtrarTrilhaCandidaturas(trilha, btnElem) {
  filtroTrilhaAtual = trilha;
  window.filtroTrilhaAtual = trilha;

  // Atualiza botões
  document.querySelectorAll('.btn-filter-trilha').forEach(btn => btn.classList.remove('active'));
  if (btnElem) {
    btnElem.classList.add('active');
  }

  const todasVagas = (dadosGlobais && dadosGlobais.candidaturas) ? dadosGlobais.candidaturas : [];
  if (trilha === 'todas') {
    renderizarTabelaCandidaturas(todasVagas);
    return;
  }

  const filtradas = todasVagas.filter(job => {
    const texto = `${job.nome} ${job.cargo} ${(job.stack || []).join(' ')} ${job.cv_pdf || ''} ${job.local || ''}`.toLowerCase();
    if (trilha === 'tech') {
      return texto.includes('java') || texto.includes('backend') || texto.includes('dev') || texto.includes('architect') || texto.includes('tech') || texto.includes('engineer');
    }
    if (trilha === 'mkt') {
      return texto.includes('marketing') || texto.includes('mkt') || texto.includes('audiovisual') || texto.includes('filmmaker') || texto.includes('design') || texto.includes('campaign') || texto.includes('growth');
    }
    if (trilha === 'suporte') {
      return texto.includes('suporte') || texto.includes('support') || texto.includes('operaç') || texto.includes('operac') || texto.includes('onboarding') || texto.includes('cx');
    }
    return true;
  });

  renderizarTabelaCandidaturas(filtradas);
  showToast(`Filtro aplicado: ${trilha.toUpperCase()} (${filtradas.length} vagas)`);
}
window.filtrarTrilhaCandidaturas = filtrarTrilhaCandidaturas;

function alternarAbaDedicada(abaId, linkElem) {
  // 1. Esconde todos os painéis com a classe .view-panel ou .view-section
  document.querySelectorAll('.view-panel, .view-section').forEach(p => {
    p.classList.remove('active', 'active-view');
    p.style.display = 'none';
  });

  // 2. Localiza e exibe o painel alvo
  let targetView = document.getElementById(abaId);
  if (!targetView && abaId === 'view-voice-studio') {
    targetView = document.getElementById('voice-studio-view');
  }
  if (!targetView && abaId === 'view-dashboard') {
    targetView = document.getElementById('dashboard-view');
  }

  if (targetView) {
    targetView.style.display = 'flex';
    targetView.classList.add('active', 'active-view');
  }

  // 3. Atualiza destaque ativo na sidebar sem saltos
  const mapaMenus = {
    'view-dashboard': 'menu-overview',
    'view-financas': 'menu-financas',
    'view-candidaturas': 'menu-candidaturas',
    'view-estudos': 'menu-estudos',
    'view-voice-studio': 'menu-voice-studio',
    'view-engenharia': 'menu-engenharia',
    'view-api-docs': 'menu-api-docs'
  };

  document.querySelectorAll('.dabang-sidebar .menu-link').forEach(l => l.classList.remove('active'));
  if (linkElem) {
    linkElem.classList.add('active');
  } else {
    const menuId = mapaMenus[abaId];
    if (menuId) {
      const el = document.getElementById(menuId);
      if (el) el.classList.add('active');
    }
  }

  // 4. Sem saltos de tela e sem recarregar a página
  window.scrollTo({ top: 0, behavior: 'instant' });

  // 5. Redimensiona gráficos quando as abas se tornam visíveis e inicializa dados
  if (abaId === 'view-financas') {
    requestAnimationFrame(() => {
      if (chartEvolucao) chartEvolucao.resize();
      if (chartCategorias) chartCategorias.resize();
      if (chartTargetReality) chartTargetReality.resize();
    });
  } else if (abaId === 'view-candidaturas') {
    requestAnimationFrame(() => {
      if (chartMatch) chartMatch.resize();
    });
  } else if (abaId === 'view-voice-studio') {
    carregarVoiceStudio();
  } else if (abaId === 'view-api-docs') {
    selecionarEndpointPayload(endpointPayloadAtualChave || 'resumo');
  }

  if (window.lucide) {
    lucide.createIcons();
  }
}
window.alternarAbaDedicada = alternarAbaDedicada;

function configurarBuscaGlobal() {
  const searchInput = document.getElementById('globalSearchInput');
  if (!searchInput) return;

  searchInput.addEventListener('keyup', (e) => {
    const termo = e.target.value.toLowerCase().trim();
    if (!termo) {
      renderizarTabelaCandidaturas(dadosGlobais ? dadosGlobais.candidaturas : []);
      return;
    }

    // Se o usuário está em outra aba, alterna suavemente para a aba de candidaturas
    const candView = document.getElementById('view-candidaturas');
    if (candView && candView.style.display === 'none') {
      alternarAbaDedicada('view-candidaturas', document.getElementById('menu-candidaturas'));
    }

    const filtrados = (dadosGlobais && dadosGlobais.candidaturas ? dadosGlobais.candidaturas : []).filter(j => 
      j.nome.toLowerCase().includes(termo) || 
      j.cargo.toLowerCase().includes(termo) ||
      j.local.toLowerCase().includes(termo) ||
      (j.stack || []).some(s => s.toLowerCase().includes(termo))
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
  if (secaoId === 'voice-studio') {
    alternarAbaDedicada('view-voice-studio', document.getElementById('menu-voice-studio'));
  } else if (secaoId === 'assistant') {
    alternarAbaDedicada('view-dashboard', document.getElementById('menu-overview'));
    const vaElem = document.getElementById('voice-assistant-section');
    if (vaElem) {
      vaElem.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  } else if (scrollTargetId === 'financas' || secaoId === 'financas') {
    alternarAbaDedicada('view-financas', document.getElementById('menu-financas'));
  } else if (scrollTargetId === 'candidaturas' || secaoId === 'candidaturas') {
    alternarAbaDedicada('view-candidaturas', document.getElementById('menu-candidaturas'));
  } else if (scrollTargetId === 'estudos' || secaoId === 'estudos') {
    alternarAbaDedicada('view-estudos', document.getElementById('menu-estudos'));
  } else if (scrollTargetId === 'engenharia' || secaoId === 'engenharia') {
    alternarAbaDedicada('view-engenharia', document.getElementById('menu-engenharia'));
  } else if (scrollTargetId === 'api-docs' || secaoId === 'api-docs') {
    alternarAbaDedicada('view-api-docs', document.getElementById('menu-api-docs'));
  } else {
    alternarAbaDedicada('view-dashboard', document.getElementById('menu-overview'));
  }
}
window.navegarParaSecao = navegarParaSecao;

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
  const texto = customText || (vozObj ? vozObj.frase_demo : MENSAGEM_BOAS_VINDAS_RECRUITERS);
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

    if (res.ok) {
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
      return;
    }

    // Fallback para /api/voice/interact se a rota retornar erro
    const fallbackRes = await fetch('/api/voice/interact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comando: texto, voz: vozId })
    });
    const fallbackData = await fallbackRes.json();
    if (fallbackData && fallbackData.audio_base64) {
      if (!vsAudioPlayerInstance) {
        vsAudioPlayerInstance = document.getElementById('vsAudioPlayer') || new Audio();
      }
      vsAudioPlayerInstance.src = "data:audio/mp3;base64," + fallbackData.audio_base64;
      conectarOrbAoAudio(vsAudioPlayerInstance);
      await vsAudioPlayerInstance.play();
      vsAudioPlayerInstance.onended = () => {
        if (playBtn) playBtn.classList.remove(isTestingActive ? 'loading' : 'playing');
      };
    } else {
      throw new Error("Áudio não retornado");
    }
  } catch (err) {
    console.error("Erro ao sintetizar áudio:", err);
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

/* ==========================================================================
   10. SPRING BOOT REST API EXPLORER & ARQUITETURA (VIEW-API-DOCS)
   ========================================================================== */

const PAYLOADS_API_DOCS = {
  resumo: {
    metodo: 'GET',
    endpoint: '/api/transacoes/resumo',
    desc: 'Cálculo consolidado de receitas, despesas e saldo atual em tempo real',
    statusReq: 'Nenhum Request Body (Endpoint de Consulta GET)',
    reqBody: '// Query Parameters (opcionais):\n// ?mes=09&ano=2026\n// Sem payload no corpo da requisição HTTP GET',
    statusResp: 'Response Body (HTTP 200 OK)',
    respBody: JSON.stringify({
      totalReceitas: 8500.00,
      totalDespesas: 3210.50,
      saldoConsolidado: 5289.50,
      burnRateDiario: 107.02,
      diasRestantesMes: 22,
      projecaoFimMes: 5120.00,
      statusFinanceiro: "SUPERAVIT"
    }, null, 2)
  },
  cadastrar: {
    metodo: 'POST',
    endpoint: '/api/transacoes',
    desc: 'Cadastro de transação com Bean Validation (@Valid) e persistência ACID',
    statusReq: 'Request Body (JSON - Jakarta Bean Validation 3.0)',
    reqBody: JSON.stringify({
      descricao: "Servidor Cloud Render - Produção",
      valor: 45.00,
      tipo: "DESPESA",
      categoria: "SERVICOS",
      data: "2026-09-08"
    }, null, 2),
    statusResp: 'Response Body (HTTP 201 CREATED)',
    respBody: JSON.stringify({
      id: 142,
      descricao: "Servidor Cloud Render - Produção",
      valor: 45.00,
      tipo: "DESPESA",
      categoria: "SERVICOS",
      data: "2026-09-08T16:12:00",
      statusConciliacao: "CONFIRMADO_H2"
    }, null, 2)
  },
  'importar-ofx': {
    metodo: 'POST',
    endpoint: '/api/transacoes/importar-ofx',
    desc: 'Parser e deduplicação bancária inteligente para extratos Nubank OFX/CSV',
    statusReq: 'Request Body (multipart/form-data)',
    reqBody: '// Content-Type: multipart/form-data\n// Campo: file (extrato_nubank_setembro.ofx)\n// O parser nativo Java 21 extrai DTPOSTED, TRNAMT, TRNTYPE e FITID',
    statusResp: 'Response Body (HTTP 200 OK)',
    respBody: JSON.stringify({
      arquivo: "extrato_nubank_setembro.ofx",
      transacoesLidas: 18,
      importadas: 15,
      duplicadasIgnoradas: 3,
      saldoAtualizado: 5289.50,
      status: "SUCESSO_CONCILIACAO_H2"
    }, null, 2)
  },
  projecao: {
    metodo: 'GET',
    endpoint: '/api/transacoes/projecao',
    desc: 'IA Preditiva de fechamento de mês, burn rate diário e dias de reserva financeira',
    statusReq: 'Nenhum Request Body (Endpoint de Consulta GET)',
    reqBody: '// Query Parameters (opcionais):\n// ?horizonteDias=30\n// Baseado no histórico relacional H2 de despesas e caixinhas',
    statusResp: 'Response Body (HTTP 200 OK)',
    respBody: JSON.stringify({
      saldoAtual: 5289.50,
      mediaDespesaDiaria: 107.02,
      diasAteFechamento: 22,
      previsaoDespesas: 2354.44,
      saldoEstimadoFimMes: 2935.06,
      mesesReservaSeguranca: 4.8,
      riscoDeficit: "BAIXO"
    }, null, 2)
  },
  voice: {
    metodo: 'POST',
    endpoint: '/api/voice/command',
    desc: 'Orquestração de comandos por voz, integração com Edge-TTS neural e Spring AI',
    statusReq: 'Request Body (JSON)',
    reqBody: JSON.stringify({
      comando: "NOVA, qual é o meu saldo atual e projeção de fechamento?",
      origem: "DASHBOARD_VOICE_ORB",
      voz: "pt-BR-FranciscaNeural",
      taxa: "+0%"
    }, null, 2),
    statusResp: 'Response Body (HTTP 200 OK)',
    respBody: JSON.stringify({
      textoResposta: "Seu saldo consolidado no banco H2 é de R$ 5.289,50 com projeção superavitária de R$ 2.935,06.",
      audioBase64: "UklGRi4AAABXQVZFZm10IBAAAAABAAEA...",
      vozUtilizada: "pt-BR-FranciscaNeural",
      mcpToolInvocada: "consultar_projecao",
      sucesso: true
    }, null, 2)
  }
};

let endpointPayloadAtualChave = 'resumo';

function selecionarEndpointPayload(chave) {
  const dados = PAYLOADS_API_DOCS[chave] || PAYLOADS_API_DOCS.resumo;
  endpointPayloadAtualChave = chave;

  const methodPill = document.getElementById('payloadMethodPill');
  const endpointPath = document.getElementById('payloadEndpointPath');
  const endpointDesc = document.getElementById('payloadEndpointDesc');
  const reqLabel = document.getElementById('payloadRequestLabel');
  const reqCode = document.getElementById('payloadRequestCode');
  const respLabel = document.getElementById('payloadResponseLabel');
  const respCode = document.getElementById('payloadResponseCode');

  if (methodPill) {
    methodPill.textContent = dados.metodo;
    methodPill.className = `api-method-pill ${dados.metodo.toLowerCase()}`;
  }
  if (endpointPath) endpointPath.textContent = dados.endpoint;
  if (endpointDesc) endpointDesc.textContent = dados.desc;
  if (reqLabel) reqLabel.textContent = dados.statusReq;
  if (reqCode) reqCode.textContent = dados.reqBody;
  if (respLabel) respLabel.textContent = dados.statusResp;
  if (respCode) respCode.textContent = dados.respBody;

  // Atualiza botões switchers
  document.querySelectorAll('.payload-endpoint-switchers .btn-switcher').forEach(btn => {
    btn.classList.remove('active');
    if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(chave)) {
      btn.classList.add('active');
    }
  });
}
window.selecionarEndpointPayload = selecionarEndpointPayload;

function copiarPayloadAtual() {
  const dados = PAYLOADS_API_DOCS[endpointPayloadAtualChave];
  if (!dados) return;

  const payloadCompleto = `// ${dados.metodo} ${dados.endpoint}\n// ${dados.desc}\n\n// --- REQUEST ---\n${dados.reqBody}\n\n// --- RESPONSE ---\n${dados.respBody}`;
  navigator.clipboard.writeText(payloadCompleto).then(() => {
    const btnText = document.getElementById('btnCopyText');
    if (btnText) {
      const original = btnText.textContent;
      btnText.textContent = 'Copiado!';
      setTimeout(() => { btnText.textContent = original; }, 1800);
    }
    showToast(`Contrato ${dados.metodo} ${dados.endpoint} copiado!`);
  }).catch(() => {
    showToast(`Erro ao copiar para a área de transferência`);
  });
}
window.copiarPayloadAtual = copiarPayloadAtual;




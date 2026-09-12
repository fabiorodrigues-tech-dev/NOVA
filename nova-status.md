# 📍 NOVA — Status do Projeto (v3.21 - Endpoint de Health Check Anti-Soneca & Otimização Render)

> Documento oficial de estado consolidado do ecossistema NOVA. Reflete a conclusão integral de **todas as 9 Fases do Roadmap**, a **Arquitetura Contábil Sênior**, a **Separação Arquitetural Definitiva Desktop vs Mobile (v3.15)**, a **Sincronização Dinâmica de Temas (v3.20)** e a **Otimização de Uptime Cloud (v3.21)**: implementação dos endpoints de health check ultra-leves `GET /health` e `GET /ping` (com suporte a método `HEAD`), respondendo em < 3ms com payload padronizado `{"status": "UP", "service": "nova-control-center", "timestamp": "..."}` para monitoramento contínuo anti-soneca (UptimeRobot) e keep-alive 24/7; binding direto da variável `PORT = int(os.environ.get("PORT", 3000))` em `0.0.0.0` no `dashboard/server.py` para resposta instantânea ao roteador do Render e atualização do `healthCheckPath` em `render.yaml`; 44 testes JUnit 5 passando com 100% de sucesso.

**Última atualização:** 12/09/2026  
**Ecossistema:** Java 21, Spring Boot 3.3.3, Spring AI (MCP), Python, Antigravity, Apple Silicon M1  
**Maturidade Geral:** 100% Operacional & Homologado (44 Testes JUnit 5 Passando)  
**Manual Oficial:** [`docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf`](file:///Users/fabioandre/Downloads/nova:/docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf)

---

## 1. Tabela das 9 Fases do Roadmap (100% Concluídas)

| Fase | Título | Status | Entregas & Componentes Chave |
|---|---|---|---|
| **Fase 1** | Arquitetura Multi-Agente & Orquestração | ✅ **100% Concluído** | MAIN Agent + 4 Agentes Especialistas em `.agents/skills/` |
| **Fase 2** | Back-end Java 21 & Clean Architecture | ✅ **100% Concluído** | Spring Boot 3.3.3, DDD, H2 persistente, Repository Pattern |
| **Fase 3** | Spring AI & Model Context Protocol (MCP) | ✅ **100% Concluído** | Tools `@Tool` expostas para IA (Cadastro, Listagem, Resumo) |
| **Fase 4** | Esteira de Carreira & Candidaturas 360° | ✅ **100% Concluído** | 23 Candidaturas (7 Tech, 14 Marketing & 2 Suporte/Operações), Harvard Tech ATS PDF, DOCX |
| **Fase 5** | Motor Gráfico & Relatórios Visuais PDF | ✅ **100% Concluído** | `chart_engine.py` (Matplotlib), Relatório Financeiro, Extrato Autenticado Co-Branding NOVA + Nubank (`financeiro/scripts/gerar_extrato_autenticado_pdf.py`), Manual Técnico Oficial (`docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf`), Dossiê Master (`docs/dossie_tecnico_nova.pdf`) e Portfólio Executivo (`Portfolio_Fabio_Rodrigues_Marketing_Campanhas.pdf`) |
| **Fase 6** | Camada de Voz Neural Humana (Voice AI) | ✅ **100% Concluído** | `edge-tts` + `afplay` nativo, Voice Studio Web (Porta 5050), isolamento estrito LGPD Safe no endpoint `/api/voice/interact` sincronizado com autenticação administrativa por PIN (`sessionStorage.getItem('nova_auth_pin')`, headers `X-NOVA-PIN` e `X-NOVA-Demo`), botão de ação com selo de verificado para download 1-clique do extrato autenticado em PDF, chaveamento dinâmico entre dados reais H2/vagas e dados simulados Demo, prevenção de loop acústico no microfone (`isProcessingVoice` + `recognition.abort()` durante reprodução) e intenção de apresentação com botões de atalho rápido |
| **Fase 7** | NOVA Control Center (Dashboard M3 & Bento Grid) | ✅ **100% Concluído** | Interface executiva de alta fidelidade: SPA com matriz de 7 abas dedicadas (Cockpit, Finanças H2, Candidaturas 360°, Estudos 100% DIO/Full Stack, Voice Studio, Engenharia e Spring Boot API Explorer), Separação Arquitetural Total Desktop & Mobile (`dashboard/css/desktop.css` para `>= 769px` 100% intacto e `dashboard/css/mobile.css` para `<= 768px` com Bottom Navigation Dock estilo iOS flutuante, zero overflow horizontal, carrossel de atalhos e ocultação total da sidebar desktop), alinhamento refinado de badges sem quebra (`white-space: nowrap !important`), Living Shader WebGL, telemetria em tempo real, WCAG AAA e controle de acesso seguro por PIN administrativo (ADMIN_PIN) |
| **Fase 8** | CI/CD GitHub Actions & Importador OFX | ✅ **100% Concluído** | `.github/workflows/ci.yml`, Parser OFX/CSV Nubank, Deduplicação H2 |
| **Fase 9** | Inteligência Preditiva & Consultor Financeiro | ✅ **100% Concluído** | Burn Rate Diário, Projeção de Fechamento, Alertas de Risco, Tool MCP |

---

## 2. Serviços Ativos (Portas Locais) & Automação

| Serviço | Tecnologia | Porta | O que faz |
|---|---|---|---|
| **NOVA Control Center** | Python / HTML5 / Material 3 Expressive / Chart.js | `3000` (`nova.local:3000`) | SPA com 7 abas isoladas (Cockpit, Finanças H2, Candidaturas 360°, Estudos 100% DIO/Full Stack, Voice Studio, Engenharia e Spring Boot API Explorer), Telemetria pulsante, Controle de Acesso por PIN, Living Shader WebGL, downloads 1-clique e Produção Nuvem (`https://nova-control-center-alsl.onrender.com`) |
| **NOVA Voice Studio** | Python / `edge-tts` / `afplay` | `5050` | Catálogo e teste de vozes neurais PT-BR e globais com frase teste executiva |
| **Agente Financeiro API** | Java 21 / Spring Boot 3 / H2 / Spring AI | `8081` | REST + ferramentas MCP + Caixinhas Nubank + Webhook + Importador OFX/CSV + Projeção Preditiva + endpoint de voz |

> **🚀 Scripts de Automação, Nuvem & Compartilhamento:**
> - `start-all.sh`: Inicializa simultaneamente os 3 serviços em background com logs em `logs/` e abre oficialmente o ecossistema no **Google Chrome**.
> - `dashboard/server.py` (`iniciar_dashboard`): Prioriza o Google Chrome no macOS (`webbrowser.get('open -a "Google Chrome" %s')`) com fallback para o navegador padrão.
> - `stop-all.sh`: Encerra e libera com segurança todas as portas (`8081`, `3000`, `5050`).
> - `Dockerfile` & `render.yaml`: Conteinerização multi-stage (Java 21 + Python 3.11) para execução contínua 24/7 no Render.
> - `dashboard/compartilhar.py` (`/compartilhar`): Gera túnel HTTPS público com **Filtro de Privacidade Ativo (Demo Mode LGPD Safe)** para acesso mobile e compartilhamento seguro.

---

## 3. Módulo Financeiro Consolidado & Caixinhas Nubank

- ✅ **Estrutura Oficial de Pastas `financeiro/`**:
  - `financeiro/scripts/`: Utilitários executivos de conciliação e emissão de extratos oficiais em PDF (`gerar_extrato_autenticado_pdf.py`).
  - `financeiro/extratos_ofx/`: Repositório oficial para arquivos `.ofx` baixados do Nubank.
  - `financeiro/investimentos_caixinhas/`: Repositório para comprovantes e saldos das Caixinhas (Reserva e Casal).
  - `financeiro/relatorios_pdf/`: Destino dos relatórios executivos e extratos oficiais autenticados gerados via ReportLab.
- ✅ **Geração Sob Demanda do Extrato Oficial Autenticado em PDF (Co-Branding NOVA + Nubank)**:
  - Script gerador executivo [`financeiro/scripts/gerar_extrato_autenticado_pdf.py`](file:///Users/fabioandre/Downloads/nova:/financeiro/scripts/gerar_extrato_autenticado_pdf.py) com ReportLab e canvas de duas passagens (`NumberedCanvas`).
  - **Co-Branding Executivo de Alto Padrão**:
    - Cabeçalho duplo com Selo Oficial NOVA Control Center (Índigo M3 `#1E1B4B` e `#4F46E5`) e Selo Oficial Nubank ("Integrado via Nubank OFX" em Roxo Nubank `#820AD1`).
    - Metadados de auditoria: Nome do titular (Fábio Rodrigues), período apurado, data e hora de emissão e **Carimbo de Autenticação SHA-256 criptográfico único**.
    - Cards de KPI: Total de Entradas (Verde `#16A34A`), Total de Saídas (Coral `#DC2626`) e Saldo Líquido do mês.
    - Tabela zebrada completa de transações (`repeatRows=1`): Data, Estabelecimento/Descrição, Categoria, Tipo e Valor com cores semânticas.
    - Rodapé oficial persistente em todas as páginas: *"Documento emitido e conciliado eletronicamente pelo NOVA Control Center em cooperação técnica com extratos Nubank"*.
  - PDFs salvos automaticamente em: `financeiro/relatorios_pdf/Extrato_Autenticado_NOVA_Nubank_[Mes]_[Ano].pdf`.
- ✅ **Download 1-Clique Integrado ao Voice Assistant & API Gateway**:
  - Disparo da geração de extrato em segundo plano a cada consulta financeira por voz, chat ou `/api/transacoes/resumo`.
  - Retorno de metadados no payload JSON: `download_url` e `download_label`.
  - Renderização dinâmica de botão elegante no balão de chat do Voice Assistant:
    `<a href="${download_url}" target="_blank" class="btn-download-extrato md3-button md3-button--filled"><span class="material-symbols-rounded">verified</span> Baixar Extrato Autenticado em PDF</a>`.
  - Estilização moderna em `dashboard/styles.css` com gradiente suave nas cores do NOVA e Nubank, ícone de verificado e elevação ao hover.
  - Servidor inteligente: endpoint `/download/` com geração sob demanda imediata se o arquivo ainda não existir no disco.
- ✅ **Calibração do Motor Financeiro & Deduplicação Estrita SHA-256 (v3.12)**:
  - Script executivo [`financeiro/scripts/calibrar_extratos_h2.py`](file:///Users/fabioandre/Downloads/nova:/financeiro/scripts/calibrar_extratos_h2.py) e Use Case Java [`ImportarExtratoOfxUseCase.java`](file:///Users/fabioandre/Downloads/nova:/java-services/agente-financeiro/src/main/java/com/nova/agentefinanceiro/application/usecase/ImportarExtratoOfxUseCase.java) com hashing criptográfico por transação: `SHA256(data + valor + fitid + descricao_limpa)`.
  - Coluna `hash_sha256` mapeada em `TransacaoJpaEntity` com verificação de unicidade no repositório (`existsByHashSha256`), descartando silenciosamente sobreposições e repetições entre extratos de Agosto (completo vs parcial).
  - Categorização semântica refinada: Outback, Ifood, Gamella, Conselho Burguer e AcaiChefCela para `ALIMENTACAO`; PIX para pessoas físicas (Gildeth, Tatiana Kecia, Washington Luiz, Fabio Andre, etc.) para `TRANSFERENCIAS`; Uber e 99 para `TRANSPORTE`; e RDB para `INVESTIMENTO`.
  - **Saldos Reais Oficiais (`financeiro/investimentos_caixinhas/saldos_atuais.properties`)**:
    - Saldo Disponível (Conta Corrente / Liquidez Imediata): `R$ 0,03`.
    - Caixinha "Poupança do Casal 🥰": Bruto `R$ 1.004,00`, Líquido `R$ 1.000,11`, Rendimento `+R$ 16,48` e Meta `R$ 2.700,00` (Progresso: `37%`).
    - Caixinha Reserva de Emergência: `R$ 0,00`.
    - Patrimônio Líquido Total Consolidado: `R$ 1.000,14` (Posição: `11/09/2026`).
  - **Separação Arquitetural no Dashboard**: Saldo Disponível isolado no Card 1 de KPIs (`kpiSaldo`) e no card de conta operacional (`valSaldoConta`), enquanto a Poupança do Casal possui card executivo próprio com barra de progresso visual de meta e rendimento acumulado, sem contaminar o extrato de fluxo operacional mensal.
  - **IA de Voz Francisca Atualizada (`/api/voice/command` e `/api/voice/interact`)**: Respostas neurais de alta precisão para consultas de saldo e caixinha.
- ✅ **Gestão de Caixinhas & Patrimônio Líquido**:
  - Entidade `Caixinha`, Repositório `CaixinhaRepository` e Use Cases `SalvarCaixinhaUseCase` e `ListarCaixinhasUseCase`.
  - Endpoints REST `POST /api/financeiro/caixinhas` e `GET /api/financeiro/caixinhas` (calcula Patrimônio Líquido Total).
- ✅ **Webhook de Notificações Instantâneas Nubank (Tempo Real)**:
  - Endpoint `POST /api/transacoes/webhook-notificacao` no gateway Python (`dashboard/server.py`) e no microsserviço Spring Boot (`java-services`).
  - Autenticação por chave de segurança (`7770`) no JSON payload (`{ "notificacao": "...", "pin": "7770" }`) ou via header HTTP `X-NOVA-PIN: 7770`.
  - Parser Regex inteligente para notificações push do iPhone:
    - *Compras Débito/Crédito:* "Compra de R$ X,XX aprovada no [LOJA]" -> `DESPESA`, valor, loja.
    - *Pix Enviado:* "Você enviou um Pix de R$ X,XX para [NOME]" -> `DESPESA`, valor, destinatário.
    - *Pix Recebido:* "Você recebeu uma transferência Pix de R$ X,XX de [NOME]" -> `RECEITA`, valor, remetente.
    - *NuPay & Pagamentos:* "Compra no débito via NuPay..." -> `DESPESA`, estabelecimento.
  - Categorização semântica automática (Alimentação, Transporte, Saúde, Compras, Transferências, etc.) e persistência idempotente no H2 com deduplicação por data e valor.
- ✅ **Conector Open Finance da Pluggy.ai (`financeiro/scripts/pluggy_sync.py`)**:
  - Integração oficial com a API da Pluggy.ai (`POST https://api.pluggy.ai/auth` e `GET https://api.pluggy.ai/transactions`).
  - Leitura segura de credenciais `PLUGGY_CLIENT_ID` e `PLUGGY_CLIENT_SECRET` via arquivo `.env` ou variáveis de ambiente, com gerador de sandbox para testes.
  - Conciliação direta no H2 com deduplicação semântica.
  - Botões executivos no topo da aba Finanças (`view-financas`): `[ 💜 Conectar Open Finance (Pluggy) ]` e `[ 🔄 Sincronizar Banco ]`.
  - Modal interativo de status e sincronização com atualização da tela sem recarregar a página.
- ✅ **Auto-Ingestão em Lote de Extratos OFX & Sincronização Recursiva (`scripts/sincronizar_extratos_ofx.py`)**:
  - Script utilitário e Use Case Java (`ImportarExtratoOfxUseCase`) com busca recursiva em toda a árvore de `financeiro/` (`financeiro/extratos_ofx/` e subpastas).
  - Extração granular de tags OFX: Data (`<DTPOSTED>`), Valor (`<TRNAMT>`), Descrição (`<MEMO>` / `<NAME>`) e ID Único (`<FITID>`).
  - Deduplicação automática no banco de dados H2 persistente (`financiadb.mv.db`), ignorando duplicatas e preservando a integridade contábil.
  - Resumo executivo em console: `Arquivos processados: X | Transações cadastradas: Y | Transações de Julho: Z`.
- ✅ **Sincronização Automática & Resiliência a Falhas no Dashboard & Voice AI**:
  - Gatilho automático no `dashboard/server.py` que verifica arquivos `.ofx` pendentes ou alterados antes de servir qualquer extrato mensal ou rota financeira.
  - Timeout estendido para 5s nas requisições ao Spring Boot e **Fallback Direto OFX** automático sem estourar código 500, eliminando a mensagem de instabilidade no Voice Assistant.
  - Extratos reais consolidados no H2: **Julho/2026** (95 transações, R$ 10.138,70 em entradas e R$ 9.977,96 em saídas) e **Agosto/2026** (102 transações, R$ 4.887,80 em entradas e R$ 3.977,78 em saídas).
  - Respostas neurais via Francisca: em Modo Real com valores consolidados e maiores categorias, e em Modo Demo com dados protegidos e instrução para desbloqueio via PIN 7770.
- ✅ **Modo Expandido (Fullscreen) do Voice Assistant (`alternarExpansaoVoiceAssistant`)**:
  - Botão de alternância no header (`#btnExpandVa`) alternando ícone entre `open_in_full` e `close_fullscreen`, acompanhado de botão de fechamento dedicado (`#btnCloseExpandedVa`) e suporte ao atalho de teclado `Esc`.
  - Janela modal ampla com Glassmorphism (`backdrop-filter: blur(28px)`), `z-index: 99999`, cantos arredondados (`28px`), elevação suave e expansão vertical da caixa de diálogo (`.va-dialog-box`) ocupando o espaço total (`min-height: 380px`, tipografia 15px e entrelinha 1.6).
- ✅ **Extrato Mensal Dinâmico por Voz, Chat e Seletor Visual (`/extrato [mês]`)**:
  - Parser semântico de meses em linguagem natural ("extrato de [mês]", "quanto gastei em [mês]", "resumo de [mês]", "balanço de [mês/ano]", `/extrato [mês]`, formatos `MM/YYYY`, `YYYY-MM`).
  - Seletor visual `<select id="selectMesExtrato">` no topo da aba Finanças com sincronização dinâmica de KPIs, Gráficos (Evolução, Categorias, Target vs Reality) e tabela de conciliação.
  - Card formatado no diálogo do Voice Assistant com Entradas, Saídas, Saldo Líquido e últimos lançamentos do mês apurado.
  - Conexão aos endpoints `GET /api/transacoes/resumo?inicio=...` e `GET /api/transacoes?inicio=...` do Spring Boot com isolamento estrito LGPD Safe (Modo Real vs Demo).
- ✅ **Refinamentos de UI/UX, PDF Limpo e Inteligência de Voz (v3.10)**:
  - **1. Tecla Enter à Prova de Falhas**: Listener global de `keydown` no `dashboard/app.js` (`!e.shiftKey` em `#vaTextInput` ou `.va-text-input`) com disparo de `enviarTextoDigitado()`, além de listener inline redundante em `dashboard/index.html` e tecla `Esc` para fechamento rápido do modal.
  - **2. Blindagem Anti-Overflow & Proporções**: Aplicação estrita de `width: 100% !important; max-width: 100% !important; box-sizing: border-box !important; overflow-x: hidden !important; word-break: break-word !important; overflow-wrap: anywhere !important;` em `.va-chat-transcription-panel`, `.va-dialog-box`, `.va-message`, `.msg-content`, `.msg-content p` e linhas de extrato no `dashboard/styles.css`. O grupo de input e botão `[▷ Enviar]` foi blindado com `min-width: 0` e `flex-shrink: 0`, eliminando cortes e estouros laterais.
  - **3. Correção Definitiva do Modo Expandido & Sincronização Dinâmica com Temas M3 (Dia e Noite)**: `.voice-assistant-hero-card.is-expanded` totalmente sincronizado com o sistema de temas do dashboard (`[data-theme="light"]` e `[data-theme="dark"]` / `:root:not([data-theme="light"])`), sem cores escuras hardcoded isoladas. No **Modo Dia**, apresenta fundo branco `#FFFFFF`, texto escuro `#1B1C1E`, borda sutil `rgba(0,0,0,0.12)`, backdrop suave de 100vmax (`rgba(0,0,0,0.40)`), painel de chat em `#F3F5FA` e botão de fechar em `#E8ECF4`. No **Modo Noite**, apresenta fundo sólido `#16181F`, texto `#FFFFFF`, borda `#FFFFFF` (16%), backdrop profundo (`rgba(0,0,0,0.82)`), painel `#1E222B`, diálogo `#E2E2E9` (`min-height: 350px`, `max-height: 480px`), botão de fechar visível `<button class="btn-close-expanded">✕ Fechar</button>` e suporte ao atalho `Esc`.
  - **4. Priorização no Topo do "Maior Extrato do Ano"**: Interceptação prioritária no motor de voz (`_processar_intencao_voz_interna` em `dashboard/server.py`) antes de checagens mensais genéricas, respondendo diretamente o recorde de Julho/2026 (R$ 10.138,70 em entradas e mais de R$ 20.116,00 em giro ao longo de 95 transações) com botão de download do Extrato Autenticado em PDF integrado ao diálogo.
  - **5. Eliminação de Quadrados Quebrados no PDF**: Remoção total de glifos unicode incompatíveis com a fonte Helvetica do ReportLab em `financeiro/scripts/gerar_extrato_autenticado_pdf.py`. Substituição por caixas estilizadas `[ NOVA FINANCIAL SUITE ]` em Azul Cobalto (`#234878`) com texto branco e `[ NUBANK CONCILIATION ]` em Roxo Nubank (`#820AD1`) com texto branco, garantindo cabeçalho limpo sem caracteres espúrios.
  - **6. Matriz Inteligente de Categorização de Transações**:
    - *Alimentação*: `OUTBACK`, `CONSELHO BURGUER`, `BETINHO`, `SANTOS ALIMENTOS`, `MELO COSTA`, `GAMELLA`, `IFOOD`.
    - *Transferências*: PIX para pessoas físicas (`IZA CORREIA`, `GILDETH`, `MARIANA`, `CLEITON`, `LUCAS`, `CICERO`, etc.) priorizados estritamente como `Transferências` (nunca Alimentação ou Transporte).
    - *Saúde*: `DISKFARMA` -> `Saúde & Farmácia`.
    - *Compras*: `COSMETICOS`, `TARCILA FERREIRA`, `AMAZON` -> `Compras`.
    - *Investimentos*: `APLICAÇÃO RDB`, `RESGATE RDB` -> `Investimentos`.
    - Extrato de Julho/2026 revalidado e gerado em `financeiro/relatorios_pdf/Extrato_Autenticado_NOVA_Nubank_Julho_2026.pdf`.
- ✅ **Refinamento Visual Executivo da UI/UX & Compactação da Primeira Dobra (v3.14)**:
  - **1. Higienização de Textos e Remoção de Jargões Internos**:
    - Cabeçalho do Voice Assistant atualizado de *"Reconhecimento em Tempo Real & Síntese Neural Base64"* para o elegante e institucional *"Assistente de Inteligência Pessoal & Operações"*.
    - Mensagem inicial de boas-vindas do chat enxugada e objetiva: *"Olá! Sou o assistente de inteligência do NOVA. Posso te ajudar com análises financeiras, esteira de candidaturas e telemetria do sistema. O que deseja consultar?"*.
    - Eliminação completa de duplicação de texto e submissão redundante no input de diálogo.
  - **2. Compactação da Primeira Dobra & Visibilidade dos 4 Cards de KPI**:
    - Altura do card do Voice Assistant reduzida para que os 4 cards de KPI (Saldo, Receitas, Despesas, Estudos) fiquem 100% visíveis na primeira dobra da tela sem exigir qualquer rolagem no desktop.
    - Padding do `.voice-assistant-hero-card` ajustado para `20px 24px`.
    - Container do Voice Orb dimensionado para `140px` e canvas interno para `120px`, mantendo a fluidez e a geometria do living shader WebGL totalmente intactas.
    - Altura da caixa de diálogo (`.va-dialog-box`) calibrada para `100px` com rolagem suave.
  - **3. Limpeza do Header & Remoção da Faixa Amarela**:
    - Remoção definitiva da faixa amarela `#demoModeBanner` do meio da tela.
    - Status consolidado no header em um único botão toggle executivo `[ 🛡️ Modo Demo | Desbloquear ]` ⇄ `[ 🔓 Dados Reais | Bloquear ]` com estilo tonal discreto sem cores berrantes, eliminando o botão secundário redundante de bloqueio.
    - Superfícies dos botões de ação do header (Voz, Telemetria, Tema, Perfil) padronizadas em acabamento monocromático sutil inspirado no design system Material 3 / Apple, mantendo apenas o ponto verde pulsante da telemetria.
  - **4. Reorganização Executiva do Cabeçalho de Finanças & Blindagem Anti-Overflow**:
    - Divisão do cabeçalho da aba Finanças (`.tab-view-header--financas`) em duas linhas funcionais e elegantes:
      * **Linha Superior:** Título institucional ("Gestão Financeira & Inteligência Preditiva") e subtítulo com largura desimpedida, acompanhado do seletor mensal e atalho direto ao Relatório PDF.
      * **Linha Inferior (Toolbar de Ações):** Agrupamento semântico entre ferramentas contábeis (`Balancete Mensal`, `Balanço Patrimonial`, `Comparar Meses`) e integrações bancárias (`Conectar Open Finance`, `Sincronizar Banco`), eliminando emojis duplicados e mantendo ícones vetoriais Material 3.
    - Blindagem estrita contra estouro horizontal em `desktop.css` e `styles.css` (`overflow-x: hidden !important`, `max-width: calc(100% - 260px) !important`), impedindo que qualquer componente deslize por baixo da sidebar ou force rolagem lateral na tela.
  - **5. Blindagem e Restauração do Modo Expandido (.is-expanded) do Voice Assistant**:
    - Eliminação de conflitos de herança em `desktop.css`: regras compactas isoladas com `:not(.is-expanded)`, impedindo que o diálogo fique travado em 100px ou o orb em 140px quando a janela modal é aberta.
    - No modo expandido, o card preenche com elegância a proporção 82vh / 90vw (max 1040px) com cabeçalho `.va-header-row` 100% visível, seletor de voz e botão `[ ✕ Fechar ]`.
    - Eliminação de containing block residual: keyframe `fadeInPanel` ajustado para finalizar em `transform: none` e liberado `overflow: visible !important` em ancestrais sob `body.va-expanded-active`, restaurando o backdrop shadow imersivo (`box-shadow: 0 0 0 100vmax rgba(0, 0, 0, 0.82)`) e o diálogo vertical expandido (`min-height: 320px; max-height: 480px`).
- ✅ **Suíte JUnit 5 Consolidada**:
  - **44 testes automatizados** cobrindo 100% dos use cases, controllers, rotinas contábeis e MCP tools (`./run-tests.sh`).

---

## 4. Estrutura dos 4 Agentes Especialistas (`.agents/skills/`)

```text
.agents/skills/
├── agente-codigo/                 # 💻 Especialista Java 21 / Spring Boot 3 / Clean Architecture / Scaffolding
├── agente-estudos/                # 📚 Especialista Trilha Santander 2026 DIO / Metodologias ativas / Feynman
├── agente-carreira-e-operacoes/   # 💼 Especialista em Candidaturas 360°, Follow-ups LinkedIn e Rotinas Operacionais
└── agente-financeiro/             # 💰 Especialista em Gestão Orçamentária, MCP Tools, OFX/CSV e Projeção Preditiva
```

---

## 5. Regras de Ouro & Segurança

1. **Modificadores de Autonomia & Gatilhos `full access` (`full access`, `(full access)`, `full acess`, `(full acess)`, `/fullaccess`, `!fullaccess`):** Execução ponta a ponta sem interrupções com salvamento prévio em `.backups/ultimo_checkpoint/` e validação final via `./run-tests.sh`.
2. **Sistema de Checkpoint & Reversão (`reverter`, `(reverter)`, `/reverter`, `!reverter`, `reverse`, `(reverse)`, `/reverse`, `!reverse`):** Restauração instantânea para o último checkpoint seguro.
3. **Fidelidade Rigorosa às Bases Oficiais:** Nenhuma candidatura inventa ferramentas ou tecnologias fora das bases oficiais.
4. **Segregação Rigorosa de Links por Especialidade:**
   - *Tech/Dev:* LinkedIn (`https://linkedin.com/in/fabiorodrigues-dev`) + GitHub (`https://github.com/fabiorodrigues-tech-dev/NOVA`).
   - *Suporte/Operações:* LinkedIn (`https://linkedin.com/in/fabiorodrigues-dev`).
   - *Filmmaker/Audiovisual:* Google Drive Audiovisual (`https://drive.google.com/drive/folders/1fhmqNSZG9h7Tv4pFzqysuuBcIY4Sw-ri?usp=sharing`) — **Sem LinkedIn**.
   - *Marketing/Campanhas/Growth/CRM/Branding:* Google Drive Marketing (`https://drive.google.com/drive/folders/1Mz7BoxVzmUnZd24H7n9zrvByGN_bzFxm?usp=sharing`) — **Sem LinkedIn**.
5. **Postura Financeira Conservadora:** Organiza, prevê e dá clareza; nunca toma decisões arbitrárias pelo usuário.
6. **Workspace Limpo:** Zero arquivos PNG residuais.
7. **Padrão Ouro de Nomenclatura de Candidaturas:** `Curriculo_Fabio_Rodrigues_[Area_ou_Cargo].pdf` e `Cover_Letter_Fabio_Rodrigues.docx` / `.pdf` organizados em subpastas por empresa (`carreira/vagas_analisadas/[trilha]/[empresa]/`).
8. **Proteção Rigorosa de Dados Reais por PIN (LGPD Safe) & Sincronização com Motor de Voz:** O servidor web e dashboard operam 100% em Modo Demonstração por padrão. O desbloqueio de dados locais H2, saldos reais e candidaturas confidenciais exige autenticação via PIN de administrador (`ADMIN_PIN`, configurável em ambiente) com token armazenado na sessão local (`sessionStorage.getItem('nova_auth_pin')`), autorização enviada via headers HTTP (`X-NOVA-PIN`, `X-NOVA-Demo`, `X-Admin-PIN` / `Authorization`) e sincronização transparente com o motor de voz (`/api/voice/interact`), que transita autonomamente entre respostas reais do banco H2 e respostas simuladas do Modo Demonstração, com botão rápido no header para bloqueio instantâneo a qualquer momento.
9. **Separação Estrita Desktop vs Mobile:** Toda e qualquer alteração solicitada para celular deve ser feita unicamente no arquivo `mobile.css`. Alterações para desktop devem ser feitas unicamente no `desktop.css`. Uma plataforma nunca pode sobrescrever ou alterar a outra.

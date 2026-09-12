# Manual de Engenharia & Arquitetura de Software — Ecossistema NOVA

**Autor:** Fábio Rodrigues (Recife/PE)  
**Stack Core:** Java 21 LTS, Spring Boot 3.3.3, Clean Architecture (Ports & Adapters), Spring AI MCP, H2 Database (ACID), Python 3.11, Voice AI, Material 3 Expressive, Docker, GitHub Actions, Render Cloud.  
**Repositório Oficial:** https://github.com/fabiorodrigues-tech-dev/NOVA  
**Perfil Profissional:** https://linkedin.com/in/fabiorodrigues-dev  
**Ambiente de Produção (Live):** https://nova-control-center-alsl.onrender.com  

---

## Sumário Executivo

O **NOVA** é um ecossistema multi-agente pessoal e profissional orientado a microsserviços e inteligência artificial autônoma. Desenvolvido sob rigorosos princípios de **Clean Architecture**, **SOLID** e **DevSecOps**, o sistema atua como copiloto de engenharia de software, esteira automatizada de carreiras 360°, motor de inteligência financeira preditiva, contabilidade corporativa sênior (Balancete, Balanço Patrimonial & DRE, Comparativo Horizontal) e síntese de voz neural em alta fidelidade. O ecossistema está 100% conteinerizado (Docker Multi-Stage), conta com suíte de **44 testes automatizados (100% Green)**, esteira de CI/CD automatizada via GitHub Actions e painel executivo NOVA Control Center em SPA com 7 abas dedicadas e refinamento visual executivo v3.14.

---

## Seção 1 — Arquitetura de Microsserviços & Clean Architecture

A arquitetura do microsserviço principal (`agente-financeiro`) foi estruturada em camadas concêntricas e estritamente desacopladas, assegurando que as regras de negócio centrais sejam totalmente agnósticas a frameworks, bancos de dados ou interfaces de entrega.

### 1.1. Estrutura de Camadas (Ports & Adapters)

```text
com.nova.agentefinanceiro/
├── domain/                  # [CAMADA NÚCLEO]
│   ├── model/               # Entidades puras (Transacao, Caixinha, ResumoFinanceiro)
│   └── repository/          # Portas de Saída (Interfaces TransacaoRepository, CaixinhaRepository)
│
├── application/             # [CAMADA DE CASOS DE USO]
│   ├── dto/                 # Records imutáveis (TransacaoRequest, BalanceteResponse, BalancoPatrimonialResponse...)
│   └── usecase/             # Casos de uso (Cadastrar, Listar, Projeção, OFX Parser, Caixinhas, Contabilidade)
│
└── infrastructure/          # [CAMADA DE ADAPTADORES & FRAMEWORKS]
    ├── persistence/         # Adaptadores JPA, hash SHA-256, Mappers bidirecionais e Repositories
    ├── web/                 # Controllers REST (TransacaoController, ContabilidadeController, RFC 7807)
    ├── mcp/                 # Tools corporativas Spring AI Model Context Protocol (@Tool)
    └── config/              # Configurações de Beans e contexto Spring
```

### 1.2. Princípios SOLID Aplicados
- **Single Responsibility Principle (SRP):** Cada Use Case possui uma única razão para mudar (`ContabilidadeUseCase` gerencia exclusivamente apurações contábeis e DRE; `CalcularProjecaoFinanceiraUseCase` foca estritamente no algoritmo preditivo; `ImportarExtratoOfxUseCase` foca na ingestão e deduplicação estrita).
- **Open/Closed Principle (OCP):** Novos formatos de importação ou novos adaptadores de persistência são adicionados via implementação de interfaces sem alterar as regras de domínio existentes.
- **Liskov Substitution Principle (LSP):** As implementações JPA em `infrastructure.persistence` respeitam integralmente os contratos definidos nas interfaces do domínio.
- **Interface Segregation Principle (ISP):** Interfaces granulares e focadas, evitando que adaptadores dependam de métodos que não utilizam.
- **Dependency Inversion Principle (DIP):** O domínio não conhece o Spring nem o JPA. A injeção de dependência ocorre das camadas externas para as internas através de construtores com tipagem forte.

### 1.3. Tratamento Global de Erros (RFC 7807 ProblemDetail)
O sistema implementa tratamento unificado de exceções via `@RestControllerAdvice` e `GlobalExceptionHandler`, emitindo payloads padronizados com timestamp, status HTTP semântico, detalhamento do erro e URI canônica para observabilidade corporativa.

---

## Seção 2 — Casos de Uso Avançados, Arquitetura Contábil Sênior & IA Preditiva

### 2.1. Ingestão Bancária com Deduplicação Estrita SHA-256: `ImportarExtratoOfxUseCase`
O caso de uso de importação bancária realiza a leitura automatizada de extratos bancários em formato `.ofx` e `.csv` do Nubank localizados na pasta `financeiro/extratos_ofx/` e subpastas de forma recursiva:
- **Parser SGML/XML Robusto:** Extração estruturada de nós `<STMTTRN>`, `<TRNAMT>`, `<MEMO>`, `<DTPOSTED>` e `<FITID>`.
- **Hashing Criptográfico SHA-256:** Cada transação gera um hash único determinístico: `SHA256(data + valor + fitid + descricao_limpa)`.
- **Deduplicação Transacional Idempotente:** O repositório verifica a unicidade (`existsByHashSha256`), descartando silenciosamente sobreposições e repetições entre extratos de diferentes períodos sem inflar o banco H2.
- **Classificação Categórica Semântica:** Mapeamento de despesas e receitas em categorias canônicas (`ALIMENTACAO`, `MORADIA`, `TRANSPORTE`, `SAUDE`, `LAZER`, `INVESTIMENTO`, `OUTROS`).

### 2.2. Inteligência Preditiva & CFO Algorítmico: `CalcularProjecaoFinanceiraUseCase`
O módulo preditivo realiza cálculos matemáticos em tempo real para antecipar o balanço financeiro no fechamento do mês:
- **Burn Rate Diário:** Média móvel ponderada de consumo por dia decorrido no ciclo orçamentário:
  $$\text{Burn Rate} = \frac{\sum \text{Despesas do Ciclo}}{\text{Dias Decorridos}}$$
- **Despesa Total Projetada:**
  $$\text{Despesa Projetada} = \text{Despesas Atuais} + (\text{Burn Rate} \times \text{Dias Restantes})$$
- **Saldo Final Projetado:**
  $$\text{Saldo Final} = \text{Receitas Atuais} - \text{Despesa Projetada}$$
- **Classificação de Risco Orçamentário:**
  - `SAUDÁVEL`: Saldo projetado positivo e folga financeira superior a 20% das receitas.
  - `ALERTA`: Saldo projetado positivo mas inferior a 10% das receitas, indicando aceleração do consumo.
  - `CRÍTICO`: Saldo projetado negativo, acionando alertas preditivos de contingência.

### 2.3. Gestão de Caixinhas Nubank & Segregação Patrimonial
- **Isolamento Arquitetural:** Separação estrita entre Conta Corrente de Liquidez Imediata (R$ 0,03) e Caixinhas de Investimento (Poupança do Casal com R$ 1.000,11 líquido / R$ 1.004,00 bruto / rendimento R$ 16,48 / meta R$ 2.700,00; Reserva de Emergência R$ 0,00).
- **Patrimônio Líquido Consolidado:** Apuração em tempo real somando a conta operacional H2 com o saldo líquido de todas as caixinhas (R$ 1.000,14).

### 2.4. Arquitetura Contábil Sênior: `ContabilidadeUseCase` (v3.13)
O ecossistema implementa uma suíte contábil formal corporativa expondo endpoints REST e DTOs Records imutáveis:
- **Balancete de Verificação Mensal (`GET /api/financeiro/balancete?mes=YYYY-MM`):**
  - Apuração de Ativo Circulante, Passivo Circulante, Despesas Operacionais e Receitas Operacionais.
  - Totalização de Créditos (Entradas), Débitos (Saídas) e Validação de Partidas Dobradas (`partidasConsistentes = true/false`).
- **Balanço Patrimonial & DRE Consolidado (`GET /api/financeiro/balanco-patrimonial`):**
  - Demonstração de Resultados do Exercício (Receita Bruta, Deduções e Resultado Líquido).
  - Balanço Patrimonial estruturado com Ativo Circulante conciliado (Conta + Caixinhas), Passivo Circulante e Patrimônio Líquido Total apurado.
- **Comparativo Horizontal de Meses (`GET /api/financeiro/comparativo?mes1=...&mes2=...`):**
  - Análise comparativa entre períodos com cálculo de variação absoluta em reais e percentual para receitas, despesas e saldo líquido.
- **Histórico Anual Consolidado 2026 (`GET /api/financeiro/anual?ano=2026`):**
  - Mapa mensal de entradas, saídas e taxa média de poupança acumulada no ano, destacando o mês de maior faturamento (Julho recorde com R$ 10.138,70).

### 2.5. Webhook Instantâneo Nubank (Tempo Real) & Open Finance (Pluggy.ai)
- **Webhook Nubank (`POST /api/transacoes/webhook-notificacao`):** Autenticação por chave de segurança PIN (7770) e parser Regex para notificações push do iPhone (compras débito/crédito, Pix enviado/recebido e pagamentos NuPay).
- **Conector Open Finance:** Integração com a API da Pluggy.ai (`financeiro/scripts/pluggy_sync.py`) para conciliação direta no H2.

---

## Seção 3 — Protocolo MCP & Integração de IA (Spring AI)

O **Model Context Protocol (MCP)** conecta agentes inteligentes ao sistema corporativo de forma determinística e segura.

### 3.1. Ferramentas Corporativas (@Tool)
Através do Spring AI MCP Server, métodos Java são expostos como ferramentas corporativas acionáveis por LLMs:
- `consultar_resumo_financeiro`: Retorna KPIs orçamentários, balanço consolidado e distribuição por categoria.
- `consultar_projecao_financeira`: Executa a projeção preditiva com Burn Rate Diário.
- `atualizar_caixinha` & `consultar_caixinhas`: Gestão de alocação de reservas e metas com recálculo de Patrimônio Líquido Total.
- `processar_notificacao_nubank`: Webhook semântico para conciliação automática de transferências e pagamentos.

### 3.2. Camada de Voz Neural Humana (Voice AI)
Integração de áudio de baixa latência conectando o pipeline Python (`edge-tts` + `afplay` nativo do macOS) ao endpoint `/api/voice/interact`:
- Transição dinâmica entre dados reais do banco H2 e respostas simuladas do Modo Demonstração.
- Prevenção ativa de loop acústico com desativação do microfone durante a fala.

---

## Seção 4 — Qualidade de Software, Testes & CI/CD (100% Green)

### 4.1. Pirâmide de Testes Automatizados (44/44 JUnit 5 + Mockito)
A suíte conta com **44 testes automatizados** executados e aprovados com 100% de sucesso via `./run-tests.sh`:
- **Testes Unitários de Casos de Uso (100% Isolados):**
  - `ContabilidadeUseCaseTest`: Validação de Balancete, Balanço Patrimonial & DRE, Comparativo de Meses e Histórico Anual.
  - `ImportarExtratoOfxUseCaseTest`: Validação de parsing SGML/XML, tags nulas e deduplicação estrita SHA-256.
  - `CalcularProjecaoFinanceiraUseCaseTest`: Cálculo de Burn Rate e projeção de fechamento orçamentário.
  - `CalcularResumoFinanceiroUseCaseTest`: Apuração consolidada de saldo, receitas, despesas e categorias.
  - `SalvarCaixinhaUseCaseTest` & `ListarCaixinhasUseCaseTest`: Persistência de Caixinhas e cálculo de Patrimônio Líquido.
  - `ProcessarNotificacaoNubankUseCaseTest`: Webhook semântico com validação de PIN 7770 e Regex.
  - `ProcessarComandoVozUseCaseTest`: Roteamento semântico de comandos neurais para ações determinísticas.
- **Testes de Integração WebMvc:**
  - `TransacaoControllerTest`: Validação de requisições mock HTTP, códigos de status e payloads RFC 7807.
  - `CaixinhaControllerTest`: Endpoints REST de consulta e movimentação de caixinhas.
- **Testes de Ferramentas Spring AI MCP:**
  - `FinanceiroMcpToolsTest`: Validação determinística das chamadas `@Tool` expostas para IA.

### 4.2. Pipeline de Integração Contínua (`.github/workflows/ci.yml`)
Esteira automatizada executando em containers Ubuntu a cada push na branch `main`:
- **Job 1 (Java 21 & Maven):** Setup JDK 21 Temurin, compilação de classes e execução da suíte de 44 testes JUnit 5 com relatórios Surefire.
- **Job 2 (Python Quality & Voice Check):** Verificação de sintaxe estática (Flake8), compilação de scripts e validação headless.

---

## Seção 5 — Infraestrutura DevOps, Docker & Deploy em Nuvem (Render)

### 5.1. Docker Multi-Stage Build (`Dockerfile`)
O ecossistema é totalmente conteinerizado através de uma imagem Docker multi-estágio otimizada:
- **Estágio 1 (Build):** Imagem Maven com Eclipse Temurin JDK 21 para compilação e empacotamento do `.jar` do Spring Boot.
- **Estágio 2 (Runtime):** Imagem leve Debian/Ubuntu contendo JRE 21 LTS e runtime Python 3.11, empacotando simultaneamente o microsserviço Java e o servidor HTTP do NOVA Control Center.
- **Segurança do Container:** Usuário não-root, isolamento de portas (`10000` / `3000`) e otimização de camadas.

### 5.2. Blueprint do Render (`render.yaml`) & Execução 24/7
- Deploy automatizado com healthcheck ativo no endpoint `/api/status?demo=true`.
- URL de Produção Oficial: **`https://nova-control-center-alsl.onrender.com`**.
- Resiliência com reinicialização automática e monitoramento contínuo de disponibilidade.

---

## Seção 6 — Frontend SPA com 7 Abas, DevSecOps & Refinamento Visual UI/UX (v3.14)

### 6.1. Matriz de Abas Dedicadas (SPA View Switcher)
O **NOVA Control Center** opera como uma Single Page Application sem recarregamento, estruturado em 7 módulos:
1. **Cockpit Dashboard:** Visão executiva consolidada, Voice Assistant interativo, KPIs corporativos e Living Shader WebGL.
2. **Finanças (H2):** Balanço patrimonial, balancete mensal, comparativo de meses, auditoria de despesas, burn rate diário e gestão de Caixinhas.
3. **Candidaturas 360°:** Rastreamento de vagas ativas, índices de aderência técnica (Match %), filtros por trilha e downloads de dossiês.
4. **Estudos & Certificações:** Monitoramento de trilhas ativas (Santander 2026 DIO 26/26 com Certificado e Full Stack Cloud DevOps 5/5).
5. **Voice Studio Pro:** Laboratório de síntese vocal neural, catálogo de vozes PT-BR/globais e testes executivos.
6. **Engenharia & Testes:** Telemetria dos microsserviços, Clean Architecture 4 Camadas, persistência H2 ACID e suíte de 44 testes 100% Green.
7. **Spring Boot API Explorer:** Painel interno de contratos REST, documentação de endpoints, esquemas JSON e RFC 7807.

### 6.2. Refinamento Visual Executivo da UI/UX (v3.14)
- **Higienização de Textos & Jargões:** Subtítulo do Voice Assistant padronizado institucionalmente como *"Assistente de Inteligência Pessoal & Operações"*, mensagem inicial enxugada e eliminação de inputs duplicados.
- **Compactação da Primeira Dobra:** Card do Voice Assistant rebaixado proporcionalmente (`padding: 20px 24px`, orb `140px/120px`, diálogo `100px`), garantindo que os 4 cards de KPI (Saldo, Receitas, Despesas, Estudos) fiquem 100% visíveis sem exigir rolagem vertical no desktop.
- **Header Limpo & Botão Toggle Unificado:** Remoção da faixa amarela e consolidação do controle de privacidade em botão único `[ 🛡️ Modo Demo | Desbloquear ]` ⇄ `[ 🔓 Dados Reais | Bloquear ]`, com superfícies monocromáticas sutis no padrão Material 3 / Apple.
- **Cabeçalho Executivo de Finanças em 2 Linhas:** Linha superior com título e seletor de mês; linha inferior com toolbar semântica agrupando ferramentas contábeis e conexões Open Finance com ícones vetoriais Material 3 (sem emojis duplicados).
- **Blindagem do Modo Expandido (.is-expanded):** Modal centralizado 82vh / 90vw (max 1040px) com cabeçalho `.va-header-row` 100% visível, botão `[ ✕ Fechar ]`, diálogo expandido fluido (min 320px, max 480px), orb 240px e backdrop escuro imersivo de 100vmax.
- **Desacoplamento Desktop vs Mobile:** Regras mantidas estritamente segregadas entre `dashboard/css/desktop.css` e `dashboard/css/mobile.css`, com blindagem contra overflow horizontal (`overflow-x: hidden !important`).

### 6.3. DevSecOps: Controle de Acesso por PIN & Modo Demonstração (LGPD Safe)
- **Inicialização 100% Protegida:** Por padrão, o painel inicializa servindo exclusivamente dados simulados (LGPD Safe).
- **Desbloqueio Administrativo por PIN:** A alternância para dados reais exige autenticação via modal com validação segura (variável `ADMIN_PIN`).
- **Sincronização com Motor de Voz:** O motor de síntese vocal transita autonomamente entre respostas reais do H2 e dados sintetizados do Modo Demo.

---

## Seção 7 — Esteira de Carreira 360° em 3 Trilhas Especializadas

A esteira de carreiras do ecossistema é segmentada com separação estrita de links e padrões de documentos:
1. 💻 **Trilha Tech & Dev:** Foco em Java 21, Spring Boot 3, Clean Architecture e Cloud. Currículos Harvard Tech ATS (`Curriculo_Fabio_Rodrigues_Java_Backend.pdf`), cartas timbradas em PDF/DOCX e links do LinkedIn e GitHub.
2. 🎬 **Trilha Audiovisual & Filmmaker:** Foco em direção, edição, motion design e sound design (Final Cut Pro, DaVinci Resolve, Apple Silicon M1). Dossiê de portfólio visual com cases reais e Google Drive exclusivo (**Sem LinkedIn**).
3. 📋 **Trilha Suporte, Operações & Administrativo:** Foco em suporte a sistemas SaaS/ERP, validação documental ICP-Brasil, Customer Experience (CX) e gestão de CRM. Currículos dedicados (`Curriculo_Fabio_Rodrigues_Suporte_TI.pdf`) e LinkedIn oficial.

---

## Seção 8 — Links Oficiais & Acessos do Ecossistema

- **Repositório Oficial no GitHub:** [https://github.com/fabiorodrigues-tech-dev/NOVA](https://github.com/fabiorodrigues-tech-dev/NOVA)
- **Perfil Profissional no LinkedIn:** [https://linkedin.com/in/fabiorodrigues-dev](https://linkedin.com/in/fabiorodrigues-dev)
- **NOVA Control Center (Produção Nuvem Live):** [https://nova-control-center-alsl.onrender.com](https://nova-control-center-alsl.onrender.com)
- **Acesso Local Unificado:** `http://localhost:3000` (via `./start-all.sh`)

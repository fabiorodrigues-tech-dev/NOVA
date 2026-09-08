# Manual de Engenharia & Arquitetura de Software — Ecossistema NOVA

**Autor:** Fábio Rodrigues (Recife/PE)  
**Stack Core:** Java 21 LTS, Spring Boot 3.3.3, Clean Architecture (Ports & Adapters), Spring AI MCP, H2 Database (ACID), Python 3.11, Voice AI, Material 3 Expressive, Docker, GitHub Actions, Render Cloud.  
**Repositório Oficial:** https://github.com/fabiorodrigues-tech-dev/NOVA  
**Perfil Profissional:** https://linkedin.com/in/fabiorodrigues-dev  
**Ambiente de Produção (Live):** https://nova-control-center-alsl.onrender.com  

---

## Sumário Executivo

O **NOVA** é um ecossistema multi-agente pessoal e profissional orientado a microsserviços e inteligência artificial autônoma. Desenvolvido sob rigorosos princípios de **Clean Architecture**, **SOLID** e **DevSecOps**, o sistema atua como copiloto de engenharia de software, esteira automatizada de carreiras 360°, inteligência preditiva financeira com parser bancário OFX e síntese de voz neural em alta fidelidade. O ecossistema está 100% conteinerizado (Docker Multi-Stage), conta com suíte de 40 testes automatizados (100% Green), esteira de CI/CD automatizada via GitHub Actions e painel executivo NOVA Control Center em SPA com 7 abas dedicadas.

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
│   ├── dto/                 # Records imutáveis de entrada/saída (TransacaoRequest, ProjecaoResponse)
│   └── usecase/             # Lógica de negócio (Cadastrar, Listar, Projeção, OFX Parser, Caixinhas)
│
└── infrastructure/          # [CAMADA DE ADAPTADORES & FRAMEWORKS]
    ├── persistence/         # Adaptadores JPA, Entidades de Banco, Mappers bidirecionais
    ├── web/                 # Controllers REST (RFC 7807) e Exception Handler Global
    ├── mcp/                 # Tools corporativas Spring AI Model Context Protocol (@Tool)
    └── config/              # Configurações de Beans e contexto Spring
```

### 1.2. Princípios SOLID Aplicados
- **Single Responsibility Principle (SRP):** Cada Use Case possui uma única razão para mudar (`CalcularProjecaoFinanceiraUseCase` foca estritamente no algoritmo preditivo; `ImportarExtratoOfxUseCase` foca na ingestão e deduplicação).
- **Open/Closed Principle (OCP):** Novos formatos de importação ou novos adaptadores de persistência são adicionados via implementação de interfaces sem alterar as regras de domínio existentes.
- **Liskov Substitution Principle (LSP):** As implementações JPA em `infrastructure.persistence` respeitam integralmente os contratos definidos nas interfaces do domínio.
- **Interface Segregation Principle (ISP):** Interfaces granulares e focadas, evitando que adaptadores dependam de métodos que não utilizam.
- **Dependency Inversion Principle (DIP):** O domínio não conhece o Spring nem o JPA. A injeção de dependência ocorre das camadas externas para as internas através de construtores com tipagem forte.

### 1.3. Tratamento Global de Erros (RFC 7807 ProblemDetail)
O sistema implementa tratamento unificado de exceções via `@RestControllerAdvice` e `GlobalExceptionHandler`, emitindo payloads padronizados com timestamp, status HTTP semântico, detalhamento do erro e URI canônica para observabilidade corporativa.

---

## Seção 2 — Casos de Uso Avançados, Parser OFX & Inteligência Preditiva (Fase 9)

### 2.1. Ingestão Bancária: `ImportarExtratoOfxUseCase`
O caso de uso de importação bancária realiza a leitura automatizada de extratos bancários em formato `.ofx` e `.csv` do Nubank localizados na pasta `financeiro/extratos_ofx/`:
- **Parser SGML/XML Robusto:** Extração estruturada de nós `<STMTTRN>`, `<TRNAMT>`, `<MEMO>`, `<DTPOSTED>` e `<FITID>`.
- **Classificação Categórica Semântica:** Mapeamento de despesas e receitas em categorias canônicas (`ALIMENTACAO`, `MORADIA`, `TRANSPORTE`, `SAUDE`, `LAZER`, `INVESTIMENTO`, `OUTROS`).
- **Deduplicação Transacional no H2:** Mecanismo de hashing e verificação temporal para evitar duplicidade de lançamentos no banco ACID.

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

### 2.3. Gestão de Caixinhas Nubank & Patrimônio Líquido Total
- Suporte a múltiplas Caixinhas temáticas com persistência transacional (Reserva de Emergência, Reserva Casal, Viagem).
- Endpoint REST `/api/caixinhas` para consulta e aportes.
- Cálculo automático de **Patrimônio Líquido Consolidado** somando saldo em conta corrente H2 e ativos alocados nas Caixinhas.

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

### 4.1. Pirâmide de Testes Automatizados (40/40 JUnit 5 + Mockito)
A suíte conta com **40 testes automatizados** executados e aprovados com 100% de sucesso via `./run-tests.sh`:
- **Testes Unitários de Casos de Uso (100% Isolados):**
  - `ImportarExtratoOfxUseCaseTest`
  - `CalcularProjecaoFinanceiraUseCaseTest`
  - `CalcularResumoFinanceiroUseCaseTest`
  - `SalvarCaixinhaUseCaseTest`
  - `ListarCaixinhasUseCaseTest`
  - `ProcessarNotificacaoNubankUseCaseTest`
  - `ProcessarComandoVozUseCaseTest`
- **Testes de Integração WebMvc:**
  - `TransacaoControllerTest`: Validação de requisições mock HTTP, códigos de status e payloads RFC 7807.
  - `CaixinhaControllerTest`: Validação de endpoints de saldo e movimentação de caixinhas.
- **Testes de Ferramentas Spring AI MCP:**
  - `FinanceiroMcpToolsTest`: Validação das chamadas `@Tool` determinísticas.

### 4.2. Pipeline de Integração Contínua (`.github/workflows/ci.yml`)
Esteira automatizada executando em containers Ubuntu a cada push na branch `main`:
- **Job 1 (Java 21 & Maven):** Setup JDK 21 Temurin, compilação de classes e execução da suíte completa de testes com publicação de relatórios Surefire.
- **Job 2 (Python Quality & Voice Check):** Verificação de sintaxe estática (Flake8), compilação de scripts e validação de compatibilidade headless.

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

## Seção 6 — Frontend SPA com 7 Abas & DevSecOps (LGPD Safe)

### 6.1. Matriz de Abas Dedicadas (SPA View Switcher)
O **NOVA Control Center** opera como uma Single Page Application sem recarregamento, estruturado em 7 módulos:
1. **Cockpit Dashboard:** Visão executiva consolidada, Voice Assistant interativo, KPIs corporativos e Living Shader WebGL.
2. **Finanças & Preditivo H2:** Balanço patrimonial, auditoria de despesas, burn rate diário, projeção de fechamento e caixinhas.
3. **Candidaturas 360°:** Rastreamento de vagas ativas, índices de aderência técnica (Match %), filtros por trilha e downloads de dossiês.
4. **Estudos & Certificações:** Monitoramento de trilhas ativas (Santander 2026 DIO 26/26 com Certificado e Full Stack Cloud DevOps 5/5).
5. **Voice Studio Pro:** Laboratório de síntese vocal neural, catálogo de vozes PT-BR/globais e testes executivos.
6. **Engenharia & Testes:** Telemetria dos microsserviços, Clean Architecture 4 Camadas, persistência H2 ACID e suíte de testes 100% OK.
7. **Spring Boot API Explorer:** Painel interno de contratos REST, 5 endpoints mapeados, visualizador interativo de payloads JSON e RFC 7807.

### 6.2. DevSecOps: Controle de Acesso por PIN & Modo Demonstração (LGPD Safe)
- **Inicialização 100% Protegida:** Por padrão, o painel inicializa servindo exclusivamente dados simulados (LGPD Safe).
- **Desbloqueio Administrativo por PIN:** A alternância para dados reais exige autenticação via modal com chave de acesso segura (configurável via variável de ambiente `ADMIN_PIN`).
- **Sincronização com Motor de Voz:** O motor de síntese vocal respeita instantaneamente o estado de autenticação, nunca vazando valores bancários reais em Modo Demonstração.

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

# 🌌 NOVA — Sistema Multi-Agente Pessoal & Profissional

[![NOVA CI/CD](https://github.com/fabiorodrigues-tech-dev/NOVA/actions/workflows/ci.yml/badge.svg)](https://github.com/fabiorodrigues-tech-dev/NOVA/actions)
![Java 21](https://img.shields.io/badge/Java-21-ED8B00?style=flat&logo=openjdk&logoColor=white)
![Spring Boot 3](https://img.shields.io/badge/Spring%20Boot-3.3.3-6DB33F?style=flat&logo=springboot&logoColor=white)
![Spring AI MCP](https://img.shields.io/badge/Spring%20AI-MCP%20Tools-007ACC?style=flat&logo=spring&logoColor=white)
![JUnit 5](https://img.shields.io/badge/JUnit%205-40%20Tests%20Passed-25A162?style=flat&logo=junit5&logoColor=white)
![Material 3](https://img.shields.io/badge/Design%20System-Material%203%20Expressive-4285F4?style=flat&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Multi--Stage-2496ED?style=flat&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-24%2F7%20Cloud-46E3B7?style=flat&logo=render&logoColor=black)

> **Enterprise-Grade Multi-Agent Copilot & Autonomous Engineering Ecosystem**  
> Desenvolvido por **Fábio Rodrigues** (Recife/PE) | [LinkedIn](https://linkedin.com/in/fabiorodrigues-dev) • [GitHub](https://github.com/fabiorodrigues-tech-dev/NOVA)

O **NOVA** é um ecossistema multi-agente pessoal e profissional orientado a microsserviços, inteligência artificial autônoma e engenharia de software de alta performance. Desenvolvido sob rigorosos princípios de **Clean Architecture (Ports & Adapters)**, **SOLID** e **DevSecOps**, o sistema integra o **Gemini via Google Antigravity**, microsserviço **Java 21 / Spring Boot 3.3.3**, protocolo **Spring AI Model Context Protocol (MCP)**, camada de **Voz Neural Humana** de baixa latência e o **NOVA Control Center** (Dashboard Executivo com Material 3 Expressive, Living Shader WebGL e Sistema de Privacidade LGPD).

---

## 📄 Destaques de Arquitetura & Documentação Oficial
Consulte os documentos executivos em PDF com pareceres de engenharia, diagramas e evidências de qualidade:
- 📑 **[Manual de Engenharia & Arquitetura (PDF Completo)](docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf)**: Manual com especificação de camadas, RFC 7807, ferramentas `@Tool` MCP, pirâmide de testes e fórmulas preditivas.
- 🏆 **[Dossiê Técnico Master (PDF)](docs/dossie_tecnico_nova.pdf)**: Relatório executivo consolidado para avaliação por Tech Leads e Arquitetos de Software.

---

## 🧭 NOVA Control Center (UI Showcase & Production Preview)

O **NOVA Control Center** é o painel de comando unificado do ecossistema, combinando Bento Grid modular, WebGL Living Shader, telemetria em tempo real via Chart.js, Voice Orb interativo e **Sistema de Privacidade Inteligente (Demo Mode)** com suporte a túnel público HTTPS seguro.

Acesse localmente em **[http://nova.local:3000](http://nova.local:3000)** (ou **[https://nova-control-center-al5l.onrender.com](https://nova-control-center-al5l.onrender.com)**) ou via comando `/dashboard`.

| ☀️ Modo Dia (Light Theme) | 🌙 Modo Noite (Dark Theme) |
| :---: | :---: |
| <img src="docs/assets/nova-light-preview.png" width="100%" alt="NOVA Control Center - Light Theme"> | <img src="docs/assets/nova-dark-preview.png" width="100%" alt="NOVA Control Center - Dark Theme"> |
| **Light Theme:** Máxima legibilidade com superfície tonal M3 Expressive, contraste WCAG AAA e visual limpo para foco diurno. | **Dark Theme:** Glassmorphism profundo, Living Shader WebGL reativo, chips vibrantes e conforto visual para imersão noturna. |

---

## 👥 Mapeamento Oficial dos 4 Agentes Especialistas (`.agents/skills/`)

```mermaid
flowchart TD
    subgraph UI_Layer ["🖥️ Interfaces & Acesso"]
        DASH["🧭 NOVA Control Center (Produção Cloud (https://nova-control-center-al5l.onrender.com) / nova.local)"]
        VOICE_UI["🎙️ Voice Studio Web (Porta 5050)"]
        CLI["⚡ Chat & CLI (Atalhos / e !)"]
        TUNNEL["🌐 Túnel Público Seguro (/compartilhar)"]
    end

    subgraph Core_Agent ["🤖 MAIN Agent (NOVA Orchestrator)"]
        ROUTER{"⚡ Roteador & Triagem Inteligente"}
    end

    subgraph Specialized_Agents ["👥 4 Agentes Especialistas"]
        FINANCEIRO["💰 Agente Financeiro\n(Java 21 / H2 ACID / OFX / Projeção)"]
        CARREIRA["💼 Agente Carreira & Operações\n(Esteira 360° Tech & Audiovisual)"]
        CODIGO["💻 Agente Código\n(Clean Architecture / Scaffolding / JUnit 5)"]
        ESTUDOS["📚 Agente Estudos\n(Trilha Santander DIO / Método Feynman)"]
    end

    subgraph Backend_Services ["☕ Microsserviços & Ferramentas"]
        SPRING["☕ Spring Boot 3.3.3 API (Porta 8081)\n• Clean Architecture (Ports & Adapters)\n• ProblemDetail (RFC 7807)\n• Parser OFX/CSV Nubank"]
        MCP["🔌 Spring AI Model Context Protocol\n• @Tool cadastrar_transacao\n• @Tool consultar_projecao\n• @Tool atualizar_caixinha"]
        H2[("💾 Banco H2 Persistente\n(financiadb.mv.db)")]
        CHART["📊 Motor Gráfico Matplotlib\n(chart_engine.py)"]
        TTS["🎙️ Bridge Neural Voice\n(edge-tts + afplay)"]
    end

    UI_Layer --> ROUTER
    TUNNEL --> DASH
    ROUTER --> FINANCEIRO
    ROUTER --> CARREIRA
    ROUTER --> CODIGO
    ROUTER --> ESTUDOS

    FINANCEIRO --> MCP
    MCP --> SPRING
    SPRING --> H2
    CARREIRA --> CHART
    VOICE_UI --> TTS
    DASH --> SPRING
```

1. 💰 **Agente Financeiro (`agente-financeiro`):**
   - Microsserviço Java 21 / Spring Boot 3 na porta `8081` com persistência H2 ACID (`financiadb.mv.db`).
   - Parser nativo de extratos `.ofx` e `.csv` do Nubank com deduplicação semântica.
   - Gestão de Caixinhas Nubank (Reserva e Casal) com recálculo automático de Patrimônio Líquido Total.
   - Inteligência Preditiva (Fase 9): Cálculo em tempo real de **Burn Rate Diário**, saldo projetado de fechamento e alertas orçamentários.
   - Ferramentas `@Tool` expostas via **Spring AI Model Context Protocol (MCP)**.

2. 💼 **Agente de Carreira & Operações (`agente-carreira-e-operacoes`):**
   - Gestão da esteira **"Candidatura Completa 360°"** com separação estrita de 2 trilhas profissionais:
     - 💻 **Trilha Tech & Dev:** Currículos Harvard Tech ATS, cartas timbradas em PDF/DOCX e link do LinkedIn oficial.
     - 🎬 **Trilha Marketing & Audiovisual:** Portfólio Google Drive, cases reais (DER-PE, Gildo Lanches, Quintal dos Primos) e setup Apple Silicon M1.
   - Mapeamento de vagas ativas com índices de aderência técnica (Match %) e relatórios gráficos executivos.

3. 💻 **Agente de Código (`agente-codigo`):**
   - Engenharia Back-end em Java 21 LTS e ecossistema Spring Boot 3.3.3.
   - Ferramenta de scaffolding automático Clean Architecture (`scripts/scaffold_feature.py`).
   - Guia de Code Review formal e suíte de testes automatizados JUnit 5, Mockito e AssertJ.

4. 📚 **Agente de Estudos (`agente-estudos`):**
   - Acompanhamento diário da **Trilha Santander 2026 - AI Java Back-end (DIO)**.
   - Aplicação de metodologias ativas: Técnica Feynman, Active Recall, Flashcards e desafios práticos orientados a testes.

---

## ⚡ Central de Atalhos Rápidos (`/` e `!`)
Consulte o catálogo completo em [`COMANDOS.md`](file:///Users/fabioandre/Downloads/nova:/COMANDOS.md):

- 🧭 **Central & Acesso:** `/dashboard` (ou `/painel`), `/compartilhar` (ou `/share`), `/atalhos` (ou `!atalhos`), `/menu`, `/ajuda`, `/status`, `/reverter`.
- 💼 **Carreira 360°:** `/candidatura [link]`, `/vagas`, `/pitch [empresa]`, `/cv`.
- 📚 **Estudos (DIO):** `/estudos`, `/feynman [tópico]`, `/desafio [tema]`, `/manual`.
- 💰 **Finanças:** `/saldo`, `/caixinhas`, `/extrato`, `/gastos [categoria]`, `/financeiro [mês]`.
- 💻 **Código & Qualidade:** `/testes`, `/review [arquivo]`, `/scaffold [Feature]`.
- 🗂️ **Operações & Foco:** `/dia`, `/semana`, `/foco`.
- 🎙️ **Voz & Studio:** `/studio`, `/voz`, `/voz [nome]`.

---

## 🚀 Guia de Inicialização Rápida

### 1. Pré-requisitos
- **Java:** JDK 21 LTS instalado
- **Python:** Python 3.10+
- **Maven:** 3.9+
- **macOS / Linux**

### 2. Inicialização Unificada de Todos os Microsserviços
Execute o script orquestrador na raiz do projeto:
```bash
./start-all.sh
```

| Serviço | Módulo / Tecnologia | Porta | Endpoint / Acesso |
| :--- | :--- | :---: | :--- |
| **NOVA Control Center** | Material 3 Expressive / Bento Grid / Chart.js | `3000` | **[http://nova.local:3000](http://nova.local:3000)** |
| **Agente Financeiro API** | Java 21 / Spring Boot 3.3.3 / Spring AI MCP | `8081` | **[http://localhost:8081/api/transacoes/resumo](http://localhost:8081/api/transacoes/resumo)** |
| **NOVA Voice Studio** | Python / `edge-tts` / `afplay` | `5050` | **[http://localhost:5050](http://localhost:5050)** |

### 3. Compartilhamento Seguro (Demo Mode Público)
Para gerar uma URL HTTPS pública para smartphone ou recrutadores com dados fictícios (LGPD Safe):
```bash
python3 dashboard/compartilhar.py
# Ou digite /compartilhar no chat
```

### 4. Execução da Suíte de Testes JUnit 5
```bash
./java-services/agente-financeiro/run-tests.sh
```

### 5. Parada Segura dos Serviços
```bash
./stop-all.sh
```

---

## ☁️ Deploy em Nuvem 24/7 (Docker & Render)

O ecossistema NOVA está totalmente conteinerizado e pronto para execução em nuvem 24/7 através de imagem multi-stage (`Dockerfile`) e blueprint do Render (`render.yaml`).

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/fabiorodrigues-tech-dev/NOVA)

### 🐳 Execução Local com Docker
```bash
# 1. Construir a imagem Docker
docker build -t nova-control-center .

# 2. Executar o container em background (Porta 10000)
docker run -d -p 10000:10000 --name nova-app nova-control-center

# 3. Acessar o Dashboard
open http://localhost:10000
```

### 🌐 Deploy Automático no Render
1. Conecte sua conta do [Render](https://render.com) ao repositório GitHub `fabiorodrigues-tech-dev/NOVA`.
2. O Render detectará automaticamente o arquivo [`render.yaml`](file:///Users/fabioandre/Downloads/nova:/render.yaml).
3. O serviço web será construído e inicializado na nuvem com healthcheck ativo em `/api/status?demo=true`.

---

## 🧪 Relatório Oficial da Suíte de Testes Automatizados (100% Green)

```text
==========================================
📊 RELATÓRIO DE EXECUÇÃO DE TESTES (NOVA)
==========================================
Total de Testes Encontrados: 40
✅ Testes que Passaram:      40
❌ Testes que Falharam:      0
⏭️ Testes Ignorados:         0
⏱️ Tempo Total de Execução:  1981ms
==========================================
🎉 TODOS OS TESTES PASSARAM COM SUCESSO! (100% GREEN)
```

- **Use Cases Unitários:** `ImportarExtratoOfxUseCaseTest`, `CalcularProjecaoFinanceiraUseCaseTest`, `CalcularResumoFinanceiroUseCaseTest`, `SalvarCaixinhaUseCaseTest`, `ListarCaixinhasUseCaseTest`, `ProcessarNotificacaoNubankUseCaseTest`, `ProcessarComandoVozUseCaseTest`.
- **Integração WebMvc:** `TransacaoControllerTest`, `CaixinhaControllerTest`.
- **Spring AI MCP Tools:** `FinanceiroMcpToolsTest` (@Tool determinísticas).

---

## 🛡️ Governança, Segurança & DevSecOps (LGPD)

- **Anonimização & Mocks Corporativos:** Todos os assets de preview, relatórios públicos e acessos via túnel utilizam datasets fictícios corporativos (`[DADOS SANITIZADOS / MOCK LGPD]`).
- **Isolamento no `.gitignore`:** Extratos bancários reais (`.ofx`, `.csv`), comprovantes (`.HEIC`), relatórios confidenciais (`.pdf`) e bancos de dados H2 locais (`*.mv.db`) estão blindados de qualquer sincronização com o repositório público.
- **Pipeline de Integração Contínua (`.github/workflows/ci.yml`):** Validação automatizada em containers Linux (Java 21, Python 3.11 e Docker Multi-Stage Build) a cada push na branch `main`.

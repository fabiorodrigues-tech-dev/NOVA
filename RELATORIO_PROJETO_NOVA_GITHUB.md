# 🌌 BRIEFING TÉCNICO & GUIA DE DEPLOY GITHUB — PROJETO NOVA

> **Documento de Contexto para LLM / Gemini / Claude / Pair Programming**  
> **Data de Emissão:** 27 de Agosto de 2026  
> **Versão do Ecossistema:** NOVA Ecosystem v3.5 (Clean Architecture, Voice AI & Predictive Finance)  
> **Repositório GitHub Oficial:** `https://github.com/fabiorodrigues-tech-dev/NOVA.git`  
> **Branch Principal:** `main`  
> **Status dos Testes:** 40/40 Testes JUnit 5 Passando (100% de Sucesso)

---

## 🎯 1. Visão Geral do Projeto NOVA

O **NOVA** é um ecossistema multi-agente pessoal e profissional que atua como copiloto central de engenharia de software, estudos técnicos, esteira de carreiras 360° e controlador financeiro com inteligência preditiva.

### 🏗️ Stack Tecnológica Consolidada:
- **Back-end Core:** Java 21 LTS, Spring Boot 3.3.3, Spring Data JPA, Spring AI (Model Context Protocol - MCP).
- **Banco de Dados:** H2 Database persistente em arquivo local (`./data/financiadb.mv.db`) com integridade transacional ACID.
- **Camada de Inteligência:** Google Gemini API via Antigravity, Spring AI MCP Tools (`@Tool`), Python Voice Studio com `edge-tts` (Voz Francisca Neural PT-BR).
- **Frontend / Dashboard:** NOVA Control Center (Porta 3000) construído em HTML5 Semântico, CSS3 com Design System Material 3 Expressive, WebGL Living Shader, Bento Grid modular e gráficos Chart.js em tempo real.
- **DevOps & Automação:** GitHub Actions CI/CD (`.github/workflows/ci.yml`), scripts de automação (`start-all.sh`, `stop-all.sh`, `./run-tests.sh`).

---

## 🗺️ 2. Status do Roadmap de Desenvolvimento (9 Fases 100% Concluídas)

| Fase | Módulo / Funcionalidade | Status | Principais Tecnologias & Entregas |
| :--- | :--- | :---: | :--- |
| **Fase 1** | Arquitetura Base & Scaffolding Multi-Agente | ✅ **100%** | Setup das skills `.agents/skills/`, regras no `AGENTS.md` e catalisadores |
| **Fase 2** | Back-end Java 21 / Spring Boot 3 | ✅ **100%** | Clean Architecture (Domain, UseCases, Ports & Adapters, H2 persistente) |
| **Fase 3** | Spring AI & Model Context Protocol (MCP) | ✅ **100%** | Ferramentas `@Tool` expostas para orquestração direta por LLMs |
| **Fase 4** | Esteira de Candidaturas 360° | ✅ **100%** | Segregação Tech/Dev (LinkedIn) vs Marketing (Drive), PDFs Harvard Tech |
| **Fase 5** | Motor de Gráficos & Relatórios Visuais | ✅ **100%** | `chart_engine.py` (Matplotlib), Relatórios Financeiros e Match de Vagas |
| **Fase 6** | Interface de Voz Neural Humana (Voice AI) | ✅ **100%** | `edge-tts` + `afplay`, Voice Studio Web na porta 5050 |
| **Fase 7** | NOVA Control Center (Dashboard Visual M3) | ✅ **100%** | Bento Grid, Living Shader WebGL, Material 3 Expressive na porta 3000 |
| **Fase 8** | CI/CD GitHub Actions & Importador OFX | ✅ **100%** | Parser OFX/CSV Nubank, deduplicação automática no banco H2 |
| **Fase 9** | Inteligência Preditiva & Caixinhas Nubank | ✅ **100%** | Burn Rate Diário, Projeção de Fechamento, Caixinhas e Webhook Nubank |

---

## 📁 3. Estrutura de Diretórios do Repositório

```text
nova/
├── .github/
│   └── workflows/
│       └── ci.yml                   # CI/CD automatizado no GitHub Actions (Java 21 + Maven)
│
├── .agents/
│   └── skills/
│       ├── agente-codigo/           # 💻 Java 21, Spring Boot 3, Clean Architecture, Scaffolding
│       ├── agente-estudos/          # 📚 Trilha Santander 2026 DIO, Metodologia Feynman, Flashcards
│       ├── agente-carreira-e-operacoes/ # 💼 Gestão 360° de Vagas (Tech e Audiovisual), Pitches LinkedIn
│       └── agente-financeiro/       # 💰 Gestão Orçamentária, Projeções Preditivas e Caixinhas
│
├── carreira/                        # 💼 Esteiras de Candidaturas 360°
│   ├── base/                        # Currículos mestres (dev e marketing) e dados de portfólio
│   └── vagas_analisadas/            # Pastas dedicadas por empresa (Capgemini, Gummy, RIO AVE, Luck)
│
├── dashboard/                       # 🧭 NOVA Control Center (Porta 3000)
│   ├── index.html                   # Interface Web com Material 3 Expressive e Bento Grid
│   ├── app.js                       # Lógica de telemetria, gráficos Chart.js e Voice Orb
│   ├── styles.css                   # Design Tokens M3 Expressive, Glassmorphism profundo
│   └── server.py                    # Gateway HTTP em Python com rotas REST e proxy reverso
│
├── estudos/                         # 📚 Trilha Santander 2026 DIO & Manuais Técnicos
│   ├── trilha_tracker.md            # Acompanhamento detalhado módulo a módulo
│   └── guia_estudos_nova/           # Dossiê e Manual de Engenharia e Arquitetura em PDF
│
├── financeiro/                      # 💰 Módulo Financeiro Consolidado
│   ├── extratos_ofx/                # 8 extratos bancários .ofx reais do Nubank (Jan a Ago/2026)
│   ├── investimentos_caixinhas/     # Comprovantes e saldos de Caixinhas (Reserva e Casal)
│   └── relatorios_pdf/              # Relatórios executivos em PDF compilados
│
├── java-services/
│   └── agente-financeiro/           # ☕ Microsserviço Java 21 / Spring Boot 3
│       ├── src/main/java/com/nova/agentefinanceiro/
│       │   ├── application/         # DTOs e Use Cases (Projeção, Caixinhas, OFX, Webhook)
│       │   ├── domain/              # Modelos ricos de domínio e contratos de repositório
│       │   └── infrastructure/      # Adaptadores JPA, Controllers REST e Tools MCP
│       ├── src/test/java/           # Suíte de 40 testes unitários e de integração JUnit 5
│       ├── data/financiadb.mv.db    # Banco de dados H2 persistente
│       └── run-tests.sh             # Script de execução rápida de testes (100% Passing)
│
├── scripts/                         # 📊 Scripts Python (Chart Engine, Geradores PDF)
├── voz/                             # 🎙️ Voice Studio Web (Porta 5050) & Configuração TTS
├── AGENTS.md                        # Regras centrais de orquestração do MAIN Agent
├── COMANDOS.md                      # Catálogo completo de atalhos rápidos (/ e !)
├── nova-status.md                   # Relatório de status e telemetria operacional
├── start-all.sh                     # Inicializador simultâneo de todos os microsserviços
├── stop-all.sh                      # Encerrador seguro de portas locais
└── README.md                        # Documentação oficial do projeto
```

---

## ⚡ 4. Diagnóstico do Git Local

- **Diretório Raiz:** `/Users/fabioandre/Downloads/nova`
- **Branch Ativa:** `main`
- **Remote Origin Atual:** `https://github.com/fabiorodrigues-tech-dev/NOVA.git`
- **Status da Árvore:** Working tree limpa (todas as 9 fases e modificações estão comitadas localmente).
- **Últimos Commits:**
  1. `98276a1` - `feat: initial commit with structural architecture and core features`
  2. `a495860` - `docs: registrar mapeamento flexível de aliases para autonomia full access e reversão rollback`
  3. `5005f34` - `feat: Fase 9 concluída - Inteligência Preditiva, Projeção Financeira H2, Checkpoint System & Full Access Mode`

---

## 🚀 5. Instruções Passo a Passo para Subir no GitHub

Caso o Gemini vá auxiliar na publicação ou sincronização com o GitHub, siga o roteiro abaixo:

### Cenário A: O repositório remoto no GitHub está vazio (Criado sem README/Licença)
Basta executar o push direto da branch `main`:
```bash
# 1. Garantir que a URL do remote está correta
git remote set-url origin https://github.com/fabiorodrigues-tech-dev/NOVA.git

# 2. Enviar a branch main com rastreamento upstream
git push -u origin main
```

### Cenário B: O repositório remoto já possui um README ou commit inicial gerado pelo GitHub
Se o GitHub recusar o push com erro `[rejected - non-fast-forward]`, sincronize ou force a atualização inicial:
```bash
# Opção 1: Mesclar histórico remoto permitindo históricos não relacionados
git pull origin main --allow-unrelated-histories --no-rebase
git push -u origin main

# Opção 2: Sobrescrever o repositório remoto com a versão completa local (Recomendado para primeiro commit)
git push -u origin main --force
```

### Cenário C: Autenticação via GitHub CLI (`gh`) ou Token de Acesso Pessoal (PAT)
Se houver solicitação de credenciais (devido à descontinuação de senhas puras pelo GitHub):
1. **Via GitHub CLI (Mais rápido):**
   ```bash
   gh auth login
   # Selecione GitHub.com -> HTTPS -> Login with a web browser
   git push -u origin main
   ```
2. **Via Personal Access Token (PAT):**
   - Acesse: `GitHub -> Settings -> Developer Settings -> Personal access tokens (classic)`.
   - Gere um token com permissão `repo`.
   - Utilize a URL com token embutido ou informe o token no prompt de senha:
   ```bash
   git remote set-url origin https://<SEU_TOKEN_GITHUB>@github.com/fabiorodrigues-tech-dev/NOVA.git
   git push -u origin main
   ```
3. **Via Chave SSH (Opcional):**
   ```bash
   git remote set-url origin git@github.com:fabiorodrigues-tech-dev/NOVA.git
   git push -u origin main
   ```

---

## 🛡️ 6. Regras de Ouro e Diretrizes do Projeto
1. **Fidelidade Rigorosa às Bases Oficiais:** Nenhuma vaga pode inventar habilidades fora dos currículos base.
2. **Segregação de Trilhas:** TI/Dev usa link do LinkedIn; Audiovisual/Marketing usa Google Drive.
3. **Clean Architecture & SOLID:** Toda nova funcionalidade segue estritamente Domain -> Use Cases -> Ports/Adapters -> Infrastructure.
4. **Qualidade Contínua:** Antes de qualquer entrega, validar 100% dos testes JUnit 5 via `./run-tests.sh`.

# 📍 NOVA — Status do Projeto (v3.5 - 100% Completo)

> Documento oficial de estado consolidado do ecossistema NOVA. Reflete a conclusão integral de **todas as 9 Fases do Roadmap**, com Inteligência Preditiva & Consultoria Financeira, CI/CD GitHub Actions, Importador OFX/CSV, Voice AI Neural, Dashboard Material 3 Expressive e Clean Architecture.

**Última atualização:** 27/08/2026  
**Ecossistema:** Java 21, Spring Boot 3.3.3, Spring AI (MCP), Python, Antigravity, Apple Silicon M1  
**Maturidade Geral:** 100% Operacional & Homologado (27 Testes JUnit 5 Passando)

---

## 1. Tabela das 9 Fases do Roadmap (100% Concluídas)

| Fase | Título | Status | Entregas & Componentes Chave |
|---|---|---|---|
| **Fase 1** | Arquitetura Multi-Agente & Orquestração | ✅ **100% Concluído** | MAIN Agent + 4 Agentes Especialistas em `.agents/skills/` |
| **Fase 2** | Back-end Java 21 & Clean Architecture | ✅ **100% Concluído** | Spring Boot 3.3.3, DDD, H2 persistente, Repository Pattern |
| **Fase 3** | Spring AI & Model Context Protocol (MCP) | ✅ **100% Concluído** | Tools `@Tool` expostas para IA (Cadastro, Listagem, Resumo) |
| **Fase 4** | Esteira de Carreira & Candidaturas 360° | ✅ **100% Concluído** | 8 Candidaturas (Tech & Marketing), Harvard Tech ATS PDF, DOCX |
| **Fase 5** | Motor Gráfico & Relatórios Visuais PDF | ✅ **100% Concluído** | `chart_engine.py` (Matplotlib), Relatório Financeiro & Manual DIO |
| **Fase 6** | Camada de Voz Neural Humana (Voice AI) | ✅ **100% Concluído** | `edge-tts` + `afplay` nativo, Voice Studio Web (Porta 5050) |
| **Fase 7** | NOVA Control Center (Dashboard M3) | ✅ **100% Concluído** | Bento Grid, Living Shader WebGL, Material 3 Expressive (Porta 3000) |
| **Fase 8** | CI/CD GitHub Actions & Importador OFX | ✅ **100% Concluído** | `.github/workflows/ci.yml`, Parser OFX/CSV Nubank, Deduplicação H2 |
| **Fase 9** | Inteligência Preditiva & Consultor Financeiro | ✅ **100% Concluído** | Burn Rate Diário, Projeção de Fechamento, Alertas de Risco, Tool MCP |

---

## 2. Serviços Ativos (Portas Locais) & Automação

| Serviço | Tecnologia | Porta | O que faz |
|---|---|---|---|
| **NOVA Control Center** | Python / HTML5 / Material 3 Expressive / Chart.js | `3000` | Dashboard visual unificado (Bento Grid, Living Shader, Projeção Preditiva, Voice Orb, downloads 1-clique) |
| **NOVA Voice Studio** | Python / `edge-tts` / `afplay` | `5050` | Catálogo e teste de vozes neurais PT-BR e globais (Google Store layout) |
| **Agente Financeiro API** | Java 21 / Spring Boot 3 / H2 / Spring AI | `8081` | REST + ferramentas MCP + importador OFX/CSV + Projeção Preditiva + endpoint de voz |

> **🚀 Scripts de Automação:**
> - `start-all.sh`: Inicializa simultaneamente os 3 serviços em background com logs em `logs/`.
> - `stop-all.sh`: Encerra e libera com segurança todas as portas (`8081`, `3000`, `5050`).

---

## 3. O que foi entregue na Fase 9 (Inteligência Preditiva)

- ✅ **Caso de Uso de Projeção Financeira (`CalcularProjecaoFinanceiraUseCase.java`)**:
  - Cálculo de Burn Rate diário médio (`totalGastos / diasDecorridos`).
  - Projeção de despesas adicionais e saldo final no último dia do mês corrente.
  - Classificação de risco: `SAUDAVEL` (Superávit), `ALERTA` (Margem apertada < 15%), `CRITICO` (Risco de déficit).
  - Emissão de alertas acionáveis e recomendações de aportes na reserva de emergência e metas do casal.
- ✅ **MCP Tool & Endpoint REST**:
  - `@Tool(name="projecao_financeira")` no `FinanceiroMcpTools.java`.
  - `GET /api/transacoes/projecao` no `TransacaoController.java`.
- ✅ **Suíte JUnit 5 Expandida**:
  - 27 testes automatizados com 100% de sucesso (`./run-tests.sh`).
- ✅ **Dashboard Visual & Voz Integrados**:
  - Card Bento de Projeção Financeira no NOVA Control Center (Porta 3000).
  - Roteamento de comandos de voz para previsão de saldo falada naturalmente pela Francisca.

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
4. **Segregação de Cabeçalhos por Trilha:** Tech usa LinkedIn; Marketing/Audiovisual usa Google Drive.
5. **Postura Financeira Conservadora:** Organiza, prevê e dá clareza; nunca toma decisões arbitrárias pelo usuário.
6. **Workspace Limpo:** Zero arquivos PNG residuais.

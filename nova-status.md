# 📍 NOVA — Status do Projeto (v3)

> Documento oficial de estado consolidado do ecossistema NOVA. Reflete a entrega da **Fase 8 (CI/CD GitHub Actions & Importador OFX/CSV)** e a reestruturação da arquitetura dos 4 agentes especialistas.

**Última atualização:** 27/08/2026  
**Ecossistema:** Java 21, Spring Boot 3.3.3, Spring AI (MCP), Python, Antigravity, Apple Silicon M1  

---

## 1. Serviços Ativos (Portas Locais) & Automação

| Serviço | Tecnologia | Porta | O que faz |
|---|---|---|---|
| **NOVA Control Center** | Python / HTML5 / Material 3 / Chart.js | `3000` | Dashboard visual (Bento Grid, Living Shader, Voice Orb, downloads 1-clique) |
| **NOVA Voice Studio** | Python / `edge-tts` / `afplay` | `5050` | Teste e síntese de vozes neurais PT-BR e globais (Google Store layout) |
| **Agente Financeiro API** | Java 21 / Spring Boot 3 / H2 / Spring AI | `8081` | REST + ferramentas MCP + importador OFX/CSV + endpoint de voz |

> **🚀 Scripts de Automação:**
> - `start-all.sh`: Inicializa simultaneamente os 3 serviços em background com redirecionamento de logs para `logs/`.
> - `stop-all.sh`: Encerra e libera com segurança todas as portas (`8081`, `3000`, `5050`).

---

## 2. O que mudou na Fase 8 (27/08/2026)

- ✅ **Fase 8 (CI/CD GitHub Actions) Implementada**: Criado `.github/workflows/ci.yml` com pipeline completo de validação do Java 21 (Temurin), compilação Maven, execução automatizada da suíte JUnit 5 e análise estática Python.
- ✅ **Importador de Extrato Nubank (OFX / CSV) no Microsserviço Java**:
  - Criado `ImportarExtratoOfxUseCase.java` com parser flexível para OFX e CSV.
  - Categorização automática inteligente (Transporte, Alimentação, Saúde, Moradia, Lazer, etc.).
  - Deduplicação nativa no banco H2 baseada em tripla `(data, valor, descricao)`.
  - Ferramenta MCP `@Tool(name="importar_extrato_ofx")` e endpoint REST `POST /api/transacoes/importar-ofx`.
- ✅ **Suíte JUnit 5 Expandida**: 21 testes unitários e de integração passando com 100% de sucesso (`./run-tests.sh`).
- ✅ **Reestruturação dos Agentes Especialistas**:
  - `agente-organizacao` evoluído e renomeado para **`agente-carreira-e-operacoes`** (`.agents/skills/agente-carreira-e-operacoes/`), unificando o gerenciamento da esteira 360° (Tech & Dev + Marketing & Audiovisual), follow-ups de recrutadores no LinkedIn, controle de prazos e notas diárias.
- ✅ **Candidaturas 360° Mapeadas (8 empresas)**: Gummy (96%), RIO AVE (95%), Aposta Ganha (94%), Grupo Luck (92%), Capgemini (92%), Accenture (88%), Deloitte (86%), FullStack (68%).

---

## 3. Estrutura dos 4 Agentes Especialistas (`.agents/skills/`)

```text
.agents/skills/
├── agente-codigo/                 # 💻 Especialista Java 21 / Spring Boot 3 / Clean Architecture / Scaffolding
├── agente-estudos/                # 📚 Especialista Trilha Santander 2026 DIO / Metodologias ativas / Feynman
├── agente-carreira-e-operacoes/   # 💼 Especialista em Candidaturas 360°, Follow-ups LinkedIn e Rotinas Operacionais
└── agente-financeiro/             # 💰 Especialista em Gestão Orçamentária, MCP Tools e Conciliação OFX/CSV
```

---

## 4. Estado por Domínio

| Domínio | Nível de Maturidade | Observação |
|---|---|---|
| 💰 Financeiro | **Produção real (v2)** | Java 21 + MCP + H2 persistente + Importador OFX/CSV + 21 testes JUnit 5 |
| 🔄 CI/CD | **Produção real** | GitHub Actions Pipeline (`.github/workflows/ci.yml`) validando builds Java e Python |
| 🎙️ Voz | **Serviço real funcionando** | Síntese neural PT-BR ativa, Voice Studio Google Store layout (Porta 5050) |
| 🧭 Dashboard | **Serviço real funcionando** | NOVA Control Center com Material 3 Expressive, Living Shader e Bento Grid |
| 💼 Carreira & Operações | **Esteira automatizada ativa** | 8 candidaturas geradas, follow-ups no LinkedIn, Daily Notes e planejamento |
| 📚 Estudos | **Skill + gerador de PDF** | Trilha DIO em andamento (7,7%), gerador do Manual Técnico em PDF |
| 💻 Código | **Skill + scripts CLI** | Scaffolding Clean Architecture e suíte de testes automatizada |
| 👤 Pessoal (`sobre-mim.md`) | **Completo** | Objetivos de carreira, projeto Sofia (Voice AI) e metas financeiras |

---

## 5. Regras de Ouro Permanentes

1. **Fidelidade Rigorosa às Bases Oficiais:** Nenhuma candidatura pode inventar ferramentas fora do CV/portfólio real cadastrado.
2. **Segregação de Cabeçalhos por Trilha:** Tech usa LinkedIn; Marketing/Audiovisual usa portfólio no Google Drive.
3. **Interface Única:** O desenvolvedor interage com uma única inteligência central que orquestra os especialistas.
4. **Postura Financeira Conservadora:** Organiza e dá clareza orçamentária; nunca toma decisões pelo usuário.
5. **Workspace Limpo:** Zero arquivos PNG soltos nas pastas de candidatura ou no repositório.

---

## 6. Próximos Passos (Roadmap)

1. **Submissão das Candidaturas de Marketing:** Enviar pacotes gerados para Gummy, RIO AVE e Aposta Ganha.
2. **Avanço na Trilha Santander DIO:** Concluir o módulo de *Fundamentos da IA Moderna*.
3. **Expansão MCP para Código & Estudos:** Implementar ferramentas MCP para validação Clean Code e sincronização de progresso da DIO.

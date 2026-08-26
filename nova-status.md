# 🧭 NOVA — Status & Estrutura do Ecossistema

Este documento reflete o estado real, atualizado e validado da estrutura de arquivos, serviços e especialidades do ecossistema **NOVA**.

---

## 1. 📊 Status dos Componentes do Workspace

| Componente / Arquivo | Estado | Detalhes & Prontidão |
| :--- | :---: | :--- |
| **[`AGENTS.md`](file:///Users/fabioandre/Downloads/nova:/AGENTS.md)** | 🟢 Ativo | Orquestrador central NOVA, Roteamento de Atalhos (`/` e `!`), Dashboard Control Center e Esteira 360°. |
| **[`dashboard/`](file:///Users/fabioandre/Downloads/nova:/dashboard)** | 🟢 Operacional | **Fase 7 Concluída:** **NOVA Control Center** (Porta `3000`), Assistente de Voz Neural integrado (Base64 + HTML5 Audio + Microfone), Design System Figma Dabang e Lucide Icons. |
| **[`COMANDOS.md`](file:///Users/fabioandre/Downloads/nova:/COMANDOS.md)** | 🟢 Ativo | Central de atalhos rápidos universais (7 módulos organizados com exemplos de uso). |
| **[`nova-blueprint.md`](file:///Users/fabioandre/Downloads/nova:/nova-blueprint.md)** | 🟢 Referência | Documento original de planejamento arquitetural (mantido como base histórica). |
| **[`nova-status.md`](file:///Users/fabioandre/Downloads/nova:/nova-status.md)** | 🟢 Ativo | Estado real, árvore de diretórios, serviços ativos, balanço financeiro e roadmap. |
| **[`sobre-mim.md`](file:///Users/fabioandre/Downloads/nova:/sobre-mim.md)** | 🟢 Ativo | ✅ Completo (Contexto, Projetos, Metas, Estudos e Objetivo de Carreira preenchidos). |
| **[`voz/`](file:///Users/fabioandre/Downloads/nova:/voz)** | 🟢 Operacional | **Fase 6 Ativa:** Voice Studio Web App (porta `5050`), menu CLI ([`configurar_voz.py`](file:///Users/fabioandre/Downloads/nova:/voz/scripts/configurar_voz.py)) e síntese neural `edge-tts`. |
| **[`estudos/`](file:///Users/fabioandre/Downloads/nova:/estudos)** | 🟢 Ativo | Rastreador Trilha Santander DIO e **Manual Técnico & Arquitetural** compilado em Markdown e PDF. |
| **[`carreira/`](file:///Users/fabioandre/Downloads/nova:/carreira)** | 🟢 Ativo | Esteira 360° 100% padronizada (CV exclusivo em PDF, Cover Letter em PDF/DOCX e Carta Recruiter). |
| **[`scripts/`](file:///Users/fabioandre/Downloads/nova:/scripts)** | 🟢 Ativo | Motor Central de Gráficos ([`chart_engine.py`](file:///Users/fabioandre/Downloads/nova:/scripts/chart_engine.py)), Gerador Financeiro e Compilador de Manuais. |
| **[`README.md`](file:///Users/fabioandre/Downloads/nova:/README.md)** | 🟢 Ativo | Guia geral do workspace e orquestração multi-agente com atalhos rápidos. |
| **[`.agents/skills/`](file:///Users/fabioandre/Downloads/nova:/.agents/skills)** | 🟢 100% Concluído | Todos os 4 agentes especialistas equipados com scaffolding, referências, guides e templates. |
| **[`resumo/financeiro/`](file:///Users/fabioandre/Downloads/nova:/resumo:financeiro)** | 🟢 Concluído | 12 extratos + 4 comprovantes + PDF Executivo Visual ([`relatorio_agosto_2026.pdf`](file:///Users/fabioandre/Downloads/nova:/resumo/financeiro/relatorio_agosto_2026.pdf)). |
| **[`java-services/agente-financeiro/`](file:///Users/fabioandre/Downloads/nova:/java-services/agente-financeiro)** | 🟢 Operacional | Microsserviço Spring Boot 3.3.3 na porta `8081` com Spring AI MCP, endpoint de voz `/api/voice/command` e 15 testes JUnit 5. |

---

## 2. 🌳 Árvore de Diretórios e Componentes

```text
nova/
├── AGENTS.md                        # Identidade e regras do NOVA (Orquestrador + Control Center + Atalhos)
├── COMANDOS.md                      # Central de atalhos rápidos e tabela de comandos
├── nova-blueprint.md                # Plano arquitetural original (mantido como referência histórica)
├── nova-status.md                   # Este arquivo — estado real, componentes e integridade
├── sobre-mim.md                     # Memória pessoal (objetivos, projetos, metas financeiras e carreira)
├── README.md                        # Visão geral do repositório NOVA
│
├── dashboard/                       # 🧭 FASE 7: NOVA Control Center (Figma Dabang + Voice Assistant + Lucide Icons)
│   ├── index.html                   # Estrutura com card Hero Voice Assistant e Lucide Icons vetoriais
│   ├── styles.css                   # Squircle icon boxes, animação de ondas no Orb e grid 20px
│   ├── app.js                       # Microfone SpeechRecognition + reprodução Base64 HTML5 + 4 gráficos Chart.js
│   └── server.py                    # Servidor Web local na porta 3000 com endpoint POST /api/voice/interact
│
├── voz/                             # 🎙️ FASE 6: Camada de Voz Neural Humana (Voice AI Layer)
│   ├── README.md                    # Documentação técnica da arquitetura de áudio, latências e catálogo de vozes
│   ├── config_voz.json              # Configuração ativa de voz (voz_padrao, velocidade, tom)
│   ├── requirements.txt             # Dependências Python (edge-tts, requests, SpeechRecognition)
│   └── scripts/
│       ├── voice_studio_app.py      # Servidor Web interativo (Porta 5050) do NOVA Voice Studio
│       ├── nova_voice_bridge.py     # Bridge principal com leitura dinâmica do config_voz.json e afplay macOS
│       └── configurar_voz.py        # Menu interativo no terminal e CLI para teste/troca de vozes neurais
│
├── scripts/                         # Motor Central e Utilitários Executivos
│   ├── chart_engine.py              # Motor de Gráficos (Matplotlib: Match, Salário, Rosca Despesas, Balanço)
│   ├── gerar_relatorio_financeiro_pdf.py # Gerador de Relatório Financeiro Executivo em PDF
│   └── gerar_manual_estudos_pdf.py  # Compilador do Manual Técnico em PDF numerado
│
├── estudos/                         # Trilha Santander 2026 e Guias de Estudo
│   ├── trilha_tracker.md            # Rastreador oficial da Trilha Santander 2026 AI Java Back-end (DIO)
│   └── guia_estudos_nova/           # Dossiê técnico completo e compêndio de engenharia
│       ├── dossie_tecnico_completo.md # Fonte completa em Markdown
│       └── Manual_Engenharia_e_Arquitetura_NOVA.pdf # PDF de 6 páginas com código, diagramas e paginação
│
├── carreira/                        # Módulo de Carreira estruturado em 4 subdiretórios limpos
│   ├── base/                        # Documentos base oficiais e inteligência consolidada
│   │   ├── curriculo_base.md        # Currículo base oficial (Fábio Rodrigues)
│   │   ├── linkedin_destaque.md     # Post/pitch de engenharia e portfólio para LinkedIn
│   │   ├── historico_matches.md     # Inteligência comparativa de demandas de mercado (4 empresas)
│   │   └── pdf/                     # PDFs oficiais compilados (Padrão Harvard Tech)
│   │       ├── curriculo_fabio_rodrigues_pt.pdf # Versão oficial em português
│   │       └── curriculo_fabio_rodrigues_en.pdf # Versão oficial em inglês
│   ├── scripts/
│   │   ├── gerar_cv_pdf.py          # Conversor PDF (suporta --type cv, match_report e cover_letter)
│   │   ├── gerar_docx.py            # Conversor Word DOCX (suporta --type cover_letter e cv)
│   │   └── gerar_relatorio_financeiro_pdf.py # Gerador financeiro sincronizado
│   ├── templates/
│   │   ├── analise_vaga_template.md # Template padrão de avaliação de match técnico
│   │   └── cover_letter_template.md # Template de carta de apresentação formal
│   └── vagas_analisadas/            # Esteira consolidada de candidaturas (Padrão Oficial 360°)
│       ├── README.md                # Painel central e tabela de controle com links e scores
│       ├── deloitte/                # Candidatura Deloitte (Score: 86%)
│       │   ├── analise_match.md
│       │   ├── relatorio_match_deloitte.pdf
│       │   ├── curriculo_deloitte.md
│       │   ├── curriculo_fabio_rodrigues_deloitte.pdf
│       │   ├── cover_letter.md
│       │   ├── cover_letter_fabio_rodrigues_deloitte.pdf
│       │   ├── cover_letter_fabio_rodrigues_deloitte.docx
│       │   └── carta_apresentacao_recruiter.md
│       ├── capgemini/               # Candidatura Capgemini (Score: 92%)
│       │   ├── analise_match.md
│       │   ├── relatorio_match_capgemini.pdf
│       │   ├── curriculo_capgemini.md
│       │   ├── curriculo_fabio_rodrigues_capgemini.pdf
│       │   ├── cover_letter.md
│       │   ├── cover_letter_fabio_rodrigues_capgemini.pdf
│       │   ├── cover_letter_fabio_rodrigues_capgemini.docx
│       │   └── carta_apresentacao_recruiter.md
│       ├── accenture/               # Candidatura Accenture (Score: 88%)
│       │   ├── analise_match.md
│       │   ├── relatorio_match_accenture.pdf
│       │   ├── curriculo_accenture.md
│       │   ├── curriculo_fabio_rodrigues_accenture.pdf
│       │   ├── cover_letter.md
│       │   ├── cover_letter_fabio_rodrigues_accenture.pdf
│       │   ├── cover_letter_fabio_rodrigues_accenture.docx
│       │   └── carta_apresentacao_recruiter.md
│       └── fullstack/               # Candidatura FullStack (Score: 68%)
│           ├── analise_match.md
│           ├── relatorio_match_fullstack.pdf
│           ├── curriculo_fullstack.md
│           ├── curriculo_fabio_rodrigues_fullstack.pdf
│           ├── cover_letter.md
│           ├── cover_letter_fabio_rodrigues_fullstack.pdf
│           ├── cover_letter_fabio_rodrigues_fullstack.docx
│           └── carta_apresentacao_recruiter.md
│
├── .agents/
│   └── skills/
│       ├── agente-codigo/
│       │   ├── SKILL.md                 # Especialista Java 21, Spring Boot 3, Clean Code, Testes
│       │   ├── references/              # Guia Clean Architecture & Checklist formal de Code Review
│       │   │   ├── clean_architecture_guide.md
│       │   │   └── code_review_checklist.md
│       │   ├── templates/               # POM Maven padrão Java 21 + Spring Boot 3.3 + Spring AI
│       │   │   └── pom_template.xml
│       │   └── scripts/                 # CLI de geração automática de features Clean Architecture
│       │       └── scaffold_feature.py
│       ├── agente-estudos/
│       │   ├── SKILL.md                 # Mentor de Aprendizado & Trilha Santander 2026
│       │   ├── references/              # Currículo Santander DIO & Guia de Aprendizado Ativo
│       │   │   ├── trilha_santander_curriculum.md
│       │   │   └── active_learning_guide.md
│       │   └── templates/               # Templates pedagógicos estruturados
│       │       ├── resumo_tecnico_template.md
│       │       ├── flashcard_template.md
│       │       └── desafio_pratico_template.md
│       ├── agente-organizacao/
│       │   ├── SKILL.md                 # Especialista em Produtividade, Prazos & Rotina
│       │   ├── references/              # Guia de Produtividade & Matriz de Priorização
│       │   │   └── prioritization_guide.md
│       │   └── templates/               # Templates de Planejamento Semanal, Daily Notes e Hábitos
│       │       ├── planejamento_semanal_template.md
│       │       ├── daily_notes_template.md
│       │       └── habitos_rotina_template.md
│       └── agente-financeiro/SKILL.md   # Controle de gastos, categorização e balanço orçamentário
│
├── resumo/financeiro/                   # Comprovantes, extratos e relatório visual
│   ├── relatorio_agosto_2026.pdf        # Relatório executivo visual em PDF com gráficos de rosca e balanço
│   ├── 2026-08-01-entrada.jpeg          # Ramon Dos Santos Ltda (R$ 500,00)
│   ├── 2026-08-01-extrato.jpeg
│   ├── 2026-08-06-extrato.jpeg
│   ├── 2026-08-08-entrada.jpeg          # Ramon Dos Santos Ltda (R$ 500,00)
│   ├── 2026-08-08-extrato.jpeg
│   ├── 2026-08-12-extrato.jpeg
│   ├── 2026-08-13-extrato.jpeg
│   ├── 2026-08-15-entrada.jpeg          # Gildeth Santos Correia De Melo (R$ 800,00)
│   ├── 2026-08-15-extrato.jpeg
│   ├── 2026-08-16-extrato.jpeg
│   ├── 2026-08-19-extrato.jpeg
│   ├── 2026-08-20-entrada.jpeg          # Sheila Karina Barbosa De Deus (R$ 400,00)
│   ├── 2026-08-21-extrato.jpeg
│   ├── 2026-08-23-extrato.jpeg
│   ├── 2026-08-24-extrato-1.jpeg
│   ├── 2026-08-24-extrato-2.jpeg
│   └── resumo_agosto.jpeg               # Fechamento consolidado do Nubank
│
└── java-services/
    └── agente-financeiro/               # Serviço Back-end Java 21 + Spring Boot 3 + Spring AI (MCP)
        ├── src/main/java/com/nova/agentefinanceiro/
        │   ├── domain/model/            # Transacao, CategoriaTransacao, TipoTransacao, ResumoFinanceiro
        │   ├── domain/repository/       # TransacaoRepository (Port)
        │   ├── application/dto/         # TransacaoRequest, TransacaoResponse, VoiceCommandRequest/Response
        │   ├── application/usecase/     # CadastrarTransacao, ListarTransacoes, CalcularResumo, ProcessarComandoVoz
        │   └── infrastructure/
        │       ├── persistence/         # Spring Data JPA + H2 persistente
        │       ├── web/controller/      # TransacaoController, VoiceCommandController (/api/voice/command)
        │       ├── web/exception/       # GlobalExceptionHandler (RFC 7807)
        │       └── mcp/                 # FinanceiroMcpTools.java (ferramentas MCP expostas ao NOVA)
        ├── src/main/resources/
        │   └── application.yml          # Configuração da aplicação (H2 em arquivo: ./data/financiadb)
        ├── src/test/
        │   ├── java/                    # 15 testes automatizados JUnit 5 (100% de sucesso)
        │   └── resources/               # application.yml de teste isolado (H2 em memória)
        ├── data/
        │   └── financiadb.mv.db         # Arquivo do banco de dados com 43 lançamentos persistidos
        ├── pom.xml                      # Gerenciador de dependências Maven
        └── run-tests.sh                 # Script de execução rápida da suíte JUnit 5
```

---

## 3. 💰 Agente Financeiro — Balanço Fechado de Agosto/2026

- **Status da Aplicação:** Ativa e respondendo na porta `http://localhost:8081`.
- **Persistência:** Banco **H2 em arquivo** (`./data/financiadb.mv.db`).
- **Total de Transações:** 43 lançamentos (36 saídas e 7 entradas).
- **Receitas Consolidadas:** **R$ 2.299,00** (100% conciliado com o extrato Nubank).
- **Gastos Consolidados:** **R$ 1.709,77** (100% conciliado com o extrato Nubank).
- **Saldo Líquido:** **+ R$ 589,23** (Positivo e em conformidade com a meta pessoal).
- **Relatório Visual:** [`resumo/financeiro/relatorio_agosto_2026.pdf`](file:///Users/fabioandre/Downloads/nova:/resumo/financeiro/relatorio_agosto_2026.pdf) gerado com sucesso.

---

## 4. 🧪 Qualidade de Código & Testes

- **Suíte JUnit 5 + Mockito:** 15 testes cobrindo domínio, casos de uso, controllers REST, tools MCP e comandos de voz.
- **Isolamento:** Banco de testes rodando em memória (`financadb_test`), preservando a integridade dos dados reais em arquivo.
- **Resultado do `run-tests.sh`:** 100% de aprovação (0 falhas, 0 erros).

---

## 5. 🗺️ Roadmap de Evolução do Ecossistema

### ✅ Tarefas Concluídas & Ativas
- [x] **Fase 7: NOVA Control Center (Figma Dabang + Assistente de Voz Neural 100% Funcional):** Servidor Web na porta `3000` com endpoint `POST /api/voice/interact`, captura de microfone via `webkitSpeechRecognition`, reprodução de áudio Base64 nativa pelo navegador, Voice Orb dinâmico e Lucide Icons.
- [x] **Central de Atalhos Rápidos:** Arquivo [`COMANDOS.md`](file:///Users/fabioandre/Downloads/nova:/COMANDOS.md) criado com roteamento universal para prefixos `/` e `!`.
- [x] **Orquestrador Central:** Identidade, triagem e resposta única configuradas no [`AGENTS.md`](file:///Users/fabioandre/Downloads/nova:/AGENTS.md).
- [x] **Voice Studio Web App (Porta 5050):** Interface visual interativa com Dark Mode, cards de vozes, player de demonstração e persistência automática.
- [x] **Menu & Gerenciador de Vozes:** Script [`voz/scripts/configurar_voz.py`](file:///Users/fabioandre/Downloads/nova:/voz/scripts/configurar_voz.py) e persistência em [`voz/config_voz.json`](file:///Users/fabioandre/Downloads/nova:/voz/config_voz.json).
- [x] **Voz Neural Humana (Fase 6):** Motor `edge-tts` integrado com reprodução nativa `afplay` (Vozes `Antonio`, `Francisca`, `Fabio`, `Thalita`, `Guy` e `Jenny`).
- [x] **Manual Técnico & Arquitetural NOVA (Compêndio DIO):** Dossiê completo e PDF de 6 páginas compilados em `/Users/fabioandre/DIO/guia_estudos_nova/` e espelhados em `estudos/guia_estudos_nova/`.
- [x] **Padronização Definitiva de Candidaturas:** Pacote padronizado obrigatório para todas as empresas (CV exclusivo em PDF, Cover Letter em PDF e DOCX, Relatório Visual com gráficos e Carta para Recruiter no LinkedIn).
- [x] **Motor Central de Gráficos:** Módulo [`scripts/chart_engine.py`](file:///Users/fabioandre/Downloads/nova:/scripts/chart_engine.py) implementado em Python/Matplotlib.
- [x] **Relatórios Visuais de Carreira:** Geração de `relatorio_match_[empresa].pdf` com gráficos via `gerar_cv_pdf.py --type match_report`.
- [x] **Relatório Financeiro Visual:** Gerador [`scripts/gerar_relatorio_financeiro_pdf.py`](file:///Users/fabioandre/Downloads/nova:/scripts/gerar_relatorio_financeiro_pdf.py) e PDF executivo gerado em [`resumo/financeiro/relatorio_agosto_2026.pdf`](file:///Users/fabioandre/Downloads/nova:/resumo/financeiro/relatorio_agosto_2026.pdf).
- [x] **Base Oficial de Currículo:** [`carreira/base/curriculo_base.md`](file:///Users/fabioandre/Downloads/nova:/carreira/base/curriculo_base.md), PDFs oficiais em `carreira/base/pdf/`.
- [x] **Rastreador Oficial de Estudos:** Trilha Santander 2026 mapeada em [`estudos/trilha_tracker.md`](file:///Users/fabioandre/Downloads/nova:/estudos/trilha_tracker.md).
- [x] **Especialização de Todos os 4 Agentes:** Código, Estudos, Organização e Financeiro.

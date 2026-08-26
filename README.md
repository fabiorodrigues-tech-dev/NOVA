# 🌌 NOVA — Sistema Multi-Agente Pessoal & Profissional

Bem-vindo ao ecossistema **NOVA**, seu ponto central de inteligência, produtividade e desenvolvimento profissional em arquitetura multi-agente, integrando o **Gemini via Google Antigravity**, microsserviços **Java 21 / Spring Boot 3** com Clean Architecture, **Model Context Protocol (MCP)**, **Voz Neural Humana** e o **NOVA Control Center** (Dashboard Visual Unificado inspirado no Design System da Apple).

---

## 🧭 Painel Visual Unificado: NOVA Control Center (Porta 3000)
Acesse a qualquer momento pelo navegador: **[http://localhost:3000](http://localhost:3000)** ou via comando `/dashboard`.

---

## ⚡ Central de Atalhos Rápidos (`/` e `!`)
Consulte o guia completo em [`COMANDOS.md`](file:///Users/fabioandre/Downloads/nova:/COMANDOS.md). Você pode usar atalhos rápidos diretamente no chat:

- 🧭 **Central:** `/dashboard` (ou `/painel`), `/atalhos` (ou `!atalhos`), `/menu`, `/ajuda`, `/status`.
- 💼 **Carreira:** `/candidatura [link]`, `/vagas`, `/pitch [empresa]`, `/cv`.
- 📚 **Estudos (DIO):** `/estudos`, `/feynman [tópico]`, `/desafio [tema]`, `/manual`.
- 💰 **Finanças:** `/saldo`, `/extrato`, `/gastos [categoria]`, `/financeiro [mês]`.
- 💻 **Código:** `/testes`, `/review [arquivo]`, `/scaffold [Feature]`.
- 🗂️ **Organização:** `/dia`, `/semana`, `/foco`.
- 🎙️ **Voz & Studio:** `/studio`, `/voz`, `/voz [nome]`.

---

## 🏛️ Arquitetura do Sistema

```text
nova/
├── AGENTS.md                        # Identidade e regras do MAIN Agent (Orquestrador central)
├── COMANDOS.md                      # Central de atalhos rápidos (/ e !)
├── nova-blueprint.md                # Planejamento arquitetural original (referência histórica)
├── nova-status.md                   # Estado real, componentes, serviços e roadmap
├── sobre-mim.md                     # Memória pessoal (objetivos, projetos, finanças e carreira)
├── README.md                        # Guia geral do workspace
│
├── dashboard/                       # 🧭 FASE 7: NOVA Control Center (Apple Design System)
│   ├── index.html                   # Bento Grid semântico e responsivo
│   ├── styles.css                   # Glassmorphism, Dark Mode profundo e animações Apple
│   ├── app.js                       # Lógica reativa, Chart.js Donut e Voice Orb interativo
│   └── server.py                    # Servidor Web local na porta 3000
│
├── voz/                             # 🎙️ FASE 6: Camada de Voz Neural Humana (Voice AI Layer)
│   ├── config_voz.json              # Configuração ativa de voz (Antônio, Francisca, etc.)
│   └── scripts/
│       ├── voice_studio_app.py      # Voice Studio Web App (Porta 5050)
│       ├── nova_voice_bridge.py     # Bridge de escuta e síntese neural edge-tts + afplay
│       └── configurar_voz.py        # Menu interativo no terminal
│
├── carreira/                        # 💼 Módulo de Carreira & Candidaturas 360°
│   ├── base/                        # Currículos oficiais base (PT e EN) e Matriz de Mercado
│   ├── scripts/                     # Geradores PDF e DOCX (Harvard Tech / ATS)
│   └── vagas_analisadas/            # Pastas dedicadas por empresa com pacotes completos
│
├── estudos/                         # 📚 Trilha Santander 2026 DIO & Guias
│   ├── trilha_tracker.md            # Rastreador oficial da Trilha Santander DIO
│   └── guia_estudos_nova/           # Dossiê e Manual de Engenharia em PDF de 6 páginas
│
├── scripts/                         # 📊 Motor Central de Gráficos e Relatórios
│   ├── chart_engine.py              # Motor Matplotlib (Match, Salário, Despesas, Balanço)
│   └── gerar_relatorio_financeiro_pdf.py # Gerador de relatório financeiro executivo
│
├── .agents/
│   └── skills/
│       ├── agente-codigo/           # Especialista Java 21 / Spring Boot 3 / Clean Architecture
│       ├── agente-estudos/          # Especialista Trilha Santander 2026 DIO / Metodologias ativas
│       ├── agente-organizacao/      # Especialista em Produtividade / Prazos / Gestão
│       └── agente-financeiro/       # Especialista em Gestão Orçamentária e Balanço Financeiro
│
└── java-services/
    └── agente-financeiro/           # Microsserviço Back-end Java 21 + Spring Boot 3 + Spring AI (MCP)
        ├── data/financiadb.mv.db    # Banco de dados H2 persistente em arquivo
        └── run-tests.sh             # Suíte de testes automatizados JUnit 5 (15 testes - 100% sucesso)
```

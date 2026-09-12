# 🏛️ Repositório Oficial de Governança & Arquitetura — Ecossistema NOVA

> **Documentação de Engenharia de Software, Dossiês de Arquitetura e Evidências Técnicas**  
> **Autoria:** Fábio Rodrigues — Desenvolvedor Java Back-end & Arquiteto de Software  
> **Repositório:** [github.com/fabiorodrigues-tech-dev/NOVA](https://github.com/fabiorodrigues-tech-dev/NOVA)  
> **Maturidade Técnica:** **Enterprise Ready / Production-Grade Architecture (v3.14)**  
> **Suíte de Testes:** 44/44 Testes Automatizados JUnit 5 (100% Passing) • Clean Architecture • Contabilidade Sênior • Spring AI MCP

---

## 🧭 Índice Geral de Documentos, Dossiês & Design System

Este diretório centraliza os manuais, artefatos visuais e relatórios executivos compilados para avaliação arquitetural por Tech Leads, Arquitetos de Software e Recrutadores.

| Documento / Artefato | Formato | Descrição & Finalidade Técnica |
| :--- | :---: | :--- |
| **[`dossie_tecnico_nova.pdf`](file:///Users/fabioandre/Downloads/nova:/docs/dossie_tecnico_nova.pdf)** | `PDF` | **Dossiê Técnico Master Consolidado (v3.14):** Arquitetura completa, auditoria DevSecOps/LGPD, homologação de 44 testes JUnit 5, módulo de Contabilidade Sênior e parecer de prontidão *Enterprise-Grade*. |
| **[`Manual de Engenharia NOVA`](file:///Users/fabioandre/Downloads/nova:/docs/Manual_Engenharia_e_Arquitetura_NOVA.pdf)** | `PDF` | **Manual de Engenharia & Arquitetura (v3.14):** Guia técnico aprofundado com boas práticas Java 21, Clean Architecture, SOLID, Arquitetura Contábil Sênior, Deduplicação SHA-256, UI/UX Executiva e Spring AI MCP. |
| **[`assets/dashboard-light.png`](file:///Users/fabioandre/Downloads/nova:/docs/assets/dashboard-light.png)** | `PNG` | **UI Showcase Light Theme:** Interface do NOVA Control Center em modo claro com Material 3 Expressive e Bento Grid. |
| **[`assets/dashboard-dark.png`](file:///Users/fabioandre/Downloads/nova:/docs/assets/dashboard-dark.png)** | `PNG` | **UI Showcase Dark Theme:** Interface do NOVA Control Center em modo escuro com Living Shader WebGL e Glassmorphism. |
| **[`design_system/`](file:///Users/fabioandre/Downloads/nova:/docs/design_system/)** | `Diretório` | Especificações e documentações de engenharia de front-end (Material 3 Expressive, tokens CSS, anatomia visual e Living Shader). |

---

## 🏛️ Pilares de Arquitetura & Governança

1. **Clean Architecture & SOLID em Java 21 LTS:**
   - Camadas estritamente isoladas: `Domain` (agnóstico e livre de frameworks), `Application` (Casos de Uso com DTO records imutáveis incluindo `ContabilidadeUseCase`) e `Infrastructure` (Spring Data JPA com deduplicação SHA-256, Controllers REST com RFC 7807 e MCP Tools).
2. **Arquitetura Contábil Sênior & Conciliação OFX (v3.14):**
   - Endpoints contábeis regulamentares: Balancete de Verificação (`/api/financeiro/balancete`), Balanço Patrimonial & DRE (`/balanco-patrimonial`), Comparativo Horizontal MoM (`/comparativo`) e Histórico Anual 2026 (`/anual`).
   - Deduplicação estrita via hash criptográfico SHA-256 da tupla `(FITID, data_transacao, valor, descricao_limpa)`.
   - Segregação rigorosa de ativos: Conta Corrente H2 persistente (R$ 0,03) vs Caixinhas Nubank (R$ 1.000,11 líquido / R$ 1.000,14 total).
3. **Spring AI & Model Context Protocol (MCP):**
   - Ferramentas nativas `@Tool` que permitem orquestração autônoma determinística por LLMs (Gemini, Claude, GPT).
4. **Privacidade & Conformidade LGPD (DevSecOps):**
   - Inicialização 100% protegida em Modo Demonstração com dados corporativos sanitizados.
   - Botão toggle unificado `[ 🛡️ Modo Demo | Desbloquear ]` com autenticação por chave `ADMIN_PIN`.
   - Dados locais, extratos bancários brutos (`*.ofx`, `*.csv`) e bancos H2 (`*.mv.db`) são estritamente isolados pelo `.gitignore`.
5. **Qualidade Contínua & Automação CI/CD:**
   - Suíte automatizada com 44 testes unitários e de integração (JUnit 5 + Mockito) validada via GitHub Actions (`.github/workflows/ci.yml`).

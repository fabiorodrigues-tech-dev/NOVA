# 🏛️ Repositório Oficial de Governança & Arquitetura — Ecossistema NOVA

> **Documentação de Engenharia de Software, Dossiês de Arquitetura e Evidências Técnicas**  
> **Autoria:** Fábio Rodrigues — Desenvolvedor Java Back-end & Arquiteto de Software  
> **Repositório:** [github.com/fabiorodrigues-tech-dev/NOVA](https://github.com/fabiorodrigues-tech-dev/NOVA)  
> **Maturidade Técnica:** **Enterprise Ready / Production-Grade Architecture**  
> **Suíte de Testes:** 40/40 Testes Automatizados JUnit 5 (100% Passing) • Clean Architecture • Spring AI MCP

---

## 🧭 Índice Geral de Documentos, Dossiês & Design System

Este diretório centraliza os manuais, artefatos visuais e relatórios executivos compilados para avaliação arquitetural por Tech Leads, Arquitetos de Software e Recrutadores.

| Documento / Artefato | Formato | Descrição & Finalidade Técnica |
| :--- | :---: | :--- |
| **[`dossie_tecnico_nova.pdf`](file:///Users/fabioandre/Downloads/nova:/docs/dossie_tecnico_nova.pdf)** | `PDF` | **Dossiê Técnico Master Consolidado:** Arquitetura completa, auditoria DevSecOps/LGPD, homologação de 40 testes JUnit 5 e parecer de prontidão *Enterprise-Grade*. |
| **[`assets/nova-light-preview.png`](file:///Users/fabioandre/Downloads/nova:/docs/assets/nova-light-preview.png)** | `PNG` | **UI Showcase Light Theme:** Interface do NOVA Control Center em modo claro com Material 3 Expressive e Bento Grid. |
| **[`assets/nova-dark-preview.png`](file:///Users/fabioandre/Downloads/nova:/docs/assets/nova-dark-preview.png)** | `PNG` | **UI Showcase Dark Theme:** Interface do NOVA Control Center em modo escuro com Living Shader WebGL e Glassmorphism. |
| **[`design_system/`](file:///Users/fabioandre/Downloads/nova:/docs/design_system/)** | `Diretório` | Especificações e documentações de engenharia de front-end (Material 3 Expressive, tokens CSS, anatomia visual e Living Shader). |
| **[`Manual de Engenharia NOVA`](file:///Users/fabioandre/Downloads/nova:/estudos/guia_estudos_nova/Manual_Engenharia_e_Arquitetura_NOVA.pdf)** | `PDF` | Manual aprofundado com boas práticas Java 21, Clean Architecture, SOLID, padrões de projeto e Spring AI MCP. |

---

## 🏛️ Pilares de Arquitetura & Governança

1. **Clean Architecture & SOLID em Java 21 LTS:**
   - Camadas estritamente isoladas: `Domain` (agnóstico e livre de frameworks), `Application` (Casos de Uso com DTO records imutáveis) e `Infrastructure` (Spring Data JPA, Controllers REST com RFC 7807 e MCP Tools).
2. **Spring AI & Model Context Protocol (MCP):**
   - Ferramentas nativas `@Tool` que permitem orquestração autônoma determinística por LLMs (Gemini, Claude, GPT).
3. **Privacidade & Conformidade LGPD (DevSecOps):**
   - Todos os dados financeiros apresentados na vitrine pública são **Mocks Corporativos de Alta Performance** (`[MOCK CORPORATIVO / DADOS SANITIZADOS LGPD]`).
   - Dados locais, extratos bancários brutos e bancos H2 (`*.mv.db`) são estritamente isolados pelo `.gitignore`.
4. **Qualidade Contínua & Automação CI/CD:**
   - Suíte automatizada com 40 testes unitários e de integração (JUnit 5 + Mockito) validada via GitHub Actions (`.github/workflows/ci.yml`).

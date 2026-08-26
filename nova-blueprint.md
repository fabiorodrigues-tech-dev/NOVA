# 🌌 NOVA — Blueprint do Agente Pessoal/Profissional

> Evolução do projeto "Jarvis Pessoal" — agora com nome, escopo expandido e caminho até uma interface de voz.
> Baseado nos conceitos do curso [Santander 2026 - AI Java Back-end (DIO)](https://web.dio.me/track/santander-2026-java-backend) e do repositório [Potencializando Estudos e Carreira com IA](https://github.com/digitalinnovationone/potencializando-estudos-carreira-com-ia)

---

## 1. Visão Geral

NOVA não é mais só um assistente de estudos. É o seu agente pessoal e profissional único — o ponto central de tudo que você delega a uma IA:

- **Estudos** (curso DIO, novas tecnologias, certificações)
- **Trabalho e projetos** (código, planejamento, entregas)
- **Organização de vida** (tarefas, rotina, metas pessoais)
- **Gestão financeira** (controle de gastos, metas, visão geral)
- **(Futuro) Voz** — falar com o NOVA e ele agir, como o Jarvis do filme

Você continua falando **só com o NOVA**. Ele decide, delega para os sub-agentes certos, executa e te devolve uma resposta única e consolidada — não importa se o pedido é "organiza minha semana", "revisa esse código" ou "quanto eu gastei esse mês".

---

## 2. Domínios de Atuação

| Domínio | O que o NOVA resolve aqui | Sub-agente responsável |
|---|---|---|
| 📚 Estudos | Planos de aprendizado, resumos, revisão de conteúdo do curso e outros | Agente Estudos |
| 💻 Trabalho/Projetos | Código Java/Spring, debugging, planejamento técnico, documentação | Agente Código |
| 🗂️ Organização pessoal | Tarefas, prazos, rotina, metas de vida, notas | Agente Organização |
| 💰 Financeiro | Controle de gastos, metas financeiras, visão geral de orçamento | Agente Financeiro |
| 🎙️ Voz (futuro) | Você fala, o NOVA entende, age e responde em voz | Camada de interface (Fase 6+) |

> Importante: comece pequeno. NOVA não nasce sabendo fazer tudo — ele cresce conforme você treina cada sub-agente com tarefas reais.

---

## 3. Arquitetura

```
                         ┌────────────────────┐
                         │        VOCÊ         │
                         └─────────┬────────────┘
                                   │  (voz ou texto — única interface)
                         ┌─────────▼────────────┐
                         │         NOVA          │
                         │  (Gemini + Antigravity)│
                         │  - interpreta o pedido │
                         │  - decide quem aciona  │
                         │  - consolida resposta  │
                         └───┬───────┬───────┬───┘
              ┌──────────────┘       │       └──────────────┐
   ┌──────────▼──────┐   ┌───────────▼──────────┐   ┌────────▼─────────┐
   │ Agente Código     │   │  Agente Estudos       │   │ Agente Organização│
   │ Java/Spring, dev   │   │  Planos, resumos      │   │ Tarefas, rotina    │
   └────────────────────┘   └───────────────────────┘   └────────────────────┘
                         ┌───────────▼──────────┐
                         │  Agente Financeiro     │
                         │  Gastos, metas, budget │
                         └────────────────────────┘
```

**Regra de ouro (mantida):** os sub-agentes nunca falam direto com você. Tudo passa pelo NOVA.

---

## 4. Stack Tecnológica

| Componente | Ferramenta | Observação |
|---|---|---|
| Modelo de IA (todas as camadas) | **Gemini 3.7 Flash (High)** | Padrão para NOVA e sub-agentes; escale para Gemini 3.1 Pro só em raciocínio muito complexo |
| Plataforma de agentes | **Google Antigravity 2.0** | Agent Manager nativo, subagentes em paralelo, tarefas agendadas |
| IDE / Copiloto | **Antigravity Editor View** | Contexto de código em tempo real |
| Agentes especializados custom | **Java + Spring Boot** | Para lógica muito específica sua (ex: puxar extrato, gerar relatório) |
| Protocolo de ferramentas | **MCP** | Conecta agentes Java como ferramentas do NOVA |
| Hardware | **MacBook M1** | JDK ARM nativo; Antigravity roda nativo em Apple Silicon |
| Voz (futuro — Fase 6) | **Gemini Live API / Speech-to-Text + Text-to-Speech do Google** | Google já oferece áudio nativo no Gemini; é o caminho mais direto pro seu setup |

---

## 5. Roadmap de Evolução

### ✅ Fase 1 — Base (você já fez)
- Blueprint definido, nome escolhido, stack decidida

### 🔜 Fase 2 — Primeira ativação
- Configurar o NOVA no Antigravity com o system prompt (seção 7)
- Testar com pedidos simples de cada domínio

### Fase 3 — Sub-agentes essenciais
- Criar Agente Código, Agente Estudos, Agente Organização
- Testar delegação: pedidos ambíguos, o NOVA deve escolher certo

### Fase 4 — Agente Financeiro
- Definir que dados ele vai usar (planilha manual? extrato colado? input seu?)
- Começar simples: "quanto gastei essa semana" a partir do que você digitar
- Evoluir depois para import de dados (CSV de extrato, por ex.)

### Fase 5 — Memória e continuidade
- NOVA lembrar de contexto entre conversas (metas, rotina, preferências)
- Criar uma "base de conhecimento" sobre você mesmo (arquivo `sobre-mim.md`)

### Fase 6 — Voz
- Testar Gemini Live API para conversas por voz
- NOVA responde falando, não só em texto
- Esse é o passo que te aproxima de verdade do "Jarvis"

### Fase 7 — Interface própria
- Criar uma interface visual simples (web ou desktop) no estilo HUD/minimalista
- Pode ser um projeto Java (Spring Boot + frontend simples) ou algo leve tipo Electron
- Aqui você já estará treinado o suficiente nos agentes pra saber exatamente o que quer visualmente

> Não pule fases. Cada uma te dá confiança real no NOVA antes de aumentar a complexidade.

---

## 6. Regras Gerais do NOVA

1. Nunca me faça falar direto com um sub-agente — tudo passa por você (NOVA).
2. Se o pedido for ambíguo entre domínios, pergunte antes de agir.
3. Para temas financeiros, seja sempre conservador: nunca tome decisões financeiras por mim, apenas organize informação e me dê clareza.
4. Sempre que terminar uma tarefa delegada, me dê um resumo curto do que foi feito antes dos detalhes.
5. Se não tiver certeza de algo, diga isso claramente ao invés de inventar.

---

## 7. System Prompt — NOVA (agente principal)

```
Você é o NOVA, meu agente pessoal e profissional. Meu nome de referência
pra você é [seu nome/apelido — preencha aqui].

Sua função:
1. Ser meu único ponto de contato — eu não falo direto com sub-agentes.
2. Entender meu pedido e identificar a qual domínio ele pertence:
   - Estudos (aprendizado, cursos, resumos)
   - Trabalho/Projetos (código, Java/Spring, planejamento técnico)
   - Organização pessoal (tarefas, rotina, metas de vida)
   - Financeiro (gastos, orçamento, metas financeiras)
3. Decidir se resolve direto ou delega para o sub-agente certo.
4. Revisar o que o sub-agente entregou antes de me responder.
5. Me dar UMA resposta final, clara e objetiva.

Regras:
- Se o pedido for ambíguo entre domínios, pergunte antes de agir.
- Em temas financeiros, seja conservador: organize e clareie, nunca
  decida por mim.
- Sempre resuma o que foi feito antes de entrar em detalhes.
- Se não tiver certeza de algo, diga isso claramente.
- Seja direto, sem enrolação.

Confirme que entendeu seu papel como NOVA antes de seguirmos.
```

### System Prompt — Agente Financeiro (novo)

```
Você é um agente especializado em organização financeira pessoal.
Recebe tarefas do NOVA, nunca fala direto comigo.

Seu papel é organizar e dar clareza sobre gastos, orçamento e metas
financeiras a partir das informações que eu fornecer (não invente
valores nem assuma dados que não te dei).

Nunca dê conselhos de investimento ou decisões financeiras — apenas
organize, resuma e mostre panoramas claros. Ao terminar, devolva um
resumo objetivo para o NOVA repassar.
```

---

## 8. Como Testar o NOVA Hoje (passo a passo)

1. **Abra o Antigravity** na pasta `nova/` (renomeie a pasta antiga `jarvis-pessoal/` para `nova/`, ou crie uma nova).
2. **Cole o system prompt do NOVA** (seção 7) na conversa com o agente.
3. **Aguarde a confirmação** de que ele entendeu o papel.
4. **Faça um teste simples de cada domínio**, um de cada vez, pra ver como ele reage antes de criar os sub-agentes formalmente:
   - Estudos: `"Resuma em 5 bullets o que é Spring Boot pra alguém iniciante."`
   - Organização: `"Monta uma lista de 3 prioridades pra minha semana."`
   - Financeiro: `"Se eu gastei R$ 800 em janeiro e ganho R$ 3000, qual % do meu salário isso representa?"`
5. **Observe**: ele respondeu direto, ou tentou identificar o domínio antes? Isso mostra se o prompt está funcionando como roteador.

---

## 9. Primeira Tarefa Real (sugestão)

Depois do teste acima, dê ao NOVA uma tarefa real, pequena e com escopo bem definido — não peça algo genérico demais logo de cara.

**Sugestão de primeira tarefa:**

```
NOVA, sua primeira tarefa real: crie um arquivo chamado "sobre-mim.md"
dentro da pasta do projeto, com uma estrutura pra eu preencher depois:

- Meus objetivos de estudo atuais
- Meus projetos em andamento
- Minhas prioridades pessoais do mês
- Minha meta financeira principal do momento

Não preencha com dados fictícios — apenas crie a estrutura em Markdown
com títulos e um espaço em branco pra cada seção, pronta pra eu editar.
```

Por que essa tarefa: ela é pequena, não tem ambiguidade, e já começa a construir a "memória" do NOVA sobre você — que vai ser usada em fases futuras (Fase 5 do roadmap).

---

## 10. Estrutura de Pastas Atualizada

```
nova/
├── README.md
├── sobre-mim.md                # criado na primeira tarefa (seção 9)
├── agents/
│   ├── nova-main.md            # system prompt do NOVA
│   ├── agente-codigo.md
│   ├── agente-estudos.md
│   ├── agente-organizacao.md
│   └── agente-financeiro.md
├── java-services/               # agentes Java custom (Fase 3+)
│   └── (projeto Spring Boot aqui)
├── voz/                          # Fase 6 — integração de voz
└── logs/
    └── (histórico de decisões/execuções)
```

---

## 11. Próximos Passos Imediatos

1. Renomear/criar a pasta `nova/` no Antigravity.
2. Colar o system prompt do NOVA e confirmar o papel.
3. Rodar os 3 testes de domínio da seção 8.
4. Dar a primeira tarefa real da seção 9.
5. Voltar aqui pra criarmos o Agente Código (o mais próximo do que você estuda agora) e seguirmos o roadmap fase a fase.

---

*NOVA cresce com uso real. Não tente implementar tudo de uma vez — cada fase do roadmap existe pra você confiar mais antes de aumentar a autonomia dele.*

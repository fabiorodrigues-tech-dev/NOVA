# 🔧 NOVA — Correção de Anatomia Visual (Diagnóstico + Fix)

> A cor está certa. A estrutura do card e a densidade de espaço não estão. Este documento existe para corrigir isso com precisão, sem precisar refazer tudo de novo.

---

## 1. Diagnóstico exato do gap

| Elemento | Como está agora | Como é na referência (Google Health) | Por quê importa |
|---|---|---|---|
| Fundo do card KPI | Cor sólida cobrindo o card inteiro (verde/dourado/azul cheio) | Fundo neutro (branco/cinza muito claro), cor só no ícone | Cor cobrindo tudo = visual "app financeiro genérico". Cor só no ícone = visual "produto premium calmo" |
| Espaçamento entre cards | Compacto, gap pequeno | Generoso, respiro grande entre blocos | Espaço em branco é luxo visual — sinaliza confiança, não aperta informação |
| Tipografia dos números | Tamanho médio | Números grandes, quase "hero", dominando o card | O número é o herói do card, tudo mais é suporte |
| Padding interno do card | Moderado | Muito generoso (24-32px+) | Cards "respirando" por dentro é assinatura M3/wellness |
| Bordas/contorno | Card com contorno sutil mas ainda "carrega peso" | Praticamente sem borda — só sombra suave levíssima | Menos contorno = mais leveza |
| Header/Voice Assistant | Ainda um bloco roxo/azul saturado grande | Seria neutro, com cor só em elementos pontuais (botão, badge) | O bloco de fundo colorido grande é o mesmo erro dos cards |

**Resumo em uma frase:** o problema não é "qual cor", é "**onde** a cor aparece". Regra M3 de verdade: cor é usada com moderação — pequenos chips, ícones, badges, botões — nunca como fundo de área grande, exceto o próprio botão de ação principal.

---

## 2. A "Anatomia do Card" correta (blueprint exato)

```
┌─────────────────────────────────────────┐
│  [chip colorido]              [badge]    │  ← ícone com fundo --nova-*-container
│    pequeno, ~40x40px           +34.5%    │     (só o CHIP tem cor, não o card)
│                                           │
│  Saldo Líquido (Agosto)                  │  ← label, --nova-on-surface-variant
│                                           │
│  R$ 589,23                               │  ← número GRANDE (40-48px), --nova-on-surface
│                                           │
│  ─────────────────────────────────       │  ← divisor sutil, opcional
│  H2 Persistente • 100% Conciliado        │  ← texto pequeno, --nova-on-surface-variant
└─────────────────────────────────────────┘
   fundo do card: --nova-surface (neutro)
   padding: 28px
   border-radius: 20px
   sombra: 0 1px 2px rgba(0,0,0,0.06), 0 1px 8px rgba(0,0,0,0.04)
   SEM borda colorida, SEM fundo colorido
```

A cor (`--nova-secondary-container` no exemplo do Saldo) vive **só no chip do ícone** — um quadrado/círculo pequeno de ~40px atrás do ícone. O resto do card é neutro.

---

## 3. Sistema de Espaçamento (para parar de "empilhar" elementos)

Adote uma escala de 8px em tudo — resolve a sensação de aperto:

```css
--nova-space-1: 8px;
--nova-space-2: 16px;
--nova-space-3: 24px;
--nova-space-4: 32px;
--nova-space-5: 48px;
--nova-space-6: 64px;
```

- Gap entre cards no grid: `--nova-space-3` (24px) mínimo, `--nova-space-4` (32px) ideal
- Padding interno de cards: `--nova-space-3` a `--nova-space-4`
- Espaço entre seções (Voice Assistant → KPIs → Gráficos): `--nova-space-5` (48px) mínimo

---

## 4. Comando Corretivo para o NOVA

```
Preciso corrigir a ANATOMIA dos cards do Dashboard — a paleta de
cores M3 está correta, mas está sendo aplicada da forma errada
(cor cobrindo o card inteiro). Corrija especificamente:

1. CARDS DE KPI (Saldo Líquido, Total Recebido, Total Gasto, Trilha
   DIO): o FUNDO do card deve ser sempre --nova-surface (neutro,
   branco no light / #121317 no dark) — NUNCA a cor container cheia.
   A cor (--nova-secondary-container, --nova-tertiary-container,
   --nova-primary-container) deve aparecer APENAS como fundo de um
   pequeno "chip" atrás do ícone, de aproximadamente 40x40px com
   border-radius de 12px — não como fundo do card inteiro.

2. TIPOGRAFIA DOS NÚMEROS: aumente o tamanho dos valores principais
   (R$ 589,23, R$ 2.299,00, etc.) para 40-48px, peso 500-600. Eles
   devem ser visualmente o elemento dominante do card.

3. REMOVA todas as bordas coloridas dos cards. Substitua por sombra
   suave apenas: box-shadow: 0 1px 2px rgba(0,0,0,0.06), 0 1px 8px
   rgba(0,0,0,0.04) — nada de contorno colorido de 2px.

4. AUMENTE O ESPAÇAMENTO em todo o sistema, usando esta escala:
   --nova-space-1: 8px; --nova-space-2: 16px; --nova-space-3: 24px;
   --nova-space-4: 32px; --nova-space-5: 48px; --nova-space-6: 64px;
   Aplique: gap entre cards do grid = --nova-space-4 (32px), padding
   interno dos cards = --nova-space-4, espaço entre seções (Voice
   Assistant → KPIs → Gráficos) = --nova-space-5 (48px).

5. PADDING INTERNO DOS CARDS: aumente para --nova-space-4 (32px) em
   todos os cards, inclusive o card do NOVA Voice Assistant.

6. NOVA VOICE ASSISTANT (card do topo): remova o fundo em gradiente
   roxo/azul saturado grande. Use --nova-surface como fundo do card
   inteiro (neutro), mantendo cor só no botão do microfone (que já
   está correto) e em badges pontuais (ex: "Pronto para ouvir").

7. BORDER-RADIUS: aumente para 20px em todos os cards (atualmente
   parece estar em ~12-14px) — isso reforça a sensação "macia" da
   referência.

Esta é uma correção estrutural, não uma reformulação de cores —
mantenha os tokens de cor já implementados, apenas corrija ONDE e
COMO eles são aplicados.

Depois de implementar, tire um print do Dashboard completo (modo
claro) pra eu comparar diretamente com a anatomia descrita acima.
```

---

## 5. Como validar se funcionou

Depois do print, faça este teste rápido: tampe a cor com a mão (mentalmente) e veja se o card ainda parece "rico" só pela tipografia, espaço e sombra. Se sim, a anatomia está certa — a cor virou tempero, não a substância. Se o card parecer "vazio" sem a cor, ainda está errado — significa que a cor estava fazendo o trabalho que o espaço e a tipografia deveriam fazer.

---

*Esta correção deve ser suficiente para fechar o gap. Se depois de aplicada ainda sentir distância da referência, o próximo suspeito é a densidade da sidebar e do header — mas vamos validar este passo primeiro antes de mexer em mais uma camada.*

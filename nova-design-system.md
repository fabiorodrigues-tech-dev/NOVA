# 🎨 NOVA — Design System v3 (Material Design Inspired)

> Documento de referência para o redesign visual do NOVA Control Center. Substitui a identidade anterior (Figma "Sales Dashboard" + tema escuro genérico) por uma linguagem inspirada no Material Design 3 do Google — a mesma base usada em apps como Google Health, Google Fit e Android.

---

## 0. Por que Material Design 3 (e não clonar a página do Google Health)

A referência visual que você gostou (Google Health Premium) usa **marcas registradas da Google** (Fitbit, Pixel, fotos de produto, imagem de atleta patrocinado). Replicar isso literalmente seria usar propriedade intelectual de terceiros num projeto que você quer publicar como portfólio — o oposto do efeito que você busca.

A solução mais forte: adotar o **Material Design 3 (M3)**, que é o sistema de design que a própria Google publica abertamente para qualquer desenvolvedor usar (https://m3.material.io). Isso te dá:
- A mesma sensação "produto Google" (limpo, calmo, cards arredondados, cor com propósito)
- Legitimidade técnica real — você pode dizer numa entrevista "usei Material Design 3" e isso é literalmente verdade
- Zero risco de marca — é um sistema público, não uma cópia de página comercial

---

## 1. Paleta de Cores

Sistema de cor tonal (inspirado no M3, mas com identidade própria do NOVA — não usa o azul exato do logo Google):

| Token | Uso | Hex sugerido |
|---|---|---|
| `--nova-primary` | Ações principais, links, ícones ativos | `#4A6FA5` (azul acinzentado, mais sóbrio que o Google Blue puro) |
| `--nova-primary-container` | Fundo de cards ativos/selecionados | `#DCE6F5` (light) / `#1E2A3D` (dark) |
| `--nova-secondary` | Acentos secundários (voz, notificações) | `#5B8A72` (verde suave, remete a "saúde/positivo") |
| `--nova-tertiary` | Alertas leves, destaques financeiros | `#B8860B` (dourado suave, para valores/dinheiro) |
| `--nova-error` | Erros, saldo negativo | `#B3261E` |
| `--nova-surface` | Fundo base | `#FFFFFF` (light) / `#121417` (dark) |
| `--nova-surface-container` | Fundo dos cards | `#F2F4F7` (light) / `#1C1F24` (dark) |
| `--nova-on-surface` | Texto principal | `#1B1C1E` (light) / `#E3E2E6` (dark) |
| `--nova-outline` | Bordas sutis | `#C4C7CC` (light) / `#3A3D42` (dark) |

**Regra de uso:** cor com propósito, não decoração. Cada cor tem um significado fixo (ex: dourado sempre = dinheiro/financeiro; verde sempre = positivo/voz ativa). Evite usar cor só "porque ficou bonito" — no M3, cor comunica estado.

---

## 2. Tipografia

- **Fonte principal:** `"Google Sans Text", "Inter", -apple-system, sans-serif` — Google Sans Text está disponível no Google Fonts; Inter como fallback tem a mesma sensação geométrica e limpa.
- **Escala tipográfica (M3):**
  | Estilo | Tamanho | Peso | Uso |
  |---|---|---|---|
  | Display | 36px | 400 | Números grandes (saldo, totais) |
  | Headline | 24px | 500 | Títulos de seção |
  | Title | 16px | 500 | Títulos de card |
  | Body | 14px | 400 | Texto corrido |
  | Label | 12px | 500 | Tags, badges, legendas |

---

## 3. Componentes-Chave

### Cards
- Cantos bem arredondados: `border-radius: 16px` (M3 usa raios generosos, é uma assinatura visual)
- Sombra suave, nunca dura: `box-shadow: 0 1px 3px rgba(0,0,0,0.08)`
- Padding interno generoso: mínimo `24px`
- Sem bordas grossas coloridas (diferente do estilo atual com borda neon) — a hierarquia vem de cor de fundo sutil, não de contorno

### Botões
- **Pill-shaped** (`border-radius: 100px`), não retangulares com cantos levemente arredondados
- Três variantes M3: Filled (ação principal), Tonal (ação secundária), Outlined (ação terciária)
- Sem gradientes vibrantes — cor sólida do token, com estado de hover por opacidade

### Navegação lateral
- Manter a navigation rail (já existe no layout atual), mas com item ativo indicado por **pílula de fundo** atrás do ícone+label (padrão M3 clássico do Android), não por borda ou glow

### Gráficos
- Paleta de dados usando os tokens de cor (primary/secondary/tertiary), nunca cores aleatórias
- Linhas mais finas, área de preenchimento com opacidade baixa (10-15%), sem glow/neon

---

## 4. Estrutura de Layout (padrão observado na referência)

A página que você gostou segue um padrão comum de apps de saúde/wellness que fazemos sentido replicar (a *estrutura*, não os assets):

1. **Hero/resumo no topo** — um número grande e central (no caso deles, era o "score"; no NOVA, pode ser o saldo ou status geral)
2. **Cards de features em grid** — cada card com ícone, título curto, descrição de 1 linha
3. **Espaço em branco generoso entre seções** — nada colado, respiro visual constante
4. **Uma cor de destaque por seção**, não a paleta inteira de uma vez

Aplicado ao NOVA:
- Dashboard: hero com saldo/status geral → grid de cards (Financeiro, Voz, Estudos, Carreira)
- Cada seção interna (Voice Studio, Finanças) segue o mesmo padrão de card, sem "trocar de estilo"

---

## 5. Motion (microinterações)

- Transições suaves e curtas: `transition: all 200ms ease-out`
- Sem animações "chamativas" (glow pulsante, gradiente animado) — M3 é sutil: fade + leve scale (`0.98 → 1`) em hover/click
- Troca de seção (Dashboard ↔ Voice Studio ↔ Finanças) com fade cross-dissolve, não slide agressivo

---

## 6. Comando para dar ao NOVA

```
Quero fazer um redesign completo do NOVA Control Center, trocando a
identidade visual atual (tema escuro genérico com bordas neon,
baseado no template Figma "Sales Dashboard") por uma linguagem
inspirada no Material Design 3 do Google (m3.material.io) — o sistema
de design público da Google, não uma cópia de nenhuma página
comercial específica.

Aplique as seguintes diretrizes:

1. PALETA: substitua as cores atuais pelos tokens abaixo, usando
   CSS custom properties:
   --nova-primary: #4A6FA5
   --nova-primary-container: #DCE6F5 (light) / #1E2A3D (dark)
   --nova-secondary: #5B8A72
   --nova-tertiary: #B8860B
   --nova-error: #B3261E
   --nova-surface: #FFFFFF (light) / #121417 (dark)
   --nova-surface-container: #F2F4F7 (light) / #1C1F24 (dark)
   --nova-on-surface: #1B1C1E (light) / #E3E2E6 (dark)
   --nova-outline: #C4C7CC (light) / #3A3D42 (dark)

2. TIPOGRAFIA: troque a fonte para "Google Sans Text" (via Google
   Fonts) com fallback para Inter. Aplique a escala: Display 36px/400
   para números grandes, Headline 24px/500 para títulos de seção,
   Title 16px/500 para títulos de card, Body 14px/400 para texto.

3. CARDS: border-radius de 16px, sombra suave (0 1px 3px
   rgba(0,0,0,0.08)), padding mínimo 24px, remova bordas neon/glow
   coloridas — hierarquia por cor de fundo sutil, não por contorno.

4. BOTÕES: formato pill (border-radius: 100px), três variantes
   (filled/tonal/outlined), sem gradientes vibrantes.

5. NAVEGAÇÃO LATERAL: item ativo com pílula de fundo atrás do
   ícone+label, ao invés do destaque atual com borda/glow.

6. GRÁFICOS: use apenas os tokens de cor definidos acima nos
   gráficos (Chart.js), linhas mais finas, preenchimento de área
   com opacidade baixa (10-15%), remova qualquer glow.

7. MOTION: transições de 200ms ease-out, sem animações chamativas.
   Troca entre seções (Dashboard/Voice Studio/Finanças) com fade
   suave, não slide.

8. Mantenha toda a funcionalidade existente (unificação com Voice
   Studio, KPIs, gráficos) — esta é uma mudança visual, não funcional.

Depois de implementar, tire um print do resultado pra eu revisar
antes de você seguir ajustando detalhes.
```

---

*Este documento existe para você ter uma referência estável de identidade visual, evitando decisões de design ad-hoc a cada sessão. Qualquer nova tela do NOVA deve seguir estes tokens.*

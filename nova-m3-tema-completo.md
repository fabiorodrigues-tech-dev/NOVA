# 🌗 NOVA — Material Design 3 Completo (Light/Dark) + Toggle de Tema

> Expande o `nova-design-system.md`. Define o par completo de esquemas de cor (claro/escuro) no padrão M3 de "color roles", e a especificação do botão de alternância. Este é o token set definitivo — qualquer tela nova do sistema (Dashboard, Voice Studio, Finanças, Carreira, Estudos) deve usar só essas variáveis, nunca hex solto.

---

## 1. Por que "color roles" (e não só "cor de fundo do card")

O erro visual nos cards atuais (Saldo/Recebido/Gasto com vermelho/dourado/verde saturados) é usar cor **decorativa** em vez de cor **com papel definido**. No M3, toda cor tem uma função fixa: `primary` é sempre ação/destaque principal, `error` é sempre estado negativo, `tertiary` é sempre um acento de apoio — nunca "essa cor porque combina". Isso é o que dá aparência de sistema profissional em vez de template.

---

## 2. Tokens Completos — Light Scheme

```css
:root[data-theme="light"] {
  --nova-primary: #4A6FA5;
  --nova-on-primary: #FFFFFF;
  --nova-primary-container: #D9E3F5;
  --nova-on-primary-container: #0F2C4E;

  --nova-secondary: #5B8A72;
  --nova-on-secondary: #FFFFFF;
  --nova-secondary-container: #D9EFE0;
  --nova-on-secondary-container: #0F2E1C;

  --nova-tertiary: #8A6D1A;
  --nova-on-tertiary: #FFFFFF;
  --nova-tertiary-container: #F5E7C4;
  --nova-on-tertiary-container: #3D2F00;

  --nova-error: #B3261E;
  --nova-on-error: #FFFFFF;
  --nova-error-container: #F9DEDC;
  --nova-on-error-container: #410E0B;

  --nova-background: #FBFBFE;
  --nova-on-background: #1B1C1E;
  --nova-surface: #FFFFFF;
  --nova-on-surface: #1B1C1E;
  --nova-surface-variant: #E1E2EC;
  --nova-on-surface-variant: #45464F;
  --nova-outline: #767680;
}
```

## 3. Tokens Completos — Dark Scheme

```css
:root[data-theme="dark"] {
  --nova-primary: #A9C7FF;
  --nova-on-primary: #123465;
  --nova-primary-container: #2C4A7C;
  --nova-on-primary-container: #D9E3F5;

  --nova-secondary: #9FD3B3;
  --nova-on-secondary: #16382A;
  --nova-secondary-container: #2C4F3B;
  --nova-on-secondary-container: #D9EFE0;

  --nova-tertiary: #E4C46E;
  --nova-on-tertiary: #3D2F00;
  --nova-tertiary-container: #5C4900;
  --nova-on-tertiary-container: #F5E7C4;

  --nova-error: #F2B8B5;
  --nova-on-error: #601410;
  --nova-error-container: #8C1D18;
  --nova-on-error-container: #F9DEDC;

  --nova-background: #121317;
  --nova-on-background: #E3E2E6;
  --nova-surface: #121317;
  --nova-on-surface: #E3E2E6;
  --nova-surface-variant: #45464F;
  --nova-on-surface-variant: #C6C6D0;
  --nova-outline: #909099;
}
```

## 4. Mapeamento Semântico (aplicar nos cards existentes)

| Card/Elemento | Antes (cor solta) | Agora (token M3) |
|---|---|---|
| Saldo Líquido (positivo) | Vermelho escuro genérico | `--nova-secondary-container` / texto `--nova-on-secondary-container` (verde = positivo) |
| Total Recebido | Dourado saturado | `--nova-tertiary-container` / `--nova-on-tertiary-container` |
| Total Gasto | Verde saturado | `--nova-primary-container` / `--nova-on-primary-container` (neutro informativo, não é "erro" s√≥ por ser saída) |
| Saldo negativo (se ocorrer) | — | `--nova-error-container` / `--nova-on-error-container` |
| Trilha DIO / progresso | Roxo genérico | `--nova-tertiary` na barra de progresso sobre `--nova-surface-variant` |
| Botão "Pressione para Falar" | Gradiente rosa/roxo | `--nova-primary` sólido, sem gradiente |

---

## 5. Especificação do Toggle Dia/Noite

### Posição
Canto superior direito do header, ao lado do seletor de voz — sempre visível, nunca escondido em menu.

### Comportamento
- Ícone de sol (☀️) em modo claro, lua (🌙) em modo escuro — troca com animação de rotação + fade de 300ms, não corte seco
- Um único botão (toggle), não dois botões separados
- Estado persiste entre sessões (salvar preferência local, ex: `localStorage`)
- Se não houver preferência salva, respeitar `prefers-color-scheme` do sistema operacional como padrão inicial
- Transição de tema aplicada com `transition: background-color 250ms ease, color 250ms ease` no `body`/containers principais — nunca troca abrupta

### Micro-interação
Ao clicar, além da troca de ícone, um leve "ripple" circular expandindo do botão (efeito M3 clássico de toque) — opcional, mas é o tipo de detalhe que impressiona.

---

## 6. Comando Único para o NOVA (execução completa)

```
Vamos aplicar o Material Design 3 completo em TODO o sistema visual
do NOVA (Dashboard, Voice Studio, Finanças, Carreira, Estudos — todas
as telas), substituindo definitivamente as cores soltas atuais.

1. TOKENS: implemente os dois blocos de CSS custom properties abaixo,
   controlados por um atributo data-theme="light" ou data-theme="dark"
   na tag <html> ou <body>:

   [Light scheme]
   --nova-primary: #4A6FA5; --nova-on-primary: #FFFFFF;
   --nova-primary-container: #D9E3F5; --nova-on-primary-container: #0F2C4E;
   --nova-secondary: #5B8A72; --nova-on-secondary: #FFFFFF;
   --nova-secondary-container: #D9EFE0; --nova-on-secondary-container: #0F2E1C;
   --nova-tertiary: #8A6D1A; --nova-on-tertiary: #FFFFFF;
   --nova-tertiary-container: #F5E7C4; --nova-on-tertiary-container: #3D2F00;
   --nova-error: #B3261E; --nova-on-error: #FFFFFF;
   --nova-error-container: #F9DEDC; --nova-on-error-container: #410E0B;
   --nova-background: #FBFBFE; --nova-on-background: #1B1C1E;
   --nova-surface: #FFFFFF; --nova-on-surface: #1B1C1E;
   --nova-surface-variant: #E1E2EC; --nova-on-surface-variant: #45464F;
   --nova-outline: #767680;

   [Dark scheme]
   --nova-primary: #A9C7FF; --nova-on-primary: #123465;
   --nova-primary-container: #2C4A7C; --nova-on-primary-container: #D9E3F5;
   --nova-secondary: #9FD3B3; --nova-on-secondary: #16382A;
   --nova-secondary-container: #2C4F3B; --nova-on-secondary-container: #D9EFE0;
   --nova-tertiary: #E4C46E; --nova-on-tertiary: #3D2F00;
   --nova-tertiary-container: #5C4900; --nova-on-tertiary-container: #F5E7C4;
   --nova-error: #F2B8B5; --nova-on-error: #601410;
   --nova-error-container: #8C1D18; --nova-on-error-container: #F9DEDC;
   --nova-background: #121317; --nova-on-background: #E3E2E6;
   --nova-surface: #121317; --nova-on-surface: #E3E2E6;
   --nova-surface-variant: #45464F; --nova-on-surface-variant: #C6C6D0;
   --nova-outline: #909099;

2. REMOVA todas as cores hardcoded atuais (vermelho, dourado, verde
   saturados nos cards de Saldo/Recebido/Gasto, gradiente rosa/roxo
   no botão de voz, glow neon nas bordas). Substitua pelo mapeamento:
   - Saldo Líquido → --nova-secondary-container / --nova-on-secondary-container
   - Total Recebido → --nova-tertiary-container / --nova-on-tertiary-container
   - Total Gasto → --nova-primary-container / --nova-on-primary-container
   - Estados de erro/saldo negativo → --nova-error-container / --nova-on-error-container
   - Botão principal de voz → --nova-primary sólido, sem gradiente

3. TOGGLE DE TEMA: adicione um botão no header, ao lado do seletor
   de voz, com ícone de sol/lua que alterna data-theme entre "light"
   e "dark" no elemento raiz. Requisitos:
   - Ícone anima com rotação + fade de 300ms na troca
   - Preferência salva em localStorage e restaurada ao recarregar
   - Se não houver preferência salva, usar prefers-color-scheme do
     sistema como padrão inicial
   - Toda troca de cor de fundo/texto no sistema usa transition de
     250ms ease, nunca corte abrupto
   - Aplique em TODAS as seções (Dashboard, Voice Studio, Finanças,
     Carreira, Estudos), não só na tela principal

4. Aplique isso de forma consistente em todos os componentes já
   existentes (cards, botões pill, gráficos Chart.js — as cores dos
   gráficos também devem usar os tokens, não paleta fixa).

Depois de implementar, tire prints do Dashboard em modo claro E
escuro, pra eu comparar os dois antes de você seguir pras outras telas.
```

---

*Depois que este comando rodar e você validar os dois modos no Dashboard, o mesmo padrão de tokens já vale para replicar nas demais seções (Finanças, Carreira, Estudos) sem precisar redefinir nada — é a vantagem de ter um token system único.*

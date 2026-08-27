# 🏆 NOVA — Frontend de Excelência & Guia de Marca

> Complementa o `nova-design-system.md`. Este documento cobre duas coisas: (1) a lógica e uso da nova marca do NOVA, (2) o padrão técnico que separa um dashboard "bonito" de um dashboard que impressiona um front-end sênior.

---

## 1. A Marca NOVA

### Lógica do símbolo
O ícone (`nova-logo.svg`) não é um sparkle genérico de "IA" — é a metáfora literal do produto: **4 formas orgânicas se fundindo num núcleo único**, uma para cada domínio core (Financeiro = dourado, Voz = verde, Dashboard = azul/núcleo dominante, Carreira = roxo). O anel pontilhado ao redor é uma referência sutil à origem cósmica do nome (Nova, Orion, Vega — a exploração de nomes que fizemos lá atrás).

### Como usar
- **Tamanho mínimo:** ícone sozinho não deve ser exibido abaixo de 24px (perde legibilidade do fundido)
- **Espaço de respiro:** sempre um espaço livre ao redor equivalente a ~20% da largura do ícone
- **Fundo escuro:** o wordmark atual usa `#1B1C1E` (texto escuro) — em telas dark mode, troque para `--nova-on-surface` do modo dark (`#E3E2E6`)
- **Nunca:** esticar desproporcionalmente, mudar as cores dos 4 blobs individualmente (eles são um sistema, não decoração solta), ou usar o ícone sem o anel pontilhado em contextos de marca (ok remover só em favicons muito pequenos)
- **Onde aplicar:** cabeçalho do sidebar (substitui o ícone atual), favicon, tela de loading/splash, possivelmente um watermark discreto nos PDFs de relatório gerados

---

## 2. O que separa "bonito" de "nível sênior"

Um front-end sênior não julga primeiro pela paleta — julga pelo que acontece nos **detalhes que a maioria ignora**. Esta é a lista real que costuma aparecer em code review sênior:

### Estados que você provavelmente não tem ainda
- [ ] **Loading state** de cada card (skeleton, não spinner genérico) — enquanto os dados do H2/MCP carregam
- [ ] **Empty state** com propósito (ex: "Nenhuma transação em setembro ainda" + call-to-action, não uma tela em branco)
- [ ] **Error state** na voz da interface (ex: "Não consegui falar com o serviço financeiro. Verifique se ele está rodando." — não um erro técnico cru tipo "Failed to fetch")
- [ ] **Estado de sucesso momentâneo** (ex: toast discreto "Transação registrada" após ação por voz)

### Acessibilidade (isso é o que mais denuncia trabalho amador)
- [ ] Foco de teclado **visível** em todo elemento interativo (outline customizado com os tokens de cor, não removido com `outline: none`)
- [ ] Contraste de texto mínimo AA (4.5:1) — validar especialmente texto claro sobre `--nova-primary-container`
- [ ] `aria-label` em botões que só têm ícone (ex: o microfone do Voice Orb)
- [ ] Respeitar `prefers-reduced-motion` — todo mundo com animação de orb/pulso precisa de fallback estático
- [ ] Ordem de tab lógica (segue a leitura visual, não a ordem do DOM se elas divergirem)

### Responsividade real (não só "não quebra")
- [ ] Testado em 3 breakpoints reais: mobile (375px), tablet (768px), desktop (1440px+)
- [ ] Sidebar vira navegação inferior ou drawer em mobile — não fica espremida
- [ ] Gráficos Chart.js redimensionam sem distorcer proporção
- [ ] Touch targets de no mínimo 44x44px em mobile (botões pill já ajudam nisso)

### Performance percebida
- [ ] Skeleton screens ao invés de tela branca durante fetch
- [ ] Otimistic UI em ações rápidas (ex: transação aparece na lista antes mesmo da confirmação do backend, com rollback silencioso se falhar)
- [ ] Sem "layout shift" — cards não pulam de posição quando o conteúdo carrega (reserve o espaço)

### Microinterações com propósito (não decoração)
- [ ] Hover em cards: leve elevação de sombra + scale 1.01, não mais que isso (M3 é sutil)
- [ ] Transição de número (ex: saldo mudando) anima contando, não só "pisca" o novo valor
- [ ] Voice Orb pulsa em sincronia real com o volume do áudio de saída (não é uma animação genérica de loop)

### Arquitetura de componentes (o que um sênior olha no código, não só na tela)
- [ ] Tokens de cor/tipografia centralizados (CSS custom properties já definidas no design system — nenhuma cor hardcoded solta em componentes)
- [ ] Componentes de card reutilizáveis (um único componente `Card`, parametrizado — não HTML duplicado pra cada seção)
- [ ] Separação clara entre dados (fetch/estado) e apresentação (JSX/HTML puro)

---

## 3. Comando para dar ao NOVA (aplicar tudo de uma vez seria arriscado — sugiro em 2 etapas)

### Etapa 1 — Marca + fundamentos
```
Aplique a nova identidade visual do NOVA usando o arquivo nova-logo.svg
como referência:

1. Substitua o ícone atual do sidebar (o círculo com raio/sparkle) pelo
   novo logo NOVA — use a versão apenas do ícone (os primeiros 200x200
   do viewBox) no tamanho compacto do sidebar, e a versão completa
   (ícone + wordmark) em qualquer tela de splash/loading, se existir.

2. Implemente os ESTADOS que faltam em cada card do Dashboard:
   - Loading: skeleton screen (retângulos com shimmer sutil) enquanto
     busca dados do backend financeiro/MCP
   - Empty: mensagem específica e propositiva quando não há dados
     (ex: sem transações no período)
   - Error: mensagem na voz da interface, nunca erro técnico cru

3. Implemente ACESSIBILIDADE básica: foco de teclado visível em
   todos os elementos interativos, aria-label no botão do microfone,
   contraste mínimo AA em todos os textos, respeito a
   prefers-reduced-motion nas animações do Voice Orb.

Depois de implementar, tire prints do Dashboard em 3 estados
diferentes (normal, loading, empty) pra eu revisar.
```

### Etapa 2 — Responsividade + polish (rodar depois de validar a Etapa 1)
```
Agora foque em responsividade real e microinterações:

1. Teste e ajuste o layout em 3 breakpoints: 375px (mobile), 768px
   (tablet), 1440px (desktop). A sidebar deve virar navegação
   inferior ou drawer em mobile.

2. Adicione microinterações sutis: hover em cards com leve elevação
   de sombra + scale 1.01 (não mais que isso), e animação de contagem
   nos números principais (saldo, totais) quando eles mudam de valor.

3. Sincronize a animação do Voice Orb com o volume real do áudio de
   saída, não um loop genérico.

4. Revise o código: centralize qualquer cor ainda hardcoded nos
   tokens CSS do design system, e garanta que os cards usem um único
   componente reutilizável.

Depois de implementar, tire prints em mobile e desktop pra eu revisar.
```

---

*Esse é o tipo de detalhe que, em uma entrevista técnica, você consegue explicar item por item — "implementei skeleton loading, respeitei prefers-reduced-motion, testei contraste AA" — e isso pesa muito mais do que só "fiz um dashboard bonito".*

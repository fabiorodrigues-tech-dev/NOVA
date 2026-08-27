# 🌌 NOVA — Splash Screen 3D (Convergência da Marca)

> Animação de abertura do app: os 4 blobs da marca (Financeiro/Voz/Dashboard/Carreira) entram separados em profundidade 3D, giram e convergem até se fundir no núcleo — a mesma metáfora do `nova-logo.svg`, agora em movimento.

---

## 1. Storyboard (4 fases, ~2.2s total)

| Fase | Tempo | O que acontece |
|---|---|---|
| **1. Dispersão** | 0 – 0ms (estado inicial) | Os 4 blobs aparecem espalhados em profundidades e ângulos diferentes no espaço 3D — como se estivessem "flutuando" desconectados |
| **2. Convergência girando** | 0 – 900ms | Os 4 blobs giram (rotateY/rotateX) e se movem em direção ao centro simultaneamente, com timing levemente escalonado (cada um começa ~60ms depois do anterior) |
| **3. Fusão + pulso** | 900 – 1300ms | Ao se encontrarem no centro, aplicamos o filtro "goo" (o mesmo do SVG) fazendo-os se fundirem organicamente; um pulso de escala (1 → 1.08 → 1) marca o momento da fusão, como um "batimento" |
| **4. Revelação** | 1300 – 1900ms | O anel orbital (pontilhado) desenha-se em volta (stroke-dashoffset animado), o wordmark "NOVA" faz fade-in com leve slide, e tudo dá fade-out revelando o Dashboard por trás |

**Regra de ouro:** só roda o storyboard completo (2.2s) no **primeiro carregamento da sessão**. Em navegações internas (trocar de seção), no máximo um "flash" rápido de 400ms do núcleo já fundido — nunca repita a cena toda, isso cansaria rápido.

---

## 2. Estrutura HTML

```html
<div id="nova-splash" class="nova-splash" role="status" aria-label="Carregando NOVA">
  <div class="nova-splash-scene">
    <div class="nova-blob nova-blob-financeiro"></div>
    <div class="nova-blob nova-blob-voz"></div>
    <div class="nova-blob nova-blob-dashboard"></div>
    <div class="nova-blob nova-blob-carreira"></div>
    <svg class="nova-splash-ring" viewBox="0 0 200 200">
      <circle cx="100" cy="100" r="90" fill="none" stroke="var(--nova-outline)"
        stroke-width="1.5" stroke-dasharray="4 10" stroke-linecap="round" />
    </svg>
  </div>
  <div class="nova-splash-wordmark">
    <span class="nova-splash-title">NOVA</span>
    <span class="nova-splash-subtitle">CONTROL CENTER</span>
  </div>
</div>
```

---

## 3. CSS (animação 3D completa)

```css
.nova-splash {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 24px;
  background: var(--nova-background);
  perspective: 1000px;
  animation: nova-splash-exit 400ms ease-in 1900ms forwards;
}

.nova-splash-scene {
  position: relative;
  width: 200px;
  height: 200px;
  transform-style: preserve-3d;
  filter: url(#novaGoo); /* reaproveita o filtro goo definido no nova-logo.svg */
}

.nova-blob {
  position: absolute;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  top: 60px;
  left: 60px;
  transform-style: preserve-3d;
  animation-duration: 900ms;
  animation-timing-function: cubic-bezier(0.34, 1.56, 0.64, 1); /* leve "overshoot", sensação de peso físico */
  animation-fill-mode: forwards;
}

.nova-blob-financeiro {
  background: var(--nova-tertiary);
  transform: translate3d(-140px, -80px, -200px) rotateY(-60deg) rotateX(30deg) scale(0.6);
  animation-name: nova-converge-1;
  animation-delay: 0ms;
}
.nova-blob-voz {
  background: var(--nova-secondary);
  transform: translate3d(140px, -100px, -160px) rotateY(70deg) rotateX(-20deg) scale(0.6);
  animation-name: nova-converge-2;
  animation-delay: 60ms;
}
.nova-blob-dashboard {
  background: var(--nova-primary);
  transform: translate3d(-120px, 110px, -220px) rotateY(-40deg) rotateX(-40deg) scale(0.7);
  animation-name: nova-converge-3;
  animation-delay: 120ms;
}
.nova-blob-carreira {
  background: #8E6FA5;
  transform: translate3d(130px, 100px, -180px) rotateY(50deg) rotateX(35deg) scale(0.6);
  animation-name: nova-converge-4;
  animation-delay: 180ms;
}

@keyframes nova-converge-1 {
  0%   { transform: translate3d(-140px, -80px, -200px) rotateY(-60deg) rotateX(30deg) scale(0.6); }
  75%  { transform: translate3d(4px, -4px, 0) rotateY(360deg) rotateX(15deg) scale(1); }
  85%  { transform: translate3d(0, 0, 0) rotateY(400deg) scale(1.08); }
  100% { transform: translate3d(0, 0, 0) rotateY(420deg) scale(1); }
}
@keyframes nova-converge-2 {
  0%   { transform: translate3d(140px, -100px, -160px) rotateY(70deg) rotateX(-20deg) scale(0.6); }
  75%  { transform: translate3d(-4px, -4px, 0) rotateY(-360deg) rotateX(-10deg) scale(1); }
  85%  { transform: translate3d(0, 0, 0) rotateY(-400deg) scale(1.08); }
  100% { transform: translate3d(0, 0, 0) rotateY(-420deg) scale(1); }
}
@keyframes nova-converge-3 {
  0%   { transform: translate3d(-120px, 110px, -220px) rotateY(-40deg) rotateX(-40deg) scale(0.7); }
  75%  { transform: translate3d(4px, 4px, 0) rotateY(300deg) rotateX(-15deg) scale(1); }
  85%  { transform: translate3d(0, 0, 0) rotateY(340deg) scale(1.08); }
  100% { transform: translate3d(0, 0, 0) rotateY(360deg) scale(1); }
}
@keyframes nova-converge-4 {
  0%   { transform: translate3d(130px, 100px, -180px) rotateY(50deg) rotateX(35deg) scale(0.6); }
  75%  { transform: translate3d(-4px, 4px, 0) rotateY(-300deg) rotateX(15deg) scale(1); }
  85%  { transform: translate3d(0, 0, 0) rotateY(-340deg) scale(1.08); }
  100% { transform: translate3d(0, 0, 0) rotateY(-360deg) scale(1); }
}

.nova-splash-ring {
  position: absolute;
  inset: -20px;
  width: 240px;
  height: 240px;
  opacity: 0;
  transform: scale(0.85) rotate(-30deg);
  animation: nova-ring-reveal 500ms ease-out 1000ms forwards;
}
.nova-splash-ring circle {
  stroke-dasharray: 565; /* aprox. 2*pi*90 */
  stroke-dashoffset: 565;
  animation: nova-ring-draw 900ms ease-out 1050ms forwards;
}

@keyframes nova-ring-reveal {
  to { opacity: 1; transform: scale(1) rotate(0deg); }
}
@keyframes nova-ring-draw {
  to { stroke-dashoffset: 0; }
}

.nova-splash-wordmark {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  opacity: 0;
  transform: translateY(12px);
  animation: nova-wordmark-in 500ms ease-out 1300ms forwards;
}
.nova-splash-title {
  font-family: 'Google Sans Text', 'Inter', sans-serif;
  font-size: 32px;
  font-weight: 500;
  letter-spacing: 1px;
  color: var(--nova-on-background);
}
.nova-splash-subtitle {
  font-family: 'Google Sans Text', 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 3px;
  color: var(--nova-on-surface-variant);
}
@keyframes nova-wordmark-in {
  to { opacity: 1; transform: translateY(0); }
}

@keyframes nova-splash-exit {
  to { opacity: 0; visibility: hidden; pointer-events: none; }
}

/* Acessibilidade: sem esta regra, a splash vira uma barreira ruim pra quem pediu menos movimento */
@media (prefers-reduced-motion: reduce) {
  .nova-splash-scene, .nova-blob, .nova-splash-ring, .nova-splash-ring circle, .nova-splash-wordmark {
    animation: none !important;
    transform: none !important;
    opacity: 1 !important;
    stroke-dashoffset: 0 !important;
  }
  .nova-splash { animation: nova-splash-exit 400ms ease-in 600ms forwards; }
}
```

---

## 4. JS (mostrar só uma vez por sessão)

```javascript
(function () {
  const hasSeenSplash = sessionStorage.getItem('nova-splash-shown');
  const splash = document.getElementById('nova-splash');

  if (hasSeenSplash) {
    splash.remove(); // não repete em navegações internas
    return;
  }

  sessionStorage.setItem('nova-splash-shown', 'true');

  // remove do DOM depois da animação de saída terminar (evita bloquear cliques)
  splash.addEventListener('animationend', (e) => {
    if (e.animationName === 'nova-splash-exit') splash.remove();
  });
})();
```

---

## 5. Comando para o NOVA

```
Implemente a splash screen 3D de abertura do NOVA Control Center,
usando exatamente o storyboard, HTML, CSS e JS abaixo (não invente
uma versão diferente — siga a especificação):

[HTML — inserir logo após a abertura da tag <body>]
[cole aqui o bloco HTML da seção 2]

[CSS — adicionar em styles.css]
[cole aqui o bloco CSS da seção 3]

[JS — adicionar em app.js ou script inline]
[cole aqui o bloco JS da seção 4]

Requisitos importantes:
1. A animação roda por completo (~2.2s) apenas no primeiro carregamento
   da sessão (controlado via sessionStorage) — NÃO repita em cada
   navegação interna entre Dashboard/Voice Studio/Finanças.
2. Respeite prefers-reduced-motion: se ativo, mostre a marca estática
   direto, sem a animação 3D.
3. O filtro "novaGoo" já existe no nova-logo.svg — reaproveite-o
   (pode ser referenciado via SVG inline ou <use>), não duplique a
   lógica de blend.
4. Depois de implementar, teste recarregando a página (deve rodar a
   animação) e depois navegando entre seções (não deve repetir).

Me mostre um GIF ou sequência de prints da animação, ou descreva o
comportamento observado, para eu validar antes de você seguir.
```

---

*Essa animação de convergência reforça a narrativa da marca toda vez que o app abre — é o tipo de "momento assinatura" que a skill de design de frontend chama de sinal de intenção: uma coisa memorável bem executada, em vez de várias animações genéricas espalhadas.*

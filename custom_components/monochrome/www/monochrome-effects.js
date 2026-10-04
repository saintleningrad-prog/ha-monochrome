// Monochrome — эффекты темы для Home Assistant: живой узор фона, шрифты, свечение текста, заставка,
// глич-эффект, подложка заголовков, текст плиток цвета иконки. Подключается интеграцией «monochrome»
// (frontend extra module). Без опроса интерфейса: всё по событиям (загрузка, переход, смена темы).
//
// Узор фона — алгоритм «2D Convolution» из проекта Fractogenesis, Serhii Herasymov
// (https://github.com/xcontcom/fractogenesis, MIT).
// Шрифты: «Monochrome VGA» — PxPlus IBM VGA 8x16, Ultimate Oldschool PC Font Pack, VileR (https://int10h.org),
// CC BY-SA 4.0; «Monochrome Mono» — JetBrains Mono, SIL OFL 1.1. Лицензии — в папке fonts/.
// Настройки из окна интеграции приходят параметрами URL модуля: glitch, every, boot, pattern.
(() => {
  if (window.__monochromeEffectsDone) return;
  window.__monochromeEffectsDone = true;

  const SELF = new URL(import.meta.url);
  const BASE = SELF.href.replace(/[^/]*$/, "");          // папка модуля (шрифты лежат в fonts/)
  const OPT = Object.fromEntries(SELF.searchParams);     // glitch=0|1, every=секунд, boot=0|1, pattern=0|1
  const optOn = (name, themeVal) => (OPT[name] === undefined ? themeVal : OPT[name] === "1");

  // шрифт: @font-face в документе действует и внутри shadow DOM интерфейса HA
  const FONT_FILES = [
    ["jbm-latin.woff2", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"],
    ["jbm-latin-ext.woff2", "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF"],
    ["jbm-cyrillic.woff2", "U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116"],
    ["jbm-cyrillic-ext.woff2", "U+0460-052F, U+1C80-1C8A, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F"],
  ];
  const fontStyle = document.createElement("style");
  fontStyle.textContent = FONT_FILES.map(([file, range]) =>
    `@font-face{font-family:'Monochrome Mono';font-style:normal;font-weight:100 800;font-display:swap;` +
    `src:url('${BASE}fonts/${file}') format('woff2');unicode-range:${range};}`).join("\n");
  fontStyle.textContent += "\n@font-face{font-family:'Monochrome VGA';font-style:normal;font-weight:400;" +
    "font-display:swap;src:url('" + BASE + "fonts/WebPlus_IBM_VGA_8x16.woff') format('woff');}";
  document.head.appendChild(fontStyle);

  // свечение люминофора: text-shadow наследуется внутрь всего интерфейса; без темы Monochrome — none
  (document.body || document.documentElement).style.textShadow = "var(--monochrome-glow, none)";

  const rootVar = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

  // Заставка «загрузки терминала»: один раз за сеанс браузера, если в прошлый раз была тема Monochrome.
  // (тема применяется позже загрузки модуля, поэтому признак запоминаем в localStorage)
  function boot() {
    let was = null;
    try { was = localStorage.getItem("monochromeBoot"); if (sessionStorage.getItem("monochromeBooted")) return; } catch (e) { return; }
    if (was !== "1") return;
    try { sessionStorage.setItem("monochromeBooted", "1"); } catch (e) {}
    let color = "#00ff41", font = "monospace", bg = "#000";
    try {
      color = localStorage.getItem("monochromeBootColor") || color;
      font = localStorage.getItem("monochromeBootFont") || font;
      bg = localStorage.getItem("monochromeBootBg") || bg;
    } catch (e) {}
    const ov = document.createElement("div");
    ov.style.cssText = `position:fixed;inset:0;z-index:2147483647;background:${bg};color:${color};` +
      `font:18px/1.5 ${font};padding:6vh 6vw;white-space:pre;cursor:pointer;` +
      `text-shadow:0 0 4px ${color};transition:opacity .35s;` +
      `background-image:repeating-linear-gradient(0deg,rgba(0,0,0,.35) 0 1px,transparent 1px 3px)`;
    document.body.appendChild(ov);
    const lines = ["HOME ASSISTANT BIOS  v" + ((window.__hassVersion) || "2026"),
      "MEMORY TEST ............ 640K OK", "NETWORK LINK ........... OK",
      "ZIGBEE COORDINATOR ..... OK", "LOADING DASHBOARD ...", "", "READY_"];
    let i = 0;
    const done = () => { ov.style.opacity = "0"; setTimeout(() => ov.remove(), 400); };
    ov.addEventListener("click", done);
    const step = () => {
      ov.textContent = lines.slice(0, ++i).join("\n");
      if (i < lines.length) setTimeout(step, 170); else setTimeout(done, 450);
    };
    step();
  }
  boot();

  // Заголовки карточек и разделов: подложка/свечение из переменных темы (--monochrome-title-*).
  // В темах без этих переменных стиль ничего не меняет (запасные значения — как у HA).
  const TITLE_CSS = `
    .card-header, .title {
      background: var(--monochrome-title-bg, none);
      background-clip: var(--monochrome-title-clip, border-box);
      box-shadow: var(--monochrome-title-ring, none);
      text-shadow: var(--monochrome-title-shadow, none);
      width: var(--monochrome-title-width, auto);
      border-radius: var(--monochrome-title-radius, 0);
    }
    .card-header {
      line-height: var(--monochrome-title-lh, var(--ha-line-height-expanded, 48px));
    }`;
  // Плитки: название и состояние того же цвета, что иконка (--tile-color вычисляет сама плитка).
  // Правило статичное — браузер сам перекрашивает текст при смене состояния, без опроса.
  // Вставляется только если в теме есть monochrome-tile-follow-icon: 1 (темы Monochrome).
  const TILE_CSS = `
    ha-tile-info {
      --ha-tile-info-primary-color: var(--tile-color);
      --ha-tile-info-secondary-color: var(--tile-color);
    }`;
  const MARK = "monochromeTitleStyle", TILE_MARK = "monochromeTileStyle";
  function addStyle(sr, css) {
    const st = document.createElement("style");
    st.textContent = css;
    sr.appendChild(st);
  }
  function injectTitles(root) {
    const walk = node => {
      const sr = node.shadowRoot;
      if (sr) {
        const tag = node.localName;
        if ((tag === "ha-card" || tag === "hui-heading-card") && !sr[MARK]) {
          addStyle(sr, TITLE_CSS);
          sr[MARK] = true;
        }
        // логотип и картинки в picture-карточках — в цвет люминофора (фильтр из --monochrome-image-filter)
        if (tag === "hui-picture-card" && !sr[MARK]) {
          addStyle(sr, "img[src*=\"#monochrome-tint\"] { filter: var(--monochrome-image-filter, none); }");
          sr[MARK] = true;
        }
        if (tag === "hui-tile-card" && !sr[TILE_MARK] &&
            getComputedStyle(node).getPropertyValue("--monochrome-tile-follow-icon").trim() === "1") {
          addStyle(sr, TILE_CSS);
          sr[TILE_MARK] = true;
        }
        sr.querySelectorAll("*").forEach(walk);
      }
    };
    root.querySelectorAll("*").forEach(walk);
  }
  // Обработка заголовков только по событиям, без постоянного опроса: при загрузке страницы,
  // переходе между вкладками и возврате на страницу — несколько проходов, т.к. карточки рисуются с задержкой.
  const idle = window.requestIdleCallback || (f => setTimeout(f, 200));
  let timers = [];
  function burst() {
    timers.forEach(clearTimeout);
    timers = [300, 1200, 3000].map(ms => setTimeout(() => idle(() => injectTitles(document)), ms));
  }
  burst();
  window.addEventListener("location-changed", burst);
  window.addEventListener("popstate", burst);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) burst(); });

  // размер поля под экран: 1024 на телефонах/планшетах, 2048 на компьютерах с большим экраном
  function pickSizeLog2() {
    const px = Math.max(screen.width, screen.height) * (window.devicePixelRatio || 1);
    const touch = window.matchMedia && window.matchMedia("(pointer: coarse)").matches;
    return !touch && px > 1600 ? 11 : 10;
  }
  const SIZE_LOG2 = pickSizeLog2();
  const G_BASE = 4, G_AMP = 52;        // зелёный канал: от 4 до 56 из 255 (~+10% яркости к первой версии)

  function padding(a, n) {             // n → 2n: значения в чётные клетки, остальные нули
    const m = n * 2, t = new Float32Array(m * m);
    for (let x = 0; x < n; x++)
      for (let y = 0; y < n; y++) t[(x * 2) * m + y * 2] = a[x * n + y];
    return t;
  }

  function convolve(a, n, k) {         // свёртка 3x3 с заворачиванием краёв
    const t = new Float32Array(n * n);
    for (let x = 0; x < n; x++) {
      const xm = (x - 1 + n) % n, xp = (x + 1) % n;
      for (let y = 0; y < n; y++) {
        const ym = (y - 1 + n) % n, yp = (y + 1) % n;
        t[x * n + y] =
          a[xm * n + ym] * k[0] + a[x * n + ym] * k[1] + a[xp * n + ym] * k[2] +
          a[xm * n + y] * k[3] + a[x * n + y] * k[4] + a[xp * n + y] * k[5] +
          a[xm * n + yp] * k[6] + a[x * n + yp] * k[7] + a[xp * n + yp] * k[8];
      }
    }
    return t;
  }

  function generate() {
    const k = [];
    for (let i = 0; i < 5; i++) { k[i] = (Math.random() - 0.5) * 2; k[8 - i] = k[i]; }
    let a = new Float32Array([1]), n = 1;
    for (let i = 0; i < SIZE_LOG2; i++) { a = padding(a, n); n *= 2; a = convolve(a, n, k); }

    // нормализация по 1-му и 99-му перцентилям выборки
    const sample = [];
    for (let i = 0; i < 40000; i++) sample.push(a[(Math.random() * a.length) | 0]);
    sample.sort((p, q) => p - q);
    const low = sample[(sample.length * 0.01) | 0], high = sample[(sample.length * 0.99) | 0];
    const range = (high - low) || 1;

    // плавные полосы светлее/темнее (0…1), как цикл оттенка в оригинале
    const shift = Math.random(), wave = new Float32Array(n * n);
    for (let i = 0; i < a.length; i++) {
      const v = Math.min(1, Math.max(0, (a[i] - low) / range));
      wave[i] = 0.5 - 0.5 * Math.cos(2 * Math.PI * (v + shift));
    }
    return { n, wave };
  }

  let TR = 0, TG = 1, TB = 0.18;       // оттенок узора (по умолчанию зелёный), из --monochrome-bg-tint
  let LIGHT = false;                   // светлый узор (--monochrome-bg-mode: light)
  function render({ n, wave }) {       // чёрный → цвет люминофора
    const c = document.createElement('canvas');
    c.width = c.height = n;
    const ctx = c.getContext('2d');
    const img = ctx.createImageData(n, n), d = img.data;
    for (let x = 0; x < n; x++)
      for (let y = 0; y < n; y++) {
        // лёгкий дизеринг (±0.5 уровня) убирает «ступеньки» на тёмных плавных переходах
        const v = G_BASE + G_AMP * wave[x * n + y];
        const i = (y * n + x) * 4;
        // светлая тема (--monochrome-bg-mode: light): белый фон с едва заметными серыми разводами
        const L = LIGHT ? 255 - v * 0.45 : 0;
        d[i] = Math.round((LIGHT ? L : v * TR) + Math.random() - 0.5);
        d[i + 1] = Math.round((LIGHT ? L : v * TG) + Math.random() - 0.5);
        d[i + 2] = Math.round((LIGHT ? L : v * TB) + Math.random() - 0.5);
        d[i + 3] = 255;
      }
    ctx.putImageData(img, 0, 0);
    return c;
  }

  function apply(tint) {
    try {
      [TR, TG, TB] = tint.split(/[ ,]+/).map(Number);
      LIGHT = rootVar("--monochrome-bg-mode") === "light";
      const canvas = render(generate());
      canvas.toBlob(blob => {
        if (!blob) return;
        const url = URL.createObjectURL(blob);
        document.documentElement.style.setProperty("--monochrome-bg-img", `url("${url}")`);
        // совместимость со старой схемой темы (lovelace-background: var(--monochrome-bg))
        document.documentElement.style.setProperty("--monochrome-bg", `#000 url("${url}") center / cover fixed`);
      }, "image/webp", 0.95);   // где WebP не поддерживается, браузер сам отдаст PNG
    } catch (e) {
      console.warn("monochrome-effects: не удалось построить узор", e);
    }
  }

  // Глич-эффект: редкий короткий «сбой сигнала» поверх всего интерфейса (полосы с инверсией/пересветом,
  // сдвиг вбок, цветовой разъезд текста). Один таймер, без обхода DOM; на скрытой вкладке и при
  // «уменьшить движение» не срабатывает. Включение и частота — из темы: --monochrome-glitch (1/0),
  // --monochrome-glitch-every (среднее число секунд между сбоями).
  const reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function glitch() {
    const host = document.createElement("div");
    host.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:2147483646;overflow:hidden";
    const strips = [];
    const n = 2 + Math.floor(Math.random() * 3);
    for (let i = 0; i < n; i++) {
      const s = document.createElement("div");
      const fx = Math.random() < 0.5 ? "invert(1)" : "brightness(1.9) contrast(1.6)";
      s.style.cssText = `position:absolute;left:0;right:0;backdrop-filter:${fx};-webkit-backdrop-filter:${fx}`;
      host.appendChild(s);
      strips.push(s);
    }
    document.body.appendChild(host);
    const body = document.body, prevShadow = body.style.textShadow;
    body.style.textShadow = "-2px 0 rgba(255,0,60,0.7), 2px 0 rgba(0,220,255,0.7)";
    let frame = 0;
    const tick = () => {
      strips.forEach(s => {
        s.style.top = (Math.random() * 100).toFixed(1) + "%";
        s.style.height = (0.4 + Math.random() * 4).toFixed(2) + "%";
        s.style.transform = `translateX(${Math.round((Math.random() - 0.5) * 40)}px)`;
      });
      if (++frame < 5) setTimeout(tick, 45 + Math.random() * 30);
      else { host.remove(); body.style.textShadow = prevShadow; }
    };
    tick();
  }
  (function glitchLoop() {
    const every = parseFloat(OPT.every) || parseFloat(rootVar("--monochrome-glitch-every")) || 25;
    const delay = (every * (0.6 + Math.random() * 0.8)) * 1000;   // ±40% от среднего
    setTimeout(() => {
      if (!reduceMotion && !document.hidden && optOn("glitch", rootVar("--monochrome-glitch") === "1")) glitch();
      glitchLoop();
    }, delay);
  })();

  // Смена темы в профиле: HA переписывает переменные в style у <html>. Следим только за этим атрибутом
  // (срабатывает лишь в момент смены темы) и перерисовываем узор, если изменился его оттенок.
  let lastTint = "";
  new MutationObserver(() => {
    const tint = rootVar("--monochrome-bg-tint"), key = tint + "|" + rootVar("--monochrome-bg-mode");
    if (tint && key !== lastTint && optOn("pattern", rootVar("--monochrome-pattern") !== "0")) {
      lastTint = key;
      idle(() => apply(tint));
    }
  }).observe(document.documentElement, { attributes: true, attributeFilter: ["style"] });

  // ждём, пока HA применит тему (до 10 с, короткими проверками). Нет темы Monochrome — узор не строим.
  let tries = 0;
  (function waitTheme() {
    const tint = rootVar("--monochrome-bg-tint");
    if (tint) {
      const key = tint + "|" + rootVar("--monochrome-bg-mode");
      if (key === lastTint) return;    // уже построен наблюдателем
      lastTint = key;
      try {
        localStorage.setItem("monochromeBoot", optOn("boot", rootVar("--monochrome-boot") === "1") ? "1" : "0");
        localStorage.setItem("monochromeBootColor", rootVar("--primary-text-color") || "#00ff41");
        localStorage.setItem("monochromeBootFont", rootVar("--ha-font-family-body") || "monospace");
        localStorage.setItem("monochromeBootBg", rootVar("--primary-background-color") || "#000");
      } catch (e) {}
      if (optOn("pattern", rootVar("--monochrome-pattern") !== "0")) idle(() => apply(tint));
      return;
    }
    if (++tries < 40) setTimeout(waitTheme, 250);
    else try { localStorage.setItem("monochromeBoot", "0"); } catch (e) {}
  })();
})();

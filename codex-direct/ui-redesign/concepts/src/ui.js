// Concept helpers: chamfered frames (panels, buttons, wells) and line icons. Runs before the screenshot.
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const ICONS = {
    menu: "M4 7h16M4 12h16M4 17h16",
    "chev-l": "M15 5l-7 7 7 7", "chev-r": "M9 5l7 7-7 7",
    check: "M5 12l5 5 9-10",
    note: "M9 18V6l10-2v12M9 18a3 2.4 0 11-6 0 3 2.4 0 016 0zM19 16a3 2.4 0 11-6 0 3 2.4 0 016 0z",
    prev: "M18 5v14L8 12zM6 5v14", next: "M6 5v14l10-7zM18 5v14",
    speed: "M4 16a8 8 0 1116 0M12 16l4-6M4 16h16",
    bolt: "M13 2L5 14h6l-1 8 8-12h-6z",
    coin: "M12 3a9 9 0 100 18 9 9 0 000-18zM12 7l5 5-5 5-5-5z",
    silo: "M6 7c0-2 12-2 12 0v11c0 2-12 2-12 0zM6 7c0 2 12 2 12 0M6 12c0 2 12 2 12 0",
    build: "M3 21V11l5-3v3l5-3v13M13 21V4h8v17M2 21h20M16 8h2M16 12h2M16 16h2",
    infantry: "M12 3a4 4 0 100 8 4 4 0 000-8zM7 7h10M5 21c0-5 3-7 7-7s7 2 7 7",
    tank: "M2 15h20l-2 5H4zM6 15v-4h9v4M15 12h7M6 20h12",
    ship: "M12 2c3 3 4 7 4 11H8c0-4 1-8 4-11zM8 13l-4 5h5M16 13l4 5h-5M10 18v3M14 18v3M12 7v3",
    palace: "M4 21v-8a8 8 0 0116 0v8M12 5V2M10 3h4M9 21v-5a3 3 0 016 0v5M2 21h20",
    upgrade: "M6 12l6-6 6 6M6 19l6-6 6 6",
    move: "M4 12h13M11 5l7 7-7 7", attack: "M12 4a8 8 0 100 16 8 8 0 000-16zM12 1v6M12 17v6M1 12h6M17 12h6",
    repair: "M14 6a4.5 4.5 0 006 6l-9.5 9.5a2 2 0 01-3-3L17 9M14 6l3 3",
    unload: "M12 3v10M7 9l5 5 5-5M4 16v4h16v-4", deploy: "M3 21h18M6 21V11l6-5 6 5v10M10 21v-5h4v5",
    rally: "M6 22V3M6 4h12l-3 4 3 4H6", release: "M12 15V4M7 8l5-5 5 5M4 13v7h16v-7",
    save: "M5 4h11l3 3v13H5zM8 4v5h7V4M8 20v-6h8v6", load: "M3 7h6l2 2h10v10H3zM12 12v5M9.5 14.5L12 17l2.5-2.5",
    lock: "M6 11h12v9H6zM8 11V8a4 4 0 018 0v3", clock: "M12 3a9 9 0 100 18 9 9 0 000-18zM12 7v5l3 2",
    warn: "M12 3l10 17H2zM12 10v5M12 17.5v.5", info: "M12 3a9 9 0 100 18 9 9 0 000-18zM12 11v6M12 7.5v.5",
    radar: "M12 3a9 9 0 109 9M12 7a5 5 0 105 5M12 12l7-7",
    star: "M12 3l2.7 5.8 6.3.7-4.7 4.3 1.3 6.2L12 17l-5.6 3 1.3-6.2L3 9.5l6.3-.7z",
    map: "M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2zM9 4v14M15 6v14",
    users: "M9 4a3.5 3.5 0 100 7 3.5 3.5 0 000-7zM2 21c0-4 3-6 7-6s7 2 7 6M17 5a3 3 0 010 6M19 15c2 1 3 3 3 6",
    dice: "M4 4h16v16H4zM8.5 8.5v.1M15.5 8.5v.1M12 12v.1M8.5 15.5v.1M15.5 15.5v.1", play: "M7 4l12 8-12 8z",
    gear: "M12 8.5a3.5 3.5 0 100 7 3.5 3.5 0 000-7zM12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.2 2.2M16.9 16.9l2.2 2.2M4.9 19.1l2.2-2.2M16.9 7.1l2.2-2.2",
    exit: "M10 4H4v16h6M14 8l4 4-4 4M8 12h10", back: "M9 6l-6 6 6 6M3 12h18",
    shield: "M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z", edit: "M4 20h4L19 9l-4-4L4 16zM13 7l4 4",
    grid: "M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z", plus: "M12 5v14M5 12h14",
  };
  const css = getComputedStyle(document.documentElement);
  const tok = function (name) { return css.getPropertyValue("--" + name).trim(); };
  const EDGE = tok("edge");
  const frameOf = function (top, bot, rim1, rim2, rim3, inner, hi) { return { top: top, bot: bot, rim1: tok(rim1), rim2: tok(rim2), rim3: tok(rim3), edge: EDGE, inner: inner, hi: hi }; };
  const PAL = {
    panel:    frameOf(tok("g3"), tok("g2"), "brass-hi", "brass-mid", "brass", "rgba(0,0,0,.55)", "rgba(255,255,255,.06)"),
    glass:    frameOf("rgba(28,36,42,.92)", "rgba(21,27,32,.95)", "brass-hi", "brass-mid", "brass", "rgba(0,0,0,.55)", "rgba(255,255,255,.06)"),
    well:     frameOf(tok("g0"), tok("g0"), "brass-lo", "brass-mid", "brass-lo", "rgba(0,0,0,.7)", "rgba(0,0,0,0)"),
    btn:      frameOf(tok("g4"), tok("g2"), "brass", "brass-lo", "brass-mid", "rgba(0,0,0,.45)", "rgba(255,255,255,.10)"),
    hover:    frameOf(tok("g5"), tok("g3"), "brass-top", "brass", "brass-hi", "rgba(0,0,0,.4)", "rgba(255,255,255,.16)"),
    pressed:  frameOf(tok("g1"), tok("g2"), "brass-mid", "brass", "brass", "rgba(0,0,0,.75)", "rgba(0,0,0,.35)"),
    disabled: frameOf(tok("g2"), tok("g1"), "rim-off", "rim-off-lo", "rim-off", "rgba(0,0,0,.3)", "rgba(255,255,255,.03)"),
    selected: frameOf(tok("sel-hi"), tok("sel-lo"), "brass-top", "brass", "brass-hi", "rgba(0,0,0,.4)", "rgba(255,255,255,.14)"),
    primary:  frameOf(tok("gold-hi"), tok("gold-lo"), "brass-top", "brass-mid", "brass-hi", "rgba(90,60,10,.45)", "rgba(255,255,255,.5)"),
    primaryh: frameOf(tok("gold-top"), tok("gold-lo2"), "brass-top", "brass-mid", "brass-top", "rgba(90,60,10,.4)", "rgba(255,255,255,.6)"),
  };

  let uid = 0;
  function path(w, h, c, i) {
    const k = Math.max(0, c - i * 0.414);
    return "M" + (i + k) + "," + i + "H" + (w - i - k) + "L" + (w - i) + "," + (i + k) + "V" + (h - i - k) +
      "L" + (w - i - k) + "," + (h - i) + "H" + (i + k) + "L" + i + "," + (h - i - k) + "V" + (i + k) + "Z";
  }
  function el(name, attrs, parent) {
    const node = document.createElementNS(NS, name);
    for (const key in attrs) node.setAttribute(key, attrs[key]);
    if (parent) parent.appendChild(node);
    return node;
  }
  function frame(target, pal, c) {
    const w = target.offsetWidth, h = target.offsetHeight;
    if (!w || !h) return;
    const id = "f" + (uid++);
    const svg = el("svg", { class: "fr", viewBox: "0 0 " + w + " " + h, preserveAspectRatio: "none" });
    const defs = el("defs", {}, svg);
    const fill = el("linearGradient", { id: id + "a", x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
    el("stop", { offset: 0, "stop-color": pal.top }, fill); el("stop", { offset: 1, "stop-color": pal.bot }, fill);
    const rim = el("linearGradient", { id: id + "b", x1: 0, y1: 0, x2: 1, y2: 1 }, defs);
    el("stop", { offset: 0, "stop-color": pal.rim1 }, rim); el("stop", { offset: .55, "stop-color": pal.rim2 }, rim); el("stop", { offset: 1, "stop-color": pal.rim3 }, rim);
    el("path", { d: path(w, h, c, 0), fill: pal.edge }, svg);
    el("path", { d: path(w, h, c, 1), fill: "url(#" + id + "b)" }, svg);
    el("path", { d: path(w, h, c, 2), fill: "url(#" + id + "a)" }, svg);
    if (target.dataset.noise !== "0" && w * h > 6000) {
      const pat = el("pattern", { id: id + "n", width: 160, height: 160, patternUnits: "userSpaceOnUse" }, defs);
      const flt = el("filter", { id: id + "t", x: 0, y: 0, width: "100%", height: "100%" }, defs);
      el("feTurbulence", { type: "fractalNoise", baseFrequency: ".8", numOctaves: 2, stitchTiles: "stitch" }, flt);
      el("feColorMatrix", { values: "0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .055 0" }, flt);
      el("rect", { width: 160, height: 160, filter: "url(#" + id + "t)" }, pat);
      el("path", { d: path(w, h, c, 2), fill: "url(#" + id + "n)" }, svg);
    }
    el("path", { d: path(w, h, c, 2.5), fill: "none", stroke: pal.inner, "stroke-width": 1 }, svg);
    const k = Math.max(0, c - 3 * 0.414);
    el("path", { d: "M" + (3 + k) + ",3.5H" + (w - 3 - k), stroke: pal.hi, "stroke-width": 1, fill: "none" }, svg);
    target.insertBefore(svg, target.firstChild);
  }
  function buttonPalette(node) {
    const has = (name) => node.classList.contains(name);
    if (has("primary") && !has("disabled")) return has("hover") ? PAL.primaryh : PAL.primary;
    for (const name of ["disabled", "pressed", "selected", "hover"]) if (has(name)) return PAL[name];
    return PAL.btn;
  }
  function icons() {
    document.querySelectorAll("i[data-i]").forEach((node) => {
      const svg = el("svg", { class: "ico " + (node.className || ""), viewBox: "0 0 24 24" });
      if (node.getAttribute("style")) svg.setAttribute("style", node.getAttribute("style"));
      el("path", { d: ICONS[node.dataset.i] || "" }, svg);
      node.replaceWith(svg);
    });
  }
  function run() {
    icons();
    document.querySelectorAll(".panel").forEach((node) => frame(node, node.classList.contains("glass") ? PAL.glass : PAL.panel, +(node.dataset.c || 10)));
    document.querySelectorAll(".wellf").forEach((node) => frame(node, PAL.well, +(node.dataset.c || 4)));
    document.querySelectorAll(".btn").forEach((node) => frame(node, buttonPalette(node), +(node.dataset.c || (node.offsetHeight >= 40 ? 6 : 4))));
    document.documentElement.dataset.ready = "1";
  }
  window.duneUi = { run: run, frame: frame, PAL: PAL, ICONS: ICONS };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { requestAnimationFrame(run); });
  else window.addEventListener("load", run);
})();

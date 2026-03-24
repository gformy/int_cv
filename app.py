#!/usr/bin/env python3
"""
Snake CV — Curriculum Vitae interattivo stile Snake
Avvia con: python app.py
Apri il browser su: http://localhost:5000
"""

from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>🐍 Snake CV</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

  :root {
    --bg:       #050d0a;
    --grid:     #0a1f14;
    --snake1:   #00ff88;
    --snake2:   #00cc66;
    --head:     #00ffaa;
    --glow:     rgba(0,255,136,0.35);
    --text:     #00ff88;
    --dim:      #1a5c38;
    --panel:    #091a10;
    --border:   #00ff8855;
    --food-glow: rgba(255,220,0,0.5);
    --info-bg:  rgba(0,15,8,0.97);
    --accent:   #00ffaa;
  }

  * { margin:0; padding:0; box-sizing:border-box; -webkit-tap-highlight-color:transparent; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Share Tech Mono', monospace;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
    touch-action: none;
  }

  /* ── HEADER ── */
  header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 16px;
    border-bottom: 1px solid var(--border);
    background: var(--panel);
    flex-shrink: 0;
  }
  .logo {
    font-family: 'Orbitron', monospace;
    font-size: clamp(13px,2.5vw,20px);
    font-weight: 900;
    color: var(--head);
    text-shadow: 0 0 12px var(--glow);
    letter-spacing: 2px;
  }
  .logo span { color: #ffd700; text-shadow: 0 0 10px rgba(255,215,0,0.6); }
  .score-box {
    display: flex;
    gap: 20px;
    font-size: clamp(10px,1.8vw,14px);
    letter-spacing: 1px;
  }
  .score-box div { display:flex; flex-direction:column; align-items:center; gap:2px; }
  .score-box .lbl { color: var(--dim); font-size: 9px; letter-spacing: 2px; }
  .score-box .val { color: var(--accent); font-weight:bold; }

  /* ── MAIN LAYOUT ── */
  main {
    display: flex;
    flex: 1;
    width: 100%;
    max-width: 960px;
    gap: 12px;
    padding: 10px;
    justify-content: center;
    align-items: flex-start;
    overflow: hidden;
  }

  /* ── CANVAS WRAPPER ── */
  #canvas-wrap {
    position: relative;
    flex-shrink: 0;
  }
  canvas {
    display: block;
    border: 2px solid var(--border);
    box-shadow: 0 0 20px var(--glow), inset 0 0 40px rgba(0,30,15,0.5);
    border-radius: 4px;
    background: var(--grid);
  }

  /* ── SIDE PANEL ── */
  #side-panel {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 300px;
  }

  .panel-box {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 12px;
  }
  .panel-box h3 {
    font-family: 'Orbitron', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: var(--dim);
    margin-bottom: 8px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 6px;
  }

  /* Progress bars */
  .skill-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 5px 0;
    font-size: 11px;
  }
  .skill-name { width: 80px; color: #aaa; flex-shrink:0; }
  .skill-bar { flex:1; height: 6px; background: #0a2014; border-radius: 3px; overflow:hidden; }
  .skill-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--snake2), var(--head));
    transition: width 0.6s ease;
    width: 0%;
    box-shadow: 0 0 6px var(--glow);
  }

  /* Collected info list */
  #info-list {
    max-height: 200px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--dim) transparent;
  }
  .info-item {
    display: flex;
    gap: 8px;
    align-items: flex-start;
    padding: 5px 0;
    border-bottom: 1px solid #0a1f14;
    font-size: 11px;
    animation: fadeIn 0.4s ease;
  }
  .info-item .cat { font-size: 14px; flex-shrink:0; }
  .info-item .txt { color: #ccc; line-height: 1.4; }
  @keyframes fadeIn { from{opacity:0;transform:translateX(-8px)} to{opacity:1;transform:none} }

  /* ── OVERLAY SCREENS ── */
  .overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(5,13,10,0.92);
    gap: 16px;
    border-radius: 4px;
    z-index: 20;
  }
  .overlay h2 {
    font-family: 'Orbitron', monospace;
    font-size: clamp(18px,4vw,32px);
    color: var(--head);
    text-shadow: 0 0 20px var(--glow);
    letter-spacing: 3px;
    text-align: center;
  }
  .overlay p {
    color: #aaa;
    font-size: clamp(10px,2vw,14px);
    text-align: center;
    line-height: 1.8;
    padding: 0 20px;
  }
  .btn {
    background: transparent;
    border: 2px solid var(--head);
    color: var(--head);
    font-family: 'Orbitron', monospace;
    font-size: clamp(11px,2vw,15px);
    letter-spacing: 2px;
    padding: 10px 28px;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.2s;
    box-shadow: 0 0 10px var(--glow);
  }
  .btn:hover, .btn:active {
    background: var(--head);
    color: var(--bg);
    box-shadow: 0 0 20px var(--glow);
  }



  /* ── MOBILE DPAD ── */
  #dpad {
    display: none;
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 30;
  }
  .dpad-grid {
    display: grid;
    grid-template-columns: repeat(3, 54px);
    grid-template-rows: repeat(3, 54px);
    gap: 4px;
  }
  .dpad-btn {
    background: rgba(0,255,136,0.08);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text);
    font-size: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    user-select: none;
    transition: background 0.1s;
    touch-action: manipulation;
  }
  .dpad-btn:active { background: rgba(0,255,136,0.25); }
  .dpad-center { background: rgba(0,255,136,0.04); pointer-events:none; }

  /* ── SPEED CONTROL ── */
  #speed-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 11px;
    color: var(--dim);
    letter-spacing: 1px;
  }
  #speed-wrap input { accent-color: var(--head); flex:1; cursor:pointer; }

  /* ── LEGEND ── */
  .legend-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    margin: 3px 0;
    color: #aaa;
  }
  .legend-dot {
    width: 14px;
    height: 14px;
    border-radius: 3px;
    flex-shrink: 0;
  }

  /* ── RESPONSIVE ── */
  @media (max-width: 640px) {
    main { flex-direction: column; align-items: center; padding: 6px; gap:6px; }
    #side-panel { max-width: 100%; width: 100%; flex-direction: row; flex-wrap: wrap; }
    .panel-box { flex: 1; min-width: 140px; }
    #info-list { max-height: 100px; }
    #dpad { display: block; }
    body { overflow: auto; }
    main { padding-bottom: 200px; }
    #speed-wrap { display: none; }
  }
  @media (min-width: 641px) {
    #dpad { display: none !important; }
  }

  /* Scanlines effect */
  #canvas-wrap::after {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0,0,0,0.04) 2px,
      rgba(0,0,0,0.04) 4px
    );
    pointer-events: none;
    border-radius: 4px;
  }
</style>
</head>
<body>

<header>
  <div class="logo">🐍 SNAKE <span>CV</span></div>
  <div class="score-box">
    <div><span class="lbl">PUNTI</span><span class="val" id="score">0</span></div>
    <div><span class="lbl">RECORD</span><span class="val" id="hiscore">0</span></div>
    <div><span class="lbl">SEZIONI</span><span class="val" id="collected">0/{{ total }}</span></div>
  </div>
</header>

<main>
  <div id="canvas-wrap">
    <canvas id="c"></canvas>


    <!-- Start screen -->
    <div class="overlay" id="start-screen">
      <h2>🐍 SNAKE CV</h2>
      <p>Mangia le informazioni del curriculum!<br>
         Ogni cibo rivela un dato del candidato.<br>
         <br>
         ← → ↑ ↓ &nbsp;|&nbsp; WASD &nbsp;|&nbsp; SWIPE
      </p>
      <button class="btn" onclick="startGame()">▶ INIZIA</button>
    </div>

    <!-- Game over screen -->
    <div class="overlay" id="gameover-screen" style="display:none">
      <h2>GAME OVER</h2>
      <p id="go-score"></p>
      <button class="btn" id="go-btn" onclick="startGame()">↺ CONTINUA CAMPAGNA</button>
      <button class="btn" style="font-size:10px;padding:7px 18px;opacity:0.5;border-color:var(--dim);color:var(--dim);" onclick="resetCampaign();startGame()">✕ RICOMINCIA DA ZERO</button>
    </div>

    <!-- Win screen — riepilogo completo -->
    <div class="overlay" id="win-screen" style="display:none;overflow-y:auto;align-items:flex-start;padding:20px 16px;justify-content:flex-start;">
      <div style="width:100%;max-width:560px;margin:0 auto;display:flex;flex-direction:column;gap:16px;">
        <div style="text-align:center;padding:10px 0 4px;">
          <h2 style="font-family:'Orbitron',monospace;font-size:clamp(16px,4vw,26px);color:var(--head);text-shadow:0 0 20px var(--glow);letter-spacing:3px;">&#x1F389; CV COMPLETATO!</h2>
          <p id="win-msg" style="color:#aaa;font-size:clamp(10px,1.8vw,13px);margin-top:8px;line-height:2;"></p>
        </div>
        <div id="win-recap" style="display:flex;flex-direction:column;gap:10px;"></div>
        <div style="text-align:center;padding:8px 0 16px;">
          <button class="btn" onclick="resetCampaign();startGame()">&#x21BA; NUOVA CAMPAGNA</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Side Panel -->
  <div id="side-panel">
    <div class="panel-box">
      <h3>COMPETENZE</h3>
      <div id="skills-panel">
        <div class="skill-row"><span class="skill-name">Python</span><div class="skill-bar"><div class="skill-fill" id="sk-python" data-val="85"></div></div></div>
        <div class="skill-row"><span class="skill-name">React/JS</span><div class="skill-bar"><div class="skill-fill" id="sk-react" data-val="80"></div></div></div>
        <div class="skill-row"><span class="skill-name">Java</span><div class="skill-bar"><div class="skill-fill" id="sk-java" data-val="75"></div></div></div>
        <div class="skill-row"><span class="skill-name">SQL/DB</span><div class="skill-bar"><div class="skill-fill" id="sk-sql" data-val="78"></div></div></div>
        <div class="skill-row"><span class="skill-name">Docker</span><div class="skill-bar"><div class="skill-fill" id="sk-docker" data-val="70"></div></div></div>
        <div class="skill-row"><span class="skill-name">KNX/IoT</span><div class="skill-bar"><div class="skill-fill" id="sk-knx" data-val="65"></div></div></div>
      </div>
    </div>

    <div class="panel-box">
      <h3>VELOCITÀ</h3>
      <div id="speed-wrap">
        <span>LENTA</span>
        <input type="range" id="speed-slider" min="1" max="5" value="3" oninput="updateSpeed(this.value)">
        <span>VELOCE</span>
      </div>
      <div style="margin-top:8px;">
        <h3 style="margin-top:0;border:none;padding:0;margin-bottom:6px;">LEGENDA CIBI</h3>
        <div class="legend-row"><div class="legend-dot" style="background:#ffd700"></div>🎓 Istruzione</div>
        <div class="legend-row"><div class="legend-dot" style="background:#ff6b35"></div>🔧 Tirocinio</div>
        <div class="legend-row"><div class="legend-dot" style="background:#4ecdc4"></div>⚡ Volontariato</div>
        <div class="legend-row"><div class="legend-dot" style="background:#a855f7"></div>💻 Sviluppatore</div>
        <div class="legend-row"><div class="legend-dot" style="background:#f43f5e"></div>🏥 Dipendente ASL ROMA 2</div>
        <div class="legend-row"><div class="legend-dot" style="background:#06b6d4"></div>🌟 Extra</div>
      </div>
    </div>

    <div class="panel-box" style="flex:2;">
      <h3>INFO RACCOLTE</h3>
      <div id="info-list">
        <div style="color:var(--dim);font-size:11px;text-align:center;padding:10px;">
          Mangia i cibi per scoprire il CV!
        </div>
      </div>
    </div>
  </div>
</main>

<!-- D-Pad mobile -->
<div id="dpad">
  <div class="dpad-grid">
    <div></div>
    <div class="dpad-btn" id="dpad-up" ontouchstart="dpadPress('UP')" ontouchend="dpadRelease()">▲</div>
    <div></div>
    <div class="dpad-btn" id="dpad-left" ontouchstart="dpadPress('LEFT')" ontouchend="dpadRelease()">◀</div>
    <div class="dpad-center"></div>
    <div class="dpad-btn" id="dpad-right" ontouchstart="dpadPress('RIGHT')" ontouchend="dpadRelease()">▶</div>
    <div></div>
    <div class="dpad-btn" id="dpad-down" ontouchstart="dpadPress('DOWN')" ontouchend="dpadRelease()">▼</div>
    <div></div>
  </div>
</div>

<script>
// ══════════════════════════════════════════════
//  CV DATA — tutte le info da mangiare
// ══════════════════════════════════════════════
const CV_ITEMS = [
  // 🎓 ISTRUZIONE
  { cat:'🎓', cat_name:'Istruzione', title:'Perito Tecnico Informatico', text:'Diploma con focus su informatica, linguaggi programmati: Assembly, C/C++, Java, HTML/CSS, PhP, DML/DDL,SQL.', color:'#ffd700', glow:'rgba(255,215,0,0.6)' },
  { cat:'🎓', cat_name:'Istruzione', title:'Laurea in Informatica', text:'Percorso universitario con specializzazione in algoritmi, reti, sistemi operativi, sicurezza informatica, Base dati.', color:'#ffd700', glow:'rgba(255,215,0,0.6)' },
  { cat:'🎓', cat_name:'Istruzione', title:'Tesi Innovativa', text:'Progetto di sviluppo di una rete neurale collegata a MongoDB.', color:'#ffd700', glow:'rgba(255,215,0,0.6)' },

  // 🔧 TIROCINIO
  { cat:'🔧', cat_name:'Tirocinio', title:'Montaggio Schede Domotiche', text:'Installazione e configurazione di centraline e moduli domotici.', color:'#ff6b35', glow:'rgba(255,107,53,0.6)' },
  { cat:'🔧', cat_name:'Tirocinio', title:'Costruttore di Base Dati', text:'Studio di fattibilità e Implementazione di un Data Base dnato al Museo della Shoah', color:'#ff6b35', glow:'rgba(255,107,53,0.6)' },

  // ⚡ VOLONTARIATO
  { cat:'⚡', cat_name:'Volontariato', title:'Volontario UEFA', text:'Supporto organizzativo per partite internazionali: accreditamenti e gestione tifosi.', color:'#4ecdc4', glow:'rgba(78,205,196,0.6)' },
  { cat:'⚡', cat_name:'Volontariato', title:'Formula E (E-Prix)', text:'Volontario alla Formula Elettrica: logistica pit-lane e assistenza pubblico.', color:'#4ecdc4', glow:'rgba(78,205,196,0.6)' },
  { cat:'⚡', cat_name:'Volontariato', title:'Gestione Alta Pressione', text:'Capacità di lavorare in eventi con migliaia di persone mantenendo la calma.', color:'#4ecdc4', glow:'rgba(78,205,196,0.6)' },

  // 💻 SVILUPPATORE
  { cat:'💻', cat_name:'Sviluppatore', title:'Python & Java Backend', text:'Sviluppo di API REST robuste, microservizi e sistemi distribuiti.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },
  { cat:'💻', cat_name:'Sviluppatore', title:'React & Vue Frontend', text:'Interfacce responsive e moderne con focus su UX e performance.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },
  { cat:'💻', cat_name:'Sviluppatore', title:'Docker & DevOps', text:'Containerizzazione, CI/CD pipelines e deploy automatizzato.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },
  { cat:'💻', cat_name:'Sviluppatore', title:'SQL & NoSQL Database', text:'Progettazione di schemi, query ottimizzate, Oracle, PostgreSQL e MongoDB.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },
  { cat:'💻', cat_name:'Sviluppatore', title:'Metodologie Agile', text:'Scrum, sprint planning, code review e continuous integration.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },
  { cat:'💻', cat_name:'Sviluppatore', title:'Git & Versionamento', text:'Workflow professionale con branch, PR e gestione repository.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },

  // 🏥 ASL
   { cat:'🏥', cat_name:'ASL', title:'BDA', text:'Sviluppo e Gestione dei Database sia per il personale interno che per i Cittadini.', color:'#f43f5e', glow:'rgba(244,63,94,0.6)' },
  { cat:'🏥', cat_name:'ASL', title:'Azienda Sanitaria Locale', text:'Sviluppatore software per sistemi sanitari critici e cartelle cliniche.', color:'#f43f5e', glow:'rgba(244,63,94,0.6)' },
  { cat:'🏥', cat_name:'ASL', title:'Standard HL7/FHIR', text:'Integrazione di sistemi per l\'interoperabilità dei dati sanitari.', color:'#f43f5e', glow:'rgba(244,63,94,0.6)' },
  { cat:'🏥', cat_name:'ASL', title:'Sistema CUP', text:'Gestione prenotazioni e accessi ai servizi sanitari per i cittadini.', color:'#f43f5e', glow:'rgba(244,63,94,0.6)' },
  { cat:'🏥', cat_name:'ASL', title:'GDPR & Privacy', text:'Rispetto normative sulla privacy in contesti regolamentati e critici.', color:'#f43f5e', glow:'rgba(244,63,94,0.6)' },

  // 🌟 EXTRA
  { cat:'🌟', cat_name:'Soft Skills', title:'Problem Solving Creativo', text:'Approccio analitico e laterale ai problemi tecnici e organizzativi.', color:'#06b6d4', glow:'rgba(6,182,212,0.6)' },
  { cat:'🌟', cat_name:'Soft Skills', title:'Team Working', text:'Esperienza in team multidisciplinari in contesti sia tecnici che di evento.', color:'#06b6d4', glow:'rgba(6,182,212,0.6)' },
  { cat:'🌟', cat_name:'Soft Skills', title:'Adattabilità', text:'Passato dall\'elettronica al codice, dalla sanità allo sport. Versatile!', color:'#06b6d4', glow:'rgba(6,182,212,0.6)' },
];

// ══════════════════════════════════════════════
//  CONSTANTS
// ══════════════════════════════════════════════
const CELL = 20;
let COLS, ROWS;
let canvas, ctx;

// Game state
let snake, dir, nextDir, food, score, hiScore, gameRunning, gameInterval;
let totalItems = CV_ITEMS.length;
let speedMs = 150;
let touchStartX, touchStartY;

// ── CAMPAIGN STATE (persiste tra le partite) ──
let collectedItems = [];   // info già scoperte — accumulate tra tutte le partite
let remainingItems = [];   // info ancora da scoprire — si svuota solo quando si vince
let sessionItems   = [];   // info mangiate in questa partita — si azzera ad ogni restart

// ══════════════════════════════════════════════
//  INIT
// ══════════════════════════════════════════════
window.addEventListener('load', () => {
  canvas = document.getElementById('c');
  ctx = canvas.getContext('2d');
  hiScore = parseInt(localStorage.getItem('snakecv_hi') || '0');
  document.getElementById('hiscore').textContent = hiScore;
  resizeCanvas();
  window.addEventListener('resize', () => { resizeCanvas(); if (!gameRunning) drawIdle(); });
  setupControls();

  // Ripristina campagna salvata
  loadCampaign();
  rebuildInfoList();
  updateScore();
  animateSkillBars();
  drawIdle();
});

function resizeCanvas() {
  const wrap = document.getElementById('canvas-wrap');
  const maxW = Math.min(window.innerWidth - 20, 480);
  const maxH = window.innerHeight < 600 ? window.innerHeight * 0.45 : Math.min(window.innerHeight - 180, 500);
  COLS = Math.floor(maxW / CELL);
  ROWS = Math.floor(maxH / CELL);
  canvas.width  = COLS * CELL;
  canvas.height = ROWS * CELL;
  wrap.style.width = canvas.width + 'px';
}

function drawIdle() {
  ctx.fillStyle = '#050d0a';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  drawGrid();
}

// ══════════════════════════════════════════════
//  GAME LOGIC
// ══════════════════════════════════════════════
function startGame() {
  hideAllOverlays();
  resizeCanvas();

  // Se non ci sono più info da scoprire → reset completo campagna
  if (remainingItems.length === 0) {
    resetCampaign();
  }

  snake = [
    { x: Math.floor(COLS/2),     y: Math.floor(ROWS/2) },
    { x: Math.floor(COLS/2) - 1, y: Math.floor(ROWS/2) },
    { x: Math.floor(COLS/2) - 2, y: Math.floor(ROWS/2) },
  ];
  dir     = { x:1, y:0 };
  nextDir = { x:1, y:0 };
  score   = 0;
  sessionItems = [];
  gameRunning  = true;

  // remainingItems conserva le info non ancora scoperte (shuffle ogni partita)
  remainingItems = shuffle([...remainingItems]);

  updateScore();
  spawnFood();
  clearInterval(gameInterval);
  gameInterval = setInterval(tick, speedMs);
}

function tick() {
  if (!gameRunning) return;
  dir = { ...nextDir };
  const head = { x: snake[0].x + dir.x, y: snake[0].y + dir.y };

  // Wall collision
  if (head.x < 0 || head.x >= COLS || head.y < 0 || head.y >= ROWS) { endGame(); return; }

  // Self collision
  if (snake.some(s => s.x === head.x && s.y === head.y)) { endGame(); return; }

  snake.unshift(head);

  // Eat food
  if (head.x === food.x && head.y === food.y) {
    eatFood();
  } else {
    snake.pop();
  }

  draw();
}

function eatFood() {
  const item = food.item;
  score += 10;
  sessionItems.push(item);
  collectedItems.push(item);
  saveCampaign();
  if (score > hiScore) { hiScore = score; localStorage.setItem('snakecv_hi', hiScore); }
  updateScore();
  addInfoItem(item);
  animateSkillBars();

  if (remainingItems.length === 0) {
    setTimeout(() => winGame(), 200);
  } else {
    spawnFood();
  }
}

function spawnFood() {
  let pos;
  const item = remainingItems.pop();
  do {
    pos = { x: Math.floor(Math.random() * COLS), y: Math.floor(Math.random() * ROWS) };
  } while (snake.some(s => s.x === pos.x && s.y === pos.y));
  food = { ...pos, item };
}

function endGame() {
  gameRunning = false;
  clearInterval(gameInterval);

  const stillLeft = remainingItems.length;
  const thisRun   = sessionItems.length;
  const done      = collectedItems.length;

  let msg = `Questa partita: +${thisRun} info scoperte\n`;
  msg    += `Totale raccolte: ${done}/${totalItems}\n`;
  if (stillLeft > 0) {
    msg  += `Ne mancano ancora ${stillLeft} — riprova!`;
  }
  document.getElementById('go-score').innerHTML =
    `<span style="color:var(--head)">+${thisRun}</span> info questa partita<br>
     Totale: <span style="color:var(--head)">${done}/${totalItems}</span> scoperte<br>
     <span style="color:var(--dim);font-size:10px">${stillLeft > 0 ? `Mancano ancora ${stillLeft} — riprova!` : 'Hai scoperto tutto!'}</span>`;

  document.getElementById('go-btn').textContent = stillLeft > 0 ? '↺ CONTINUA CAMPAGNA' : '🎉 VEDI RIEPILOGO';
  document.getElementById('gameover-screen').style.display = 'flex';

  if (score > hiScore) {
    hiScore = score;
    localStorage.setItem('snakecv_hi', hiScore);
    document.getElementById('hiscore').textContent = hiScore;
  }
}

function winGame() {
  gameRunning = false;
  clearInterval(gameInterval);

  document.getElementById('win-msg').innerHTML =
    `Hai scoperto tutte le <strong style="color:var(--head)">${totalItems}</strong> informazioni!<br>
     Punteggio totale: <strong style="color:var(--head)">${score}</strong> pt`;

  buildWinRecap();
  document.getElementById('win-screen').style.display = 'flex';
  // NON resettiamo qui — l'utente clicca "Nuova Campagna" per ricominciare
}

function buildWinRecap() {
  const recap = document.getElementById('win-recap');
  recap.innerHTML = '';

  // Raggruppa per categoria
  const cats = {};
  collectedItems.forEach(item => {
    if (!cats[item.cat_name]) cats[item.cat_name] = { cat: item.cat, color: item.color, items: [] };
    cats[item.cat_name].items.push(item);
  });

  Object.entries(cats).forEach(([catName, group], gi) => {
    // Sezione categoria
    const section = document.createElement('div');
    section.style.cssText = `background:#071410;border:1px solid ${group.color}44;border-radius:8px;overflow:hidden;animation:fadeIn 0.4s ease ${gi*0.08}s both;`;

    // Header categoria
    const hdr = document.createElement('div');
    hdr.style.cssText = `display:flex;align-items:center;gap:10px;padding:10px 14px;background:${group.color}18;border-bottom:1px solid ${group.color}33;`;
    hdr.innerHTML = `<span style="font-size:20px">${group.cat}</span>
      <span style="font-family:'Orbitron',monospace;font-size:10px;letter-spacing:2px;color:${group.color}">${catName.toUpperCase()}</span>
      <span style="margin-left:auto;font-size:10px;color:var(--dim)">${group.items.length} info</span>`;
    section.appendChild(hdr);

    // Righe info
    group.items.forEach((item, ii) => {
      const row = document.createElement('div');
      row.style.cssText = `display:flex;gap:12px;padding:10px 14px;border-bottom:1px solid #0a1f14;animation:fadeIn 0.3s ease ${gi*0.08+ii*0.05}s both;`;
      row.innerHTML = `
        <div style="flex:0 0 auto;margin-top:3px;">
          <div style="width:8px;height:8px;border-radius:50%;background:${item.color};box-shadow:0 0 6px ${item.color};margin-top:4px;"></div>
        </div>
        <div>
          <div style="font-family:'Orbitron',monospace;font-size:10px;font-weight:700;color:${item.color};letter-spacing:1px;margin-bottom:3px;">${item.title}</div>
          <div style="font-size:12px;color:#bbb;line-height:1.6;">${item.text}</div>
        </div>`;
      section.appendChild(row);
    });

    recap.appendChild(section);
  });
}

// ── CAMPAIGN PERSISTENCE ──
function saveCampaign() {
  const titles = collectedItems.map(i => i.title);
  localStorage.setItem('snakecv_campaign', JSON.stringify(titles));
}

function loadCampaign() {
  const saved = localStorage.getItem('snakecv_campaign');
  if (saved) {
    const titles = JSON.parse(saved);
    collectedItems = CV_ITEMS.filter(i => titles.includes(i.title));
    remainingItems = CV_ITEMS.filter(i => !titles.includes(i.title));
  } else {
    collectedItems = [];
    remainingItems = [...CV_ITEMS];
  }
}

function resetCampaign() {
  collectedItems = [];
  remainingItems = [...CV_ITEMS];
  sessionItems   = [];
  localStorage.removeItem('snakecv_campaign');
  document.getElementById('info-list').innerHTML =
    '<div style="color:var(--dim);font-size:11px;text-align:center;padding:10px;">Mangia i cibi per scoprire il CV!</div>';
}

function rebuildInfoList() {
  const list = document.getElementById('info-list');
  list.innerHTML = '';
  if (collectedItems.length === 0) {
    list.innerHTML = '<div style="color:var(--dim);font-size:11px;text-align:center;padding:10px;">Mangia i cibi per scoprire il CV!</div>';
    return;
  }
  // Show most recent first
  [...collectedItems].reverse().forEach(item => {
    const el = document.createElement('div');
    el.className = 'info-item';
    el.innerHTML = `<span class="cat">${item.cat}</span><div class="txt"><strong style="color:${item.color}">${item.title}</strong><br>${item.text}</div>`;
    list.appendChild(el);
  });
}

// ══════════════════════════════════════════════
//  DRAWING
// ══════════════════════════════════════════════
let foodPulse = 0;

function draw() {
  foodPulse = (foodPulse + 0.12) % (Math.PI * 2);
  ctx.fillStyle = '#050d0a';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  drawGrid();
  drawSnake();
  drawFood();
}

function drawGrid() {
  ctx.strokeStyle = '#0a1f14';
  ctx.lineWidth = 0.5;
  for (let x = 0; x <= COLS; x++) {
    ctx.beginPath(); ctx.moveTo(x*CELL,0); ctx.lineTo(x*CELL,canvas.height); ctx.stroke();
  }
  for (let y = 0; y <= ROWS; y++) {
    ctx.beginPath(); ctx.moveTo(0,y*CELL); ctx.lineTo(canvas.width,y*CELL); ctx.stroke();
  }
}

function drawSnake() {
  snake.forEach((seg, i) => {
    const isHead = i === 0;
    const t = i / snake.length;
    const r = ctx.createRadialGradient(
      seg.x*CELL + CELL/2, seg.y*CELL + CELL/2, 0,
      seg.x*CELL + CELL/2, seg.y*CELL + CELL/2, CELL*0.8
    );
    if (isHead) {
      r.addColorStop(0, '#00ffcc');
      r.addColorStop(1, '#00cc88');
    } else {
      const g = Math.floor(255 * (1 - t * 0.6));
      r.addColorStop(0, `rgba(0,${g},${Math.floor(g*0.5)},0.95)`);
      r.addColorStop(1, `rgba(0,${Math.floor(g*0.6)},${Math.floor(g*0.3)},0.8)`);
    }

    ctx.fillStyle = r;
    ctx.beginPath();
    ctx.roundRect(seg.x*CELL+1, seg.y*CELL+1, CELL-2, CELL-2, isHead ? 6 : 3);
    ctx.fill();

    if (isHead) {
      // Eyes
      ctx.fillStyle = '#000';
      const ex = dir.x === 0 ? [5, 13] : (dir.x > 0 ? [13, 13] : [5, 5]);
      const ey = dir.y === 0 ? [5, 13] : (dir.y > 0 ? [13, 13] : [5, 5]);
      ctx.beginPath(); ctx.arc(seg.x*CELL+ex[0], seg.y*CELL+ey[0], 2, 0, Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(seg.x*CELL+ex[1], seg.y*CELL+ey[1], 2, 0, Math.PI*2); ctx.fill();
      // Pupils
      ctx.fillStyle = '#00ffcc';
      ctx.beginPath(); ctx.arc(seg.x*CELL+ex[0], seg.y*CELL+ey[0], 1, 0, Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(seg.x*CELL+ex[1], seg.y*CELL+ey[1], 1, 0, Math.PI*2); ctx.fill();

      // Glow
      ctx.shadowColor = '#00ff88';
      ctx.shadowBlur = 12;
      ctx.fillStyle = 'transparent';
      ctx.beginPath();
      ctx.roundRect(seg.x*CELL+1, seg.y*CELL+1, CELL-2, CELL-2, 6);
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  });
}

function drawFood() {
  if (!food) return;
  const pulse = 1 + Math.sin(foodPulse) * 0.15;
  const cx = food.x*CELL + CELL/2;
  const cy = food.y*CELL + CELL/2;
  const r = (CELL/2 - 2) * pulse;

  // Glow
  ctx.shadowColor = food.item.glow;
  ctx.shadowBlur = 18;

  // Circle
  ctx.fillStyle = food.item.color;
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI*2);
  ctx.fill();

  // Emoji
  ctx.shadowBlur = 0;
  ctx.font = `${Math.floor(CELL * 0.65)}px serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(food.item.cat, cx, cy + 1);
}

// ══════════════════════════════════════════════
//  UI UPDATES
// ══════════════════════════════════════════════
function updateScore() {
  document.getElementById('score').textContent = score;
  document.getElementById('hiscore').textContent = hiScore;
  document.getElementById('collected').textContent = `${collectedItems.length}/${totalItems}`;
}

function addInfoItem(item) {
  const list = document.getElementById('info-list');
  // Remove placeholder
  const placeholder = list.querySelector('div[style]');
  if (placeholder) placeholder.remove();

  const el = document.createElement('div');
  el.className = 'info-item';
  el.innerHTML = `<span class="cat">${item.cat}</span><div class="txt"><strong style="color:${item.color}">${item.title}</strong><br>${item.text}</div>`;
  list.insertBefore(el, list.firstChild);
  list.scrollTop = 0;
}


const SKILL_MAP = {
  'Sviluppatore': ['python','react','java','sql','docker'],
  'Tirocinio': ['knx'],
  'Istruzione': ['python','java'],
  'ASL': ['sql','python'],
};

function animateSkillBars() {
  const cats = collectedItems.map(i => i.cat_name);
  const allSkills = document.querySelectorAll('.skill-fill');
  allSkills.forEach(bar => {
    const base = parseInt(bar.dataset.val);
    const boost = cats.filter(c => {
      const sk = bar.id.replace('sk-','');
      return (SKILL_MAP[c]||[]).includes(sk);
    }).length * 3;
    bar.style.width = Math.min(100, base + boost) + '%';
  });
}

function updateSkillBars(pct) {
  document.querySelectorAll('.skill-fill').forEach(b => b.style.width = '0%');
  setTimeout(() => {
    document.querySelectorAll('.skill-fill').forEach(b => {
      b.style.width = parseInt(b.dataset.val) * (pct/100) + '%';
    });
  }, 100);
}

function updateSpeed(val) {
  const speeds = [220, 175, 140, 110, 80];
  speedMs = speeds[val - 1];
  if (gameRunning) {
    clearInterval(gameInterval);
    gameInterval = setInterval(tick, speedMs);
  }
}

function hideAllOverlays() {
  ['start-screen','gameover-screen','win-screen'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
  });
}

// ══════════════════════════════════════════════
//  CONTROLS
// ══════════════════════════════════════════════
function setupControls() {
  // Keyboard
  document.addEventListener('keydown', e => {
    const map = {
      ArrowUp:'UP', ArrowDown:'DOWN', ArrowLeft:'LEFT', ArrowRight:'RIGHT',
      KeyW:'UP', KeyS:'DOWN', KeyA:'LEFT', KeyD:'RIGHT',
    };
    if (map[e.code]) {
      e.preventDefault();
      setDir(map[e.code]);
    }
  });

  // Touch swipe
  canvas.addEventListener('touchstart', e => {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
    e.preventDefault();
  }, { passive:false });

  canvas.addEventListener('touchend', e => {
    if (touchStartX === undefined) return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    const dy = e.changedTouches[0].clientY - touchStartY;
    if (Math.abs(dx) > Math.abs(dy)) {
      setDir(dx > 0 ? 'RIGHT' : 'LEFT');
    } else {
      setDir(dy > 0 ? 'DOWN' : 'UP');
    }
    e.preventDefault();
  }, { passive:false });
}

function setDir(d) {
  if (!gameRunning) return;
  const map = {
    UP:    { x:0,  y:-1 },
    DOWN:  { x:0,  y:1  },
    LEFT:  { x:-1, y:0  },
    RIGHT: { x:1,  y:0  },
  };
  const nd = map[d];
  // Prevent 180°
  if (nd.x === -dir.x && nd.y === -dir.y) return;
  nextDir = nd;
}

function dpadPress(d) { setDir(d); }
function dpadRelease() {}

// ══════════════════════════════════════════════
//  UTILS
// ══════════════════════════════════════════════
function shuffle(arr) {
  for (let i = arr.length-1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i+1));
    [arr[i],arr[j]] = [arr[j],arr[i]];
  }
  return arr;
}

// skill bars are restored on load via animateSkillBars() in the load handler
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, total=len([
        'Liceo Scientifico-Tecnologico','Laurea in Informatica','Tesi Innovativa','Olimpiadi Informatica',
        'Montaggio Schede Domotiche','Protocollo KNX/RS485','Automazione Edifici',
        'Volontario UEFA','Formula E (E-Prix)','Gestione Alta Pressione',
        'Python & Java Backend','React & Vue Frontend','Docker & DevOps',
        'SQL & NoSQL Database','Metodologie Agile','Git & Versionamento',
        'Azienda Sanitaria Locale','Standard HL7/FHIR','Sistema CUP','GDPR & Privacy',
        'Problem Solving Creativo','Team Working','Adattabilità',
    ]))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print(f"""
╔══════════════════════════════════════╗
║        🐍  SNAKE CV  🐍              ║
╠══════════════════════════════════════╣
║  Apri il browser su:                 ║
║  http://localhost:{port}               ║
║                                      ║
║  Da mobile sulla stessa rete:        ║
║  http://<tuo-ip>:{port}               ║
║                                      ║
║  Ctrl+C per fermare il server        ║
╚══════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port, debug=False)
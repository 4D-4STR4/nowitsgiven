/*
 * SALVAGE — core-loop prototype
 * Engine-independent gray-box that validates the loop the Unity build must reproduce:
 *   board a procedural wreck -> scavenge salvage (value vs weight vs depth) under a rising
 *   Wreck Instability meter -> at 100% the reactor melts down on a countdown -> EXTRACT at the
 *   airlock or lose everything in your hold. Only extracted salvage counts toward the quota.
 * Single-player here, but every rule is authored to scale to 1-4 player listen-server co-op.
 */
'use strict';

// ---------------------------------------------------------------- constants
const TS = 16;                  // tile size (px)
const COLS = 60, ROWS = 38;     // wreck grid
const WALL = 0, FLOOR = 1, AIRLOCK = 2, REACTOR = 3, BREACH = 4;

const cv = document.getElementById('cv');
const ctx = cv.getContext('2d');

// ---------------------------------------------------------------- tiny audio (optional, guarded)
let actx = null;
function beep(freq, dur, type, gain) {
  try {
    if (!actx) actx = new (window.AudioContext || window.webkitAudioContext)();
    const o = actx.createOscillator(), g = actx.createGain();
    o.type = type || 'square'; o.frequency.value = freq;
    g.gain.value = gain == null ? 0.04 : gain;
    o.connect(g); g.connect(actx.destination);
    o.start(); g.gain.exponentialRampToValueAtTime(0.0001, actx.currentTime + dur);
    o.stop(actx.currentTime + dur);
  } catch (e) { /* audio is a bonus, never a blocker */ }
}

// ---------------------------------------------------------------- rng (seeded, so runs are reproducible / net-deterministic later)
function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ---------------------------------------------------------------- game state
let grid, rooms, player, salvage, enemies, breaches;
let banked, quota, instability, meltdown, oxygen, flashlight, seed;
let toastT = 0, runState; // 'active' | 'extracted' | 'dead'
const keys = {};

function rndInt(rng, a, b) { return a + Math.floor(rng() * (b - a + 1)); }

// --------------------------------------------------------- procedural wreck (modular rooms + corridors)
function generateWreck(s) {
  seed = s;
  const rng = mulberry32(s);
  grid = new Array(COLS * ROWS).fill(WALL);
  rooms = [];
  const tries = 80, maxRooms = 11;
  for (let i = 0; i < tries && rooms.length < maxRooms; i++) {
    const w = rndInt(rng, 5, 9), h = rndInt(rng, 4, 7);
    const x = rndInt(rng, 1, COLS - w - 2), y = rndInt(rng, 1, ROWS - h - 2);
    const r = { x, y, w, h, cx: (x + (w >> 1)), cy: (y + (h >> 1)) };
    if (rooms.some(o => x < o.x + o.w + 1 && x + w + 1 > o.x && y < o.y + o.h + 1 && y + h + 1 > o.y)) continue;
    rooms.push(r);
    for (let yy = y; yy < y + h; yy++) for (let xx = x; xx < x + w; xx++) grid[yy * COLS + xx] = FLOOR;
  }
  // connect rooms in placement order with L-corridors (room-graph spine)
  for (let i = 1; i < rooms.length; i++) carveCorridor(rooms[i - 1], rooms[i], rng);

  // airlock in the first room (extraction), reactor in the farthest room (the greedy depth)
  const start = rooms[0];
  let far = rooms[0], best = -1;
  for (const r of rooms) {
    const d = Math.abs(r.cx - start.cx) + Math.abs(r.cy - start.cy);
    if (d > best) { best = d; far = r; }
  }
  grid[start.cy * COLS + start.cx] = AIRLOCK;
  grid[far.cy * COLS + far.cx] = REACTOR;

  // a few hull breaches (the "vent" signature toy) on room edges, deeper rooms favoured
  breaches = [];
  for (let i = 1; i < rooms.length; i++) {
    if (rng() < 0.5) {
      const r = rooms[i];
      const bx = r.x + rndInt(rng, 1, r.w - 2), by = r.y;
      grid[by * COLS + bx] = BREACH;
      breaches.push({ x: bx, y: by, vented: false });
    }
  }

  // salvage: value scales with distance from the airlock (risk = reward); weight roughly tracks value
  salvage = [];
  const kinds = [
    { name: 'scrap',     base: 18,  wt: 4,  col: '#9aa6b2' },
    { name: 'cell',      base: 45,  wt: 7,  col: '#5ad7ff' },
    { name: 'alloy',     base: 80,  wt: 12, col: '#c4a35a' },
    { name: 'core',      base: 160, wt: 22, col: '#ff7be0' },
  ];
  for (const r of rooms) {
    if (r === start) continue;
    const depth = (Math.abs(r.cx - start.cx) + Math.abs(r.cy - start.cy)) / (COLS + ROWS); // 0..~1
    const n = rndInt(rng, 1, 3);
    for (let k = 0; k < n; k++) {
      // deeper rooms bias toward richer (heavier) kinds
      let ki = Math.min(kinds.length - 1, Math.floor(rng() * (1 + depth * 5)));
      if (r === far) ki = 3; // the reactor core room always holds a core
      const kd = kinds[ki];
      const sx = r.x + rndInt(rng, 1, r.w - 2), sy = r.y + rndInt(rng, 1, r.h - 2);
      if (grid[sy * COLS + sx] !== FLOOR) continue;
      const jitter = 0.8 + rng() * 0.5;
      salvage.push({ x: sx, y: sy, value: Math.round(kd.base * jitter), weight: kd.wt,
        name: kd.name, col: kd.col, taken: false });
    }
  }

  // one roaming stalker per ~3 rooms (drawn to light/noise) — avoidance, not power fantasy
  enemies = [];
  const ecount = Math.max(1, Math.floor(rooms.length / 3));
  for (let i = 0; i < ecount; i++) {
    const r = rooms[rndInt(rng, 1, rooms.length - 1)];
    enemies.push({ x: r.cx + 0.5, y: r.cy + 0.5, vx: 0, vy: 0, alerted: 0, alive: true, wanderT: 0 });
  }

  // explored memory (fog of war)
  for (let i = 0; i < grid.length; i++) grid[i] |= 0;
  explored = new Uint8Array(COLS * ROWS);

  player = { x: start.cx + 0.5, y: start.cy + 0.5, hold: [], carriedValue: 0, load: 0 };
  banked = 0;
  quota = 260 + (s % 5) * 40;
  instability = 0; meltdown = 0; oxygen = 100; flashlight = true;
  runState = 'active';
  hideBanner();
  toast('WRECK ' + (s).toString(16).toUpperCase().padStart(4, '0') + ' — find the salvage. Mind the reactor.');
}

let explored;

function carveCorridor(a, b, rng) {
  let x = a.cx, y = a.cy;
  const horizFirst = rng() < 0.5;
  const stepX = () => { while (x !== b.cx) { x += x < b.cx ? 1 : -1; set(x, y); } };
  const stepY = () => { while (y !== b.cy) { y += y < b.cy ? 1 : -1; set(x, y); } };
  if (horizFirst) { stepX(); stepY(); } else { stepY(); stepX(); }
  function set(cx, cy) { if (grid[cy * COLS + cx] === WALL) grid[cy * COLS + cx] = FLOOR; }
}

const MAX_LOAD = 40; // kg — the trip-planning cap

// ---------------------------------------------------------------- helpers
function tileAt(tx, ty) { if (tx < 0 || ty < 0 || tx >= COLS || ty >= ROWS) return WALL; return grid[ty * COLS + tx]; }
function walkable(tx, ty) { return tileAt(tx, ty) !== WALL; }
function dist(ax, ay, bx, by) { return Math.hypot(ax - bx, ay - by); }

function toast(msg) { const t = document.getElementById('toast'); t.textContent = msg; t.style.opacity = 1; toastT = 3.2; }
function showBanner(title, sub) {
  const b = document.getElementById('banner');
  b.innerHTML = title + '<small>' + sub + '</small>'; b.style.display = 'block';
}
function hideBanner() { document.getElementById('banner').style.display = 'none'; }

// ---------------------------------------------------------------- input
window.addEventListener('keydown', e => {
  keys[e.key.toLowerCase()] = true;
  const k = e.key.toLowerCase();
  if (['arrowup', 'arrowdown', 'arrowleft', 'arrowright', ' '].includes(k)) e.preventDefault();
  if (k === 'e') interact();
  if (k === 'f') { flashlight = !flashlight; toast('Flashlight ' + (flashlight ? 'ON — you can see, and be seen' : 'OFF — running dark')); }
  if (k === 'v') ventNearby();
  if (k === 'r') generateWreck((seed + 1) >>> 0);
});
window.addEventListener('keyup', e => { keys[e.key.toLowerCase()] = false; });

// ---------------------------------------------------------------- actions
function interact() {
  if (runState !== 'active') { if (keys) generateWreck((seed + 1) >>> 0); return; }
  const px = Math.floor(player.x), py = Math.floor(player.y);
  // extract at the airlock
  if (tileAt(px, py) === AIRLOCK) {
    if (player.carriedValue > 0) {
      banked += player.carriedValue;
      beep(880, 0.18, 'sine', 0.06); beep(1320, 0.22, 'sine', 0.05);
      toast('EXTRACTED +$' + player.carriedValue + '  (banked $' + banked + ')');
      player.hold = []; player.carriedValue = 0; player.load = 0;
      instability = Math.max(0, instability - 12); // breathing room after a successful run-out
      if (banked >= quota && runState === 'active') win();
    } else {
      toast('Airlock secure. Bring back salvage to bank it.');
    }
    return;
  }
  // grab nearby salvage
  let best = null, bd = 0.9;
  for (const s of salvage) { if (s.taken) continue; const d = dist(player.x, player.y, s.x + 0.5, s.y + 0.5); if (d < bd) { bd = d; best = s; } }
  if (best) {
    if (player.load + best.weight > MAX_LOAD) { toast('Too heavy! Drop a trip at the airlock first.'); beep(140, 0.15, 'sawtooth', 0.05); return; }
    best.taken = true; player.hold.push(best); player.carriedValue += best.value; player.load += best.weight;
    instability += best.value * 0.05; // greed wakes the wreck
    beep(520, 0.07, 'square', 0.05);
    toast('Grabbed ' + best.name + '  +$' + best.value + '  (' + best.weight + 'kg)');
  }
}

function ventNearby() {
  if (runState !== 'active') return;
  let b = null, bd = 2.2;
  for (const br of breaches) { if (br.vented) continue; const d = dist(player.x, player.y, br.x + 0.5, br.y + 0.5); if (d < bd) { bd = d; b = br; } }
  if (!b) { toast('No hull breach in reach to vent.'); return; }
  b.vented = true;
  // explosive decompression: kill stalkers near the breach, shove the player, spike instability
  for (const en of enemies) { if (en.alive && dist(en.x, en.y, b.x + 0.5, b.y + 0.5) < 4.5) { en.alive = false; } }
  const ang = Math.atan2(player.y - (b.y + 0.5), player.x - (b.x + 0.5));
  player.x += Math.cos(ang) * 1.2; player.y += Math.sin(ang) * 1.2;
  instability += 18; oxygen = Math.max(0, oxygen - 14);
  beep(90, 0.5, 'sawtooth', 0.08);
  toast('VENTED! Decompression clears the threat — but the wreck screams (instability +18).');
}

function win() { runState = 'extracted'; beep(660, 0.3, 'sine', 0.06); showBanner('QUOTA MET', 'Banked $' + banked + ' / $' + quota + ' — debt paid for the shift.  [R] next wreck'); }
function die(reason) { if (runState !== 'active') return; runState = 'dead'; beep(70, 0.8, 'sawtooth', 0.09); showBanner('CREW LOST', reason + '  Hold ($' + player.carriedValue + ') drifts in the dark.  [R] new wreck'); }

// ---------------------------------------------------------------- update
let last = performance.now();
function update(dt) {
  if (runState !== 'active') return;

  // movement — load drags you down (trip-planning tension)
  const loadFactor = 1 - (player.load / MAX_LOAD) * 0.55;
  const spd = 5.2 * loadFactor * dt;
  let mx = 0, my = 0;
  if (keys['w'] || keys['arrowup']) my -= 1;
  if (keys['s'] || keys['arrowdown']) my += 1;
  if (keys['a'] || keys['arrowleft']) mx -= 1;
  if (keys['d'] || keys['arrowright']) mx += 1;
  if (mx || my) { const m = Math.hypot(mx, my); mx /= m; my /= m; }
  moveEntity(player, mx * spd, my * spd);

  // instability: time + proximity to the reactor + your greed (carried value), minus nothing — it only climbs
  const px = Math.floor(player.x), py = Math.floor(player.y);
  let nearReactor = 0;
  for (const r of rooms) { /* reactor glow handled below */ }
  const reactorTile = findTile(REACTOR);
  if (reactorTile) nearReactor = Math.max(0, 1 - dist(player.x, player.y, reactorTile.x + 0.5, reactorTile.y + 0.5) / 8);
  if (meltdown <= 0) {
    instability += (0.55 + nearReactor * 1.4 + player.carriedValue * 0.0009) * dt;
    if (instability >= 100) { instability = 100; meltdown = 24; toast('!! REACTOR BREACH — MELTDOWN IN 24s — GET TO THE AIRLOCK !!'); beep(200, 0.4, 'square', 0.07); }
  } else {
    meltdown -= dt;
    if (Math.floor(meltdown) !== Math.floor(meltdown + dt)) beep(300, 0.08, 'square', 0.06); // tick
    if (meltdown <= 0) die('The reactor went critical.');
  }

  // oxygen slowly drains; vented sections cost more (abstracted)
  oxygen -= 0.6 * dt;
  if (oxygen <= 0) { oxygen = 0; die('Suit oxygen ran out.'); }

  // enemies: wander, but are drawn to your flashlight; contact downs you
  for (const en of enemies) {
    if (!en.alive) continue;
    const dToP = dist(en.x, en.y, player.x, player.y);
    const sees = flashlight && dToP < 9;
    if (sees) en.alerted = 2.5;
    en.alerted = Math.max(0, en.alerted - dt);
    let ex = 0, ey = 0;
    if (en.alerted > 0) { const a = Math.atan2(player.y - en.y, player.x - en.x); ex = Math.cos(a); ey = Math.sin(a); }
    else { en.wanderT -= dt; if (en.wanderT <= 0) { en.wanderT = 1 + Math.random() * 2; en.vx = (Math.random() * 2 - 1); en.vy = (Math.random() * 2 - 1); } ex = en.vx; ey = en.vy; }
    const espd = (en.alerted > 0 ? 3.4 : 1.6) * dt;
    const m = Math.hypot(ex, ey) || 1;
    moveEntity(en, (ex / m) * espd, (ey / m) * espd);
    if (dToP < 0.6) {
      // downed: drop hold where you stand, respawn at airlock (tense setback, not instant wipe)
      if (player.carriedValue > 0) toast('STALKER HIT! You drop your hold ($' + player.carriedValue + ') and scramble back.');
      else toast('STALKER HIT! You scramble back to the airlock.');
      for (const s of player.hold) { s.taken = false; s.x = Math.floor(player.x); s.y = Math.floor(player.y); }
      player.hold = []; player.carriedValue = 0; player.load = 0;
      const al = findTile(AIRLOCK); if (al) { player.x = al.x + 0.5; player.y = al.y + 0.5; }
      instability += 6; oxygen = Math.max(0, oxygen - 8);
      beep(110, 0.3, 'sawtooth', 0.07);
    }
  }

  // reveal explored tiles around the player (memory persists, dimly)
  const R = flashlight ? 6 : 3;
  for (let yy = py - R; yy <= py + R; yy++) for (let xx = px - R; xx <= px + R; xx++) {
    if (xx < 0 || yy < 0 || xx >= COLS || yy >= ROWS) continue;
    if (dist(px + 0.5, py + 0.5, xx + 0.5, yy + 0.5) <= R) explored[yy * COLS + xx] = 1;
  }

  if (toastT > 0) { toastT -= dt; if (toastT <= 0) document.getElementById('toast').style.opacity = 0; }
  updateHUD();
}

function findTile(type) {
  for (let y = 0; y < ROWS; y++) for (let x = 0; x < COLS; x++) if (grid[y * COLS + x] === type) return { x, y };
  return null;
}

function moveEntity(ent, dx, dy) {
  // axis-separated collision against walls
  if (walkable(Math.floor(ent.x + dx + Math.sign(dx) * 0.25), Math.floor(ent.y))) ent.x += dx;
  if (walkable(Math.floor(ent.x), Math.floor(ent.y + dy + Math.sign(dy) * 0.25))) ent.y += dy;
}

// ---------------------------------------------------------------- render
function render() {
  ctx.clearRect(0, 0, cv.width, cv.height);
  const px = player.x, py = player.y;
  const lightR = flashlight ? 6.0 : 3.0;

  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      const t = grid[y * COLS + x];
      const d = dist(px, py, x + 0.5, y + 0.5);
      const lit = d <= lightR;
      const mem = explored[y * COLS + x];
      if (!lit && !mem) continue;
      let col;
      if (t === WALL) col = '#161d27';
      else if (t === AIRLOCK) col = '#1e6f8f';
      else if (t === REACTOR) col = '#7a2a2a';
      else if (t === BREACH) col = '#2b2440';
      else col = '#0c1622';
      // light falloff
      let b = lit ? Math.max(0.25, 1 - d / (lightR + 1)) : 0.16;
      ctx.fillStyle = shade(col, b);
      ctx.fillRect(x * TS, y * TS, TS, TS);
      if (t === REACTOR && lit) { ctx.fillStyle = 'rgba(255,80,60,' + (0.25 + 0.2 * Math.sin(performance.now() / 200)) + ')'; ctx.fillRect(x * TS, y * TS, TS, TS); }
      if (t === BREACH) { ctx.strokeStyle = shade('#6a5acd', b); ctx.strokeRect(x * TS + 2, y * TS + 2, TS - 4, TS - 4); }
    }
  }

  // salvage
  for (const s of salvage) {
    if (s.taken) continue;
    const d = dist(px, py, s.x + 0.5, s.y + 0.5);
    if (d > lightR && !explored[s.y * COLS + s.x]) continue;
    const b = d <= lightR ? 1 : 0.4;
    ctx.fillStyle = shade(s.col, b);
    ctx.beginPath(); ctx.arc(s.x * TS + TS / 2, s.y * TS + TS / 2, 4, 0, Math.PI * 2); ctx.fill();
    if (d <= lightR) { ctx.fillStyle = 'rgba(255,255,255,.5)'; ctx.font = '8px monospace'; ctx.textAlign = 'center'; ctx.fillText('$' + s.value, s.x * TS + TS / 2, s.y * TS - 3); }
  }

  // enemies (only when visible / lit — they hide in the dark)
  for (const en of enemies) {
    if (!en.alive) continue;
    const d = dist(px, py, en.x, en.y);
    if (d > lightR + 0.5) continue;
    ctx.fillStyle = en.alerted > 0 ? '#ff5252' : '#b34b8c';
    ctx.beginPath(); ctx.arc(en.x * TS, en.y * TS, 5, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#000'; ctx.fillRect(en.x * TS - 2, en.y * TS - 1, 1.5, 1.5); ctx.fillRect(en.x * TS + 1, en.y * TS - 1, 1.5, 1.5);
  }

  // player + flashlight cone hint
  ctx.fillStyle = '#ffd27f';
  ctx.beginPath(); ctx.arc(px * TS, py * TS, 5, 0, Math.PI * 2); ctx.fill();

  // vignette / darkness wash
  const g = ctx.createRadialGradient(px * TS, py * TS, lightR * TS * 0.4, px * TS, py * TS, lightR * TS * 1.3);
  g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0.82)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, cv.width, cv.height);

  // meltdown red pulse
  if (meltdown > 0) {
    ctx.fillStyle = 'rgba(255,30,30,' + (0.10 + 0.10 * Math.sin(performance.now() / 120)) + ')';
    ctx.fillRect(0, 0, cv.width, cv.height);
    ctx.fillStyle = '#ff5252'; ctx.font = 'bold 22px monospace'; ctx.textAlign = 'center';
    ctx.fillText('MELTDOWN ' + meltdown.toFixed(1) + 's', cv.width / 2, 40);
  }
}

function shade(hex, f) {
  const n = parseInt(hex.slice(1), 16);
  let r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
  r = Math.min(255, r * f) | 0; g = Math.min(255, g * f) | 0; b = Math.min(255, b * f) | 0;
  return 'rgb(' + r + ',' + g + ',' + b + ')';
}

// ---------------------------------------------------------------- HUD
function updateHUD() {
  document.getElementById('banked').textContent = banked;
  document.getElementById('quota').textContent = quota;
  document.getElementById('carried').textContent = player.carriedValue;
  document.getElementById('load').textContent = player.load;
  document.getElementById('loadmax').textContent = '/' + MAX_LOAD + ' kg';
  document.getElementById('instFill').style.width = Math.min(100, instability) + '%';
  document.getElementById('oxyFill').style.width = Math.max(0, oxygen) + '%';
}

// ---------------------------------------------------------------- main loop
function frame(now) {
  let dt = (now - last) / 1000; last = now;
  if (dt > 0.05) dt = 0.05; // clamp
  update(dt);
  render();
  requestAnimationFrame(frame);
}

generateWreck((Math.random() * 0xffffffff) >>> 0);
updateHUD();
requestAnimationFrame(frame);

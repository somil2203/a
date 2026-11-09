// Katha Deep animated storybook engine (shared). An episode's scenes.js calls add(t0, t1, draw, transition).
const W = 1080, H = 1920;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, k) => a + (b - a) * k;
const eio = (x) => { x = clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const eo = (x) => 1 - Math.pow(1 - clamp(x), 3);
const back = (x) => { x = clamp(x); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const seg = (t, a, b) => clamp((t - a) / (b - a));
const TT = window.TIMES;   // phrase -> seconds (from the ElevenLabs alignment)
const at = (k) => TT[k];

const DEFS = `<defs>${ART_DEFS}
<radialGradient id="halo"><stop offset="0" stop-color="#FFE7A8" stop-opacity=".95"/><stop offset=".5" stop-color="#FFD36A" stop-opacity=".35"/><stop offset="1" stop-color="#FFC94A" stop-opacity="0"/></radialGradient>
<radialGradient id="rage"><stop offset="0" stop-color="#FF7A3A" stop-opacity=".95"/><stop offset="1" stop-color="#C1121F" stop-opacity="0"/></radialGradient>
<radialGradient id="moonglow"><stop offset="0" stop-color="#FFF6DA" stop-opacity=".7"/><stop offset="1" stop-color="#FFF6DA" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
${[['night', '#0E1433', '#2B2F6B'], ['storm', '#1E2333', '#4A5068'], ['dawn', '#F6B98A', '#FFE9C2'], ['dusk', '#4A1F3D', '#E0875A'], ['saffron', '#F08A2C', '#FFD27A'],
   ['rage', '#3A0A12', '#A3261E'], ['court', '#F3DDB8', '#FFF4E0'], ['sky', '#7FB2E6', '#E8F1FA'], ['gold', '#B8641A', '#FFD27A'], ['maroon', '#2A0E22', '#6E1F2A'], ['rain', '#5E6E8C', '#B9C6D8'], ['day', '#6FA8E8', '#FFF0C9']]
  .map(([id, a, b]) => `<linearGradient id="g_${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient>`).join('')}
<clipPath id="outsideMountain"><path d="M0 0 H1080 V860 H0Z M0 860 H40 V1920 H0Z M1040 860 H1080 V1920 H1040Z"/></clipPath>${window.EXTRA_DEFS || ''}
</defs>`;

function rnd(i) { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
function bg(id) { return `<rect x="-600" y="-600" width="2280" height="3120" fill="url(#g_${id})"/>`; }
function stars(t, n = 70) {
  let s = ''; for (let i = 0; i < n; i++) { const a = 0.35 + 0.65 * Math.abs(Math.sin(t * (1 + rnd(i) * 2) + i)); s += `<circle cx="${rnd(i) * W}" cy="${rnd(i + 99) * H * 0.6}" r="${1.5 + rnd(i + 7) * 2.5}" fill="#FFF6DA" opacity="${a.toFixed(2)}"/>`; } return s;
}
function moon(x, y, r = 60) { return `<circle cx="${x}" cy="${y}" r="${r * 3}" fill="url(#moonglow)"/><circle cx="${x}" cy="${y}" r="${r}" fill="#FFF3D1"/><circle cx="${x + r * 0.45}" cy="${y - r * 0.2}" r="${r * 0.9}" fill="#1A2150" opacity=".9"/>`; }
function sun(x, y, r = 90, col = '#FFE08A') { return `<circle cx="${x}" cy="${y}" r="${r * 2.6}" fill="url(#halo)" opacity=".8"/><circle cx="${x}" cy="${y}" r="${r}" fill="${col}"/>`; }
function dust(t, n = 40, col = '#FFD98A', rise = 40) {
  let s = ''; for (let i = 0; i < n; i++) { const y = ((rnd(i + 3) * H - t * rise * (0.5 + rnd(i))) % H + H) % H; const x = rnd(i) * W + Math.sin(t + i) * 20;
    s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${(2 + rnd(i + 5) * 4).toFixed(1)}" fill="${col}" opacity="${(0.3 + 0.6 * rnd(i + 9)).toFixed(2)}"/>`; } return s;
}
function petals(t, t0, n = 40) {
  let s = ''; for (let i = 0; i < n; i++) { const y = -60 + (t - t0) * (180 + rnd(i) * 140) - rnd(i + 1) * 900; if (y < -60 || y > H) continue; const x = rnd(i + 2) * W + Math.sin(t * 2 + i) * 40;
    s += `<ellipse cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" rx="11" ry="6" fill="${['#F28C28', '#F5C04A', '#E0483A'][i % 3]}" transform="rotate(${((t * 90 + i * 40) % 360).toFixed(0)} ${x.toFixed(1)} ${y.toFixed(1)})"/>`; } return s;
}
function rain(t, dens = 1, alpha = 0.55, slant = 0.18, clip = '', col = '#D6E4FF') {
  let s = ''; const n = Math.round(140 * dens);
  for (let i = 0; i < n; i++) { const sp = 1600 + rnd(i) * 1400, len = 40 + rnd(i + 4) * 70; const y = ((rnd(i + 1) * (H + 300) + t * sp) % (H + 300)) - 150; const x = ((rnd(i + 2) * (W + 400) - 200 + y * slant) % (W + 400)) - 100;
    s += `<line x1="${x.toFixed(1)}" y1="${y.toFixed(1)}" x2="${(x + len * slant).toFixed(1)}" y2="${(y + len).toFixed(1)}" stroke="${col}" stroke-width="${(2 + rnd(i + 3) * 2).toFixed(1)}" stroke-linecap="round" opacity="${(alpha * (0.4 + 0.6 * rnd(i + 6))).toFixed(2)}"/>`; }
  return clip ? `<g clip-path="url(#${clip})">${s}</g>` : s;
}
function wind(t, k = 1) {
  let s = ''; for (let i = 0; i < 14; i++) { const x = ((rnd(i) * W * 1.6 + t * 1800) % (W * 1.6)) - 300, y = rnd(i + 3) * H * 0.8;
    s += `<path d="M${x.toFixed(0)} ${y.toFixed(0)} q120 -30 240 0" stroke="#E6EEFF" stroke-width="4" fill="none" opacity="${(0.35 * k).toFixed(2)}" stroke-linecap="round"/>`; } return s;
}
function ground(y, col = '#5E9E5A', col2 = '#4C8A4A') { return `<path d="M-600 ${y} Q540 ${y - 40} 1680 ${y} V2600 H-600Z" fill="${col}"/><path d="M-600 ${y + 90} Q540 ${y + 50} 1680 ${y + 90} V2600 H-600Z" fill="${col2}"/>`; }
function water(t, level, a = 0.85) { // level = y of water surface
  let p = `M-200 ${level}`; for (let x = -200; x <= 1300; x += 40) p += ` L${x} ${(level + Math.sin(x / 70 + t * 4) * 12).toFixed(1)}`; p += ' V2400 H-200Z';
  return `<path d="${p}" fill="#3E6FA8" opacity="${a}"/><path d="${p}" transform="translate(0 26)" fill="#2D5486" opacity="${a}"/>`;
}
function title(txt, y, size, k, col = '#F5C04A', font = 'Baloo', weight = 800, sub = null, subCol = '#FFF3DC') {
  if (k <= 0) return '';
  const sc = lerp(0.8, 1, back(k)), op = clamp(k * 1.6);
  let s = `<g opacity="${op.toFixed(2)}" transform="translate(540 ${y}) scale(${sc.toFixed(3)})"><text x="0" y="0" text-anchor="middle" font-family="${font}" font-weight="${weight}" font-size="${size}" fill="${col}" stroke="#2A1408" stroke-width="${size * 0.06}" paint-order="stroke" letter-spacing="${size > 100 ? 2 : 1}">${txt}</text>`;
  if (sub) s += `<text x="0" y="${size * 0.5}" text-anchor="middle" font-family="Baloo" font-weight="700" font-size="30" fill="${subCol}" letter-spacing="6">${sub}</text>`;
  return s + '</g>';
}
function counter(n, of, label, x, y, k, col = '#F5C04A') {   // like "RAAT 3/9"
  if (k <= 0) return '';
  return `<g opacity="${clamp(k * 1.5).toFixed(2)}" transform="translate(${x} ${y})"><text x="0" y="-92" font-family="Baloo" font-weight="700" font-size="26" fill="#FFF3DC" letter-spacing="6">${label}</text>
    <text x="0" y="0" font-family="Baloo" font-weight="800" font-size="110" fill="${col}">${n}</text><text x="${n >= 10 ? 120 : 64}" y="0" font-family="Baloo" font-weight="700" font-size="40" fill="#FFF3DC">/${of}</text></g>`;
}
function bubble(x, y, txt, k) {
  if (k <= 0) return '';
  const s = back(k);
  return `<g transform="translate(${x} ${y}) scale(${s.toFixed(3)})" opacity="${clamp(k * 2).toFixed(2)}"><rect x="-200" y="-90" width="400" height="150" rx="60" fill="#FFF8EA" stroke="#2A1B3D" stroke-width="5"/>
    <path d="M-30 58 L-60 120 L20 58Z" fill="#FFF8EA" stroke="#2A1B3D" stroke-width="5" stroke-linejoin="round"/><rect x="-36" y="50" width="70" height="14" fill="#FFF8EA"/>
    <text x="0" y="12" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="62" fill="#2A1B3D">${txt}</text></g>`;
}
const cam = (cx, cy, z, inner) => `<g transform="translate(540 960) scale(${z.toFixed(4)}) translate(${(-cx).toFixed(2)} ${(-cy).toFixed(2)})">${inner}</g>`;
function camPath(t, keys) {   // keys: [[time, cx, cy, z], ...] eased between keys
  if (t <= keys[0][0]) return keys[0].slice(1);
  for (let i = 0; i < keys.length - 1; i++) { const [a, ...p] = keys[i], [b, ...q] = keys[i + 1]; if (t <= b) { const k = eio(seg(t, a, b)); return p.map((v, j) => lerp(v, q[j], k)); } }
  return keys[keys.length - 1].slice(1);
}
const shake = (t, t0, d = 0.6, amp = 18) => { const k = 1 - seg(t, t0, t0 + d); if (t < t0 || k <= 0) return ''; return `translate(${(Math.sin(t * 91) * amp * k).toFixed(1)} ${(Math.cos(t * 77) * amp * 0.7 * k).toFixed(1)})`; };
const flashRect = (t, t0, d = 0.35, col = '#FFF6E0') => { const k = 1 - seg(t, t0, t0 + d); if (t < t0 || k <= 0) return ''; return `<rect width="1080" height="1920" fill="${col}" opacity="${(k * k * 0.9).toFixed(2)}"/>`; };

const S = [];
const add = (t0, t1, draw, tin = 'fade') => S.push({ t0, t1, draw, tin });

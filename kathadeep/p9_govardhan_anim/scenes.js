// Govardhan — animated storybook reel. renderAt(t) draws the frame at time t (seconds), deterministic.
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
<clipPath id="outsideMountain"><path d="M0 0 H1080 V860 H0Z M0 860 H40 V1920 H0Z M1040 860 H1080 V1920 H1040Z"/></clipPath>
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

// ------------------------------------------------------------------ scenes
const S = [];
const add = (t0, t1, draw, tin = 'fade') => S.push({ t0, t1, draw, tin });

// 0 HOOK — night storm, a child holding a mountain
function wideLift(t, o) {
  const lift = o.lift ?? 1;
  let s = bg(o.sky || 'storm');
  if (o.starsOn) s += stars(t);
  s += o.extraSky || '';
  s += ground(1500, o.g1 || '#2F4F3A', o.g2 || '#263F30');
  if (o.rain) s += rain(t, o.rain, 0.6, 0.15, 'outsideMountain');
  if (o.glowDome) s += `<ellipse cx="540" cy="1250" rx="520" ry="380" fill="url(#halo)" opacity="${o.glowDome}"/>`;
  // sheltered villagers + cows
  s += cow({ x: 210, y: 1520, s: 0.5, flip: true }) + cow({ x: 880, y: 1530, s: 0.5 });
  s += person({ x: 120, y: 1540, s: 0.5, gopi: true, veil: '#C2405A', top: '#F2A03D' }) + person({ x: 330, y: 1530, s: 0.48, stick: true, top: '#3E8E5A' });
  s += person({ x: 760, y: 1530, s: 0.48, top: '#C2405A' }) + person({ x: 980, y: 1545, s: 0.5, gopi: true, veil: '#7B4BB7', top: '#F5C04A' });
  const my = lerp(1500, 772, lift);
  s += mountain({ x: lerp(540, 470, lift), y: my, w: 1040, h: 500, lifted: lift > 0.05, sway: t });
  s += krishna({ x: 540, y: 1545, s: 1.0, armL: lerp(18, 166, eo(o.arm ?? 1)), fingerL: (o.arm ?? 1) > 0.02, glow: o.kglow ?? 0.6, eyes: 'closed' });
  return s;
}
add(0, at('कल गोवर्धन'), (t) => {
  const c = camPath(t, [[0, 540, 1110, 2.3], [at('सात दिन तक') - 0.1, 540, 1110, 2.0], [at('सात दिन तक') + 0.9, 540, 1020, 1.45], [at('एक पूरा पहाड़') + 1.2, 540, 960, 1.0],
                        [at('उसके हाथ') + 0.05, 540, 960, 1.0], [at('उसके हाथ') + 0.45, 500, 900, 1.5], [at('कल गोवर्धन'), 520, 940, 1.3]]);
  let s = cam(...c, `<g transform="${shake(t, at('उसके हाथ'), 0.5, 10)}">${wideLift(t, { rain: 1.0 })}</g>`);
  s += rain(t, 0.5, 0.35, 0.15);
  s += counter(7, '', 'DIN TAK', 70, 330, seg(t, at('सात दिन तक'), at('सात दिन तक') + 0.4)).replace('>/<', '><');
  s += flashRect(t, at('उसके हाथ'), 0.3);
  return s;
});

// 1 DEEPOTSAV TRACKER
function tracker(t, lit, glowIdx, igniteT) {
  let s = bg('night') + stars(t) + moon(860, 300, 54);
  const names = ['DHANTERAS', 'CHHOTI DIWALI', 'LAKSHMI PUJA', 'GOVARDHAN', 'BHAI DOOJ'];
  for (let i = 0; i < 5; i++) {
    const x = 140 + i * 200, on = i < lit || (i === glowIdx && t >= igniteT);
    const g = i === glowIdx ? 1 + 0.6 * Math.sin(t * 6) * (t >= igniteT ? 0.4 : 1) : 1;
    s += diya(x, 1180, 0.9, t, i, on, on ? g : 0);
    if (i === glowIdx && t < igniteT) s += `<circle cx="${x}" cy="1150" r="${(70 + 10 * Math.sin(t * 6)).toFixed(1)}" fill="none" stroke="#F5C04A" stroke-width="4" opacity=".6" stroke-dasharray="8 10"/>`;
    s += `<text x="${x}" y="1270" text-anchor="middle" font-family="Baloo" font-weight="700" font-size="24" fill="${i === glowIdx ? '#F5C04A' : '#E8DCC4'}" letter-spacing="2">${names[i]}</text>`;
  }
  if (igniteT && t >= igniteT) { const k = seg(t, igniteT, igniteT + 0.6); const x = 140 + glowIdx * 200;
    s += `<circle cx="${x}" cy="1150" r="${(40 + 260 * eo(k)).toFixed(0)}" fill="none" stroke="#FFE29A" stroke-width="${(10 * (1 - k)).toFixed(1)}" opacity="${(1 - k).toFixed(2)}"/>`; }
  return s;
}
add(at('कल गोवर्धन'), at('भागवत'), (t) => {
  const z = t < at('आज उसकी') ? lerp(1.0, 1.06, seg(t, at('कल गोवर्धन'), at('आज उसकी'))) : lerp(1.06, 4.2, eio(seg(t, at('आज उसकी'), at('भागवत'))));
  const cx = t < at('आज उसकी') ? 540 : lerp(540, 740, eio(seg(t, at('आज उसकी'), at('भागवत') - 0.6)));
  const cy = t < at('आज उसकी') ? 960 : lerp(960, 1130, eio(seg(t, at('आज उसकी'), at('भागवत') - 0.6)));
  let s = cam(cx, cy, z, tracker(t, 3, 3, at('चौथा दिया')));
  const k = seg(t, at('कल गोवर्धन') + 0.1, at('कल गोवर्धन') + 0.6) * (1 - seg(t, at('आज उसकी') + 0.4, at('आज उसकी') + 0.9));
  s += title('गोवर्धन पूजा', 640, 150, k, '#F5C04A', 'Baloo', 800, 'DEEPOTSAV · DIN 4 / 5');
  s += title('CHAUTHA DIYA', 860, 54, seg(t, at('चौथा दिया'), at('चौथा दिया') + 0.4) * (1 - seg(t, at('आज उसकी') + 0.4, at('आज उसकी') + 0.9)), '#FFF3DC');
  return s;
});

// 2 BRAJ — village at dawn, Indra in the clouds, the yajna
add(at('भागवत'), at('नन्हे'), (t) => {
  const c = camPath(t, [[at('भागवत'), 420, 1000, 1.18], [at('इंद्र देव') - 0.2, 640, 1000, 1.12], [at('इंद्र देव') + 0.5, 600, 820, 1.05], [at('यज्ञ होता') - 0.1, 600, 840, 1.05], [at('यज्ञ होता') + 0.8, 540, 1300, 1.3], [at('नन्हे'), 540, 1330, 1.36]]);
  let w = bg('dawn') + sun(820, 520, 90);
  w += cloud(200, 380, 0.7, '#FFF4E4', '#F7DCC4') + cloud(900, 260, 0.5, '#FFF4E4', '#F7DCC4');
  // Indra on Airavata arrives in a cloud bank
  const ik = eo(seg(t, at('इंद्र देव') - 0.1, at('इंद्र देव') + 0.8));
  w += `<g transform="translate(0 ${(-400 * (1 - ik)).toFixed(1)})" opacity="${ik.toFixed(2)}">` + indra({ x: 470, y: 600, s: 0.38 })
       + cloud(330, 720, 1.1, '#FFFFFF', '#E9E4F4') + cloud(560, 740, 0.9, '#FFFFFF', '#E9E4F4') + `</g>`;
  w += mountain({ x: 880, y: 1180, w: 520, h: 300, back: '#5E9466', front: '#79B27A' });
  w += ground(1150, '#8CBF6A', '#78AD5C');
  w += hut(160, 1200, 0.6) + hut(380, 1230, 0.5, '#C98A5A') + tree(620, 1200, 0.6) + hut(1000, 1240, 0.5);
  w += cow({ x: 300 + (t - at('भागवत')) * 18, y: 1340, s: 0.45, ph: t * 5, flip: true }) + cow({ x: 780, y: 1360, s: 0.42, ph: 0 }) + person({ x: 120 + (t - at('भागवत')) * 22, y: 1360, s: 0.42, gopi: true, pot: true, armR: -150, veil: '#C2405A' });
  // yajna in the foreground
  const yk = eo(seg(t, at('यज्ञ होता') - 0.2, at('यज्ञ होता') + 0.5));
  w += `<g opacity="${yk.toFixed(2)}">` + person({ x: 300, y: 1640, s: 0.6, top: '#C2405A', armR: -80, eyes: 'closed' }) + person({ x: 780, y: 1640, s: 0.6, gopi: true, veil: '#3E8E5A', armL: 80 }) + kund(540, 1660, 1.0 * yk, t, lerp(0.6, 1.3, yk)) + `</g>`;
  let s = cam(...c, w);
  const sk = seg(t, at('भागवत'), at('भागवत') + 0.4) * (1 - seg(t, at('ब्रज में') + 0.6, at('ब्रज में') + 1.0));
  s += title('श्रीमद् भागवत', 300, 92, sk, '#7A2E12', 'Baloo', 800, 'DASHAM SKANDH · 24–27', '#7A2E12');
  s += title('INDRA DEV', 300, 84, seg(t, at('इंद्र देव'), at('इंद्र देव') + 0.3) * (1 - seg(t, at('यज्ञ होता') - 0.1, at('यज्ञ होता') + 0.2)), '#FFF3DC');
  s += title('INDRA YAGYA', 300, 84, seg(t, at('यज्ञ होता'), at('यज्ञ होता') + 0.3), '#FFF3DC');
  return s;
});

// 3 NAND BABA & KRISHNA — the question
add(at('नन्हे'), at('इंद्र के लिए'), (t) => {
  const c = camPath(t, [[at('नन्हे'), 420, 1140, 1.5], [at('नंद बाबा') + 0.3, 540, 1080, 1.15], [at('किसके लिए') - 0.2, 470, 1080, 1.3], [at('नंद बोले'), 560, 1000, 1.12], [at('इंद्र के लिए'), 560, 760, 1.2]]);
  let w = bg('court');
  for (let i = 0; i < 4; i++) w += `<path d="M${60 + i * 260} 1300 V640 Q${60 + i * 260 + 100} 520 ${60 + i * 260 + 200} 640 V1300Z" fill="#F7E6C8" stroke="#E8CFA4" stroke-width="6"/>`;
  w += `<rect x="-200" y="1300" width="1500" height="900" fill="#D9A26A"/><rect x="-200" y="1300" width="1500" height="24" fill="#B9814A"/>`;
  w += kund(900, 1380, 0.45, t, 0.8);
  const point = seg(t, at('नंद बोले') + 0.1, at('नंद बोले') + 0.6);
  w += nand({ x: 660, y: 1640, s: 1.05, armR: lerp(-14, -165, eo(point)), armL: 14, eyes: t > at('नंद बोले') ? 'open' : 'closed' });
  const tug = Math.sin(t * 9) * 6 * (t < at('किसके लिए') ? 1 : 0);
  w += krishna({ x: 350, y: 1640, s: 0.82, armR: -70 + tug, armL: 20, eyes: 'open', mouth: (t > at('किसके लिए') - 0.6 && t < at('नंद बोले') && Math.sin(t * 20) > 0) ? 'open' : 'smile', tilt: -6 });
  w += bubble(330, 1020, 'किसके लिए?', seg(t, at('किसके लिए') - 0.5, at('किसके लिए')) * (1 - seg(t, at('नंद बोले') + 0.3, at('नंद बोले') + 0.6)));
  let s = cam(...c, w);
  s += title('NAND BABA', 300, 84, seg(t, at('नंद बाबा'), at('नंद बाबा') + 0.3) * (1 - seg(t, at('किसके लिए') - 0.4, at('किसके लिए') - 0.1)), '#7A2E12');
  return s;
});

// 3b Indra brings rain
add(at('इंद्र के लिए'), at('कृष्ण बोले'), (t) => {
  const c = camPath(t, [[at('इंद्र के लिए'), 540, 820, 1.25], [at('बारिश देते'), 540, 900, 1.05], [at('कृष्ण बोले'), 540, 1000, 1.0]]);
  let w = bg('sky');
  w += indra({ x: 540, y: 880, s: 0.56, aura: 0.6, armR: -140 });
  w += cloud(300, 940, 1.5, '#E9EEF6', '#B9C5D9') + cloud(740, 960, 1.4, '#E9EEF6', '#B9C5D9') + cloud(540, 1000, 1.2, '#F4F7FB', '#C3CEE0');
  const rk = seg(t, at('बारिश देते') - 0.2, at('बारिश देते') + 0.4);
  if (rk > 0) w += `<g opacity="${rk.toFixed(2)}" clip-path="url(#belowClouds)">${rain(t, 1.3, 0.85, 0.05, '', '#4F78B8')}</g>`;
  w += ground(1450, '#7DB868', '#68A257');
  for (let i = 0; i < 9; i++) { const x = 80 + i * 115, h = 30 + 40 * rk + 10 * Math.sin(i); w += `<path d="M${x} 1520 q-10 ${-h} 0 ${-h * 1.4} q10 ${h * 0.4} 0 ${h * 1.4}Z" fill="#3E8E5A"/><path d="M${x} ${1520 - h} q-30 -10 -34 -30 q24 4 34 30Z" fill="#5BA463"/>`; }
  let s = cam(...c, `<clipPath id="belowClouds"><rect x="-500" y="1000" width="2100" height="1500"/></clipPath>` + w);
  s += title('VAHI BAARISH DETE HAIN', 220, 66, seg(t, at('बारिश देते'), at('बारिश देते') + 0.3), '#1C2347', 'Baloo', 800);
  return s;
}, 'up');

// 4 KRISHNA'S ANSWER — dhan = gaayein, sahara = Govardhan
add(at('कृष्ण बोले'), at('और ब्रजवासियों'), (t) => {
  const c = camPath(t, [[at('कृष्ण बोले'), 540, 1180, 1.55], [at('हमारी गायें') - 0.1, 540, 1150, 1.4], [at('हमारी गायें') + 0.9, 540, 1250, 1.05], [at('हमारा सहारा'), 540, 1250, 1.05],
                        [at('गोवर्धन पर्वत') + 0.6, 540, 1000, 0.92], [at('और ब्रजवासियों'), 540, 1040, 0.98]]);
  let w = bg('saffron');
  for (let i = 0; i < 16; i++) { const a = i * 22.5 + t * 4; w += `<path d="M540 900 L${(540 + Math.cos(a * Math.PI / 180) * 2400).toFixed(0)} ${(900 + Math.sin(a * Math.PI / 180) * 2400).toFixed(0)} L${(540 + Math.cos((a + 8) * Math.PI / 180) * 2400).toFixed(0)} ${(900 + Math.sin((a + 8) * Math.PI / 180) * 2400).toFixed(0)}Z" fill="#FFF2C6" opacity=".18"/>`; }
  const mk = eo(seg(t, at('हमारा सहारा') - 0.3, at('गोवर्धन पर्वत') + 0.3));
  w += `<g opacity="${mk.toFixed(2)}" transform="translate(0 ${(200 * (1 - mk)).toFixed(1)})">` + mountain({ x: 540, y: 1420, w: 1300, h: 760, diyas: t > at('पूजा इनकी'), t, sway: t }) + `</g>`;
  w += ground(1400, '#C98A4A', '#B47A3E');
  const ck = eo(seg(t, at('हमारी गायें') - 0.2, at('हमारी गायें') + 0.9));
  w += cow({ x: lerp(-260, 200, ck), y: 1700, s: 0.75, ph: t * 7 * (1 - ck), flip: true, cloth: true }) + cow({ x: lerp(1340, 880, ck), y: 1700, s: 0.75, ph: t * 7 * (1 - ck) });
  const speaking = Math.sin(t * 18) > 0 && t < at('पूजा इनकी') + 1.4;
  const pointUp = seg(t, at('पूजा इनकी') - 0.2, at('पूजा इनकी') + 0.3);
  w += krishna({ x: 540, y: 1660, s: 1.1, armR: lerp(-40 + Math.sin(t * 3) * 10, -150, eo(pointUp)), armL: 20, eyes: 'open', mouth: speaking ? 'open' : 'smile', glow: 0.5 });
  let s = cam(...c, w);
  s += title('HAMARA DHAN', 260, 92, seg(t, at('हमारा') - 0.1, at('हमारा') + 0.3) * (1 - seg(t, at('हमारा सहारा') - 0.3, at('हमारा सहारा'))), '#FFF8E6', 'Baloo', 800, null);
  s += title('= GAAYEIN', 370, 92, seg(t, at('हमारी गायें'), at('हमारी गायें') + 0.3) * (1 - seg(t, at('हमारा सहारा') - 0.3, at('हमारा सहारा'))), '#7A1E12');
  s += title('HAMARA SAHARA', 260, 84, seg(t, at('हमारा सहारा'), at('हमारा सहारा') + 0.3) * (1 - seg(t, at('पूजा इनकी') - 0.2, at('पूजा इनकी'))), '#FFF8E6');
  s += title('GOVARDHAN PARVAT', 370, 84, seg(t, at('गोवर्धन पर्वत'), at('गोवर्धन पर्वत') + 0.3) * (1 - seg(t, at('पूजा इनकी') - 0.2, at('पूजा इनकी'))), '#7A1E12');
  s += title('POOJA INKI KIJIYE', 300, 84, seg(t, at('पूजा इनकी'), at('पूजा इनकी') + 0.3), '#FFF8E6');
  return s;
}, 'zoom');

// 5 BRAJ WORSHIPS GOVARDHAN
add(at('और ब्रजवासियों'), at('इंद्र का अहंकार'), (t) => {
  const c = camPath(t, [[at('और ब्रजवासियों'), 540, 1100, 1.15], [at('इंद्र का अहंकार'), 540, 980, 1.0]]);
  let w = bg('dusk') + sun(540, 760, 120, '#FFC46B');
  w += mountain({ x: 540, y: 1430, w: 1200, h: 720, diyas: true, garland: true, t, sway: t, back: '#3B6E48', front: '#4F8C56' });
  w += ground(1420, '#6B3B2A', '#5A3022');
  const ppl = [['g', 110, '#C2405A', '#F2A03D'], ['m', 290, '#3E8E5A'], ['g', 470, '#7B4BB7', '#F5C04A'], ['m', 640, '#D8432F'], ['g', 820, '#2F7FB8', '#F2A03D'], ['m', 990, '#F2A03D']];
  for (const [k, x, a, b] of ppl) w += k === 'g' ? person({ x, y: 1700, s: 0.62, gopi: true, veil: a, top: b, armL: 150, armR: -150 }) : person({ x, y: 1700, s: 0.62, top: a, armL: 160, armR: -160 });
  w += petals(t, at('और ब्रजवासियों'), 50);
  let s = cam(...c, w);
  s += title('GOVARDHAN PUJA', 300, 96, seg(t, at('और ब्रजवासियों') + 0.6, at('और ब्रजवासियों') + 1.0), '#FFE29A', 'Baloo', 800, 'PEHLI BAAR');
  return s;
});

// 6 INDRA'S RAGE
add(at('इंद्र का अहंकार'), at('प्रलय'), (t) => {
  const c = camPath(t, [[at('इंद्र का अहंकार'), 540, 1020, 1.3], [at('भड़क'), 540, 940, 1.55], [at('प्रलय'), 540, 900, 1.75]]);
  let w = bg('rage');
  for (let i = 0; i < 26; i++) w += flame(rnd(i) * 1080, 1920 - rnd(i + 2) * 160, 1.6 + rnd(i + 3) * 1.6, t, i);
  w += indra({ x: 540, y: 1720, s: 1.25, mood: 'angry', aura: 0.9, armR: -150 });
  w += dust(t, 40, '#FF8A4A', 260);
  let s = cam(...c, `<g transform="${shake(t, at('भड़क'), 0.9, 22)}">${w}</g>`);
  s += title('INDRA KA AHANKAAR', 270, 88, seg(t, at('इंद्र का अहंकार') + 0.1, at('इंद्र का अहंकार') + 0.4), '#FFD1A6');
  s += flashRect(t, at('भड़क'), 0.3, '#FF5A2A');
  return s;
}, 'flash');

// 7 PRALAY — clouds, rain, storm, lightning
add(at('प्रलय'), at('ब्रज डूबने'), (t) => {
  const c = camPath(t, [[at('प्रलय'), 540, 900, 1.2], [at('मूसलाधार'), 540, 1000, 1.05], [at('ब्रज डूबने'), 540, 1050, 1.0]]);
  const ck = eo(seg(t, at('प्रलय') - 0.3, at('प्रलय') + 1.2));
  let w = bg('storm');
  w += ground(1450, '#2F4F3A', '#263F30');
  const bend = 8 * seg(t, at('आँधी') - 0.2, at('आँधी') + 0.3) * (1 + 0.4 * Math.sin(t * 12));
  w += hut(170, 1520, 0.62, '#9A7056') + tree(400, 1500, 0.7, '#2E6E4A', '#22573A', bend) + hut(640, 1540, 0.55, '#9A7056') + tree(900, 1510, 0.8, '#2E6E4A', '#22573A', bend);
  w += rain(t, lerp(0.4, 2.0, seg(t, at('मूसलाधार') - 0.2, at('मूसलाधार') + 0.4)), 0.7, lerp(0.15, 0.5, seg(t, at('आँधी') - 0.2, at('आँधी') + 0.4)));
  if (t > at('आँधी') - 0.2) w += wind(t, seg(t, at('आँधी') - 0.2, at('आँधी') + 0.3));
  for (let i = 0; i < 7; i++) { const x = lerp(-700 + i * 160, 60 + i * 160, ck) + Math.sin(t * 0.8 + i) * 20; w += cloud(x, 260 + (i % 3) * 120, 1.6 + rnd(i) * 0.5, '#3C4258', '#2A2F42'); }
  for (let i = 0; i < 5; i++) { const x = lerp(1800 - i * 200, 1000 - i * 200, ck); w += cloud(x, 520 + (i % 2) * 110, 1.3, '#4B5270', '#363C55'); }
  for (let i = 0; i < 6; i++) { const x = lerp(-900 + i * 220, 0 + i * 220, ck); w += cloud(x, 780 + (i % 2) * 90, 1.1, '#5A617E', '#454B66'); }
  const b0 = at('बिजली');
  if (t > b0 && t < b0 + 0.45) w += bolt(560, 300, 1.4, 7);
  let s = cam(...c, `<g transform="${shake(t, at('बिजली'), 0.6, 18)}">${w}</g>`);
  s += flashRect(t, b0, 0.35, '#DDE8FF');
  s += title('PRALAY KE BAADAL', 300, 84, seg(t, at('प्रलय') + 0.1, at('प्रलय') + 0.4) * (1 - seg(t, at('मूसलाधार') - 0.1, at('मूसलाधार') + 0.1)), '#DDE6FF');
  s += title('MOOSLADHAAR', 300, 96, seg(t, at('मूसलाधार'), at('मूसलाधार') + 0.25) * (1 - seg(t, at('आँधी') - 0.1, at('आँधी'))), '#DDE6FF');
  s += title('AANDHI', 300, 110, seg(t, at('आँधी'), at('आँधी') + 0.2) * (1 - seg(t, at('बिजली') - 0.05, at('बिजली'))), '#DDE6FF');
  s += title('BIJLI', 300, 130, seg(t, at('बिजली'), at('बिजली') + 0.15), '#FFF27A');
  return s;
}, 'wipe');

// 8 FLOOD — everyone runs to Krishna
add(at('ब्रज डूबने'), at('और तब'), (t) => {
  const lv = lerp(1700, 1520, eo(seg(t, at('ब्रज डूबने'), at('गायें, ग्वाले'))));
  const c = camPath(t, [[at('ब्रज डूबने'), 460, 1080, 1.12], [at('सब दौड़े'), 540, 1080, 1.08], [at('और तब'), 700, 1120, 1.2]]);
  let w = bg('storm');
  w += ground(1450, '#2F4F3A', '#263F30') + hut(120, 1520, 0.62, '#9A7056') + hut(420, 1540, 0.55, '#9A7056');
  w += krishna({ x: 800, y: 1560, s: 0.8, glow: 0.9, eyes: 'closed', armL: 30, armR: -30 });
  const run = seg(t, at('गायें, ग्वाले') - 0.3, at('और तब'));
  const runners = [[cow, -60, 1640, 0.5, {}], [person, 120, 1650, 0.5, { stick: true, top: '#3E8E5A' }], [cow, 300, 1650, 0.46, {}], [person, 460, 1640, 0.5, { gopi: true, veil: '#C2405A', top: '#F2A03D' }], [person, 220, 1660, 0.46, { top: '#D8432F' }]];
  runners.forEach(([fn, x0, y, sc, o], i) => { const x = x0 + run * 420; w += fn({ ...o, x, y: y + Math.abs(Math.sin(t * 9 + i)) * -10, s: sc, ph: t * 10, flip: true, armL: 40 + Math.sin(t * 10 + i) * 30, armR: -40 - Math.sin(t * 10 + i) * 30 }); });
  w += water(t, lv);
  w += rain(t, 1.6, 0.65, 0.3);
  let s = cam(...c, w);
  s += title('BRAJ DOOBNE LAGA', 300, 88, seg(t, at('ब्रज डूबने'), at('ब्रज डूबने') + 0.3) * (1 - seg(t, at('सब दौड़े') - 0.2, at('सब दौड़े'))), '#DDE6FF');
  s += title('SAB DAUDE KRISHNA KI OR', 300, 72, seg(t, at('सब दौड़े'), at('सब दौड़े') + 0.3), '#FFE29A');
  return s;
}, 'zoom');

// 9 THE LIFT
add(at('और तब'), at('जैसे कोई'), (t) => {
  const arm = seg(t, at('एक हाथ से') - 0.1, at('एक हाथ से') + 1.0);
  const lift = eio(seg(t, at('उठा लिया') - 0.5, at('उठा लिया') + 0.7));
  const c = camPath(t, [[at('और तब'), 540, 1180, 1.6], [at('एक हाथ से') + 0.8, 520, 1060, 1.3], [at('उठा लिया') - 0.4, 540, 1000, 1.1], [at('उठा लिया') + 0.6, 540, 960, 1.0], [at('जैसे कोई'), 540, 960, 1.04]]);
  let w = wideLift(t, { rain: lerp(1.6, 1.0, lift), lift, arm, kglow: lerp(0.7, 1, lift), glowDome: 0.5 * lift });
  let s = cam(...c, `<g transform="${shake(t, at('उठा लिया') - 0.2, 1.0, 16)}">${w}</g>`);
  if (lift < 0.6) s += rain(t, 0.8, 0.45, 0.15);
  s += flashRect(t, at('उठा लिया') + 0.1, 0.45, '#FFF2C8');
  s += title('EK HAATH SE', 260, 92, seg(t, at('एक हाथ से'), at('एक हाथ से') + 0.3) * (1 - seg(t, at('उठा लिया') - 0.2, at('उठा लिया'))), '#FFE29A');
  s += title('POORA GOVARDHAN!', 230, 92, seg(t, at('उठा लिया'), at('उठा लिया') + 0.3), '#FFE29A');
  return s;
}, 'iris');

// 9b like a child lifts a mushroom (Bhagavata 10.25.19)
add(at('जैसे कोई'), at('सात दिन,'), (t) => {
  const m = eio(seg(t, at('कुकुरमुत्ता') + 0.2, at('कुकुरमुत्ता') + 1.1));
  let s = bg('gold') + dust(t, 50, '#FFF0C0', 30);
  for (let i = 0; i < 18; i++) { const a = i * 20 + t * 6; s += `<path d="M540 1060 L${(540 + Math.cos(a * Math.PI / 180) * 2200).toFixed(0)} ${(1060 + Math.sin(a * Math.PI / 180) * 2200).toFixed(0)} L${(540 + Math.cos((a + 7) * Math.PI / 180) * 2200).toFixed(0)} ${(1060 + Math.sin((a + 7) * Math.PI / 180) * 2200).toFixed(0)}Z" fill="#FFF2C6" opacity=".16"/>`; }
  const up = Math.sin(t * 2) * 8;
  s += `<g transform="translate(0 ${up.toFixed(1)})">`;
  s += `<rect x="512" y="1150" width="56" height="900" rx="28" fill="#4F7FE0"/><circle cx="540" cy="1150" r="34" fill="#4F7FE0"/>`;
  s += `<g opacity="${(1 - m).toFixed(2)}">${mushroom(540, 1130, 1.6)}</g>`;
  s += `<g opacity="${m.toFixed(2)}">${mountain({ x: 540, y: 1100, w: 560, h: 320, lifted: true })}</g>`;
  s += '</g>';
  s += `<text x="540" y="560" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="78" fill="#4A1A08">छत्राकमिव बालकः</text>`;
  s += `<text x="540" y="630" text-anchor="middle" font-family="Baloo" font-weight="700" font-size="30" fill="#5A2A12" letter-spacing="5">BHAGAVAT 10.25.19</text>`;
  s += title(m < 0.5 ? 'KUKURMUTTA' : 'GOVARDHAN', 380, 92, seg(t, at('कुकुरमुत्ता') - 0.1, at('कुकुरमुत्ता') + 0.2), '#FFF8E6');
  return s;
}, 'zoom');

// 10 SEVEN DAYS, SEVEN NIGHTS
add(at('सात दिन,'), at('इंद्र का घमंड'), (t) => {
  const t0 = at('सात दिन,'), t1 = at('पूरा ब्रज');
  const p = seg(t, t0, t1) * 7, day = Math.min(7, 1 + Math.floor(p));
  const ph = p - Math.floor(p), isNight = (ph > 0.5 && t < t1);
  const sky = t >= t1 ? 'storm' : (isNight ? 'night' : 'rain');
  const c = camPath(t, [[t0, 540, 1000, 1.08], [t1, 540, 980, 1.0], [at('इंद्र का घमंड'), 540, 1060, 1.12]]);
  const arcX = lerp(-100, 1180, (ph * 2) % 1), arcY = 700 - Math.sin(((ph * 2) % 1) * Math.PI) * 420;
  const extra = t < t1 ? (isNight ? moon(arcX, arcY, 46) : sun(arcX, arcY, 60, '#FFE6A8')) : '';
  let s = cam(...c, wideLift(t, { sky, starsOn: isNight, extraSky: extra, rain: 1.1, glowDome: t > t1 ? 0.6 * seg(t, t1, t1 + 0.6) : 0.25 }));
  s += counter(day, 7, isNight ? 'RAAT' : 'DIN', 70, 330, 1);
  s += title('POORA BRAJ SURAKSHIT', 1830 - 1600 + 40, 0, 0);
  return s;
}, 'fade');

// 11 INDRA HUMBLED, KAMDHENU, ABHISHEK
add(at('इंद्र का घमंड'), at('उस दिन'), (t) => {
  const t0 = at('इंद्र का घमंड');
  const clear = eo(seg(t, t0 + 0.3, t0 + 2.0));
  const c = camPath(t, [[t0, 660, 980, 1.3], [at('हाथ जोड़कर') - 0.3, 640, 980, 1.26], [at('हाथ जोड़कर') + 0.6, 540, 1080, 1.0], [at('कामधेनु') + 0.6, 540, 940, 0.96], [at('अभिषेक') + 0.5, 420, 1060, 1.1], [at('उस दिन'), 420, 1060, 1.14]]);
  let w = `<g opacity="${(1 - clear).toFixed(2)}">${bg('storm')}</g><g opacity="${clear.toFixed(2)}">${bg('dawn')}${sun(540, 560, 110)}</g>`;
  w += ground(1500, '#8CBF6A', '#78AD5C');
  const fold = t > at('हाथ जोड़कर') - 0.1;
  const crack = t > at('टूट');
  w += krishna({ x: 330, y: 1620, s: 0.95, glow: 0.9, armL: 20, armR: -20, eyes: 'closed' });
  w += indra({ x: 760, y: 1660, s: 0.85, folded: fold, cracked: crack, crownTilt: crack ? lerp(0, -14, eo(seg(t, at('टूट'), at('टूट') + 0.4))) : 0, eyes: 'closed', armR: -20, armL: 20 });
  const kk = eo(seg(t, at('कामधेनु') - 0.3, at('कामधेनु') + 1.0));
  w += `<g opacity="${kk.toFixed(2)}" transform="translate(0 ${(-260 * (1 - kk)).toFixed(1)})">` + cloud(560, 640, 1.2) + cow({ x: 600, y: 600, s: 0.75, crown: true, cloth: true, halo: 0.9, flip: false }) + `</g>`;
  const mk = seg(t, at('अभिषेक') - 0.3, at('अभिषेक') + 0.4);
  if (mk > 0) {
    const yEnd = lerp(560, 1080, mk);
    w += `<path d="M470 520 Q 380 700 340 ${yEnd.toFixed(0)}" stroke="#FFFFFF" stroke-width="26" fill="none" stroke-linecap="round" opacity=".95"/><path d="M470 520 Q 380 700 340 ${yEnd.toFixed(0)}" stroke="#EAF2FF" stroke-width="10" fill="none" stroke-linecap="round"/>`;
    if (mk >= 1) for (let i = 0; i < 14; i++) { const a = rnd(i) * Math.PI, r = ((t * 200 + i * 37) % 120); w += `<circle cx="${(330 + Math.cos(a) * r * 1.4).toFixed(0)}" cy="${(1080 - Math.sin(a) * r * 0.5).toFixed(0)}" r="${(8 - r / 18).toFixed(1)}" fill="#FFFFFF" opacity=".85"/>`; }
    w += dust(t, 30, '#FFF6D0', 60);
  }
  if (t < t0 + 1.8) w += `<g opacity="${(1 - clear).toFixed(2)}">${rain(t, 1.0, 0.5, 0.15)}</g>`;
  let s = cam(...c, w);
  s += title('GHAMAND TOOT GAYA', 300, 84, seg(t, at('टूट'), at('टूट') + 0.3) * (1 - seg(t, at('हाथ जोड़कर') - 0.2, at('हाथ जोड़कर'))), '#FFF3DC');
  s += title('KAMDHENU', 300, 100, seg(t, at('कामधेनु'), at('कामधेनु') + 0.3) * (1 - seg(t, at('अभिषेक') - 0.2, at('अभिषेक'))), '#7A2E12');
  s += title('ABHISHEK', 300, 100, seg(t, at('अभिषेक'), at('अभिषेक') + 0.3), '#7A2E12');
  { const k = 1 - seg(t, at('टूट'), at('टूट') + 0.25); if (t >= at('टूट') && k > 0) s += `<rect width="1080" height="1920" fill="#FFF4DC" opacity="${(k * k * 0.35).toFixed(2)}"/>`; }
  return s;
}, 'fade');

// 12 GOVIND
add(at('उस दिन'), at('इसीलिए'), (t) => {
  const c = camPath(t, [[at('उस दिन'), 540, 1260, 1.35], [at('गोविंद'), 540, 1100, 1.05], [at('इसीलिए'), 540, 1080, 1.0]]);
  let w = bg('gold');
  for (let i = 0; i < 20; i++) { const a = i * 18 + t * 5; w += `<path d="M540 1150 L${(540 + Math.cos(a * Math.PI / 180) * 2400).toFixed(0)} ${(1150 + Math.sin(a * Math.PI / 180) * 2400).toFixed(0)} L${(540 + Math.cos((a + 7) * Math.PI / 180) * 2400).toFixed(0)} ${(1150 + Math.sin((a + 7) * Math.PI / 180) * 2400).toFixed(0)}Z" fill="#FFF2C6" opacity=".2"/>`; }
  w += ground(1560, '#B9813E', '#A06F34');
  w += cow({ x: 200, y: 1700, s: 0.7, flip: true, cloth: true }) + cow({ x: 880, y: 1700, s: 0.7, cloth: true });
  w += krishna({ x: 540, y: 1680, s: 1.15, glow: 1, flute: true, armR: -100, armL: 60, eyes: 'closed' });
  w += dust(t, 50, '#FFF0C0', 40);
  let s = cam(...c, w);
  const gk = seg(t, at('गोविंद') - 0.1, at('गोविंद') + 0.4);
  s += title('गोविंद', 420, 220, gk, '#FFF4D6', 'Baloo', 800, 'GAAYON KE INDRA · BHAGAVAT 10.27', '#4A1A08');
  s += flashRect(t, at('गोविंद'), 0.3, '#FFF6E0');
  return s;
}, 'zoom');

// 13 ANNAKUT
add(at('इसीलिए'), at('और परसों'), (t) => {
  const c = camPath(t, [[at('इसीलिए'), 540, 1200, 1.3], [at('और परसों'), 540, 1100, 1.05]]);
  let w = bg('maroon') + stars(t, 40) + annakut(540, 1500, 1.25, t) + dust(t, 40);
  let s = cam(...c, w);
  s += title('अन्नकूट', 420, 170, seg(t, at('अन्नकूट') - 0.1, at('अन्नकूट') + 0.3), '#F5C04A', 'Baloo', 800, 'KAL · 56 BHOG');
  return s;
}, 'whip');

// 14 PARSON: BHAI DOOJ — teaser
add(at('और परसों'), 999, (t) => {
  const z = lerp(1.0, 1.08, seg(t, at('और परसों'), at('और परसों') + 9));
  const yk = eo(seg(t, at('यमराज') - 0.2, at('यमराज') + 1.0));
  let w = `<g transform="translate(0 ${(-260 * yk).toFixed(1)})" opacity="${(1 - 0.55 * yk).toFixed(2)}">` + tracker(t, 4, 4, at('पाँचवाँ') + 0.2) + `</g>`;
  let riv = `M-200 1560`; for (let x = -200; x <= 1300; x += 40) riv += ` L${x} ${(1560 + Math.sin(x / 90 + t * 2) * 10).toFixed(1)}`; riv += ' V2400 H-200Z';
  const sil = (fn, x, s) => fn(x, 1580, s).replace(/#1B1030/g, '#2C2152');
  w += `<g opacity="${yk.toFixed(2)}"><circle cx="540" cy="1260" r="420" fill="url(#moonglow)"/><circle cx="540" cy="1260" r="190" fill="#FFF3D1" opacity=".9"/>
        <path d="${riv}" fill="#2A3A7A"/><path d="${riv}" transform="translate(0 34)" fill="#1E2A5E"/>
        <path d="M440 1600 Q540 1620 640 1600" stroke="#FFF3D1" stroke-width="6" opacity=".5" fill="none"/><path d="M470 1650 Q540 1662 610 1650" stroke="#FFF3D1" stroke-width="5" opacity=".35" fill="none"/>`
       + `<g transform="translate(0 ${(60 * (1 - yk)).toFixed(1)})">` + sil(yamraj, 400, 0.78) + sil(yamuna, 690, 0.8) + `</g></g>`;
  let s = cam(540, 960, z, w);
  const tk = 1 - seg(t, at('यमराज') - 0.2, at('यमराज') + 0.3);
  s += title('PARSON', 520, 64, seg(t, at('और परसों'), at('और परसों') + 0.3) * tk, '#FFF3DC');
  s += title('BHAI DOOJ', 660, 140, seg(t, at('भाई दूज'), at('भाई दूज') + 0.3) * tk, '#F5C04A', 'Baloo', 800, 'DEEPOTSAV · DIN 5 / 5');
  s += title('YAMRAJ', 330, 120, seg(t, at('यमराज'), at('यमराज') + 0.3), '#F5C04A', 'Baloo', 800, null);
  s += title('AUR UNKI BEHEN YAMUNA', 440, 56, seg(t, at('यमराज') + 0.9, at('यमराज') + 1.2), '#FFF3DC');
  s += title('BHAI DOOJ KI KAHANI · PARSON', 540, 36, seg(t, at('यमराज') + 1.8, at('यमराज') + 2.1), '#F5C04A');
  return s;
}, 'fade');

// ------------------------------------------------------------------ transitions + frame
const TR = { fade: 0.5, zoom: 0.4, up: 0.6, flash: 0.35, wipe: 0.9, iris: 0.7, whip: 0.35 };
function frame(t) {
  let i = S.findIndex((s) => t >= s.t0 && t < s.t1); if (i < 0) i = S.length - 1;
  const cur = S[i];
  let out = cur.draw(t);
  // incoming transition (blend the previous scene over the start of this one)
  const d = TR[cur.tin] || 0.5;
  if (i > 0 && t < cur.t0 + d) {
    const k = eio(seg(t, cur.t0, cur.t0 + d)), prev = S[i - 1].draw(t);
    if (cur.tin === 'zoom') out = `<g opacity="${(1 - k).toFixed(3)}" transform="translate(540 960) scale(${(1 + 0.25 * k).toFixed(3)}) translate(-540 -960)">${prev}</g><g opacity="${k.toFixed(3)}" transform="translate(540 960) scale(${(1.15 - 0.15 * k).toFixed(3)}) translate(-540 -960)">${out}</g>`;
    else if (cur.tin === 'up') out = `<g transform="translate(0 ${(1920 * k).toFixed(1)})">${prev}</g><g transform="translate(0 ${(-1920 * (1 - k)).toFixed(1)})">${out}</g>`;
    else if (cur.tin === 'whip') out = `<g transform="translate(${(-1080 * k).toFixed(1)} 0)">${prev}</g><g transform="translate(${(1080 * (1 - k)).toFixed(1)} 0)">${out}</g>`;
    else if (cur.tin === 'iris') out = `${prev}<clipPath id="irisc"><circle cx="540" cy="1150" r="${(1300 * k).toFixed(1)}"/></clipPath><g clip-path="url(#irisc)">${out}</g>`;
    else if (cur.tin === 'wipe') { // storm clouds sweep across
      let cl = ''; for (let j = 0; j < 9; j++) cl += cloud(lerp(-900, 1900, k) + (j % 3) * 260 - 300, 200 + j * 200, 2.6, '#2E3346', '#22273A');
      out = `<g opacity="${(1 - clamp(k * 1.6 - 0.3)).toFixed(3)}">${prev}</g><g opacity="${clamp(k * 1.6 - 0.3).toFixed(3)}">${out}</g>${k < 1 ? cl : ''}`;
    } else if (cur.tin === 'flash') out = `<g opacity="${(1 - k).toFixed(3)}">${prev}</g><g opacity="${k.toFixed(3)}">${out}</g><rect width="1080" height="1920" fill="#FFE2C0" opacity="${(Math.sin(k * Math.PI) * 0.85).toFixed(2)}"/>`;
    else out = `<g opacity="${(1 - k).toFixed(3)}">${prev}</g><g opacity="${k.toFixed(3)}">${out}</g>`;
  }
  return DEFS + out + `<rect width="1080" height="1920" fill="url(#vig)"/>`;
}

// ------------------------------------------------------------------ subtitles (Hinglish, word highlight)
const SUBS = window.SUBS;
const CHUNKS = (() => { const ch = []; let cur = []; SUBS.forEach((w, i) => { cur.push(i); const n = cur.map((j) => SUBS[j].w).join(' ').length; if (w.br || n > 30) { ch.push(cur); cur = []; } }); if (cur.length) ch.push(cur); return ch; })();
function subs(t) {
  let chunk = null;
  for (const ch of CHUNKS) { const a = SUBS[ch[0]].a - 0.08, b = SUBS[ch[ch.length - 1]].b + 0.35; if (t >= a && t <= b) chunk = ch; }
  if (!chunk) return '';
  return chunk.map((i) => { const w = SUBS[i]; const on = t >= w.a - 0.02 && t <= w.b + 0.06; const past = t > w.b;
    return `<span class="${on ? 'on' : past ? 'past' : 'fut'}${w.key ? ' key' : ''}">${w.w}</span>`; }).join(' ');
}

window.renderAt = (t) => {
  window.T_NOW = t;
  document.getElementById('v').innerHTML = frame(t);
  document.getElementById('subs').innerHTML = subs(t);
};

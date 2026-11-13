// Set 8: Mahabharat — Pandava princes, the crane at the lake, Drona, Eklavya, the clay idol, the dog, bows.
const HUMAN_SKIN = '#D9A07A';
// a bow held vertically; string at x=0, limbs bulge to +x (towards the target). draw 0..1 pulls the string back.
function bowSVG(L = 170, draw = 0, arrow = false) {
  const p = -draw * L * 0.55;
  let g = `<path d="M0 ${-L} C${L * 0.55} ${-L * 0.7} ${L * 0.55} ${L * 0.7} 0 ${L}" stroke="#7A4A22" stroke-width="13" fill="none" stroke-linecap="round"/>
    <path d="M0 ${-L} C${L * 0.5} ${-L * 0.7} ${L * 0.5} ${L * 0.7} 0 ${L}" stroke="#A8743E" stroke-width="5" fill="none"/>
    <rect x="${L * 0.38}" y="-22" width="16" height="44" rx="6" fill="#5A2E14"/>
    <path d="M0 ${-L} L${p.toFixed(1)} 0 L0 ${L}" stroke="#F4ECDC" stroke-width="3" fill="none"/>`;
  if (arrow) g += `<g transform="translate(${p.toFixed(1)} 0)"><rect x="0" y="-3" width="${L * 1.3}" height="6" fill="#7A4A22"/><path d="M${L * 1.3} -12 L${L * 1.3 + 30} 0 L${L * 1.3} 12Z" fill="#C0C6CC"/><path d="M0 0 l-22 -12 l10 12 l-10 12z" fill="#D6332A"/></g>`;
  return g;
}
const holdUp = (sum, inner) => `<g transform="rotate(${-sum})">${inner}</g>`;
function pandav(name, o = {}) {
  const robe = { yudhi: '#E9DDB8', bhima: '#8E2A2A', arjun: '#2F6FB8', nakul: '#2E8A6E', sahdev: '#7E4AA8' }[name] || '#8E2A2A';
  const sum = (o.armR ?? -130) + (o.elbowR ?? -20);
  let held = '';
  if (name === 'bhima') held = holdUp(sum, `<g transform="translate(0 40) scale(1.1)"><rect x="-9" y="-150" width="18" height="190" rx="8" fill="url(#goldG)"/><circle cx="0" cy="-160" r="48" fill="url(#goldG)"/><circle cx="-14" cy="-174" r="12" fill="#FFF0B8"/></g>`);
  else if (name === 'arjun') held = holdUp(sum, `<g transform="translate(6 0)">${bowSVG(190, 0)}</g>`);
  else if (name === 'yudhi') held = holdUp(sum, `<rect x="-6" y="-260" width="12" height="420" rx="6" fill="#8A5A2A"/><path d="M-16 -260 L0 -320 L16 -260Z" fill="#C0C6CC"/>`);
  let s = indra2({ ...o, x: 0, y: 0, s: 1, held: o.held !== undefined ? o.held : held })
    .replace(/url\(#redRobe\)/g, robe).replace(/url\(#skinGold\)/g, o.skin || HUMAN_SKIN).replace(/#F2BC7A/g, o.skin || HUMAN_SKIN);
  if (name === 'bhima') s = `<g transform="scale(1.12 1)">${s}</g>`;
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}
// lying on the ground, head to the left (or right with flip); svg must have its feet at (0,0)
function fallen(svg, x, y, s = 1, flip = false) { return `<g transform="translate(${x} ${y}) scale(${flip ? -s : s} ${s}) rotate(-90)"><g transform="translate(0 -110)">${svg}</g></g>`; }
// the speaking crane (the Yaksha in disguise), standing on one leg in shallow water
function crane(x, y, s, t, talk = 0) {
  const nod = Math.sin(t * 1.6) * 4, open = talk > 0 ? 6 + 6 * Math.abs(Math.sin(t * 14)) : 0;
  return G2(x, y, s, `<path d="M0 0 L4 -150 M4 -150 L30 -110" stroke="#2A2A2A" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-6 -60 L10 -150" stroke="#2A2A2A" stroke-width="7" stroke-linecap="round"/>
    <ellipse cx="0" cy="-200" rx="110" ry="62" fill="#FFFFFF"/><path d="M-20 -230 C-120 -230 -170 -190 -190 -150 C-120 -170 -60 -170 10 -170Z" fill="#B9C2CC"/><path d="M-120 -170 L-200 -130 L-150 -165Z" fill="#3A3F48"/>
    <g transform="rotate(${nod.toFixed(1)} 60 -230)"><path d="M70 -230 C110 -280 50 -330 70 -380 C80 -410 120 -420 140 -400 C120 -380 90 -350 100 -320 C120 -270 110 -230 96 -210Z" fill="#FFFFFF"/>
    <circle cx="112" cy="-396" r="7" fill="#1A1A1A"/><circle cx="114" cy="-398" r="2.5" fill="#FFF"/><path d="M128 -412 C146 -420 158 -420 168 -414" stroke="#2A2A2A" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M136 -398 L250 ${-392 - open / 2} L136 -390Z" fill="#E8A82E"/><path d="M136 -390 L246 ${-386 + open} L136 -384Z" fill="#C98A1E"/></g>
    <ellipse cx="0" cy="4" rx="90" ry="14" fill="#BFE3FF" opacity=".5"/>`);
}
function lake(t, y = 1380, o = {}) {
  let w = `<ellipse cx="540" cy="${y + 120}" rx="900" ry="300" fill="#2E6FB0"/><ellipse cx="540" cy="${y + 110}" rx="860" ry="270" fill="url(#lakeG)"/>`;
  for (let i = 0; i < 9; i++) { const xx = 80 + i * 120 + Math.sin(t * 0.8 + i) * 20, yy = y + 30 + (i % 3) * 70; w += `<path d="M${xx - 40} ${yy} q40 -10 80 0" stroke="#CFE9FF" stroke-width="4" fill="none" opacity="${(0.35 + 0.25 * Math.sin(t * 2 + i)).toFixed(2)}"/>`; }
  if (o.lotus !== false) w += lotus(160, y + 160, 0.32) + lotus(900, y + 120, 0.28) + lotus(760, y + 260, 0.22);
  for (let i = 0; i < 7; i++) w += `<path d="M${-40 + i * 26} ${y + 60} q${8 + Math.sin(t + i) * 6} -120 ${20} -200" stroke="#3E8A3A" stroke-width="7" fill="none"/>`;
  return w;
}
function drona(o = {}) {   // the guru: white beard, saffron, bow on his back
  const back = `<g transform="translate(70 -470) rotate(20)">${bowSVG(200, 0)}</g>`;
  return `<g>${G2(o.x || 0, o.y || 0, o.s || 1, back)}${rishi({ eyes: o.eyes || 'open', ...o })}</g>`;
}
function eklavya(o = {}) {
  const sum = (o.armR ?? -18) + (o.elbowR ?? -14);
  const held = o.bow ? holdUp(sum, `<g transform="translate(4 0)">${bowSVG(150, o.draw || 0, o.arrow)}</g>`) : (o.held || '');
  let s = gwala2({ ...o, x: 0, y: 0, s: 1, skin: '#A86E4E', top: '#2E6A3A', dhoti: '#9A7A4A', held });
  s += `<path d="M30 -486 C44 -560 70 -600 60 -640 C40 -600 26 -560 22 -490Z" fill="#E8762E"/><path d="M40 -540 L52 -600" stroke="#7A3A12" stroke-width="3"/>`;   // feather
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}
// the clay image of Drona that Eklavya made in the forest
function clayIdol(x, y, s, glow = 0) {
  return `${glow ? `<circle cx="${x}" cy="${y - 420 * s}" r="${380 * s}" fill="url(#halo)" opacity="${glow}"/>` : ''}<g filter="url(#clay)">${rishi({ x, y: y - 40 * s, s, eyes: 'closed' })}</g>
    ${G2(x, y, s, `<path d="M-170 0 C-160 -50 160 -50 170 0Z" fill="#8A5634"/><path d="M-120 -30 C-60 -50 60 -50 120 -30" stroke="#A8744E" stroke-width="6" fill="none"/>`)}`;
}
function dog(x, y, s, t, o = {}) {   // facing right; bark opens the mouth; arrows 0..1 fills the mouth with 7 arrows
  const bark = o.bark ? Math.abs(Math.sin(t * 12)) : 0, open = o.arrows > 0 ? 0.7 : bark;
  const wag = Math.sin(t * 10) * 14;
  let g = `<g transform="rotate(${wag.toFixed(1)} -150 -170)"><path d="M-150 -170 C-200 -220 -210 -270 -190 -300" stroke="#B9824E" stroke-width="22" fill="none" stroke-linecap="round"/></g>
    <rect x="-150" y="-120" width="26" height="120" rx="12" fill="#A06A3A"/><rect x="-100" y="-120" width="26" height="120" rx="12" fill="#B9824E"/><rect x="60" y="-120" width="26" height="120" rx="12" fill="#A06A3A"/><rect x="110" y="-120" width="26" height="120" rx="12" fill="#B9824E"/>
    <ellipse cx="-10" cy="-150" rx="170" ry="72" fill="#C99258"/><ellipse cx="-10" cy="-120" rx="120" ry="34" fill="#E2B888"/>`;
  g += `<g transform="translate(150 -230)"><ellipse cx="0" cy="0" rx="78" ry="66" fill="#C99258"/><path d="M-50 -40 C-80 -10 -80 50 -46 60 C-40 20 -30 -10 -20 -40Z" fill="#7A4A2A"/>
    <path d="M30 -10 L120 ${(-6 - 20 * open).toFixed(0)} C130 ${(4 - 20 * open).toFixed(0)} 120 ${(16 - 10 * open).toFixed(0)} 100 ${(16 - 6 * open).toFixed(0)} L30 18Z" fill="#C99258"/>
    <path d="M30 22 L104 ${(26 + 30 * open).toFixed(0)} C110 ${(40 + 30 * open).toFixed(0)} 90 ${(48 + 28 * open).toFixed(0)} 60 ${(44 + 20 * open).toFixed(0)} L28 36Z" fill="#B9824E"/>
    ${open > 0.05 ? `<path d="M40 20 L110 ${(10 + 6 * open).toFixed(0)} L104 ${(28 + 26 * open).toFixed(0)}Z" fill="#7A1E2A"/>` : ''}
    <circle cx="124" cy="${(-12 - 20 * open).toFixed(0)}" r="11" fill="#2A1A1A"/><circle cx="20" cy="-20" r="9" fill="#1A1A1A"/><circle cx="23" cy="-23" r="3" fill="#FFF"/></g>`;
  const k = o.arrows || 0;
  for (let i = 0; i < 7; i++) { const kk = clamp(k * 7 - i); if (kk <= 0) continue; const a = -26 + i * 8;
    const off = (260 * (1 - eo(kk))).toFixed(0);
    g += `<g transform="translate(236 -214) rotate(${a})" opacity="${clamp(kk * 3).toFixed(2)}"><g transform="translate(${off} 0)"><rect x="0" y="-3" width="150" height="6" fill="#7A4A22"/><path d="M150 0 l22 -13 l-8 13 l8 13z M132 0 l22 -13 l-8 13 l8 13z" fill="#D6332A"/></g></g>`; }
  return G2(x, y, s, g, o.flip);
}
function forest(t, dark = 0) {
  let w = bg('day') + `<rect x="-300" y="1380" width="1700" height="900" fill="#4E7A3A"/>`;
  for (let i = 0; i < 7; i++) w += tree2(-60 + i * 190, 1420 + (i % 2) * 30, 1.6 + (i % 3) * 0.3, Math.sin(t * 0.7 + i) * 2, '#2A6A44', '#1E5034', '#3A8A55');
  w += `<rect x="-300" y="1460" width="1700" height="900" fill="#5E8A44"/>`;
  if (dark) w += `<rect x="-300" y="-300" width="1700" height="2600" fill="#0E1A10" opacity="${dark}"/>`;
  return w;
}
function leafPlate(x, y, s, glow = 0) {
  return G2(x, y, s, `${glow ? `<circle cx="0" cy="-30" r="220" fill="url(#halo)" opacity="${glow}"/>` : ''}<path d="M-200 0 C-150 -90 150 -90 200 0 C150 70 -150 70 -200 0Z" fill="#3E8A3A"/><path d="M-190 0 L190 0" stroke="#2A6A2A" stroke-width="4"/>
    ${[-120, -60, 0, 60, 120].map((a) => `<path d="M${a} 0 l30 -30 M${a} 0 l30 30" stroke="#2A6A2A" stroke-width="3"/>`).join('')}`);
}
const ART8_DEFS = `<filter id="clay"><feColorMatrix type="matrix" values="0.19 0.37 0.07 0 0.20  0.13 0.25 0.05 0 0.10  0.09 0.18 0.03 0 0.05  0 0 0 1 0"/></filter>
<linearGradient id="lakeG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5FA8E0"/><stop offset="1" stop-color="#1E5A9A"/></linearGradient>`;

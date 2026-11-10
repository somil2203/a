// Set 5: Yamraj (green-skinned Dharmaraja with gada and pasha), buffalo, Yamuna Devi, Surya's chariot, scales of karma,
// Yamaloka gate, sister's home door.
const YAMA_SKIN = '#4E8A6E', YAMA_SKIN_D = '#3E735A';
function yamraj(o = {}) {
  const gadaHeld = `<g transform="rotate(${-(o.armR ?? -130) - (o.elbowR ?? -20)})"><rect x="-8" y="-150" width="16" height="250" rx="8" fill="url(#goldG)"/><circle cx="0" cy="-160" r="44" fill="url(#goldG)"/><circle cx="-14" cy="-172" r="10" fill="#FFF0B8"/>${[0, 60, 120, 180, 240, 300].map((a) => `<circle cx="${(Math.cos(a * Math.PI / 180) * 44).toFixed(0)}" cy="${(-160 + Math.sin(a * Math.PI / 180) * 44).toFixed(0)}" r="9" fill="#C98A1E"/>`).join('')}</g>`;
  let s = indra2({ ...o, x: 0, y: 0, s: 1, held: o.held !== undefined ? o.held : (o.folded ? undefined : gadaHeld) })
    .replace(/url\(#skinGold\)/g, YAMA_SKIN).replace(/#F2BC7A/g, YAMA_SKIN).replace(/#E9946A/g, YAMA_SKIN_D)
    .replace(/url\(#redRobe\)/g, '#B8282A');
  // yellow uttariya over the shoulders + pasha (noose) at the left hand
  s += `<path d="M-96 -520 C-140 -420 -150 -300 -120 -200 L-100 -210 C-120 -300 -110 -420 -76 -500Z" fill="#F2B233"/><path d="M96 -520 C140 -420 150 -300 120 -200 L100 -210 C120 -300 110 -420 76 -500Z" fill="#F2B233"/>`;
  if (!o.folded && o.pasha !== false) s += `<g transform="translate(-150 -330)"><circle r="36" fill="none" stroke="#C98A1E" stroke-width="7"/><path d="M0 36 q-10 40 6 80" stroke="#C98A1E" stroke-width="7" fill="none"/></g>`;
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}
function buffalo(o = {}) {   // side view, faces left; (0,0) at feet
  const ph = o.ph || 0, sw = (k) => Math.sin(ph + k) * 12;
  const leg = (x, k, far) => `<g transform="${R2(sw(k), x, -150)}"><path d="M${x - 22} -170 C${x - 24} -100 ${x - 18} -50 ${x - 16} -14 L${x + 16} -14 C${x + 18} -50 ${x + 22} -100 ${x + 22} -170Z" fill="${far ? '#2A2530' : '#36303D'}"/><path d="M${x - 18} -16 h36 l4 16 h-44z" fill="#14101A"/></g>`;
  let s = leg(-80, Math.PI, true) + leg(150, 0, true);
  s += `<path d="M200 -260 C230 -230 240 -170 226 -120" stroke="#2A2530" stroke-width="10" fill="none"/><path d="M226 -132 c-14 12 -10 36 2 42 c10 -8 12 -32 -2 -42z" fill="#14101A"/>`;
  s += `<path d="M-150 -290 C-120 -330 40 -330 160 -310 C220 -300 240 -250 230 -200 C220 -150 190 -130 150 -126 C60 -116 -40 -116 -110 -128 C-150 -136 -170 -170 -170 -210 C-170 -250 -164 -276 -150 -290Z" fill="#3A3442"/>`;
  s += `<path d="M-120 -300 C-60 -324 60 -322 150 -306" stroke="#4E4858" stroke-width="10" fill="none" opacity=".6"/>`;
  if (o.cloth !== false) s += `<path d="M-70 -312 C0 -322 70 -318 120 -306 L130 -200 C70 -186 0 -186 -60 -196Z" fill="#B8282A"/><path d="M-60 -196 C0 -186 70 -186 130 -200" stroke="#F5C04A" stroke-width="12" fill="none"/>${[0, 1, 2, 3].map((i) => `<circle cx="${-30 + i * 48}" cy="${-252 + (i % 2) * 10}" r="9" fill="#F5C04A"/>`).join('')}`;
  s += leg(-110, 0, false) + leg(180, Math.PI, false);
  s += `<path d="M-150 -280 C-200 -290 -250 -270 -270 -230 L-280 -170 C-270 -140 -230 -130 -200 -150 C-176 -170 -160 -210 -150 -240Z" fill="#3A3442"/>`;
  s += `<ellipse cx="-262" cy="-156" rx="34" ry="26" fill="#5A5262"/><circle cx="-272" cy="-158" r="5" fill="#14101A"/><circle cx="-250" cy="-160" r="5" fill="#14101A"/>`;
  s += `<path d="M-230 -270 C-280 -330 -360 -320 -380 -270 C-350 -300 -300 -300 -250 -250Z" fill="#E8DCC0"/><path d="M-180 -284 C-150 -340 -70 -350 -40 -310 C-80 -330 -130 -320 -170 -264Z" fill="#E8DCC0"/>`;
  s += `<path d="M-236 -220 q10 8 20 0" stroke="#F5C04A" stroke-width="4" fill="none"/><path d="M-210 -150 C-190 -130 -160 -128 -140 -142" stroke="#B8282A" stroke-width="8" fill="none"/><path d="M-176 -136 l-10 26 h24z" fill="url(#goldG)"/>`;
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}
function yamaRiding(x, y, s, t, o = {}) {   // Yama seated on his buffalo
  return G2(x, y, s, yamraj({ x: 20, y: -150, s: 0.62, eyes: o.eyes || 'closed', armR: o.armR ?? -130, elbowR: o.elbowR ?? -20, armL: 30 }) + buffalo({ x: 0, y: 0, s: 1, ph: o.walk ? t * 6 : 0 }));
}
function yamunaDevi(o = {}) {
  return gopi2({ veil: '#2A4AA8', top: '#2A4AA8', skirt: '#1E3A8A', ...o }).replace(/#E8A983/g, '#B07A56') +
    G2(o.x || 0, o.y || 0, o.s || 1, `<path d="M-40 -508 l40 -26 l40 26 l-10 -34 l-18 12 l-12 -28 l-12 28 l-18 -12z" fill="url(#goldG)"/>`);
}
function suryaRath(x, y, s, t) {
  let g = `<circle cx="0" cy="-120" r="300" fill="url(#halo)" opacity=".9"/>`;
  for (let i = 0; i < 16; i++) { const a = i * 22.5 + t * 10; g += `<path d="M0 -120 L${(Math.cos(a * Math.PI / 180) * 240).toFixed(0)} ${(-120 + Math.sin(a * Math.PI / 180) * 240).toFixed(0)}" stroke="#FFD24A" stroke-width="14" stroke-linecap="round" opacity=".6"/>`; }
  g += `<circle cx="0" cy="-120" r="150" fill="#FFC23A"/><circle cx="0" cy="-120" r="118" fill="#FFD966"/><path d="M-40 -130 q8 -8 16 0 M24 -130 q8 -8 16 0" stroke="#C97A10" stroke-width="5" fill="none"/><path d="M-26 -90 q26 18 52 0" stroke="#C97A10" stroke-width="5" fill="none"/>`;
  g += `<path d="M-120 60 L160 60 L140 0 L-100 0Z" fill="url(#goldG)"/><circle cx="-60" cy="70" r="40" fill="none" stroke="#C98A1E" stroke-width="10"/><circle cx="100" cy="70" r="40" fill="none" stroke="#C98A1E" stroke-width="10"/>`;
  return G2(x, y, s, g);
}
function scales(x, y, s, t) {
  const a = Math.sin(t * 1.6) * 8;
  return G2(x, y, s, `<rect x="-10" y="-300" width="20" height="300" fill="url(#goldG)"/><path d="M-80 0 h160 l-20 -30 h-120z" fill="url(#goldG)"/>
    <g transform="rotate(${a.toFixed(1)} 0 -290)"><rect x="-200" y="-298" width="400" height="16" rx="8" fill="url(#goldG)"/>
      <g transform="rotate(${(-a).toFixed(1)} -190 -290)"><path d="M-190 -290 L-250 -170 M-190 -290 L-130 -170" stroke="#C98A1E" stroke-width="4"/><path d="M-260 -170 Q-190 -120 -120 -170Z" fill="url(#goldG)"/></g>
      <g transform="rotate(${(-a).toFixed(1)} 190 -290)"><path d="M190 -290 L130 -170 M190 -290 L250 -170" stroke="#C98A1E" stroke-width="4"/><path d="M120 -170 Q190 -120 260 -170Z" fill="url(#goldG)"/></g></g>
    <circle cx="0" cy="-310" r="18" fill="#F5C04A"/>`);
}
function yamlokGate(x, y, s, open = 0, t = 0) {
  const fl = (fx) => flame(fx, -560, 1.2, t, fx);
  return G2(x, y, s, `<rect x="-420" y="-900" width="840" height="900" fill="#2A1418"/><path d="M-460 -900 L460 -900 L420 -980 L-420 -980Z" fill="#3A1A20"/>
    <rect x="-470" y="-900" width="70" height="900" fill="#3A1A20"/><rect x="400" y="-900" width="70" height="900" fill="#3A1A20"/>
    <circle cx="0" cy="-820" r="60" fill="#5A2A30"/><circle cx="0" cy="-820" r="34" fill="#8E1F2A"/>
    <rect x="-330" y="-740" width="660" height="740" fill="#0E0608"/>
    <g transform="translate(${(-330 * open).toFixed(0)} 0)"><rect x="-330" y="-740" width="330" height="740" fill="#5A2A22"/>${[0, 1, 2, 3].map((r) => [0, 1].map((c) => `<rect x="${-300 + c * 150}" y="${-700 + r * 175}" width="120" height="140" rx="10" fill="#6E3A2E" stroke="#3A1A14" stroke-width="6"/>`).join('')).join('')}<circle cx="-40" cy="-380" r="16" fill="#C98A1E"/></g>
    <g transform="translate(${(330 * open).toFixed(0)} 0)"><rect x="0" y="-740" width="330" height="740" fill="#5A2A22"/>${[0, 1, 2, 3].map((r) => [0, 1].map((c) => `<rect x="${30 + c * 150}" y="${-700 + r * 175}" width="120" height="140" rx="10" fill="#6E3A2E" stroke="#3A1A14" stroke-width="6"/>`).join('')).join('')}<circle cx="40" cy="-380" r="16" fill="#C98A1E"/></g>
    ${open > 0 ? `<rect x="${(-330 * open + 0).toFixed(0)}" y="-740" width="${(660 * open).toFixed(0)}" height="740" fill="url(#rage)" opacity=".5"/>` : ''}
    <rect x="-380" y="-600" width="20" height="80" fill="#3A1A14"/><rect x="360" y="-600" width="20" height="80" fill="#3A1A14"/>${fl(-370)}${fl(370)}`);
}
function sisterHome(x, y, s, t, o = {}) {   // a modest home with toran, diyas and rangoli at the door
  let g = `<rect x="-360" y="-560" width="720" height="560" fill="#E8C49A"/><path d="M-420 -540 L0 -800 L420 -540Z" fill="#B8553A"/><path d="M-420 -540 L420 -540 L400 -510 L-400 -510Z" fill="#8E3A26"/>
    <rect x="-130" y="-420" width="260" height="420" rx="120" fill="${o.open ? '#FFD27A' : '#6E3A22'}"/>${o.open ? `<rect x="-130" y="-420" width="260" height="420" rx="120" fill="url(#halo)"/>` : ''}
    <path d="M-150 -430 Q0 -380 150 -430" stroke="#2E8A4E" stroke-width="10" fill="none"/>${[-120, -80, -40, 0, 40, 80, 120].map((xx, i) => `<path d="M${xx} ${-424 + Math.abs(xx) * 0.1} l-10 34 l20 0z" fill="${i % 2 ? '#F28C28' : '#3E8E5A'}"/>`).join('')}
    <rect x="-300" y="-380" width="100" height="120" rx="8" fill="#6E3A22"/><rect x="200" y="-380" width="100" height="120" rx="8" fill="#6E3A22"/>
    <ellipse cx="0" cy="40" rx="260" ry="50" fill="#F4EBDD" opacity=".9"/>${[0, 1, 2, 3, 4, 5, 6, 7].map((i) => `<ellipse cx="${(Math.cos(i * Math.PI / 4) * 160).toFixed(0)}" cy="${(40 + Math.sin(i * Math.PI / 4) * 30).toFixed(0)}" rx="40" ry="12" fill="${['#D6332A', '#F5B935', '#2E8A4E', '#7B4BB7'][i % 4]}" transform="rotate(${i * 45} ${(Math.cos(i * Math.PI / 4) * 160).toFixed(0)} ${(40 + Math.sin(i * Math.PI / 4) * 30).toFixed(0)})"/>`).join('')}<circle cx="0" cy="40" r="30" fill="#F5B935"/>`;
  g += diya(-200, 0, 0.6, t, 1) + diya(200, 0, 0.6, t, 2);
  return G2(x, y, s, g);
}

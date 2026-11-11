// Set 6: Chitragupta + ledger/pen/inkpot, rishi, Jabala, Satyakama (boy), bull, swan, diver bird, cow counter.
function quill(x, y, s, a = 0) {
  return G2(x, y, s, `<g transform="rotate(${a})"><path d="M0 0 C-30 -60 -40 -140 -10 -220 C10 -150 14 -70 0 0Z" fill="#FFF6E2" stroke="#D9C8A8" stroke-width="3"/><path d="M-2 -10 L-14 -200" stroke="#C9B48A" stroke-width="3"/><path d="M0 0 l-4 26 l6 -2z" fill="#2A1B3D"/></g>`);
}
function dawat(x, y, s) {
  return G2(x, y, s, `<ellipse cx="0" cy="6" rx="58" ry="14" fill="#000" opacity=".2"/><path d="M-50 0 C-56 -50 -36 -70 0 -70 C36 -70 56 -50 50 0Z" fill="#1E2A4A"/><ellipse cx="0" cy="-66" rx="30" ry="9" fill="#0E1426"/><path d="M-40 -30 Q0 -20 40 -30" stroke="#F5C04A" stroke-width="5" fill="none"/>`);
}
function ledger(x, y, s, t, lines = 1, o = {}) {   // big open book; lines 0..1 = how much of the page is written
  let g = `<path d="M-420 40 L0 70 L420 40 L420 -460 L0 -430 L-420 -460Z" fill="#8E1F2A"/><path d="M-400 20 L0 50 L400 20 L400 -470 L0 -440 L-400 -470Z" fill="#F4EBDD"/><path d="M0 -440 L0 50" stroke="#C9B48A" stroke-width="4"/>`;
  const n = 14, shown = lines * n * 2;
  for (let i = 0; i < n * 2; i++) { const side = i < n ? -1 : 1, row = i % n, k = clamp(shown - i);
    if (k <= 0) continue; const x0 = side < 0 ? -370 : 30, w = 300 * k * (0.7 + 0.3 * rnd(i + 3));
    g += `<path d="M${x0} ${-420 + row * 31 + (side < 0 ? -row * 0.8 : row * 0.8)} h${w.toFixed(0)}" stroke="${o.ink || '#2A2A44'}" stroke-width="5" stroke-linecap="round" opacity=".8"/>`; }
  return G2(x, y, s, g);
}
function chitragupta(o = {}) {
  const pen = `<g transform="rotate(${-(o.armR ?? -60) - (o.elbowR ?? -70)})">${quill(0, 0, 0.8, 30)}</g>`;
  let s = indra2({ ...o, x: 0, y: 0, s: 1, held: pen }).replace(/url\(#redRobe\)/g, '#E8A42A').replace(/url\(#skinGold\)/g, '#E9B07A').replace(/#F2BC7A/g, '#E9B07A');
  return G2(o.x || 0, o.y || 0, o.s || 1, s);
}
function rishi(o = {}) { return nand2({ eyes: 'closed', ...o }).replace(/#F08A2C/g, '#DADADA').replace(/#C9631A/g, '#BDBDBD').replace(/url\(#creamG\)/g, '#E8762E').replace(/#F4ECDC/g, '#E8762E').replace(/#E86A3E/g, '#C9A27A'); }
function jabala(o = {}) { return gopi2({ veil: '#E9E2D2', top: '#C9A27A', skirt: '#E2D8C4', ...o }).replace(/#E8A983/g, '#C98E68'); }
function satyakam(o = {}) {
  return vamana({ umbrella: false, ...o }).replace(/url\(#kBlueV\)/g, '#C98A62').replace(/url\(#kBlue\)/g, '#D9A07A').replace(/#4E7EE6/g, '#D9A07A').replace(/#3E66C8/g, '#C08060').replace(/#3A62C2/g, '#B9805C').replace(/#3A60BE/g, '#B07858').replace(/url\(#pitam\)/g, '#F4F1EA').replace(/#F0B42A/g, '#E6E0D2');
}
function bull(o = {}) { return cow2({ ...o, body: undefined }).replace(/url\(#cowG\)/g, '#E8E2D8').replace(/<path d="M-74 -306 C-60 -330 -30 -326 -30 -300 C-46 -296 -62 -296 -74 -306Z" fill="#F7F1E6"\/>/, '<path d="M-90 -300 C-80 -380 -10 -380 -20 -290 C-46 -286 -70 -288 -90 -300Z" fill="#E8E2D8"/>'); }
function swan(x, y, s, t) {
  const b = Math.sin(t * 2) * 6;
  return G2(x, y + b, s, `<ellipse cx="0" cy="0" rx="110" ry="50" fill="#FFFFFF"/><path d="M-60 -20 C-140 -60 -140 -180 -80 -200 C-40 -210 -30 -170 -60 -150 C-90 -130 -80 -60 -40 -30Z" fill="#FFFFFF"/>
    <path d="M-80 -200 l-40 10 l38 8z" fill="#F28C28"/><circle cx="-80" cy="-190" r="5" fill="#1A1A1A"/><path d="M0 -20 C40 -60 100 -50 120 -10" stroke="#E8E8F0" stroke-width="10" fill="none"/>
    <path d="M-160 30 Q0 60 160 30" stroke="#7FB8F0" stroke-width="8" fill="none" opacity=".6"/>`);
}
function diverBird(x, y, s, t) {   // madgu, a water bird
  return G2(x, y, s, `<ellipse cx="0" cy="0" rx="80" ry="36" fill="#2E3A4A"/><circle cx="-80" cy="-30" r="30" fill="#2E3A4A"/><path d="M-106 -30 l-50 8 l50 6z" fill="#E8B04A"/><circle cx="-90" cy="-36" r="5" fill="#FFF"/><circle cx="-90" cy="-36" r="2.5" fill="#000"/>
    <path d="M-10 -20 C30 -50 70 -40 90 -10" stroke="#4A5A6E" stroke-width="10" fill="none"/><path d="M-120 30 Q0 50 120 30" stroke="#7FB8F0" stroke-width="8" fill="none" opacity=".6"/>`);
}
function ashram(t) {
  let w = bg('dawn') + sun(820, 420, 80) + `<rect x="-300" y="1440" width="1700" height="900" fill="#9CC46E"/>`;
  w += tree2(200, 1460, 1.2, Math.sin(t * 2) * 3) + hut(860, 1460, 0.75, '#C9955A');
  w += kund(560, 1520, 0.4, t, 0.6);
  return w;
}

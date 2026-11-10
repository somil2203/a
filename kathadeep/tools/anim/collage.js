// Collage / editorial motion-graphics kit (reference grammar studied from the viral Bhai Dooj reel, executed originally):
// top-left condensed caps built word-by-word, mono pills, paper cards, calendar, strikethrough list, stamps, manuscripts.
const ANTON = 'Anton';
const _mcache = {};
function mw(txt, size) {
  const k = txt + '|' + size; if (_mcache[k]) return _mcache[k];
  const c = document.createElement('canvas').getContext('2d'); c.font = `${size}px Anton`; const w = c.measureText(txt).width;
  if (document.fonts && document.fonts.check(`${size}px Anton`)) _mcache[k] = w; return w;
}
const INK = '#16110E', PAPER = '#F4EBDD', PAPER2 = '#EADFCB', RED = '#D6332A', GOLDT = '#F5B935';

// One caption = up to 2 lines. Words of line 1 appear one by one from t0; line 2 from t2 (or right after line 1).
function kcap(t, c) {
  const { t0, l1, l2 = '', acc = RED, dark = false, t2, te, y = 330, size = 92 } = c;
  if (t < t0 || (te && t > te + 0.18)) return '';
  const out = te ? clamp((te + 0.18 - t) / 0.18) : 1;
  const col1 = dark ? INK : '#FFFFFF', sh = dark ? 'none' : 'url(#capShadow)';
  const words = (txt, tStart, yy, col, size) => {
    let x = 58, s = '';
    txt.split(' ').forEach((w, i) => {
      const k = clamp((t - tStart - i * 0.11) / 0.14); if (k <= 0) { x += mw(w, size) + size * 0.24; return; }
      const sc = 1 + 0.18 * (1 - eo(k));
      s += `<text x="${x.toFixed(1)}" y="${yy}" font-family="${ANTON}" font-size="${size}" fill="${col}" opacity="${k.toFixed(2)}" filter="${sh}" transform="translate(${x} ${yy}) scale(${sc.toFixed(3)}) translate(${-x} ${-yy})" letter-spacing="0.5">${w}</text>`;
      x += mw(w, size) + size * 0.24;
    });
    return s;
  };
  const fit = (txt) => { const w = txt.split(' ').reduce((a, x) => a + mw(x, size) + size * 0.24, 0) - size * 0.24; return w > 964 ? size * 964 / w : size; };
  const tl2 = t2 ?? t0 + l1.split(' ').length * 0.11 + 0.15;
  const s1 = fit(l1), s2 = l2 ? fit(l2) : size;
  return `<g opacity="${out.toFixed(2)}">${words(l1, t0, y, col1, s1)}${l2 ? words(l2, tl2, y + s1 * 0.12 + s2 * 0.9, acc, s2) : ''}</g>`;
}
// list of captions: each ends when the next begins
function caps(t, list) {
  let s = '';
  list.forEach((c, i) => { const next = list[i + 1]; s += kcap(t, { ...c, te: c.te ?? (next ? next.t0 - 0.2 : undefined) }); });
  return s;
}
function pill(t, t0, txt, x, y, o = {}) {
  if (t < t0 || (o.te && t > o.te)) return '';
  const k = eo(seg(t, t0, t0 + 0.25)), w = txt.length * 15.5 + 34, bg = o.bg || INK, fg = o.fg || '#F4EBDD';
  const xx = o.right ? x - w : (o.center ? x - w / 2 : x);
  return `<g opacity="${k.toFixed(2)}" transform="translate(${(xx + (1 - k) * -20).toFixed(1)} ${y})"><rect x="0" y="-30" width="${w}" height="44" rx="6" fill="${bg}"/><text x="17" y="0" font-family="SpaceMono" font-weight="700" font-size="24" fill="${fg}" letter-spacing="1">${txt}</text></g>`;
}
function tagTR(txt) { return `<g transform="translate(1022 150)"><rect x="${-txt.length * 14 - 30}" y="-26" width="${txt.length * 14 + 30}" height="38" rx="6" fill="${INK}" opacity=".85"/><text x="-15" y="0" text-anchor="end" font-family="SpaceMono" font-weight="700" font-size="21" fill="#F4EBDD" letter-spacing="1">${txt}</text></g>`; }
function paper(x, y, w, h, rot, inner, o = {}) {
  let edge = `M0 0`; for (let i = 1; i <= 12; i++) edge += ` L${(w * i / 12).toFixed(0)} ${(rnd(i + (o.seed || 0)) * 8 - 4).toFixed(0)}`;
  edge += ` L${w} ${h}`; for (let i = 11; i >= 0; i--) edge += ` L${(w * i / 12).toFixed(0)} ${(h + rnd(i + 30 + (o.seed || 0)) * 8 - 4).toFixed(0)}`; edge += 'Z';
  return `<g transform="translate(${x} ${y}) rotate(${rot})"><path d="${edge}" transform="translate(10 14)" fill="#000" opacity=".22" filter="url(#blur6)"/><path d="${edge}" fill="${o.fill || PAPER}"/>
    ${o.tape ? `<rect x="${w / 2 - 60}" y="-20" width="120" height="38" fill="#E8D9A8" opacity=".8" transform="rotate(-4 ${w / 2} 0)"/>` : ''}${inner}</g>`;
}
function invite(x, y, s, rot) {   // Yamuna's invitation card
  return G2(x, y, s, paper(-170, -110, 340, 220, rot, `<circle cx="70" cy="110" r="44" fill="${GOLDT}"/><circle cx="70" cy="110" r="44" fill="none" stroke="#C98A1E" stroke-width="5" stroke-dasharray="6 6"/>
    <path d="M52 112 q18 -30 36 0 q-18 12 -36 0z" fill="#E86A3E"/><text x="132" y="98" font-family="Baloo" font-weight="800" font-size="46" fill="${INK}">घर आओ</text><text x="132" y="148" font-family="Baloo" font-weight="800" font-size="46" fill="${RED}">भैया</text>
    <text x="132" y="188" font-family="SpaceMono" font-weight="700" font-size="20" fill="#6A5A4A">— YAMUNA</text>`, { seed: Math.round(rot * 3) }));
}
function calendar(x, y, s, t, o = {}) {   // November 2026 (1 Nov = Sunday)
  const ticks = o.ticks || [], circ = o.circle, kc = o.kc ?? 1;
  let g = `<rect x="-280" y="-250" width="560" height="560" rx="12" fill="${PAPER}"/><rect x="-280" y="-250" width="560" height="110" rx="12" fill="${RED}"/><rect x="-280" y="-160" width="560" height="20" fill="${RED}"/>
    <text x="-240" y="-178" font-family="${ANTON}" font-size="58" fill="#FFF">NOVEMBER</text><text x="240" y="-178" text-anchor="end" font-family="${ANTON}" font-size="40" fill="#FFE2D8">2026</text>`;
  ['S', 'M', 'T', 'W', 'T', 'F', 'S'].forEach((d, i) => { g += `<text x="${-225 + i * 75}" y="-104" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="22" fill="#8A7A6A">${d}</text>`; });
  for (let d = 1; d <= 30; d++) { const i = d - 1, cx = -225 + (i % 7) * 75, cy = -54 + Math.floor(i / 7) * 70;
    g += `<text x="${cx}" y="${cy}" text-anchor="middle" font-family="${ANTON}" font-size="34" fill="${INK}">${d}</text>`;
    if (ticks.includes(d)) g += `<path d="M${cx - 18} ${cy - 16} l12 14 l26 -30" stroke="${RED}" stroke-width="6" fill="none" stroke-linecap="round"/>`;
    if (d === circ && kc > 0) { const r = 34, len = 2 * Math.PI * r; g += `<circle cx="${cx}" cy="${cy - 12}" r="${r}" fill="none" stroke="${GOLDT}" stroke-width="7" stroke-dasharray="${(len * kc).toFixed(0)} ${len.toFixed(0)}"/>`; } }
  return G2(x, y, s, `<g transform="translate(10 14)" opacity=".2"><rect x="-280" y="-250" width="560" height="560" rx="12" fill="#000" filter="url(#blur6)"/></g>${g}`);
}
function strikeList(t, x, y, items, o = {}) {   // items: [txt, tIn, tStrike]
  let s = '';
  items.forEach(([txt, tin, tst], i) => {
    if (t < tin) return; const k = eo(seg(t, tin, tin + 0.22)), yy = y + i * 120, w = txt.length * 34 + 60;
    s += `<g opacity="${k.toFixed(2)}" transform="translate(${x + (1 - k) * -30} ${yy})">${paper(0, -60, w, 86, (i % 2 ? 1.5 : -1.5), `<text x="30" y="58" font-family="${ANTON}" font-size="56" fill="${INK}">${txt}</text>`, { seed: i * 7 })}`;
    if (tst && t > tst) { const ks = eo(seg(t, tst, tst + 0.2)); s += `<path d="M18 -14 L${(18 + (w - 30) * ks).toFixed(0)} -20" stroke="${RED}" stroke-width="10" stroke-linecap="round"/>`; }
    s += `</g>`;
  });
  return s;
}
function stamp2(t, t0, txt, x, y, o = {}) {
  const st = seg(t, t0 - 0.05, t0 + 0.22); if (st <= 0) return ''; const sc = lerp(2.0, 1, eo(st)), w = txt.length * 40 + 80;
  return `<g transform="translate(${x} ${y}) rotate(${o.rot ?? -9}) scale(${sc.toFixed(3)})" opacity="${clamp(st * 2).toFixed(2)}"><rect x="${-w / 2}" y="-56" width="${w}" height="112" rx="14" fill="none" stroke="${o.col || RED}" stroke-width="9"/>
    <text x="0" y="22" text-anchor="middle" font-family="${ANTON}" font-size="70" fill="${o.col || RED}" letter-spacing="3">${txt}</text></g>`;
}
function pothi(x, y, s, label, t) {   // palm-leaf manuscript bundle in red cloth
  return G2(x, y, s, `<ellipse cx="0" cy="40" rx="330" ry="30" fill="#000" opacity=".18"/><rect x="-320" y="-50" width="640" height="90" rx="40" fill="#E8D4A8"/><rect x="-320" y="-50" width="640" height="90" rx="40" fill="none" stroke="#C9A86A" stroke-width="4"/>
    ${[-30, -10, 10].map((yy) => `<path d="M-300 ${yy} H300" stroke="#C9A86A" stroke-width="2"/>`).join('')}<rect x="-340" y="-70" width="680" height="40" rx="18" fill="#8E1F2A"/><path d="M-330 -50 H330" stroke="${GOLDT}" stroke-width="6" stroke-dasharray="10 10"/>
    <circle cx="0" cy="-50" r="26" fill="${GOLDT}"/><path d="M-12 -40 q12 -24 24 0" stroke="#8E1F2A" stroke-width="4" fill="none"/><path d="M-30 30 q-30 40 -70 46 M30 30 q30 40 70 46" stroke="${RED}" stroke-width="10" fill="none" stroke-linecap="round"/>`)
    + (label ? pill(t, 0, label, x, y + 130 * s, { center: true }) : '');
}
const COLLAGE_DEFS = `<filter id="capShadow" x="-10%" y="-10%" width="130%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000" flood-opacity=".55"/></filter>
<filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter>`;
function paperBg(t) {   // editorial cream board with faint grid
  let s = `<rect x="-300" y="-300" width="1700" height="2600" fill="${PAPER2}"/>`;
  for (let i = 0; i < 30; i++) s += `<line x1="-300" y1="${i * 80}" x2="1400" y2="${i * 80}" stroke="#D9CCB4" stroke-width="2" opacity=".5"/>`;
  return s;
}

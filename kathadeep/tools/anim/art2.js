// Katha Deep character library v2 — smooth silhouettes, two-tone shading, ornaments. Feet at (0,0).
const ART_DEFS = `
<linearGradient id="kBlue" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4E7EE6"/><stop offset=".6" stop-color="#5A8CF0"/><stop offset="1" stop-color="#3F68CC"/></linearGradient>
<linearGradient id="kBlueV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5C8EF2"/><stop offset="1" stop-color="#3E66C8"/></linearGradient>
<linearGradient id="pitam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD24A"/><stop offset="1" stop-color="#F2A81E"/></linearGradient>
<linearGradient id="goldG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE7A0"/><stop offset=".5" stop-color="#F5C04A"/><stop offset="1" stop-color="#C98A1E"/></linearGradient>
<linearGradient id="cowG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFDF7"/><stop offset=".7" stop-color="#F3ECDF"/><stop offset="1" stop-color="#DCCFBC"/></linearGradient>
<linearGradient id="cowBrown" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D59A68"/><stop offset="1" stop-color="#A86A40"/></linearGradient>
<linearGradient id="skinG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#EDB38A"/><stop offset="1" stop-color="#D4916A"/></linearGradient>
<linearGradient id="skinGold" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F7CB8E"/><stop offset="1" stop-color="#E3A866"/></linearGradient>
<linearGradient id="redRobe" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C8352C"/><stop offset="1" stop-color="#8E1F1E"/></linearGradient>
<linearGradient id="creamG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF8EA"/><stop offset="1" stop-color="#EADFC8"/></linearGradient>
<radialGradient id="cheek"><stop offset="0" stop-color="#FF7FA0" stop-opacity=".55"/><stop offset="1" stop-color="#FF7FA0" stop-opacity="0"/></radialGradient>
<linearGradient id="mtnG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5DA868"/><stop offset="1" stop-color="#2F6E46"/></linearGradient>
<linearGradient id="mtnB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3E8452"/><stop offset="1" stop-color="#22543A"/></linearGradient>
`;
const P2 = (n) => (Math.round(n * 10) / 10);
const R2 = (a, x = 0, y = 0) => `rotate(${P2(a)} ${P2(x)} ${P2(y)})`;
const G2 = (x, y, s, inner, flip) => `<g transform="translate(${P2(x)} ${P2(y)}) scale(${flip ? -P2(s) : P2(s)} ${P2(s)})">${inner}</g>`;

function closedEye(x, y, w = 15, col = '#2A1B3D', lash = true) {
  return `<path d="M${x - w} ${y - 2} Q${x} ${y + w * 0.62} ${x + w} ${y - 2}" stroke="${col}" stroke-width="4.5" fill="none" stroke-linecap="round"/>` +
    (lash ? `<path d="M${x - w} ${y - 2} l-7 -5 M${x - w + 3} ${y + 2} l-7 1" stroke="${col}" stroke-width="3" stroke-linecap="round"/>` : '');
}
function openEye(x, y, w = 13, col = '#2A1B3D') {
  return `<path d="M${x - w} ${y} Q${x} ${y - w * 0.95} ${x + w} ${y} Q${x} ${y + w * 0.7} ${x - w} ${y}Z" fill="#FFFDF8"/>
    <circle cx="${x + 1}" cy="${y}" r="${w * 0.55}" fill="${col}"/><circle cx="${x + 3}" cy="${y - 3}" r="${w * 0.18}" fill="#fff"/>
    <path d="M${x - w - 2} ${y + 1} Q${x} ${y - w * 1.1} ${x + w + 4} ${y - 2}" stroke="${col}" stroke-width="4" fill="none" stroke-linecap="round"/>`;
}
// tapered limb with a joint; ang1 = upper segment angle (0 = down), ang2 = lower relative
function limb(x, y, ang1, ang2, l1, l2, w1, w2, fill, hand, extras = {}) {
  const lower = `<g transform="translate(0 ${l1}) ${R2(ang2)}">
      <path d="M${-w1 * 0.42} -4 C${-w1 * 0.42} ${l2 * 0.4} ${-w2 * 0.5} ${l2 * 0.8} ${-w2 * 0.5} ${l2} L${w2 * 0.5} ${l2} C${w2 * 0.5} ${l2 * 0.8} ${w1 * 0.42} ${l2 * 0.4} ${w1 * 0.42} -4Z" fill="${fill}"/>
      ${extras.bangle ? `<rect x="${-w2 * 0.62}" y="${l2 - 18}" width="${w2 * 1.24}" height="8" rx="4" fill="#F5C04A"/><rect x="${-w2 * 0.6}" y="${l2 - 8}" width="${w2 * 1.2}" height="6" rx="3" fill="#D8432F"/>` : ''}
      <g transform="translate(0 ${l2})">${hand}${extras.held || ''}</g></g>`;
  return `<g transform="translate(${P2(x)} ${P2(y)}) ${R2(ang1)}">
    <path d="M${-w1 * 0.5} 0 C${-w1 * 0.55} ${l1 * 0.5} ${-w1 * 0.45} ${l1} ${-w1 * 0.42} ${l1 + 6} L${w1 * 0.42} ${l1 + 6} C${w1 * 0.45} ${l1} ${w1 * 0.55} ${l1 * 0.5} ${w1 * 0.5} 0Z" fill="${fill}"/>
    ${extras.armlet ? `<path d="M${-w1 * 0.55} ${l1 * 0.3} Q0 ${l1 * 0.3 + 10} ${w1 * 0.55} ${l1 * 0.3}" stroke="#F5C04A" stroke-width="7" fill="none"/>` : ''}
    ${lower}<circle cx="0" cy="${l1}" r="${w1 * 0.44}" fill="${fill}"/></g>`;
}
const handShape = (fill, s = 1) => `<g transform="scale(${s})"><path d="M-14 -4 C-18 10 -14 26 0 28 C14 26 18 10 14 -4Z" fill="${fill}"/><path d="M12 2 C22 4 24 12 16 16" stroke="${fill}" stroke-width="9" fill="none" stroke-linecap="round"/></g>`;
const fingerUp = (fill) => `<path d="M-14 -4 C-18 10 -14 26 0 28 C14 26 18 10 14 -4Z" fill="${fill}"/><rect x="-6" y="18" width="12" height="40" rx="6" fill="${fill}"/>`;

function feather(x, y, a, s = 1) {
  return `<g transform="translate(${x} ${y}) rotate(${a}) scale(${s})">
    <path d="M0 0 C 6 -50 10 -100 2 -150" stroke="#5B3B16" stroke-width="3.5" fill="none"/>
    <path d="M2 -40 C-30 -80 -26 -150 2 -186 C30 -150 34 -80 2 -40Z" fill="#2F9E6E"/>
    <path d="M2 -60 C-16 -90 -14 -140 2 -168 C18 -140 20 -90 2 -60Z" fill="#43B97F"/>
    <ellipse cx="2" cy="-150" rx="24" ry="30" fill="#E6B635"/><ellipse cx="2" cy="-148" rx="17" ry="22" fill="#1E9A8A"/>
    <ellipse cx="2" cy="-146" rx="11" ry="15" fill="#1C4FB0"/><ellipse cx="3" cy="-144" rx="5" ry="7" fill="#0C1640"/></g>`;
}
function flowerGarland(x0, y0, x1, y1, sag, n, t = 0) {
  let s = `<path d="M${x0} ${y0} Q${(x0 + x1) / 2} ${y0 + sag} ${x1} ${y1}" stroke="#2E8A4E" stroke-width="7" fill="none"/>`;
  for (let i = 0; i <= n; i++) {
    const k = i / n, x = (1 - k) * (1 - k) * x0 + 2 * k * (1 - k) * (x0 + x1) / 2 + k * k * x1, y = (1 - k) * (1 - k) * y0 + 2 * k * (1 - k) * (y0 + sag) + k * k * y1;
    const c = ['#F5F1E6', '#E0483A', '#F5C04A', '#F28C28'][i % 4];
    s += `<g transform="translate(${P2(x)} ${P2(y)})">${[0, 72, 144, 216, 288].map((a) => `<ellipse cx="0" cy="-6" rx="4.5" ry="7" fill="${c}" transform="rotate(${a})"/>`).join('')}<circle r="3.5" fill="#F5C04A"/></g>`;
  }
  return s;
}

// ------------------------------------------------------------------ KRISHNA (child)
function krishna2(o = {}) {
  const t = o.t || 0, sway = Math.sin(t * 2.2) * 3;
  const aL = o.armL ?? 14, aR = o.armR ?? -14, eL = o.elbowL ?? 10, eR = o.elbowR ?? -10;
  const B = 'url(#kBlue)', BV = 'url(#kBlueV)';
  let s = '';
  if (o.glow) s += `<circle cx="0" cy="-330" r="340" fill="url(#halo)" opacity="${o.glow}"/>`;
  // back: flowing uttariya
  s += `<path d="M-60 -400 C-120 -330 -140 -230 ${-150 + sway} -150 C-120 -170 -100 -260 -54 -330Z" fill="#E0573A"/>`;
  // legs
  s += `<path d="M-46 -190 C-48 -110 -40 -50 -36 -14 L-12 -14 C-10 -60 -12 -130 -10 -190Z" fill="${BV}"/>
        <path d="M46 -190 C48 -110 40 -50 36 -14 L12 -14 C10 -60 12 -130 10 -190Z" fill="${BV}"/>
        <path d="M-40 -14 C-56 -12 -60 2 -44 4 L-6 4 C-4 -6 -8 -14 -14 -14Z" fill="#3E66C8"/><path d="M40 -14 C56 -12 60 2 44 4 L6 4 C4 -6 8 -14 14 -14Z" fill="#3E66C8"/>
        <path d="M-42 -34 L-10 -34" stroke="#F5C04A" stroke-width="7" stroke-linecap="round"/><path d="M42 -34 L10 -34" stroke="#F5C04A" stroke-width="7" stroke-linecap="round"/>
        <circle cx="-30" cy="-26" r="3" fill="#F5C04A"/><circle cx="-20" cy="-26" r="3" fill="#F5C04A"/><circle cx="30" cy="-26" r="3" fill="#F5C04A"/><circle cx="20" cy="-26" r="3" fill="#F5C04A"/>`;
  // pitambar dhoti with pleats
  s += `<path d="M-72 -300 C-80 -250 -92 -200 -84 -150 Q-42 -134 0 -146 Q42 -134 84 -150 C92 -200 80 -250 72 -300Z" fill="url(#pitam)"/>
        <path d="M-12 -292 C-18 -240 -24 -190 -22 -142 L22 -142 C24 -190 18 -240 12 -292Z" fill="#F0B42A"/>
        <path d="M-6 -280 L-10 -146 M6 -280 L10 -146" stroke="#E39A18" stroke-width="3"/>
        <path d="M-60 -250 Q-66 -200 -70 -160 M60 -250 Q66 -200 70 -160" stroke="#E7A320" stroke-width="3" fill="none"/>
        <path d="M-84 -150 Q-42 -134 0 -146 Q42 -134 84 -150" stroke="#C98A1E" stroke-width="5" fill="none"/>`;
  // kamarbandh (red sash) with falling end
  s += `<path d="M-74 -306 Q0 -286 74 -306 L74 -280 Q0 -262 -74 -280Z" fill="#D8432F"/><path d="M-74 -296 Q0 -276 74 -296" stroke="#F5C04A" stroke-width="3" fill="none"/>
        <path d="M40 -290 C44 -250 ${50 + sway} -220 ${44 + sway} -190 L${30 + sway} -194 C34 -224 30 -250 26 -284Z" fill="#C2352A"/>`;
  // torso
  s += `<path d="M-60 -404 C-76 -398 -80 -370 -74 -330 C-72 -316 -72 -304 -70 -296 L70 -296 C72 -304 72 -316 74 -330 C80 -370 76 -398 60 -404 Q0 -416 -60 -404Z" fill="${B}"/>
        <path d="M-30 -340 Q-20 -332 -8 -340 M8 -340 Q20 -332 30 -340" stroke="#3A60BE" stroke-width="3" fill="none" opacity=".6"/>`;
  // uttariya across the chest
  s += `<path d="M-62 -402 C-30 -380 20 -330 60 -300 L68 -318 C30 -346 -10 -390 -44 -410Z" fill="#E86A3E"/><path d="M-50 -404 C-20 -382 24 -338 62 -310" stroke="#F5C04A" stroke-width="3" fill="none"/>`;
  // necklaces + vaijayanti garland down to the knees
  s += `<path d="M-34 -404 Q0 -372 34 -404" stroke="url(#goldG)" stroke-width="8" fill="none"/><circle cx="0" cy="-382" r="7" fill="#D8432F" stroke="#F5C04A" stroke-width="3"/>`;
  s += flowerGarland(-52, -400, 52, -400, 360, 16);
  // arms
  const arm = (side, a, e) => limb(side * 66, -392, a, e, 92, 82, 34, 26, B, o.liftHand && side < 0 ? fingerUp('#4E7EE6') : handShape('#4E7EE6'), { bangle: true, armlet: true, held: side > 0 && o.flute ? `<g transform="rotate(${-(a + e)})"><rect x="-30" y="-8" width="190" height="14" rx="7" fill="#8C3B2E"/><rect x="-30" y="-8" width="20" height="14" rx="5" fill="#F5C04A"/><circle cx="40" cy="-1" r="3" fill="#3A1A10"/><circle cx="70" cy="-1" r="3" fill="#3A1A10"/><circle cx="100" cy="-1" r="3" fill="#3A1A10"/></g>` : '' });
  s += (o.liftHand ? '' : arm(-1, aL, eL)) + arm(1, aR, eR);
  // neck + head
  s += `<g transform="${R2(o.tilt || 0, 0, -420)}">`;
  s += `<path d="M-16 -432 L-16 -404 Q0 -396 16 -404 L16 -432Z" fill="#3E66C8"/>`;
  // back hair curls
  s += `<path d="M-86 -480 C-104 -420 -96 -380 -70 -372 C-80 -400 -74 -430 -60 -450Z" fill="#1F1A3A"/><path d="M86 -480 C104 -420 96 -380 70 -372 C80 -400 74 -430 60 -450Z" fill="#1F1A3A"/>`;
  s += `<path d="M-80 -500 C-82 -450 -60 -414 0 -412 C60 -414 82 -450 80 -500 C80 -556 44 -584 0 -584 C-44 -584 -80 -556 -80 -500Z" fill="${B}"/>`;
  // front hair fringe
  s += `<path d="M-82 -506 C-84 -570 -40 -600 0 -598 C40 -600 84 -570 82 -506 C70 -536 56 -548 36 -552 C24 -534 6 -540 0 -554 C-6 -540 -24 -534 -36 -552 C-56 -548 -70 -536 -82 -506Z" fill="#1F1A3A"/>`;
  // crown (mukut)
  s += `<path d="M-74 -566 L74 -566 L66 -612 L44 -596 L30 -640 L12 -606 L0 -656 L-12 -606 L-30 -640 L-44 -596 L-66 -612Z" fill="url(#goldG)"/>
        <rect x="-78" y="-576" width="156" height="20" rx="8" fill="#D9A02A"/><path d="M-70 -566 L70 -566" stroke="#FFF0B8" stroke-width="2"/>
        <circle cx="0" cy="-566" r="9" fill="#D8432F" stroke="#FFF0B8" stroke-width="2"/><circle cx="-40" cy="-566" r="6" fill="#2E9E5B"/><circle cx="40" cy="-566" r="6" fill="#2E9E5B"/>
        <circle cx="0" cy="-620" r="6" fill="#D8432F"/><circle cx="-30" cy="-612" r="4" fill="#2E9E5B"/><circle cx="30" cy="-612" r="4" fill="#2E9E5B"/>`;
  if (!o.noFeather) s += feather(30, -616, 16 + sway * 0.5, 0.9);
  // makara kundal
  s += `<path d="M-84 -486 c-10 6 -12 22 0 30 c12 -2 14 -18 4 -26z" fill="url(#goldG)"/><path d="M84 -486 c10 6 12 22 0 30 c-12 -2 -14 -18 -4 -26z" fill="url(#goldG)"/>`;
  // face
  s += `<ellipse cx="-42" cy="-472" rx="22" ry="14" fill="url(#cheek)"/><ellipse cx="42" cy="-472" rx="22" ry="14" fill="url(#cheek)"/>`;
  s += o.eyes === 'open' ? openEye(-30, -500) + openEye(30, -500) : closedEye(-30, -500) + `<g transform="scale(-1 1)">${closedEye(-30, -500)}</g>`;
  s += `<path d="M-46 -526 Q-30 -534 -14 -526 M14 -526 Q30 -534 46 -526" stroke="#1F1A3A" stroke-width="3.5" fill="none" stroke-linecap="round"/>`;
  s += `<path d="M-2 -486 Q2 -478 -3 -472" stroke="#3A60BE" stroke-width="3" fill="none" stroke-linecap="round"/>`;
  s += `<path d="M-8 -546 L-5 -520 M8 -546 L5 -520" stroke="#FFF6E0" stroke-width="4.5" stroke-linecap="round"/><path d="M0 -544 L0 -524" stroke="#D8432F" stroke-width="4.5" stroke-linecap="round"/>`;
  s += o.mouth === 'open' ? `<path d="M-12 -458 Q0 -444 12 -458 Q0 -452 -12 -458Z" fill="#8A2A3A" stroke="#8A2A3A" stroke-width="3" stroke-linejoin="round"/>`
                          : `<path d="M-14 -458 Q0 -446 14 -458" stroke="#8A2A3A" stroke-width="4.5" fill="none" stroke-linecap="round"/>`;
  s += `</g>`;
  if (o.liftHand) s += limb(-70, -392, aL, eL, 112, 104, 36, 28, B, fingerUp('#4E7EE6'), { bangle: true, armlet: true });
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}

// ------------------------------------------------------------------ COW (Indian, Gir-like). Faces left.
function cow2(o = {}) {
  const ph = o.ph || 0, t = o.t || 0;
  const swing = (k) => Math.sin(ph + k) * 14;
  const body = 'url(#cowG)';
  let s = '';
  if (o.halo) s += `<circle cx="-40" cy="-200" r="260" fill="url(#halo)" opacity="${o.halo}"/>`;
  const leg = (x, k, far) => `<g transform="${R2(swing(k), x, -150)}"><path d="M${x - 16} -160 C${x - 18} -110 ${x - 12} -70 ${x - 10} -18 L${x + 8} -18 C${x + 8} -70 ${x + 12} -110 ${x + 14} -160Z" fill="${far ? '#E2D6C2' : body}"/>
     <ellipse cx="${x - 1}" cy="-62" rx="10" ry="8" fill="${far ? '#D6C8B2' : '#EDE3D2'}"/><path d="M${x - 12} -20 L${x + 10} -20 L${x + 12} 0 L${x - 14} 0Z" fill="#4A3426"/></g>`;
  s += leg(-60, Math.PI, true) + leg(118, 0, true);
  // tail
  s += `<path d="M168 -230 C190 -200 ${196 + Math.sin(t * 3) * 8} -150 ${188 + Math.sin(t * 3) * 10} -96" stroke="#E8DCC8" stroke-width="7" fill="none" stroke-linecap="round"/>
        <path d="M${188 + Math.sin(t * 3) * 10} -110 c-12 10 -10 34 0 40 c10 -6 12 -30 0 -40z" fill="#3A2A20"/>`;
  // body with hump + dewlap
  s += `<path d="M-120 -250 C-110 -300 -70 -318 -40 -296 C-10 -276 40 -270 100 -268 C150 -266 178 -250 180 -210 C182 -170 170 -140 140 -128 C90 -112 0 -112 -60 -124
            C-90 -130 -110 -140 -120 -150 C-132 -170 -150 -200 -150 -224 Z" fill="${body}"/>`;
  s += `<path d="M-74 -306 C-60 -330 -30 -326 -30 -300 C-46 -296 -62 -296 -74 -306Z" fill="#F7F1E6"/>`; // hump
  s += `<path d="M-150 -200 C-150 -150 -132 -118 -104 -116 C-112 -140 -118 -170 -118 -196Z" fill="#EFE6D6"/>`; // dewlap
  if (o.patch !== false) s += `<path d="M30 -268 C70 -272 120 -262 140 -232 C130 -206 90 -200 60 -214 C40 -226 26 -246 30 -268Z" fill="url(#cowBrown)" opacity=".9"/>`;
  s += `<path d="M-60 -126 C0 -116 90 -116 140 -130" stroke="#D9CBB4" stroke-width="5" fill="none" opacity=".7"/>`;
  if (o.cloth) s += `<path d="M-40 -290 C0 -276 60 -272 110 -270 L118 -190 C70 -170 0 -172 -40 -186Z" fill="#C2352A"/><path d="M-40 -186 C0 -172 70 -170 118 -190" stroke="#F5C04A" stroke-width="10" fill="none"/>
        ${[0, 1, 2].map((i) => `<circle cx="${-6 + i * 44}" cy="${-232 + (i % 2) * 8}" r="9" fill="#F5C04A"/><circle cx="${-6 + i * 44}" cy="${-232 + (i % 2) * 8}" r="4" fill="#E9F3FF"/>`).join('')}
        <path d="M-40 -186 l8 18 l8 -16 l8 18 l8 -16 l8 18 l8 -16 l8 18 l8 -16 l8 18 l8 -16 l8 18 l8 -16 l8 18 l8 -16 l8 18 l8 -14 l8 16 l8 -18" stroke="#F5C04A" stroke-width="4" fill="none"/>`;
  s += leg(-90, 0, false) + leg(146, Math.PI, false);
  // neck + head (angled down, long face)
  s += `<path d="M-118 -246 C-140 -270 -170 -276 -196 -262 L-178 -196 C-160 -196 -140 -200 -126 -210Z" fill="${body}"/>`;
  s += `<g transform="${R2(o.headTilt || 0, -180, -250)}">`;
  s += `<path d="M-226 -270 C-214 -296 -170 -298 -160 -268 C-154 -240 -170 -200 -192 -176 C-204 -164 -228 -166 -238 -182 C-248 -204 -238 -248 -226 -270Z" fill="${body}"/>`;
  s += `<path d="M-240 -196 C-244 -174 -228 -160 -210 -164 C-196 -168 -190 -182 -196 -194 C-210 -190 -228 -190 -240 -196Z" fill="#E8B9A6"/><ellipse cx="-226" cy="-182" rx="4" ry="3" fill="#6E4636"/><ellipse cx="-208" cy="-184" rx="4" ry="3" fill="#6E4636"/>`;
  // Gir drooping ear
  s += `<path d="M-166 -262 C-140 -258 -120 -236 -118 -206 C-130 -204 -150 -220 -164 -244Z" fill="#EDE3D2"/><path d="M-160 -252 C-142 -246 -130 -232 -126 -214" stroke="#E2B6A2" stroke-width="5" fill="none"/>`;
  // horns, painted
  s += `<path d="M-216 -286 C-232 -306 -230 -330 -210 -344 C-214 -326 -208 -306 -200 -292Z" fill="#E6D3B0"/><path d="M-222 -318 l10 -4 M-224 -306 l10 -4" stroke="#D8432F" stroke-width="4"/>
        <path d="M-180 -290 C-170 -312 -150 -324 -126 -320 C-144 -312 -156 -300 -166 -284Z" fill="#E6D3B0"/><path d="M-156 -312 l2 10 M-144 -316 l2 10" stroke="#2E7FB8" stroke-width="4"/>
        <circle cx="-210" cy="-346" r="5" fill="#F5C04A"/><circle cx="-124" cy="-320" r="5" fill="#F5C04A"/>`;
  s += `<path d="M-200 -276 C-206 -262 -204 -248 -198 -240" stroke="#D8432F" stroke-width="5" fill="none" stroke-linecap="round"/>`; // tilak
  s += `<path d="M-224 -236 Q-214 -228 -204 -236" stroke="#2A1B3D" stroke-width="3.5" fill="none" stroke-linecap="round"/><path d="M-204 -236 l6 -4" stroke="#2A1B3D" stroke-width="2.5" stroke-linecap="round"/>`;
  if (o.crown) s += `<path d="M-222 -286 L-168 -286 L-172 -314 L-184 -304 L-195 -326 L-206 -304 L-218 -314Z" fill="url(#goldG)"/><circle cx="-195" cy="-292" r="4" fill="#D8432F"/>`;
  s += `</g>`;
  // neck rope + bell
  s += `<path d="M-176 -214 C-160 -190 -134 -184 -120 -196" stroke="#D8432F" stroke-width="7" fill="none"/>${[0, 1, 2, 3].map((i) => `<circle cx="${-170 + i * 14}" cy="${-200 + Math.sin(i) * 6}" r="3" fill="#F5C04A"/>`).join('')}
        <g transform="${R2(Math.sin(t * 4 + ph) * 10, -150, -192)}"><path d="M-160 -192 L-140 -192 L-136 -166 L-164 -166Z" fill="url(#goldG)"/><circle cx="-150" cy="-162" r="4" fill="#9A6A1E"/></g>`;
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}

// ------------------------------------------------------------------ NAND BABA
function nand2(o = {}) {
  const S = 'url(#skinG)';
  let s = '';
  s += `<path d="M-44 -150 L-40 -12 L-14 -12 L-12 -150Z M44 -150 L40 -12 L14 -12 L12 -150Z" fill="#C98660"/><path d="M-46 -12 l40 0 l2 12 l-48 0z M46 -12 l-40 0 l-2 12 l48 0z" fill="#7A4A2A"/>`;
  s += `<path d="M-86 -440 C-100 -360 -106 -250 -96 -140 Q0 -120 96 -140 C106 -250 100 -360 86 -440Z" fill="url(#creamG)"/>`;
  s += `<path d="M-96 -150 Q0 -128 96 -150 L96 -136 Q0 -114 -96 -136Z" fill="#E86A3E"/><path d="M-20 -430 L-26 -150 M20 -430 L26 -150" stroke="#E2D6BE" stroke-width="3"/>`;
  s += `<path d="M-84 -446 C-40 -400 30 -330 80 -280 L92 -310 C40 -360 -20 -420 -60 -456Z" fill="#E86A3E"/>`;
  const armR = limb(84, -436, o.armR ?? -10, o.elbowR ?? -6, 120, 110, 40, 32, '#F4ECDC', handShape('#E3A27C', 1.2), { held: o.held !== undefined ? o.held : o.staff ? `<rect x="-8" y="-280" width="16" height="560" rx="8" fill="#7A4A22"/><circle cx="0" cy="-286" r="12" fill="#9A6A34"/>` : '' });
  const armL = limb(-84, -436, o.armL ?? 10, o.elbowL ?? 6, 120, 110, 40, 32, '#F4ECDC', handShape('#E3A27C', 1.2));
  s += armL + armR;
  s += `<path d="M-20 -480 L-20 -440 L20 -440 L20 -480Z" fill="#C98660"/>`;
  s += `<path d="M-70 -540 C-72 -480 -40 -456 0 -456 C40 -456 72 -480 70 -540 C70 -590 40 -614 0 -614 C-40 -614 -70 -590 -70 -540Z" fill="${S}"/>`;
  s += `<path d="M-72 -540 C-80 -470 -50 -406 0 -398 C50 -406 80 -470 72 -540 C60 -508 40 -496 0 -498 C-40 -496 -60 -508 -72 -540Z" fill="#F7F4EE"/>`;
  s += `<path d="M-44 -508 C-30 -490 -10 -498 0 -506 C10 -498 30 -490 44 -508 C30 -500 12 -510 0 -516 C-12 -510 -30 -500 -44 -508Z" fill="#E6E1D6"/>`;
  s += `<path d="M-8 -530 Q0 -520 8 -530" stroke="#B9744E" stroke-width="3" fill="none"/>`;
  s += o.eyes === 'open' ? openEye(-26, -556, 12) + openEye(26, -556, 12) : closedEye(-26, -556, 13) + `<g transform="scale(-1 1)">${closedEye(-26, -556, 13)}</g>`;
  s += `<path d="M-42 -580 Q-26 -590 -10 -580 M10 -580 Q26 -590 42 -580" stroke="#F7F4EE" stroke-width="6" fill="none" stroke-linecap="round"/>`;
  s += `<path d="M-80 -580 C-90 -660 -40 -690 0 -690 C50 -690 92 -656 80 -580 C50 -604 -40 -606 -80 -580Z" fill="#F08A2C"/>
        <path d="M-80 -584 C-30 -620 40 -616 80 -584 M-70 -620 C-20 -650 40 -646 74 -616 M-50 -656 C-10 -676 30 -674 56 -652" stroke="#C9631A" stroke-width="5" fill="none"/>
        <circle cx="0" cy="-640" r="11" fill="url(#goldG)"/><path d="M0 -650 c-4 -20 6 -32 14 -40" stroke="#F5C04A" stroke-width="4" fill="none"/>`;
  s += `<path d="M-10 -596 L10 -596" stroke="#D8432F" stroke-width="5" stroke-linecap="round"/>`;
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}

// ------------------------------------------------------------------ INDRA
function indra2(o = {}) {
  const angry = o.mood === 'angry', S = angry ? '#E9946A' : 'url(#skinGold)', hand = angry ? '#E9946A' : '#F2BC7A';
  let s = '';
  if (o.aura) s += `<circle cx="0" cy="-480" r="360" fill="url(#${angry ? 'rage' : 'halo'})" opacity="${o.aura}"/>`;
  s += `<path d="M-96 -390 C-110 -260 -126 -120 -130 0 L130 0 C126 -120 110 -260 96 -390Z" fill="url(#redRobe)"/>
        <path d="M-130 -20 L130 -20 L132 0 L-132 0Z" fill="url(#goldG)"/><path d="M-14 -390 L-22 0 L22 0 L14 -390Z" fill="url(#goldG)"/>
        <path d="M-110 -200 Q0 -180 110 -200" stroke="#F5C04A" stroke-width="5" fill="none" opacity=".7"/>`;
  s += `<path d="M-90 -530 C-104 -480 -100 -420 -96 -380 L96 -380 C100 -420 104 -480 90 -530 Q0 -550 -90 -530Z" fill="${S}"/>`;
  s += `<path d="M-100 -396 Q0 -370 100 -396 L100 -372 Q0 -346 -100 -372Z" fill="url(#goldG)"/>`;
  s += `<path d="M-86 -530 C-40 -480 30 -430 90 -400" stroke="#F5C04A" stroke-width="12" fill="none"/>`;
  s += `<path d="M-60 -530 Q0 -470 60 -530" stroke="url(#goldG)" stroke-width="14" fill="none"/><path d="M-40 -520 Q0 -488 40 -520" stroke="#D8432F" stroke-width="5" fill="none"/>`;
  if (o.folded) {
    s += limb(-88, -520, 40, -110, 110, 96, 42, 32, S, '') + limb(88, -520, -40, 110, 110, 96, 42, 32, S, '');
    s += `<path d="M-16 -420 C-18 -460 -6 -488 0 -496 C6 -488 18 -460 16 -420Z" fill="${hand}"/>`;
  } else {
    const vj = o.held !== undefined ? o.held : `<g transform="rotate(${-(o.armR ?? -130) - (o.elbowR ?? -20)})"><rect x="-8" y="-70" width="16" height="140" rx="6" fill="url(#goldG)"/>
      <path d="M-30 -70 L-14 -120 L0 -96 L14 -120 L30 -70Z" fill="url(#goldG)"/><path d="M-30 70 L-14 120 L0 96 L14 120 L30 70Z" fill="url(#goldG)"/><circle r="18" fill="#C98A1E"/><circle r="8" fill="#FFE7A0"/></g>`;
    s += limb(-88, -520, o.armL ?? 16, o.elbowL ?? 10, 120, 104, 42, 32, S, handShape(hand, 1.2), { bangle: true, armlet: true });
    s += limb(88, -520, o.armR ?? -130, o.elbowR ?? -20, 120, 104, 42, 32, S, handShape(hand, 1.2), { bangle: true, armlet: true, held: vj });
  }
  s += `<path d="M-22 -570 L-22 -528 L22 -528 L22 -570Z" fill="${hand}"/>`;
  s += `<path d="M-74 -620 C-76 -560 -44 -540 0 -540 C44 -540 76 -560 74 -620 C74 -672 44 -700 0 -700 C-44 -700 -74 -672 -74 -620Z" fill="${S}"/>`;
  s += `<path d="M-76 -640 C-92 -600 -84 -560 -64 -548 C-70 -580 -70 -610 -62 -630Z M76 -640 C92 -600 84 -560 64 -548 C70 -580 70 -610 62 -630Z" fill="#1F1A3A"/>`;
  s += `<path d="M-80 -604 c-10 6 -10 26 2 30 c10 -4 10 -24 -2 -30z M80 -604 c10 6 10 26 -2 30 c-10 -4 -10 -24 2 -30z" fill="url(#goldG)"/>`;
  s += `<g transform="${R2(o.crownTilt || 0, 0, -680)}"><path d="M-78 -676 L78 -676 L50 -860 L0 -920 L-50 -860Z" fill="url(#goldG)"/>
        <path d="M-78 -676 L78 -676 L74 -706 L-74 -706Z" fill="#C98A1E"/><path d="M-62 -760 L62 -760 M-52 -820 L52 -820" stroke="#C98A1E" stroke-width="7"/>
        <circle cx="0" cy="-732" r="16" fill="#D8432F" stroke="#FFE7A0" stroke-width="3"/><circle cx="-34" cy="-726" r="8" fill="#2E9E5B"/><circle cx="34" cy="-726" r="8" fill="#2E9E5B"/>
        <circle cx="0" cy="-790" r="10" fill="#2E7FB8"/><circle cx="0" cy="-926" r="11" fill="#FFE7A0"/>
        ${o.cracked ? `<path d="M-6 -900 L10 -846 L-12 -806 L12 -760 L-4 -720" stroke="#3A2210" stroke-width="6" fill="none" stroke-linejoin="round"/>` : ''}</g>`;
  if (angry) {
    s += `<path d="M-50 -650 L-14 -632 M50 -650 L14 -632" stroke="#2A1B3D" stroke-width="7" stroke-linecap="round"/>` + openEye(-28, -616, 12, '#2A1B3D').replace('#FFFDF8', '#FFE9D6') + openEye(28, -616, 12, '#2A1B3D').replace('#FFFDF8', '#FFE9D6');
    s += `<path d="M-18 -568 Q0 -582 18 -568" stroke="#5C1A1A" stroke-width="6" fill="none" stroke-linecap="round"/>`;
  } else {
    s += (o.eyes === 'open' ? openEye(-28, -616, 12) + openEye(28, -616, 12) : closedEye(-28, -616, 13) + `<g transform="scale(-1 1)">${closedEye(-28, -616, 13)}</g>`);
    s += `<path d="M-44 -640 Q-28 -650 -12 -640 M12 -640 Q28 -650 44 -640" stroke="#1F1A3A" stroke-width="4" fill="none" stroke-linecap="round"/>`;
    s += `<path d="M-14 -570 Q0 -560 14 -570" stroke="#8A2A3A" stroke-width="4.5" fill="none" stroke-linecap="round"/>`;
  }
  s += `<path d="M-24 -582 C-12 -592 0 -584 0 -584 C0 -584 12 -592 24 -582" stroke="#1F1A3A" stroke-width="5" fill="none" stroke-linecap="round"/>`;
  s += `<path d="M-8 -664 Q0 -648 8 -664" stroke="#D8432F" stroke-width="5" fill="none"/><ellipse cx="0" cy="-662" rx="5" ry="8" fill="#D8432F"/>`;
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}

// ------------------------------------------------------------------ GOPI / GWALA
function gopi2(o = {}) {
  const v = o.veil || '#C2405A', top = o.top || '#F2A03D', skirt = o.skirt || '#2F7FB8', S = '#E8A983';
  let s = '';
  s += `<path d="M-100 0 C-96 -100 -70 -200 -40 -260 L40 -260 C70 -200 96 -100 100 0 Q0 16 -100 0Z" fill="${skirt}"/>
        <path d="M-100 0 Q0 16 100 0 L98 -22 Q0 -6 -98 -22Z" fill="#F5C04A"/>${[-60, -20, 20, 60].map((x) => `<path d="M${x * 0.5} -250 Q${x} -120 ${x * 1.3} -8" stroke="#00000022" stroke-width="5" fill="none"/>`).join('')}`;
  s += `<path d="M-52 -360 C-60 -330 -56 -290 -46 -262 L46 -262 C56 -290 60 -330 52 -360 Q0 -372 -52 -360Z" fill="${top}"/>`;
  s += limb(-52, -352, o.armL ?? 20, o.elbowL ?? 20, 76, 70, 26, 20, top, handShape(S, 0.9), { bangle: true });
  s += limb(52, -352, o.armR ?? -20, o.elbowR ?? -20, 76, 70, 26, 20, top, handShape(S, 0.9), { bangle: true, held: o.pot ? `<g transform="rotate(${-(o.armR ?? -20) - (o.elbowR ?? -20)})"><ellipse cx="0" cy="-40" rx="46" ry="38" fill="#C46A35"/><rect x="-22" y="-86" width="44" height="16" rx="6" fill="#A2522A"/><path d="M-40 -40 Q0 -28 40 -40" stroke="#F5C04A" stroke-width="5" fill="none"/></g>` : (o.thali ? `<g transform="rotate(${-(o.armR ?? -20) - (o.elbowR ?? -20)})"><ellipse cx="0" cy="-6" rx="56" ry="12" fill="url(#goldG)"/>${flame(0, -12, 0.35, o.t || 0)}</g>` : '') });
  s += `<path d="M-14 -392 L-14 -360 L14 -360 L14 -392Z" fill="${S}"/>`;
  s += `<path d="M-52 -436 C-54 -390 -30 -378 0 -378 C30 -378 54 -390 52 -436 C52 -476 30 -494 0 -494 C-30 -494 -52 -476 -52 -436Z" fill="${S}"/>`;
  s += `<path d="M-54 -446 C-56 -490 -24 -502 0 -500 C24 -502 56 -490 54 -446 C40 -470 20 -474 0 -470 C-20 -474 -40 -470 -54 -446Z" fill="#1F1A3A"/>`;
  s += `<path d="M-64 -440 C-74 -510 -30 -528 0 -528 C30 -528 74 -510 64 -440 C76 -360 92 -300 110 -250 L76 -300 C64 -350 60 -420 52 -446 C36 -488 -36 -488 -52 -446 C-60 -420 -64 -350 -76 -300 L-110 -250 C-92 -300 -76 -360 -64 -440Z" fill="${v}"/>
        <path d="M-60 -470 C-30 -500 30 -500 60 -470" stroke="#F5C04A" stroke-width="5" fill="none"/>`;
  s += closedEye(-18, -436, 11) + `<g transform="scale(-1 1)">${closedEye(-18, -436, 11)}</g>`;
  s += `<ellipse cx="-30" cy="-414" rx="14" ry="9" fill="url(#cheek)"/><ellipse cx="30" cy="-414" rx="14" ry="9" fill="url(#cheek)"/><circle cx="0" cy="-466" r="5" fill="#D8432F"/>`;
  s += `<path d="M-10 -406 Q0 -398 10 -406" stroke="#8A2A3A" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="12" cy="-424" r="3" fill="#F5C04A"/>`;
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}
function gwala2(o = {}) {
  const S = o.skin || '#D9946C', top = o.top || '#E86A3E';
  let s = '';
  s += `<path d="M-36 -140 L-32 -10 L-12 -10 L-10 -140Z M36 -140 L32 -10 L12 -10 L10 -140Z" fill="${S}"/><path d="M-36 -10 h26 l2 10 h-30z M36 -10 h-26 l-2 10 h30z" fill="#6E4636"/>`;
  s += `<path d="M-58 -260 C-64 -210 -66 -170 -60 -124 Q0 -110 60 -124 C66 -170 64 -210 58 -260Z" fill="${o.dhoti || '#F3ECDD'}"/><path d="M-6 -256 L-10 -118 M6 -256 L10 -118" stroke="#DCD2BE" stroke-width="3"/>`;
  s += `<path d="M-52 -360 C-60 -320 -60 -290 -56 -258 L56 -258 C60 -290 60 -320 52 -360 Q0 -372 -52 -360Z" fill="${S}"/><path d="M-50 -360 L46 -262" stroke="${top}" stroke-width="18"/>`;
  s += limb(-52, -352, o.armL ?? 18, o.elbowL ?? 14, 78, 72, 26, 20, S, handShape(S, 0.9), { bangle: true });
  s += limb(52, -352, o.armR ?? -18, o.elbowR ?? -14, 78, 72, 26, 20, S, handShape(S, 0.9), { bangle: true, held: o.held !== undefined ? o.held : o.stick ? `<g transform="rotate(${-(o.armR ?? -18) - (o.elbowR ?? -14)})"><rect x="-6" y="-200" width="12" height="380" rx="6" fill="#7A4A22"/></g>` : '' });
  s += `<path d="M-14 -392 L-14 -358 L14 -358 L14 -392Z" fill="${S}"/>`;
  s += `<path d="M-50 -436 C-52 -392 -28 -380 0 -380 C28 -380 52 -392 50 -436 C50 -476 28 -494 0 -494 C-28 -494 -50 -476 -50 -436Z" fill="${S}"/>`;
  s += `<path d="M-54 -442 C-58 -500 -20 -510 0 -508 C20 -510 58 -500 54 -442 C44 -470 22 -474 0 -472 C-22 -474 -44 -470 -54 -442Z" fill="#1F1A3A"/>`;
  s += `<path d="M-56 -466 C-30 -490 30 -490 56 -466 L54 -448 C30 -472 -30 -472 -54 -448Z" fill="${top}"/><path d="M50 -460 c14 10 16 26 8 36" stroke="${top}" stroke-width="10" fill="none" stroke-linecap="round"/>`;
  s += closedEye(-18, -436, 11) + `<g transform="scale(-1 1)">${closedEye(-18, -436, 11)}</g>`;
  s += `<path d="M-10 -406 Q0 -398 10 -406" stroke="#7A2236" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M-4 -460 L4 -460" stroke="#D8432F" stroke-width="4" stroke-linecap="round"/>`;
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}

// ------------------------------------------------------------------ GOVARDHAN v2 (rounded hill, layered, rocks, trees)
function tree2(x, y, s, sway = 0, c1 = '#2F8A55', c2 = '#22693F', c3 = '#4FAE6E') {
  return G2(x, y, s, `<path d="M-10 0 C-8 -60 -12 -110 -6 -160 L6 -160 C12 -110 8 -60 10 0Z" fill="#6B4A2E"/>
    <g transform="${R2(sway, 0, -150)}"><circle cx="0" cy="-230" r="92" fill="${c2}"/><circle cx="-56" cy="-196" r="64" fill="${c1}"/><circle cx="54" cy="-204" r="70" fill="${c1}"/><circle cx="0" cy="-262" r="66" fill="${c1}"/>
    <circle cx="-22" cy="-284" r="26" fill="${c3}" opacity=".7"/><circle cx="40" cy="-232" r="18" fill="${c3}" opacity=".6"/></g>`);
}
function mountain2(o = {}) {
  const w = o.w || 900, h = o.h || 520, L = -w / 2, R = w / 2, t = o.t || 0;
  let s = '';
  if (o.lifted) s += `<path d="M${L + 30} -6 C${L + 120} 60 ${L + 240} 90 ${-60} 120 C${80} 140 ${R - 200} 100 ${R - 30} -6Z" fill="#7A5236"/>
      <path d="M${L + 120} 30 l30 56 l26 -44 M${-80} 80 l30 66 l32 -56 M${R - 230} 50 l24 50 l22 -40" fill="#5E3E28"/>
      <path d="M${L + 60} 10 C${L + 200} 50 ${R - 200} 50 ${R - 60} 10" stroke="#946646" stroke-width="10" fill="none"/>`;
  s += `<path d="M${L} 0 C${L + 40} ${-h * 0.4} ${L + w * 0.14} ${-h * 0.66} ${L + w * 0.27} ${-h * 0.74} C${L + w * 0.36} ${-h * 0.98} ${-w * 0.06} ${-h * 1.04} ${w * 0.02} ${-h * 0.98}
          C${w * 0.12} ${-h * 1.06} ${R - w * 0.26} ${-h * 0.92} ${R - w * 0.2} ${-h * 0.7} C${R - w * 0.1} ${-h * 0.6} ${R - 30} ${-h * 0.3} ${R} 0Z" fill="url(#mtnB)"/>`;
  s += `<path d="M${L + 50} 0 C${L + w * 0.16} ${-h * 0.5} ${-w * 0.18} ${-h * 0.72} ${-w * 0.02} ${-h * 0.7} C${w * 0.14} ${-h * 0.76} ${R - w * 0.2} ${-h * 0.5} ${R - 60} 0Z" fill="url(#mtnG)"/>`;
  s += `<path d="M${-w * 0.24} ${-h * 0.82} C${-w * 0.1} ${-h * 0.96} ${w * 0.04} ${-h * 0.98} ${w * 0.16} ${-h * 0.88}" stroke="#7CC27C" stroke-width="18" fill="none" stroke-linecap="round" opacity=".55"/>`;
  const trees = [[-0.34, -0.44, 0.4], [-0.2, -0.76, 0.44], [0.02, -0.9, 0.48], [0.2, -0.68, 0.42], [0.33, -0.4, 0.38], [-0.08, -0.46, 0.36], [0.12, -0.3, 0.34], [-0.26, -0.18, 0.32], [0.28, -0.14, 0.3]];
  for (const [tx, ty, ts] of trees) s += tree2(tx * w, ty * h + 40, ts, o.sway ? Math.sin(t * 2 + tx * 5) * 3 : 0);
  s += `<path d="M${-w * 0.36} -10 c10 -40 70 -50 90 -10z" fill="#9C9C94"/><path d="M${w * 0.24} -8 c8 -30 60 -36 72 -8z" fill="#A8A8A0"/>`;
  if (o.garland) s += flowerGarland(L + w * 0.16, -h * 0.5, R - w * 0.16, -h * 0.5, h * 0.36, 26);
  if (o.diyas) for (let i = 0; i < 7; i++) s += diya(L + w * 0.13 + i * w * 0.124, -4, 0.5, t, i);
  return G2(o.x || 0, o.y || 0, o.s || 1, s);
}

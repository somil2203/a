// Chitragupta — Yama's record-keeper (Chitragupta Puja on Yama Dvitiya). Story as commonly told in the Chitragupta katha:
// Yama asks Brahma for help keeping the account of countless beings; Brahma meditates; Chitragupta emerges from his body (kaya)
// with pen and inkpot; named Kayastha (born of the body) and Chitragupta (hidden within). The pen-and-inkpot puja is tradition.
const DARK = { dark: false }, LIGHT = { dark: true };
const TAG = () => tagTR('YAM DWITIYA · CHITRAGUPT');
const rays = (cx, cy, n, op, t, col = '#FFF2C6') => [...Array(n)].map((_, i) => { const a = (i * 360 / n + t * 5) * Math.PI / 180, b = a + 0.12;
  return `<path d="M${cx} ${cy} L${(cx + Math.cos(a) * 2600).toFixed(0)} ${(cy + Math.sin(a) * 2600).toFixed(0)} L${(cx + Math.cos(b) * 2600).toFixed(0)} ${(cy + Math.sin(b) * 2600).toFixed(0)}Z" fill="${col}" opacity="${op}"/>`; }).join('');
const yamaHall = (t) => { let w = bg('rage') + `<rect x="-300" y="1460" width="1700" height="900" fill="#2A0E10"/>`;
  for (let i = 0; i < 4; i++) w += `<rect x="${-20 + i * 300}" y="600" width="60" height="860" fill="#3A1418"/>`; return w; };
const writingPen = (t, x0, y0, w) => { const p = (t * 0.9) % 1; return quill(x0 + p * w, y0 - Math.abs(Math.sin(t * 14)) * 6, 0.8, 20); };

// 0 HOOK — every deed is being written... by whom?
add(0, at('आज सुबह'), (t) => {
  const lines = seg(t, 0, at('आज सुबह')) * 0.9 + 0.08;
  let w = `<rect x="-300" y="-300" width="1700" height="2600" fill="#0E0A14"/>` + stars(t, 40) + `<circle cx="540" cy="1150" r="560" fill="url(#halo)" opacity=".35"/>`;
  w += ledger(540, 1500, 1.15, t, lines, { ink: '#2A2A44' }) + writingPen(t, 160 + 400 * (Math.floor(lines * 28) >= 14 ? 1 : 0), 1500 - 1.15 * (420 - (Math.floor(lines * 28) % 14) * 31), 320);
  const c = camPath(t, [[0, 540, 1180, 1.35], [at('सवाल है'), 540, 1150, 1.1], [at('आज सुबह'), 540, 1150, 1.0]]);
  let s = cam(...c, w);
  s += caps(t, [{ t0: 0, l1: 'AAPKA HAR KARM', l2: 'LIKHA JA RAHA HAI', t2: 0.45, acc: GOLDT, ...DARK }, { t0: at('सवाल है'), l1: 'LIKHTA', l2: 'KAUN HAI?', acc: '#FF5A4A', ...DARK, size: 120 }]);
  return s + TAG();
});

// 1 THIS MORNING (Bhai Dooj) — but in Yamaloka, beside him: his scribe
add(at('आज सुबह'), at('कथा कहती'), (t) => {
  const inHall = t > at('पर यमलोक') - 0.15;
  let s = '';
  if (!inHall) {
    let w = paperBg(t) + paper(170, 640, 740, 820, -3, `<rect x="30" y="30" width="680" height="620" fill="#4A1F2A"/><g transform="translate(370 610) scale(.55)">${sisterHome(0, 0, 1, t, { open: true })}${yamraj({ x: -260, y: 0, s: 0.8, eyes: 'closed', armL: 30, armR: -30, pasha: false, held: '' })}</g><text x="370" y="740" text-anchor="middle" font-family="${ANTON}" font-size="54" fill="${INK}">BHAI DOOJ · AAJ SUBAH</text>`, { tape: true, seed: 2 });
    s += cam(540, 1060, lerp(1.0, 1.06, seg(t, at('आज सुबह'), at('पर यमलोक'))), w);
    s += caps(t, [{ t0: at('आज सुबह'), l1: 'AAJ SUBAH', l2: 'YAMRAJ BEHEN KE GHAR', t2: at('यमराज बहन'), acc: RED, ...LIGHT }]);
  } else {
    const reveal = eo(seg(t, at('चित्रगुप्त।') - 0.2, at('चित्रगुप्त।') + 0.5));
    let w = yamaHall(t) + yamraj({ x: 330, y: 1720, s: 0.95, eyes: 'open', armR: -120, elbowR: -20 });
    w += `<g opacity="${(0.35 + 0.65 * reveal).toFixed(2)}">${chitragupta({ x: 790, y: 1720, s: 0.85, eyes: 'closed', armR: -60, elbowR: -70, armL: 30 })}</g>`;
    if (reveal < 1) w += `<g opacity="${(0.6 * (1 - reveal)).toFixed(2)}"><rect x="600" y="900" width="380" height="900" fill="#14080A"/></g>`;
    w += ledger(780, 1760, 0.38, t, 0.6) + dawat(960, 1760, 0.6);
    s += cam(lerp(500, 680, eio(seg(t, at('पर यमलोक'), at('चित्रगुप्त।') + 0.3))), lerp(1290, 1250, seg(t, at('पर यमलोक'), at('कथा कहती'))), lerp(1.0, 1.2, eio(seg(t, at('पर यमलोक'), at('चित्रगुप्त।') + 0.5))) + 0.05 * seg(t, at('चित्रगुप्त।'), at('कथा कहती')), w);
    s += flashRect(t, at('चित्रगुप्त।'), 0.3, '#FFF2C8');
    s += caps(t, [{ t0: at('पर यमलोक'), l1: 'PAR YAMLOK MEIN', l2: 'UNKE LEKHAAKAAR', t2: at('उनके लेखाकार'), acc: GOLDT, ...DARK }, { t0: at('चित्रगुप्त।'), l1: 'CHITRAGUPT', acc: GOLDT, ...DARK, size: 130 }]);
  }
  return s + TAG();
}, 'zoom');

// 2 YAMA TO BRAHMA — countless beings: how do I keep the account alone?
add(at('कथा कहती'), at('तब ब्रह्मा'), (t) => {
  let w = bg('sky') + cloud(300, 1500, 1.6) + cloud(800, 1520, 1.5) + brahma({ x: 760, y: 1460, s: 0.75, t, glow: 0.5 });
  w += yamraj({ x: 260, y: 1720, s: 0.72, folded: true, eyes: 'open' });
  const sw = seg(t, at('अनगिनत') - 0.2, at('तब ब्रह्मा'));
  for (let i = 0; i < Math.floor(260 * sw); i++) w += `<circle cx="${(rnd(i) * 1080).toFixed(0)}" cy="${(560 + rnd(i + 7) * 700).toFixed(0)}" r="${(3 + rnd(i + 3) * 5).toFixed(1)}" fill="${['#FFE29A', '#9FD0FF', '#FFB0C0'][i % 3]}" opacity=".85"/>`;
  w += bubble(300, 1000, 'अकेले कैसे?', seg(t, at('मैं अकेले') - 0.1, at('मैं अकेले') + 0.3));
  let s = cam(540, 1150, lerp(1.0, 1.06, seg(t, at('कथा कहती'), at('तब ब्रह्मा'))), w);
  s += pill(t, at('कथा कहती') + 0.3, 'CHITRAGUPT KATHA', 60, 560);
  s += caps(t, [{ t0: at('यमराज ने ब्रह्मा'), l1: 'YAMRAJ → BRAHMA', ...LIGHT }, { t0: at('अनगिनत'), l1: 'ANGINAT JEEV', l2: 'ANGINAT KARM', t2: at('सबके कर्मों'), acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'whip');

// 3 BRAHMA MEDITATES — from his body appears a being with pen and inkpot
add(at('तब ब्रह्मा'), at('ब्रह्मा बोले'), (t) => {
  const em = eo(seg(t, at('उनकी काया') - 0.1, at('उनकी काया') + 1.6));
  const closeUp = t > at('हाथ में क़लम') - 0.15;
  let w = `<rect x="-300" y="-300" width="1700" height="2600" fill="#1A1030"/>` + stars(t, 60) + rays(540, 1100, 20, 0.05 + 0.08 * em, t) + `<circle cx="540" cy="1150" r="${(300 + 300 * em).toFixed(0)}" fill="url(#halo)" opacity="${(0.4 + 0.4 * em).toFixed(2)}"/>`;
  w += `<g opacity="${(1 - 0.6 * em).toFixed(2)}">${brahma({ x: 540, y: 1520, s: 0.85, t, folded: true })}</g>`;
  w += `<g opacity="${em.toFixed(2)}" transform="translate(0 ${(-120 * em).toFixed(0)})">${chitragupta({ x: 540, y: 1560, s: lerp(0.4, 0.82, em), eyes: 'closed', armR: -60, elbowR: -70, armL: 50, elbowL: 70 })}${dawat(700, 1500, 0.7 * em)}</g>`;
  const cyc = seg(t, at('और बहुत समय'), at('उनकी काया'));
  if (cyc > 0 && cyc < 1) w += `<g opacity=".7">${(cyc * 6) % 1 < 0.5 ? sun(160, 520, 50) : moon(160, 520, 40)}</g>`;
  const c = closeUp ? [t < at('और दवात') - 0.1 ? 560 : 700, 1240, 2.2] : [540, 1200, 1.0];
  let s = cam(...c, w);
  s += caps(t, [{ t0: at('तब ब्रह्मा'), l1: 'BRAHMA', l2: 'DHYAAN MEIN', acc: GOLDT, ...DARK }, { t0: at('और बहुत समय'), l1: 'BAHUT SAMAY BAAD...', ...DARK },
    { t0: at('उनकी काया'), l1: 'KAAYA SE PRAKAT', l2: 'EK DIVYA PURUSH', acc: GOLDT, ...DARK }, { t0: at('हाथ में क़लम'), l1: 'KALAM', l2: '+ DAWAAT', t2: at('और दवात'), acc: GOLDT, ...DARK, size: 120 }]);
  s += flashRect(t, at('उनकी काया') + 0.3, 0.4, '#FFF2C8');
  return s + TAG();
}, 'fade');

// 4 THE NAMES — kaya → Kayastha; gupt → Chitragupta
add(at('ब्रह्मा बोले'), at('तब से'), (t) => {
  let w = paperBg(t) + `<g opacity=".95">${chitragupta({ x: 820, y: 1880, s: 0.95, eyes: 'closed', armR: -60, elbowR: -70, armL: 30 })}</g>`;
  let s = cam(540, 1060, lerp(1.0, 1.06, seg(t, at('ब्रह्मा बोले'), at('तब से'))), w);
  const c1 = eo(seg(t, at('तुम मेरी') + 0.6, at('तुम मेरी') + 1.0)), c2 = eo(seg(t, at('इसलिए कायस्थ'), at('इसलिए कायस्थ') + 0.4)), c3 = eo(seg(t, at('और मेरे भीतर') + 0.4, at('और मेरे भीतर') + 0.8)), c4 = eo(seg(t, at('इसलिए नाम') + 1.0, at('इसलिए नाम') + 1.4));
  const card = (k, x, y, rot, dev, rom, col) => k > 0 ? `<g opacity="${k.toFixed(2)}">${paper(x, y, 420, 170, rot, `<text x="210" y="96" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="76" fill="${col}">${dev}</text><text x="210" y="146" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="24" fill="#6A5A4A">${rom}</text>`, { seed: x })}</g>` : '';
  s += card(c1, 60, 640, -3, 'काया', 'KAAYA = SHAREER', INK) + `<text x="510" y="760" font-family="${ANTON}" font-size="90" fill="${RED}" opacity="${c2.toFixed(2)}">→</text>` + card(c2, 590, 640, 2, 'कायस्थ', 'KAAYASTH', RED);
  s += card(c3, 60, 880, 2, 'गुप्त', 'GUPT = CHHIPA HUA', INK) + `<text x="510" y="1000" font-family="${ANTON}" font-size="90" fill="${RED}" opacity="${c4.toFixed(2)}">→</text>` + card(c4, 590, 880, -2, 'चित्रगुप्त', 'CHITRAGUPT', RED);
  s += caps(t, [{ t0: at('ब्रह्मा बोले'), l1: 'BRAHMA NE', l2: 'NAAM DIYA', acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'zoom');

// 5 HE WRITES EVERY DEED; YAMA JUDGES BY IT
add(at('तब से'), at('इसीलिए आज'), (t) => {
  const judge = t > at('और उसी') - 0.15;
  let w = yamaHall(t);
  if (!judge) { w += chitragupta({ x: 330, y: 1700, s: 0.85, eyes: 'closed', armR: -70 + Math.sin(t * 12) * 6, elbowR: -80, armL: 30 }) + ledger(700, 1700, 0.75, t, seg(t, at('तब से'), at('और उसी'))) + dawat(980, 1700, 0.7);
    for (let i = 0; i < 12; i++) { const ph = (t * 0.5 + rnd(i)) % 1; w += `<circle cx="${(1100 - ph * 500).toFixed(0)}" cy="${(700 + rnd(i + 3) * 500).toFixed(0)}" r="10" fill="#FFE29A" opacity="${(1 - ph).toFixed(2)}"/>`; } }
  else w += ledger(300, 1700, 0.5, t, 1) + scales(560, 1640, 0.8, t) + yamraj({ x: 860, y: 1720, s: 0.85, eyes: 'open', armR: -130, elbowR: -20 });
  let s = cam(540, 1250, lerp(1.0, 1.08, seg(t, at('तब से'), at('इसीलिए आज'))), w);
  s += caps(t, [{ t0: at('तब से'), l1: 'HAR JEEV KA', l2: 'HAR KARM', t2: at('हर जीव का') + 0.8, acc: GOLDT, ...DARK }, { t0: at('और उसी'), l1: 'USI LEKHE PAR', l2: 'YAMRAJ KA FAISLA', t2: at('यमराज फ़ैसला'), acc: '#FF5A4A', ...DARK }]);
  return s + TAG();
}, 'whip');

// 6 TODAY — Chitragupta Puja; tradition: worship of pen and inkpot
add(at('इसीलिए आज'), at('तो अगली'), (t) => {
  let w = bg('maroon') + rays(540, 1100, 18, 0.07, t) + `<rect x="200" y="1300" width="680" height="40" rx="10" fill="#C98A1E"/><rect x="230" y="1340" width="620" height="300" fill="#7A2E22"/>`;
  w += `<g transform="translate(540 1280)">${quill(-60, 0, 1.2, 25)}${dawat(80, 0, 1.0)}</g>`;
  for (let i = 0; i < 6; i++) w += diya(160 + i * 152, 1720, 0.55, t, i);
  w += petals(t, at('इसीलिए आज'), 40);
  let s = cam(540, 1250, lerp(1.1, 1.0, seg(t, at('इसीलिए आज'), at('तो अगली'))), w);
  s += pill(t, at('यम द्वितीया'), 'YAM DWITIYA · 11 NOV', 60, 560);
  s += stamp2(t, at('और परंपरा') + 0.3, 'PARAMPARA', 540, 1500, { col: GOLDT, rot: -6 });
  s += caps(t, [{ t0: at('इसीलिए आज'), l1: 'ISILIYE AAJ', l2: 'CHITRAGUPT PUJA', t2: at('चित्रगुप्त पूजा'), acc: GOLDT, ...DARK }, { t0: at('क़लम और दवात'), l1: 'KALAM + DAWAAT', l2: 'KI PUJA', acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'fade');

// 7 THE PEN IS MOVING
add(at('तो अगली'), 999, (t) => {
  const lines = 0.4 + 0.5 * seg(t, at('तो अगली'), at('तो अगली') + 7);
  let w = `<rect x="-300" y="-300" width="1700" height="2600" fill="#0E0A14"/>` + stars(t, 40) + `<circle cx="540" cy="1150" r="560" fill="url(#halo)" opacity=".3"/>` + ledger(540, 1500, 1.15, t, lines) + writingPen(t, 560, 1500 - 1.15 * (420 - (Math.floor(lines * 28) % 14) * 31), 320);
  let s = cam(540, 1180, lerp(1.0, 1.25, seg(t, at('तो अगली'), at('तो अगली') + 7)), w);
  s += caps(t, [{ t0: at('तो अगली'), l1: 'AGLI BAAR', l2: 'KUCH KARNE SE PEHLE...', t2: at('कुछ भी'), acc: GOLDT, ...DARK }, { t0: at('क़लम चल'), l1: 'KALAM', l2: 'CHAL RAHI HAI.', acc: '#FF5A4A', ...DARK, size: 120 }]);
  const cta = eo(seg(t, at('क़लम चल') + 1.4, at('क़लम चल') + 1.8));
  if (cta > 0) s += pill(t, at('क़लम चल') + 1.4, 'SAVE KARO · SHARE KARO', 540, 1450, { center: true, bg: RED });
  return s + TAG();
}, 'fade');

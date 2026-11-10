// Annakut · 56 Bhog kyun? (10 Nov 2026). Scripture: Bhagavata Purana 10.24.26 (dishes cooked from the Indra-yajna stores),
// 10.24.35-36 (Krishna takes a huge form, "shailo 'smi", eats the offerings; child Krishna bows with the Vrajavasis to that form).
// The 7 days x 8 pahar = 56 explanation is folk tradition and is labelled so on screen.
const rays = (cx, cy, n, op, t, col = '#FFF2C6') => [...Array(n)].map((_, i) => { const a = (i * 360 / n + t * 5) * Math.PI / 180, b = a + 0.12;
  return `<path d="M${cx} ${cy} L${(cx + Math.cos(a) * 2400).toFixed(0)} ${(cy + Math.sin(a) * 2400).toFixed(0)} L${(cx + Math.cos(b) * 2400).toFixed(0)} ${(cy + Math.sin(b) * 2400).toFixed(0)}Z" fill="${col}" opacity="${op}"/>`; }).join('');
const pop = (t, t0, d = 0.35) => back(seg(t, t0, t0 + d));
const C56 = at('छप्पन।');
window.HOOK = { l1: 'कृष्ण ने ख़ुद को', l2: 'प्रणाम किया?', t1: at('और उनका ही') - 0.1, y: 860 };

// 0 HOOK — little Krishna bows to... himself
add(0, at('आज अन्नकूट'), (t) => {
  const gk = Math.max(0.9, eo(seg(t, at('ख़ुद को') - 0.2, at('ख़ुद को') + 1.2)));
  const c = camPath(t, [[0, 470, 1180, 1.12], [at('ख़ुद को') + 0.2, 380, 1320, 1.5], [at('और उनका ही') + 0.3, 540, 980, 0.95], [at('पूरे ब्रज'), 540, 1000, 1.0], [at('आज अन्नकूट'), 600, 900, 1.15]]);
  let w = bg('dusk') + stars(t, 30);
  w += giantKrishna(620, 1200, 1.55, gk, t);
  w += mountain({ x: 600, y: 1520, w: 1100, h: 520, t, diyas: true });
  w += ground(1500, '#6B3B2A', '#5A3022');
  // the bhog in front, rising toward the giant form
  const fly = seg(t, at('पूरे ब्रज') + 0.4, at('आज अन्नकूट') - 0.1);
  ['laddoo', 'kheer', 'jalebi', 'puri', 'halwa'].forEach((f, i) => { const k = eio(clamp(fly * 1.4 - i * 0.1)); const x0 = 560 + (i - 2) * 120, y0 = 1700;
    w += `<g opacity="${(1 - k * 0.9).toFixed(2)}">${food(f, lerp(x0, 640, k), lerp(y0, 760, k), lerp(0.55, 0.15, k), t)}</g>`; });
  w += krishna({ x: 300, y: 1690, s: 0.62, armL: 38, elbowL: -112, armR: -38, elbowR: 112, tilt: 8, eyes: 'closed' });
  w += person({ x: 150, y: 1700, s: 0.5, gopi: true, veil: '#C2405A', top: '#F2A03D', armL: 38, elbowL: -112, armR: -38, elbowR: 112 });
  let s = cam(...c, w);
  s += title('DOOSRA ROOP', 280, 96, seg(t, at('और उनका ही') + 0.5, at('और उनका ही') + 0.8) * (1 - seg(t, at('पूरे ब्रज') - 0.2, at('पूरे ब्रज'))), '#FFE29A');
  s += title('BRAJ KA SAARA BHOG', 280, 84, seg(t, at('पूरे ब्रज'), at('पूरे ब्रज') + 0.3), '#FFE29A');
  return s;
});

// 1 TODAY: ANNAKUT · 56 BHOG · WHY 56?
add(at('आज अन्नकूट'), at('भागवत पुराण'), (t) => {
  const c = camPath(t, [[at('आज अन्नकूट'), 540, 1150, 1.25], [at('और आज बनते'), 540, 1050, 1.05], [at('पर छप्पन ही'), 540, 1000, 1.0], [at('भागवत पुराण'), 540, 960, 1.1]]);
  let w = bg('maroon') + stars(t, 40) + rays(540, 1200, 18, 0.06, t) + annakut(540, 1560, 1.35, t) + dust(t, 40);
  let s = cam(...c, w);
  s += title('आज अन्नकूट', 380, 150, seg(t, at('आज अन्नकूट'), at('आज अन्नकूट') + 0.4) * (1 - seg(t, at('और आज बनते'), at('और आज बनते') + 0.3)), '#F5C04A', 'Baloo', 800, 'GOVARDHAN PUJA · 10 NOV');
  const n = Math.round(56 * eo(seg(t, at('और आज बनते') + 0.3, at('छप्पन भोग') + 0.6)));
  s += title(`${n} BHOG`, 400, 170, seg(t, at('और आज बनते') + 0.3, at('और आज बनते') + 0.6) * (1 - seg(t, at('पर छप्पन ही') - 0.1, at('पर छप्पन ही') + 0.2)), '#F5C04A');
  const q = seg(t, at('पर छप्पन ही'), at('पर छप्पन ही') + 0.35);
  s += title('56 HI KYUN?', 400, 160 + 8 * Math.sin(t * 8) * q, q, '#FFF3DC');
  return s;
}, 'zoom');

// 2 BHAGAVATA: cook from the yajna stores — kheer, halwa, pue, puriyan — offer to Govardhan
add(at('भागवत पुराण'), at('तभी हुआ'), (t) => {
  const c = camPath(t, [[at('भागवत पुराण'), 540, 1180, 1.3], [at('इंद्र के यज्ञ'), 540, 1080, 1.05], [at('खीर') - 0.2, 540, 1000, 1.0], [at('और ये भोग'), 540, 1000, 1.0], [at('तभी हुआ'), 540, 900, 0.92]]);
  let w = bg('dawn') + sun(860, 500, 80) + rays(860, 500, 14, 0.07, t);
  const mk = eo(seg(t, at('और ये भोग') - 0.2, at('और ये भोग') + 0.8));
  w += `<g opacity="${mk.toFixed(2)}">${mountain({ x: 540, y: 1340, w: 1200, h: 640, t, garland: true })}</g>`;
  w += ground(1330, '#8CBF6A', '#78AD5C');
  const ck = 1 - seg(t, at('खीर') - 0.4, at('खीर'));
  if (ck > 0) {
    w += `<g opacity="${ck.toFixed(2)}">` + krishna({ x: 540, y: 1600, s: 0.9, eyes: 'open', armR: -60 + Math.sin(t * 3) * 12, elbowR: -50, mouth: Math.sin(t * 17) > 0 ? 'open' : 'smile' });
    w += person({ x: 190, y: 1640, s: 0.62, stick: true, top: '#3E8E5A' }) + person({ x: 890, y: 1640, s: 0.62, gopi: true, veil: '#7B4BB7', top: '#F5C04A' });
    const yk = seg(t, at('इंद्र के यज्ञ') - 0.2, at('इंद्र के यज्ञ') + 0.4);
    w += `<g opacity="${yk.toFixed(2)}">${chulha(300, 1820, 0.7, t, 1)}${chulha(780, 1820, 0.7, t, 2)}</g></g>`;
  }
  // the dishes, one per word, then they line up in front of the mountain as bhog
  const dishes = [['kheer', 'खीर', at('खीर')], ['halwa', 'हलवा', at('हलवा')], ['pua', 'पुए', at('पुए')], ['puri', 'पूड़ियाँ', at('पूड़ियाँ')]];
  const line = eio(seg(t, at('और ये भोग'), at('और ये भोग') + 0.9));
  dishes.forEach(([f, label, t0], i) => {
    if (t < t0 - 0.05) return;
    const k = pop(t, t0, 0.3), next = i < 3 ? dishes[i + 1][2] : at('और ये भोग');
    const solo = t < next;
    const gx = 540 + (i - 1.5) * 230, gy = 1520;
    const x = solo ? 540 : lerp(540, gx, line), y = solo ? 1150 : lerp(1150, gy, line), sc = solo ? 1.9 * k : lerp(1.9, 0.75, line);
    if (!solo && line === 0) return;
    w += food(f, x, y, sc, t);
    if (solo) w += `<text x="540" y="1380" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="110" fill="#7A2E12" opacity="${clamp(k).toFixed(2)}">${label}</text>`;
  });
  let s = cam(...c, w);
  s += title('श्रीमद् भागवत', 300, 92, seg(t, at('भागवत पुराण'), at('भागवत पुराण') + 0.4) * (1 - seg(t, at('इंद्र के यज्ञ') - 0.2, at('इंद्र के यज्ञ'))), '#7A2E12', 'Baloo', 800, '10.24.26', '#7A2E12');
  s += title('YAGYA KI SAAMAGRI = PAKWAAN', 300, 62, seg(t, at('इंद्र के यज्ञ'), at('इंद्र के यज्ञ') + 0.3) * (1 - seg(t, at('खीर') - 0.3, at('खीर') - 0.1)), '#7A2E12');
  s += title('BHOG GOVARDHAN KO', 300, 84, seg(t, at('और ये भोग') + 0.2, at('और ये भोग') + 0.5), '#7A2E12');
  return s;
}, 'push');

// 3 THE WONDER — the huge form: "I am Govardhan"; it accepts the bhog
add(at('तभी हुआ'), at('और नन्हे'), (t) => {
  const gk = eo(seg(t, at('विशाल रूप') - 0.3, at('विशाल रूप') + 1.4));
  const c = camPath(t, [[at('तभी हुआ'), 540, 1300, 1.2], [at('विशाल रूप'), 540, 1250, 1.05], [at('विशाल रूप') + 1.6, 540, 900, 0.82], [at('मैं ही'), 540, 820, 0.95], [at('और वो सारा'), 540, 900, 0.88], [at('और नन्हे'), 540, 960, 0.92]]);
  let w = `<g opacity="${(1 - gk).toFixed(2)}">${bg('dawn')}</g><g opacity="${gk.toFixed(2)}">${bg('dusk')}${stars(t, 40)}</g>`;
  w += giantKrishna(540, 1420, 1.9, gk, t);
  w += mountain({ x: 540, y: 1560, w: 1300, h: 640, t, garland: true, diyas: true });
  w += ground(1550, '#6B3B2A', '#5A3022');
  const eat = seg(t, at('और वो सारा') + 0.2, at('और नन्हे') - 0.4);
  ['kheer', 'halwa', 'pua', 'puri', 'laddoo', 'jalebi'].forEach((f, i) => { const k = eio(clamp(eat * 1.6 - i * 0.12)); const x0 = 160 + i * 152;
    w += `<g opacity="${(1 - k).toFixed(2)}">${food(f, lerp(x0, 540, k), lerp(1720, 700, k), lerp(0.62, 0.2, k), t)}</g>`;
    if (k > 0.05 && k < 0.95) w += `<circle cx="${lerp(x0, 540, k).toFixed(0)}" cy="${lerp(1720, 700, k).toFixed(0)}" r="40" fill="url(#halo)"/>`; });
  w += dust(t, 40, '#FFE7A0', 50);
  let s = cam(...c, `<g transform="${shake(t, at('विशाल रूप'), 0.8, 10)}">${w}</g>`);
  s += title('TABHI HUA ADBHUT', 300, 84, seg(t, at('तभी हुआ'), at('तभी हुआ') + 0.3) * (1 - seg(t, at('विशाल रूप') - 0.2, at('विशाल रूप'))), '#7A2E12');
  s += title('VISHAAL ROOP', 250, 110, seg(t, at('विशाल रूप') + 0.3, at('विशाल रूप') + 0.6) * (1 - seg(t, at('मैं ही') - 0.2, at('मैं ही'))), '#FFE29A');
  const sk = seg(t, at('मैं ही'), at('मैं ही') + 0.4) * (1 - seg(t, at('और वो सारा') + 0.6, at('और वो सारा') + 0.9));
  s += title('शैलोऽस्मि', 260, 150, sk, '#FFE29A', 'Baloo', 800, '"MAIN HI GOVARDHAN HOON" · BHAGAVAT 10.24.35', '#FFF3DC');
  s += title('SAARA BHOG GRAHAN', 260, 84, seg(t, at('और वो सारा') + 0.9, at('और वो सारा') + 1.2), '#FFE29A');
  s += flashRect(t, at('विशाल रूप') + 0.2, 0.45, '#FFF2C8');
  return s;
}, 'fade');

// 4 LITTLE KRISHNA BOWS — and the mountain becomes a mountain of food
add(at('और नन्हे'), at('अब छप्पन'), (t) => {
  const c = camPath(t, [[at('और नन्हे'), 380, 1450, 1.6], [at('उसी रूप') - 0.2, 460, 1350, 1.25], [at('उसी रूप') + 1.2, 540, 960, 0.9], [at('यही है'), 540, 960, 0.9], [at('अब छप्पन'), 540, 1100, 1.05]]);
  const morph = eio(seg(t, at('यही है') + 0.3, at('अन्न का') + 0.3));
  let w = bg('dusk') + stars(t, 40);
  w += `<g opacity="${(1 - morph).toFixed(2)}">${giantKrishna(540, 1380, 1.9, 1, t)}${mountain({ x: 540, y: 1520, w: 1300, h: 640, t, garland: true, diyas: true })}</g>`;
  w += `<g opacity="${morph.toFixed(2)}">${rays(540, 1100, 18, 0.08, t)}${annakut(540, 1520, 2.0, t)}</g>`;
  w += ground(1510, '#6B3B2A', '#5A3022');
  const bowK = seg(t, at('उसी रूप'), at('उसी रूप') + 0.6), tilt = 14 * eo(bowK);
  const fold = { armL: 38, elbowL: -112, armR: -38, elbowR: 112 };
  w += krishna({ x: 420, y: 1720, s: 0.7, ...fold, tilt, eyes: 'closed' });
  w += person({ x: 220, y: 1730, s: 0.55, gopi: true, veil: '#C2405A', top: '#F2A03D', ...fold }) + person({ x: 620, y: 1730, s: 0.55, top: '#3E8E5A', ...fold }) + person({ x: 820, y: 1730, s: 0.55, gopi: true, veil: '#2F7FB8', top: '#F5C04A', ...fold }) + person({ x: 80, y: 1740, s: 0.5, top: '#D8432F', ...fold });
  let s = cam(...c, w);
  s += title('NANHE KRISHNA', 280, 92, seg(t, at('और नन्हे'), at('और नन्हे') + 0.3) * (1 - seg(t, at('उसी रूप') - 0.1, at('उसी रूप') + 0.1)), '#FFE29A');
  s += title('KHUD KO PRANAAM', 280, 92, seg(t, at('उसी रूप') + 0.2, at('उसी रूप') + 0.5) * (1 - seg(t, at('यही है') - 0.1, at('यही है') + 0.1)), '#FFE29A');
  s += title('अन्नकूट', 300, 160, seg(t, at('यही है') + 0.2, at('यही है') + 0.6), '#F5C04A', 'Baloo', 800, null);
  s += title('= ANN KA PAHAAD', 430, 70, seg(t, at('अन्न का'), at('अन्न का') + 0.3), '#FFF3DC');
  return s;
}, 'fade');

// 5 THE MATH OF 56 — stamped: folk belief, not scripture
add(at('अब छप्पन'), at('कहते हैं'), (t) => {
  let w = bg('court');
  for (let i = 0; i < 26; i++) w += `<line x1="0" y1="${300 + i * 60}" x2="1080" y2="${300 + i * 60}" stroke="#E3CFA8" stroke-width="2"/>`;
  w += `<line x1="140" y1="0" x2="140" y2="1920" stroke="#E7A9A0" stroke-width="3"/>`;
  const k = pop(t, at('अब छप्पन'), 0.4);
  w += `<g transform="translate(540 900) scale(${k.toFixed(3)})"><text x="0" y="0" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="300" fill="#7A2E12">56</text>
       <text x="0" y="120" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="90" fill="#B8641A">= ? × ?</text></g>`;
  const st = seg(t, at('लोक-मान्यता') - 0.1, at('लोक-मान्यता') + 0.25);
  if (st > 0) { const sc = lerp(2.2, 1, eo(st));
    w += `<g transform="translate(540 1330) rotate(-8) scale(${sc.toFixed(3)})" opacity="${clamp(st * 2).toFixed(2)}"><rect x="-330" y="-90" width="660" height="180" rx="26" fill="none" stroke="#C1272D" stroke-width="12"/>
          <text x="0" y="-12" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="70" fill="#C1272D">LOK-MAANYATA</text><text x="0" y="56" text-anchor="middle" font-family="Baloo" font-weight="700" font-size="38" fill="#C1272D">SHAASTRA NAHI</text></g>`; }
  let s = cam(540, 960, lerp(1.0, 1.06, seg(t, at('अब छप्पन'), at('कहते हैं'))), w);
  s += title('CHHAPPAN KA HISAAB', 300, 84, seg(t, at('अब छप्पन'), at('अब छप्पन') + 0.3), '#7A2E12');
  return s;
}, 'whip');

// 6 KANHA EATS 8 TIMES A DAY — eight pahar dial
add(at('कहते हैं'), at('पर जब'), (t) => {
  const lit = Math.floor(8 * seg(t, at('आठ बार') - 0.2, at('आठ पहर') + 0.2) + 0.001);
  let w = bg('saffron') + rays(540, 1180, 16, 0.12, t);
  w += dial8(540, 1180, 400, lit, t);
  const bite = Math.sin(t * 6) > 0.3;
  w += food('makhan', 690, 1500, 0.8, t);
  w += krishna({ x: 520, y: 1580, s: 0.82, eyes: 'closed', armR: bite ? -150 : -120, elbowR: bite ? -40 : -20, armL: 30, mouth: bite ? 'open' : 'smile' });
  if (bite) w += `<circle cx="${(520 + 70).toFixed(0)}" cy="1160" r="18" fill="#FFF8DC"/>`;
  let s = cam(540, 1180, lerp(1.15, 1.0, seg(t, at('कहते हैं'), at('पर जब'))), w);
  s += title('KANHA', 260, 100, seg(t, at('कहते हैं') + 0.4, at('कहते हैं') + 0.7) * (1 - seg(t, at('आठ बार') - 0.2, at('आठ बार'))), '#FFF8E6');
  s += title('DIN MEIN 8 BAAR BHOJAN', 260, 76, seg(t, at('आठ बार'), at('आठ बार') + 0.3) * (1 - seg(t, at('आठ पहर') - 0.1, at('आठ पहर'))), '#7A1E12');
  s += title('8 PEHAR', 260, 130, seg(t, at('आठ पहर'), at('आठ पहर') + 0.3), '#7A1E12');
  return s;
}, 'zoom');

// 7 SEVEN DAYS — not a single grain
add(at('पर जब'), at('बारिश थमी'), (t) => {
  const t0 = at('पर जब'), t1 = at('एक दाना');
  const p = seg(t, t0, t1) * 7, day = Math.min(7, 1 + Math.floor(p)), isNight = (p - Math.floor(p)) > 0.5 && t < t1;
  let s = cam(540, 980, lerp(1.0, 1.1, seg(t, t0, at('बारिश थमी'))), wideLift(t, { sky: isNight ? 'night' : 'storm', starsOn: isNight, rain: 1.0, glowDome: 0.35 }));
  s += counter(day, 7, isNight ? 'RAAT' : 'DIN', 70, 330, 1);
  const ek = seg(t, t1, t1 + 0.35);
  if (ek > 0) {
    s += `<g transform="translate(800 330) scale(${back(ek).toFixed(3)})"><circle r="110" fill="#F5C04A" opacity=".95"/><circle r="90" fill="#F2C766"/><path d="M-64 -64 L64 64 M64 -64 L-64 64" stroke="#C1272D" stroke-width="18" stroke-linecap="round"/></g>`;
    s += title('EK DAANA BHI NAHI', 560, 80, ek, '#FFE29A');
  }
  return s;
}, 'whip');

// 8 RAIN STOPS — Yashoda and Braj cook 7 days x 8 pahar together
const GRID = { x0: 150, y0: 640, dx: 112, dy: 92 };
function grid56(t, n, glowAll = 0) {
  let g = '';
  for (let d = 0; d < 7; d++) g += `<text x="${GRID.x0 + d * GRID.dx}" y="${GRID.y0 - 60}" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="30" fill="#7A2E12">D${d + 1}</text>`;
  for (let i = 0; i < Math.min(56, n); i++) {
    const d = Math.floor(i / 8), p = i % 8, x = GRID.x0 + d * GRID.dx, y = GRID.y0 + p * GRID.dy;
    const k = clamp((n - i) * 1.5);
    g += `<g transform="translate(${x} ${y}) scale(${(0.33 * back(k)).toFixed(3)})">${food(FOODS[(i * 3) % FOODS.length], 0, 40, 1, t)}</g>`;
  }
  if (glowAll) g += `<rect x="${GRID.x0 - 70}" y="${GRID.y0 - 100}" width="${GRID.dx * 6 + 140}" height="${GRID.dy * 8 + 70}" rx="30" fill="none" stroke="#F5C04A" stroke-width="10" opacity="${glowAll}"/>`;
  return g;
}
add(at('बारिश थमी'), at('सात गुणा'), (t) => {
  const c = camPath(t, [[at('बारिश थमी'), 540, 1100, 1.2], [at('माँ यशोदा') + 0.6, 540, 1250, 1.0], [at('सात दिन के') - 0.1, 540, 1250, 1.0], [at('सात दिन के') + 0.8, 540, 960, 1.0]]);
  const clear = eo(seg(t, at('बारिश थमी') - 0.2, at('बारिश थमी') + 1.0));
  const gridK = eio(seg(t, at('सात दिन के') - 0.2, at('सात दिन के') + 0.6));
  let w = `<g opacity="${(1 - clear).toFixed(2)}">${bg('storm')}</g><g opacity="${clear.toFixed(2)}">${bg('dawn')}${sun(820, 420, 90)}</g>`;
  if (clear < 1) w += `<g opacity="${(1 - clear).toFixed(2)}">${rain(t, 1.2, 0.6, 0.15)}</g>`;
  w += `<g opacity="${(1 - gridK * 0.85).toFixed(2)}">`;
  w += ground(1500, '#8CBF6A', '#78AD5C');
  w += chulha(230, 1760, 0.8, t, 1) + chulha(560, 1780, 0.8, t, 2) + chulha(880, 1760, 0.8, t, 3);
  const yk = pop(t, at('बारिश थमी') + 0.5, 0.5);
  w += `<g opacity="${clamp(yk).toFixed(2)}">${yashoda({ x: 400, y: 1600, s: 0.85, armR: -70 + Math.sin(t * 5) * 14, elbowR: -60, t })}${person({ x: 720, y: 1610, s: 0.72, gopi: true, veil: '#2F7FB8', top: '#F2A03D', armL: 70 + Math.sin(t * 5 + 1) * 14, elbowL: 60, t })}${person({ x: 980, y: 1620, s: 0.62, top: '#3E8E5A', armL: 60, elbowL: 50 })}</g>`;
  w += `</g>`;
  if (gridK > 0) { const n = 56 * seg(t, at('सात दिन के') + 0.3, at('सात गुणा') - 0.1) ** 0.8;
    w += `<g opacity="${gridK.toFixed(2)}"><rect x="60" y="500" width="960" height="860" rx="40" fill="#FFF6E2" opacity=".92"/>${grid56(t, n)}</g>`; }
  let s = cam(...c, w);
  s += title('BAARISH THAMI', 300, 96, seg(t, at('बारिश थमी'), at('बारिश थमी') + 0.3) * (1 - seg(t, at('माँ यशोदा') - 0.2, at('माँ यशोदा'))), '#7A2E12');
  s += title('MAA YASHODA + BRAJ', 300, 84, seg(t, at('माँ यशोदा'), at('माँ यशोदा') + 0.3) * (1 - seg(t, at('सात दिन के') - 0.2, at('सात दिन के'))), '#7A2E12');
  s += title('7 DIN × 8 PEHAR', 330, 96, seg(t, at('सात दिन के'), at('सात दिन के') + 0.3), '#7A2E12');
  return s;
}, 'fade');

// 9 7 × 8 = 56
add(at('सात गुणा'), at('तो आज'), (t) => {
  let w = bg('gold') + rays(540, 900, 20, 0.12, t) + `<rect x="60" y="500" width="960" height="860" rx="40" fill="#FFF6E2" opacity=".92"/>` + grid56(t, 56, seg(t, C56 - 0.1, C56 + 0.3));
  let s = cam(540, 960, lerp(1.0, 0.94, seg(t, at('सात गुणा'), at('तो आज'))), w);
  const n = t < C56 ? 0 : Math.round(56 * eo(seg(t, C56, C56 + 0.7)));
  s += title('7 × 8', 330, 150, seg(t, at('सात गुणा'), at('सात गुणा') + 0.3) * (1 - seg(t, C56 - 0.15, C56)), '#4A1A08');
  if (t >= C56) s += title(`= ${n}`, 340, 190, seg(t, C56, C56 + 0.25), '#4A1A08');
  s += title('CHHAPPAN BHOG', 1500, 110, seg(t, C56 + 0.8, C56 + 1.1), '#7A1E12');
  s += flashRect(t, C56, 0.3, '#FFF6E0');
  return s;
}, 'zoom');

// 10 THE THALI — not God's hunger, our love
add(at('तो आज'), at('कल, पाँचवाँ'), (t) => {
  const c = camPath(t, [[at('तो आज'), 540, 1000, 1.25], [at('याद रखिए'), 540, 960, 1.0], [at('हमारा प्रेम') - 0.4, 540, 1180, 1.05], [at('कल, पाँचवाँ'), 540, 1180, 1.12]]);
  const fill = Math.floor(8 * seg(t, at('तो आज'), at('याद रखिए')) + 0.001);
  const love = eio(seg(t, at('हमारा प्रेम') - 0.8, at('हमारा प्रेम') + 0.2));
  let w = bg('maroon') + stars(t, 40);
  w += `<g opacity="${(1 - love).toFixed(2)}">${thali(540, 1000, 1.25, fill, t)}</g>`;
  w += `<g opacity="${love.toFixed(2)}">${rays(540, 1100, 18, 0.07, t)}<circle cx="540" cy="1150" r="420" fill="url(#halo)"/>`;
  w += yashoda({ x: 640, y: 1640, s: 0.95, armR: -150 + Math.sin(t * 2) * 6, elbowR: -50, t }) + krishna({ x: 420, y: 1640, s: 0.8, armL: 20, armR: -20, eyes: 'closed', mouth: 'open' });
  w += food('laddoo', 300, 1680, 0.5, t) + `</g>`;
  w += dust(t, 40, '#FFD98A', 40);
  let s = cam(...c, w);
  s += title('THAALI SAJAAYEIN', 260, 88, seg(t, at('तो आज') + 0.2, at('तो आज') + 0.5) * (1 - seg(t, at('याद रखिए') - 0.2, at('याद रखिए'))), '#FFE29A');
  s += title('BHAGWAN KI BHOOKH NAHI', 260, 76, seg(t, at('याद रखिए') + 0.6, at('याद रखिए') + 0.9) * (1 - seg(t, at('हमारा प्रेम') - 0.2, at('हमारा प्रेम'))), '#FFE29A');
  s += title('HAMARA PREM', 260, 130, seg(t, at('हमारा प्रेम'), at('हमारा प्रेम') + 0.3), '#F5C04A', 'Baloo', 800, '❤');
  return s;
}, 'fade');

// 11 TOMORROW — the fifth and last diya: Bhai Dooj
add(at('कल, पाँचवाँ'), 999, (t) => {
  const yk = eo(seg(t, at('यमराज') - 0.2, at('यमराज') + 0.8));
  let w = `<g transform="translate(0 ${(-260 * yk).toFixed(1)})" opacity="${(1 - 0.5 * yk).toFixed(2)}">` + tracker(t, 4, 4, at('भाई दूज')) + `</g>`;
  w += `<g opacity="${yk.toFixed(2)}"><circle cx="540" cy="1260" r="420" fill="url(#moonglow)"/><circle cx="540" cy="1260" r="190" fill="#FFF3D1" opacity=".9"/>`;
  let riv = 'M-200 1560'; for (let x = -200; x <= 1300; x += 40) riv += ` L${x} ${(1560 + Math.sin(x / 90 + t * 2) * 10).toFixed(1)}`; riv += ' V2400 H-200Z';
  w += `<path d="${riv}" fill="#2A3A7A"/><path d="${riv}" transform="translate(0 34)" fill="#1E2A5E"/>`;
  w += yamraj(420, 1580, 0.78).replace(/#1B1030/g, '#2C2152') + `<g opacity="${eo(seg(t, at('यमराज') + 1.6, at('यमराज') + 2.4)).toFixed(2)}">` + hut(770, 1560, 0.7, '#3A2E62').replace(/#[0-9A-F]{6}/gi, (m) => m === '#3A2E62' ? m : '#2C2152') + `<rect x="740" y="1470" width="60" height="70" rx="20" fill="#FFD27A" opacity=".85"/></g></g>`;
  let s = cam(540, 960, lerp(1.0, 1.08, seg(t, at('कल, पाँचवाँ'), at('कल, पाँचवाँ') + 9)), w);
  const tk = 1 - seg(t, at('यमराज') - 0.2, at('यमराज') + 0.3);
  s += title('KAL · AAKHIRI DIYA', 520, 64, seg(t, at('कल, पाँचवाँ'), at('कल, पाँचवाँ') + 0.3) * tk, '#FFF3DC');
  s += title('BHAI DOOJ', 660, 140, seg(t, at('भाई दूज'), at('भाई दूज') + 0.3) * tk, '#F5C04A', 'Baloo', 800, 'DEEPOTSAV · DIN 5 / 5');
  s += title('YAMRAJ', 330, 120, seg(t, at('यमराज'), at('यमराज') + 0.3), '#F5C04A');
  s += title('BEHEN KE GHAR KYUN GAYE?', 440, 60, seg(t, at('यमराज') + 1.0, at('यमराज') + 1.3), '#FFF3DC');
  return s;
}, 'fade');

// Yaksha Prashna — Mahabharata, Vana (Aranyaka) Parva: thirsty Pandavas at a lake; a crane (the Yaksha) forbids drinking
// before answering; Nakula, Sahadeva, Arjuna, Bhima drink and fall; Yudhishthira answers (mother heavier than earth, father
// higher than sky, mind swifter than wind; the greatest wonder: people die daily yet the rest think they will live forever);
// offered one brother's life he chooses Nakula so that Madri too has a living son; the Yaksha is Dharma himself; all revive.
const DARK = { dark: false }, LIGHT = { dark: true };
const TAG = () => tagTR('MAHABHARAT KI KAHANIYAAN');
const BRO = ['nakul', 'sahdev', 'arjun', 'bhima'];
const NAMES = { nakul: 'NAKUL', sahdev: 'SAHDEV', arjun: 'ARJUN', bhima: 'BHIM' };
const armsFor = (n) => n === 'bhima' ? { armR: -150, elbowR: -10 } : { armR: -20, elbowR: -10 };
const fallenRow = (y, s = 0.36, op = 1) => BRO.map((n, i) => `<g opacity="${op}">${fallen(pandav(n, { eyes: 'closed', ...armsFor(n) }), 180 + i * 230 + (i % 2) * 20, y + (i % 2) * 40, s, i % 2 === 1)}</g>`).join('');
const dusk = (t) => bg('dusk') + sun(820, 700, 70, '#FFC07A') + `<rect x="-300" y="1360" width="1700" height="900" fill="#5E6A3A"/>` + tree2(-40, 1000, 2.2, Math.sin(t) * 2, '#2A4A3A', '#1E3A2E', '#3A5E44') + tree2(1120, 1000, 2.4, Math.sin(t + 1) * 2, '#2A4A3A', '#1E3A2E', '#3A5E44');

// 0 HOOK — four brothers lie by the lake; the fifth walks in
add(0, at('महाभारत'), (t) => {
  let w = dusk(t) + lake(t, 960) + crane(770, 1290, 0.85, t, 0) + fallenRow(1430);
  w += pandav('yudhi', { x: lerp(70, 200, eo(seg(t, 0, 4))), y: 1600, s: 0.55, eyes: 'open', armR: -20, elbowR: -10 });
  let s = cam(540, lerp(1260, 1300, seg(t, 0, 6)), lerp(1.32, 1.2, eo(seg(t, 0, 6))), w);
  s += caps(t, [{ t0: -0.6, l1: '4 BHAI GIR PADE', l2: '5VE KE PAAS SIRF JAWAAB', t2: at('पाँचवें के'), acc: GOLDT, ...DARK }]);
  return s + TAG();
});

// 1 THE LAKE AND THE CRANE — "answer first, then drink"
add(at('महाभारत'), at('नकुल, सहदेव'), (t) => {
  const walk = eo(seg(t, at('प्यासे पांडव') - 0.4, at('एक बगुला')));
  let w = bg('day') + `<rect x="-300" y="1360" width="1700" height="900" fill="#6E8A44"/>` + tree2(-40, 1000, 2.2, Math.sin(t) * 2) + tree2(1120, 1000, 2.4, Math.sin(t + 1) * 2) + lake(t, 960);
  const talk = t > at('एक बगुला') + 0.6 && t < at('नकुल, सहदेव') - 0.3 ? 1 : 0;
  w += crane(760, 1290, 0.85, t, talk);
  ['yudhi', 'bhima', 'arjun', 'nakul', 'sahdev'].forEach((n, i) => { w += pandav(n, { x: lerp(-400 + i * 120, 90 + i * 110, walk), y: 1600 + (i % 2) * 30, s: 0.5, eyes: 'open', ...armsFor(n) }); });
  let s = cam(lerp(500, 580, seg(t, at('महाभारत'), at('नकुल, सहदेव'))), 1300, lerp(1.2, 1.28, seg(t, at('एक बगुला'), at('नकुल, सहदेव'))), w);
  s += pill(t, at('महाभारत') + 0.3, 'MAHABHARAT · VAN PARVA', 60, 560);
  s += caps(t, [{ t0: at('महाभारत'), l1: 'PYAASE PANDAV', l2: 'JHEEL PAR', t2: at('प्यासे पांडव'), acc: RED, ...LIGHT },
    { t0: at('एक बगुला'), l1: 'EK BAGULA BOLA:', l2: '"PEHLE JAWAAB, PHIR PAANI"', t2: at('पहले मेरे'), acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'push');

// 2 FOUR BROTHERS DRINK AND FALL
add(at('नकुल, सहदेव'), at('फिर आए'), (t) => {
  const T0 = at('नकुल, सहदेव'), T1 = at('किसी ने'), step = (T1 - T0) / 4;
  let w = dusk(t) + lake(t, 960) + crane(800, 1290, 0.8, t, 0);
  BRO.forEach((n, i) => { const tf = T0 + step * i + 0.35, k = eio(seg(t, tf, tf + 0.35)), x = 150 + i * 240, y = 1520;
    w += k <= 0 ? pandav(n, { x, y, s: 0.5, eyes: 'open', ...armsFor(n) }) : `<g transform="translate(${x} ${y}) rotate(${(-88 * k).toFixed(1)}) translate(${-x} ${-y})">${pandav(n, { x, y, s: 0.5, eyes: k > 0.5 ? 'closed' : 'open', ...armsFor(n) })}</g>`; });
  let s = `<g transform="${shake(t, at('चारों गिर'), 0.5, 14)}">${cam(540, 1300, lerp(1.2, 1.26, seg(t, T0, at('फिर आए'))), w)}</g>`;
  BRO.forEach((n, i) => { s += pill(t, T0 + step * i, NAMES[n], 540 + (150 + i * 240 - 540) * 1.2, 1460, { bg: RED, center: true }); });
  s += caps(t, [{ t0: T0, l1: 'NAKUL, SAHDEV', l2: 'ARJUN, BHIM', t2: T0 + step * 2, acc: '#FF8A6A', ...DARK }, { t0: at('किसी ने'), l1: 'KISI NE NAHI SUNA', l2: 'CHAARON GIRE', t2: at('चारों गिर'), acc: '#FF5A4A', ...DARK }]);
  return s + TAG();
}, 'whip');

// 3 YUDHISHTHIRA ANSWERS — question cards with stamped answers
add(at('फिर आए'), at('सबसे बड़ा'), (t) => {
  let w = dusk(t) + lake(t, 960) + crane(800, 1290, 0.8, t, t > at('धरती से') - 0.1 ? 1 : 0) + fallenRow(1440, 0.3, 0.8);
  w += pandav('yudhi', { x: 230, y: 1600, s: 0.5, eyes: 'open', folded: true });
  let s = cam(540, lerp(1290, 1310, seg(t, at('फिर आए'), at('सबसे बड़ा'))), lerp(1.2, 1.25, seg(t, at('फिर आए'), at('सबसे बड़ा'))), w);
  const Q = [['DHARTI SE BHAARI?', 'MAA', at('धरती से'), at('माँ।')], ['AAKASH SE UNCHA?', 'PITA', at('आकाश से'), at('पिता')], ['HAWA SE TEZ?', 'MANN', at('हवा से'), at('मन।')]];
  Q.forEach(([q, a, tq, ta], i) => { if (t < tq) return; const k = eo(seg(t, tq, tq + 0.25)), y = 560 + i * 140;
    s += `<g opacity="${k.toFixed(2)}" transform="translate(${(1 - k) * -40} 0)">${paper(60, y, 960, 112, i % 2 ? 1 : -1, `<text x="30" y="80" font-family="${ANTON}" font-size="60" fill="${INK}">${q}</text>`, { seed: i * 5 })}</g>`;
    s += stamp2(t, ta, a, 830, y + 56, { rot: -6, col: i === 0 ? RED : '#2E7A4E' }); });
  s += caps(t, [{ t0: at('फिर आए'), l1: 'YUDHISHTHIR:', l2: '"POOCHHIYE"', t2: at('पूछिए'), acc: GOLDT, ...DARK, te: at('धरती से') - 0.2 }]);
  return s + TAG();
}, 'fade');

// 4 THE GREATEST WONDER — people die every day, yet the rest think they will live forever
add(at('सबसे बड़ा'), at('यक्ष बोला'), (t) => {
  const T0 = at('सबसे बड़ा');
  let w = `<rect x="-300" y="-300" width="1700" height="2600" fill="#120C22"/>` + stars(t, 80) + yamlokGate(540, 1420, 0.55, 0.6, t) + `<rect x="-300" y="1420" width="1700" height="900" fill="#1E1630"/>`;
  for (let i = 0; i < 9; i++) { const p = ((t - T0) * 0.06 + i / 9) % 1, x = lerp(-80, 540, p), y = lerp(1600, 1440, p), sc = lerp(0.32, 0.16, p);
    w += `<g opacity="${(0.85 * (1 - p)).toFixed(2)}">${gwala2({ x, y, s: sc, top: '#5A5070', dhoti: '#8A8098', skin: '#7A6A80' })}</g>`; }
  const busy = eo(seg(t, at('फिर भी बाकी') - 0.2, at('फिर भी बाकी') + 0.5));
  for (let i = 0; i < 4; i++) w += `<g opacity="${busy.toFixed(2)}">${gwala2({ x: 760 + i * 90, y: 1640, s: 0.34, top: '#E8762E', armR: -60 + Math.sin(t * 3 + i) * 20, elbowR: -40 })}</g>`;
  let s = cam(540, 1300, lerp(1.2, 1.32, seg(t, T0, at('यक्ष बोला'))), w);
  s += pill(t, at('रोज़ लोग') + 0.3, 'ROZ: YAMLOK KI OR', 60, 1500, { bg: '#5A5070' });
  s += caps(t, [{ t0: T0, l1: 'SABSE BADA', l2: 'AASHCHARYA?', acc: GOLDT, ...DARK, size: 120 },
    { t0: at('रोज़ लोग'), l1: 'ROZ LOG MARTE HAIN...', l2: 'BAAKI SOCHTE: HUM HAMESHA RAHENGE', t2: at('फिर भी बाकी'), acc: GOLDT, ...DARK }]);
  return s + flashRect(t, at('हम हमेशा'), 0.3, '#FFE6B0') + TAG();
}, 'iris');

// 5 THE CHOICE — one brother's life: Nakula, so that Madri too has a living son
add(at('यक्ष बोला'), at('यक्ष प्रसन्न'), (t) => {
  const bal = t > at('कुंती का') - 0.2;
  let w = dusk(t) + lake(t, 960) + crane(880, 1290, 0.8, t, t < at('युधिष्ठिर बोले') ? 1 : 0);
  if (!bal) w += fallenRow(1450, 0.34) + pandav('yudhi', { x: 330, y: 1660, s: 0.5, eyes: 'open', armR: -60, elbowR: -60 });
  else { const ang = Math.sin(t * 1.6) * 8 * Math.PI / 180, dy = 190 * 1.5 * Math.sin(ang);
    w += `<rect x="-300" y="-300" width="1700" height="2600" fill="#1A1030" opacity=".55"/>` + scales(540, 1500, 1.5, t) + pandav('yudhi', { x: 255, y: 1262 - dy, s: 0.17, eyes: 'open', folded: true });
    if (t > at('माद्री का') - 0.1) w += `<g opacity="${eo(seg(t, at('माद्री का') - 0.1, at('माद्री का') + 0.4)).toFixed(2)}">${pandav('nakul', { x: 825, y: 1262 + dy, s: 0.17, eyes: 'open', folded: true })}</g>`; }
  let s = bal ? cam(540, 1250, lerp(1.0, 1.06, seg(t, at('यक्ष बोला'), at('यक्ष प्रसन्न'))), w) : cam(540, 1300, lerp(1.2, 1.26, seg(t, at('यक्ष बोला'), at('यक्ष प्रसन्न'))), w);
  if (!bal) s += strikeList(t, 60, 620, [['BHIM?', at('चुनो') + 0.1, at('युधिष्ठिर बोले') - 0.1], ['ARJUN?', at('चुनो') + 0.4, at('युधिष्ठिर बोले') + 0.1], ['NAKUL ✓', at('युधिष्ठिर बोले') + 0.8, null]]);
  else {
    s += `<text x="255" y="1440" text-anchor="middle" font-family="${ANTON}" font-size="58" fill="#FFE29A">MAA KUNTI</text><text x="255" y="1500" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="28" fill="#FFF3DC">YUDHISHTHIR</text>`;
    if (t > at('माद्री का') - 0.1) s += `<text x="825" y="1440" text-anchor="middle" font-family="${ANTON}" font-size="58" fill="#FFE29A">MAA MADRI</text><text x="825" y="1500" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="28" fill="#FFF3DC">NAKUL</text>`;
  }
  s += caps(t, [{ t0: at('यक्ष बोला'), l1: '"EK BHAI KO JEEVAN.', l2: 'CHUNO."', t2: at('चुनो'), acc: RED, ...LIGHT, te: at('कुंती का') - 0.2 },
    { t0: at('कुंती का'), l1: 'KUNTI KA EK BETA JEEVIT...', l2: 'MADRI KA BHI EK', t2: at('माद्री का'), acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'fade');

// 6 THE YAKSHA IS DHARMA HIMSELF — the brothers rise
add(at('यक्ष प्रसन्न'), at('आप होते'), (t) => {
  const T0 = at('यक्ष प्रसन्न'), rise = eio(seg(t, at('चारों भाई जी') - 0.1, at('चारों भाई जी') + 0.9)), dh = eo(seg(t, at('वो स्वयं') - 0.2, at('वो स्वयं') + 0.6));
  let w = bg('dawn') + sun(540, 760, 90) + `<rect x="-300" y="1360" width="1700" height="900" fill="#7A8A44"/>` + lake(t, 960, { lotus: true });
  w += `<g opacity="${(1 - dh).toFixed(2)}">${crane(540, 1290, 0.85, t, 0)}</g><g opacity="${dh.toFixed(2)}">${yamraj({ x: 540, y: 1250, s: 0.62, folded: true })}</g>`;
  w += `<circle cx="540" cy="900" r="${(200 + 300 * dh).toFixed(0)}" fill="url(#halo)" opacity="${(0.2 + 0.6 * dh).toFixed(2)}"/>`;
  BRO.forEach((n, i) => { const x = 140 + i * 260 + (i > 1 ? 0 : 0), y = 1620;
    w += `<g transform="translate(${x} ${y}) rotate(${(-88 * (1 - rise)).toFixed(1)}) translate(${-x} ${-y})">${pandav(n, { x, y, s: 0.42, eyes: rise > 0.6 ? 'open' : 'closed', ...armsFor(n) })}</g>`; });
  let s = cam(540, lerp(1300, 1260, seg(t, T0, at('आप होते'))), lerp(1.15, 1.2, seg(t, T0, at('आप होते'))), w);
  s += caps(t, [{ t0: T0, l1: 'YAKSHA PRASANN', l2: 'CHAARON JI UTHE', t2: at('चारों भाई जी'), acc: RED, ...LIGHT }, { t0: at('वो स्वयं'), l1: 'WOH SWAYAM', l2: 'DHARMRAJ THE', acc: RED, ...LIGHT, size: 110 }]);
  return s + flashRect(t, at('वो स्वयं') - 0.1, 0.4) + TAG();
}, 'flash');

// 7 THE QUESTION FOR THE VIEWER
add(at('आप होते'), 999, (t) => {
  const T0 = at('आप होते');
  let w = paperBg(t);
  ['bhima', 'arjun', 'nakul', 'sahdev'].forEach((n, i) => { w += pandav(n, { x: 150 + i * 260, y: 1500, s: 0.5, eyes: 'open', ...armsFor(n) }); });
  let s = cam(540, 1150, lerp(1.0, 1.05, seg(t, T0, T0 + 4)), w);
  ['BHIM', 'ARJUN', 'NAKUL', 'SAHDEV'].forEach((n, i) => { s += pill(t, T0 + 0.3 + i * 0.2, n, 150 + i * 260, 1560, { center: true, bg: i === 2 ? '#2E8A4E' : INK }); });
  s += caps(t, [{ t0: T0, l1: 'AAP HOTE,', l2: 'TOH KISE CHUNTE?', t2: T0 + 0.6, acc: RED, ...LIGHT, size: 110 }]);
  s += pill(t, T0 + 1.4, 'COMMENT MEIN BATAIYE', 540, 620, { center: true, bg: RED });
  s += pill(t, T0 + 2.0, 'FOLLOW · MAHABHARAT SERIES', 540, 690, { center: true });
  return s + TAG();
}, 'zoom');

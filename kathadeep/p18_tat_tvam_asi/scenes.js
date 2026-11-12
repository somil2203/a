// Tat Tvam Asi — Chandogya Upanishad 6.1 (Shvetaketu returns proud after his studies; "did you ask for that teaching by which
// the unheard becomes heard, the unknown known?") and 6.13 (salt in water: not seen, yet everywhere; "that subtle essence…
// that is the Self — tat tvam asi, Shvetaketu").
const DARK = { dark: false }, LIGHT = { dark: true };
const TAG = () => tagTR('UPANISHAD KI KAHANIYAAN · 2');
const rays = (cx, cy, n, op, t, col = '#FFF2C6') => [...Array(n)].map((_, i) => { const a = (i * 360 / n + t * 5) * Math.PI / 180, b = a + 0.12;
  return `<path d="M${cx} ${cy} L${(cx + Math.cos(a) * 2600).toFixed(0)} ${(cy + Math.sin(a) * 2600).toFixed(0)} L${(cx + Math.cos(b) * 2600).toFixed(0)} ${(cy + Math.sin(b) * 2600).toFixed(0)}Z" fill="${col}" opacity="${op}"/>`; }).join('');

// 0 HOOK — 12 years of study, silenced by one question
add(0, at('छांदोग्य'), (t) => {
  const c = camPath(t, [[0, 600, 1250, 1.1], [at('और पिता के'), 420, 1220, 1.35], [at('चुप हो'), 680, 1200, 1.5], [at('छांदोग्य'), 660, 1200, 1.55]]);
  let w = ashram(t) + rishi({ x: 330, y: 1700, s: 0.95, eyes: 'open', armR: -60, elbowR: -50, armL: 30 }) + youngScholar({ x: 760, y: 1700, s: 0.8, eyes: 'open', armL: 20, armR: -20 });
  let s = cam(...c, w);
  s += pill(t, 0.3, '12 SAAL KI PADHAI', 1022, 560, { right: true, bg: RED });
  s += caps(t, [{ t0: 0, l1: '12 SAAL PADHKAR', l2: 'EK SAWAAL PAR CHUP', t2: at('और पिता के'), acc: RED, ...LIGHT }]);
  return s + TAG();
});

// 1 THE PROUD SON
add(at('छांदोग्य'), at('पिता ने पूछा'), (t) => {
  let w = paperBg(t) + pothi(540, 860, 1.1, '', t) + youngScholar({ x: 540, y: 1640, s: 0.9, eyes: 'closed', armL: 40, elbowL: 80, armR: -40, elbowR: -80 });
  let s = cam(540, lerp(1100, 1200, seg(t, at('छांदोग्य'), at('पिता ने पूछा'))), lerp(1.0, 1.12, seg(t, at('छांदोग्य'), at('पिता ने पूछा'))), w);
  s += pill(t, at('छांदोग्य') + 0.3, 'CHHANDOGYA UPANISHAD · 6', 540, 1010, { center: true });
  s += caps(t, [{ t0: at('छांदोग्य'), l1: 'UDDALAK KA BETA', l2: 'SHVETAKETU', t2: at('ऋषि उद्दालक') + 1.0, acc: RED, ...LIGHT }, { t0: at('और घमंड'), l1: 'SAARE VED PADHE...', l2: 'AUR GHAMAND', acc: RED, ...LIGHT }]);
  s += stamp2(t, at('और घमंड') + 0.4, 'GHAMAND', 760, 1480, { rot: 8 });
  return s + TAG();
}, 'push');

// 2 THE QUESTION
add(at('पिता ने पूछा'), at('पिता बोले — इस'), (t) => {
  let w = ashram(t) + rishi({ x: 330, y: 1700, s: 0.95, eyes: 'open', armR: -100, elbowR: -20, armL: 30 }) + youngScholar({ x: 760, y: 1700, s: 0.8, eyes: t > at('श्वेतकेतु बोला') ? 'closed' : 'open', armL: 20, armR: -20 });
  let s = cam(540, 1250, lerp(1.0, 1.1, seg(t, at('पिता ने पूछा'), at('पिता बोले — इस'))), w);
  s += caps(t, [{ t0: at('पिता ने पूछा'), l1: 'JISSE ANSUNA', l2: 'SUNAAI DE?', t2: at('जिससे अनसुना') + 0.6, acc: RED, ...LIGHT }, { t0: at('और अनजाना'), l1: 'AUR ANJAANA', l2: 'JAANA JAAYE?', acc: RED, ...LIGHT },
    { t0: at('श्वेतकेतु बोला'), l1: '"NAHI.', l2: 'AAP HI SIKHAAIYE."', t2: at('आप ही'), acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'fade');

// 3 THE SALT — dissolved overnight; then: taste from the top, the middle, the bottom
add(at('पिता बोले — इस'), at('पिता बोले — दिखता'), (t) => {
  const night = seg(t, at('और सुबह') - 0.2, at('सुबह बोले'));
  const dis = eo(seg(t, at('इस पानी') + 0.5, at('सुबह बोले')));
  const dips = [[0.05, eo(seg(t, at('ऊपर से') + 0.3, at('ऊपर से') + 0.8))], [0.5, eo(seg(t, at('बीच से'), at('बीच से') + 0.5))], [0.92, eo(seg(t, at('नीचे से'), at('नीचे से') + 0.5))]];
  let w = (night > 0 && night < 1 ? bg('night') + stars(t, 40) : paperBg(t)) + saltGlass(540, 1650, 1.25, t, dis, dips);
  if (t > at('ऊपर से') - 0.2) [['KHAARA', at('ऊपर से') + 0.6, 1060], ['KHAARA', at('बीच से') + 0.3, 1310], ['KHAARA', at('नीचे से') + 0.3, 1560]].forEach(([tx, t0, y]) => { w += pill(t, t0, tx, 880, y, { bg: RED }); });
  let s = cam(540, lerp(1250, 1300, seg(t, at('पिता बोले — इस'), at('पिता बोले — दिखता'))), lerp(1.0, 1.08, seg(t, at('पिता बोले — इस'), at('पिता बोले — दिखता'))), w);
  s += caps(t, [{ t0: at('पिता बोले — इस'), l1: 'PAANI MEIN', l2: 'NAMAK DAALO', acc: RED, ...LIGHT }, { t0: at('सुबह बोले'), l1: '"AB NAMAK', l2: 'NIKAALO."', acc: RED, ...LIGHT }, { t0: at('नमक दिखा'), l1: 'NAMAK', l2: 'DIKHA HI NAHI', acc: RED, ...LIGHT },
    { t0: at('ऊपर से'), l1: 'UPAR · BEECH · NEECHE', l2: 'HAR JAGAH KHAARA', t2: at('नीचे से') + 0.4, acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'zoom');

// 4 "UNSEEN, YET IN EVERY DROP" — the subtle truth in the whole world
add(at('पिता बोले — दिखता'), at('वही सत्य'), (t) => {
  const world = eo(seg(t, at('वैसे ही'), at('इस पूरे') + 0.8));
  let w = `<rect x="-300" y="-300" width="1700" height="2600" fill="#0B0620"/>` + stars(t, 80);
  w += `<g opacity="${(1 - world).toFixed(2)}">${saltGlass(540, 1650, 1.25, t, 1, [])}</g>`;
  w += `<g opacity="${world.toFixed(2)}">${cosmos(540, 1150, lerp(200, 440, world), t, { aakash: 1, prithvi: 1, samudra: 1, parvat: 1, dweep: 1, taare: 1 })}</g>`;
  for (let i = 0; i < 40; i++) { const ph = (t * 0.3 + rnd(i)) % 1; w += `<circle cx="${(rnd(i + 2) * 1080).toFixed(0)}" cy="${(1900 - ph * 1500).toFixed(0)}" r="${(2 + rnd(i) * 4).toFixed(1)}" fill="#FFF6DA" opacity="${(0.7 * Math.sin(ph * Math.PI)).toFixed(2)}"/>`; }
  let s = cam(540, 1200, lerp(1.0, 1.06, seg(t, at('पिता बोले — दिखता'), at('वही सत्य'))), w);
  s += caps(t, [{ t0: at('पिता बोले — दिखता'), l1: 'DIKHTA NAHI...', l2: 'PAR HAR BOOND MEIN', t2: at('पर हर बूँद'), acc: GOLDT, ...DARK }, { t0: at('वैसे ही'), l1: 'EK SOOKSHM SATYA', l2: 'POORE JAGAT MEIN', t2: at('इस पूरे'), acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'fade');

// 5 TAT TVAM ASI
add(at('वही सत्य'), at('उपनिषद की अगली'), (t) => {
  const k = eo(seg(t, at('तत् त्वम्') - 0.1, at('तत् त्वम्') + 0.6));
  let w = bg('gold') + rays(540, 1100, 22, 0.14, t) + `<circle cx="540" cy="1250" r="460" fill="url(#halo)"/>` + youngScholar({ x: 540, y: 1800, s: 0.95, eyes: 'closed', armL: 38, elbowL: -112, armR: -38, elbowR: 112 });
  let s = cam(540, 1250, lerp(1.1, 1.0, seg(t, at('वही सत्य'), at('उपनिषद की अगली'))), w);
  if (k > 0) s += `<g opacity="${k.toFixed(2)}" transform="translate(540 1000) scale(${lerp(0.8, 1, back(k)).toFixed(3)})"><text text-anchor="middle" font-family="Baloo" font-weight="800" font-size="150" fill="#4A1A08">तत् त्वम् असि</text><text y="80" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="28" fill="#4A1A08" letter-spacing="3">CHHANDOGYA UPANISHAD 6.8.7</text></g>`;
  s += caps(t, [{ t0: at('वही सत्य'), l1: 'WAHI SATYA', l2: 'WAHI AATMA', t2: at('वही आत्मा'), acc: RED, ...LIGHT }, { t0: at('वो तुम हो'), l1: 'WOH', l2: 'TUM HO.', acc: RED, ...LIGHT, size: 130 }]);
  s += flashRect(t, at('तत् त्वम्'), 0.35, '#FFF6E0');
  return s + TAG();
}, 'iris');

// 6 NEXT — a woman questions the greatest sage in the king's court
add(at('उपनिषद की अगली'), 999, (t) => {
  let w = sabha(t) + gargi({ x: 420, y: 1720, s: 0.95, t, armR: -120, elbowR: -20, armL: 30 }) + rishi({ x: 800, y: 1720, s: 0.8, eyes: 'open', armL: 30, armR: -30 });
  let s = cam(540, 1250, lerp(1.1, 1.0, seg(t, at('उपनिषद की अगली'), at('उपनिषद की अगली') + 6)), w);
  s += caps(t, [{ t0: at('उपनिषद की अगली'), l1: 'AGLI KAHANI', ...DARK }, { t0: at('जब एक स्त्री'), l1: 'EK STREE NE', l2: 'RAJA KI SABHA MEIN SAWAAL KIYE', t2: at('राजा की सभा'), acc: GOLDT, ...DARK }]);
  s += pill(t, at('सबसे बड़े') + 1.2, 'FOLLOW · UPANISHAD SERIES', 540, 1450, { center: true, bg: RED });
  return s + TAG();
}, 'whip');

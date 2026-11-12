// Indra and Virochana — Chandogya Upanishad 8.7-8.12: Prajapati's declaration about the Self; Indra (devas) and Virochana
// (asuras) live 32 years as students; "look into a pan of water"; adorned, they see their adorned bodies; Virochana leaves
// content (body = self) and teaches the asuras; Indra doubts on the way and returns: 32 + 32 + 5 more years — 101 in all.
const DARK = { dark: false }, LIGHT = { dark: true };
const TAG = () => tagTR('UPANISHAD KI KAHANIYAAN · 4');
const rays = (cx, cy, n, op, t, col = '#FFF2C6') => [...Array(n)].map((_, i) => { const a = (i * 360 / n + t * 5) * Math.PI / 180, b = a + 0.12;
  return `<path d="M${cx} ${cy} L${(cx + Math.cos(a) * 2600).toFixed(0)} ${(cy + Math.sin(a) * 2600).toFixed(0)} L${(cx + Math.cos(b) * 2600).toFixed(0)} ${(cy + Math.sin(b) * 2600).toFixed(0)}Z" fill="${col}" opacity="${op}"/>`; }).join('');
const yrs = (t, n, x = 1022, y = 560) => pill(t, 0, `${n} SAAL`, x, y, { right: true, bg: n >= 101 ? '#2E8A4E' : RED });

// 0 HOOK — 101 years for one answer
add(0, at('छांदोग्य'), (t) => {
  const n = Math.round(lerp(1, 101, eo(seg(t, 0.2, at('छांदोग्य') - 0.3))));
  let w = `<rect x="-300" y="-300" width="1700" height="2600" fill="#1A1030"/>` + stars(t, 70) + rays(540, 1150, 20, 0.06, t);
  w += `<text x="540" y="1020" text-anchor="middle" font-family="${ANTON}" font-size="360" fill="#FFE29A" opacity=".9" stroke="#14060A" stroke-width="14" paint-order="stroke">${n}</text><text x="540" y="1100" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="40" fill="#FFF3DC" letter-spacing="8">SAAL</text>`;
  w += indra({ x: 540, y: 1880, s: 0.55, eyes: 'closed', folded: true });
  let s = cam(540, 1200, lerp(1.15, 1.0, seg(t, 0, at('छांदोग्य'))), w);
  s += caps(t, [{ t0: 0, l1: 'EK SAWAAL KA JAWAAB', l2: '101 SAAL!', t2: at('इंद्र को एक'), acc: GOLDT, ...DARK }]);
  return s + TAG();
});

// 1 PRAJAPATI: whoever knows the Self obtains everything — devas send Indra, asuras send Virochana
add(at('छांदोग्य'), at('प्रजापति बोले'), (t) => {
  const two = eo(seg(t, at('देवों ने') - 0.1, at('असुरों ने विरोचन') + 0.5));
  let w = bg('sky') + cloud(300, 1560, 1.6) + cloud(800, 1580, 1.5) + brahma({ x: 540, y: 1260, s: 0.7, t, glow: 0.5 });
  w += `<g opacity="${two.toFixed(2)}">${indra({ x: 260, y: 1820, s: 0.62, eyes: 'open', folded: true })}${virochan({ x: 820, y: 1820, s: 0.62, folded: true, eyes: 'open' })}</g>`;
  let s = cam(540, 1300, lerp(1.0, 1.06, seg(t, at('छांदोग्य'), at('प्रजापति बोले'))), w);
  s += pill(t, at('छांदोग्य') + 0.3, 'CHHANDOGYA UPANISHAD · 8.7', 60, 560);
  s += pill(t, at('देवों ने') + 0.3, 'DEV: INDRA', 120, 1500) + pill(t, at('असुरों ने विरोचन') + 0.3, 'ASUR: VIROCHAN', 640, 1500);
  s += yrs(t, Math.round(lerp(0, 32, seg(t, at('बत्तीस साल, दोनों'), at('प्रजापति बोले') - 0.2))));
  s += caps(t, [{ t0: at('प्रजापति ने कहा'), l1: 'JO AATMA JAANE', l2: 'USE SAB MILE', t2: at('उसे सब'), acc: RED, ...LIGHT }, { t0: at('देवों ने'), l1: 'INDRA', l2: 'VS VIROCHAN', t2: at('असुरों ने विरोचन'), acc: RED, ...LIGHT },
    { t0: at('बत्तीस साल, दोनों'), l1: '32 SAAL', l2: 'SEVA', acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'push');

// 2 THE WATER BOWL — they see their own adorned bodies
add(at('प्रजापति बोले'), at('विरोचन संतुष्ट'), (t) => {
  const look = t > at('दोनों ने सज') - 0.1;
  const refl = look ? `<g transform="translate(-90 0) scale(.16)">${indra({ x: 0, y: 0, s: 1, eyes: 'closed' })}</g><g transform="translate(90 0) scale(.16)">${virochan({ x: 0, y: 0, s: 1, eyes: 'closed' })}</g>` : '';
  let w = bg('dawn') + `<rect x="-300" y="1500" width="1700" height="900" fill="#C9955A"/>` + waterBowl(540, 1620, 1.2, t, refl);
  w += indra({ x: 220, y: 1720, s: 0.62, eyes: 'open', armL: 30, armR: -30 }) + virochan({ x: 860, y: 1720, s: 0.62, eyes: 'open', armL: 30, armR: -30 });
  const dr = seg(t, at('प्रजापति बोले'), at('दोनों ने सज')), dl = seg(t, at('दोनों ने सज'), at('विरोचन संतुष्ट'));
  const c = look ? [540 + 40 * Math.sin(dl * Math.PI), lerp(1540, 1600, dl), 1.5 + 0.2 * dl] : [540, lerp(1280, 1380, dr), 1.0 + 0.15 * dr];
  let s = cam(...c, w);
  s += caps(t, [{ t0: at('प्रजापति बोले'), l1: '"PAANI MEIN DEKHO.', l2: 'JO DIKHE, WAHI AATMA."', t2: at('जो दिखे'), acc: RED, ...LIGHT }, { t0: at('दोनों ने सज'), l1: 'SAJ-DHAJKAR DEKHA', l2: 'SHAREER DIKHA', t2: at('अपना ही'), acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'zoom');

// 3 VIROCHANA LEAVES SATISFIED — "the body is the Self" — and teaches the asuras
add(at('विरोचन संतुष्ट'), at('पर इंद्र'), (t) => {
  let w = bg('rage') + `<rect x="-300" y="1500" width="1700" height="900" fill="#3A0A12"/>` + virochan({ x: 540, y: 1720, s: 0.9, eyes: 'closed', armR: -120, elbowR: -20, armL: 30, laugh: true });
  const crowd = eo(seg(t, at('और असुरों') - 0.1, at('और असुरों') + 0.6));
  for (let i = 0; i < 6; i++) w += `<g opacity="${crowd.toFixed(2)}">${gwala2({ x: 100 + i * 180, y: 1900, s: 0.45, top: '#6E1F1F', skin: '#9A6A5A' })}</g>`;
  let s = cam(540, 1300, lerp(1.0, 1.08, seg(t, at('विरोचन संतुष्ट'), at('पर इंद्र'))), w);
  s += stamp2(t, at('शरीर ही आत्मा') + 0.2, 'SHAREER = AATMA?', 540, 1000, { rot: -6 });
  s += caps(t, [{ t0: at('विरोचन संतुष्ट'), l1: 'VIROCHAN', l2: 'SANTUSHT LAUTA', acc: '#FF5A4A', ...DARK }, { t0: at('और असुरों'), l1: 'ASURON KO', l2: 'YAHI SIKHAAYA', acc: '#FF5A4A', ...DARK }]);
  return s + TAG();
}, 'whip');

// 4 INDRA DOUBTS ON THE WAY — the body ages and dies
add(at('पर इंद्र'), at('वो लौटे'), (t) => {
  const age = seg(t, at('शरीर तो'), at('मरता है') + 0.4);
  let w = bg('dusk') + `<rect x="-300" y="1500" width="1700" height="900" fill="#8E5A3A"/>` + `<path d="M-300 1560 C300 1520 800 1600 1400 1540" stroke="#C9955A" stroke-width="60" fill="none"/>`;
  w += `<g opacity="${(1 - 0.5 * age).toFixed(2)}">${indra({ x: 540, y: 1720, s: 0.95, eyes: 'open', armR: -60, elbowR: -100, armL: 30 })}</g>`;
  let s = cam(540, 1250, lerp(1.0, 1.15, seg(t, at('पर इंद्र'), at('वो लौटे'))), w);
  s += caps(t, [{ t0: at('पर इंद्र'), l1: 'PAR INDRA', l2: 'RAASTE MEIN RUKE', acc: GOLDT, ...DARK }, { t0: at('शरीर तो'), l1: 'SHAREER BOODHA HOTA', l2: 'MARTA HAI', t2: at('मरता है'), acc: '#FF5A4A', ...DARK }, { t0: at('ये आत्मा कैसे'), l1: 'YE AATMA', l2: 'KAISE?', acc: GOLDT, ...DARK, size: 120 }]);
  return s + TAG();
}, 'fade');

// 5 HE RETURNS — 32 + 32 + 5 more — 101 years
add(at('वो लौटे'), at('जवाब जल्दी'), (t) => {
  const n = t < at('फिर बत्तीस साल') ? 32 : t < at('फिर बत्तीस।') ? Math.round(lerp(32, 64, seg(t, at('फिर बत्तीस साल'), at('फिर बत्तीस।')))) : t < at('फिर पाँच') ? Math.round(lerp(64, 96, seg(t, at('फिर बत्तीस।'), at('फिर पाँच')))) : Math.round(lerp(96, 101, seg(t, at('फिर पाँच'), at('कुल एक सौ'))));
  const know = eo(seg(t, at('तब जाना') - 0.2, at('जो इसमें') + 0.6));
  let w = `<rect x="-300" y="-300" width="1700" height="2600" fill="#1A1030"/>` + stars(t, 60) + rays(540, 1100, 20, 0.04 + 0.1 * know, t) + `<circle cx="540" cy="1200" r="${(200 + 400 * know).toFixed(0)}" fill="url(#halo)" opacity="${(0.25 + 0.5 * know).toFixed(2)}"/>`;
  w += brahma({ x: 770, y: 1700, s: 0.55, t, glow: 0.4 }) + indra({ x: 320, y: 1920, s: 0.7, eyes: 'closed', folded: true });
  let s = cam(540, 1250, 1.0, w);
  s += `<text x="540" y="790" text-anchor="middle" font-family="${ANTON}" font-size="210" fill="#FFE29A" stroke="#14060A" stroke-width="10" paint-order="stroke" opacity="${(1 - know * 0.8).toFixed(2)}">${n}</text><text x="540" y="850" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="30" fill="#FFF3DC" letter-spacing="6" opacity="${(1 - know * 0.8).toFixed(2)}">32 + 32 + 32 + 5</text>`;
  s += caps(t, [{ t0: at('वो लौटे'), l1: 'WOH LAUTE', ...DARK }, { t0: at('कुल एक सौ'), l1: 'KUL 101 SAAL', acc: GOLDT, ...DARK }, { t0: at('तब जाना'), l1: 'SHAREER NAHI...', l2: 'JO DEKHTA HAI, WAHI AATMA', t2: at('जो इसमें'), acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'fade');

// 6 THE QUESTION FOR US
add(at('जवाब जल्दी'), 999, (t) => {
  let w = paperBg(t) + `<g opacity=".95">${virochan({ x: 300, y: 1880, s: 0.75, eyes: 'closed', laugh: true, armL: 20, armR: -20 })}${indra({ x: 780, y: 1880, s: 0.75, eyes: 'closed', folded: true })}</g>`;
  let s = cam(540, 1060, lerp(1.0, 1.06, seg(t, at('जवाब जल्दी'), at('जवाब जल्दी') + 7)), w);
  s += strikeList(t, 60, 760, [['JALDI WAALA JAWAAB?', at('कहीं वो') - 0.2, at('कहीं वो') + 1.6], ['RUKKAR SOCHA JAWAAB', at('कहीं वो') + 2.0, null]]);
  s += caps(t, [{ t0: at('जवाब जल्दी'), l1: 'JAWAAB JALDI MILE...', l2: 'TOH RUKKAR SOCHIYE', t2: at('तो रुककर'), acc: RED, ...LIGHT }]);
  s += pill(t, at('कहीं वो') + 2.6, 'FOLLOW · UPANISHAD SERIES', 540, 1450, { center: true, bg: RED });
  return s + TAG();
}, 'zoom');

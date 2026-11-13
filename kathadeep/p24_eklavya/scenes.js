// Eklavya — Mahabharata, Adi Parva: the Nishada prince is refused by Drona; he makes a clay image of Drona in the forest and
// practises before it; the Pandavas' dog barks and he fills its mouth with seven arrows without hurting it; Arjuna, promised by
// Drona that no pupil would surpass him, is dismayed; Drona goes to Eklavya, who calls him his guru; Drona asks for the right
// thumb as guru-dakshina and Eklavya cuts it off without hesitation. (Shown without gore: a flash and an offering on a leaf.)
const DARK = { dark: false }, LIGHT = { dark: true };
const TAG = () => tagTR('MAHABHARAT KI KAHANIYAAN');
const target = (x, y, s, hits = 0) => G2(x, y, s, `<circle r="90" fill="#F4EBDD" stroke="#5A2E14" stroke-width="8"/><circle r="62" fill="#D6332A"/><circle r="36" fill="#F4EBDD"/><circle r="14" fill="#D6332A"/>
  ${[...Array(Math.min(hits, 6))].map((_, i) => `<g transform="rotate(${-160 + i * 6})"><rect x="${(i % 3) * 4}" y="-3" width="120" height="6" fill="#7A4A22"/><path d="M120 0 l18 -11 l-6 11 l6 11z" fill="#D6332A"/></g>`).join('')}`);
const nightForest = (t, k = 0.35) => forest(t, k);

// 0 HOOK — the guru asks for the thumb; the pupil gives it gladly
add(0, at('महाभारत'), (t) => {
  let w = nightForest(t, 0.45) + `<circle cx="540" cy="1250" r="420" fill="url(#halo)" opacity=".45"/>`;
  w += drona({ x: 270, y: 1640, s: 0.6, eyes: 'open', armR: -70, elbowR: -50 }) + eklavya({ x: 800, y: 1640, s: 0.9, armL: 60, elbowL: 40, armR: -60, elbowR: -50, flip: true });
  w += leafPlate(540, 1480, 0.55, 0.6 + 0.2 * Math.sin(t * 3));
  let s = cam(540, lerp(1300, 1340, seg(t, 0, 6)), lerp(1.3, 1.2, eo(seg(t, 0, 6))), w);
  s += stamp2(t, at('और शिष्य ने') + 0.4, 'GURU DAKSHINA', 540, 1460, { rot: -6, col: GOLDT });
  s += caps(t, [{ t0: -0.6, l1: 'GURU NE MAANGA', l2: 'SHISHYA KA ANGOOTHA', t2: -0.5, acc: GOLDT, ...DARK }, { t0: at('और शिष्य ने'), l1: 'SHISHYA NE', l2: 'KHUSHI-KHUSHI DE DIYA', t2: at('और शिष्य ने') + 0.8, acc: GOLDT, ...DARK }]);
  return s + TAG();
});

// 1 THE ASHRAM — the Nishada prince asks; Drona refuses
add(at('महाभारत'), at('एकलव्य ने जंगल'), (t) => {
  const T0 = at('महाभारत'), no = t > at('द्रोण ने मना') - 0.1;
  const walk = eo(seg(t, at('निषाद') - 0.3, at('द्रोणाचार्य से') + 0.5));
  let w = bg('day') + `<rect x="-300" y="1380" width="1700" height="900" fill="#C9A86A"/>` + tree2(-30, 1400, 2.2, Math.sin(t) * 2) + tree2(1110, 1400, 2.2, Math.sin(t + 1) * 2) + target(900, 1220, 0.8, 4);
  w += pandav('arjun', { x: 680, y: 1640, s: 0.42, eyes: 'open', armR: -20, elbowR: -10 }) + pandav('bhima', { x: 840, y: 1660, s: 0.42, eyes: 'open', armR: -150, elbowR: -10 });
  w += drona({ x: 420, y: 1660, s: 0.55, eyes: 'open', armR: no ? -150 : -20, elbowR: no ? 10 : -10 });
  w += eklavya({ x: lerp(-200, 180, walk), y: 1680, s: 0.8, armL: 30, elbowL: 20, armR: -30, elbowR: -20, bow: true });
  let s = `<g transform="${shake(t, at('द्रोण ने मना'), 0.4, 10)}">${cam(lerp(480, 520, seg(t, T0, at('एकलव्य ने जंगल'))), 1360, lerp(1.2, 1.28, seg(t, T0, at('एकलव्य ने जंगल'))), w)}</g>`;
  s += pill(t, T0 + 0.3, 'MAHABHARAT · AADI PARVA', 60, 560);
  s += stamp2(t, at('द्रोण ने मना') + 0.3, 'MANAA', 760, 900, { rot: -8 });
  s += caps(t, [{ t0: at('निषाद'), l1: 'NISHAD RAJKUMAR', l2: 'EKLAVYA', acc: '#2E8A4E', ...LIGHT }, { t0: at('द्रोणाचार्य से'), l1: 'DRONACHARYA SE', l2: 'DHANURVIDYA SEEKHNE AAYA', t2: at('द्रोणाचार्य से') + 1.2, acc: RED, ...LIGHT },
    { t0: at('द्रोण ने मना'), l1: 'DRONA NE', l2: 'MANA KAR DIYA', acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'push');

// 2 THE CLAY GURU — he practises before the image
add(at('एकलव्य ने जंगल'), at('एक दिन'), (t) => {
  const T0 = at('एकलव्य ने जंगल'), form = eo(seg(t, at('मिट्टी से') - 0.2, at('और उसी') - 0.4)), prac = t > at('और उसी');
  const hits = prac ? Math.floor((t - at('और उसी')) / 0.45) : 0, draw = prac ? 0.5 + 0.5 * Math.abs(Math.sin((t - at('और उसी')) * 7)) : 0;
  let w = forest(t) + target(930, 1280, 0.9, hits);
  w += `<g opacity="${form.toFixed(2)}" transform="translate(0 ${((1 - form) * 40).toFixed(0)})">${clayIdol(250, 1640, 0.5, prac ? 0.35 : 0.15)}</g>`;
  w += eklavya({ x: 560, y: 1680, s: 0.9, bow: prac, arrow: prac, draw, armR: prac ? -90 : -40, elbowR: prac ? -2 : -30, armL: prac ? 80 : 30, elbowL: prac ? 20 : 20 });
  let s = cam(lerp(560, 600, seg(t, T0, at('एक दिन'))), 1380, lerp(1.2, 1.26, seg(t, T0, at('एक दिन'))), w);
  s += caps(t, [{ t0: T0, l1: 'JANGAL MEIN', l2: 'MITTI KI MOORTI', t2: at('मिट्टी से'), acc: '#FFC48A', ...DARK }, { t0: at('और उसी'), l1: 'USI KO GURU MAANKAR', l2: 'ABHYAAS', acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'fade');

// 3 THE DOG — seven arrows fill its mouth, not a scratch
add(at('एक दिन'), at('अर्जुन हैरान'), (t) => {
  const T0 = at('एक दिन'), shot = seg(t, at('सात बाण') - 0.6, at('सात बाण') + 0.9);
  let w = forest(t) + dog(330, 1660, 0.95, t, { bark: t < at('सात बाण') - 0.6, arrows: shot });
  w += eklavya({ x: 900, y: 1680, s: 0.85, bow: true, arrow: shot < 1, draw: shot > 0 && shot < 1 ? 1 : 0.3, armR: -90, elbowR: -2, armL: 80, elbowL: 20, flip: true });
  let s = cam(540, lerp(1380, 1400, seg(t, T0, at('अर्जुन हैरान'))), lerp(1.2, 1.3, seg(t, at('एकलव्य ने उसके'), at('अर्जुन हैरान'))), w);
  if (t > at('सात बाण')) s += `<text x="${540 + (330 - 540) * 1.25 + 40}" y="980" text-anchor="middle" font-family="${ANTON}" font-size="150" fill="${GOLDT}" stroke="${INK}" stroke-width="8" paint-order="stroke">${Math.max(1, Math.min(7, Math.ceil(shot * 7)))}</text>`;
  s += stamp2(t, at('और कुत्ते') + 0.6, 'CHOT: ZERO', 540, 1330, { rot: -7, col: '#2E7A4E' });
  s += caps(t, [{ t0: T0, l1: 'PANDAVON KA KUTTA', l2: 'BHAUNKA', t2: T0 + 1.6, acc: GOLDT, ...DARK }, { t0: at('एकलव्य ने उसके'), l1: 'MUNH MEIN', l2: '7 BAAN', t2: at('सात बाण'), acc: GOLDT, ...DARK, size: 110 },
    { t0: at('और कुत्ते'), l1: 'AUR CHOT', l2: 'TAK NAHI LAGI', acc: '#8CFFA8', ...DARK }]);
  return s + TAG();
}, 'whip');

// 4 ARJUNA IS DISMAYED — the promise
add(at('अर्जुन हैरान'), at('द्रोण पहुँचे'), (t) => {
  const T0 = at('अर्जुन हैरान');
  let w = bg('day') + `<rect x="-300" y="1380" width="1700" height="900" fill="#C9A86A"/>` + tree2(-30, 1400, 2.2, Math.sin(t) * 2) + tree2(1110, 1400, 2.2, Math.sin(t + 1) * 2);
  w += pandav('arjun', { x: 300, y: 1680, s: 0.62, eyes: 'open', armR: -60, elbowR: -70 }) + dog(760, 1680, 0.7, t, { arrows: 1, flip: true });
  let s = cam(lerp(520, 560, seg(t, T0, at('द्रोण पहुँचे'))), 1400, lerp(1.2, 1.28, seg(t, T0, at('द्रोण पहुँचे'))), w);
  const k = eo(seg(t, at('गुरुदेव ने'), at('गुरुदेव ने') + 0.4));
  if (k > 0) s += `<g opacity="${k.toFixed(2)}" transform="translate(${(1 - k) * -30} 0)">${paper(60, 600, 960, 250, -1.5, `<text x="40" y="70" font-family="SpaceMono" font-weight="700" font-size="30" fill="${RED}" letter-spacing="2">DRONA KA VACHAN:</text><text x="40" y="150" font-family="${ANTON}" font-size="66" fill="${INK}">"TUMSE BADA DHANURDHAR</text><text x="40" y="222" font-family="${ANTON}" font-size="66" fill="${INK}">KOI NAHI HOGA"</text>`, { tape: true })}</g>`;
  s += caps(t, [{ t0: T0, l1: 'ARJUN', l2: 'HAIRAAN', acc: RED, ...LIGHT, size: 120, te: at('गुरुदेव ने') - 0.2 }]);
  return s + TAG();
}, 'fade');

// 5 DRONA ARRIVES — "you are my guru"
add(at('द्रोण पहुँचे'), at('द्रोण बोले'), (t) => {
  const T0 = at('द्रोण पहुँचे'), walk = eo(seg(t, T0 - 0.2, T0 + 1.4));
  let w = forest(t, 0.15) + clayIdol(540, 1600, 0.42, 0.3);
  w += drona({ x: lerp(-100, 220, walk), y: 1680, s: 0.6, eyes: 'open' }) + eklavya({ x: 850, y: 1690, s: 0.9, armL: 60, elbowL: 40, armR: -60, elbowR: -50, flip: true });
  let s = cam(540, 1400, lerp(1.2, 1.27, seg(t, T0, at('द्रोण बोले'))), w);
  s += caps(t, [{ t0: T0, l1: 'DRONA', l2: 'PAHUNCHE', acc: GOLDT, ...DARK }, { t0: at('एकलव्य बोला'), l1: '"AAP HI MERE', l2: 'GURU HAIN"', t2: at('आप ही'), acc: '#8CFFA8', ...DARK, size: 110 }]);
  return s + TAG();
}, 'fade');

// 6 THE DAKSHINA — the right thumb; given without a pause
add(at('द्रोण बोले'), at('अब आप'), (t) => {
  const T0 = at('द्रोण बोले'), give = eo(seg(t, at('काटकर') + 0.1, at('काटकर') + 0.8));
  let w = nightForest(t, 0.5) + `<circle cx="540" cy="1300" r="${(300 + 200 * give).toFixed(0)}" fill="url(#halo)" opacity="${(0.3 + 0.4 * give).toFixed(2)}"/>`;
  w += drona({ x: 260, y: 1660, s: 0.6, eyes: 'open', armR: -70, elbowR: -50 }) + eklavya({ x: 800, y: 1680, s: 0.9, armL: 60, elbowL: 40, armR: -60, elbowR: -50, flip: true });
  w += `<g opacity="${give.toFixed(2)}">${leafPlate(540, 1500, 0.55, 0.7)}</g>`;
  const z = t < at('एकलव्य ने बिना') ? lerp(1.2, 1.32, seg(t, T0, at('एकलव्य ने बिना'))) : lerp(1.32, 1.22, seg(t, at('एकलव्य ने बिना'), at('अब आप')));
  let s = cam(540, 1360, z, w);
  s += stamp2(t, at('काटकर') + 0.7, 'GURU DAKSHINA', 540, 1440, { rot: -6, col: GOLDT });
  s += caps(t, [{ t0: T0, l1: '"TOH GURU DAKSHINA DO:', l2: 'DAAYEN HAATH KA ANGOOTHA"', t2: at('दाएँ हाथ'), acc: '#FF5A4A', ...DARK }, { t0: at('एकलव्य ने बिना'), l1: 'BINA RUKE', l2: 'KAATKAR RAKH DIYA', t2: at('काटकर'), acc: GOLDT, ...DARK }]);
  return s + flashRect(t, at('काटकर'), 0.5, '#FFFFFF') + TAG();
}, 'zoom');

// 7 THE QUESTION FOR THE VIEWER
add(at('अब आप'), 999, (t) => {
  const T0 = at('अब आप');
  let w = paperBg(t) + drona({ x: 280, y: 1560, s: 0.55, eyes: 'open' }) + eklavya({ x: 800, y: 1580, s: 0.85, armL: 30, elbowL: 20, armR: -30, elbowR: -20, flip: true, bow: true });
  let s = cam(540, 1180, lerp(1.0, 1.05, seg(t, T0, T0 + 5)), w);
  s += caps(t, [{ t0: T0, l1: 'GURU SAHI THE,', l2: 'YA NAHI?', t2: at('सही थे') + 0.5, acc: RED, ...LIGHT, size: 110 }]);
  s += pill(t, at('सही थे') + 1.0, 'A: VACHAN NIBHAYA', 60, 620, { bg: '#2E7A4E' }) + pill(t, at('सही थे') + 1.3, 'B: ANYAAY HUA', 60, 690, { bg: RED });
  s += pill(t, at('सही थे') + 1.8, 'COMMENT MEIN A YA B', 60, 760) + pill(t, at('सही थे') + 2.3, 'FOLLOW · MAHABHARAT SERIES', 540, 1500, { center: true });
  return s + TAG();
}, 'zoom');

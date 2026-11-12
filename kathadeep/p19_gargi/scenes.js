// Gargi and Yajnavalkya — Brihadaranyaka Upanishad 3.1 (Janaka sets apart a thousand cows with gold on their horns for the
// best knower of Brahman; Yajnavalkya tells his pupil to drive them home; the assembly questions him), 3.6 (Gargi: "on what is
// water woven?"… "Gargi, do not ask too far, lest your head fall off"), 3.8 (Gargi returns "like a warrior with two arrows";
// "across what are past, present and future woven?" — the Akshara, the imperishable; Gargi tells the assembly none can defeat him).
const DARK = { dark: false }, LIGHT = { dark: true };
const TAG = () => tagTR('UPANISHAD KI KAHANIYAAN · 3');
const rays = (cx, cy, n, op, t, col = '#FFF2C6') => [...Array(n)].map((_, i) => { const a = (i * 360 / n + t * 5) * Math.PI / 180, b = a + 0.12;
  return `<path d="M${cx} ${cy} L${(cx + Math.cos(a) * 2600).toFixed(0)} ${(cy + Math.sin(a) * 2600).toFixed(0)} L${(cx + Math.cos(b) * 2600).toFixed(0)} ${(cy + Math.sin(b) * 2600).toFixed(0)}Z" fill="${col}" opacity="${op}"/>`; }).join('');
const herd = (t, n = 12) => { let w = ''; for (let i = 0; i < n; i++) w += cow2({ x: 90 + (i % 6) * 190, y: 1520 + Math.floor(i / 6) * 120, s: 0.34, t, flip: i % 2 === 0, cloth: true }); return w; };

// 0 HOOK — a thousand cows with gold on their horns, and a woman stands up
add(0, at('बृहदारण्यक'), (t) => {
  const her = eo(seg(t, at('और एक स्त्री') - 0.2, at('और एक स्त्री') + 0.6));
  const c = camPath(t, [[0, 540, 1380, 1.5], [at('हर सींग'), 420, 1400, 1.9], [at('और एक स्त्री'), 540, 1250, 1.0], [at('बृहदारण्यक'), 540, 1250, 1.08]]);
  let w = sabha(t) + herd(t) + `<g opacity="${her.toFixed(2)}" transform="translate(0 ${(60 * (1 - her)).toFixed(0)})">${gargi({ x: 540, y: 1420, s: 0.8, t, armR: -120, elbowR: -20, armL: 30 })}</g>`;
  let s = cam(...c, w);
  s += pill(t, 0.3, '1000 GAAYEIN', 1022, 560, { right: true, bg: RED });
  s += caps(t, [{ t0: 0, l1: '1000 GAAYEIN', l2: 'HAR SEENG PAR SONA', t2: at('हर सींग'), acc: GOLDT, ...DARK }, { t0: at('और एक स्त्री'), l1: 'AUR EK STREE', l2: 'KHADI HUI...', acc: GOLDT, ...DARK }]);
  return s + TAG();
});

// 1 JANAKA'S CHALLENGE — Yajnavalkya: "drive them home" — the assembly erupts
add(at('बृहदारण्यक'), at('फिर उठीं — गार्गी'), (t) => {
  let w = sabha(t) + herd(t, 6).replace(/translate\(/, 'translate(');
  w += janak({ x: 300, y: 1700, s: 0.85, eyes: 'open', armR: -110, elbowR: -20, armL: 20 });
  const yk = eo(seg(t, at('ऋषि याज्ञवल्क्य') - 0.2, at('ऋषि याज्ञवल्क्य') + 0.5));
  w += `<g opacity="${yk.toFixed(2)}">${rishi({ x: 780, y: 1700, s: 0.85, eyes: 'closed', armR: -100, elbowR: -10, armL: 30 })}</g>`;
  const uproar = seg(t, at('सभा भड़क'), at('फिर उठीं — गार्गी'));
  if (uproar > 0) for (let i = 0; i < 5; i++) w += `<text x="${150 + i * 190}" y="${(1000 - (i % 2) * 60).toFixed(0)}" font-family="${ANTON}" font-size="120" fill="#FFE29A" opacity="${clamp(uproar * 4 - i * 0.4).toFixed(2)}" stroke="#14060A" stroke-width="8" paint-order="stroke">?</text>`;
  let s = cam(540, 1250, lerp(1.0, 1.08, seg(t, at('बृहदारण्यक'), at('फिर उठीं — गार्गी'))), w);
  s += pill(t, at('बृहदारण्यक') + 0.3, 'BRIHADARANYAKA UPANISHAD · 3', 60, 560);
  s += caps(t, [{ t0: at('राजा जनक'), l1: 'RAJA JANAK:', l2: '"SABSE BADA BRAHMAGYAANI?"', t2: at('जो सबसे बड़ा'), acc: GOLDT, ...DARK }, { t0: at('ऋषि याज्ञवल्क्य'), l1: 'YAGYAVALKYA:', l2: '"GAAYEIN HAANK LO"', t2: at('गायें हाँक'), acc: GOLDT, ...DARK },
    { t0: at('सभा भड़क'), l1: 'SABHA', l2: 'BHADAK UTHI', acc: '#FF5A4A', ...DARK }]);
  return s + TAG();
}, 'push');

// 2 GARGI'S CHAIN OF QUESTIONS — water, air, sky… further
add(at('फिर उठीं — गार्गी'), at('याज्ञवल्क्य बोले'), (t) => {
  const k = seg(t, at('सब कुछ जल') - 0.2, at('और आगे') + 1.2);
  let w = `<rect x="-300" y="-300" width="1700" height="2600" fill="#1A1030"/>` + stars(t, 60) + weave(540, 1080, 1.5, t, k, ['जल', 'वायु', 'आकाश', '…और आगे']);
  w += gargi({ x: 540, y: 1880, s: 0.75, t, armR: -120, elbowR: -20, armL: 30 });
  let s = cam(540, 1250, lerp(1.0, 0.92, seg(t, at('फिर उठीं — गार्गी'), at('याज्ञवल्क्य बोले'))), w);
  s += caps(t, [{ t0: at('फिर उठीं — गार्गी'), l1: 'GAARGI', ...DARK, size: 130 }, { t0: at('सब कुछ जल'), l1: 'JAL KISMEIN?', l2: 'VAAYU KISMEIN?', t2: at('वायु किसमें'), acc: GOLDT, ...DARK }, { t0: at('और आगे'), l1: 'AUR AAGE...', l2: 'AUR AAGE...', acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'zoom');

// 3 "DON'T ASK TOO FAR" — she sits... but is not defeated
add(at('याज्ञवल्क्य बोले'), at('फिर उठीं — जैसे'), (t) => {
  const sit = eo(seg(t, at('गार्गी बैठ') - 0.1, at('गार्गी बैठ') + 0.6));
  let w = sabha(t) + rishi({ x: 760, y: 1700, s: 0.9, eyes: 'open', armR: -120, elbowR: -10, armL: 30 });
  w += `<g transform="translate(0 ${(120 * sit).toFixed(0)})">${gargi({ x: 320, y: 1700, s: 0.9, t, armL: 20, armR: -20 })}</g>`;
  const dr = seg(t, at('याज्ञवल्क्य बोले'), at('फिर उठीं — जैसे'));
  let s = cam(lerp(620, 380, sit) + 30 * Math.sin(dr * Math.PI), lerp(1300, 1260, dr), lerp(1.05, 1.3, sit) + 0.1 * dr, w);
  s += caps(t, [{ t0: at('याज्ञवल्क्य बोले'), l1: '"GAARGI, ITNA', l2: 'MAT POOCHHO..."', t2: at('गार्गी, इतना') + 0.6, acc: '#FF5A4A', ...DARK }, { t0: at('गार्गी बैठ'), l1: 'BAITH GAYIN...', l2: 'PAR HAARI NAHI', t2: at('पर हारी'), acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'fade');

// 4 TWO ARROWS — two questions
add(at('फिर उठीं — जैसे'), at('उत्तर मिला'), (t) => {
  const a1 = eo(seg(t, at('जैसे योद्धा') + 0.8, at('जैसे योद्धा') + 1.3)), a2 = eo(seg(t, at('मैं दो प्रश्न'), at('मैं दो प्रश्न') + 0.5));
  const q = t > at('जो आकाश') - 0.1;
  let w = bg('rage') + rays(540, 1000, 18, 0.06, t) + `<rect x="-300" y="1480" width="1700" height="900" fill="#3A0A12"/>`;
  w += gargi({ x: 540, y: 1720, s: 1.0, t, armR: -150, elbowR: 0, armL: 30 });
  w += arrow2(540, 820, 1.0, -12, a1) + arrow2(540, 900, 1.0, 12, a2);
  if (q) { const kk = seg(t, at('जो आकाश'), at('वो किसमें') + 0.5); w += weave(540, 820, 0.7, t, kk, ['धरती', 'आकाश', 'भूत · वर्तमान · भविष्य']); }
  let s = cam(540, 1200, lerp(1.0, 1.08, seg(t, at('फिर उठीं — जैसे'), at('उत्तर मिला'))), w);
  s += caps(t, [{ t0: at('फिर उठीं — जैसे'), l1: 'JAISE YODDHA', l2: '2 BAAN LEKAR', t2: at('जैसे योद्धा') + 0.8, acc: GOLDT, ...DARK }, { t0: at('मैं दो प्रश्न'), l1: 'MAIN 2 PRASHN', l2: 'LAAYI HOON', acc: GOLDT, ...DARK },
    { t0: at('जो आकाश'), l1: 'BHOOT · VARTMAAN · BHAVISHYA', l2: 'KISMEIN BUNA HAI?', t2: at('वो किसमें'), acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'flash');

// 5 THE AKSHARA — and Gargi herself declares him unbeatable
add(at('उत्तर मिला'), 999, (t) => {
  const ak = eo(seg(t, at('अक्षर में') - 0.1, at('अक्षर में') + 0.5));
  const end = t > at('और गार्गी ने') - 0.15;
  let w = end ? sabha(t) + rays(540, 1100, 18, 0.06, t) + gargi({ x: 360, y: 1720, s: 0.95, t, armR: -100, elbowR: -20, armL: 30 }) + rishi({ x: 780, y: 1720, s: 0.85, eyes: 'closed', armL: 30, armR: -30 })
              : `<rect x="-300" y="-300" width="1700" height="2600" fill="#0B0620"/>` + stars(t, 80) + `<g opacity="${(0.5 * (1 - ak)).toFixed(2)}">${weave(540, 1150, 1.3, t, 1, ['धरती', 'आकाश', 'भूत · वर्तमान · भविष्य', '?'])}</g>` + rays(540, 1100, 22, 0.1 * ak, t) + `<circle cx="540" cy="1100" r="${(200 + 400 * ak).toFixed(0)}" fill="url(#halo)" opacity="${(0.7 * ak).toFixed(2)}"/>`;
  let s = cam(540, 1200, lerp(1.0, 1.06, seg(t, at('उत्तर मिला'), at('उत्तर मिला') + 10)), w);
  if (!end && ak > 0) s += `<g opacity="${ak.toFixed(2)}" transform="translate(540 1150) scale(${lerp(0.8, 1, back(ak)).toFixed(3)})"><text text-anchor="middle" font-family="Baloo" font-weight="800" font-size="200" fill="#FFE29A" stroke="#14060A" stroke-width="10" paint-order="stroke">अक्षर</text><text y="80" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="28" fill="#FFF3DC" letter-spacing="3">AVINAASHI · BRIHADARANYAKA 3.8.8</text></g>`;
  s += caps(t, [{ t0: at('उत्तर मिला'), l1: 'UTTAR:', ...DARK }, { t0: at('और गार्गी ने'), l1: 'GAARGI NE HI KAHA:', l2: '"INHE KOI NAHI HARA SAKTA"', t2: at('इन्हें कोई'), acc: GOLDT, ...DARK }]);
  if (end) s += pill(t, at('इन्हें कोई') + 2.0, 'FOLLOW · UPANISHAD SERIES', 540, 1450, { center: true, bg: RED });
  return s + TAG();
}, 'iris');

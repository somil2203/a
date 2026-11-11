// Satyakama Jabala — Chandogya Upanishad 4.4-4.9: his mother Jabala's candid answer about his lineage; Haridrumata Gautama
// accepts him for his truthfulness ("fetch fuel, I will initiate you"); 400 lean, weak cows; his vow not to return before they
// are a thousand; the bull, the fire, the swan and a water bird (madgu) teach him about Brahman.
const DARK = { dark: false }, LIGHT = { dark: true };
const TAG = () => tagTR('UPANISHAD KI KAHANIYAAN · 1');
const rays = (cx, cy, n, op, t, col = '#FFF2C6') => [...Array(n)].map((_, i) => { const a = (i * 360 / n + t * 5) * Math.PI / 180, b = a + 0.12;
  return `<path d="M${cx} ${cy} L${(cx + Math.cos(a) * 2600).toFixed(0)} ${(cy + Math.sin(a) * 2600).toFixed(0)} L${(cx + Math.cos(b) * 2600).toFixed(0)} ${(cy + Math.sin(b) * 2600).toFixed(0)}Z" fill="${col}" opacity="${op}"/>`; }).join('');
const fold = { armL: 38, elbowL: -112, armR: -38, elbowR: 112 };
const homeIn = (t) => { let w = bg('dusk') + `<rect x="-300" y="1440" width="1700" height="900" fill="#8E5A3A"/><rect x="-300" y="560" width="1700" height="880" fill="#C9955A" opacity=".55"/>`;
  w += `<rect x="760" y="760" width="200" height="260" rx="10" fill="#3A1A14"/>` + diya(860, 1440, 0.6, t, 2); return w; };

// 0 HOOK — "who is your father?" — and the boy told the truth
add(0, at('छांदोग्य'), (t) => {
  const c = camPath(t, [[0, 540, 1250, 1.05], [at('और उस बच्चे'), 640, 1260, 1.35], [at('जो कोई'), 640, 1200, 1.55], [at('छांदोग्य'), 600, 1200, 1.5]]);
  let w = ashram(t) + rishi({ x: 330, y: 1700, s: 0.95, eyes: 'open', armR: -60, elbowR: -50, armL: 30 }) + satyakam({ x: 740, y: 1700, s: 0.7, t, eyes: 'open', ...fold, mouth: t > at('वो सच बोल') && t < at('जो कोई') && Math.sin(t * 16) > 0 ? 'open' : 'smile' });
  let s = cam(...c, w);
  s += caps(t, [{ t0: 0, l1: 'GURU NE POOCHHA:', l2: '"TUMHARE PITA KAUN?"', t2: 0.4, acc: '#C1272D', ...LIGHT }, { t0: at('और उस बच्चे'), l1: 'AUR BACHCHE NE', l2: 'SACH BOL DIYA', t2: at('वो सच बोल'), acc: '#C1272D', ...LIGHT },
    { t0: at('जो कोई'), l1: 'JO KOI BHI', l2: 'CHHIPA LETA', acc: '#C1272D', ...LIGHT }]);
  return s + TAG();
});

// 1 THE SOURCE — Chandogya Upanishad; a boy who wants to learn the Vedas
add(at('छांदोग्य'), at('उसने माँ'), (t) => {
  let w = paperBg(t) + pothi(540, 900, 1.15, '', t) + satyakam({ x: 540, y: 1560, s: 0.75, t, eyes: 'open', armL: 20, armR: -20 });
  let s = cam(540, lerp(1100, 1200, seg(t, at('छांदोग्य'), at('उसने माँ'))), lerp(1.0, 1.15, seg(t, at('छांदोग्य'), at('उसने माँ'))), w);
  s += pill(t, at('छांदोग्य') + 0.4, 'CHHANDOGYA UPANISHAD · 4.4', 540, 1060, { center: true });
  s += caps(t, [{ t0: at('छांदोग्य'), l1: 'CHHANDOGYA', l2: 'UPANISHAD', acc: RED, ...LIGHT }, { t0: at('सत्यकाम नाम'), l1: 'SATYAKAAM', l2: 'VED PADHNA CHAHTA THA', t2: at('वेद पढ़ना'), acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'push');

// 2 HIS MOTHER'S HONEST ANSWER
add(at('उसने माँ'), at('सत्यकाम गुरु'), (t) => {
  const talk = (t0, t1) => t > t0 && t < t1 && Math.sin(t * 15) > 0;
  let w = homeIn(t) + jabala({ x: 360, y: 1720, s: 1.0, t, armL: 30, elbowL: 40, armR: -40, elbowR: -60 }) + satyakam({ x: 740, y: 1720, s: 0.68, t, eyes: 'open', armL: 20, armR: -20, mouth: talk(at('उसने माँ'), at('माँ बोलीं')) ? 'open' : 'smile' });
  w += bubble(740, 1020, 'मेरा गोत्र?', seg(t, at('माँ, मेरा') - 0.2, at('माँ, मेरा') + 0.2) * (1 - seg(t, at('माँ बोलीं') - 0.2, at('माँ बोलीं'))));
  const nameCard = eo(seg(t, at('कहना') + 0.2, at('कहना') + 0.6));
  const dr = seg(t, at('उसने माँ'), at('सत्यकाम गुरु'));
  let s = cam(lerp(540, 420, eio(seg(t, at('माँ बोलीं'), at('माँ बोलीं') + 1))) + 40 * Math.sin(dr * Math.PI), lerp(1340, 1260, dr), lerp(1.0, 1.2, eio(seg(t, at('माँ बोलीं'), at('माँ बोलीं') + 1))) + 0.12 * dr, w);
  if (nameCard > 0) s += `<g opacity="${nameCard.toFixed(2)}" transform="translate(0 ${(30 * (1 - nameCard)).toFixed(0)})">${paper(140, 640, 800, 240, -2, `<text x="400" y="130" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="104" fill="${INK}">सत्यकाम जाबाल</text><text x="400" y="200" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="26" fill="#6A5A4A">SATYAKAAM, JABALA KA BETA</text>`, { tape: true, seed: 4 })}</g>`;
  s += caps(t, [{ t0: at('उसने माँ'), l1: 'MAA JABALA SE', l2: 'GOTRA POOCHHA', t2: at('माँ, मेरा'), acc: GOLDT, ...DARK }, { t0: at('बेटा, जवानी'), l1: 'JAWAANI MEIN', l2: 'MAIN DAASI THI', acc: GOLDT, ...DARK },
    { t0: at('मुझे नहीं'), l1: 'GOTRA', l2: 'NAHI PATA', acc: '#FF5A4A', ...DARK }, { t0: at('मैं जबाला'), l1: 'MAIN JABALA,', l2: 'TU SATYAKAAM', t2: at('तू सत्यकाम'), acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'fade');

// 3 BEFORE THE GURU — the same question; the same words, nothing hidden
add(at('सत्यकाम गुरु'), at('गुरु बोले'), (t) => {
  const note = eo(seg(t, at('माँ की बात') - 0.1, at('माँ की बात') + 0.4));
  let w = ashram(t) + rishi({ x: 330, y: 1700, s: 0.95, eyes: 'open', armR: -60, elbowR: -50, armL: 30 }) + satyakam({ x: 740, y: 1700, s: 0.7, t, eyes: 'open', ...fold, mouth: t > at('और सत्यकाम ने') && Math.sin(t * 15) > 0 ? 'open' : 'smile' });
  let s = cam(540, 1250, lerp(1.0, 1.1, seg(t, at('सत्यकाम गुरु'), at('गुरु बोले'))), w);
  if (note > 0) s += `<g opacity="${note.toFixed(2)}">${paper(90, 640, 900, 210, 1.5, `<text x="30" y="80" font-family="${ANTON}" font-size="46" fill="${INK}">"MAA KO NAHI PATA MERA GOTRA.</text><text x="30" y="142" font-family="${ANTON}" font-size="46" fill="${INK}">MAIN SATYAKAAM JAABAAL HOON."</text><text x="30" y="190" font-family="SpaceMono" font-weight="700" font-size="22" fill="${RED}">— JYON KA TYON</text>`, { seed: 6 })}</g>`;
  s += caps(t, [{ t0: at('सत्यकाम गुरु'), l1: 'GURU GAUTAM', l2: 'KE PAAS', acc: RED, ...LIGHT }, { t0: at('और सत्यकाम ने'), l1: 'BINA KUCH', l2: 'CHHIPAAYE', t2: at('बिना कुछ'), acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'whip');

// 4 "ONLY A BRAHMANA SPEAKS SUCH TRUTH" — fetch the fuel, initiation
add(at('गुरु बोले'), at('फिर गुरु'), (t) => {
  let w = ashram(t) + rays(330, 1100, 18, 0.08, t) + `<circle cx="330" cy="1150" r="420" fill="url(#halo)" opacity=".45"/>` + rishi({ x: 330, y: 1700, s: 0.95, eyes: 'closed', armR: -120, elbowR: -10, armL: 30 });
  w += satyakam({ x: 740, y: 1700, s: 0.7, t, eyes: 'closed', ...fold });
  const sticks = eo(seg(t, at('जाओ') + 0.3, at('जाओ') + 0.9));
  if (sticks > 0) w += `<g opacity="${sticks.toFixed(2)}" transform="translate(740 ${(1300 + 40 * (1 - sticks)).toFixed(0)})">${[-30, 0, 30].map((dx, i) => `<rect x="${dx - 60}" y="${-10 + i * 18}" width="150" height="16" rx="8" fill="#7A4A22" transform="rotate(${-8 + i * 6})"/>`).join('')}</g>`;
  let s = cam(540, 1250, lerp(1.0, 1.06, seg(t, at('गुरु बोले'), at('फिर गुरु'))), w);
  s += stamp2(t, at('मैं तुम्हें') + 0.4, 'DEEKSHA', 540, 1500, { col: RED, rot: -6 });
  s += caps(t, [{ t0: at('गुरु बोले'), l1: '"ITNA SACH', l2: 'BRAAHMAN HI BOL SAKTA"', t2: at('केवल ब्राह्मण'), acc: RED, ...LIGHT }, { t0: at('जाओ'), l1: 'SAMIDHA LAAO', ...LIGHT }]);
  return s + TAG();
}, 'fade');

// 5 FOUR HUNDRED WEAK COWS — "I won't return until they are a thousand"
add(at('फिर गुरु'), at('और जब गायें'), (t) => {
  let w = bg('day') + `<rect x="-300" y="1300" width="1700" height="900" fill="#B9C47A"/>`;
  for (let i = 0; i < 9; i++) { const x = 120 + (i % 3) * 300 + (Math.floor(i / 3) % 2) * 120, y = 1420 + Math.floor(i / 3) * 140;
    w += `<g transform="translate(0 0)">${cow2({ x, y, s: 0.42, t, ph: 0, patch: false }).replace(/url\(#cowG\)/g, '#D9D2C4')}</g>`; }
  w += satyakam({ x: 540, y: 1840, s: 0.72, t, eyes: 'open', armL: 20, armR: t > at('सत्यकाम बोले') ? -160 : -20, elbowR: 0 });
  let s = cam(540, 1300, lerp(1.0, 1.08, seg(t, at('फिर गुरु'), at('और जब गायें'))), w);
  s += pill(t, at('फिर गुरु') + 0.8, 'GAAYEIN: 400', 1022, 560, { right: true, bg: RED }) + pill(t, at('जब तक'), 'LAKSHYA: 1000', 1022, 620, { right: true });
  s += caps(t, [{ t0: at('फिर गुरु'), l1: '400 GAAYEIN', l2: 'DUBLI, KAMZOR', t2: at('कमज़ोर'), acc: RED, ...LIGHT }, { t0: at('सत्यकाम बोले'), l1: '"1000 HONE TAK', l2: 'NAHI LAUTUNGA"', t2: at('मैं नहीं लौटूँगा'), acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'zoom');

// 6 A THOUSAND — the bull, fire, swan and water bird teach him Brahman
add(at('और जब गायें'), at('जन्म से'), (t) => {
  const n = Math.round(lerp(400, 1000, eo(seg(t, at('और जब गायें'), at('तो एक बैल') - 0.2))));
  const teach = t > at('तो एक बैल') - 0.15;
  let w = (teach ? `<rect x="-300" y="-300" width="1700" height="2600" fill="#1A1030"/>` + stars(t, 60) + rays(540, 1100, 20, 0.06, t) : bg('dawn') + `<rect x="-300" y="1300" width="1700" height="900" fill="#9CC46E"/>`);
  if (!teach) for (let i = 0; i < 15; i++) w += cow2({ x: 80 + (i % 5) * 240, y: 1400 + Math.floor(i / 5) * 150, s: 0.36, t, flip: i % 2 === 0 });
  else {
    const it = [['bull', at('तो एक बैल'), 300, 1150], ['agni', at('अग्नि'), 780, 1100], ['hans', at('हंस'), 300, 1560], ['madgu', at('और एक जल'), 780, 1560]];
    it.forEach(([k, t0, x, y]) => { const e = back(seg(t, t0 - 0.05, t0 + 0.3)); if (e <= 0) return;
      w += `<g transform="translate(${x} ${y}) scale(${e.toFixed(3)}) translate(${-x} ${-y})"><circle cx="${x}" cy="${y - 80}" r="190" fill="url(#halo)" opacity=".6"/>`;
      if (k === 'bull') w += bull({ x: x + 60, y: y + 40, s: 0.62, t });
      if (k === 'agni') w += kund(x, y + 60, 0.7, t, 1.0);
      if (k === 'hans') w += swan(x, y, 0.95, t);
      if (k === 'madgu') w += diverBird(x, y, 1.0, t);
      w += `</g>`; });
    const g = eo(seg(t, at('उसे ब्रह्म') - 0.1, at('उसे ब्रह्म') + 0.6)); w += `<circle cx="540" cy="1350" r="${(100 + 500 * g).toFixed(0)}" fill="url(#halo)" opacity="${(0.7 * g).toFixed(2)}"/>`;
  }
  let s = cam(540, 1300, 1.0, w);
  s += pill(t, at('और जब गायें'), `GAAYEIN: ${n}`, 1022, 560, { right: true, bg: n >= 1000 ? '#2E8A4E' : RED });
  s += caps(t, [{ t0: at('और जब गायें'), l1: '400 → 1000', acc: GOLDT, ...(teach ? DARK : LIGHT), size: 120 }, { t0: at('तो एक बैल'), l1: 'BAIL · AGNI', l2: 'HANS · JAL-PAKSHI', t2: at('हंस'), acc: GOLDT, ...DARK },
    { t0: at('उसे ब्रह्म'), l1: 'BRAHM KA', l2: 'GYAAN', acc: GOLDT, ...DARK, size: 120 }]);
  return s + TAG();
}, 'fade');

// 7 NOT BY BIRTH — BY TRUTH
add(at('जन्म से'), at('ये रील'), (t) => {
  let w = bg('gold') + rays(540, 1100, 22, 0.14, t) + `<circle cx="540" cy="1200" r="460" fill="url(#halo)"/>` + satyakam({ x: 540, y: 1760, s: 0.9, t, eyes: 'closed', armL: 20, armR: -20 });
  let s = cam(540, 1250, lerp(1.1, 1.0, seg(t, at('जन्म से'), at('ये रील'))), w);
  s += caps(t, [{ t0: at('जन्म से'), l1: 'JANM SE NAHI.', l2: 'SACH SE.', t2: at('सच से'), acc: RED, ...LIGHT, size: 120 }]);
  return s + TAG();
}, 'flash');

// 8 SHARE
add(at('ये रील'), 999, (t) => {
  let w = paperBg(t) + jabala({ x: 300, y: 1880, s: 0.9, t, armL: 40, elbowL: 60, armR: -40, elbowR: -60 }) + satyakam({ x: 620, y: 1880, s: 0.62, t, eyes: 'closed', armL: 20, armR: -20 });
  let s = cam(540, 1060, lerp(1.0, 1.06, seg(t, at('ये रील'), at('ये रील') + 6)), w);
  const cta = eo(seg(t, at('जिसे आज') - 0.2, at('जिसे आज') + 0.3));
  if (cta > 0) s += `<g opacity="${cta.toFixed(2)}"><path d="M40 1000 L1040 980 L1030 1100 L50 1120Z" fill="${RED}"/><text x="90" y="1075" font-family="${ANTON}" font-size="60" fill="#FFF">USE BHEJO JISE AAJ</text>
      <path d="M40 1130 L1040 1120 L1035 1240 L45 1250Z" fill="${INK}"/><path d="M80 1160 l60 30 l-60 30 l12 -30z" fill="${GOLDT}"/><text x="170" y="1210" font-family="${ANTON}" font-size="56" fill="${GOLDT}">SACH BOLNE KI HIMMAT CHAHIYE</text></g>`;
  s += caps(t, [{ t0: at('ये रील'), l1: 'YE REEL', l2: 'BHEJO...', acc: RED, ...LIGHT, size: 110 }]);
  return s + TAG();
}, 'zoom');

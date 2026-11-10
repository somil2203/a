// Bhai Dooj · Deepotsav Din 5/5 — Yama & Yamuna. Source: Padma Purana, Uttara Khanda (Yama-dvitiya: Yamuna feeds her brother;
// a brother should eat from his sister's hand on Kartika Shukla Dvitiya). Surya's children Yama & Yamuna (Puranic genealogy).
// Grammar after the reference: top-left condensed caps built word by word (no bottom subtitles), mono pills, paper props,
// a viewer question with a strikethrough list, a callback to the series (Nachiketa at Yama's door, Dhanteras), share CTA.
const DARK = { dark: false }, LIGHT = { dark: true };
const TAG = () => tagTR('DEEPOTSAV · DIN 5/5');
const rays = (cx, cy, n, op, t, col = '#FFF2C6') => [...Array(n)].map((_, i) => { const a = (i * 360 / n + t * 5) * Math.PI / 180, b = a + 0.12;
  return `<path d="M${cx} ${cy} L${(cx + Math.cos(a) * 2600).toFixed(0)} ${(cy + Math.sin(a) * 2600).toFixed(0)} L${(cx + Math.cos(b) * 2600).toFixed(0)} ${(cy + Math.sin(b) * 2600).toFixed(0)}Z" fill="${col}" opacity="${op}"/>`; }).join('');
const nachiketa = (o) => vamana({ umbrella: false, ...o }).replace(/url\(#kBlueV\)/g, '#C98A62').replace(/url\(#kBlue\)/g, '#D9A07A').replace(/#4E7EE6/g, '#D9A07A').replace(/#3E66C8/g, '#C08060').replace(/#3A62C2/g, '#B9805C').replace(/#3A60BE/g, '#B07858');
const interior = (t) => { let w = bg('maroon') + `<rect x="-300" y="1420" width="1700" height="900" fill="#7A2E22"/>`;
  for (let i = 0; i < 4; i++) w += `<path d="M${-40 + i * 300} 1420 V700 Q${-40 + i * 300 + 130} 540 ${-40 + i * 300 + 260} 700 V1420Z" fill="#5A1E2A" stroke="#C98A1E" stroke-width="6"/>`;
  for (let i = 0; i < 6; i++) w += diya(80 + i * 190, 1450, 0.45, t, i);
  return w; };

// 0 HOOK — the god of death at a door, coming to eat
add(0, at('आज भाई दूज'), (t) => {
  const toHome = t > at('साल में एक') - 0.15;
  let s = '';
  if (!toHome) {
    const push = seg(t, 0, at('साल में एक'));
    s += cam(540, lerp(1200, 1120, push), lerp(1.12, 1.3, eio(push)), bg('rage') + `<rect x="-300" y="1500" width="1700" height="900" fill="#2A0E10"/>` + yamlokGate(540, 1500, 1.0, 0, t) + yamaRiding(600, 1760, 0.95, t, { eyes: 'open' }) + dust(t, 30, '#FF8A4A', 120));
    s += flashRect(t, 0, 0.25, '#000000');
  } else {
    const walk = eio(seg(t, at('साल में एक'), at('खाना खाने') + 0.2));
    s += cam(lerp(420, 700, walk), 1250, lerp(1.0, 1.15, walk), bg('dusk') + sun(540, 760, 120, '#FFB86A') + `<rect x="-300" y="1500" width="1700" height="900" fill="#8E5A3A"/>`
      + sisterHome(880, 1500, 0.85, t, { open: true }) + yamaRiding(lerp(-80, 560, walk), 1780, 0.75, t, { walk: walk < 1, eyes: 'open' }));
    s += pill(t, at('ख़ुद किसी') + 0.3, 'YAMUNA KA GHAR', 640, 1160);
  }
  s += caps(t, [{ t0: 0.0, l1: 'MAUT KE DEVTA', ...DARK }, { t0: at('जिनके दरवाज़े'), l1: 'JINKE DARWAAZE SE', l2: 'KOI NAHI LAUTA', acc: '#FF5A4A', ...DARK },
    { t0: at('साल में एक'), l1: 'SAAL MEIN EK DIN...', l2: 'KHUD KISI KE DARWAAZE PAR', t2: at('ख़ुद किसी'), acc: GOLDT, ...DARK },
    { t0: at('खाना खाने'), l1: 'KHAANA', l2: 'KHAANE!', acc: GOLDT, ...DARK, size: 120 }]);
  return s + TAG();
});

// 1 TODAY — the calendar, the fifth diya
add(at('आज भाई दूज'), at('पद्म पुराण'), (t) => {
  const kc = eo(seg(t, at('आज भाई दूज') + 0.3, at('आज भाई दूज') + 1.0));
  const door = eo(seg(t, at('उसी दरवाज़े') - 0.2, at('उसी दरवाज़े') + 0.4));
  let w = paperBg(t) + calendar(540, 1060, 1.25, t, { ticks: [6, 7, 8, 10], circle: 11, kc });
  if (door > 0) w += `<g opacity="${door.toFixed(2)}" transform="translate(0 ${(40 * (1 - door)).toFixed(0)})">${paper(600, 1260, 380, 420, 5, `<rect x="20" y="20" width="340" height="340" fill="#3A1A20"/><g transform="translate(190 330) scale(.4)">${sisterHome(0, 0, 1, t, { open: true })}</g>`, { tape: true, seed: 3 })}</g>`;
  let s = cam(540, 1060, lerp(1.0, 1.06, seg(t, at('आज भाई दूज'), at('पद्म पुराण'))), w);
  s += pill(t, at('दीपोत्सव'), 'DIN 1 DHANTERAS → DIN 5 BHAI DOOJ', 80, 1480);
  s += caps(t, [{ t0: at('आज भाई दूज'), l1: 'AAJ BHAI DOOJ', l2: 'DIN 5 · AAKHIRI DIYA', t2: at('दीपोत्सव'), ...LIGHT }, { t0: at('और ये कहानी'), l1: 'AUR YE KAHANI', l2: 'USI DARWAAZE KI', t2: at('उसी दरवाज़े'), ...LIGHT }]);
  return s + TAG();
}, 'zoom');

// 2 SOURCE — Padma Purana
add(at('पद्म पुराण'), at('सूर्य देव'), (t) => {
  const drop = back(seg(t, at('पद्म पुराण'), at('पद्म पुराण') + 0.5));
  let w = paperBg(t) + `<g transform="translate(0 ${(-500 * (1 - clamp(drop))).toFixed(0)})">${pothi(540, 1100, 1.25, '', t)}</g>`;
  let s = cam(540, 1060, lerp(1.0, 1.08, seg(t, at('पद्म पुराण'), at('सूर्य देव'))), w);
  s += pill(t, at('पद्म पुराण') + 0.5, 'PADMA PURANA · UTTARA KHANDA', 540, 1300, { center: true });
  s += caps(t, [{ t0: at('पद्म पुराण'), l1: 'PADMA PURAAN', l2: 'MEIN YE KATHA', ...LIGHT }]);
  return s + TAG();
}, 'push');

// 3 SURYA'S CHILDREN — Yama and Yamuna, brother and sister
add(at('सूर्य देव'), at('यम बने'), (t) => {
  const kids = eo(seg(t, at('यम और यमुना') - 0.3, at('यम और यमुना') + 0.6));
  let w = bg('sky') + suryaRath(540, 760, 0.95, t) + cloud(300, 1560, 1.6) + cloud(780, 1580, 1.5);
  if (kids > 0) {
    w += `<g opacity="${kids.toFixed(2)}"><path d="M540 860 Q420 1100 380 1260 M540 860 Q660 1100 700 1260" stroke="${RED}" stroke-width="5" stroke-dasharray="12 12" fill="none"/>`;
    w += krishna2({ x: 380, y: 1600, s: 0.55, noFeather: true, eyes: 'open', t }).replace(/url\(#kBlueV\)/g, YAMA_SKIN_D).replace(/url\(#kBlue\)/g, YAMA_SKIN).replace(/#4E7EE6/g, YAMA_SKIN).replace(/#3E66C8/g, YAMA_SKIN_D).replace(/#3A60BE/g, YAMA_SKIN_D);
    w += gopi2({ x: 700, y: 1600, s: 0.6, veil: '#2A4AA8', top: '#2A4AA8', skirt: '#1E3A8A', t }).replace(/#E8A983/g, '#B07A56') + `</g>`;
  }
  let s = cam(540, 1100, lerp(1.08, 1.0, seg(t, at('सूर्य देव'), at('यम बने'))), w);
  s += pill(t, at('यम और यमुना') + 0.2, 'YAM', 300, 1470) + pill(t, at('यम और यमुना') + 0.5, 'YAMUNA', 630, 1470);
  s += caps(t, [{ t0: at('सूर्य देव'), l1: 'SURYA DEV KI', l2: 'DO SANTAANEIN', ...LIGHT }, { t0: at('भाई और बहन'), l1: 'BHAI', l2: '+ BEHEN', acc: RED, ...LIGHT, size: 110 }]);
  return s + TAG();
}, 'fade');

// 4 YAMA → DHARMARAJA (the scales of karma)
add(at('यम बने'), at('और यमुना, धरती'), (t) => {
  let w = bg('rage') + `<rect x="-300" y="1520" width="1700" height="900" fill="#3A0A12"/>` + `<circle cx="540" cy="1100" r="480" fill="url(#halo)" opacity=".35"/>`;
  w += yamraj({ x: 700, y: 1760, s: 0.95, eyes: 'closed', armR: -130, elbowR: -20 }) + scales(300, 1620, 0.85, t);
  let s = cam(540, 1200, lerp(1.0, 1.1, seg(t, at('यम बने'), at('और यमुना, धरती'))), w);
  s += pill(t, at('हर जीव'), 'HAR JEEV KE KARMON KA HISAAB', 60, 560);
  s += caps(t, [{ t0: at('यम बने'), l1: 'YAM →', l2: 'DHARMARAJ', acc: GOLDT, ...DARK, size: 110 }]);
  return s + TAG();
}, 'whip');

// 5 YAMUNA → THE RIVER
add(at('और यमुना, धरती'), at('यमुना बार-बार'), (t) => {
  const flow = eo(seg(t, at('और यमुना, धरती'), at('और यमुना, धरती') + 2.0));
  let w = bg('day') + `<path d="M-300 900 L60 520 L300 760 L520 460 L800 780 L1000 560 L1400 900Z" fill="#9AA8B8"/><path d="M60 520 L130 600 L20 610Z M520 460 L600 560 L450 560Z M1000 560 L1060 640 L940 640Z" fill="#FFFFFF"/>`;
  w += `<rect x="-300" y="880" width="1700" height="1400" fill="#8CBF6A"/>`;
  const L = 1500 * flow; w += `<path d="M520 880 C420 1100 760 1260 560 1480 C400 1660 700 1800 640 2100" stroke="#3E86D8" stroke-width="130" fill="none" stroke-dasharray="${L.toFixed(0)} 3000" stroke-linecap="round"/><path d="M520 880 C420 1100 760 1260 560 1480 C400 1660 700 1800 640 2100" stroke="#7FB8F0" stroke-width="40" fill="none" stroke-dasharray="${L.toFixed(0)} 3000" opacity=".6"/>`;
  w += `<g opacity="${clamp(flow * 1.4 - 0.3).toFixed(2)}">${yamunaDevi({ x: 600, y: 1520, s: 0.85, t, armL: 40, elbowL: 30, armR: -40, elbowR: -30 })}</g>`;
  let s = cam(540, lerp(1000, 1200, flow), lerp(1.0, 1.08, seg(t, at('और यमुना, धरती'), at('यमुना बार-बार'))), w);
  s += caps(t, [{ t0: at('और यमुना, धरती'), l1: 'YAMUNA →', l2: 'NADI BANI', acc: '#1E5AB8', ...LIGHT, size: 110 }]);
  return s + TAG();
}, 'fade');

// 6 THE INVITATIONS PILE UP — "today no... tomorrow... some other time"
add(at('यमुना बार-बार'), at('फिर आई'), (t) => {
  const n = Math.floor(lerp(1, 99, seg(t, at('यमुना बार-बार'), at('न्योते पर') + 1.2) ** 1.6));
  let w = interior(t) + `<rect x="120" y="1240" width="840" height="60" rx="10" fill="#4A1A12"/><rect x="160" y="1300" width="40" height="300" fill="#3A140E"/><rect x="880" y="1300" width="40" height="300" fill="#3A140E"/>`;
  w += yamraj({ x: 540, y: 1580, s: 0.82, eyes: t > at('पर यम के') ? 'open' : 'closed', armR: -40, elbowR: -60, armL: 40, elbowL: 60 });
  // the ledger scroll unrolls while he works
  const led = eo(seg(t, at('हर दिन') - 0.2, at('अनगिनत') + 1.0));
  w += `<path d="M300 1250 L300 ${(1250 + 520 * led).toFixed(0)} L520 ${(1250 + 520 * led).toFixed(0)} L520 1250Z" fill="#F4EBDD"/>${[...Array(Math.floor(12 * led))].map((_, i) => `<path d="M320 ${1280 + i * 40} h${120 + rnd(i) * 60}" stroke="#8A7A6A" stroke-width="5"/>`).join('')}`;
  // invitation cards land, one after another, then pile up
  const cards = Math.floor(lerp(1, 14, seg(t, at('यमुना बार-बार') + 0.3, at('न्योते पर') + 1.4)));
  for (let i = 0; i < cards; i++) { const tl = at('यमुना बार-बार') + 0.3 + i * ((at('न्योते पर') + 1.4 - at('यमुना बार-बार') - 0.3) / 13), k = eo(seg(t, tl, tl + 0.3));
    w += `<g transform="translate(${(lerp(1300, 600 + (rnd(i) - 0.5) * 520, k)).toFixed(0)} ${(lerp(400, 1300 + (rnd(i + 9) - 0.5) * 380, k)).toFixed(0)})">${invite(0, 0, 0.7, (rnd(i + 4) - 0.5) * 30)}</g>`; }
  let s = cam(540, 1250, lerp(1.0, 1.08, seg(t, at('यमुना बार-बार'), at('फिर आई'))), w);
  s += pill(t, at('यमुना बार-बार') + 0.4, `NYOTA #${n}`, 1022, 560, { right: true, bg: RED });
  s += caps(t, [{ t0: at('यमुना बार-बार'), l1: 'BAAR-BAAR', l2: 'NYOTA', acc: GOLDT, ...DARK },
    { t0: at('भैया'), l1: '"BHAIYA,', l2: 'GHAR AAO."', acc: GOLDT, ...DARK },
    { t0: at('पर यम के'), l1: 'PAR SAMAY', l2: 'KAHAAN?', acc: '#FF5A4A', ...DARK },
    { t0: at('हर दिन'), l1: 'HAR DIN', l2: 'ANGINAT HISAAB', t2: at('अनगिनत'), acc: GOLDT, ...DARK },
    { t0: at('आज नहीं'), l1: 'AAJ NAHI. KAL...', l2: 'PHIR KABHI.', t2: at('फिर कभी'), acc: '#FF5A4A', ...DARK },
    { t0: at('न्योते पर'), l1: 'NYOTE PAR', l2: 'NYOTE...', acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'fade');

// 7 KARTIK SHUKLA DVITIYA — this time he could not say no (the hook's road, again)
add(at('फिर आई'), at('यमुना ने आरती'), (t) => {
  const onRoad = t > at('यमराज मना') - 0.3;
  let s = '';
  if (!onRoad) {
    const kc = eo(seg(t, at('फिर आई') + 0.6, at('फिर आई') + 1.4));
    s += cam(540, 1060, 1.1, paperBg(t) + calendar(540, 1060, 1.25, t, { ticks: [], circle: 11, kc }));
    s += pill(t, at('फिर आई') + 1.2, 'KARTIK MAAS · SHUKLA PAKSH · DOOJ', 540, 1520, { center: true });
    s += caps(t, [{ t0: at('फिर आई'), l1: 'KARTIK SHUKLA', l2: 'DWITIYA', acc: RED, ...LIGHT, size: 104 }, { t0: at('और इस बार'), l1: 'AUR IS BAAR...', ...LIGHT }]);
  } else {
    const walk = eio(seg(t, at('यमराज मना') - 0.3, at('यमुना ने आरती')));
    let w = bg('dusk') + stars(t, 30) + `<rect x="-300" y="1500" width="1700" height="900" fill="#6E4A3A"/>` + `<g opacity=".7">${yamlokGate(120, 1500, 0.4, 1, t)}</g>` + sisterHome(900, 1500, 0.55, t, { open: true });
    w += `<path d="M200 1560 C400 1640 700 1640 880 1560" stroke="#FFE29A" stroke-width="6" stroke-dasharray="14 14" fill="none"/>`;
    w += yamaRiding(lerp(220, 760, walk), 1640, 0.45, t, { walk: true, eyes: 'open' });
    s += cam(540, 1300, 1.0, w);
    s += caps(t, [{ t0: at('यमराज मना') - 0.3, l1: 'YAMRAJ', l2: 'MANA NAHI KAR PAAYE', acc: GOLDT, ...DARK }]);
  }
  return s + TAG();
}, 'zoom');

// 8 THE WELCOME — aarti, tilak, food from her own hands
add(at('यमुना ने आरती'), at('यमराज इतने'), (t) => {
  const tilakK = eo(seg(t, at('माथे पर') + 0.2, at('माथे पर') + 0.9));
  const food = eo(seg(t, at('और अपने हाथों') - 0.1, at('और अपने हाथों') + 0.8));
  const close = t > at('माथे पर') - 0.1 && t < at('और अपने हाथों') - 0.1;
  let w = interior(t) + yamraj({ x: 330, y: 1700, s: 0.9, eyes: 'closed', armL: 30, armR: -30, pasha: false, held: '' });
  if (tilakK > 0) w += `<path d="M330 ${(1700 - 0.9 * 628).toFixed(0)} l0 ${(-26 * tilakK).toFixed(0)}" stroke="#E0201A" stroke-width="13" stroke-linecap="round"/>${[[-7, 4], [6, 8], [-2, 14]].map(([dx, dy]) => `<ellipse cx="${330 + dx}" cy="${(1700 - 0.9 * 628 - 26 * tilakK + dy).toFixed(0)}" rx="3" ry="2" fill="#FFF6DA" opacity="${tilakK.toFixed(2)}"/>`).join('')}`;
  const aarti = t < at('माथे पर');
  w += yamunaDevi({ x: 760, y: 1700, s: 0.95, t, armR: aarti ? -110 + Math.sin(t * 3) * 25 : (close ? -150 : -60), elbowR: aarti ? -40 : -30, thali: aarti, armL: 30 });
  if (food > 0) w += `<g opacity="${food.toFixed(2)}" transform="translate(0 ${(60 * (1 - food)).toFixed(0)})">${thali(540, 1820, 0.55, 8, t)}</g>`;
  const c = close ? [330, 1700 - 0.9 * 640, 3.0] : [540, 1300, 1.0];
  let s = cam(...c, w);
  s += pill(t, at('यमुना ने आरती'), 'AARTI', 60, 1300) + pill(t, at('माथे पर'), 'TILAK', 230, 1300) + pill(t, at('और अपने हाथों'), 'BHOJAN', 400, 1300);
  s += caps(t, [{ t0: at('यमुना ने आरती'), l1: 'SWAGAT', ...DARK, size: 110 }, { t0: at('माथे पर'), l1: 'MAATHE PAR', l2: 'TILAK', acc: '#FF5A4A', ...DARK }, { t0: at('और अपने हाथों'), l1: 'APNE HAATHON SE', l2: 'BHOJAN', acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'fade');

// 9 "SISTER, ASK FOR ANYTHING"
add(at('यमराज इतने'), at('आप होते'), (t) => {
  let w = interior(t) + rays(330, 1100, 18, 0.06, t) + `<circle cx="330" cy="1150" r="440" fill="url(#halo)" opacity=".5"/>` + thali(540, 1820, 0.55, 8, t);
  w += yamraj({ x: 330, y: 1700, s: 0.9, eyes: 'open', armR: -100, elbowR: -20, armL: 30, pasha: false, held: '' }) + `<path d="M330 ${(1700 - 0.9 * 628).toFixed(0)} l0 -26" stroke="#E0201A" stroke-width="13" stroke-linecap="round"/>`;
  w += yamunaDevi({ x: 760, y: 1700, s: 0.95, t, armL: 38, elbowL: -112, armR: -38, elbowR: 112 });
  let s = cam(540, 1300, lerp(1.0, 1.1, seg(t, at('यमराज इतने'), at('आप होते'))), w);
  s += caps(t, [{ t0: at('यमराज इतने'), l1: 'YAMRAJ', l2: 'PRASANN', acc: GOLDT, ...DARK }, { t0: at('बहन, जो चाहो'), l1: '"BEHEN,', l2: 'JO CHAHO MAANG LO."', acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'fade');

// 10 THE VIEWER'S QUESTION — gold? heaven? immortality?
add(at('आप होते'), at('यमुना ने अपने'), (t) => {
  let w = paperBg(t) + `<g opacity=".95">${yamunaDevi({ x: 760, y: 1820, s: 1.2, t, armL: 38, elbowL: -112, armR: -38, elbowR: 112 })}</g>`;
  let s = cam(540, 1060, lerp(1.0, 1.06, seg(t, at('आप होते'), at('यमुना ने अपने'))), w);
  s += strikeList(t, 60, 760, [['SONA?', at('सोना') - 0.05, at('यमुना ने अपने') - 0.5], ['SWARG?', at('स्वर्ग') - 0.05, at('यमुना ने अपने') - 0.35], ['AMARTA?', at('अमरता') - 0.05, at('यमुना ने अपने') - 0.2]]);
  s += caps(t, [{ t0: at('आप होते'), l1: 'AAP HOTE', l2: 'TOH KYA MAANGTE?', acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'whip');

// 11 NOTHING FOR HERSELF — two wishes on her note
add(at('यमुना ने अपने'), at('यमराज बोले'), (t) => {
  let w = paperBg(t) + `<g opacity=".95">${yamunaDevi({ x: 780, y: 1860, s: 1.1, t, armL: 38, elbowL: -112, armR: -38, elbowR: 112 })}</g>`;
  let s = cam(540, 1060, lerp(1.0, 1.07, seg(t, at('यमुना ने अपने'), at('यमराज बोले'))), w);
  const n1 = eo(seg(t, at('हर साल इसी') - 0.1, at('हर साल इसी') + 0.3)), n2 = eo(seg(t, at('और जो भाई') - 0.1, at('और जो भाई') + 0.3)), hl = seg(t, at('उसे आपका') - 0.1, at('उसे आपका') + 0.4);
  if (n1 > 0) s += `<g opacity="${n1.toFixed(2)}">${paper(50, 640, 700, 150, -1.5, `<text x="28" y="66" font-family="${ANTON}" font-size="44" fill="${INK}">1 · HAR SAAL ISI DIN,</text><text x="28" y="122" font-family="${ANTON}" font-size="44" fill="${INK}">MERE GHAR AANA.</text>`, { seed: 5 })}</g>`;
  if (n2 > 0) s += `<g opacity="${n2.toFixed(2)}">${paper(60, 830, 760, 210, 1.2, `<text x="28" y="66" font-family="${ANTON}" font-size="44" fill="${INK}">2 · JO BHAI AAJ BEHEN KE GHAR</text><text x="28" y="122" font-family="${ANTON}" font-size="44" fill="${INK}">BHOJAN KARE —</text>${hl > 0 ? `<rect x="22" y="${140}" width="${(560 * hl).toFixed(0)}" height="56" fill="${GOLDT}" opacity=".85"/>` : ''}<text x="28" y="182" font-family="${ANTON}" font-size="44" fill="${RED}">USE AAPKA BHAY NA HO.</text>`, { seed: 8 })}</g>`;
  s += pill(t, at('और जो भाई') + 0.6, 'PADMA PURANA · YAMA DVITIYA', 60, 1110);
  s += caps(t, [{ t0: at('यमुना ने अपने'), l1: 'APNE LIYE:', l2: 'KUCH NAHI', t2: at('कुछ नहीं'), acc: RED, ...LIGHT }]);
  return s + TAG();
}, 'fade');

// 12 TATHASTU
add(at('यमराज बोले'), at('सोचिए'), (t) => {
  let w = bg('maroon') + rays(540, 1100, 20, 0.1, t) + `<circle cx="540" cy="1150" r="500" fill="url(#halo)" opacity=".55"/>` + `<rect x="-300" y="1600" width="1700" height="900" fill="#5A1E2A"/>`;
  w += yamraj({ x: 540, y: 1760, s: 1.1, eyes: 'closed', armR: -150, elbowR: 0, armL: 30, pasha: false, held: '' });
  let s = cam(540, 1250, lerp(1.15, 1.0, seg(t, at('यमराज बोले'), at('सोचिए'))), w);
  s += stamp2(t, at('तथास्तु'), 'TATHASTU', 540, 1500, { col: GOLDT });
  s += caps(t, [{ t0: at('यमराज बोले'), l1: 'YAMRAJ BOLE', ...DARK }, { t0: at('तथास्तु'), l1: '"TATHASTU."', l2: 'AISA HI HO', acc: GOLDT, ...DARK }]);
  s += flashRect(t, at('तथास्तु'), 0.3, '#FFF2C8');
  return s + TAG();
}, 'fade');

// 13 CALLBACK — Dhanteras: Nachiketa at Yama's door. Today: Yama at his sister's door.
add(at('सोचिए'), at('पाँच दिन'), (t) => {
  const today = t > at('और आज') - 0.15;
  let s = '';
  if (!today) s += cam(540, 1300, lerp(1.0, 1.12, seg(t, at('सोचिए'), at('और आज'))), bg('rage') + `<rect x="-300" y="1500" width="1700" height="900" fill="#2A0E10"/>` + yamlokGate(540, 1500, 0.95, 0, t) + nachiketa({ x: 540, y: 1720, s: 0.62, t, eyes: 'open', armL: 20, armR: -20 }));
  else s += cam(560, 1300, lerp(1.0, 1.1, seg(t, at('और आज'), at('पाँच दिन'))), bg('dusk') + sun(540, 760, 120, '#FFB86A') + `<rect x="-300" y="1500" width="1700" height="900" fill="#8E5A3A"/>` + sisterHome(700, 1500, 0.85, t, { open: true }) + yamraj({ x: 470, y: 1760, s: 0.8, eyes: 'closed', armL: 30, armR: -30, pasha: false, held: '' }) + yamunaDevi({ x: 850, y: 1760, s: 0.72, t, thali: true, armR: -110, elbowR: -40 }));
  s += today ? pill(t, at('और आज') + 0.2, 'DIN 5 · YAMUNA KA DWAAR', 60, 560) : pill(t, at('धनतेरस पर'), 'DHANTERAS · YAMLOK KA DWAAR', 60, 560);
  s += caps(t, [{ t0: at('सोचिए'), l1: 'SOCHIYE...', ...DARK }, { t0: at('धनतेरस पर'), l1: 'DHANTERAS PAR', l2: 'NACHIKETA YAMRAJ KE DWAAR', t2: at('नचिकेता'), acc: '#FF5A4A', ...DARK },
    { t0: at('और आज'), l1: 'AUR AAJ', l2: 'YAMRAJ BEHEN KE DWAAR', t2: at('ख़ुद यमराज'), acc: GOLDT, ...DARK }]);
  return s + TAG();
}, 'whip');

// 14 FIVE DAYS, FIVE DIYAS, FIVE STORIES — share with your sibling
add(at('पाँच दिन'), 999, (t) => {
  const names = ['DHANTERAS', 'CHHOTI DIWALI', 'LAKSHMI PUJA', 'GOVARDHAN', 'BHAI DOOJ'];
  let w = paperBg(t);
  names.forEach((n, i) => { const tin = at('पाँच दिन') + i * 0.18, k = eo(seg(t, tin, tin + 0.3)), lit = t > at('पाँच दिये') + i * 0.2;
    w += `<g opacity="${k.toFixed(2)}" transform="translate(${(60 + i * 196)} ${(820 + (1 - k) * 40).toFixed(0)})">${paper(0, 0, 180, 250, (i % 2 ? 2 : -2), `<text x="90" y="44" text-anchor="middle" font-family="${ANTON}" font-size="30" fill="${RED}">DIN ${i + 1}</text><g transform="translate(90 170)">${diya(0, 0, 0.62, t, i, lit, lit ? 1 : 0)}</g><text x="90" y="228" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="15" fill="${INK}">${n}</text>`, { fill: i === 4 ? '#FFF6DA' : PAPER, seed: i * 3 })}</g>`; });
  let s = cam(540, lerp(1060, 1100, seg(t, at('पाँच दिन'), at('पाँच दिन') + 10)), lerp(1.0, 1.07, seg(t, at('पाँच दिन'), at('पाँच दिन') + 10)), w);
  s += stamp2(t, at('आज पूरी'), 'POORI!', 760, 680, { rot: 8 });
  const cta = eo(seg(t, at('ये रील') - 0.1, at('ये रील') + 0.35));
  if (cta > 0) s += `<g opacity="${cta.toFixed(2)}" transform="translate(${(-60 * (1 - cta)).toFixed(0)} 0)"><path d="M40 1170 L1040 1150 L1030 1270 L50 1290Z" fill="${RED}"/><text x="90" y="1245" font-family="${ANTON}" font-size="64" fill="#FFF">SAVE KARO · POORI SERIES</text>
      <path d="M40 1300 L1040 1290 L1035 1410 L45 1420Z" fill="${INK}"/><path d="M80 1330 l60 30 l-60 30 l12 -30z" fill="${GOLDT}"/><text x="170" y="1380" font-family="${ANTON}" font-size="60" fill="${GOLDT}">BHAI / BEHEN KO BHEJO</text></g>`;
  s += caps(t, [{ t0: at('पाँच दिन'), l1: '5 DIN. 5 DIYE.', l2: '5 KAHANIYAAN.', t2: at('पाँच कहानियाँ'), acc: RED, ...LIGHT, size: 104 }]);
  return s + TAG();
}, 'zoom');

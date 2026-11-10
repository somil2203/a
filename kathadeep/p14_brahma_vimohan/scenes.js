// Brahma Vimohana. Bhagavata Purana 10.13 (the picnic on the Yamuna, the calves stray, Krishna searches; Brahma hides calves and
// boys; Krishna becomes every calf and every boy — same bodies, sticks, flutes, nature, 10.13.19; the mothers' and cows' love
// grows; a full year passes, 10.13.27-35; Brahma returns after a moment of his time, 10.13.40, sees them both in the cave and with
// Krishna, then all as four-armed Vishnu forms, 10.13.46-49) and 10.14 (Brahma falls at Krishna's feet; the boys return thinking
// only a moment passed: "you came back so quickly, we haven't eaten a morsel", 10.14.43-44).
window.HOOK = { l1: '1 साल तक हर घर में', l2: 'बेटा बनकर कृष्ण लौटे!', t1: at('उसका बेटा') - 0.05, y: 360, size: 104 };
const rays = (cx, cy, n, op, t, col = '#FFF2C6') => [...Array(n)].map((_, i) => { const a = (i * 360 / n + t * 5) * Math.PI / 180, b = a + 0.12;
  return `<path d="M${cx} ${cy} L${(cx + Math.cos(a) * 2600).toFixed(0)} ${(cy + Math.sin(a) * 2600).toFixed(0)} L${(cx + Math.cos(b) * 2600).toFixed(0)} ${(cy + Math.sin(b) * 2600).toFixed(0)}Z" fill="${col}" opacity="${op}"/>`; }).join('');
const word = (txt, k, y = 1250, col = '#FFE29A', size = 110) => k <= 0 ? '' : `<g opacity="${clamp(k * 2).toFixed(2)}" transform="translate(540 ${y}) scale(${lerp(0.8, 1, back(k)).toFixed(3)})"><text text-anchor="middle" font-family="Baloo" font-weight="800" font-size="${size}" fill="${col}" stroke="#1A0A20" stroke-width="${size * 0.08}" paint-order="stroke">${txt}</text></g>`;
const fold = { armL: 38, elbowL: -112, armR: -38, elbowR: 112 };
const VEILS = ['#C2405A', '#7B4BB7', '#2F7FB8', '#2E8A6E', '#D8432F'];
function homes(t, kids = 'krishna', hug = 0) {   // a row of Braj homes, a mother in each doorway, her child coming home
  let w = bg('dusk') + sun(540, 900, 110, '#FFB86A') + `<path d="M-300 1440 Q540 1400 1400 1440 V2400 H-300Z" fill="#B9814A"/>`;
  for (let i = 0; i < 4; i++) { const x = 140 + i * 270; w += hut(x, 1440, 0.78, ['#D49563', '#C98A5A', '#D9A070', '#C47E52'][i]);
    w += gopi2({ x: x + 70, y: 1520, s: 0.5, veil: VEILS[i], top: '#F5C04A', armL: lerp(20, 60, hug), elbowL: lerp(0, 90, hug), armR: lerp(-20, -60, hug), elbowR: lerp(0, -90, hug), t }); }
  return w;
}

// 0 HOOK — every boy coming home is Krishna
add(0, at('भागवत पुराण'), (t) => {
  const run = eo(seg(t, 0, at('ख़ुद कृष्ण लौटते') + 0.5));
  const reveal = 1;
  let w = homes(t, 'krishna', eo(seg(t, at('और किसी को') - 0.2, at('और किसी को') + 0.8)));
  for (let i = 0; i < 4; i++) { const x = 140 + i * 270 - 60, y = 1600;
    const kx = lerp(x - 260, x, run), bob = -Math.abs(Math.sin(t * 10 + i)) * 10 * (1 - run);
    w += `<g opacity="${(1 - reveal).toFixed(2)}">${gwala2({ x: kx, y: y + bob, s: 0.42, top: VEILS[(i + 2) % 5] })}</g>`;
    w += `<g opacity="${reveal.toFixed(2)}">${krishna({ x: kx, y: y + bob, s: 0.4, eyes: 'closed', armL: 20, armR: -20, glow: 0.6 * reveal })}</g>`; }
  const c = camPath(t, [[0, 330, 1380, 1.75], [at('ब्रज की हर'), 330, 1380, 1.6], [at('ख़ुद कृष्ण लौटते'), 540, 1320, 1.05], [at('और किसी को'), 400, 1380, 1.3], [at('भागवत पुराण'), 400, 1360, 1.35]]);
  let s = cam(...c, w);
  s += title('KHUD KRISHNA!', 330, 110, seg(t, at('ख़ुद कृष्ण लौटते') + 0.2, at('ख़ुद कृष्ण लौटते') + 0.5) * (1 - seg(t, at('और किसी को') - 0.1, at('और किसी को'))), '#FFE29A');
  s += title('KISI KO PATA NAHI CHALA', 330, 76, seg(t, at('और किसी को') + 0.4, at('और किसी को') + 0.7), '#FFF3DC');
  return s;
});

// 1 THE PICNIC ON THE YAMUNA — the calves wander — Krishna goes to find them
function picnic(t, boysOn = 1, calvesOn = 1, calvesGone = 0, krishnaX = 540, plates = 1) {
  let w = bg('day') + sun(860, 380, 80) + cloud(220, 420, 0.6);
  let rv = 'M-300 1180'; for (let x = -300; x <= 1400; x += 40) rv += ` L${x} ${(1180 + Math.sin(x / 80 + t * 1.6) * 8).toFixed(1)}`; rv += ' V1300 H-300Z';
  w += `<rect x="-300" y="1150" width="1700" height="40" fill="#8CBF6A"/><path d="${rv}" fill="#4F9AD8"/><rect x="-300" y="1290" width="1700" height="900" fill="#8CBF6A"/>`;
  w += tree2(120, 1330, 0.7, Math.sin(t * 2) * 3) + tree2(980, 1340, 0.6, Math.sin(t * 2 + 1) * 3);
  [[180, 1540], [380, 1620], [700, 1620], [900, 1540]].forEach(([x, y], i) => {
    if (plates) w += `<ellipse cx="${x}" cy="${y + 10}" rx="60" ry="16" fill="#3E8A4A"/><circle cx="${x - 14}" cy="${y + 2}" r="12" fill="#F29A26"/><circle cx="${x + 14}" cy="${y + 4}" r="10" fill="#FFF6E2"/>`;
    if (boysOn > 0) w += `<g opacity="${boysOn.toFixed(2)}">${gwala2({ x, y: y - 10, s: 0.5, top: VEILS[i], armR: -60 + Math.sin(t * 6 + i) * 20, elbowR: -90 })}</g>`; });
  for (let i = 0; i < 3; i++) { const x = 300 + i * 220 + calvesGone * 900, y = 1400 + (i % 2) * 30;
    if (calvesOn > 0) w += `<g opacity="${calvesOn.toFixed(2)}">${calf({ x, y, s: 0.75, t, ph: calvesGone > 0 ? t * 8 : 0, flip: calvesGone > 0 })}</g>`; }
  if (krishnaX !== null) w += krishna({ x: krishnaX, y: 1580, s: 0.6, eyes: 'open', armL: 20, armR: -60, elbowR: -90 });
  return w;
}
add(at('भागवत पुराण'), at('ये सब देख'), (t) => {
  const gone = eio(seg(t, at('बछड़े चरते') + 0.3, at('कृष्ण बछड़ों') + 0.2));
  const walk = eio(seg(t, at('कृष्ण बछड़ों') + 0.3, at('ये सब देख')));
  let w = picnic(t, 1, 1, gone, lerp(540, 1300, walk));
  const c = camPath(t, [[at('भागवत पुराण'), 540, 1300, 1.2], [at('कृष्ण ग्वाल-बालों'), 540, 1350, 1.0], [at('बछड़े चरते') + 0.4, 700, 1300, 1.0], [at('ये सब देख'), 760, 1300, 1.1]]);
  let s = cam(...c, w);
  s += title('BHAGAVAT 10.13', 330, 70, seg(t, at('भागवत पुराण'), at('भागवत पुराण') + 0.3) * (1 - seg(t, at('एक दिन यमुना') - 0.1, at('एक दिन यमुना'))), '#1C2347');
  s += title('YAMUNA KINAARE BHOJAN', 330, 76, seg(t, at('एक दिन यमुना'), at('एक दिन यमुना') + 0.3) * (1 - seg(t, at('बछड़े चरते') - 0.1, at('बछड़े चरते'))), '#1C2347');
  s += title('BACHHDE DOOR NIKAL GAYE', 330, 76, seg(t, at('बछड़े चरते'), at('बछड़े चरते') + 0.3) * (1 - seg(t, at('कृष्ण बछड़ों') - 0.1, at('कृष्ण बछड़ों'))), '#1C2347');
  s += title('KRISHNA DHOONDHNE GAYE', 330, 76, seg(t, at('कृष्ण बछड़ों'), at('कृष्ण बछड़ों') + 0.3), '#1C2347');
  return s;
}, 'fade');

// 2 BRAHMA WATCHES — "is this child really God?"
add(at('ये सब देख'), at('ब्रह्मा ने सारे'), (t) => {
  let w = bg('sky') + cloud(300, 1150, 1.6) + cloud(780, 1180, 1.5) + cloud(540, 1220, 1.4);
  w += brahma({ x: 540, y: 1180, s: 0.85, t, glow: 0.6, armL: t > at('उन्होंने सोचा') ? 30 : 50, elbowL: t > at('उन्होंने सोचा') ? 110 : 70 });
  w += `<g transform="translate(0 0)"><rect x="-300" y="1400" width="1700" height="900" fill="#8CBF6A" opacity=".85"/></g>`;
  for (let i = 0; i < 4; i++) w += gwala2({ x: 200 + i * 230, y: 1700, s: 0.4, top: VEILS[i] });
  w += bubble(780, 560, 'सच में भगवान?', seg(t, at('देखूँ') - 0.2, at('देखूँ') + 0.3));
  let s = cam(540, lerp(1000, 1100, seg(t, at('ये सब देख'), at('ब्रह्मा ने सारे'))), lerp(1.15, 1.0, seg(t, at('ये सब देख'), at('ब्रह्मा ने सारे'))), w);
  s += title('SRISHTI KE RACHAYITA', 330, 80, seg(t, at('सृष्टि'), at('सृष्टि') + 0.3) * (1 - seg(t, at('उन्होंने सोचा') - 0.1, at('उन्होंने सोचा'))), '#1C2347', 'Baloo', 800, 'BRAHMA JI', '#1C2347');
  s += title('PAREEKSHA!', 330, 120, seg(t, at('उन्होंने सोचा'), at('उन्होंने सोचा') + 0.3) * (1 - seg(t, at('देखूँ') - 0.3, at('देखूँ'))), '#7A1E12');
  return s;
}, 'up');

// 3 HIDDEN IN A CAVE
add(at('ब्रह्मा ने सारे'), at('कृष्ण लौटे'), (t) => {
  const suck = eio(seg(t, at('ब्रह्मा ने सारे') + 0.2, at('एक गुफा') + 0.8));
  let w = bg('dusk') + cave(540, 1300, 1.3, 0.3 * suck) + `<rect x="-300" y="1300" width="1700" height="900" fill="#6E5A4A"/>`;
  for (let i = 0; i < 8; i++) { const x0 = 120 + (i % 4) * 280, y0 = 1650 + Math.floor(i / 4) * 140, k = clamp(suck * 1.3 - i * 0.04);
    const x = lerp(x0, 540, k), y = lerp(y0, 1180, k), sc = lerp(0.42, 0.06, k);
    w += `<g opacity="${(1 - k * 0.9).toFixed(2)}" transform="rotate(${(k * 200).toFixed(0)} ${x} ${y - 100})">${i % 2 ? calf({ x, y, s: sc * 1.6, t }) : gwala2({ x, y, s: sc, top: VEILS[i % 5] })}</g>`; }
  w += `<g opacity=".9">${brahma({ x: 880, y: 760, s: 0.35, t, glow: 0.5 })}</g>`;
  let s = cam(540, 1250, lerp(1.0, 1.15, suck), w);
  s += title('SAB GUFA MEIN CHHIPA DIYE', 330, 76, seg(t, at('एक गुफा'), at('एक गुफा') + 0.3), '#FFE29A');
  return s;
}, 'whip');

// 4 KRISHNA RETURNS — no calves, no friends — he understands
add(at('कृष्ण लौटे'), at('और तब कृष्ण'), (t) => {
  let w = picnic(t, 0, 0, 0, 540, 1);
  if (t > at('वो समझ')) w += `<g opacity="${eo(seg(t, at('वो समझ'), at('वो समझ') + 0.6)).toFixed(2)}">${brahma({ x: 880, y: 700, s: 0.3, t, glow: 0.4 })}</g>`;
  let s = cam(540, 1350, lerp(1.0, 1.35, seg(t, at('कृष्ण लौटे'), at('और तब कृष्ण'))), w);
  s += title('NA BACHHDE, NA DOST', 330, 92, seg(t, at('न बछड़े'), at('न बछड़े') + 0.3) * (1 - seg(t, at('वो समझ') - 0.1, at('वो समझ'))), '#1C2347');
  s += title('YE KISKA KHEL HAI...', 330, 92, seg(t, at('वो समझ') + 0.6, at('वो समझ') + 0.9), '#1C2347');
  return s;
}, 'fade');

// 5 HE BECOMES EVERY CALF AND EVERY BOY — same faces, sticks, flutes, mischief
const SLOTS = [[150, 1600], [380, 1680], [700, 1680], [930, 1600], [260, 1430], [540, 1460], [820, 1430]];
add(at('और तब कृष्ण'), at('शाम को'), (t) => {
  const split = eio(seg(t, at('वो ख़ुद') - 0.2, at('वो ख़ुद') + 0.9));
  const toCalf = eo(seg(t, at('हर बछड़ा बन') - 0.1, at('हर बछड़ा बन') + 0.6));
  const toBoy = eo(seg(t, at('हर ग्वाल-बाल बन') - 0.1, at('हर ग्वाल-बाल बन') + 0.6));
  const detail = t > at('वही चेहरे') - 0.1;
  let w = bg('gold') + rays(540, 1100, 18, 0.12, t) + `<rect x="-300" y="1400" width="1700" height="900" fill="#B9813E"/>`;
  if (!detail) {
    if (split < 0.05) w += krishna({ x: 540, y: 1640, s: 0.8, eyes: 'closed', armL: 20, armR: -20, glow: 0.9 * eo(seg(t, at('और तब कृष्ण'), at('और तब कृष्ण') + 1)) });
    else SLOTS.forEach(([x, y], i) => { const px = lerp(540, x, split), py = lerp(1640, y, split), calfSlot = i >= 4;
      const k = calfSlot ? toCalf : toBoy;
      w += `<g opacity="${(1 - k).toFixed(2)}">${krishna({ x: px, y: py, s: 0.45, eyes: 'closed', armL: 20, armR: -20, glow: 0.4 })}</g>`;
      if (k > 0) w += `<g opacity="${k.toFixed(2)}">${calfSlot ? calf({ x: px + 60, y: py, s: 0.8, t }) : gwala2({ x: px, y: py, s: 0.48, top: VEILS[i % 5], stick: true })}</g>`; });
  } else {
    const items = [['वही चेहरे', at('वही चेहरे')], ['वही लाठियाँ', at('वही लाठियाँ')], ['वही बाँसुरी', at('वही बाँसुरी')], ['वही शरारतें', at('वही शरारतें')]];
    let cur = 0; items.forEach(([, t0], i) => { if (t >= t0 - 0.1) cur = i; });
    const jump = cur === 3 ? -Math.abs(Math.sin(t * 9)) * 40 : 0;
    w += gwala2({ x: 540, y: 1700 + jump, s: 1.0, top: VEILS[cur], stick: cur === 1, eyes: 'closed', armR: cur === 2 ? -80 : -20, elbowR: cur === 2 ? -70 : -20 });
    if (cur === 2) w += `<rect x="560" y="1290" width="200" height="16" rx="8" fill="#8C3B2E" transform="rotate(-10 560 1290)"/>`;
    w += word(items[cur][0], seg(t, items[cur][1] - 0.1, items[cur][1] + 0.2), 1130, '#4A1A08', 120);
  }
  let s = cam(540, detail ? 1150 : 1300, detail ? 1.35 : 1.0, w);
  s += title('JO KOI SOCH BHI NAHI SAKTA', 330, 70, seg(t, at('जो कोई'), at('जो कोई') + 0.3) * (1 - seg(t, at('वो ख़ुद') - 0.1, at('वो ख़ुद'))), '#4A1A08');
  s += title('HAR BACHHDA', 330, 110, seg(t, at('हर बछड़ा बन'), at('हर बछड़ा बन') + 0.3) * (1 - seg(t, at('हर ग्वाल-बाल बन') - 0.1, at('हर ग्वाल-बाल बन'))), '#4A1A08');
  s += title('HAR GWAAL-BAAL', 330, 110, seg(t, at('हर ग्वाल-बाल बन'), at('हर ग्वाल-बाल बन') + 0.3) * (1 - seg(t, at('वही चेहरे') - 0.2, at('वही चेहरे'))), '#4A1A08');
  s += flashRect(t, at('वो ख़ुद'), 0.3, '#FFF2C8');
  return s;
}, 'zoom');

// 6 EVENING — every calf to its cow, every boy to his mother; their love grows
add(at('शाम को'), at('ऐसे पूरा'), (t) => {
  const run = eo(seg(t, at('शाम को'), at('हर बालक अपनी') + 0.6));
  const hug = eo(seg(t, at('हर बालक अपनी'), at('हर बालक अपनी') + 0.8));
  let w = homes(t, 'gwala', hug);
  for (let i = 0; i < 4; i++) { const x = 140 + i * 270 - 30; w += gwala2({ x: lerp(x - 300, x, run), y: 1590 - Math.abs(Math.sin(t * 10 + i)) * 10 * (1 - run), s: 0.4, top: VEILS[(i + 2) % 5] }); }
  const love = seg(t, at('और माँओं'), at('ऐसे पूरा'));
  for (let i = 0; i < 16; i++) { const ph = (t * 0.6 + rnd(i)) % 1, x = 140 + (i % 4) * 270 + Math.sin(t * 2 + i) * 20, y = 1350 - ph * 500, sz = lerp(14, 34, love) * (0.7 + rnd(i + 3) * 0.6);
    if (love > 0) w += `<path d="M0 ${sz * 0.3} C${-sz} ${-sz * 0.5} ${-sz * 0.4} ${-sz * 1.2} 0 ${-sz * 0.5} C${sz * 0.4} ${-sz * 1.2} ${sz} ${-sz * 0.5} 0 ${sz * 0.3}Z" fill="#FF5A7A" opacity="${(love * (1 - ph)).toFixed(2)}" transform="translate(${x.toFixed(0)} ${y.toFixed(0)})"/>`; }
  let s = cam(540, 1350, lerp(1.0, 1.1, seg(t, at('शाम को'), at('ऐसे पूरा'))), w);
  s += title('MAA KA PYAAR', 330, 110, seg(t, at('और माँओं'), at('और माँओं') + 0.3) * (1 - seg(t, at('पहले से भी') - 0.1, at('पहले से भी'))), '#FFE29A');
  s += title('PEHLE SE BHI ZYADA', 330, 96, seg(t, at('पहले से भी'), at('पहले से भी') + 0.3), '#FFE29A');
  return s;
}, 'fade');

// 7 A WHOLE YEAR — 12 months tick by
add(at('ऐसे पूरा'), at('फिर ब्रह्मा लौटे'), (t) => {
  const p = seg(t, at('ऐसे पूरा') + 0.2, at('फिर ब्रह्मा लौटे') - 0.2), m = Math.min(12, 1 + Math.floor(p * 12));
  const skies = ['day', 'dawn', 'rain', 'storm', 'day', 'dusk'];
  let w = bg(skies[m % skies.length]) + `<path d="M-300 1400 Q540 1360 1400 1400 V2400 H-300Z" fill="${m > 8 ? '#C9D6C9' : '#8CBF6A'}"/>`;
  if (m >= 4 && m <= 6) w += rain(t, 0.8, 0.5, 0.15);
  w += tree2(540, 1420, 1.2, Math.sin(t * 3) * 4);
  let s = cam(540, 1100, 1.0, w);
  s += counter(m, 12, 'MAHINA', 70, 360, 1);
  s += title('POORA EK SAAL', 560, 110, seg(t, at('ऐसे पूरा') + 0.3, at('ऐसे पूरा') + 0.6), '#FFF3DC');
  return s;
}, 'zoom');

// 8 BRAHMA RETURNS — they are in the cave AND with Krishna
add(at('फिर ब्रह्मा लौटे'), at('और फिर उन्होंने'), (t) => {
  const split = eo(seg(t, at('गुफा में भी') - 0.2, at('गुफा में भी') + 0.4));
  const right = eo(seg(t, at('और कृष्ण के साथ') - 0.2, at('और कृष्ण के साथ') + 0.4));
  let w = bg('dusk') + `<rect x="-300" y="1450" width="1700" height="900" fill="#B9814A"/>`;
  w += brahma({ x: 540, y: 820, s: 0.5, t, glow: 0.5 });
  w += `<g opacity="${split.toFixed(2)}">${cave(280, 1500, 0.75, 0.6)}${gwala2({ x: 250, y: 1490, s: 0.3, top: '#C2405A' })}${gwala2({ x: 320, y: 1490, s: 0.3, top: '#2F7FB8' })}<path d="M220 1360 q8 -10 16 0 M300 1350 q8 -10 16 0" stroke="#FFF6DA" stroke-width="3" fill="none"/></g>`;
  w += `<g opacity="${right.toFixed(2)}">${krishna({ x: 800, y: 1640, s: 0.45, eyes: 'closed', armL: 20, armR: -20, glow: 0.5 })}${gwala2({ x: 680, y: 1650, s: 0.4, top: '#C2405A' })}${gwala2({ x: 930, y: 1650, s: 0.4, top: '#2F7FB8' })}</g>`;
  w += `<path d="M540 1180 V1880" stroke="#FFF3DC" stroke-width="6" stroke-dasharray="20 16" opacity="${split.toFixed(2)}"/>`;
  if (right > 0.5) w += `<text x="540" y="560" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="140" fill="#FFE29A" stroke="#14060A" stroke-width="10" paint-order="stroke" opacity="${right.toFixed(2)}">? ? ?</text>`;
  let s = cam(540, 1250, 1.0, w);
  s += title('BRAHMA LAUTE', 330, 100, seg(t, at('फिर ब्रह्मा लौटे'), at('फिर ब्रह्मा लौटे') + 0.3) * (1 - seg(t, at('गुफा में भी') - 0.2, at('गुफा में भी'))), '#FFF3DC');
  s += title('GUFA MEIN BHI · BAAHAR BHI', 330, 70, seg(t, at('गुफा में भी'), at('गुफा में भी') + 0.3), '#FFF3DC');
  return s;
}, 'fade');

// 9 EVERY ONE BECOMES CHATURBHUJ VISHNU
add(at('और फिर उन्होंने'), at('ब्रह्मा का घमंड'), (t) => {
  const v = eo(seg(t, at('चतुर्भुज') - 0.3, at('चतुर्भुज') + 0.6));
  let w = `<rect x="-300" y="-300" width="1700" height="2600" fill="#0B0620"/>` + stars(t, 80) + `<g opacity="${v.toFixed(2)}">${rays(540, 1100, 22, 0.12, t)}</g>`;
  [[200, 1500], [540, 1520], [880, 1500], [360, 1830], [720, 1830]].forEach(([x, y], i) => {
    w += `<g opacity="${(1 - v).toFixed(2)}">${i % 2 ? calf({ x, y, s: 0.9, t }) : gwala2({ x, y, s: 0.5, top: VEILS[i] })}</g>`;
    w += `<g opacity="${v.toFixed(2)}">${vishnu4({ x, y, s: 0.5, t, glow: 0.7 })}</g>`; });
  let s = cam(540, 1300, lerp(1.0, 0.95, v), w);
  s += word('चतुर्भुज विष्णु', v, 600, '#FFE29A', 120);
  s += flashRect(t, at('चतुर्भुज'), 0.35, '#FFF2C8');
  return s;
}, 'iris');

// 10 BRAHMA FALLS AT KRISHNA'S FEET
add(at('ब्रह्मा का घमंड'), at('और जब दोस्त'), (t) => {
  const bow = eo(seg(t, at('वो कृष्ण के चरणों') - 0.2, at('वो कृष्ण के चरणों') + 0.8));
  let w = bg('gold') + rays(400, 1000, 18, 0.12, t) + `<rect x="-300" y="1560" width="1700" height="900" fill="#B9813E"/>`;
  w += krishna({ x: 330, y: 1640, s: 0.85, eyes: 'closed', armL: 20, armR: -60, elbowR: -80, glow: 0.9 });
  w += `<g transform="rotate(${(-28 * bow).toFixed(1)} 760 1700)">${brahma({ x: 760, y: 1700, s: 0.62, t, folded: true, armL: 40, elbowL: 100, armR: -40, elbowR: -100 })}</g>`;
  let s = cam(540, 1250, lerp(1.1, 1.0, bow), w);
  s += title('GHAMAND CHOOR', 330, 110, seg(t, at('ब्रह्मा का घमंड'), at('ब्रह्मा का घमंड') + 0.3) * (1 - seg(t, at('वो कृष्ण के चरणों') - 0.1, at('वो कृष्ण के चरणों'))), '#4A1A08');
  s += title('CHARANON MEIN', 330, 110, seg(t, at('वो कृष्ण के चरणों'), at('वो कृष्ण के चरणों') + 0.3), '#4A1A08', 'Baloo', 800, 'BHAGAVAT 10.14', '#4A1A08');
  return s;
}, 'fade');

// 11 THE BOYS RETURN — "so quick? we haven't eaten a bite!"
add(at('और जब दोस्त'), at('उनके लिए'), (t) => {
  let w = picnic(t, 1, 1, 0, 540, 1);
  w += bubble(380, 1140, 'इतनी जल्दी?', seg(t, at('कान्हा, इतनी') - 0.1, at('कान्हा, इतनी') + 0.3) * (1 - seg(t, at('हमने तो') - 0.1, at('हमने तो'))));
  w += bubble(700, 1140, 'एक कौर भी नहीं!', seg(t, at('हमने तो') - 0.1, at('हमने तो') + 0.3)).replace('width="400"', 'width="520"').replace('x="-200"', 'x="-260"');
  let s = cam(540, 1360, lerp(1.0, 1.15, seg(t, at('और जब दोस्त'), at('उनके लिए'))), w);
  s += title('DOST LAUTE', 330, 100, seg(t, at('और जब दोस्त') + 0.3, at('और जब दोस्त') + 0.6) * (1 - seg(t, at('कान्हा, इतनी') - 0.2, at('कान्हा, इतनी'))), '#1C2347');
  return s;
}, 'fade');

// 12 ONE YEAR = ONE MOMENT
add(at('उनके लिए'), at('कल — दीपोत्सव'), (t) => {
  let w = `<rect x="-300" y="-300" width="1700" height="2600" fill="#0B0620"/>` + stars(t, 80);
  const k = seg(t, at('बस एक पल') - 0.2, at('बस एक पल') + 0.2);
  w += `<g transform="translate(540 930)"><path d="M-130 -220 L130 -220 L20 0 L130 220 L-130 220 L-20 0Z" fill="none" stroke="#F5C04A" stroke-width="16" stroke-linejoin="round"/>
        <path d="M${-100 + 80 * k} -190 L${100 - 80 * k} -190 L0 -20Z" fill="#FFE29A"/><path d="M${-100 * k} 190 L${100 * k} 190 L0 ${190 - 160 * k}Z" fill="#FFE29A"/></g>`;
  let s = cam(540, 960, 1.0, w);
  s += word('1 साल', seg(t, at('उनके लिए'), at('उनके लिए') + 0.3), 560, '#FFFFFF', 140);
  s += word('= 1 पल', seg(t, at('बस एक पल'), at('बस एक पल') + 0.3), 1310, '#FFE29A', 140);
  return s;
}, 'zoom');

// 13 TOMORROW — Bhai Dooj, the last diya
add(at('कल — दीपोत्सव'), 999, (t) => {
  const yk = eo(seg(t, at('भाई दूज'), at('भाई दूज') + 1.0));
  let w = `<g transform="translate(0 ${(-260 * yk).toFixed(1)})" opacity="${(1 - 0.5 * yk).toFixed(2)}">` + tracker(t, 4, 4, at('भाई दूज')) + `</g>`;
  let riv = 'M-200 1560'; for (let x = -200; x <= 1300; x += 40) riv += ` L${x} ${(1560 + Math.sin(x / 90 + t * 2) * 10).toFixed(1)}`; riv += ' V2400 H-200Z';
  w += `<g opacity="${yk.toFixed(2)}"><circle cx="540" cy="1260" r="420" fill="url(#moonglow)"/><circle cx="540" cy="1260" r="190" fill="#FFF3D1" opacity=".9"/><path d="${riv}" fill="#2A3A7A"/>`
    + yamraj(400, 1580, 0.78).replace(/#1B1030/g, '#2C2152') + yamuna(690, 1580, 0.8).replace(/#1B1030/g, '#2C2152') + `</g>`;
  let s = cam(540, 960, lerp(1.0, 1.06, seg(t, at('कल — दीपोत्सव'), at('कल — दीपोत्सव') + 7)), w);
  s += title('KAL · AAKHIRI DIYA', 520, 64, seg(t, at('कल — दीपोत्सव'), at('कल — दीपोत्सव') + 0.3) * (1 - yk), '#FFF3DC');
  s += title('BHAI DOOJ', 330, 140, seg(t, at('भाई दूज'), at('भाई दूज') + 0.3), '#F5C04A', 'Baloo', 800, 'YAMRAJ + YAMUNA');
  return s;
}, 'fade');

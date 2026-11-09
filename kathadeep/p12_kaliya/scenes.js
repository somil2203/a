// Kaliya Daman. Bhagavata Purana 10.15.47-52 (cowherds and cows drink the poisoned water and fall; Krishna revives them with
// his nectar glance), 10.16.4-7 (birds flying over the pool fall; Krishna climbs the kadamba and jumps), 10.16.9 (coils),
// 10.16.15-22 (Vraja on the bank, Balarama calm), 10.16.25-30 (Krishna expands, frees himself, dances on the hoods),
// 10.16.31-53 (the naga-patnis pray), 10.16.60-63 (Ramanaka island; "my footprints on your hoods: Garuda will not eat you").
const rays = (cx, cy, n, op, t, col = '#FFF2C6') => [...Array(n)].map((_, i) => { const a = (i * 360 / n + t * 5) * Math.PI / 180, b = a + 0.12;
  return `<path d="M${cx} ${cy} L${(cx + Math.cos(a) * 2400).toFixed(0)} ${(cy + Math.sin(a) * 2400).toFixed(0)} L${(cx + Math.cos(b) * 2400).toFixed(0)} ${(cy + Math.sin(b) * 2400).toFixed(0)}Z" fill="${col}" opacity="${op}"/>`; }).join('');
const fold = { armL: 38, elbowL: -112, armR: -38, elbowR: 112 };
const lying = (svg, x, y, k) => `<g transform="rotate(${(-80 * k).toFixed(1)} ${x} ${y})">${svg}</g>`;
const splash = (x, y, t, t0, s = 1) => { const k = seg(t, t0, t0 + 0.8); if (t < t0 || k >= 1) return '';
  let g = `<ellipse cx="${x}" cy="${y}" rx="${(40 + 220 * k) * s}" ry="${(12 + 50 * k) * s}" fill="none" stroke="#9FF0C0" stroke-width="${(10 * (1 - k)).toFixed(1)}"/>`;
  for (let i = 0; i < 12; i++) { const a = -Math.PI * (0.1 + 0.8 * rnd(i)), v = 300 + rnd(i + 1) * 300; g += `<circle cx="${(x + Math.cos(a) * v * k * s).toFixed(0)}" cy="${(y + (Math.sin(a) * v * k + 600 * k * k) * s).toFixed(0)}" r="${(10 * (1 - k) * s).toFixed(1)}" fill="#7CE0A8"/>`; }
  return g; };
function bank(t, sky = 'rain') {
  let w = bg(sky) + cloud(200, 380, 0.7, '#C9D6C9', '#A9B8A9') + cloud(860, 300, 0.5, '#C9D6C9', '#A9B8A9');
  w += `<path d="M-300 1360 Q540 1300 1400 1360 V1480 H-300Z" fill="#6E9A5A"/><path d="M-300 1440 Q540 1400 1400 1440 V1500 H-300Z" fill="#5E8A4A"/>`;
  return w;
}

// 0 HOOK — water so poisonous that birds fell from the sky; a child jumped in
add(0, at('भागवत पुराण'), (t) => {
  const c = camPath(t, [[0, 540, 900, 1.0], [at('कि ऊपर') + 1.6, 540, 1000, 1.0], [at('और एक बालक'), 740, 900, 1.25], [at('उसी पानी') + 0.4, 700, 1000, 1.05], [at('भागवत पुराण'), 540, 1250, 1.1]]);
  let w = bg('rain') + `<rect x="-300" y="-300" width="1700" height="2600" fill="#2A4A30" opacity=".35"/>`;
  w += kadamb(840, 1440, 0.95, t);
  w += poisonWater(t, 1420) + fumes(t, 1420, 9, 0.42);
  for (let i = 0; i < 5; i++) { const fallT = at('कि ऊपर') + 0.4 + i * 0.35, f = seg(t, fallT, fallT + 1.2);
    const x = 140 + i * 170 + Math.sin(t * 2 + i) * 20 + (t - fallT) * 30 * (f === 0 ? 1 : 0), y = 420 + (i % 2) * 90 + 1100 * f * f;
    if (f < 1) w += bird(x, y, 0.9, t * 12 + i, f > 0); }
  const jump = seg(t, at('उसी पानी') + 0.2, at('उसी पानी') + 1.2);
  if (t > at('और एक बालक') - 0.3 && jump < 1) {
    const kx = lerp(770, 560, jump), ky = lerp(1020, 1460, jump * jump) - Math.sin(jump * Math.PI) * 160;
    w += `<g transform="rotate(${(lerp(0, 160, jump)).toFixed(1)} ${kx} ${ky - 200})">${krishna({ x: kx, y: ky, s: 0.5, armL: jump > 0 ? 170 : 20, armR: jump > 0 ? -170 : -20, eyes: 'open' })}</g>`;
  }
  w += splash(560, 1440, t, at('उसी पानी') + 1.2, 1.2);
  let s = cam(...c, w);
  s += title('ZEHREELI YAMUNA', 300, 92, seg(t, 0.1, 0.4) * (1 - seg(t, at('कि ऊपर') - 0.1, at('कि ऊपर'))), '#7CFF9A');
  s += title('PAKSHI BHI GIR JAATE', 300, 80, seg(t, at('कि ऊपर') + 0.4, at('कि ऊपर') + 0.7) * (1 - seg(t, at('और एक बालक') - 0.2, at('और एक बालक'))), '#FFF3DC');
  s += title('AUR EK BAALAK...', 300, 96, seg(t, at('और एक बालक'), at('और एक बालक') + 0.3), '#FFE29A');
  return s;
});

// 1 THE POOL — Kaliya rises, many hoods, spitting poison
add(at('भागवत पुराण'), at('एक दिन'), (t) => {
  const rise = eo(seg(t, at('कालिया नाग') - 0.6, at('कालिया नाग') + 0.8));
  const n = Math.max(1, Math.round(lerp(1, 7, eo(seg(t, at('कई फनों') - 0.1, at('कई फनों') + 1.2)))));
  const c = camPath(t, [[at('भागवत पुराण'), 540, 1300, 1.15], [at('कालिया नाग'), 540, 1150, 1.0], [at('कई फनों') + 1.2, 540, 1050, 0.95], [at('एक दिन'), 540, 980, 1.1]]);
  let w = bg('night') + stars(t, 40) + moon(860, 320, 46);
  w += `<g transform="${shake(t, at('कालिया नाग'), 0.8, 12)}">` + kaliya({ x: 540, y: 1560, s: 1.25, t, rise, n }) + `</g>`;
  if (t > at('ज़हर उगलता') - 0.2) for (let i = 0; i < 30; i++) { const ph = (t * 1.2 + rnd(i)) % 1, a = rnd(i + 5) * Math.PI * 2;
    w += `<circle cx="${(540 + Math.cos(a) * ph * 420).toFixed(0)}" cy="${(880 + Math.sin(a) * ph * 260 + ph * ph * 300).toFixed(0)}" r="${(12 * (1 - ph)).toFixed(1)}" fill="#7CFF9A" opacity="${(0.8 * (1 - ph)).toFixed(2)}"/>`; }
  w += poisonWater(t, 1500) + fumes(t, 1500, 9, 0.35);
  let s = cam(...c, w);
  s += title('BHAGAVAT 10.16', 300, 70, seg(t, at('भागवत पुराण'), at('भागवत पुराण') + 0.3) * (1 - seg(t, at('कालिया नाग') - 0.2, at('कालिया नाग'))), '#FFF3DC');
  s += title('KALIYA NAAG', 280, 140, seg(t, at('कालिया नाग'), at('कालिया नाग') + 0.3) * (1 - seg(t, at('ज़हर उगलता') - 0.2, at('ज़हर उगलता'))), '#7CFF9A');
  s += title('ZEHAR!', 280, 150, seg(t, at('ज़हर उगलता'), at('ज़हर उगलता') + 0.3), '#7CFF9A');
  return s;
}, 'zoom');

// 2 THE BOYS AND COWS DRINK, FALL — AND KRISHNA'S NECTAR GLANCE REVIVES THEM
add(at('एक दिन'), at('फिर कृष्ण कदंब'), (t) => {
  const fall = eio(seg(t, at('और बेहोश') - 0.1, at('और बेहोश') + 0.8)) * (1 - eio(seg(t, at('सबको फिर') + 0.2, at('सबको फिर') + 1.2)));
  const gaze = seg(t, at('कृष्ण ने अपनी') + 0.4, at('सबको फिर') + 1.6);
  const c = camPath(t, [[at('एक दिन'), 520, 1250, 1.2], [at('और बेहोश') + 0.6, 480, 1300, 1.15], [at('कृष्ण ने अपनी'), 640, 1200, 1.0], [at('फिर कृष्ण कदंब'), 600, 1150, 1.0]]);
  let w = bank(t) + poisonWater(t, 1500) + fumes(t, 1500, 5, 0.25);
  const drink = t < at('और बेहोश') ? Math.sin(t * 3) * 4 : 0;
  w += lying(cow({ x: 180, y: 1470, s: 0.55, t, headTilt: 20 + drink }), 180, 1470, fall) + lying(cow({ x: 470, y: 1480, s: 0.5, t, headTilt: 22 - drink, flip: true }), 470, 1480, fall);
  w += lying(gwala2({ x: 320, y: 1490, s: 0.55, top: '#3E8E5A', armR: -60, elbowR: -60 }), 320, 1490, fall) + lying(gwala2({ x: 620, y: 1490, s: 0.52, top: '#D8432F', armL: 60, elbowL: 60 }), 620, 1490, fall);
  const kk = eo(seg(t, at('कृष्ण ने अपनी') - 0.4, at('कृष्ण ने अपनी') + 0.4));
  if (kk > 0) {
    w += `<g opacity="${kk.toFixed(2)}">${krishna({ x: 880, y: 1500, s: 0.7, eyes: 'open', armL: 30, armR: -30, glow: 0.9 })}</g>`;
    if (gaze > 0 && gaze < 1) for (let i = 0; i < 4; i++) w += `<path d="M860 ${1500 - 0.7 * 500} L${[180, 320, 470, 620][i]} 1440" stroke="#FFE7A0" stroke-width="${(22 * Math.sin(gaze * Math.PI)).toFixed(1)}" opacity=".55" stroke-linecap="round"/>`;
  }
  if (gaze > 0) w += dust(t, 30, '#FFE7A0', 60);
  let s = cam(...c, w);
  s += title('PAANI PI LIYA', 300, 96, seg(t, at('एक दिन') + 0.8, at('एक दिन') + 1.1) * (1 - seg(t, at('और बेहोश') - 0.2, at('और बेहोश'))), '#1C2347');
  s += title('BEHOSH!', 300, 140, seg(t, at('और बेहोश'), at('और बेहोश') + 0.3) * (1 - seg(t, at('कृष्ण ने अपनी') - 0.2, at('कृष्ण ने अपनी'))), '#7A1E12');
  s += title('AMRIT DRISHTI', 300, 110, seg(t, at('कृष्ण ने अपनी') + 0.6, at('कृष्ण ने अपनी') + 0.9) * (1 - seg(t, at('सबको फिर') + 0.6, at('सबको फिर') + 0.9)), '#7A1E12');
  s += title('PHIR SE JEEVIT', 300, 110, seg(t, at('सबको फिर') + 1.0, at('सबको फिर') + 1.3), '#7A1E12');
  return s;
}, 'fade');

// 3 THE KADAMBA — he climbs and leaps
add(at('फिर कृष्ण कदंब'), at('कालिया ने उन्हें'), (t) => {
  const climb = eio(seg(t, at('फिर कृष्ण कदंब') + 0.3, at('और ज़हरीले') - 0.2));
  const jump = seg(t, at('छलाँग') - 0.1, at('छलाँग') + 0.9);
  const c = camPath(t, [[at('फिर कृष्ण कदंब'), 700, 1200, 1.05], [at('और ज़हरीले'), 720, 900, 1.2], [at('छलाँग'), 640, 1000, 1.0], [at('कालिया ने उन्हें'), 540, 1200, 1.05]]);
  let w = bank(t) + kadamb(760, 1460, 1.15, t);
  let kx = 760, ky = lerp(1460, 1060, climb);
  if (jump > 0) { kx = lerp(860, 520, jump); ky = lerp(1060, 1560, jump * jump) - Math.sin(jump * Math.PI) * 220; }
  if (jump < 1) w += `<g transform="rotate(${lerp(0, 170, jump).toFixed(1)} ${kx} ${ky - 220})">${krishna({ x: jump > 0 ? kx : lerp(760, 860, eio(seg(t, at('और ज़हरीले') - 0.4, at('और ज़हरीले')))), y: ky, s: 0.62, eyes: 'open', armL: jump > 0 ? 175 : 40, armR: jump > 0 ? -175 : -40 })}</g>`;
  w += poisonWater(t, 1500) + fumes(t, 1500, 7, 0.3) + splash(520, 1520, t, at('छलाँग') + 0.9, 1.3);
  let s = cam(...c, w);
  s += title('KADAMB KA PED', 300, 92, seg(t, at('फिर कृष्ण कदंब') + 0.6, at('फिर कृष्ण कदंब') + 0.9) * (1 - seg(t, at('छलाँग') - 0.2, at('छलाँग'))), '#1C2347');
  s += title('CHHALAANG!', 300, 140, seg(t, at('छलाँग'), at('छलाँग') + 0.25), '#7A1E12');
  s += flashRect(t, at('छलाँग') + 0.9, 0.3, '#C8FFE0');
  return s;
}, 'whip');

// 4 COILS — the bank weeps; only Balarama is calm
add(at('कालिया ने उन्हें'), at('तभी कृष्ण'), (t) => {
  const onBank = t > at('किनारे पर') - 0.3;
  if (!onBank) {
    const sq = 1 + 0.03 * Math.sin(t * 6);
    let w = bg('night') + stars(t, 30) + poisonWater(t, 1380) + fumes(t, 1380, 6, 0.3);
    w += krishna({ x: 540, y: 1560, s: 0.7, eyes: 'closed', armL: 20, armR: -20 });
    for (let i = 0; i < 4; i++) w += `<ellipse cx="540" cy="${1560 - 80 - i * 75}" rx="${(140 * sq).toFixed(1)}" ry="40" fill="none" stroke="#1F3A5A" stroke-width="44"/><ellipse cx="540" cy="${1560 - 80 - i * 75}" rx="${(140 * sq).toFixed(1)}" ry="40" fill="none" stroke="#2F6A92" stroke-width="24" stroke-dasharray="26 18"/>`;
    w += kaliya({ x: 760, y: 1500, s: 0.8, t, n: 5, rise: 0.9 });
    let s = cam(540, 1250, lerp(1.25, 1.1, seg(t, at('कालिया ने उन्हें'), at('किनारे पर'))), w);
    s += title('KUNDALI MEIN JAKAD LIYA', 300, 72, seg(t, at('कालिया ने उन्हें') + 0.4, at('कालिया ने उन्हें') + 0.7), '#7CFF9A');
    return s;
  }
  const c = camPath(t, [[at('किनारे पर') - 0.3, 540, 1250, 1.0], [at('नंद बाबा'), 420, 1300, 1.3], [at('सिर्फ़ बलराम') - 0.2, 420, 1300, 1.3], [at('सिर्फ़ बलराम') + 0.4, 760, 1300, 1.4], [at('तभी कृष्ण'), 740, 1280, 1.35]]);
  let w = bank(t, 'storm') + poisonWater(t, 1560);
  const cry = (x) => [0, 1].map((i) => { const ph = (t * 1.4 + i * 0.5 + x) % 1; return `<path d="M${x + (i ? 14 : -14)} ${(1100 + ph * 40).toFixed(0)} q-5 10 0 14 q5 -4 0 -14z" fill="#9FD0FF" opacity="${(1 - ph).toFixed(2)}"/>`; }).join('');
  w += person({ x: 90, y: 1500, s: 0.55, gopi: true, veil: '#7B4BB7', top: '#F5C04A', ...fold }) + nand2({ x: 290, y: 1520, s: 0.68, armL: 30, elbowL: 60, armR: -30, elbowR: -60 });
  w += yashoda({ x: 500, y: 1520, s: 0.75, armL: 40, elbowL: 100, armR: -40, elbowR: -100, t }) + person({ x: 650, y: 1510, s: 0.55, stick: true, top: '#3E8E5A' });
  w += `<g opacity=".8">${cry(260)}${cry(470)}</g>`;
  w += balaram({ x: 860, y: 1520, s: 0.72, eyes: 'closed', armL: 20, armR: -20, glow: seg(t, at('सिर्फ़ बलराम'), at('सिर्फ़ बलराम') + 0.6) * 0.8 });
  let s = cam(...c, w);
  s += title('BRAJ RO RAHA THA', 300, 92, seg(t, at('किनारे पर') + 0.2, at('किनारे पर') + 0.5) * (1 - seg(t, at('नंद बाबा') - 0.1, at('नंद बाबा'))), '#FFF3DC');
  s += title('NAND BABA · YASHODA MAIYA', 300, 66, seg(t, at('नंद बाबा'), at('नंद बाबा') + 0.3) * (1 - seg(t, at('सिर्फ़ बलराम') - 0.2, at('सिर्फ़ बलराम'))), '#FFF3DC');
  s += title('SIRF BALRAM SHAANT', 300, 84, seg(t, at('सिर्फ़ बलराम'), at('सिर्फ़ बलराम') + 0.3), '#FFE29A');
  return s;
}, 'fade');

// 5 HE EXPANDS, THE COILS LOOSEN, HE LEAPS ONTO THE HOODS
add(at('तभी कृष्ण'), at('और फिर'), (t) => {
  const grow = eo(seg(t, at('तभी कृष्ण') + 0.4, at('कुंडली ढीली')));
  const loose = eio(seg(t, at('कुंडली ढीली'), at('और कृष्ण उछलकर')));
  const leap = eio(seg(t, at('और कृष्ण उछलकर'), at('कालिया के फनों') + 0.3));
  let w = bg('night') + stars(t, 30) + `<circle cx="540" cy="1250" r="${(200 + 400 * grow).toFixed(0)}" fill="url(#halo)" opacity="${(0.5 * grow * (1 - leap)).toFixed(2)}"/>`;
  w += kaliya({ x: 540, y: 1620, s: 1.2, t, n: 7, rise: lerp(0.7, 1, leap) });
  const ks = lerp(0.7, 0.9, grow) * lerp(1, 0.62, leap), kx = lerp(320, 540, leap), ky = lerp(1600, 985, leap) - Math.sin(leap * Math.PI) * 260;
  w += krishna({ x: kx, y: ky, s: ks, eyes: 'open', armL: lerp(20, 60, leap), armR: lerp(-20, -60, leap), glow: 0.8 });
  if (leap < 0.3) for (let i = 0; i < 4; i++) { const rx = lerp(140, 380, loose) * lerp(1, 1.25, grow); w += `<ellipse cx="320" cy="${1600 - 80 - i * 75}" rx="${rx.toFixed(0)}" ry="${(40 + 30 * loose).toFixed(0)}" fill="none" stroke="#1F3A5A" stroke-width="44" opacity="${(1 - loose).toFixed(2)}"/>`; }
  w += poisonWater(t, 1560);
  let s = cam(540, lerp(1300, 1050, leap), lerp(1.1, 1.0, leap), `<g transform="${shake(t, at('कुंडली ढीली'), 0.6, 12)}">${w}</g>`);
  s += title('SHAREER PHAILAAYA', 300, 88, seg(t, at('तभी कृष्ण') + 0.5, at('तभी कृष्ण') + 0.8) * (1 - seg(t, at('कुंडली ढीली') - 0.1, at('कुंडली ढीली'))), '#FFE29A');
  s += title('KUNDALI DHEELI', 300, 96, seg(t, at('कुंडली ढीली'), at('कुंडली ढीली') + 0.3) * (1 - seg(t, at('और कृष्ण उछलकर') - 0.1, at('और कृष्ण उछलकर'))), '#FFE29A');
  s += title('PHANON PAR!', 300, 120, seg(t, at('कालिया के फनों'), at('कालिया के फनों') + 0.3), '#FFE29A');
  return s;
}, 'fade');

// 6 THE DANCE — whichever hood rises, his foot lands on it
add(at('और फिर'), at('कालिया थककर'), (t) => {
  const step = Math.floor(t * 2.4), bob = Math.abs(Math.sin(t * Math.PI * 2.4)) * 30;
  let w = bg('night') + stars(t, 50) + rays(540, 820, 20, 0.07, t) + `<circle cx="540" cy="760" r="380" fill="url(#halo)" opacity=".7"/>`;
  w += kaliya({ x: 540, y: 1620, s: 1.2, t: t * 0.6, n: 7, rise: 1 - 0.06 * Math.abs(Math.sin(t * Math.PI * 2.4)) });
  for (let i = 0; i < 3; i++) { const ph = (t * 2.4 + i / 3) % 1; w += `<ellipse cx="540" cy="1600" rx="${(100 + 500 * ph).toFixed(0)}" ry="${(30 + 120 * ph).toFixed(0)}" fill="none" stroke="#FFE7A0" stroke-width="5" opacity="${(0.6 * (1 - ph)).toFixed(2)}"/>`; }
  w += krishna({ x: 540 + Math.sin(t * Math.PI * 1.2) * 16, y: 985 - bob * 0.6, s: 0.62, eyes: 'closed', flute: t > at('जो फन') - 0.5, armR: -80, elbowR: -70, armL: step % 2 ? 150 : 60, elbowL: step % 2 ? 20 : 80, tilt: Math.sin(t * Math.PI * 1.2) * 8, glow: 0.9 });
  w += poisonWater(t, 1560).replace(/#1E4A4A/g, '#1E3A5A').replace(/#163A3C/g, '#162E4C') + dust(t, 50, '#FFE7A0', 80);
  let s = cam(540, lerp(1000, 960, seg(t, at('और फिर'), at('कालिया थककर'))), 1.0, w);
  s += title('NRITYA!', 280, 150, seg(t, at('नृत्य'), at('नृत्य') + 0.25) * (1 - seg(t, at('जो फन') - 0.2, at('जो फन'))), '#FFE29A');
  s += title('KALIYA DAMAN', 280, 120, seg(t, at('जो फन') + 0.6, at('जो फन') + 0.9), '#FFE29A', 'Baloo', 800, 'JO PHAN UTHTA, USI PAR CHARAN');
  return s;
}, 'flash');

// 7 EXHAUSTED — the naga-patnis pray for mercy
add(at('कालिया थककर'), at('कृष्ण ने कालिया'), (t) => {
  const tired = eo(seg(t, at('कालिया थककर'), at('कालिया थककर') + 1.2));
  const wives = eo(seg(t, at('तब नाग') - 0.2, at('तब नाग') + 1.0));
  let w = bg('night') + stars(t, 50);
  w += kaliya({ x: 540, y: 1620, s: 1.2, t: t * 0.3, n: 7, rise: lerp(1, 0.85, tired), bow: tired, angry: false });
  w += krishna({ x: 540, y: 985 + 40 * tired, s: 0.62, eyes: 'closed', flute: true, armR: -80, elbowR: -70, armL: 60, elbowL: 80, glow: 0.9 });
  w += `<g opacity="${wives.toFixed(2)}" transform="translate(0 ${(200 * (1 - wives)).toFixed(0)})">${nagapatni({ x: 200, y: 1700, s: 0.75, t })}${nagapatni({ x: 880, y: 1700, s: 0.75, t, veil: '#8A3E8A', top: '#2E6A8A' })}${nagapatni({ x: 540, y: 1780, s: 0.6, t, veil: '#2E7A5A' })}</g>`;
  w += poisonWater(t, 1600).replace(/#1E4A4A/g, '#1E3A5A').replace(/#163A3C/g, '#162E4C');
  w += bubble(260, 1080, 'क्षमा प्रभु!', seg(t, at('प्रभु') - 0.1, at('प्रभु') + 0.3));
  let s = cam(540, lerp(1000, 1200, wives), lerp(1.0, 1.05, wives), w);
  s += title('THAK KAR CHOOR', 300, 100, seg(t, at('कालिया थककर') + 0.3, at('कालिया थककर') + 0.6) * (1 - seg(t, at('तब नाग') - 0.2, at('तब नाग'))), '#FFF3DC');
  s += title('NAAG-PATNIYAAN', 300, 100, seg(t, at('तब नाग') + 0.3, at('तब नाग') + 0.6), '#9FF0C0');
  return s;
}, 'fade');

// 8 MERCY — leave the Yamuna, go to Ramanaka island in the ocean
add(at('कृष्ण ने कालिया'), at('और एक वरदान'), (t) => {
  const go = eio(seg(t, at('यमुना छोड़कर') - 0.2, at('समुद्र के') + 1.4));
  const sea = eo(seg(t, at('समुद्र के') - 0.2, at('समुद्र के') + 0.6));
  let w = `<g opacity="${(1 - sea).toFixed(2)}">${bank(t, 'day')}${krishna({ x: 260, y: 1460, s: 0.7, eyes: 'closed', armL: 20, armR: -90, elbowR: -20, glow: 0.7 })}</g>`;
  w += `<g opacity="${sea.toFixed(2)}">${bg('day')}${sun(840, 420, 80)}${island(820, 1380, 1.1, t)}</g>`;
  let rv = 'M-300 1440'; for (let x = -300; x <= 1400; x += 40) rv += ` L${x} ${(1440 + Math.sin(x / 80 + t * 2) * 12).toFixed(1)}`; rv += ' V2600 H-300Z';
  w += `<path d="${rv}" fill="${sea > 0.5 ? '#2F7FD8' : '#3E8A9A'}"/><path d="${rv}" transform="translate(0 50)" fill="${sea > 0.5 ? '#2468B8' : '#2E7080'}"/>`;
  w += kaliya({ x: lerp(560, 700, go), y: 1600, s: lerp(0.9, 0.5, go), t, n: 7, rise: 0.8, bow: 0.4, angry: false });
  let s = cam(540, 1150, 1.0, w);
  s += title('KSHAMA', 300, 120, seg(t, at('कृष्ण ने कालिया') + 0.2, at('कृष्ण ने कालिया') + 0.5) * (1 - seg(t, at('यमुना छोड़कर') - 0.2, at('यमुना छोड़कर'))), '#1C2347');
  s += title('YAMUNA CHHODO', 300, 100, seg(t, at('यमुना छोड़कर'), at('यमुना छोड़कर') + 0.3) * (1 - seg(t, at('समुद्र के') - 0.1, at('समुद्र के'))), '#1C2347');
  s += title('RAMANAK DWEEP', 300, 110, seg(t, at('समुद्र के') + 0.5, at('समुद्र के') + 0.8), '#1C2347', 'Baloo', 800, 'SAMUDRA MEIN', '#1C2347');
  return s;
}, 'fade');

// 9 THE BOON — his footprints on the hoods; even Garuda will not touch Kaliya
add(at('और एक वरदान'), at('कल सुबह'), (t) => {
  const pr = eo(seg(t, at('तुम्हारे फनों') + 0.4, at('तुम्हारे फनों') + 1.2));
  const gk = eo(seg(t, at('अब गरुड़') - 0.2, at('अब गरुड़') + 0.8));
  let w = bg('gold') + rays(540, 900, 18, 0.12, t);
  w += kaliya({ x: 540, y: 1700, s: 1.35, t: t * 0.3, n: 7, rise: 1, bow: 0.15, angry: false, prints: pr > 0.05 });
  if (pr > 0 && pr < 1) w += `<circle cx="540" cy="900" r="${(600 * pr).toFixed(0)}" fill="none" stroke="#FFF6DA" stroke-width="${(20 * (1 - pr)).toFixed(1)}"/>`;
  if (gk > 0) w += `<g opacity="${gk.toFixed(2)}">${garuda(lerp(1400, 760, gk), 620 + Math.sin(t * 2) * 20, 1.0, t)}<circle cx="600" cy="840" r="80" fill="#FFF6E2" opacity="${(gk * 0.8).toFixed(2)}"/><circle cx="600" cy="840" r="80" fill="none" stroke="#C1272D" stroke-width="14" opacity="${gk.toFixed(2)}"/><path d="M544 784 L656 896" stroke="#C1272D" stroke-width="14" opacity="${gk.toFixed(2)}"/></g>`;
  let s = cam(540, 1080, lerp(1.0, 1.04, seg(t, at('और एक वरदान'), at('कल सुबह'))), w);
  s += title('VARDAAN', 300, 130, seg(t, at('और एक वरदान'), at('और एक वरदान') + 0.3) * (1 - seg(t, at('तुम्हारे फनों') - 0.1, at('तुम्हारे फनों'))), '#4A1A08');
  s += title('CHARANON KE NISHAAN', 300, 84, seg(t, at('तुम्हारे फनों') + 0.4, at('तुम्हारे फनों') + 0.7) * (1 - seg(t, at('अब गरुड़') - 0.2, at('अब गरुड़'))), '#4A1A08');
  s += title('GARUD BHI NAHI CHHUEGA', 240, 76, seg(t, at('अब गरुड़') + 0.3, at('अब गरुड़') + 0.6), '#4A1A08', 'Baloo', 800, 'BHAGAVAT 10.16.63', '#4A1A08');
  return s;
}, 'zoom');

// 10 TOMORROW MORNING — why 56 bhog?
add(at('कल सुबह'), 999, (t) => {
  let w = bg('maroon') + stars(t, 40) + rays(540, 1200, 18, 0.06, t) + thali(540, 1200, 1.1, 8, t) + dust(t, 30);
  let s = cam(540, 1100, lerp(1.1, 1.0, seg(t, at('कल सुबह'), at('कल सुबह') + 6)), w);
  s += title('KAL SUBAH', 300, 70, seg(t, at('कल सुबह'), at('कल सुबह') + 0.3), '#FFF3DC');
  s += title('56 BHOG KYUN?', 430, 130, seg(t, at('कल सुबह') + 0.8, at('कल सुबह') + 1.1), '#F5C04A');
  return s;
}, 'whip');

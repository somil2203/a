// Vamana & Raja Bali (Bali Pratipada, 10 Nov 2026). Bhagavata Purana 8.15 (Bali, Prahlada's grandson, conquers the three
// worlds), 8.17 (Aditi's vow, Vishnu born as her son), 8.18 (Vamana with chhatra and kamandalu at Bali's yajna at Bhrigukaccha
// on the Narmada; "ask what you wish"), 8.19 (three steps; Shukracharya warns: this is Vishnu), 8.20 (Bali keeps his word; the
// sankalpa water; Trivikrama: one step the earth, the second the heavens), 8.22.2 (third step on Bali's head), 8.22.31-35
// (Sutala; "you will always see me at your gate"). Bali's yearly visit on Bali Pratipada is labelled lok-manyata.
window.HOOK = { l1: '2 क़दम में', l2: 'पूरा ब्रह्मांड!', t1: at('एक छोटा') - 0.05, y: 340, size: 130 };
const rays = (cx, cy, n, op, t, col = '#FFF2C6') => [...Array(n)].map((_, i) => { const a = (i * 360 / n + t * 5) * Math.PI / 180, b = a + 0.12;
  return `<path d="M${cx} ${cy} L${(cx + Math.cos(a) * 2600).toFixed(0)} ${(cy + Math.sin(a) * 2600).toFixed(0)} L${(cx + Math.cos(b) * 2600).toFixed(0)} ${(cy + Math.sin(b) * 2600).toFixed(0)}Z" fill="${col}" opacity="${op}"/>`; }).join('');
const EARTH = { aakash: 1, parvat: 1, dweep: 1, samudra: 1, prithvi: 1, taare: 1 };
const foot3 = (x, y, s, on) => G2(x, y, s, `<g opacity="${clamp(on).toFixed(2)}"><ellipse cx="0" cy="0" rx="34" ry="56" fill="#F5C04A"/>${[-24, -12, 0, 12, 24].map((xx, i) => `<circle cx="${xx}" cy="${-62 - (i === 0 || i === 4 ? 0 : 6)}" r="${i === 0 ? 10 : 8}" fill="#F5C04A"/>`).join('')}</g>`);
const stamp = (t, t0, txt, sub, y = 1250) => { const st = seg(t, t0 - 0.05, t0 + 0.25); if (st <= 0) return ''; const sc = lerp(2.2, 1, eo(st));
  return `<g transform="translate(540 ${y}) rotate(-8) scale(${sc.toFixed(3)})" opacity="${clamp(st * 2).toFixed(2)}"><rect x="-330" y="-90" width="660" height="180" rx="26" fill="#FFF6E2" opacity=".9"/><rect x="-330" y="-90" width="660" height="180" rx="26" fill="none" stroke="#C1272D" stroke-width="12"/>
    <text x="0" y="-12" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="70" fill="#C1272D">${txt}</text><text x="0" y="56" text-anchor="middle" font-family="Baloo" font-weight="700" font-size="36" fill="#C1272D">${sub}</text></g>`; };
function riverBank(t) {
  let w = bg('dawn') + sun(840, 420, 80);
  let rv = 'M-300 1240'; for (let x = -300; x <= 1400; x += 40) rv += ` L${x} ${(1240 + Math.sin(x / 80 + t * 1.6) * 10).toFixed(1)}`; rv += ' V1400 H-300Z';
  w += `<rect x="-300" y="1200" width="1700" height="40" fill="#8CBF6A"/><path d="${rv}" fill="#4F9AD8"/><rect x="-300" y="1380" width="1700" height="900" fill="#D9A26A"/><rect x="-300" y="1380" width="1700" height="18" fill="#B9814A"/>`;
  w += `<text x="900" y="1320" text-anchor="middle" font-family="Baloo" font-weight="700" font-size="34" fill="#FFFFFF" opacity=".75">NARMADA</text>`;
  return w;
}

// 0 COLD OPEN — a giant foot comes down on the earth; then: a small brahmin boy
add(0, at('आज बलि'), (t) => {
  const slam = eo(seg(t, 0, 0.45));
  const small = t > at('एक छोटा') - 0.1 && t < at('और उसने') + 0.2;
  let s = '';
  if (!small) {
    const grow = eio(seg(t, at('और उसने'), at('पूरा ब्रह्मांड') + 1.2));
    s += `<rect width="1080" height="1920" fill="#0B0620"/>` + stars(t, 80);
    s += cam(540, 980, t < at('एक छोटा') ? lerp(1.25, 1.0, slam) : lerp(1.3, 0.9, grow), cosmos(540, 1250, 420, t, EARTH) + giantLeg(560, lerp(380, 860, slam), 1.0, 1, t));
    s = `<g transform="${shake(t, 0.42, 0.6, 22)}">${s}</g>` + flashRect(t, 0.42, 0.3, '#FFF2C8');
    if (t > at('और उसने')) s += title('DO KADAM = BRAHMAAND', 300, 78, seg(t, at('पूरा ब्रह्मांड'), at('पूरा ब्रह्मांड') + 0.3), '#FFE29A');
  } else {
    let w = bg('dawn') + rays(540, 900, 16, 0.12, t) + `<path d="M-400 1500 Q540 1350 1500 1500 V2400 H-400Z" fill="#5BA463"/><path d="M-400 1560 Q540 1420 1500 1560 V2400 H-400Z" fill="#4A8C52"/>`;
    w += vamana({ x: 540, y: 1520, s: 0.95, t, eyes: 'open' });
    s += cam(540, lerp(1150, 1220, seg(t, at('एक छोटा'), at('और उसने'))), lerp(1.05, 1.2, seg(t, at('एक छोटा'), at('और उसने'))), w);
    s += title('EK CHHOTA SA BAALAK...', 300, 80, seg(t, at('एक छोटा') + 0.1, at('एक छोटा') + 0.4), '#7A2E12');
  }
  return s;
});

// 1 TODAY IS BALI PRATIPADA
add(at('आज बलि'), at('भागवत पुराण'), (t) => {
  let w = bg('maroon') + stars(t, 40) + rays(540, 1100, 18, 0.07, t) + `<circle cx="540" cy="1100" r="460" fill="url(#halo)" opacity=".6"/>`;
  for (let i = 0; i < 7; i++) w += diya(150 + i * 130, 1560, 0.6, t, i);
  w += bali({ x: 540, y: 1480, s: 1.0, eyes: 'open', glow: 0.4 });
  let s = cam(540, lerp(1100, 1000, seg(t, at('आज बलि'), at('भागवत पुराण'))), lerp(1.0, 1.15, seg(t, at('आज बलि'), at('भागवत पुराण'))), w);
  s += title('AAJ BALI PRATIPADA', 300, 92, seg(t, at('आज बलि'), at('आज बलि') + 0.3) * (1 - seg(t, at('और ये कहानी') - 0.1, at('और ये कहानी'))), '#F5C04A', 'Baloo', 800, '10 NOVEMBER');
  s += title('RAJA BALI', 300, 130, seg(t, at('और ये कहानी') + 0.8, at('और ये कहानी') + 1.1), '#F5C04A');
  return s;
}, 'zoom');

// 2 PRAHLADA'S GRANDSON CONQUERS THE THREE WORLDS; THE DEVAS LOSE HEAVEN
add(at('भागवत पुराण'), at('तब माता'), (t) => {
  const lokas = eo(seg(t, at('तीनों लोक') - 0.1, at('तीनों लोक') + 0.8));
  const exile = eo(seg(t, at('देवता') - 0.1, at('देवता') + 1.4));
  let w = bg('dusk') + stars(t, 30);
  if (t < at('देवता') - 0.2) {
    w += bali({ x: 540, y: 1600, s: 0.95, armR: -150, elbowR: -10, eyes: 'open' });
    ['BHU', 'BHUVAH', 'SWAH'].forEach((n, i) => { const k = clamp(lokas * 3 - i); const x = 220 + i * 320, y = 760 - (i === 1 ? 70 : 0);
      w += `<g opacity="${k.toFixed(2)}" transform="translate(${x} ${y}) scale(${lerp(0.6, 1, back(k)).toFixed(3)})"><circle r="100" fill="${['#2F7FD8', '#7FB2E6', '#F5C04A'][i]}"/><circle r="100" fill="none" stroke="#FFF3DC" stroke-width="8"/>
        <path d="M-10 -96 L-10 -170 L50 -150 L-10 -130" fill="#8E1F2A" stroke="#5A2A7A" stroke-width="4"/><text y="16" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="40" fill="#1C2347">${n}</text></g>`; });
  } else {
    w += swarga(540, 860, 1.1, t);
    w += `<g transform="translate(${lerp(0, -420, exile).toFixed(0)} 0)">${indra({ x: 600, y: 1640, s: 0.62, eyes: 'closed', armL: 20, armR: -20 })}</g>`;
    w += `<path d="M380 760 L700 760" stroke="#8E1F2A" stroke-width="10"/>`;
  }
  let s = cam(540, 1100, lerp(1.08, 1.0, seg(t, at('भागवत पुराण'), at('तब माता'))), w);
  s += title('BHAGAVAT 8.15', 300, 70, seg(t, at('भागवत पुराण'), at('भागवत पुराण') + 0.3) * (1 - seg(t, at('प्रह्लाद') - 0.1, at('प्रह्लाद'))), '#FFF3DC');
  s += title('PRAHLAD KE POTE', 300, 92, seg(t, at('प्रह्लाद'), at('प्रह्लाद') + 0.3) * (1 - seg(t, at('तीनों लोक') - 0.1, at('तीनों लोक'))), '#FFE29A');
  s += title('TEENON LOK JEETE', 300, 92, seg(t, at('तीनों लोक'), at('तीनों लोक') + 0.3) * (1 - seg(t, at('देवता') - 0.2, at('देवता'))), '#FFE29A');
  s += title('DEVTA BEGHAR', 300, 110, seg(t, at('देवता'), at('देवता') + 0.3), '#FFE29A');
  return s;
}, 'whip');

// 3 ADITI'S SON — VAMANA, WITH CHHATRA AND KAMANDALU
add(at('तब माता'), at('बलि उस समय'), (t) => {
  const born = eo(seg(t, at('भगवान विष्णु') - 0.2, at('वामन रूप') + 0.2));
  let w = bg('day') + rays(540, 900, 18, 0.12 * born, t) + `<circle cx="540" cy="1000" r="${(200 + 300 * born).toFixed(0)}" fill="url(#halo)" opacity="${(0.4 + 0.5 * born).toFixed(2)}"/>`;
  w += `<path d="M-300 1500 Q540 1460 1400 1500 V2400 H-300Z" fill="#8CBF6A"/>`;
  w += gopi2({ x: 300, y: 1680, s: 0.95, veil: '#C2405A', top: '#F5C04A', skirt: '#7A2E8C', armL: 38, elbowL: -112, armR: -38, elbowR: 112, t }) + `<path d="M232 ${1680 - 0.95 * 520} l68 -30 l68 30 l-14 -40 l-24 16 l-30 -36 l-30 36 l-24 -16z" fill="url(#goldG)"/>`;
  w += `<g opacity="${born.toFixed(2)}">${vamana({ x: 720, y: 1660, s: lerp(0.4, 0.82, born), t, eyes: 'closed' })}</g>`;
  if (t > at('छोटा सा क़द') - 0.1) { const k = seg(t, at('छोटा सा क़द'), at('छोटा सा क़द') + 0.5); w += `<g opacity="${k.toFixed(2)}"><path d="M880 1660 V${(1660 - 0.82 * 600).toFixed(0)}" stroke="#7A2E12" stroke-width="6"/><path d="M860 1660 h40 M860 ${(1660 - 0.82 * 600).toFixed(0)} h40" stroke="#7A2E12" stroke-width="6"/></g>`; }
  const c = camPath(t, [[at('तब माता'), 380, 1250, 1.25], [at('भगवान विष्णु'), 540, 1200, 1.0], [at('वामन रूप') + 0.3, 700, 1250, 1.3], [at('हाथ में छत्र'), 680, 1060, 1.45], [at('बलि उस समय'), 680, 1100, 1.4]]);
  let s = cam(...c, w);
  s += title('MATA ADITI', 300, 100, seg(t, at('तब माता'), at('तब माता') + 0.3) * (1 - seg(t, at('भगवान विष्णु') - 0.1, at('भगवान विष्णु'))), '#7A2E12');
  s += title('VAAMAN AVATAAR', 300, 100, seg(t, at('वामन रूप'), at('वामन रूप') + 0.3) * (1 - seg(t, at('हाथ में छत्र') - 0.1, at('हाथ में छत्र'))), '#7A2E12');
  s += title('CHHATRA + KAMANDAL', 300, 84, seg(t, at('हाथ में छत्र'), at('हाथ में छत्र') + 0.3), '#7A2E12');
  return s;
}, 'fade');

// 4 BALI'S YAJNA ON THE NARMADA — "ask what you wish" — "three steps of land"
add(at('बलि उस समय'), at('बलि हँसे'), (t) => {
  const c = camPath(t, [[at('बलि उस समय'), 540, 1150, 1.0], [at('उन्होंने वामन'), 640, 1250, 1.2], [at('वामन बोले'), 380, 1300, 1.3], [at('तीन क़दम'), 420, 1200, 1.15], [at('बलि हँसे'), 420, 1200, 1.15]]);
  let w = riverBank(t) + kund(540, 1560, 0.6, t, 0.9);
  w += bali({ x: 760, y: 1720, s: 0.85, eyes: 'open', armR: -60, elbowR: -50, armL: 20 }) + vamana({ x: 300, y: 1720, s: 0.62, t, eyes: 'open' });
  w += bubble(760, 980, 'माँग लो!', seg(t, at('जो चाहो') - 0.2, at('जो चाहो') + 0.2) * (1 - seg(t, at('वामन बोले') - 0.2, at('वामन बोले'))));
  const steps = seg(t, at('तीन क़दम') - 0.1, at('तीन क़दम') + 1.0);
  for (let i = 0; i < 3; i++) w += foot3(170 + i * 130, 900, 1.3, clamp(steps * 3 - i));
  let s = cam(...c, w);
  s += title('NARMADA KINAARE YAGYA', 300, 76, seg(t, at('बलि उस समय'), at('बलि उस समय') + 0.3) * (1 - seg(t, at('उन्होंने वामन') - 0.1, at('उन्होंने वामन'))), '#7A2E12');
  s += title('BAS TEEN KADAM', 300, 110, seg(t, at('तीन क़दम'), at('तीन क़दम') + 0.3), '#7A2E12');
  return s;
}, 'whip');

// 5 BALI LAUGHS — "that's all?"
add(at('बलि हँसे'), at('तभी गुरु'), (t) => {
  let w = riverBank(t) + bali({ x: 540, y: 1700, s: 1.05, eyes: 'closed', laugh: Math.sin(t * 14) > 0, armL: 30, elbowL: 40, armR: -30, elbowR: -40 });
  let s = cam(540, 1150, lerp(1.25, 1.35, seg(t, at('बलि हँसे'), at('तभी गुरु'))), `<g transform="${shake(t, at('बलि हँसे'), 0.4, 6)}">${w}</g>`);
  s += title('BAS ITNA?', 300, 150, seg(t, at('बस इतना') - 0.1, at('बस इतना') + 0.2), '#7A2E12');
  return s;
}, 'zoom');

// 6 SHUKRACHARYA'S WARNING — "this is Vishnu himself"
add(at('तभी गुरु'), at('पर बलि'), (t) => {
  const v = eo(seg(t, at('स्वयं विष्णु') - 0.2, at('स्वयं विष्णु') + 0.6));
  let w = bg('rage') + `<rect x="-300" y="1380" width="1700" height="900" fill="#3A0A12"/>`;
  w += `<g opacity="${v.toFixed(2)}">${rays(780, 1000, 18, 0.12, t)}<circle cx="780" cy="1100" r="420" fill="url(#halo)"/>${vishnu4({ x: 780, y: 1640, s: 0.95, t })}</g>`;
  w += `<g opacity="${(1 - v * 0.85).toFixed(2)}">${vamana({ x: 780, y: 1640, s: 0.62, t, eyes: 'closed' })}</g>`;
  w += shukra({ x: 300, y: 1700, s: 0.95, armR: -150 + Math.sin(t * 8) * 8, elbowR: -10, eyes: 'open' });
  let s = cam(540, 1180, lerp(1.0, 1.08, seg(t, at('तभी गुरु'), at('पर बलि'))), w);
  s += title('GURU SHUKRACHARYA', 300, 84, seg(t, at('तभी गुरु'), at('तभी गुरु') + 0.3) * (1 - seg(t, at('स्वयं विष्णु') - 0.2, at('स्वयं विष्णु'))), '#FFD1A6');
  s += title('YE SWAYAM VISHNU HAIN!', 300, 84, seg(t, at('स्वयं विष्णु'), at('स्वयं विष्णु') + 0.3) * (1 - seg(t, at('ये सब छीन') - 0.1, at('ये सब छीन'))), '#FFE29A');
  s += title('SAB CHHEEN LENGE!', 300, 100, seg(t, at('ये सब छीन'), at('ये सब छीन') + 0.3), '#FFD1A6');
  s += flashRect(t, at('स्वयं विष्णु'), 0.3, '#FFF2C8');
  return s;
}, 'flash');

// 7 BALI KEEPS HIS WORD
add(at('पर बलि'), at('और जैसे ही'), (t) => {
  let w = bg('gold') + rays(540, 1000, 18, 0.14, t) + `<circle cx="540" cy="1100" r="440" fill="url(#halo)"/>`;
  w += bali({ x: 540, y: 1700, s: 1.1, eyes: 'closed', armR: -20, armL: 60, elbowL: 100, glow: 0.6 });
  let s = cam(540, 1180, lerp(1.2, 1.05, seg(t, at('पर बलि'), at('और जैसे ही'))), w);
  s += title('VACHAN NAHI TODUNGA', 300, 84, seg(t, at('जो वचन'), at('जो वचन') + 0.3), '#4A1A08');
  return s;
}, 'fade');

// 8 THE SANKALPA WATER — VAMANA GROWS — STEP ONE: EARTH, STEP TWO: HEAVEN
add(at('और जैसे ही'), at('और तीसरा'), (t) => {
  const pour = seg(t, at('और जैसे ही') + 0.6, at('वामन बढ़ने'));
  const grow = eio(seg(t, at('वामन बढ़ने') - 0.1, at('आकाश तक') + 0.8));
  let s = '';
  if (t < at('पहले क़दम') - 0.2) {
    let w = `<g opacity="${(1 - grow).toFixed(2)}">${riverBank(t)}</g><g opacity="${grow.toFixed(2)}"><rect x="-30000" y="-60000" width="60000" height="120000" fill="#0B0620"/>${stars(t, 80)}</g>`;
    w += bali({ x: 820, y: 1720, s: 0.85, jal: true, armR: -70, elbowR: -50, eyes: 'open' });
    if (pour > 0 && pour < 1) w += `<path d="M700 ${1720 - 0.85 * 470} Q620 1300 ${lerp(640, 470, pour).toFixed(0)} ${lerp(1320, 1420, pour).toFixed(0)}" stroke="#9FD8FF" stroke-width="14" fill="none" stroke-linecap="round"/>`;
    w += vamana({ x: 420, y: 1720, s: lerp(0.62, 9, grow), t, eyes: 'closed' });
    s += cam(540, lerp(1150, 900 - grow * 3500, grow), lerp(1.0, 0.16, grow), w);
    s = `<g transform="${shake(t, at('वामन बढ़ने'), 2.5, 10)}">${s}</g>`;
    s += title('SANKALP KA JAL', 300, 92, seg(t, at('और जैसे ही') + 0.5, at('और जैसे ही') + 0.8) * (1 - seg(t, at('वामन बढ़ने') - 0.1, at('वामन बढ़ने'))), '#7A2E12');
    s += title('BADHTE GAYE...', 300, 100, seg(t, at('बढ़ते गए'), at('बढ़ते गए') + 0.3), '#FFE29A');
  } else {
    const two = t > at('दूसरे क़दम') - 0.2;
    const st = eo(seg(t, (two ? at('दूसरे क़दम') : at('पहले क़दम')) - 0.1, (two ? at('दूसरे क़दम') : at('पहले क़दम')) + 0.5));
    s += `<rect width="1080" height="1920" fill="#0B0620"/>` + stars(t, 90);
    if (!two) s += cam(540, 1000, 1.0, cosmos(540, 1280, 400, t, EARTH) + giantLeg(560, lerp(300, 900, st), 0.95, 1, t));
    else s += cam(540, 1000, 1.0, `<g transform="translate(0 ${(-30 * st).toFixed(0)})">${swarga(540, 1280, 1.2, t)}</g>` + giantLeg(560, lerp(300, 1000, st), 0.95, 1, t));
    s = `<g transform="${shake(t, (two ? at('दूसरे क़दम') : at('पहले क़दम')) + 0.35, 0.5, 18)}">${s}</g>`;
    s += title(two ? 'DOOSRA KADAM: SWARG' : 'PEHLA KADAM: PRITHVI', 300, 84, st, '#FFE29A');
  }
  return s;
}, 'fade');

// 9 AND THE THIRD? — NO PLACE LEFT
add(at('और तीसरा'), at('तब बलि ने सिर'), (t) => {
  let s = `<rect width="1080" height="1920" fill="#0B0620"/>` + stars(t, 90);
  s += cam(540, 1000, lerp(1.0, 1.08, seg(t, at('और तीसरा'), at('तब बलि ने सिर'))), `<g opacity=".55">${cosmos(300, 1250, 200, t, EARTH)}${swarga(780, 1300, 0.6, t)}</g>`);
  const q = seg(t, at('और तीसरा'), at('और तीसरा') + 0.3);
  s += `<g opacity="${q.toFixed(2)}" transform="translate(540 820) scale(${lerp(0.7, 1, back(q)).toFixed(3)})"><text text-anchor="middle" font-family="Baloo" font-weight="800" font-size="380" fill="#FFE29A" stroke="#14060A" stroke-width="20" paint-order="stroke">3?</text></g>`;
  s += title('JAGAH HI NAHI BACHI', 300, 90, seg(t, at('रखने की'), at('रखने की') + 0.3), '#FFF3DC');
  return s;
}, 'zoom');

// 10 BALI BOWS HIS HEAD — THE THIRD STEP
add(at('तब बलि ने सिर'), at('भगवान प्रसन्न'), (t) => {
  const bow = eo(seg(t, at('तब बलि ने सिर'), at('तब बलि ने सिर') + 1.0));
  const step = eo(seg(t, at('प्रभु') + 1.0, at('प्रभु') + 2.0));
  let w = bg('gold') + rays(540, 900, 18, 0.12, t);
  w += `<path d="M-300 1560 Q540 1520 1400 1560 V2400 H-300Z" fill="#B9813E"/>`;
  w += bali({ x: 540, y: 1720, s: 1.0, folded: true, bow: 22 * bow, eyes: 'closed' });
  w += giantLeg(560, lerp(200, 1040, step), 0.55, step > 0 ? 1 : 0, t);
  if (step > 0.9) w += `<circle cx="540" cy="1060" r="${(120 + 200 * (step - 0.9) * 10).toFixed(0)}" fill="url(#halo)" opacity=".8"/>`;
  let s = cam(540, 1180, lerp(1.05, 1.0, step), w);
  s += title('SIR JHUKAAYA', 300, 100, seg(t, at('तब बलि ने सिर') + 0.4, at('तब बलि ने सिर') + 0.7) * (1 - seg(t, at('प्रभु') - 0.1, at('प्रभु'))), '#4A1A08');
  s += title('TEESRA KADAM: MERE SIR PAR', 300, 70, seg(t, at('प्रभु') + 0.4, at('प्रभु') + 0.7), '#4A1A08');
  return s;
}, 'fade');

// 11 SUTALA — AND THE LORD AT HIS GATE
add(at('भगवान प्रसन्न'), at('लोक-मान्यता'), (t) => {
  const gate = eo(seg(t, at('मैं हमेशा') - 0.2, at('मैं हमेशा') + 0.8));
  let w = bg('maroon') + rays(540, 900, 18, 0.06, t);
  w += `<rect x="140" y="760" width="800" height="760" fill="#C98A1E"/><path d="M100 760 L540 520 L980 760Z" fill="url(#goldG)"/><rect x="420" y="1100" width="240" height="420" rx="120" fill="#5A2A0A"/>
        ${[200, 330, 750, 880].map((x) => `<rect x="${x - 18}" y="800" width="36" height="720" fill="#E8B04A"/>`).join('')}`;
  w += bali({ x: 540, y: 1650, s: 0.7, eyes: 'closed', glow: 0.5 });
  w += `<g opacity="${gate.toFixed(2)}">${vishnu4({ x: 880, y: 1720, s: 0.75, t })}${gada(960, 1120, 1.0)}</g>`;
  let s = cam(lerp(540, 680, gate), 1200, lerp(1.0, 1.15, gate), w);
  s += title('BHAGWAN PRASANN', 300, 92, seg(t, at('भगवान प्रसन्न'), at('भगवान प्रसन्न') + 0.3) * (1 - seg(t, at('सुतल') - 0.1, at('सुतल'))), '#F5C04A');
  s += title('SUTAL LOK KA RAAJ', 300, 92, seg(t, at('सुतल'), at('सुतल') + 0.3) * (1 - seg(t, at('मैं हमेशा') - 0.2, at('मैं हमेशा'))), '#F5C04A');
  s += title('DWAAR PAR BHAGWAN', 300, 92, seg(t, at('मैं हमेशा'), at('मैं हमेशा') + 0.3), '#F5C04A', 'Baloo', 800, 'BHAGAVAT 8.22.35');
  return s;
}, 'fade');

// 12 LOK-MANYATA — BALI VISITS HIS PEOPLE TODAY
add(at('लोक-मान्यता'), at('आज रात'), (t) => {
  let w = bg('night') + stars(t, 60) + `<path d="M-300 1500 Q540 1460 1400 1500 V2400 H-300Z" fill="#3A2A3A"/>`;
  w += bali({ x: 540, y: 1640, s: 0.8, eyes: 'closed', armL: 40, elbowL: 60, armR: -40, elbowR: -60, glow: 0.6 });
  [[150, '#C2405A'], [300, '#3E8E5A'], [780, '#7B4BB7'], [930, '#D8432F']].forEach(([x, c], i) => { w += (i % 2 ? gwala2({ x, y: 1660, s: 0.55, top: c }) : gopi2({ x, y: 1660, s: 0.58, veil: c, top: '#F5C04A', thali: true, armR: -60, elbowR: -50, t })); });
  for (let i = 0; i < 9; i++) w += diya(80 + i * 115, 1700, 0.45, t, i);
  let s = cam(540, 1200, lerp(1.1, 1.0, seg(t, at('लोक-मान्यता'), at('आज रात'))), w);
  s += stamp(t, at('लोक-मान्यता') + 0.1, 'LOK-MAANYATA', 'SHAASTRA NAHI', 600);
  s += title('BALI PRAJA SE MILNE AATE HAIN', 300, 60, seg(t, at('आज के दिन'), at('आज के दिन') + 0.3), '#FFE29A');
  return s;
}, 'fade');

// 13 TONIGHT — Brahma tests Krishna
add(at('आज रात'), 999, (t) => {
  let w = bg('night') + stars(t, 60) + rays(540, 1100, 18, 0.06, t) + brahma({ x: 540, y: 1520, s: 1.0, t, glow: 0.6 });
  let s = cam(540, 1150, lerp(1.1, 1.0, seg(t, at('आज रात'), at('आज रात') + 6)), w);
  s += title('AAJ RAAT', 300, 70, seg(t, at('आज रात'), at('आज रात') + 0.3), '#FFF3DC');
  s += title('BRAHMA KI PAREEKSHA', 420, 100, seg(t, at('आज रात') + 0.8, at('आज रात') + 1.1), '#F5C04A');
  return s;
}, 'whip');

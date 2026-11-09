// Maa Yashoda & the universe in Kanha's mouth. Bhagavata Purana 10.8.32-45 (Balarama and the cowherd boys report that
// Krishna ate earth; "naham bhakshitavan amba" 10.8.35; Yashoda sees the universe and Vraja and herself 10.8.37-39;
// Krishna spreads his Vaishnavi maya, she forgets and takes him on her lap 10.8.43).
const rays = (cx, cy, n, op, t, col = '#FFF2C6') => [...Array(n)].map((_, i) => { const a = (i * 360 / n + t * 5) * Math.PI / 180, b = a + 0.12;
  return `<path d="M${cx} ${cy} L${(cx + Math.cos(a) * 2400).toFixed(0)} ${(cy + Math.sin(a) * 2400).toFixed(0)} L${(cx + Math.cos(b) * 2400).toFixed(0)} ${(cy + Math.sin(b) * 2400).toFixed(0)}Z" fill="${col}" opacity="${op}"/>`; }).join('');
const word = (txt, k, y = 1420, col = '#FFE29A', size = 120) => k <= 0 ? '' : `<g opacity="${clamp(k * 2).toFixed(2)}" transform="translate(540 ${y}) scale(${lerp(0.8, 1, back(k)).toFixed(3)})"><text text-anchor="middle" font-family="Baloo" font-weight="800" font-size="${size}" fill="${col}" stroke="#1A0A20" stroke-width="${size * 0.07}" paint-order="stroke">${txt}</text></g>`;
const ALL = { aakash: 1, disha: 1, parvat: 1, dweep: 1, samudra: 1, prithvi: 1, agni: 1, vayu: 1, chandra: 1, taare: 1 };
const fold = { armL: 38, elbowL: -112, armR: -38, elbowR: 112 };

function courtyard(t) {
  let w = bg('day') + sun(880, 380, 80) + cloud(220, 420, 0.6, '#FFFFFF', '#E9E4F4');
  w += hut(150, 1280, 0.7) + hut(930, 1300, 0.6, '#C98A5A') + tree(560, 1260, 0.55);
  w += `<rect x="-300" y="1270" width="1700" height="900" fill="#D9A26A"/><rect x="-300" y="1270" width="1700" height="20" fill="#B9814A"/>`;
  return w;
}

// 0 HOOK — "open your mouth" ... the whole universe
add(0, at('गोकुल की बात'), (t) => {
  const open = seg(t, at('मुँह खोलो') + 0.2, at('मुँह खोलो') + 0.6);
  const into = eio(seg(t, at('और उस छोटे') + 0.3, at('पूरा ब्रह्मांड')));
  const c = camPath(t, [[0, 520, 1200, 1.3], [at('मुँह खोलो') + 0.4, 640, 1180, 1.7], [at('पूरा ब्रह्मांड'), 700, 1228, 9]]);
  let w = courtyard(t);
  w += yashoda({ x: 340, y: 1700, s: 1.0, armR: -60, elbowR: -50, eyes: 'open', t });
  w += krishna({ x: 700, y: 1640, s: 0.9, armL: 20, armR: -20, eyes: 'open', mouth: open > 0.3 ? 'open' : 'smile' });
  if (open > 0) w += `<circle cx="700" cy="${1640 - 0.9 * 451}" r="${(26 * open).toFixed(1)}" fill="url(#halo)"/>`;
  let s = cam(...c, w);
  if (into > 0.6) s += `<g opacity="${clamp((into - 0.6) / 0.4).toFixed(2)}">${cosmos(540, 960, 1200, t, ALL)}</g>`;
  if (t > at('पूरा ब्रह्मांड') - 0.2) s = `${cosmos(540, 960, lerp(600, 520, seg(t, at('पूरा ब्रह्मांड'), at('गोकुल की बात'))), t, ALL)}`.replace('<circle cx="540" cy="960" r="', '<rect width="1080" height="1920" fill="#0B0620"/><circle cx="540" cy="960" r="');
  s += title('MUNH KHOLO', 300, 100, seg(t, at('मुँह खोलो'), at('मुँह खोलो') + 0.3) * (1 - seg(t, at('और उस छोटे') + 0.3, at('और उस छोटे') + 0.6)), '#7A2E12');
  s += title('POORA BRAHMAAND', 300, 100, seg(t, at('पूरा ब्रह्मांड'), at('पूरा ब्रह्मांड') + 0.3), '#FFE29A');
  return s;
});

// 1 GOKUL — Balarama and the boys run to Yashoda
add(at('गोकुल की बात'), at('यशोदा ने कान्हा'), (t) => {
  const c = camPath(t, [[at('गोकुल की बात'), 540, 1000, 1.0], [at('बलराम') + 0.4, 420, 1300, 1.2], [at('यशोदा मैया') + 0.4, 600, 1250, 1.12], [at('मैया, कान्हा') + 0.5, 520, 1250, 1.1], [at('यशोदा ने कान्हा'), 520, 1250, 1.12]]);
  let w = courtyard(t) + cow({ x: 900, y: 1330, s: 0.45, t });
  const run = eo(seg(t, at('बलराम') - 0.3, at('यशोदा मैया') + 0.6));
  const bob = (i) => -Math.abs(Math.sin(t * 10 + i)) * 12 * (1 - run);
  w += yashoda({ x: 820, y: 1700, s: 0.98, armL: 30, armR: -40, eyes: 'open', t });
  const pointing = t > at('मैया, कान्हा');
  w += balaram({ x: lerp(-150, 520, run), y: 1700 + bob(0), s: 0.82, armR: pointing ? -95 : -30, elbowR: pointing ? -10 : -40, armL: 30, eyes: 'open', mouth: pointing && Math.sin(t * 16) > 0 ? 'open' : 'smile' });
  w += gwala2({ x: lerp(-320, 330, run), y: 1710 + bob(1), s: 0.62, top: '#3E8E5A', armR: -40, eyes: 'open' }) + gwala2({ x: lerp(-480, 170, run), y: 1720 + bob(2), s: 0.58, top: '#D8432F', armL: 40 });
  // Kanha in the corner with mud
  w += krishna({ x: 200, y: 1460, s: 0.5, armR: -150, elbowR: -40, eyes: 'closed', mouth: 'open' }) + mudLump(200 + 40, 1460 - 0.5 * 470, 0.6);
  w += `<circle cx="196" cy="${1460 - 0.5 * 455}" r="8" fill="#7A4A2A"/>`;
  w += bubble(560, 1060, 'मिट्टी खाई!', seg(t, at('मैया, कान्हा') + 0.3, at('मैया, कान्हा') + 0.7));
  let s = cam(...c, w);
  s += title('GOKUL', 300, 110, seg(t, at('गोकुल की बात'), at('गोकुल की बात') + 0.3) * (1 - seg(t, at('बलराम') - 0.2, at('बलराम'))), '#1C2347');
  s += title('BALRAM + GWAAL-BAAL', 300, 76, seg(t, at('बलराम'), at('बलराम') + 0.3) * (1 - seg(t, at('यशोदा मैया') - 0.2, at('यशोदा मैया'))), '#1C2347');
  s += title('YASHODA MAIYA', 300, 92, seg(t, at('यशोदा मैया'), at('यशोदा मैया') + 0.3) * (1 - seg(t, at('मैया, कान्हा') - 0.2, at('मैया, कान्हा'))), '#1C2347');
  return s;
}, 'zoom');

// 2 SCOLDING — "why did you eat mud?" / 3 "I didn't, they lie — look in my mouth"
add(at('यशोदा ने कान्हा'), at('और कान्हा ने मुँह'), (t) => {
  const c = camPath(t, [[at('यशोदा ने कान्हा'), 540, 1250, 1.2], [at('और डाँटा'), 500, 1200, 1.3], [at('कान्हा बोले'), 640, 1260, 1.5], [at('ये सब झूठ') + 0.3, 600, 1200, 1.2], [at('विश्वास न'), 640, 1260, 1.6], [at('और कान्हा ने मुँह'), 650, 1230, 1.9]]);
  let w = courtyard(t);
  const scold = t > at('और डाँटा') - 0.1 && t < at('कान्हा बोले');
  w += yashoda({ x: 380, y: 1700, s: 1.0, armR: scold ? -150 + Math.sin(t * 9) * 10 : -70, elbowR: scold ? -10 : -40, armL: 20, eyes: 'open', t });
  const talk = t > at('कान्हा बोले') && Math.sin(t * 17) > 0;
  const shakeHead = t > at('मैंने नहीं') && t < at('ये सब झूठ') ? Math.sin(t * 12) * 8 : 0;
  const pointBoys = t > at('ये सब झूठ') && t < at('विश्वास न');
  w += krishna({ x: 660, y: 1660, s: 0.86, eyes: 'open', mouth: talk ? 'open' : 'smile', tilt: shakeHead, armR: pointBoys ? -100 : -30, elbowR: pointBoys ? -10 : -30, armL: 24 });
  if (pointBoys) w += gwala2({ x: 980, y: 1700, s: 0.6, top: '#3E8E5A', eyes: 'open' }) + balaram({ x: 1120, y: 1700, s: 0.7, eyes: 'open' });
  w += bubble(380, 860, 'क्यों खाई?', seg(t, at('क्यों खाई') - 0.2, at('क्यों खाई') + 0.2) * (1 - seg(t, at('कान्हा बोले') - 0.2, at('कान्हा बोले'))));
  w += bubble(660, 1000, 'नहीं खाई!', seg(t, at('मैंने नहीं') - 0.1, at('मैंने नहीं') + 0.3) * (1 - seg(t, at('ये सब झूठ') - 0.1, at('ये सब झूठ') + 0.1)));
  w += bubble(660, 1000, 'मुँह देख लो', seg(t, at('मेरा मुँह') - 0.1, at('मेरा मुँह') + 0.3));
  let s = cam(...c, w);
  s += title('KYUN KHAAYI MITTI?', 300, 88, seg(t, at('और डाँटा'), at('और डाँटा') + 0.3) * (1 - seg(t, at('कान्हा बोले') - 0.2, at('कान्हा बोले'))), '#7A2E12');
  s += title('SAB JHOOTH BOL RAHE HAIN', 300, 72, seg(t, at('ये सब झूठ'), at('ये सब झूठ') + 0.3) * (1 - seg(t, at('विश्वास न') - 0.1, at('विश्वास न'))), '#7A2E12');
  return s;
}, 'fade');

// 4 THE MOUTH OPENS
add(at('और कान्हा ने मुँह'), at('भागवत पुराण'), (t) => {
  const t0 = at('और कान्हा ने मुँह'), t1 = at('भागवत पुराण');
  const open = seg(t, t0 + 0.6, t0 + 1.2);
  const c = camPath(t, [[t0, 540, 980, 2.2], [t0 + 1.3, 540, 980, 2.4], [t1, 540, 1060, 9]]);
  let w = bg('saffron') + rays(540, 1000, 18, 0.12 + 0.1 * open, t);
  w += krishna({ x: 540, y: 1430, s: 1.0, eyes: 'closed', mouth: open > 0.2 ? 'open' : 'smile', armL: 20, armR: -20, glow: 0.4 });
  if (open > 0) w += `<ellipse cx="540" cy="${(1430 - 455).toFixed(0)}" rx="${(13 * open).toFixed(1)}" ry="${(9 * open).toFixed(1)}" fill="#0B0620"/><circle cx="540" cy="975" r="${(60 * open).toFixed(0)}" fill="url(#halo)" opacity=".8"/>`;
  let s = cam(...c, w);
  const iris = seg(t, t1 - 0.9, t1);
  if (iris > 0) s += `<rect width="1080" height="1920" fill="#2A1450" opacity="${(iris * 0.75).toFixed(2)}"/><circle cx="540" cy="960" r="${(900 * iris).toFixed(0)}" fill="url(#halo)" opacity="${(iris * 0.8).toFixed(2)}"/>`;
  return s;
}, 'zoom');

// 5 THE UNIVERSE — every element on its word
const ORDER = [['aakash', 'आकाश', 'आकाश'], ['disha', 'दिशाएँ', 'दिशाएँ'], ['parvat', 'पर्वत', 'पर्वत'], ['dweep', 'द्वीप', 'द्वीप'], ['samudra', 'समुद्र', 'समुद्र'], ['prithvi', 'पृथ्वी', 'पूरी पृथ्वी'], ['agni', 'अग्नि', 'अग्नि'], ['vayu', 'वायु', 'वायु'], ['chandra', 'चंद्रमा', 'चंद्रमा'], ['taare', 'तारे', 'तारे']];
add(at('भागवत पुराण'), at('और उसी में'), (t) => {
  const k = {}; ORDER.forEach(([id, , key]) => { k[id] = eo(seg(t, at(key) - 0.15, at(key) + 0.5)); });
  k.aakash = Math.max(k.aakash, 0.55 * eo(seg(t, at('भागवत पुराण'), at('भागवत पुराण') + 0.5)));
  const z = lerp(0.9, 1.05, seg(t, at('भागवत पुराण'), at('और उसी में')));
  let s = `<rect width="1080" height="1920" fill="#0B0620"/>` + stars(t, 90);
  s += cam(540, 900, z, cosmos(540, 900, 470, t, k));
  let cur = null; ORDER.forEach(([id, label, key]) => { if (t >= at(key) - 0.1) cur = [label, key]; });
  if (cur && t > at('आकाश') - 0.2) s += word(cur[0], seg(t, at(cur[1]) - 0.1, at(cur[1]) + 0.25), 1520, '#FFE29A', 130);
  s += title('BHAGAVAT 10.8.37', 260, 60, seg(t, at('भागवत पुराण'), at('भागवत पुराण') + 0.3) * (1 - seg(t, at('आकाश') - 0.3, at('आकाश'))), '#FFE29A');
  s += title('YASHODA NE DEKHA...', 260, 76, seg(t, at('यशोदा ने उस'), at('यशोदा ने उस') + 0.3) * (1 - seg(t, at('आकाश') - 0.3, at('आकाश'))), '#FFF3DC');
  s += title('BRAHMAAND', 230, 84, seg(t, at('आकाश'), at('आकाश') + 0.4), '#F5C04A');
  return s;
}, 'iris');

// 6 ...AND IN IT, GOKUL — AND YASHODA HERSELF
add(at('और उसी में'), at('यशोदा काँप'), (t) => {
  const zin = eio(seg(t, at('और उसी में'), at('और उसी में') + 1.6));
  const self = eo(seg(t, at('ख़ुद यशोदा') - 0.3, at('ख़ुद यशोदा') + 0.6));
  let s = `<rect width="1080" height="1920" fill="#0B0620"/>` + stars(t, 90);
  s += cam(540, 900, lerp(1.05, 3.2, zin), cosmos(540, 900, 470, t, ALL));
  if (zin > 0.5) {
    const k = clamp((zin - 0.5) * 2), R = 430;
    let v = `<clipPath id="gk"><circle cx="540" cy="900" r="${R}"/></clipPath><g clip-path="url(#gk)" opacity="${k.toFixed(2)}">`;
    v += `<g transform="translate(540 900) scale(.62) translate(-540 -1100)">${courtyard(t)}${cow({ x: 900, y: 1330, s: 0.45, t })}`;
    v += `<g opacity="${self.toFixed(2)}">${yashoda({ x: 380, y: 1700, s: 1.0, armL: 20, armR: -20, eyes: 'open', t })}${krishna({ x: 660, y: 1660, s: 0.86, eyes: 'closed', mouth: 'open', armL: 20, armR: -20 })}</g></g></g>`;
    v += `<circle cx="540" cy="900" r="${R}" fill="none" stroke="#F5C04A" stroke-width="10" opacity="${k.toFixed(2)}"/>`;
    s += v;
  }
  s += word('गोकुल', seg(t, at('और उसी में') + 1.0, at('और उसी में') + 1.3) * (1 - seg(t, at('ख़ुद यशोदा') - 0.3, at('ख़ुद यशोदा'))), 1520, '#FFE29A', 140);
  s += word('ख़ुद यशोदा!', seg(t, at('ख़ुद यशोदा'), at('ख़ुद यशोदा') + 0.3), 1520, '#FFE29A', 120);
  return s;
}, 'fade');

// 7 YASHODA TREMBLES — dream? maya? or is my son God himself?
add(at('यशोदा काँप'), at('तभी कान्हा'), (t) => {
  const q = [['SAPNA?', at('ये सपना')], ['MAAYA?', at('माया है')], ['YA MERA BETA...', at('या मेरा बेटा')], ['SWAYAM BHAGWAN?', at('स्वयं भगवान')]];
  const god = eo(seg(t, at('स्वयं भगवान') - 0.2, at('स्वयं भगवान') + 0.8));
  let w = bg('night') + stars(t, 60) + `<g opacity="${god.toFixed(2)}">${rays(700, 1100, 18, 0.12, t)}<circle cx="700" cy="1150" r="520" fill="url(#halo)"/></g>`;
  w += `<g transform="${shake(t, at('यशोदा काँप'), 1.6, 9)}">${yashoda({ x: 330, y: 1720, s: 1.05, armL: 60, elbowL: 80, armR: -60, elbowR: -80, eyes: 'open', t })}</g>`;
  w += krishna({ x: 760, y: 1680, s: 0.92, eyes: 'closed', armL: 20, armR: -20, glow: god });
  let s = cam(540, lerp(1250, 1100, seg(t, at('यशोदा काँप'), at('तभी कान्हा'))), lerp(1.25, 1.0, seg(t, at('यशोदा काँप'), at('तभी कान्हा'))), w);
  let cur = null; q.forEach(([txt, t0]) => { if (t >= t0 - 0.05) cur = [txt, t0]; });
  if (cur) s += title(cur[0], 300, cur[0].length > 10 ? 96 : 130, seg(t, cur[1] - 0.05, cur[1] + 0.25), cur[0].startsWith('SWAYAM') ? '#F5C04A' : '#FFF3DC');
  else s += title('YASHODA KAANP GAYIN', 300, 84, seg(t, at('यशोदा काँप'), at('यशोदा काँप') + 0.3), '#FFF3DC');
  return s;
}, 'fade');

// 8 MAYA — she forgets, and lifts her son into her lap
add(at('तभी कान्हा'), at('सोचिए'), (t) => {
  const mist = seg(t, at('तभी कान्हा') + 0.5, at('यशोदा सब भूल') + 0.6);
  const lap = eio(seg(t, at('और बेटे को') - 0.2, at('और बेटे को') + 1.2));
  let w = `<g opacity="${(1 - mist).toFixed(2)}">${bg('night')}${stars(t, 60)}</g><g opacity="${mist.toFixed(2)}">${courtyard(t)}</g>`;
  w += yashoda({ x: 420, y: 1720, s: 1.05, armL: lerp(20, 60, lap), elbowL: lerp(0, 90, lap), armR: lerp(-20, -60, lap), elbowR: lerp(0, -90, lap), eyes: 'closed', t });
  w += krishna({ x: lerp(760, 470, lap), y: lerp(1680, 1500, lap), s: lerp(0.92, 0.62, lap), eyes: 'closed', armL: 20, armR: -20 });
  // the maya mist sweeping across
  if (mist > 0 && mist < 1) for (let i = 0; i < 8; i++) w += cloud(lerp(-600, 1700, mist) + (i % 3) * 200 - 300, 300 + i * 200, 2.2, '#FFD9E8', '#F2B8D0');
  let s = cam(540, lerp(1150, 1250, lap), lerp(1.0, 1.25, lap), w);
  s += title('KANHA KI MAAYA', 300, 92, seg(t, at('तभी कान्हा') + 0.4, at('तभी कान्हा') + 0.7) * (1 - seg(t, at('यशोदा सब भूल') - 0.2, at('यशोदा सब भूल'))), '#7A2E12');
  s += title('SAB BHOOL GAYIN', 300, 96, seg(t, at('यशोदा सब भूल'), at('यशोदा सब भूल') + 0.3) * (1 - seg(t, at('और बेटे को') - 0.2, at('और बेटे को'))), '#7A2E12');
  s += title('PHIR SE GOD MEIN', 300, 96, seg(t, at('और बेटे को') + 0.4, at('और बेटे को') + 0.7), '#7A2E12');
  return s;
}, 'wipe');

// 9 THE THOUGHT — the one holding the universe wanted to be only a child in his mother's lap
add(at('सोचिए'), at('अगली कहानी'), (t) => {
  const warm = eo(seg(t, at('वो माँ की') - 0.3, at('वो माँ की') + 0.6));
  let w = `<g opacity="${(1 - warm).toFixed(2)}"><rect x="-300" y="-300" width="1700" height="2600" fill="#0B0620"/>${stars(t, 80)}</g><g opacity="${warm.toFixed(2)}">${bg('gold')}${rays(540, 1200, 18, 0.14, t)}<circle cx="540" cy="1250" r="460" fill="url(#halo)"/></g>`;
  w += `<g transform="translate(540 ${lerp(820, 520, warm).toFixed(0)}) scale(${lerp(1, 0.55, warm).toFixed(3)}) translate(-540 -820)">${cosmos(540, 820, 360, t, ALL)}</g>`;
  w += `<g opacity="${clamp(warm * 1.4).toFixed(2)}">${yashoda({ x: 520, y: 1760, s: 1.0, armL: 60, elbowL: 90, armR: -60, elbowR: -90, eyes: 'closed', t })}${krishna({ x: 560, y: 1560, s: 0.6, eyes: 'closed', armL: 20, armR: -20 })}</g>`;
  w += dust(t, 40, '#FFF0C0', 40);
  let s = cam(540, 960, lerp(1.0, 1.05, seg(t, at('सोचिए'), at('अगली कहानी'))), w);
  s += title('SOCHIYE...', 300, 100, seg(t, at('सोचिए'), at('सोचिए') + 0.3) * (1 - seg(t, at('जिसके मुँह') - 0.1, at('जिसके मुँह'))), '#FFF3DC');
  s += title('BRAHMAAND WAALA', 1130, 84, seg(t, at('जिसके मुँह') + 0.3, at('जिसके मुँह') + 0.6) * (1 - seg(t, at('वो माँ की') - 0.2, at('वो माँ की'))), '#FFE29A');
  s += title('BAS EK BACHCHA', 260, 120, seg(t, at('बस एक बच्चा'), at('बस एक बच्चा') + 0.3), '#4A1A08', 'Baloo', 800, '❤');
  return s;
}, 'fade');

// 10 NEXT — Kaliya
add(at('अगली कहानी'), 999, (t) => {
  const rise = eo(seg(t, at('अगली कहानी') + 0.3, at('कालिया') + 0.2));
  let w = bg('night') + stars(t, 50) + moon(860, 300, 50);
  w += kaliya({ x: 540, y: 1600, s: 1.1, t, rise, n: 5 });
  w += poisonWater(t, 1560) + fumes(t, 1560, 8, 0.3);
  let s = cam(540, 1100, lerp(1.1, 1.0, seg(t, at('अगली कहानी'), at('अगली कहानी') + 6)), w);
  s += title('AGLI KAHANI', 300, 70, seg(t, at('अगली कहानी'), at('अगली कहानी') + 0.3), '#FFF3DC');
  s += title('KALIYA NAAG', 420, 140, seg(t, at('कालिया') - 0.3, at('कालिया')), '#7CFF9A');
  return s;
}, 'whip');

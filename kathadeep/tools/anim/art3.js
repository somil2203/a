// Characters & worlds set 3: Balarama, cosmos-in-the-mouth, Kaliya, poisoned Yamuna, kadamba, naga-patni, Garuda, island.
function balaram(o = {}) {
  return krishna2({ ...o, noFeather: true })
    .replace(/url\(#kBlueV\)/g, '#EAC9AE').replace(/url\(#kBlue\)/g, '#F4DCC6').replace(/#4E7EE6/g, '#F4DCC6').replace(/#3E66C8/g, '#E2BC9E').replace(/#3A60BE/g, '#D9AE8E')
    .replace(/url\(#pitam\)/g, '#2F5FB8').replace(/#F0B42A/g, '#264E9E').replace(/#E39A18/g, '#1E4088').replace(/#E7A320/g, '#2A56A8').replace(/#E86A3E/g, '#3A72C8').replace(/#E0573A/g, '#2E62B8');
}
function mudLump(x, y, s) { return G2(x, y, s, `<path d="M-30 0 C-40 -24 -10 -40 6 -30 C30 -40 44 -12 30 4 C20 18 -20 18 -30 0Z" fill="#7A4A2A"/><circle cx="-8" cy="-14" r="5" fill="#9A6A44"/><circle cx="14" cy="-6" r="4" fill="#5E3A20"/>`); }

// ---- the universe seen in Krishna's mouth: elements reveal one by one (k = map of 0..1 per element)
function cosmos(cx, cy, r, t, k = {}) {
  const on = (n) => clamp(k[n] ?? 0);
  let g = `<clipPath id="cosmoClip"><circle cx="${cx}" cy="${cy}" r="${r}"/></clipPath><g clip-path="url(#cosmoClip)">`;
  g += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="#0B0620"/>`;
  // aakash: nebula + galaxy
  if (on('aakash')) {
    g += `<g opacity="${on('aakash').toFixed(2)}"><circle cx="${cx - r * 0.3}" cy="${cy - r * 0.3}" r="${r * 0.7}" fill="#5A2A8A" opacity=".45"/><circle cx="${cx + r * 0.35}" cy="${cy + r * 0.2}" r="${r * 0.6}" fill="#1E4A8A" opacity=".45"/>`;
    for (let i = 0; i < 260; i++) { const a = i * 0.21 + t * 0.15, rr = (i / 260) * r * 0.9, arm = (i % 2) * Math.PI;
      g += `<circle cx="${(cx + Math.cos(a + arm) * rr).toFixed(1)}" cy="${(cy + Math.sin(a + arm) * rr * 0.55).toFixed(1)}" r="${(1 + rnd(i) * 2.5).toFixed(1)}" fill="${['#FFF6DA', '#C9B8FF', '#9FD0FF'][i % 3]}" opacity="${(0.4 + 0.6 * rnd(i + 3)).toFixed(2)}"/>`; }
    g += `<circle cx="${cx}" cy="${cy}" r="${r * 0.12}" fill="#FFF0C8" opacity=".9"/><circle cx="${cx}" cy="${cy}" r="${r * 0.3}" fill="url(#halo)"/></g>`;
  }
  // dishaayein: compass rose
  if (on('disha')) { const o = on('disha'); g += `<g opacity="${(o * 0.85).toFixed(2)}" transform="translate(${cx} ${cy}) rotate(${(t * 6).toFixed(1)})">${[0, 45, 90, 135, 180, 225, 270, 315].map((a, i) => `<path d="M0 0 L${i % 2 ? 10 : 18} ${-(i % 2 ? r * 0.55 : r * 0.85)} L0 ${-(i % 2 ? r * 0.5 : r * 0.78)} L${-(i % 2 ? 10 : 18)} ${-(i % 2 ? r * 0.55 : r * 0.85)}Z" fill="#F5C04A" opacity="${i % 2 ? 0.5 : 0.9}" transform="rotate(${a})"/>`).join('')}</g>`; }
  // prithvi (earth) with parvat, dweep, samudra
  const ek = Math.max(on('parvat'), on('dweep'), on('samudra'), on('prithvi'));
  if (ek) {
    const er = r * lerp(0.42, 0.5, on('prithvi'));
    g += `<g opacity="${ek.toFixed(2)}"><circle cx="${cx}" cy="${cy}" r="${er * 1.2}" fill="#4FA8FF" opacity=".18"/><circle cx="${cx}" cy="${cy}" r="${er}" fill="${on('samudra') ? '#2F7FD8' : '#1E3A6A'}"/>`;
    if (on('dweep')) g += `<g opacity="${on('dweep').toFixed(2)}"><path d="M${cx - er * 0.6} ${cy - er * 0.2} c20 -60 120 -70 150 -20 c30 50 -40 90 -90 70 c-40 -10 -70 -20 -60 -50z" fill="#4FAE5E"/><path d="M${cx + er * 0.1} ${cy + er * 0.25} c30 -40 110 -20 120 20 c10 40 -70 60 -100 40 c-20 -14 -30 -40 -20 -60z" fill="#5BB86A"/><circle cx="${cx + er * 0.5}" cy="${cy - er * 0.45}" r="${er * 0.12}" fill="#4FAE5E"/></g>`;
    if (on('parvat')) g += `<g opacity="${on('parvat').toFixed(2)}"><path d="M${cx - er * 0.5} ${cy - er * 0.08} l40 -70 l40 70z M${cx - er * 0.32} ${cy - er * 0.1} l30 -50 l30 50z M${cx + er * 0.22} ${cy + er * 0.26} l34 -60 l34 60z" fill="#8A6A4A"/><path d="M${cx - er * 0.5 + 40} ${cy - er * 0.08 - 70} l-14 24 l28 0z" fill="#FFFFFF"/></g>`;
    if (on('samudra')) for (let i = 0; i < 6; i++) g += `<path d="M${cx - er * 0.7 + i * er * 0.25} ${cy + er * 0.55 - (i % 2) * 20} q14 -10 28 0 q14 10 28 0" stroke="#BFE3FF" stroke-width="5" fill="none" opacity="${(0.5 + 0.4 * Math.sin(t * 3 + i)).toFixed(2)}"/>`;
    g += `<path d="M${cx - er} ${cy} A${er} ${er} 0 0 0 ${cx + er} ${cy}" fill="#000000" opacity=".22"/></g>`;
  }
  // agni, vayu, chandrama, taare around the earth
  if (on('agni')) { const a = on('agni'); g += `<g opacity="${a.toFixed(2)}">${sun(cx - r * 0.62, cy - r * 0.5, r * 0.1, '#FFB43A')}${flame(cx - r * 0.62, cy - r * 0.42, 1.0, t, 3)}</g>`; }
  if (on('vayu')) { const a = on('vayu'); for (let i = 0; i < 4; i++) g += `<path d="M${cx - r * 0.85} ${cy + r * (0.1 + i * 0.12)} q${r * 0.3} -${r * 0.12} ${r * 0.6} 0 q${r * 0.2} ${r * 0.08} ${r * 0.34} -${r * 0.06}" stroke="#DDEBFF" stroke-width="6" fill="none" stroke-linecap="round" opacity="${(a * 0.7).toFixed(2)}" transform="translate(${((t * 80 + i * 40) % 60).toFixed(0)} 0)"/>`; }
  if (on('chandra')) g += `<g opacity="${on('chandra').toFixed(2)}">${moon(cx + r * 0.6, cy - r * 0.55, r * 0.09)}</g>`;
  if (on('taare')) for (let i = 0; i < 40; i++) { const a = rnd(i + 40) * Math.PI * 2, rr = r * (0.55 + rnd(i + 41) * 0.42);
    g += `<path d="M0 -10 L3 -3 L10 0 L3 3 L0 10 L-3 3 L-10 0 L-3 -3Z" fill="#FFF6DA" opacity="${(on('taare') * (0.5 + 0.5 * Math.sin(t * 4 + i))).toFixed(2)}" transform="translate(${(cx + Math.cos(a) * rr).toFixed(0)} ${(cy + Math.sin(a) * rr).toFixed(0)}) scale(${(0.6 + rnd(i) * 0.9).toFixed(2)})"/>`; }
  // ringed planet for richness
  if (on('aakash')) g += `<g opacity="${on('aakash').toFixed(2)}" transform="translate(${cx + r * 0.62} ${cy + r * 0.45})"><ellipse rx="${r * 0.16}" ry="${r * 0.04}" fill="none" stroke="#E8C88A" stroke-width="6" transform="rotate(-18)"/><circle r="${r * 0.08}" fill="#D9925A"/></g>`;
  return g + `</g><circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#F5C04A" stroke-width="10" opacity=".9"/>`;
}

// ---- Yamuna poisoned pool
function poisonWater(t, y, x0 = -300, x1 = 1400) {
  let p = `M${x0} ${y}`; for (let x = x0; x <= x1; x += 40) p += ` L${x} ${(y + Math.sin(x / 70 + t * 2.2) * 12).toFixed(1)}`; p += ` V2600 H${x0}Z`;
  let s = `<path d="${p}" fill="#1E4A4A"/><path d="${p}" transform="translate(0 40)" fill="#163A3C"/><path d="${p}" transform="translate(0 110)" fill="#0F2C2E"/>`;
  for (let i = 0; i < 14; i++) { const bx = ((rnd(i) * 1300 + t * 20 * (i % 3)) % 1300) - 100, by = y + 40 + rnd(i + 1) * 300, br = 6 + rnd(i + 2) * 12, ph = (t * 0.7 + rnd(i + 3)) % 1;
    s += `<circle cx="${bx.toFixed(0)}" cy="${(by - ph * 40).toFixed(0)}" r="${(br * (1 - ph * 0.5)).toFixed(1)}" fill="none" stroke="#7CFF9A" stroke-width="3" opacity="${(0.6 * (1 - ph)).toFixed(2)}"/>`; }
  return s;
}
function fumes(t, y, n = 8, op = 0.35) {
  let s = ''; for (let i = 0; i < n; i++) { const x = 60 + i * 140 + Math.sin(t + i) * 20, ph = (t * 0.25 + i * 0.13) % 1;
    s += `<path d="M${x.toFixed(0)} ${(y - ph * 500).toFixed(0)} c-40 -40 40 -80 0 -120 c-40 -40 40 -80 0 -120" stroke="#6BE08A" stroke-width="${(26 * (1 - ph * 0.5)).toFixed(0)}" fill="none" stroke-linecap="round" opacity="${(op * Math.sin(ph * Math.PI)).toFixed(2)}"/>`; }
  return s;
}
function bird(x, y, s, flap, falling = false) {
  const w = Math.sin(flap) * 18;
  return G2(x, y, s, `<g ${falling ? 'transform="rotate(70)"' : ''}><path d="M0 0 Q-30 ${-20 - w} -60 ${-4 - w}" stroke="#2A2030" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M0 0 Q30 ${-20 - w} 60 ${-4 - w}" stroke="#2A2030" stroke-width="7" fill="none" stroke-linecap="round"/><circle r="7" fill="#2A2030"/></g>`);
}
function kadamb(x, y, s, t) {
  let g = `<path d="M-16 0 C-14 -100 -20 -200 -10 -300 L10 -300 C20 -200 14 -100 16 0Z" fill="#6B4A2E"/><path d="M0 -220 C40 -250 70 -260 110 -250" stroke="#6B4A2E" stroke-width="16" fill="none" stroke-linecap="round"/>
    <circle cx="0" cy="-380" r="150" fill="#22693F"/><circle cx="-100" cy="-320" r="100" fill="#2F8A55"/><circle cx="100" cy="-330" r="110" fill="#2F8A55"/><circle cx="0" cy="-440" r="110" fill="#2F8A55"/>`;
  for (let i = 0; i < 22; i++) { const a = rnd(i + 70) * Math.PI * 2, rr = 40 + rnd(i + 71) * 150; g += `<circle cx="${(Math.cos(a) * rr).toFixed(0)}" cy="${(-370 + Math.sin(a) * rr * 0.7).toFixed(0)}" r="13" fill="#F5C04A"/><circle cx="${(Math.cos(a) * rr - 3).toFixed(0)}" cy="${(-373 + Math.sin(a) * rr * 0.7).toFixed(0)}" r="5" fill="#FFE7A0"/>`; }
  return G2(x, y, s, g);
}
// ---- Kaliya: coiled body + fan of hoods. o: n hoods, rise (0..1), bow (0..1), prints (bool), angry
function kaliya(o = {}) {
  const t = o.t || 0, n = o.n || 5, bow = o.bow || 0, rise = o.rise ?? 1;
  let s = '';
  // coils (in water)
  for (let i = 0; i < 3; i++) s += `<ellipse cx="${-160 + i * 160}" cy="${40 + (i % 2) * 20}" rx="150" ry="52" fill="none" stroke="#1F3A5A" stroke-width="70"/><ellipse cx="${-160 + i * 160}" cy="${40 + (i % 2) * 20}" rx="150" ry="52" fill="none" stroke="#2C5A80" stroke-width="40" stroke-dasharray="30 22"/>`;
  // neck
  s += `<path d="M-60 40 C-80 -80 -40 ${-200 * rise} 0 ${-280 * rise} C40 ${-200 * rise} 80 -80 60 40Z" fill="#244A6E"/><path d="M-20 30 C-30 -60 -10 ${-170 * rise} 0 ${-240 * rise} C10 ${-170 * rise} 30 -60 20 30Z" fill="#E8D49A" opacity=".85"/>`;
  for (let j = 0; j < 6; j++) s += `<path d="M-22 ${-20 - j * 36 * rise} h44" stroke="#C9B276" stroke-width="3"/>`;
  // hoods
  const hy = -300 * rise + bow * 120;
  for (let i = 0; i < n; i++) {
    const a = (i - (n - 1) / 2) * 24, bob = Math.sin(t * 3 + i) * 8 * (1 - bow);
    const tongue = Math.sin(t * 9 + i * 2) > 0.4 && bow < 0.5;
    s += `<g transform="translate(0 ${(hy + bob).toFixed(1)}) rotate(${a.toFixed(1)}) translate(0 -140)">
      <path d="M0 150 C-26 110 -96 70 -96 -6 C-96 -64 -50 -96 0 -96 C50 -96 96 -64 96 -6 C96 70 26 110 0 150Z" fill="#1E3F60"/>
      <path d="M0 132 C-20 100 -76 62 -76 -2 C-76 -50 -40 -76 0 -76 C40 -76 76 -50 76 -2 C76 62 20 100 0 132Z" fill="#2F6A92"/>
      <path d="M-34 -6 a20 20 0 1 0 0.1 0 M34 -6 a20 20 0 1 0 0.1 0" fill="none" stroke="#E8D49A" stroke-width="9"/><path d="M-14 -6 q14 14 28 0" stroke="#E8D49A" stroke-width="8" fill="none"/>
      <path d="M0 60 C-10 40 -10 20 0 10 C10 20 10 40 0 60Z" fill="#E8D49A" opacity=".5"/>
      <path d="M-40 -84 C-40 -120 -18 -136 0 -136 C18 -136 40 -120 40 -84 C40 -70 20 -60 0 -60 C-20 -60 -40 -70 -40 -84Z" fill="#244E74"/>
      <path d="M-24 -118 q24 -14 48 0" stroke="#3E7AA6" stroke-width="5" fill="none"/>
      ${o.angry !== false && bow < 0.5 ? `<ellipse cx="-17" cy="-96" rx="8" ry="6" fill="#FF3A2A"/><ellipse cx="17" cy="-96" rx="8" ry="6" fill="#FF3A2A"/><circle cx="-17" cy="-96" r="12" fill="#FF3A2A" opacity=".25"/><circle cx="17" cy="-96" r="12" fill="#FF3A2A" opacity=".25"/>`
                                           : `<path d="M-24 -96 q7 5 14 0 M10 -96 q7 5 14 0" stroke="#0E2236" stroke-width="4" fill="none"/>`}
      ${tongue ? `<path d="M0 -60 l0 26 m0 0 l-8 12 m8 -12 l8 12" stroke="#E0303A" stroke-width="4" fill="none" stroke-linecap="round"/>` : ''}
      ${o.prints ? `<g transform="translate(0 30) scale(1.1)"><ellipse cx="0" cy="10" rx="15" ry="24" fill="#FFF6DA" opacity=".9"/>${[-11, -4, 3, 10].map((x) => `<circle cx="${x}" cy="-20" r="3.6" fill="#FFF6DA" opacity=".9"/>`).join('')}</g>` : ''}
    </g>`;
  }
  return G2(o.x || 0, o.y || 0, o.s || 1, s);
}
function nagapatni(o = {}) {
  const hood = `<g transform="translate(0 -440)"><path d="M0 60 C-40 40 -110 0 -110 -60 C-110 -110 -50 -140 0 -140 C50 -140 110 -110 110 -60 C110 0 40 40 0 60Z" fill="#2A5478"/><path d="M0 40 C-24 26 -70 -4 -70 -50 C-70 -86 -30 -104 0 -104 C30 -104 70 -86 70 -50 C70 -4 24 26 0 40Z" fill="#E8D49A" opacity=".8"/></g>`;
  return G2(o.x || 0, o.y || 0, o.s || 1, hood) + gopi2({ veil: '#2E8A6E', top: '#1E6A8A', skirt: '#2A5478', armL: 38, elbowL: -112, armR: -38, elbowR: 112, ...o });
}
function garuda(x, y, s, t) {
  const f = Math.sin(t * 6) * 14;
  return G2(x, y, s, `<path d="M0 0 C-80 ${-60 - f} -200 ${-70 - f} -300 ${-20 - f} C-220 ${-10 - f / 2} -140 10 -40 30Z" fill="#E09A2A"/><path d="M0 0 C80 ${-60 - f} 200 ${-70 - f} 300 ${-20 - f} C220 ${-10 - f / 2} 140 10 40 30Z" fill="#E09A2A"/>
    <path d="M-240 ${-24 - f} l-30 18 M-200 ${-30 - f} l-28 22 M240 ${-24 - f} l30 18 M200 ${-30 - f} l28 22" stroke="#B8701A" stroke-width="8"/>
    <ellipse cx="0" cy="20" rx="46" ry="70" fill="#D8432F"/><circle cx="0" cy="-50" r="36" fill="#F5C04A"/><path d="M-10 -40 l40 10 l-34 14z" fill="#C98A1E"/><circle cx="8" cy="-56" r="5" fill="#2A1B3D"/>
    <path d="M-24 -84 l12 -30 l12 22 l12 -26 l10 30" fill="url(#goldG)"/><path d="M-30 80 l30 50 l30 -50z" fill="#E09A2A"/>`);
}
function island(x, y, s, t) {
  return G2(x, y, s, `<ellipse cx="0" cy="10" rx="300" ry="50" fill="#1E5A8A" opacity=".6"/><path d="M-260 10 C-200 -80 -60 -110 40 -100 C160 -90 240 -40 260 10Z" fill="#E8D49A"/><path d="M-200 0 C-140 -60 -40 -80 40 -76 C130 -70 190 -30 210 0Z" fill="#5BB86A"/>
    ${tree2(-60, -70, 0.5, Math.sin(t * 2) * 3)}${tree2(80, -66, 0.42, Math.sin(t * 2 + 1) * 3)}`);
}

// Set 4: Vamana, Bali, Shukracharya, Trivikrama foot, swarga, Brahma (four faces), chaturbhuj Vishnu, calf, cave, gada.
function chhatra(x, y, s, t) {
  return G2(x, y, s, `<rect x="-5" y="-10" width="10" height="230" rx="5" fill="#7A4A22"/><path d="M-110 0 Q0 -90 110 0Z" fill="#E86A3E"/><path d="M-110 0 Q0 -90 110 0" stroke="#F5C04A" stroke-width="7" fill="none"/>
    ${[-80, -40, 0, 40, 80].map((xx) => `<path d="M${xx} ${-Math.sqrt(Math.max(0, 1 - (xx / 110) ** 2)) * 60 + 4} l0 22" stroke="#F5C04A" stroke-width="5"/><circle cx="${xx}" cy="${-Math.sqrt(Math.max(0, 1 - (xx / 110) ** 2)) * 60 + 30}" r="5" fill="#F5C04A"/>`).join('')}<circle cx="0" cy="-60" r="9" fill="#F5C04A"/>`);
}
function vamana(o = {}) {   // dwarf brahmin boy: shaved head with shikha, janeu, deerskin, kamandalu, chhatra
  const t = o.t || 0;
  let s = krishna2({ ...o, x: 0, y: 0, s: 1, noFeather: true, armR: o.armR ?? -150, elbowR: o.elbowR ?? -10, flute: false })
    .replace(/<path d="M-74 -566 L74 -566 L66 -612[^>]*>/, '').replace(/<rect x="-78" y="-576"[^>]*\/>/, '');
  s = s.replace(/(<path d="M-82 -506 C-84 -570[^"]*" fill=")#1F1A3A/, '$1#3A62C2').replace(/<path d="M-86 -480 C-104[^>]*>/, '')
       .replace(/<circle cx="0" cy="-566"[^>]*\/>|<circle cx="-40" cy="-566"[^>]*\/>|<circle cx="40" cy="-566"[^>]*\/>|<circle cx="0" cy="-620"[^>]*\/>|<circle cx="-30" cy="-612"[^>]*\/>|<circle cx="30" cy="-612"[^>]*\/>/g, '');
  s += `<path d="M-4 -592 C-10 -640 14 -672 32 -660 C18 -652 10 -630 10 -594Z" fill="#1F1A3A"/>
        <path d="M-56 -404 L58 -290" stroke="#FFF6E0" stroke-width="7"/><path d="M-70 -296 C-40 -320 40 -320 70 -296 L64 -250 C30 -270 -30 -270 -64 -250Z" fill="#C9955A"/>
        <circle cx="-40" cy="-280" r="5" fill="#8A5A2A"/><circle cx="-10" cy="-286" r="5" fill="#8A5A2A"/><circle cx="24" cy="-282" r="5" fill="#8A5A2A"/>`;
  s += `<g transform="translate(-118 -240)"><path d="M-30 0 C-34 40 34 40 30 0 L22 -26 L-22 -26Z" fill="#B5562E"/><rect x="-24" y="-34" width="48" height="10" rx="5" fill="#8E4426"/><path d="M28 -20 q26 -6 30 -26" stroke="#B5562E" stroke-width="7" fill="none"/></g>`;
  if (o.umbrella !== false) s += chhatra(96, -760, 0.9, t);
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}
function bali(o = {}) {   // the generous asura king
  const S = '#D9A27A';
  let s = '';
  if (o.glow) s += `<circle cx="0" cy="-460" r="360" fill="url(#halo)" opacity="${o.glow}"/>`;
  s += `<path d="M-100 -400 C-114 -260 -126 -120 -130 0 L130 0 C126 -120 114 -260 100 -400Z" fill="#5A2A7A"/><path d="M-130 -22 L130 -22 L132 0 L-132 0Z" fill="url(#goldG)"/><path d="M-16 -400 L-24 0 L24 0 L16 -400Z" fill="url(#goldG)"/>`;
  s += `<path d="M-94 -540 C-108 -490 -104 -430 -100 -390 L100 -390 C104 -430 108 -490 94 -540 Q0 -560 -94 -540Z" fill="${S}"/>`;
  s += `<path d="M-100 -404 Q0 -380 100 -404 L100 -380 Q0 -356 -100 -380Z" fill="url(#goldG)"/><path d="M-70 -540 Q0 -470 70 -540" stroke="url(#goldG)" stroke-width="16" fill="none"/>`;
  s += `<path d="M-96 -540 C-140 -500 -150 -300 -120 -180 L-100 -200 C-120 -300 -110 -460 -80 -520Z" fill="#8E1F2A"/>`;   // cape
  if (o.folded) { s += limb(-92, -530, 40, -110, 112, 98, 42, 32, S, '') + limb(92, -530, -40, 110, 112, 98, 42, 32, S, '') + `<path d="M-16 -430 C-18 -470 -6 -496 0 -504 C6 -496 18 -470 16 -430Z" fill="${S}"/>`; }
  else { s += limb(-92, -530, o.armL ?? 18, o.elbowL ?? 12, 120, 104, 42, 32, S, handShape(S, 1.2), { bangle: true, armlet: true });
         s += limb(92, -530, o.armR ?? -18, o.elbowR ?? -12, 120, 104, 42, 32, S, handShape(S, 1.2), { bangle: true, armlet: true, held: o.jal ? `<g transform="rotate(${-(o.armR ?? -18) - (o.elbowR ?? -12)})"><path d="M-26 -10 C-30 30 30 30 26 -10Z" fill="url(#goldG)"/><path d="M20 -6 q30 -4 40 10" stroke="#C98A1E" stroke-width="6" fill="none"/></g>` : '' }); }
  s += `<path d="M-22 -580 L-22 -536 L22 -536 L22 -580Z" fill="${S}"/>`;
  s += `<g transform="${R2(o.bow || 0, 0, -560)}"><path d="M-74 -630 C-76 -570 -44 -548 0 -548 C44 -548 76 -570 74 -630 C74 -682 44 -710 0 -710 C-44 -710 -74 -682 -74 -630Z" fill="${S}"/>
    <path d="M-76 -650 C-92 -600 -84 -560 -64 -548 C-70 -590 -70 -620 -62 -640Z M76 -650 C92 -600 84 -560 64 -548 C70 -590 70 -620 62 -640Z" fill="#1F1A3A"/>
    <path d="M-30 -588 Q-14 -600 0 -592 Q14 -600 30 -588 Q14 -582 0 -588 Q-14 -582 -30 -588Z" fill="#1F1A3A"/>
    ${o.eyes === 'open' ? openEye(-28, -628, 12) + openEye(28, -628, 12) : closedEye(-28, -628, 13) + `<g transform="scale(-1 1)">${closedEye(-28, -628, 13)}</g>`}
    <path d="M-44 -652 Q-28 -662 -12 -652 M12 -652 Q28 -662 44 -652" stroke="#1F1A3A" stroke-width="4.5" fill="none" stroke-linecap="round"/>
    ${o.laugh ? `<path d="M-16 -574 Q0 -556 16 -574Z" fill="#8A2A3A"/>` : `<path d="M-14 -574 Q0 -564 14 -574" stroke="#8A2A3A" stroke-width="4.5" fill="none" stroke-linecap="round"/>`}
    <path d="M-80 -690 L80 -690 L66 -760 L40 -738 L20 -790 L0 -748 L-20 -790 L-40 -738 L-66 -760Z" fill="url(#goldG)"/><rect x="-82" y="-700" width="164" height="22" rx="8" fill="#C98A1E"/><circle cx="0" cy="-690" r="11" fill="#2E7FB8" stroke="#FFF0B8" stroke-width="2"/></g>`;
  return G2(o.x || 0, o.y || 0, o.s || 1, s, o.flip);
}
function shukra(o = {}) {   // the asura guru: old sage, white beard and hair, saffron, rudraksha
  return nand2({ ...o }).replace(/#F08A2C/g, '#F4F1EA').replace(/#C9631A/g, '#DCD6C8').replace(/url\(#creamG\)/g, '#E8762E').replace(/#F4ECDC/g, '#E8762E').replace(/#E86A3E/g, '#8E4426');
}
function swarga(x, y, s, t) {   // heaven: palace on clouds
  return G2(x, y, s, `${cloud(-160, 40, 1.4)}${cloud(160, 50, 1.3)}${cloud(0, 70, 1.6)}
    <rect x="-150" y="-200" width="300" height="200" fill="#F7E6C8"/><path d="M-170 -200 L0 -320 L170 -200Z" fill="url(#goldG)"/><rect x="-40" y="-120" width="80" height="120" rx="40" fill="#C98A1E"/>
    ${[-110, -70, 70, 110].map((xx) => `<rect x="${xx - 10}" y="-190" width="20" height="190" fill="#EAD7B4"/>`).join('')}<circle cx="0" cy="-330" r="14" fill="#FFE7A0"/>`);
}
function giantLeg(x, y, s, k, t) {   // Trivikrama's foot coming down from the sky; (x,y) = sole position
  return G2(x, y, s, `<g opacity="${clamp(k).toFixed(2)}"><circle cx="0" cy="-60" r="420" fill="url(#halo)" opacity=".8"/>
    <path d="M-120 -2400 C-110 -1400 -140 -600 -110 -150 L120 -150 C140 -600 110 -1400 120 -2400Z" fill="url(#kBlue)"/>
    <path d="M-130 -400 Q0 -360 130 -400 L130 -330 Q0 -290 -130 -330Z" fill="url(#pitam)"/>
    <path d="M-110 -160 C-180 -150 -260 -110 -270 -40 C-270 10 -200 10 -100 6 L120 6 C150 -20 140 -100 110 -160Z" fill="url(#kBlue)"/>
    <path d="M-120 -190 Q0 -160 120 -190 L120 -160 Q0 -134 -120 -160Z" fill="url(#goldG)"/>
    ${[0, 1, 2, 3, 4].map((i) => `<ellipse cx="${-262 + i * 30}" cy="${-14 - (i === 0 ? 8 : 0)}" rx="14" ry="12" fill="#3E66C8"/>`).join('')}
    <path d="M-230 -6 C-140 -20 -40 -20 100 -6" stroke="#E86A8A" stroke-width="6" fill="none" opacity=".5"/></g>`);
}
function lotus(x, y, s) {
  return G2(x, y, s, `${[-150, -100, -50, 0, 50, 100, 150].map((a) => `<path d="M0 0 C-40 -40 -40 -150 0 -190 C40 -150 40 -40 0 0Z" fill="${Math.abs(a) > 90 ? '#E87AA0' : '#F7A8C4'}" transform="rotate(${a * 0.55})"/>`).join('')}
    <ellipse cx="0" cy="0" rx="190" ry="40" fill="#2E8A4E"/><ellipse cx="0" cy="-6" rx="120" ry="24" fill="#F5C04A"/>`);
}
function brahma(o = {}) {   // four-faced creator, seated on a lotus; three faces visible
  const S = '#E9A06A', t = o.t || 0;
  let s = '';
  if (o.glow) s += `<circle cx="0" cy="-420" r="380" fill="url(#halo)" opacity="${o.glow}"/>`;
  s += lotus(0, 40, 1.2);
  s += `<path d="M-160 0 C-160 -60 -100 -90 0 -90 C100 -90 160 -60 160 0 Q0 30 -160 0Z" fill="#D8432F"/><path d="M-160 -4 Q0 26 160 -4" stroke="#F5C04A" stroke-width="8" fill="none"/>`;
  s += `<path d="M-100 -380 C-112 -260 -120 -160 -110 -70 L110 -70 C120 -160 112 -260 100 -380 Q0 -400 -100 -380Z" fill="${S}"/>`;
  s += `<path d="M-100 -380 C-40 -330 40 -230 100 -150" stroke="#F5C04A" stroke-width="14" fill="none"/><path d="M-80 -120 Q0 -96 80 -120 L80 -70 Q0 -50 -80 -70Z" fill="#D8432F"/>`;
  const book = `<g transform="rotate(${-(o.armL ?? 50) - (o.elbowL ?? 70)})"><rect x="-34" y="-24" width="68" height="44" rx="4" fill="#C98A1E"/><path d="M0 -24 L0 20" stroke="#7A4A12" stroke-width="3"/><path d="M-28 -14 h22 M-28 -4 h22 M6 -14 h22 M6 -4 h22" stroke="#FFF0C8" stroke-width="3"/></g>`;
  const kam = `<g transform="rotate(${-(o.armR ?? -50) - (o.elbowR ?? -70)})"><path d="M-26 0 C-30 40 30 40 26 0 L18 -20 L-18 -20Z" fill="url(#goldG)"/></g>`;
  s += limb(-96, -370, o.armL ?? 50, o.elbowL ?? 70, 110, 96, 40, 30, S, handShape(S, 1.1), { bangle: true, held: book });
  s += limb(96, -370, o.armR ?? -50, o.elbowR ?? -70, 110, 96, 40, 30, S, handShape(S, 1.1), { bangle: true, held: kam });
  if (o.folded) s += `<path d="M-16 -250 C-18 -290 -6 -316 0 -324 C6 -316 18 -290 16 -250Z" fill="${S}"/>`;
  const face = (dx, sc, side) => `<g transform="translate(${dx} 0) scale(${sc} 1)">
      <path d="M-62 -470 C-64 -420 -36 -400 0 -400 C36 -400 64 -420 62 -470 C62 -514 36 -536 0 -536 C-36 -536 -62 -514 -62 -470Z" fill="${S}"/>
      <path d="M-64 -470 C-70 -400 -40 -340 0 -330 C40 -340 70 -400 64 -470 C52 -440 34 -432 0 -434 C-34 -432 -52 -440 -64 -470Z" fill="#F7F4EE"/>
      ${closedEye(-22, -478, 10)}<g transform="scale(-1 1)">${closedEye(-22, -478, 10)}</g><path d="M-6 -514 L6 -514" stroke="#D8432F" stroke-width="5"/>
      <path d="M-58 -530 L58 -530 L44 -600 L22 -584 L0 -620 L-22 -584 L-44 -600Z" fill="url(#goldG)"/></g>`;
  s += `<g opacity=".92">${face(-92, 0.62, -1)}${face(92, 0.62, 1)}</g>` + face(0, 1, 0);
  return G2(o.x || 0, o.y || 0, o.s || 1, s);
}
function gada(x, y, s) { return G2(x, y, s, `<rect x="-8" y="0" width="16" height="200" rx="8" fill="url(#goldG)"/><circle cx="0" cy="-10" r="40" fill="url(#goldG)"/><circle cx="-12" cy="-22" r="10" fill="#FFF0B8"/>`); }
function vishnu4(o = {}) {   // chaturbhuj form: extra upper arms with shankh & chakra, tall kirit
  const t = o.t || 0;
  const shankh = `<g transform="rotate(-150)"><path d="M-22 -10 C-30 20 10 40 26 20 C40 0 20 -30 -22 -10Z" fill="#FFF8EE"/><path d="M-10 0 C0 10 14 8 18 0" stroke="#D9C8A8" stroke-width="4" fill="none"/></g>`;
  const chakra = `<g transform="rotate(150)"><circle r="30" fill="none" stroke="url(#goldG)" stroke-width="10"/><g transform="rotate(${(t * 240) % 360})">${[0, 45, 90, 135].map((a) => `<path d="M-30 0 L30 0" stroke="#F5C04A" stroke-width="4" transform="rotate(${a})"/>`).join('')}</g><circle r="8" fill="#F5C04A"/></g>`;
  let s = limb(-70, -380, 150, 20, 92, 82, 32, 26, 'url(#kBlue)', handShape('#4E7EE6'), { bangle: true, held: shankh }) +
          limb(70, -380, -150, -20, 92, 82, 32, 26, 'url(#kBlue)', handShape('#4E7EE6'), { bangle: true, held: chakra });
  s += krishna2({ ...o, x: 0, y: 0, s: 1, noFeather: true, armL: 20, armR: -30, elbowR: -40, glow: o.glow ?? 0.8, eyes: 'closed' });
  s += `<path d="M-60 -600 L60 -600 L36 -740 L0 -780 L-36 -740Z" fill="url(#goldG)"/><circle cx="0" cy="-650" r="12" fill="#D8432F"/>`;
  return G2(o.x || 0, o.y || 0, o.s || 1, s);
}
function calf(o = {}) { return cow2({ ...o, s: (o.s || 1) * 0.62, patch: o.patch, crown: false }).replace(/<path d="M-216 -286[^]*?fill="#F5C04A"\/>/, ''); }
function cave(x, y, s, glow = 0) {
  return G2(x, y, s, `<path d="M-360 0 C-340 -280 -200 -420 0 -430 C200 -420 340 -280 360 0Z" fill="#6E5A4A"/><path d="M-320 0 C-300 -240 -180 -360 0 -370 C180 -360 300 -240 320 0Z" fill="#584638"/>
    <path d="M-170 0 C-170 -170 -90 -250 0 -250 C90 -250 170 -170 170 0Z" fill="#160E0A"/>${glow ? `<ellipse cx="0" cy="-80" rx="120" ry="90" fill="url(#halo)" opacity="${glow}"/>` : ''}
    <path d="M-250 -160 l30 -40 l20 30 M180 -220 l30 -30 l16 30" stroke="#7E6A58" stroke-width="10" fill="none"/>`);
}

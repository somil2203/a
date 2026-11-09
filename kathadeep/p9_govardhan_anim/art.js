// Katha Deep — flat vector storybook character & prop library (original artwork, drawn in code).
// Every function returns an SVG string. Characters are drawn with feet at (0,0), facing the viewer.
const C = {
  blue: '#4F7FE0', blueD: '#3A62C2', blueL: '#7FA5F0',
  gold: '#F5C04A', goldD: '#C98A1E', goldL: '#FFE29A',
  yellow: '#F6C431', orange: '#EE8A2B', red: '#D8432F', redD: '#9E2A22', maroon: '#6E1F2A',
  cream: '#FFF3DC', white: '#FFFFFF', ink: '#2A1B3D', navy: '#1C2347',
  skin: '#E6A57C', skinD: '#C9825C', skinG: '#F2BC7A', green: '#3E8E5A', greenD: '#2A6B44', greenL: '#6DB772',
};
const f2 = (n) => Math.round(n * 100) / 100;
const rot = (a, x = 0, y = 0) => `rotate(${f2(a)} ${f2(x)} ${f2(y)})`;
const G = (x, y, s, inner, extra = '') => `<g transform="translate(${f2(x)} ${f2(y)}) scale(${f2(s)})" ${extra}>${inner}</g>`;

function eyes(x, y, gap, mode, col = C.ink, blink = 0) {
  if (mode === 'open' && blink < 0.5) {
    return `<ellipse cx="${x - gap}" cy="${y}" rx="7" ry="9" fill="${col}"/><ellipse cx="${x + gap}" cy="${y}" rx="7" ry="9" fill="${col}"/>
            <circle cx="${x - gap + 2}" cy="${y - 3}" r="2.4" fill="#fff"/><circle cx="${x + gap + 2}" cy="${y - 3}" r="2.4" fill="#fff"/>`;
  }
  if (mode === 'angry') {
    return `<path d="M${x - gap - 14} ${y - 16} L${x - gap + 12} ${y - 6}" stroke="${col}" stroke-width="6" stroke-linecap="round"/>
            <path d="M${x + gap + 14} ${y - 16} L${x + gap - 12} ${y - 6}" stroke="${col}" stroke-width="6" stroke-linecap="round"/>
            <ellipse cx="${x - gap}" cy="${y + 4}" rx="7" ry="6" fill="${col}"/><ellipse cx="${x + gap}" cy="${y + 4}" rx="7" ry="6" fill="${col}"/>`;
  }
  // closed, content (smiling arcs)
  return `<path d="M${x - gap - 11} ${y} q11 9 22 0" stroke="${col}" stroke-width="5" fill="none" stroke-linecap="round"/>
          <path d="M${x + gap - 11} ${y} q11 9 22 0" stroke="${col}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
}

function arm(sx, sy, ang, len, w, col, hand, extra = '') {
  return `<g transform="${rot(ang, sx, sy)}"><rect x="${sx - w / 2}" y="${sy}" width="${w}" height="${len}" rx="${w / 2}" fill="${col}"/>
          <circle cx="${sx}" cy="${sy + len}" r="${w * 0.62}" fill="${hand}"/><g transform="translate(${sx} ${sy + len})">${extra}</g></g>`;
}

function peacockFeather(x, y, a, s = 1) {
  return `<g transform="translate(${x} ${y}) rotate(${a}) scale(${s})">
    <path d="M0 0 C 4 -40, 6 -80, 4 -118" stroke="#6B4A1E" stroke-width="3" fill="none"/>
    <path d="M4 -70 q-22 -30 -6 -70 q26 30 6 70z" fill="#2F9E6E" opacity=".9"/>
    <ellipse cx="4" cy="-122" rx="22" ry="30" fill="#2C9C5E"/>
    <ellipse cx="4" cy="-120" rx="15" ry="21" fill="#E6B635"/>
    <ellipse cx="4" cy="-118" rx="10" ry="14" fill="#1C5FB8"/>
    <ellipse cx="4" cy="-116" rx="5" ry="7" fill="#0E1E4A"/></g>`;
}

// Child Krishna. opts: armL/armR angles (deg, 0 = hanging down, 180 = straight up), eyes, mouth, flute, glow
function krishna(o = {}) {
  const aL = o.armL ?? 18, aR = o.armR ?? -18, ey = o.eyes || 'closed', mouth = o.mouth || 'smile';
  const tilt = o.tilt || 0;
  let s = '';
  if (o.glow) s += `<circle cx="0" cy="-300" r="300" fill="url(#halo)" opacity="${o.glow}"/>`;
  // legs
  s += `<rect x="-40" y="-150" width="30" height="150" rx="14" fill="${C.blueD}"/><rect x="10" y="-150" width="30" height="150" rx="14" fill="${C.blueD}"/>
        <ellipse cx="-27" cy="-4" rx="24" ry="10" fill="${C.blueD}"/><ellipse cx="27" cy="-4" rx="24" ry="10" fill="${C.blueD}"/>
        <rect x="-38" y="-40" width="26" height="9" rx="4" fill="${C.gold}"/><rect x="12" y="-40" width="26" height="9" rx="4" fill="${C.gold}"/>`;
  // dhoti
  s += `<path d="M-66 -250 L66 -250 L76 -118 Q0 -98 -76 -118 Z" fill="${C.yellow}"/>
        <path d="M-8 -250 L8 -250 L14 -112 L-14 -112 Z" fill="#E9A91E"/>
        <path d="M-70 -250 Q0 -232 70 -250 L70 -228 Q0 -212 -70 -228Z" fill="${C.red}"/>`;
  // torso
  s += `<rect x="-60" y="-350" width="120" height="112" rx="40" fill="${C.blue}"/>`;
  // garland (vaijayanti) + necklace
  s += `<path d="M-46 -338 Q0 -200 46 -338" stroke="#2E9E5B" stroke-width="12" fill="none"/>`;
  for (let i = 0; i <= 8; i++) {
    const t = i / 8, x = -46 + 92 * t, y = -338 + 4 * 138 * t * (1 - t) * 0.5 * 2;
    s += `<circle cx="${f2(x)}" cy="${f2(y)}" r="7" fill="${i % 2 ? C.red : '#F2F2F2'}"/>`;
  }
  s += `<path d="M-34 -342 Q0 -300 34 -342" stroke="${C.gold}" stroke-width="8" fill="none"/>`;
  // arms (drawn per side; hand at the end)
  const flute = o.flute ? `<rect x="-20" y="-6" width="150" height="12" rx="6" fill="#8C3B2E"/><circle cx="30" cy="0" r="3" fill="${C.gold}"/><circle cx="70" cy="0" r="3" fill="${C.gold}"/>` : '';
  const finger = `<rect x="-7" y="4" width="14" height="40" rx="7" fill="${C.blue}"/>`;
  s += arm(-60, -340, aL, 112, 32, C.blue, C.blue, o.fingerL ? finger : '');
  s += arm(60, -340, aR, 112, 32, C.blue, C.blue, flute);
  // bracelets
  // head
  s += `<g transform="${rot(tilt, 0, -380)}">`;
  s += `<rect x="-14" y="-380" width="28" height="30" fill="${C.blueD}"/>`;
  s += `<circle cx="0" cy="-440" r="80" fill="${C.blue}"/>`;
  // hair
  s += `<path d="M-82 -446 Q-80 -530 0 -530 Q80 -530 82 -446 Q60 -488 0 -486 Q-60 -488 -82 -446Z" fill="${C.ink}"/>
        <circle cx="-80" cy="-430" r="16" fill="${C.ink}"/><circle cx="80" cy="-430" r="16" fill="${C.ink}"/>`;
  // ears + earrings
  s += `<circle cx="-80" cy="-440" r="14" fill="${C.blue}"/><circle cx="80" cy="-440" r="14" fill="${C.blue}"/>
        <circle cx="-82" cy="-414" r="9" fill="${C.gold}"/><circle cx="82" cy="-414" r="9" fill="${C.gold}"/>`;
  // crown band + feather
  s += `<path d="M-70 -500 L70 -500 L62 -536 L36 -522 L18 -552 L0 -526 L-18 -552 L-36 -522 L-62 -536Z" fill="${C.gold}"/>
        <rect x="-72" y="-506" width="144" height="16" rx="6" fill="${C.goldD}"/>
        <circle cx="0" cy="-498" r="7" fill="${C.red}"/><circle cx="-36" cy="-498" r="5" fill="#2E9E5B"/><circle cx="36" cy="-498" r="5" fill="#2E9E5B"/>`;
  s += peacockFeather(26, -540, 18, 0.9);
  // tilak
  s += `<path d="M-9 -488 L-6 -462 M9 -488 L6 -462" stroke="#FFF6E0" stroke-width="5" stroke-linecap="round"/><path d="M0 -486 L0 -466" stroke="${C.red}" stroke-width="5" stroke-linecap="round"/>`;
  s += eyes(0, -440, 30, ey, C.ink, o.blink || 0);
  s += `<circle cx="-46" cy="-410" r="11" fill="#E77A9A" opacity=".45"/><circle cx="46" cy="-410" r="11" fill="#E77A9A" opacity=".45"/>`;
  s += mouth === 'open' ? `<ellipse cx="0" cy="-402" rx="12" ry="9" fill="#7A2236"/>` : `<path d="M-14 -406 q14 12 28 0" stroke="#7A2236" stroke-width="5" fill="none" stroke-linecap="round"/>`;
  s += `</g>`;
  return G(o.x || 0, o.y || 0, o.s || 1, s, o.flip ? '' : '');
}

function nand(o = {}) {
  let s = '';
  const aR = o.armR ?? -14, aL = o.armL ?? 14;
  s += `<rect x="-46" y="-130" width="34" height="130" rx="14" fill="${C.skinD}"/><rect x="12" y="-130" width="34" height="130" rx="14" fill="${C.skinD}"/>`;
  s += `<path d="M-80 -360 L80 -360 L96 -110 L-96 -110Z" fill="${C.cream}"/><path d="M-96 -130 L96 -130 L96 -110 L-96 -110Z" fill="${C.orange}"/>`;
  s += `<path d="M-78 -460 L78 -460 L84 -340 L-84 -340Z" fill="${C.cream}"/>`;
  s += `<path d="M-60 -460 L60 -300" stroke="${C.orange}" stroke-width="22"/>`;
  s += arm(-78, -450, aL, 150, 38, C.cream, C.skin);
  s += arm(78, -450, aR, 150, 38, C.cream, C.skin, o.staff ? `<rect x="-8" y="-260" width="16" height="420" rx="8" fill="#7A4A22"/>` : '');
  s += `<rect x="-18" y="-492" width="36" height="40" fill="${C.skinD}"/>`;
  s += `<circle cx="0" cy="-550" r="74" fill="${C.skin}"/>`;
  s += `<path d="M-70 -540 Q-74 -440 0 -420 Q74 -440 70 -540 Q50 -500 0 -506 Q-50 -500 -70 -540Z" fill="#F4F1EA"/>`; // beard
  s += `<path d="M-40 -515 Q-20 -500 0 -512 Q20 -500 40 -515 Q20 -490 0 -500 Q-20 -490 -40 -515Z" fill="#E4E0D6"/>`;
  s += `<path d="M-80 -580 Q-84 -660 0 -664 Q84 -660 80 -580 Q40 -600 0 -598 Q-40 -600 -80 -580Z" fill="${C.orange}"/>
        <path d="M-78 -596 Q0 -620 78 -596" stroke="#C9631A" stroke-width="8" fill="none"/><circle cx="0" cy="-640" r="10" fill="${C.gold}"/>`;
  s += eyes(0, -560, 28, o.eyes || 'closed', C.ink);
  s += `<path d="M-10 -588 L10 -588" stroke="${C.red}" stroke-width="6" stroke-linecap="round"/>`;
  return G(o.x || 0, o.y || 0, o.s || 1, s);
}

function indra(o = {}) {
  let s = '';
  const mood = o.mood || 'calm';
  const skin = mood === 'angry' ? '#E98A5E' : C.skinG;
  if (o.aura) s += `<circle cx="0" cy="-420" r="330" fill="url(#${mood === 'angry' ? 'rage' : 'halo'})" opacity="${o.aura}"/>`;
  s += `<path d="M-90 -380 L90 -380 L120 0 L-120 0Z" fill="${C.redD}"/><path d="M-120 -20 L120 -20 L122 0 L-122 0Z" fill="${C.gold}"/>`;
  s += `<path d="M-10 -380 L10 -380 L18 0 L-18 0Z" fill="${C.gold}"/>`;
  s += `<path d="M-84 -500 L84 -500 L92 -360 L-92 -360Z" fill="${skin}"/>`;
  s += `<path d="M-84 -500 L84 -360" stroke="${C.gold}" stroke-width="14"/>`;
  s += `<path d="M-56 -496 Q0 -430 56 -496" stroke="${C.gold}" stroke-width="12" fill="none"/>`;
  if (o.folded) {
    s += arm(-84, -490, 32, 120, 40, skin, skin) + arm(84, -490, -32, 120, 40, skin, skin);
    s += `<path d="M-20 -400 L0 -470 L20 -400Z" fill="${skin}" stroke="${C.goldD}" stroke-width="3"/>`;
  } else {
    const vj = `<g><rect x="-8" y="-60" width="16" height="120" rx="6" fill="${C.gold}"/><path d="M-26 -60 L0 -110 L26 -60Z" fill="${C.goldL}"/><path d="M-26 60 L0 110 L26 60Z" fill="${C.goldL}"/><circle r="16" fill="${C.goldD}"/></g>`;
    s += arm(-84, -490, o.armL ?? 20, 150, 40, skin, skin) + arm(84, -490, o.armR ?? -120, 150, 40, skin, skin, vj);
  }
  s += `<rect x="-20" y="-540" width="40" height="44" fill="${skin}"/>`;
  s += `<circle cx="0" cy="-600" r="78" fill="${skin}"/>`;
  s += `<circle cx="-80" cy="-590" r="13" fill="${skin}"/><circle cx="80" cy="-590" r="13" fill="${skin}"/><circle cx="-82" cy="-566" r="10" fill="${C.gold}"/><circle cx="82" cy="-566" r="10" fill="${C.gold}"/>`;
  // tall kirit mukut
  const cr = o.cracked ? `<path d="M-10 -840 L8 -790 L-12 -760 L10 -700" stroke="#3A2210" stroke-width="5" fill="none"/>` : '';
  s += `<g transform="${rot(o.crownTilt || 0, 0, -660)}"><path d="M-74 -650 L74 -650 L40 -830 L0 -880 L-40 -830Z" fill="${C.gold}"/>
        <path d="M-74 -650 L74 -650 L70 -680 L-70 -680Z" fill="${C.goldD}"/><circle cx="0" cy="-730" r="16" fill="${C.red}"/>
        <path d="M-50 -760 L50 -760" stroke="${C.goldD}" stroke-width="7"/><circle cx="0" cy="-885" r="10" fill="${C.goldL}"/>${cr}</g>`;
  s += `<path d="M-60 -660 Q-80 -600 -64 -560 M60 -660 Q80 -600 64 -560" stroke="${C.ink}" stroke-width="16" fill="none" stroke-linecap="round"/>`;
  s += eyes(0, -600, 30, mood === 'angry' ? 'angry' : (o.eyes || 'closed'), C.ink);
  s += `<path d="M-6 -650 Q0 -636 6 -650" stroke="${C.red}" stroke-width="5" fill="none"/>`;
  s += mood === 'angry' ? `<path d="M-18 -556 q18 -12 36 0" stroke="#5C1A1A" stroke-width="6" fill="none" stroke-linecap="round"/>`
                        : `<path d="M-14 -562 q14 10 28 0" stroke="#7A2236" stroke-width="5" fill="none" stroke-linecap="round"/>`;
  s += `<path d="M-22 -572 Q0 -584 22 -572" stroke="${C.ink}" stroke-width="5" fill="none"/>`;
  return G(o.x || 0, o.y || 0, o.s || 1, s);
}

function elephant(o = {}) {   // Airavata, side view facing left, feet at 0
  let s = '';
  s += `<rect x="-180" y="-220" width="60" height="220" rx="24" fill="#E9E6EE"/><rect x="100" y="-220" width="60" height="220" rx="24" fill="#E9E6EE"/>
        <rect x="-110" y="-210" width="56" height="210" rx="24" fill="#D9D5E0"/><rect x="40" y="-210" width="56" height="210" rx="24" fill="#D9D5E0"/>`;
  s += `<ellipse cx="0" cy="-300" rx="230" ry="150" fill="#F2F0F5"/>`;
  s += `<path d="M-150 -420 Q0 -470 150 -420 L170 -260 Q0 -220 -170 -260Z" fill="${C.red}"/><path d="M-170 -262 Q0 -222 170 -262 L172 -240 Q0 -200 -172 -240Z" fill="${C.gold}"/>`;
  s += `<circle cx="-250" cy="-360" r="110" fill="#F2F0F5"/>`;
  s += `<path d="M-330 -330 Q-380 -200 -330 -100 Q-320 -70 -300 -90 Q-340 -200 -290 -310Z" fill="#F2F0F5"/>`;
  s += `<path d="M-300 -300 Q-360 -280 -380 -230" stroke="#FFFDF3" stroke-width="14" fill="none" stroke-linecap="round"/>`;
  s += `<ellipse cx="-180" cy="-360" rx="80" ry="100" fill="#E4E0EA"/>`;
  s += `<path d="M-300 -470 L-200 -470 L-220 -430 L-280 -430Z" fill="${C.gold}"/>`;
  s += `<path d="M-290 -380 q14 10 26 0" stroke="${C.ink}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
  return G(o.x || 0, o.y || 0, o.s || 1, s, '');
}

function cow(o = {}) {   // side view facing left (flip:true faces right); walk phase o.ph
  const ph = o.ph || 0, body = o.body || '#F7F1E6', patch = o.patch || '#B9784C';
  const lg = (i) => Math.sin(ph + i * Math.PI) * 12;
  let s = '';
  if (o.halo) s += `<circle cx="-40" cy="-170" r="220" fill="url(#halo)" opacity="${o.halo}"/>`;
  s += `<g transform="${rot(lg(0), -70, -100)}"><rect x="-82" y="-110" width="24" height="110" rx="10" fill="${body}"/><rect x="-82" y="-14" width="24" height="14" rx="4" fill="#5A3B2A"/></g>
        <g transform="${rot(lg(1), 70, -100)}"><rect x="58" y="-110" width="24" height="110" rx="10" fill="${body}"/><rect x="58" y="-14" width="24" height="14" rx="4" fill="#5A3B2A"/></g>
        <g transform="${rot(lg(1), -40, -100)}"><rect x="-50" y="-110" width="22" height="104" rx="10" fill="#E5DCCB"/></g>
        <g transform="${rot(lg(0), 100, -100)}"><rect x="90" y="-110" width="22" height="104" rx="10" fill="#E5DCCB"/></g>`;
  s += `<path d="M120 -170 Q160 -150 150 -90" stroke="${body}" stroke-width="8" fill="none"/><circle cx="150" cy="-86" r="10" fill="${patch}"/>`;
  s += `<rect x="-110" y="-210" width="240" height="120" rx="58" fill="${body}"/>`;
  s += `<path d="M10 -208 Q60 -220 90 -190 Q70 -150 20 -160Z" fill="${patch}"/><circle cx="-50" cy="-120" r="20" fill="${patch}" opacity=".8"/>`;
  s += `<path d="M-120 -200 Q-150 -260 -170 -230 L-150 -160Z" fill="${body}"/>`;
  s += `<rect x="-200" y="-260" width="80" height="110" rx="36" fill="${body}"/>`;
  s += `<rect x="-206" y="-190" width="66" height="44" rx="20" fill="#F2C2B0"/><circle cx="-190" cy="-170" r="4" fill="#7A4A3A"/><circle cx="-168" cy="-170" r="4" fill="#7A4A3A"/>`;
  s += `<path d="M-188 -256 Q-214 -300 -196 -310 M-132 -256 Q-110 -300 -128 -310" stroke="#D9C3A0" stroke-width="10" fill="none" stroke-linecap="round"/>`;
  s += `<ellipse cx="-114" cy="-238" rx="24" ry="12" fill="${body}" transform="rotate(25 -114 -238)"/>`;
  s += `<path d="M-182 -226 q8 6 16 0" stroke="${C.ink}" stroke-width="4" fill="none" stroke-linecap="round"/>`;
  s += `<path d="M-150 -150 Q-130 -126 -110 -150" stroke="${C.red}" stroke-width="8" fill="none"/><path d="M-138 -138 l-10 26 h26z" fill="${C.gold}"/>`;
  if (o.crown) s += `<path d="M-196 -262 L-124 -262 L-130 -296 L-148 -282 L-160 -306 L-172 -282 L-190 -296Z" fill="${C.gold}"/>`;
  if (o.cloth) s += `<path d="M-60 -212 L80 -212 L70 -140 Q10 -128 -50 -140Z" fill="${C.red}"/><path d="M-50 -142 Q10 -130 70 -142 L68 -128 Q10 -116 -48 -128Z" fill="${C.gold}"/>`;
  if (o.flip) s = `<g transform="scale(-1 1)">${s}</g>`;
  return G(o.x || 0, o.y || 0, o.s || 1, s);
}

function person(o = {}) {  // cowherd (gwala) or gopi; feet at 0
  const skin = o.skin || C.skin, cloth = o.cloth || '#E9E3D3', top = o.top || C.orange;
  let s = '';
  if (o.gopi) {
    s += `<path d="M-90 0 Q-80 -220 0 -250 Q80 -220 90 0Z" fill="${cloth}"/><path d="M-90 0 Q0 -24 90 0 L90 -16 Q0 -40 -90 -16Z" fill="${C.gold}"/>`;
    s += `<rect x="-50" y="-330" width="100" height="100" rx="34" fill="${top}"/>`;
    s += arm(-50, -320, o.armL ?? 24, 100, 26, top, skin) + arm(50, -320, o.armR ?? -24, 100, 26, top, skin, o.pot ? `<ellipse cx="0" cy="30" rx="40" ry="32" fill="#C46A35"/><rect x="-20" y="-6" width="40" height="16" rx="6" fill="#A2522A"/>` : '');
    s += `<circle cx="0" cy="-385" r="56" fill="${skin}"/>`;
    s += `<path d="M-66 -380 Q-70 -460 0 -462 Q70 -460 66 -380 Q74 -260 86 -230 L60 -300 Q56 -420 0 -430 Q-56 -420 -60 -300 L-86 -230 Q-74 -260 -66 -380Z" fill="${o.veil || C.red}"/>`;
    s += `<path d="M-60 -420 Q0 -440 60 -420" stroke="${C.gold}" stroke-width="6" fill="none"/>`;
    s += eyes(0, -385, 20, o.eyes || 'closed', C.ink) + `<circle cx="0" cy="-412" r="5" fill="${C.red}"/><path d="M-9 -362 q9 7 18 0" stroke="#7A2236" stroke-width="4" fill="none" stroke-linecap="round"/>`;
  } else {
    s += `<rect x="-34" y="-120" width="26" height="120" rx="12" fill="${skin}"/><rect x="8" y="-120" width="26" height="120" rx="12" fill="${skin}"/>`;
    s += `<path d="M-52 -230 L52 -230 L60 -100 Q0 -88 -60 -100Z" fill="${cloth}"/>`;
    s += `<rect x="-50" y="-320" width="100" height="100" rx="34" fill="${skin}"/><path d="M-50 -310 L40 -230" stroke="${top}" stroke-width="16"/>`;
    s += arm(-50, -312, o.armL ?? 20, 100, 26, skin, skin) + arm(50, -312, o.armR ?? -20, 100, 26, skin, skin, o.stick ? `<rect x="-6" y="-150" width="12" height="300" rx="6" fill="#7A4A22"/>` : '');
    s += `<circle cx="0" cy="-375" r="54" fill="${skin}"/>`;
    s += `<path d="M-56 -384 Q-56 -436 0 -436 Q56 -436 56 -384 Q30 -404 0 -404 Q-30 -404 -56 -384Z" fill="${C.ink}"/>`;
    s += `<path d="M-58 -404 Q0 -428 58 -404 L58 -386 Q0 -410 -58 -386Z" fill="${top}"/>`;
    s += eyes(0, -375, 20, o.eyes || 'closed', C.ink) + `<path d="M-9 -352 q9 7 18 0" stroke="#7A2236" stroke-width="4" fill="none" stroke-linecap="round"/>`;
  }
  return G(o.x || 0, o.y || 0, o.s || 1, s);
}

function tree(x, y, s = 1, col = C.green, colD = C.greenD, sway = 0) {
  return G(x, y, s, `<rect x="-12" y="-160" width="24" height="160" rx="8" fill="#6B4A2E"/>
    <g transform="${rot(sway, 0, -150)}"><circle cx="0" cy="-230" r="90" fill="${colD}"/><circle cx="-50" cy="-200" r="64" fill="${col}"/><circle cx="46" cy="-210" r="70" fill="${col}"/><circle cx="0" cy="-262" r="62" fill="${col}"/>
    <circle cx="-26" cy="-276" r="18" fill="#8FD08A" opacity=".5"/></g>`);
}

function hut(x, y, s = 1, wall = '#D49563') {
  return G(x, y, s, `<rect x="-110" y="-150" width="220" height="150" rx="10" fill="${wall}"/><rect x="-30" y="-100" width="60" height="100" rx="26" fill="#5A3322"/>
    <path d="M-150 -140 L0 -280 L150 -140Z" fill="#9A6A34"/><path d="M-150 -140 L150 -140 L140 -126 L-140 -126Z" fill="#7A4E22"/>
    <path d="M-100 -170 L-40 -230 M-40 -160 L20 -230 M30 -160 L70 -200" stroke="#7A4E22" stroke-width="5"/>
    <circle cx="-70" cy="-60" r="10" fill="#F2E3C8"/><circle cx="70" cy="-60" r="10" fill="#F2E3C8"/>`);
}

// Govardhan: base at (0,0), width w. lifted: show rocky underside.
function mountain(o = {}) {
  const w = o.w || 900, h = o.h || 520, under = o.lifted;
  let s = '';
  const L = -w / 2, R = w / 2;
  if (under) s += `<path d="M${L + 20} -10 Q${L + 120} 70 ${L + 260} 40 Q${-40} 110 ${120} 50 Q${R - 160} 90 ${R - 20} -10Z" fill="#7A5236"/>
                   <path d="M${L + 80} 20 l40 50 l20 -40 M${-20} 50 l30 60 l30 -50 M${R - 200} 30 l26 46 l22 -40" fill="#5E3E28"/>`;
  s += `<path d="M${L} 0 Q${L + 60} ${-h * 0.55} ${L + w * 0.22} ${-h * 0.7} Q${L + w * 0.34} ${-h * 1.02} ${-w * 0.02} ${-h} Q${w * 0.18} ${-h * 1.05} ${R - w * 0.24} ${-h * 0.72} Q${R - 40} ${-h * 0.5} ${R} 0Z" fill="${o.back || '#3F7F4E'}"/>`;
  s += `<path d="M${L + 40} 0 Q${L + w * 0.2} ${-h * 0.62} ${-w * 0.08} ${-h * 0.66} Q${w * 0.2} ${-h * 0.7} ${R - 60} 0Z" fill="${o.front || '#5BA463'}"/>`;
  s += `<path d="M${-w * 0.2} ${-h * 0.8} Q${0} ${-h * 0.98} ${w * 0.12} ${-h * 0.86}" stroke="#7CC27C" stroke-width="16" fill="none" stroke-linecap="round" opacity=".7"/>`;
  const trees = [[-0.36, -0.42, 0.42], [-0.18, -0.74, 0.46], [0.04, -0.86, 0.5], [0.22, -0.6, 0.44], [0.34, -0.36, 0.4], [-0.06, -0.4, 0.38], [0.14, -0.28, 0.36], [-0.26, -0.18, 0.34]];
  for (const [tx, ty, ts] of trees) s += tree(tx * w, ty * h + 40, ts, '#2F8A55', '#226B40', o.sway ? Math.sin((o.sway + tx) * 3) * 4 : 0);
  s += `<ellipse cx="${-w * 0.3}" cy="-30" rx="60" ry="26" fill="#8C8C8C"/><ellipse cx="${w * 0.28}" cy="-26" rx="44" ry="20" fill="#9A9A9A"/>`;
  if (o.diyas) for (let i = 0; i < 7; i++) s += diya(L + w * 0.12 + i * w * 0.126, -6, 0.5, o.t || 0, i);
  if (o.garland) s += `<path d="M${L + w * 0.18} ${-h * 0.5} Q0 ${-h * 0.18} ${R - w * 0.18} ${-h * 0.5}" stroke="${C.orange}" stroke-width="16" stroke-dasharray="2 18" stroke-linecap="round" fill="none"/>`;
  return G(o.x || 0, o.y || 0, o.s || 1, s);
}

function cloud(x, y, s = 1, col = '#FFFFFF', shade = '#E8E4F2') {
  return G(x, y, s, `<ellipse cx="0" cy="10" rx="170" ry="60" fill="${shade}"/><circle cx="-90" cy="-10" r="70" fill="${col}"/><circle cx="0" cy="-40" r="95" fill="${col}"/><circle cx="90" cy="-10" r="72" fill="${col}"/><rect x="-160" y="-10" width="320" height="60" rx="30" fill="${col}"/>`);
}

function flame(x, y, s, t, k = 0) {
  const w = Math.sin(t * 13 + k * 1.7) * 0.08 + Math.sin(t * 7.3 + k) * 0.05;
  return G(x, y, s, `<g transform="scale(${f2(1 + w)} ${f2(1 - w * 0.6)})"><path d="M0 0 C -26 -10 -24 -50 0 -96 C 24 -50 26 -10 0 0Z" fill="${C.orange}"/>
    <path d="M0 -4 C -14 -10 -14 -36 0 -64 C 14 -36 14 -10 0 -4Z" fill="${C.goldL}"/></g>`);
}

function diya(x, y, s, t, k = 0, lit = true, glow = 1) {
  let g = '';
  if (lit) g += `<circle cx="0" cy="-60" r="110" fill="url(#halo)" opacity="${f2(0.75 * glow)}"/>` + flame(0, -30, 0.6, t, k).replace(/^<g/, '<g');
  return G(x, y, s, `${g}<path d="M-70 -34 Q0 40 70 -34 Q60 -20 0 -16 Q-60 -20 -70 -34Z" fill="#B5562E"/><path d="M-70 -34 Q0 -48 70 -34 Q0 -22 -70 -34Z" fill="#7E3418"/>
    <path d="M-48 -6 Q0 18 48 -6" stroke="${C.gold}" stroke-width="4" fill="none" opacity=".8"/>`);
}

function kund(x, y, s, t, big = 1) {  // yajna fire altar
  let f = '';
  for (let i = -2; i <= 2; i++) f += flame(i * 34, -70, (1.5 - Math.abs(i) * 0.25) * big, t, i);
  return G(x, y, s, `<circle cx="0" cy="-160" r="240" fill="url(#halo)" opacity=".8"/>${f}
    <path d="M-160 -80 L160 -80 L130 0 L-130 0Z" fill="#B0603A"/><path d="M-170 -96 L170 -96 L160 -76 L-160 -76Z" fill="#8E4426"/>
    <path d="M-120 -56 L120 -56 M-100 -30 L100 -30" stroke="#8E4426" stroke-width="5"/><path d="M-60 -78 L-60 -56 M0 -78 L0 -56 M60 -78 L60 -56 M-30 -56 L-30 -30 M30 -56 L30 -30" stroke="#8E4426" stroke-width="5"/>`);
}

function mushroom(x, y, s) {
  return G(x, y, s, `<rect x="-22" y="-110" width="44" height="110" rx="18" fill="#F4E7CF"/><path d="M-110 -100 Q0 -230 110 -100 Q0 -80 -110 -100Z" fill="${C.red}"/>
    <circle cx="-40" cy="-140" r="14" fill="#fff"/><circle cx="20" cy="-160" r="11" fill="#fff"/><circle cx="56" cy="-122" r="9" fill="#fff"/>`);
}

function bolt(x, y, s, seed = 1) {
  let p = 'M0 0', xx = 0, yy = 0, r = seed;
  const rnd = () => (r = (r * 9301 + 49297) % 233280) / 233280;
  for (let i = 0; i < 9; i++) { yy += 60 + rnd() * 40; xx += (rnd() - 0.5) * 120; p += ` L${f2(xx)} ${f2(yy)}`; }
  return G(x, y, s, `<path d="${p}" stroke="#CFE0FF" stroke-width="22" fill="none" opacity=".45" stroke-linejoin="round"/><path d="${p}" stroke="#FFFFFF" stroke-width="7" fill="none" stroke-linejoin="round"/>`);
}

function annakut(x, y, s, t) {
  let sw = '';
  const cols = ['#F2A93B', '#E8763A', '#F7D488', '#C9582C', '#FFF1D0'];
  let k = 0;
  for (let row = 0; row < 7; row++) {
    const n = 7 - row;
    for (let i = 0; i < n; i++) { const cx = (i - (n - 1) / 2) * 58, cy = -40 - row * 50; sw += `<circle cx="${cx}" cy="${cy}" r="30" fill="${cols[(k++) % 5]}"/><circle cx="${cx - 8}" cy="${cy - 10}" r="7" fill="#fff" opacity=".35"/>`; }
  }
  return G(x, y, s, `<circle cx="0" cy="-220" r="330" fill="url(#halo)" opacity=".7"/><ellipse cx="0" cy="0" rx="300" ry="50" fill="#3E8A4A"/><ellipse cx="0" cy="-6" rx="270" ry="38" fill="#57A85E"/>${sw}
    <path d="M-10 -400 q10 -40 20 0z" fill="${C.green}"/>${diya(-250, 30, 0.6, t, 1)}${diya(250, 30, 0.6, t, 2)}`);
}

function yamraj(x, y, s) {   // silhouette for the teaser (no face)
  return G(x, y, s, `<path d="M-90 0 L-70 -330 Q0 -360 70 -330 L90 0Z" fill="#1B1030"/><circle cx="0" cy="-400" r="64" fill="#1B1030"/>
    <path d="M-56 -440 L56 -440 L30 -560 L0 -590 L-30 -560Z" fill="#1B1030"/><rect x="80" y="-420" width="18" height="420" rx="8" fill="#1B1030"/><circle cx="89" cy="-440" r="40" fill="#1B1030"/>
    <path d="M-56 -440 L56 -440" stroke="${C.gold}" stroke-width="6"/>`);
}
function yamuna(x, y, s) {
  return G(x, y, s, `<path d="M-100 0 Q-80 -240 0 -280 Q80 -240 100 0Z" fill="#1B1030"/><circle cx="0" cy="-330" r="56" fill="#1B1030"/>
    <path d="M-68 -320 Q-74 -410 0 -412 Q74 -410 68 -320 Q80 -220 100 -170 L70 -230 Q62 -370 0 -380 Q-62 -370 -70 -230 L-100 -170Z" fill="#1B1030"/>
    <path d="M-62 -372 Q0 -392 62 -372" stroke="${C.gold}" stroke-width="5" fill="none"/>`);
}

if (typeof module !== 'undefined') module.exports = { C };

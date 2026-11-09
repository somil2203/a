// Food, kitchen and devotional props for the animated storybook reels.
function bowl(inner, rim = '#C98A1E', body = 'url(#goldG)') {
  return `<ellipse cx="0" cy="6" rx="96" ry="18" fill="#00000030"/><path d="M-90 -40 C-86 10 -50 30 0 30 C50 30 86 10 90 -40Z" fill="${body}"/>
    <ellipse cx="0" cy="-40" rx="90" ry="24" fill="${rim}"/>${inner}<path d="M-70 -14 C-50 4 -20 12 10 12" stroke="#FFF0B8" stroke-width="5" fill="none" opacity=".6"/>`;
}
function food(kind, x, y, s = 1, t = 0) {
  let g = '';
  const steam = (n = 3) => Array.from({ length: n }, (_, i) => `<path d="M${-30 + i * 30} -70 c-14 -20 14 -36 0 -56 c-12 -18 10 -30 2 -44" stroke="#FFFFFF" stroke-width="7" fill="none" stroke-linecap="round" opacity="${(0.35 + 0.25 * Math.sin(t * 3 + i)).toFixed(2)}" transform="translate(0 ${(-8 * ((t * 1.5 + i * 0.3) % 1)).toFixed(1)})"/>`).join('');
  switch (kind) {
    case 'kheer': g = steam() + bowl(`<ellipse cx="0" cy="-40" rx="80" ry="19" fill="#FFF6E2"/><path d="M-30 -44 l10 -3 M10 -36 l12 -2 M30 -46 l9 2" stroke="#C98A4A" stroke-width="6" stroke-linecap="round"/><circle cx="-6" cy="-42" r="4" fill="#4FA86A"/><circle cx="22" cy="-44" r="3" fill="#E0B030"/>`); break;
    case 'halwa': g = steam(2) + bowl(`<path d="M-80 -40 C-60 -86 60 -86 80 -40Z" fill="#E8962E"/><path d="M-50 -56 C-30 -76 20 -78 44 -60" stroke="#F7C46A" stroke-width="8" fill="none" stroke-linecap="round"/><circle cx="-14" cy="-70" r="5" fill="#5FAE6E"/><circle cx="16" cy="-66" r="5" fill="#C98A4A"/>`); break;
    case 'dal': g = steam(2) + bowl(`<ellipse cx="0" cy="-40" rx="80" ry="19" fill="#F2B72E"/><circle cx="-20" cy="-42" r="5" fill="#3E8E5A"/><circle cx="16" cy="-38" r="4" fill="#D8432F"/>`); break;
    case 'rice': g = bowl(`<path d="M-82 -40 C-70 -100 70 -100 82 -40Z" fill="#FBF8F0"/>${[-40, -10, 22, 50, -24, 8, 36].map((x, i) => `<ellipse cx="${x}" cy="${-56 - (i % 3) * 10}" rx="6" ry="3" fill="#E8E0CC"/>`).join('')}`); break;
    case 'pua': g = `<ellipse cx="0" cy="8" rx="110" ry="20" fill="#00000030"/><ellipse cx="0" cy="0" rx="120" ry="26" fill="url(#goldG)"/>` + [0, 1, 2].map((i) => `<ellipse cx="${(i - 1) * 8}" cy="${-20 - i * 26}" rx="78" ry="24" fill="${['#A85A22', '#B8662A', '#C77632'][i]}"/><ellipse cx="${(i - 1) * 8}" cy="${-26 - i * 26}" rx="60" ry="14" fill="#D9904A" opacity=".7"/>`).join('') + `<path d="M-30 -90 q30 -14 60 0" stroke="#F7D488" stroke-width="5" fill="none"/>`; break;
    case 'puri': g = `<ellipse cx="0" cy="8" rx="110" ry="20" fill="#00000030"/><ellipse cx="0" cy="0" rx="120" ry="26" fill="url(#goldG)"/>` + [[-44, -36], [44, -36], [0, -60], [-20, -90], [26, -96]].map(([px, py], i) => `<ellipse cx="${px}" cy="${py}" rx="58" ry="40" fill="${i % 2 ? '#E9A53A' : '#F2B84A'}"/><ellipse cx="${px - 10}" cy="${py - 12}" rx="22" ry="10" fill="#FFE2A0" opacity=".7"/>`).join(''); break;
    case 'laddoo': g = `<ellipse cx="0" cy="8" rx="110" ry="20" fill="#00000030"/><ellipse cx="0" cy="0" rx="120" ry="26" fill="url(#goldG)"/>` + [[-50, -36], [0, -36], [50, -36], [-25, -76], [25, -76], [0, -114]].map(([px, py]) => `<circle cx="${px}" cy="${py}" r="30" fill="#F29A26"/><circle cx="${px - 10}" cy="${py - 10}" r="8" fill="#FFC66A"/>${[0, 1, 2, 3].map((k) => `<circle cx="${px - 14 + k * 9}" cy="${py + 6 - (k % 2) * 12}" r="2.5" fill="#C96E10"/>`).join('')}`).join(''); break;
    case 'jalebi': g = `<ellipse cx="0" cy="8" rx="110" ry="20" fill="#00000030"/><ellipse cx="0" cy="0" rx="120" ry="26" fill="url(#goldG)"/>` + [[-40, -40], [40, -40], [0, -78]].map(([px, py]) => `<path d="M${px} ${py} m-6 0 a6 6 0 1 1 12 0 a14 14 0 1 1 -28 0 a22 22 0 1 1 44 0 a30 30 0 1 1 -60 0" stroke="#F28A1A" stroke-width="11" fill="none" stroke-linecap="round"/><path d="M${px} ${py} m-6 0 a6 6 0 1 1 12 0 a14 14 0 1 1 -28 0 a22 22 0 1 1 44 0 a30 30 0 1 1 -60 0" stroke="#FFC060" stroke-width="3" fill="none" opacity=".7"/>`).join(''); break;
    case 'makhan': g = `<ellipse cx="0" cy="8" rx="80" ry="16" fill="#00000030"/><path d="M-70 -50 C-90 0 -50 20 0 20 C50 20 90 0 70 -50Z" fill="#C46A35"/><path d="M-70 -50 Q0 -30 70 -50 L60 -70 Q0 -54 -60 -70Z" fill="#A2522A"/>
        <path d="M-56 -66 C-50 -110 50 -110 56 -66 Q0 -54 -56 -66Z" fill="#FFF8DC"/><path d="M-20 -100 c10 -14 30 -10 34 4" stroke="#FFFFFF" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M-40 -10 Q0 4 40 -10" stroke="#F5C04A" stroke-width="5" fill="none"/>`; break;
    case 'barfi': g = `<ellipse cx="0" cy="8" rx="110" ry="20" fill="#00000030"/><ellipse cx="0" cy="0" rx="120" ry="26" fill="url(#goldG)"/>` + [[-44, -30], [44, -30], [0, -50], [0, -14]].map(([px, py]) => `<path d="M${px} ${py - 26} l36 22 l-36 22 l-36 -22z" fill="#F7EBD0"/><path d="M${px} ${py - 26} l36 22 l-36 22 l-36 -22z" fill="none" stroke="#D9D2C0" stroke-width="3"/><path d="M${px - 14} ${py - 4} l28 0" stroke="#C8CCD4" stroke-width="5"/>`).join(''); break;
    case 'fruit': g = `<ellipse cx="0" cy="8" rx="110" ry="20" fill="#00000030"/><ellipse cx="0" cy="0" rx="120" ry="26" fill="url(#goldG)"/><path d="M-80 -30 C-60 -90 20 -100 40 -60 C0 -70 -40 -60 -70 -20Z" fill="#F5D33A"/><path d="M-70 -30 C-46 -76 10 -86 32 -64" stroke="#D9B21E" stroke-width="4" fill="none"/>
        <ellipse cx="50" cy="-46" rx="40" ry="34" fill="#F29A26"/><ellipse cx="38" cy="-58" rx="12" ry="8" fill="#FFC870"/><path d="M50 -80 q8 -14 22 -10" stroke="#3E8E5A" stroke-width="6" fill="none"/><circle cx="-6" cy="-36" r="24" fill="#D8432F"/><circle cx="-14" cy="-44" r="6" fill="#FF8A7A"/>`; break;
  }
  return G2(x, y, s, g);
}
const FOODS = ['kheer', 'halwa', 'pua', 'puri', 'laddoo', 'jalebi', 'dal', 'rice', 'makhan', 'barfi', 'fruit'];

function thali(x, y, s, n = 8, t = 0) {   // top-down thali with katoris
  let g = `<circle cx="0" cy="10" r="300" fill="#00000035"/><circle r="300" fill="url(#goldG)"/><circle r="270" fill="#F2C766"/><circle r="270" fill="none" stroke="#C98A1E" stroke-width="6" stroke-dasharray="4 14"/>`;
  const cols = ['#FFF6E2', '#E8962E', '#F2B72E', '#FBF8F0', '#B8662A', '#F29A26', '#7FB24A', '#D8432F'];
  for (let i = 0; i < Math.min(n, 8); i++) {
    const a = i / 8 * Math.PI * 2 - Math.PI / 2, cx = Math.cos(a) * 180, cy = Math.sin(a) * 180;
    g += `<circle cx="${P2(cx)}" cy="${P2(cy)}" r="66" fill="#C98A1E"/><circle cx="${P2(cx)}" cy="${P2(cy)}" r="56" fill="${cols[i]}"/><circle cx="${P2(cx - 16)}" cy="${P2(cy - 16)}" r="14" fill="#FFFFFF" opacity=".25"/>`;
  }
  g += `<circle r="70" fill="#F29A26"/>` + [[-26, -10], [24, -12], [0, 22]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="28" fill="#F7A93A"/><circle cx="${a - 8}" cy="${b - 8}" r="7" fill="#FFD08A"/>`).join('');
  g += `<g transform="translate(0 -250)">${diya(0, 0, 0.5, t, 3)}</g>`;
  return G2(x, y, s, g);
}

function chulha(x, y, s, t, k = 0) {
  let fl = ''; for (let i = -1; i <= 1; i++) fl += flame(i * 30, -40, 0.8 - Math.abs(i) * 0.2, t, i + k);
  const steam = [0, 1, 2].map((i) => `<path d="M${-30 + i * 30} -250 c-16 -24 16 -40 0 -64 c-14 -20 12 -34 2 -50" stroke="#FFFFFF" stroke-width="9" fill="none" stroke-linecap="round" opacity="${(0.3 + 0.2 * Math.sin(t * 3 + i + k)).toFixed(2)}"/>`).join('');
  return G2(x, y, s, `<path d="M-130 0 L-110 -90 L110 -90 L130 0Z" fill="#B0603A"/><path d="M-50 0 C-50 -50 50 -50 50 0Z" fill="#3A1A10"/>${fl}
    ${steam}<path d="M-110 -100 C-120 -200 120 -200 110 -100Z" fill="#7A7A80"/><ellipse cx="0" cy="-170" rx="98" ry="22" fill="#5E5E66"/><ellipse cx="0" cy="-172" rx="84" ry="16" fill="#F2B72E"/>
    <path d="M-100 -130 Q0 -110 100 -130" stroke="#9A9AA2" stroke-width="5" fill="none"/>`);
}

function dial8(x, y, r, lit, t) {   // eight pahar
  let g = '';
  for (let i = 0; i < 8; i++) {
    const a0 = (i / 8) * Math.PI * 2 - Math.PI / 2 - Math.PI / 8 + 0.04, a1 = a0 + Math.PI / 4 - 0.08;
    const on = i < lit;
    const p = (a, rr) => `${P2(Math.cos(a) * rr)} ${P2(Math.sin(a) * rr)}`;
    g += `<path d="M${p(a0, r * 0.62)} L${p(a0, r)} A${r} ${r} 0 0 1 ${p(a1, r)} L${p(a1, r * 0.62)} A${r * 0.62} ${r * 0.62} 0 0 0 ${p(a0, r * 0.62)}Z" fill="${on ? '#FFF3C4' : '#7A2E1230'}" stroke="${on ? '#7A2E12' : '#7A2E1260'}" stroke-width="5"/>`;
    const am = (a0 + a1) / 2;
    g += `<text x="${P2(Math.cos(am) * r * 0.81)}" y="${P2(Math.sin(am) * r * 0.81 + 14)}" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="40" fill="${on ? '#7A2E12' : '#7A2E1288'}">${i + 1}</text>`;
  }
  return G2(x, y, 1, g);
}

function yashoda(o = {}) {
  return gopi2({ veil: '#B8325A', top: '#2E8A4E', skirt: '#7A2E8C', ...o });
}

function giantKrishna(x, y, s, k, t) {   // the 'vishaal roop' rising behind Govardhan (Bhagavata 10.24.35)
  return `<g opacity="${clamp(k).toFixed(2)}"><circle cx="${x}" cy="${y - 420 * s}" r="${520 * s}" fill="url(#halo)" opacity=".95"/>
    ${[...Array(16)].map((_, i) => { const a = i * 22.5 + t * 6; return `<path d="M${x} ${y - 420 * s} L${P2(x + Math.cos(a * Math.PI / 180) * 1400)} ${P2(y - 420 * s + Math.sin(a * Math.PI / 180) * 1400)} L${P2(x + Math.cos((a + 6) * Math.PI / 180) * 1400)} ${P2(y - 420 * s + Math.sin((a + 6) * Math.PI / 180) * 1400)}Z" fill="#FFF2C6" opacity=".14"/>`; }).join('')}
    ${krishna2({ x, y, s, glow: 0, eyes: 'closed', armL: 30, armR: -60, elbowR: -70, t })}</g>`;
}

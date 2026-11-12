// Set 7: Upanishad series props — glass of salt water, weave diagram, arrows, water bowl, scholars and kings.
function saltGlass(x, y, s, t, dissolve = 0, dips = []) {   // dips: [[level 0..1, k]] spoon dip points with "khaara" glow
  let g = `<path d="M-160 -520 L160 -520 L130 0 L-130 0Z" fill="#DDEEFF" opacity=".35" stroke="#FFFFFF" stroke-width="6"/>`;
  g += `<path d="M-150 -430 L150 -430 L130 0 L-130 0Z" fill="#8EC8F0" opacity=".55"/>`;
  for (let i = 0; i < 26; i++) { const px = (rnd(i) - 0.5) * 220, fall = Math.min(1, dissolve * 2.2), py = -60 - rnd(i + 3) * 40 + (1 - fall) * -330, a = 1 - clamp(dissolve * 1.6 - 0.6);
    if (a > 0.02) g += `<rect x="${px.toFixed(0)}" y="${py.toFixed(0)}" width="14" height="14" fill="#FFFFFF" opacity="${a.toFixed(2)}" transform="rotate(${(i * 37) % 90} ${px.toFixed(0)} ${py.toFixed(0)})"/>`; }
  if (dissolve > 0.6) g += `<path d="M-150 -430 L150 -430 L130 0 L-130 0Z" fill="#FFFFFF" opacity="${(0.12 * clamp((dissolve - 0.6) * 3)).toFixed(2)}"/>`;
  dips.forEach(([lv, k]) => { if (k <= 0) return; const yy = -430 + lv * 400; g += `<circle cx="0" cy="${yy}" r="${(30 + 60 * k).toFixed(0)}" fill="url(#halo)" opacity="${k.toFixed(2)}"/><circle cx="0" cy="${yy}" r="14" fill="#FFF6DA" opacity="${k.toFixed(2)}"/>`; });
  return G2(x, y, s, g);
}
function weave(x, y, s, t, k = 1, labels = []) {   // concentric 'woven in' rings, innermost first
  let g = '';
  labels.forEach((lb, i) => { const kk = clamp(k * labels.length - i); if (kk <= 0) return; const r = 90 + i * 85;
    g += `<circle r="${r}" fill="none" stroke="#F5C04A" stroke-width="6" stroke-dasharray="${(2 * Math.PI * r * kk).toFixed(0)} 9999" opacity=".85" transform="rotate(${(-90 + t * (i % 2 ? -6 : 6)).toFixed(1)})"/>`;
    for (let j = 0; j < 12; j++) { const a = j * 30 * Math.PI / 180; g += `<path d="M${(Math.cos(a) * (r - 18)).toFixed(0)} ${(Math.sin(a) * (r - 18)).toFixed(0)} L${(Math.cos(a) * (r + 18)).toFixed(0)} ${(Math.sin(a) * (r + 18)).toFixed(0)}" stroke="#F5C04A" stroke-width="2" opacity="${(0.5 * kk).toFixed(2)}"/>`; }
    g += `<text x="0" y="${-r + 12}" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="40" fill="#FFF3DC" opacity="${kk.toFixed(2)}" stroke="#14060A" stroke-width="5" paint-order="stroke">${lb}</text>`; });
  return G2(x, y, s, g);
}
function arrow2(x, y, s, a, k) {
  if (k <= 0) return '';
  return G2(x, y, s, `<g transform="rotate(${a})" opacity="${clamp(k * 2).toFixed(2)}"><rect x="-200" y="-5" width="380" height="10" rx="5" fill="#7A4A22"/><path d="M180 -26 L240 0 L180 26Z" fill="#C0C6CC"/><path d="M-200 0 l-40 -24 l20 24 l-20 24z" fill="#D6332A"/></g>`);
}
function waterBowl(x, y, s, t, reflect = '') {
  return G2(x, y, s, `<ellipse cx="0" cy="10" rx="260" ry="50" fill="#000" opacity=".2"/><path d="M-250 -40 C-240 60 240 60 250 -40Z" fill="url(#goldG)"/><ellipse cx="0" cy="-40" rx="250" ry="60" fill="#C98A1E"/>
    <ellipse cx="0" cy="-40" rx="225" ry="48" fill="#3E86D8"/><clipPath id="bowlc"><ellipse cx="0" cy="-40" rx="225" ry="48"/></clipPath><g clip-path="url(#bowlc)" opacity=".8">${reflect}</g>
    <path d="M-150 -50 q40 -10 80 0" stroke="#BFE3FF" stroke-width="5" fill="none" opacity="${(0.5 + 0.3 * Math.sin(t * 3)).toFixed(2)}"/>`);
}
function gargi(o = {}) { return gopi2({ veil: '#E8762E', top: '#F5C04A', skirt: '#F4F1EA', ...o }).replace(/#E8A983/g, '#D49A74'); }
function janak(o = {}) { return bali(o).replace(/#5A2A7A/g, '#1E4A8A').replace(/#8E1F2A/g, '#2A5A9A'); }
function virochan(o = {}) { return bali(o).replace(/#5A2A7A/g, '#3A1A1A').replace(/#8E1F2A/g, '#6E1F1F').replace(/#D9A27A/g, '#B9806A'); }
function youngScholar(o = {}) { return gwala2({ top: '#F2B233', dhoti: '#F4F1EA', skin: '#D9A07A', ...o }); }
function sabha(t) {   // royal assembly hall
  let w = bg('maroon') + `<rect x="-300" y="1450" width="1700" height="900" fill="#5A1E2A"/>`;
  for (let i = 0; i < 5; i++) w += `<path d="M${-60 + i * 260} 1450 V620 Q${-60 + i * 260 + 110} 500 ${-60 + i * 260 + 220} 620 V1450Z" fill="#7A2E3A" stroke="#C98A1E" stroke-width="6"/>`;
  return w;
}

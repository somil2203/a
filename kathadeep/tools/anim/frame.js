// ------------------------------------------------------------------ transitions + frame
const TR = { fade: 0.5, zoom: 0.4, up: 0.6, flash: 0.35, wipe: 0.9, iris: 0.7, whip: 0.35 };
function frame(t) {
  let i = S.findIndex((s) => t >= s.t0 && t < s.t1); if (i < 0) i = S.length - 1;
  const cur = S[i];
  let out = cur.draw(t);
  // incoming transition (blend the previous scene over the start of this one)
  const d = TR[cur.tin] || 0.5;
  if (i > 0 && t < cur.t0 + d) {
    const k = eio(seg(t, cur.t0, cur.t0 + d)), prev = S[i - 1].draw(t);
    if (cur.tin === 'zoom') out = `<g opacity="${(1 - k).toFixed(3)}" transform="translate(540 960) scale(${(1 + 0.25 * k).toFixed(3)}) translate(-540 -960)">${prev}</g><g opacity="${k.toFixed(3)}" transform="translate(540 960) scale(${(1.15 - 0.15 * k).toFixed(3)}) translate(-540 -960)">${out}</g>`;
    else if (cur.tin === 'up') out = `<g transform="translate(0 ${(1920 * k).toFixed(1)})">${prev}</g><g transform="translate(0 ${(-1920 * (1 - k)).toFixed(1)})">${out}</g>`;
    else if (cur.tin === 'whip') out = `<g transform="translate(${(-1080 * k).toFixed(1)} 0)">${prev}</g><g transform="translate(${(1080 * (1 - k)).toFixed(1)} 0)">${out}</g>`;
    else if (cur.tin === 'iris') out = `${prev}<clipPath id="irisc"><circle cx="540" cy="1150" r="${(1300 * k).toFixed(1)}"/></clipPath><g clip-path="url(#irisc)">${out}</g>`;
    else if (cur.tin === 'wipe') { // storm clouds sweep across
      let cl = ''; for (let j = 0; j < 9; j++) cl += cloud(lerp(-900, 1900, k) + (j % 3) * 260 - 300, 200 + j * 200, 2.6, '#2E3346', '#22273A');
      out = `<g opacity="${(1 - clamp(k * 1.6 - 0.3)).toFixed(3)}">${prev}</g><g opacity="${clamp(k * 1.6 - 0.3).toFixed(3)}">${out}</g>${k < 1 ? cl : ''}`;
    } else if (cur.tin === 'flash') out = `<g opacity="${(1 - k).toFixed(3)}">${prev}</g><g opacity="${k.toFixed(3)}">${out}</g><rect width="1080" height="1920" fill="#FFE2C0" opacity="${(Math.sin(k * Math.PI) * 0.85).toFixed(2)}"/>`;
    else out = `<g opacity="${(1 - k).toFixed(3)}">${prev}</g><g opacity="${k.toFixed(3)}">${out}</g>`;
  }
  return DEFS + out + `<rect width="1080" height="1920" fill="url(#vig)"/>` + hookCard(t);
}

// ------------------------------------------------------------------ HOOK CARD (retention fix 10 Nov 2026)
// Instagram data: ~50% skip in the first seconds when the opening had small, fading-in text. The hook text is now
// on screen at full size from frame 0 (no fade-in), high contrast, inside the safe zone, until HOOK.t1.
function hookCard(t) {
  const H0 = window.HOOK; if (!H0 || t > H0.t1) return '';
  const out = clamp((H0.t1 - t) / 0.25), pulse = 1 + 0.07 * Math.max(0, 1 - t / 0.3) + 0.012 * Math.sin(t * 9);
  const y = H0.y || 520, s1 = H0.size || 118;
  const line = (txt, yy, col, sz) => `<text x="540" y="${yy}" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="${sz}" fill="${col}" stroke="#14060A" stroke-width="${(sz * 0.11).toFixed(1)}" paint-order="stroke" stroke-linejoin="round">${txt}</text>`;
  return `<g opacity="${out.toFixed(2)}"><rect x="0" y="${y - s1 * 1.3}" width="1080" height="${s1 * 2.9}" fill="#0A0410" opacity=".42"/>
    <g transform="translate(540 ${y}) scale(${pulse.toFixed(3)}) translate(-540 ${-y})">${line(H0.l1, y, '#FFFFFF', s1)}${H0.l2 ? line(H0.l2, y + s1 * 1.12, '#FFD24A', s1) : ''}</g></g>`;
}

// ------------------------------------------------------------------ subtitles (Hinglish, word highlight)
const SUBS = window.SUBS;
const CHUNKS = (() => { const ch = []; let cur = []; SUBS.forEach((w, i) => { cur.push(i); const n = cur.map((j) => SUBS[j].w).join(' ').length; if (w.br || n > 30) { ch.push(cur); cur = []; } }); if (cur.length) ch.push(cur); return ch; })();
function subs(t) {
  let chunk = null;
  for (const ch of CHUNKS) { const a = SUBS[ch[0]].a - 0.08, b = SUBS[ch[ch.length - 1]].b + 0.35; if (t >= a && t <= b) chunk = ch; }
  if (!chunk) return '';
  return chunk.map((i) => { const w = SUBS[i]; const on = t >= w.a - 0.02 && t <= w.b + 0.06; const past = t > w.b;
    return `<span class="${on ? 'on' : past ? 'past' : 'fut'}${w.key ? ' key' : ''}">${w.w}</span>`; }).join(' ');
}

window.renderAt = (t) => {
  window.T_NOW = t;
  document.getElementById('v').innerHTML = frame(t);
  document.getElementById('subs').innerHTML = subs(t);
};

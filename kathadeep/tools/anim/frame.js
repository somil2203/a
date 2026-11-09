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
  return DEFS + out + `<rect width="1080" height="1920" fill="url(#vig)"/>`;
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

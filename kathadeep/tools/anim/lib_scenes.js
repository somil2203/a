// reusable scene builders (from Din 4 Govardhan)
function wideLift(t, o) {
  const lift = o.lift ?? 1;
  let s = bg(o.sky || 'storm');
  if (o.starsOn) s += stars(t);
  s += o.extraSky || '';
  s += ground(1500, o.g1 || '#2F4F3A', o.g2 || '#263F30');
  if (o.rain) s += rain(t, o.rain, 0.6, 0.15, 'outsideMountain');
  if (o.glowDome) s += `<ellipse cx="540" cy="1250" rx="520" ry="380" fill="url(#halo)" opacity="${o.glowDome}"/>`;
  // sheltered villagers + cows
  s += cow({ x: 210, y: 1520, s: 0.5, flip: true }) + cow({ x: 880, y: 1530, s: 0.5 });
  s += person({ x: 120, y: 1540, s: 0.5, gopi: true, veil: '#C2405A', top: '#F2A03D' }) + person({ x: 330, y: 1530, s: 0.48, stick: true, top: '#3E8E5A' });
  s += person({ x: 760, y: 1530, s: 0.48, top: '#C2405A' }) + person({ x: 980, y: 1545, s: 0.5, gopi: true, veil: '#7B4BB7', top: '#F5C04A' });
  const my = lerp(1500, 772, lift);
  s += mountain({ x: lerp(540, 470, lift), y: my, w: 1040, h: 500, lifted: lift > 0.05, sway: t });
  s += krishna({ x: 540, y: 1545, s: 1.0, armL: lerp(18, 166, eo(o.arm ?? 1)), fingerL: (o.arm ?? 1) > 0.02, glow: o.kglow ?? 0.6, eyes: 'closed' });
  return s;
}

function tracker(t, lit, glowIdx, igniteT) {
  let s = bg('night') + stars(t) + moon(860, 300, 54);
  const names = ['DHANTERAS', 'CHHOTI DIWALI', 'LAKSHMI PUJA', 'GOVARDHAN', 'BHAI DOOJ'];
  for (let i = 0; i < 5; i++) {
    const x = 140 + i * 200, on = i < lit || (i === glowIdx && t >= igniteT);
    const g = i === glowIdx ? 1 + 0.6 * Math.sin(t * 6) * (t >= igniteT ? 0.4 : 1) : 1;
    s += diya(x, 1180, 0.9, t, i, on, on ? g : 0);
    if (i === glowIdx && t < igniteT) s += `<circle cx="${x}" cy="1150" r="${(70 + 10 * Math.sin(t * 6)).toFixed(1)}" fill="none" stroke="#F5C04A" stroke-width="4" opacity=".6" stroke-dasharray="8 10"/>`;
    s += `<text x="${x}" y="1270" text-anchor="middle" font-family="Baloo" font-weight="700" font-size="24" fill="${i === glowIdx ? '#F5C04A' : '#E8DCC4'}" letter-spacing="2">${names[i]}</text>`;
  }
  if (igniteT && t >= igniteT) { const k = seg(t, igniteT, igniteT + 0.6); const x = 140 + glowIdx * 200;
    s += `<circle cx="${x}" cy="1150" r="${(40 + 260 * eo(k)).toFixed(0)}" fill="none" stroke="#FFE29A" stroke-width="${(10 * (1 - k)).toFixed(1)}" opacity="${(1 - k).toFixed(2)}"/>`; }
  return s;
}

// route the scene engine's calls to the v2 character library
window.T_NOW = 0;
krishna = (o = {}) => krishna2({ ...o, t: T_NOW, liftHand: o.fingerL, elbowL: o.elbowL ?? ((o.armL ?? 0) > 120 ? 0 : 10) });
cow = (o = {}) => cow2({ ...o, t: T_NOW });
nand = (o = {}) => nand2(o);
indra = (o = {}) => indra2(o);
person = (o = {}) => (o.gopi ? gopi2({ ...o, t: T_NOW }) : gwala2(o));
mountain = (o = {}) => mountain2({ ...o, t: o.t ?? T_NOW });
tree = (x, y, s = 1, c, cd, sway = 0) => tree2(x, y, s, sway);

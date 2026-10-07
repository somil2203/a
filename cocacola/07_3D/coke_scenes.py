"""Blender (bpy, Cycles CPU) shots for the Coca-Cola Short. All geometry is generated here.

usage: python3 coke_scenes.py SHOT OUTDIR [--frame N] [--res WxH] [--samples S] [--step K]
shots:
  apothecary  3.95 s  dark 1880s pharmacy shelf; push to MORPHINE, focus racks to COCA   (119 f)
  mol_in      1.45 s  cocaine molecule (PubChem CID 446220 3D conformer) assembles       (44 f)
  mol_out     2.35 s  same molecule; on "removed" its atoms scatter into darkness         (71 f)
  leaves      2.95 s  coca leaves (Erythroxylum-style blades with twin lines) drifting   (89 f)
"""
import math
import os
import random
import sys

import bpy
from mathutils import Vector
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/home/user/a/tesla/07_3D")
from tesla_scenes import camera, key, light, obj_box, reset  # noqa: E402  (shared helpers)


def mat(name, col, rough=0.4, metal=0.0, emit=None, es=0.0, coat=0.0, image=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*col, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    p.inputs["Coat Weight"].default_value = coat
    if image:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(image)
        nt.links.new(tex.outputs["Color"], p.inputs["Base Color"])
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1)
    p.inputs["Emission Strength"].default_value = es
    return m

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "_tex")
os.makedirs(TEX, exist_ok=True)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def label_tex(name, line1, line2=""):
    p = os.path.join(TEX, f"label_{name}.png")
    im = Image.new("RGB", (512, 640), (222, 206, 168))
    d = ImageDraw.Draw(im)
    d.rectangle((14, 14, 497, 625), outline=(70, 40, 20), width=6)
    d.rectangle((30, 30, 481, 609), outline=(70, 40, 20), width=2)
    f1 = ImageFont.truetype(SERIF, 86 if len(line1) <= 6 else 62)
    d.text((256, 260), line1, font=f1, fill=(50, 25, 10), anchor="mm")
    if line2:
        d.text((256, 380), line2, font=ImageFont.truetype(SERIF, 44), fill=(80, 45, 20), anchor="mm")
    d.text((256, 520), "ATLANTA · GA", font=ImageFont.truetype(SERIF, 30), fill=(90, 60, 30), anchor="mm")
    im.save(p)
    return p


def glass_mat(name, tint):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*tint, 1)
    p.inputs["Roughness"].default_value = 0.06
    p.inputs["Transmission Weight"].default_value = 1.0
    p.inputs["IOR"].default_value = 1.45
    return m


def bottle(x, y, h, r, tint, label=None, name="b"):
    """apothecary bottle: body + shoulder + neck + stopper, optional paper label facing -Y"""
    g = glass_mat(f"g_{name}", tint)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=r, depth=h, location=(x, y, h / 2))
    body = bpy.context.object
    body.data.materials.append(g)
    bv = body.modifiers.new("b", "BEVEL")
    bv.width = r * 0.25
    bv.segments = 4
    bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=r, radius2=r * 0.35, depth=r * 0.7,
                                    location=(x, y, h + r * 0.35))
    sh = bpy.context.object
    sh.data.materials.append(g)
    bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=r * 0.35, depth=r * 0.55, location=(x, y, h + r * 0.95))
    nk = bpy.context.object
    nk.data.materials.append(g)
    bpy.ops.object.shade_smooth()
    cork = mat(f"cork_{name}", (0.35, 0.22, 0.12), 0.8)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=r * 0.38, depth=r * 0.4, location=(x, y, h + r * 1.35))
    bpy.context.object.data.materials.append(cork)
    if label:
        lm = mat(f"lab_{name}", (1, 1, 1), 0.7, image=label)
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y - r - 0.004, h * 0.5), rotation=(math.radians(90), 0, 0))
        lp = bpy.context.object
        lp.scale = (r * 1.25, h * 0.48, 1)
        lp.data.materials.append(lm)
        cw = lp.modifiers.new("curve", "SIMPLE_DEFORM")
        cw.deform_method = "BEND"
        cw.deform_axis = "Y"
        cw.angle = math.radians(-60)
    return body


def apothecary(sc, n=119):
    sc.cycles.samples = min(sc.cycles.samples, 14)
    sc.cycles.transmission_bounces = 4
    sc.cycles.max_bounces = 6
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.004, 0.003, 0.002, 1)
    wood = mat("wood", (0.10, 0.05, 0.025), 0.45)
    obj_box((6, 1.2, 0.08), (0, 0.2, -0.04), wood)            # shelf board
    obj_box((6, 0.08, 4), (0, 0.85, 1.6), mat("wall", (0.02, 0.014, 0.009), 0.9))
    rng = random.Random(3)
    lineup = [(-1.45, "a", (0.25, 0.32, 0.18), None), (-1.0, "b", (0.55, 0.32, 0.12), label_tex("lau", "TINCT.", "OPII")),
              (-0.45, "morph", (0.42, 0.22, 0.08), label_tex("morph", "MORPHINE", "SULPH.")),
              (0.15, "c", (0.2, 0.3, 0.42), None), (0.62, "coca", (0.32, 0.42, 0.2), label_tex("coca", "COCA", "EXT. FLUID")),
              (1.12, "d", (0.5, 0.36, 0.2), None), (1.55, "e", (0.25, 0.32, 0.18), None)]
    for x, nm, tint, lab in lineup:
        h = 0.62 + rng.uniform(-0.12, 0.12) if nm not in ("morph", "coca") else 0.66
        r = 0.16 + rng.uniform(-0.02, 0.03)
        bottle(x, 0.25 + rng.uniform(-0.05, 0.05), h, r, tint, lab, nm)
    # warm oil-lamp key + cool rim
    light("POINT", (-1.4, -0.9, 1.25), 60, col=(1.0, 0.62, 0.3))
    light("AREA", (1.8, -1.6, 1.8), 120, 1.5, (1.0, 0.8, 0.6), target=(0, 0.2, 0.4))
    light("AREA", (0, 1.5, 2.2), 90, 2.0, (0.55, 0.65, 0.9), target=(0, 0.2, 0.4))
    cam, tgt = camera((-0.3, -2.6, 0.75), (-0.45, 0.25, 0.42), 50)
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = 1.8
    focus = bpy.data.objects.new("focus", None)
    bpy.context.scene.collection.objects.link(focus)
    cam.data.dof.focus_object = focus
    key(cam, 1, location=Vector((-0.55, -2.7, 0.8)))
    key(cam, 70, location=Vector((-0.45, -1.9, 0.62)))
    key(cam, n, location=Vector((0.55, -2.0, 0.62)))
    key(tgt, 1, location=Vector((-0.45, 0.25, 0.42)))
    key(tgt, 70, location=Vector((-0.45, 0.25, 0.4)))
    key(tgt, n, location=Vector((0.62, 0.25, 0.4)))
    key(focus, 1, location=Vector((-0.45, 0.08, 0.38)))     # MORPHINE sharp
    key(focus, 72, location=Vector((-0.45, 0.08, 0.38)))
    key(focus, 100, location=Vector((0.62, 0.08, 0.38)))     # rack to COCA ("searching for a cure")
    sc.frame_start, sc.frame_end = 1, n


def read_sdf(path):
    lines = open(path).read().splitlines()
    na, nb = int(lines[3][:3]), int(lines[3][3:6])
    atoms = []
    for l in lines[4:4 + na]:
        p = l.split()
        atoms.append((Vector((float(p[0]), float(p[1]), float(p[2]))), p[3]))
    bonds = []
    for l in lines[4 + na:4 + na + nb]:
        bonds.append((int(l[:3]) - 1, int(l[3:6]) - 1, int(l[6:9])))
    return atoms, bonds


CPK = {"C": ((0.16, 0.16, 0.17), 0.30), "H": ((0.92, 0.92, 0.94), 0.17), "N": ((0.2, 0.35, 1.0), 0.32),
       "O": ((1.0, 0.12, 0.08), 0.31)}


def molecule(sc, n, scatter_at=None, assemble=False):
    sc.cycles.samples = min(sc.cycles.samples, 20)
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.002, 0.002, 0.003, 1)
    atoms, bonds = read_sdf(os.path.join(HERE, "data", "cocaine_cid446220_3d.sdf"))
    c = sum((a for a, _ in atoms), Vector()) / len(atoms)
    root = bpy.data.objects.new("mol", None)
    bpy.context.scene.collection.objects.link(root)
    mats = {e: mat(f"m_{e}", col, 0.22, emit=col, es=0.15) for e, (col, _) in CPK.items()}
    bondm = mat("bond", (0.55, 0.57, 0.62), 0.3, metal=0.4)
    rng = random.Random(7)
    objs = []
    for i, (p, e) in enumerate(atoms):
        col, rad = CPK.get(e, CPK["C"])
        bpy.ops.mesh.primitive_uv_sphere_add(radius=rad, location=p - c, segments=32, ring_count=16)
        o = bpy.context.object
        o.data.materials.append(mats.get(e, mats["C"]))
        bpy.ops.object.shade_smooth()
        o.parent = root
        objs.append(o)
    for a, b, order in bonds:
        pa, pb = atoms[a][0] - c, atoms[b][0] - c
        d = pb - pa
        offs = [0.0] if order == 1 else [-0.06, 0.06]
        for off in offs:
            side = d.cross(Vector((0, 0, 1))).normalized() * off if d.cross(Vector((0, 0, 1))).length > 1e-6 else Vector()
            bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=d.length, location=(pa + pb) / 2 + side, vertices=16)
            cy = bpy.context.object
            cy.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
            cy.data.materials.append(bondm)
            cy.parent = root
            objs.append(cy)
    key(root, 1, rotation_euler=(math.radians(20), 0, math.radians(-30)))
    key(root, n, rotation_euler=(math.radians(28), 0, math.radians(-30 + 1.6 * n)))
    if assemble:  # atoms fly in from scattered positions
        for o in objs:
            final = o.location.copy()
            start = final * 3.5 + Vector((rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(-3, 3)))
            f0 = rng.randint(1, 10)
            key(o, f0, location=start)
            key(o, f0 + 22, location=final)
            key(o, 1, scale=(0.01, 0.01, 0.01))
            key(o, f0 + 6, scale=(1, 1, 1))
    if scatter_at:
        for o in objs:
            start = o.location.copy()
            out = start * 4 + Vector((rng.uniform(-4, 4), rng.uniform(-4, 4), rng.uniform(-4, 4)))
            f0 = scatter_at + rng.randint(-2, 6)
            key(o, f0, location=start)
            key(o, n, location=out)
            key(o, f0, scale=(1, 1, 1))
            key(o, n, scale=(0.05, 0.05, 0.05))
    light("AREA", (4, -5, 4), 900, 4, (1.0, 0.95, 0.9), target=(0, 0, 0))
    light("AREA", (-5, 2, 2), 500, 3, (0.5, 0.65, 1.0), target=(0, 0, 0))
    light("AREA", (0, 5, -2), 400, 3, (1.0, 0.4, 0.3), target=(0, 0, 0))
    cam, tgt = camera((0, -33, 0), (0, 0, 0), 50)
    key(cam, 1, location=Vector((0, -35.0, 0.6)))
    key(cam, n, location=Vector((0, -30.0, 0.2)))
    sc.frame_start, sc.frame_end = 1, n


def make_leaf(name, m, length=1.0):
    """coca-style leaf: elliptical blade, slight fold, twin longitudinal lines either side of the midrib"""
    bm_verts, faces = [], []
    nx, ny = 24, 8
    for i in range(nx + 1):
        u = i / nx
        half_w = 0.24 * length * math.sin(math.pi * u) ** 0.85
        for j in range(ny + 1):
            v = j / ny * 2 - 1
            x = (u - 0.5) * length
            y = v * half_w
            z = 0.06 * length * (abs(v) ** 1.6) + 0.04 * length * math.sin(math.pi * u)
            bm_verts.append((x, y, z))
    for i in range(nx):
        for j in range(ny):
            a = i * (ny + 1) + j
            faces.append((a, a + 1, a + ny + 2, a + ny + 1))
    me = bpy.data.meshes.new(name)
    me.from_pydata(bm_verts, [], faces)
    me.update()
    me.uv_layers.new()
    for poly in me.polygons:
        poly.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(m)
    sol = o.modifiers.new("s", "SOLIDIFY")
    sol.thickness = 0.008
    return o


def leaf_texture():
    p = os.path.join(TEX, "coca_leaf.png")
    w, h = 1024, 512
    im = Image.new("RGB", (w, h), (70, 128, 45))
    d = ImageDraw.Draw(im)
    for k in range(40):
        y = h // 2 + (k - 20) * 3
    d.line((0, h // 2, w, h // 2), fill=(150, 190, 110), width=6)              # midrib
    for s in (-1, 1):                                                          # coca's twin arcs
        pts = [(x, h // 2 + s * (h * 0.28) * math.sin(math.pi * x / w) ** 1.2) for x in range(0, w + 1, 16)]
        d.line(pts, fill=(105, 155, 75), width=3)
    for k in range(1, 14):                                                     # fine lateral veins
        x = k * w / 14
        for s in (-1, 1):
            d.line((x, h // 2, x + 40, h // 2 + s * h * 0.45), fill=(88, 140, 60), width=2)
    im.save(p)
    return p


def leaves(sc, n=89):
    sc.cycles.samples = min(sc.cycles.samples, 20)
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.002, 0.004, 0.002, 1)
    lm = mat("leaf", (1, 1, 1), 0.38, image=leaf_texture(), coat=0.6)
    p = lm.node_tree.nodes["Principled BSDF"]
    p.inputs["Subsurface Weight"].default_value = 0.15
    rng = random.Random(11)
    for k in range(9):
        o = make_leaf(f"leaf{k}", lm, rng.uniform(0.8, 1.25))
        x, z = rng.uniform(-1.3, 1.3), rng.uniform(-1.6, 2.4)
        y = rng.uniform(-0.6, 1.6)
        r0 = (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(0, 6.28))
        key(o, 1, location=Vector((x, y, z + 0.6)), rotation_euler=r0)
        key(o, n, location=Vector((x + rng.uniform(-0.3, 0.3), y, z - 0.9)),
            rotation_euler=(r0[0] + rng.uniform(-0.8, 0.8), r0[1] + rng.uniform(-0.8, 0.8), r0[2] + rng.uniform(-1, 1)))
    light("AREA", (2.5, -3, 3), 500, 3, (1.0, 0.95, 0.85), target=(0, 0, 0.3))
    light("AREA", (-3, 2, 1), 400, 2.5, (0.6, 1.0, 0.7), target=(0, 0, 0.3))
    light("AREA", (0, 4, 3), 350, 3, (0.9, 1.0, 0.8), target=(0, 0, 0.3))
    cam, tgt = camera((0, -5.2, 0.4), (0, 0, 0.3), 45)
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = 2.8
    cam.data.dof.focus_distance = 5.0
    key(cam, 1, location=Vector((0.2, -5.6, 0.5)))
    key(cam, n, location=Vector((-0.1, -4.6, 0.3)))
    sc.frame_start, sc.frame_end = 1, n


def main():
    shot, out = sys.argv[1], sys.argv[2]
    a = sys.argv[3:]
    res = tuple(int(v) for v in a[a.index("--res") + 1].split("x")) if "--res" in a else (720, 1280)
    samples = int(a[a.index("--samples") + 1]) if "--samples" in a else 16
    sc = reset(res, samples)
    {"apothecary": apothecary, "mol_in": lambda s: molecule(s, 44, assemble=True),
     "mol_out": lambda s: molecule(s, 71, scatter_at=37), "leaves": leaves}[shot](sc)
    os.makedirs(out, exist_ok=True)
    if "--frame" in a:
        f = int(a[a.index("--frame") + 1])
        sc.frame_set(f)
        sc.render.filepath = os.path.join(out, f"test_{shot}_{f}.png")
        bpy.ops.render.render(write_still=True)
    else:
        if "--step" in a:
            sc.frame_step = int(a[a.index("--step") + 1])
        sc.render.filepath = os.path.join(out, "f")
        bpy.ops.render.render(animation=True)


if __name__ == "__main__":
    main()

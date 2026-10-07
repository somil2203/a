"""Blender (bpy, Cycles CPU) shots for the Tesla Short. Generated assets, no external models.

usage: python3 tesla_scenes.py SHOT OUTDIR [--frame N] [--res WxH] [--samples S]
shots:
  year2003  1.65s  extruded "2003", numbers rise, slow dolly            (50 f)
  doorway   4.55s  dark corridor, door opens, backlit figure walks in    (137 f)
  network   5.70s  company node network, Eberhard's node is cut out      (171 f)
"""
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_ANTON = "/home/user/a/edit/fonts/anton.woff"
FONT_INTER = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FPS = 30


def reset(res, samples):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6
    sc.cycles.diffuse_bounces = 2
    sc.cycles.glossy_bounces = 3
    sc.cycles.volume_bounces = 1
    sc.render.fps = FPS
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.0, 0.0, 0.0, 1)
    return sc


def mat(name, col, rough=0.4, metal=0.0, emit=None, es=0.0, alpha=1.0, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*col, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    p.inputs["Coat Weight"].default_value = coat
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1)
    p.inputs["Emission Strength"].default_value = es
    if alpha < 1:
        p.inputs["Alpha"].default_value = alpha
    return m


def obj_box(size, loc, m=None, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        b = o.modifiers.new("b", "BEVEL")
        b.width = bevel
        b.segments = 4
    if m:
        o.data.materials.append(m)
    return o


def text(body, size, extrude, loc, rot, m, font=FONT_ANTON, bevel=0.0):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.data.body = body
    o.data.size = size
    o.data.extrude = extrude
    o.data.bevel_depth = bevel
    o.data.bevel_resolution = 3
    o.data.align_x = "CENTER"
    o.data.align_y = "CENTER"
    o.data.font = bpy.data.fonts.load(font)
    o.data.materials.append(m)
    return o


def light(kind, loc, energy, size=1.0, col=(1, 1, 1), target=None, spot=None):
    d = bpy.data.lights.new(kind, kind)
    d.energy = energy
    d.color = col
    if kind == "AREA":
        d.size = size
    if kind == "SPOT" and spot:
        d.spot_size = spot
        d.spot_blend = 0.4
    o = bpy.data.objects.new(kind, d)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    if target:
        o.rotation_euler = (Vector(target) - o.location).to_track_quat("-Z", "Y").to_euler()
    return o


def camera(loc, target, lens):
    c = bpy.data.cameras.new("cam")
    c.lens = lens
    o = bpy.data.objects.new("cam", c)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    bpy.context.scene.camera = o
    t = bpy.data.objects.new("tgt", None)
    bpy.context.scene.collection.objects.link(t)
    t.location = target
    cn = o.constraints.new("TRACK_TO")
    cn.target = t
    cn.track_axis = "TRACK_NEGATIVE_Z"
    cn.up_axis = "UP_Y"
    return o, t


def key(o, f, **kw):
    for k, v in kw.items():
        setattr(o, k, v)
        o.keyframe_insert(data_path=k, frame=f)


def fog(density, size=(30, 30, 12), loc=(0, 0, 4)):
    m = bpy.data.materials.new("fog")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    v = nt.nodes.new("ShaderNodeVolumePrincipled")
    v.inputs["Density"].default_value = density
    v.inputs["Anisotropy"].default_value = 0.45
    nt.links.new(v.outputs[0], nt.nodes["Material Output"].inputs["Volume"])
    obj_box(size, loc, m)


# ------------------------------------------------------------------ shots
def year2003(sc, n=50):
    """'It's 2003.' - gold-chrome digits rise out of darkness one by one, camera dollies in."""
    gold = mat("gold", (0.85, 0.66, 0.32), 0.22, metal=1.0)
    floor = mat("floor", (0.004, 0.004, 0.005), 0.9)
    obj_box((30, 30, 0.1), (0, 0, -0.05), floor)
    light("AREA", (3, -4, 5), 900, 4, (1.0, 0.9, 0.8), target=(0, 0, 1))
    light("AREA", (-4, 2, 3), 500, 3, (0.5, 0.65, 1.0), target=(0, 0, 1))
    light("AREA", (0, 3, 2.2), 260, 2, (0.6, 0.75, 1.0), target=(0, 0, 1.2))
    digits = []
    for i, ch in enumerate("2003"):
        o = text(ch, 1.9, 0.2, ((i - 1.5) * 0.86, 0, 0.9), (math.radians(90), 0, 0), gold, bevel=0.02)
        digits.append(o)
        f0 = 1 + i * 4
        key(o, f0, location=Vector(((i - 1.5) * 0.86, 0, -1.3)))
        key(o, f0 + 12, location=Vector(((i - 1.5) * 0.86, 0, 0.9)))
        key(o, f0, rotation_euler=(math.radians(150), 0, 0))
        key(o, f0 + 12, rotation_euler=(math.radians(90), 0, 0))
    cam, tgt = camera((0.8, -8.5, 0.9), (0, 0, 0.95), 35)
    key(cam, 1, location=Vector((1.1, -9.2, 0.55)))
    key(cam, n, location=Vector((0.3, -7.7, 0.95)))
    sc.frame_start, sc.frame_end = 1, n


def make_figure(m):
    """Stylised human silhouette from primitives (only ever seen backlit)."""
    root = bpy.data.objects.new("figure", None)
    bpy.context.scene.collection.objects.link(root)
    parts = {}

    def cap(name, r, depth, loc, parent):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, vertices=24)
        o = bpy.context.object
        b = o.modifiers.new("b", "BEVEL")
        b.width = r * 0.9
        b.segments = 5
        o.data.materials.append(m)
        o.parent = parent
        parts[name] = o
        return o

    torso = cap("torso", 0.21, 0.62, (0, 0, 1.25), root)
    torso.scale = (1.0, 0.55, 1.0)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(0, 0, 1.72))
    head = bpy.context.object
    head.data.materials.append(m)
    head.parent = root
    for side in (-1, 1):
        hip = bpy.data.objects.new(f"hip{side}", None)
        bpy.context.scene.collection.objects.link(hip)
        hip.parent = root
        hip.location = (0.1 * side, 0, 0.95)
        leg = cap(f"leg{side}", 0.08, 0.92, (0, 0, -0.46), hip)
        parts[f"hip{side}"] = hip
        sh = bpy.data.objects.new(f"sh{side}", None)
        bpy.context.scene.collection.objects.link(sh)
        sh.parent = root
        sh.location = (0.27 * side, 0, 1.5)
        cap(f"arm{side}", 0.055, 0.66, (0, 0, -0.33), sh)
        parts[f"sh{side}"] = sh
    return root, parts


def doorway(sc, n=54):
    """'Then in 2004 ... walks in. Elon Musk.' - a door opens onto blinding light; a figure walks in."""
    sc.cycles.samples = min(sc.cycles.samples, 24)
    dark = mat("wall", (0.006, 0.007, 0.009), 0.85)
    floorm = mat("floor", (0.015, 0.015, 0.018), 0.18)
    obj_box((6, 40, 0.1), (0, 8, -0.05), floorm)
    obj_box((0.1, 40, 4), (-2.0, 8, 2), dark)
    obj_box((0.1, 40, 4), (2.0, 8, 2), dark)
    obj_box((6, 40, 0.1), (0, 8, 4.0), dark)
    # back wall with door opening
    obj_box((1.4, 0.2, 4), (-1.3, 12, 2), dark)
    obj_box((1.4, 0.2, 4), (1.3, 12, 2), dark)
    obj_box((1.2, 0.2, 1.2), (0, 12, 3.4), dark)
    glow = mat("glow", (1, 1, 1), 0.5, emit=(1.0, 0.95, 0.88), es=0.0)
    obj_box((1.4, 0.05, 2.9), (0, 13.6, 1.4), glow)
    es = glow.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    es.default_value = 0.0
    es.keyframe_insert("default_value", frame=1)
    es.default_value = 18.0
    es.keyframe_insert("default_value", frame=26)
    # two sliding door leaves
    doorm = mat("door", (0.05, 0.05, 0.06), 0.35, metal=0.6)
    L = obj_box((0.6, 0.12, 2.8), (-0.3, 12.05, 1.4), doorm)
    R = obj_box((0.6, 0.12, 2.8), (0.3, 12.05, 1.4), doorm)
    key(L, 4, location=Vector((-0.3, 12.05, 1.4)))
    key(L, 24, location=Vector((-0.95, 12.05, 1.4)))
    key(R, 4, location=Vector((0.3, 12.05, 1.4)))
    key(R, 24, location=Vector((0.95, 12.05, 1.4)))
    bl = light("AREA", (0, 13.3, 1.6), 0, 1.5, (1.0, 0.95, 0.88), target=(0, 0, 1.0))
    bl.data.shape = "RECTANGLE"
    bl.data.size, bl.data.size_y = 1.2, 2.8
    key(bl.data, 1, energy=0.0)
    key(bl.data, 26, energy=700.0)
    beam = bpy.data.materials.new("beam")
    beam.use_nodes = True
    nt = beam.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = (1.0, 0.93, 0.85, 1)
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    grad = nt.nodes.new("ShaderNodeTexGradient")
    grad.gradient_type = "LINEAR"
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (0, 0, math.radians(90))
    nt.links.new(tc.outputs["Generated"], mp.inputs[0])
    nt.links.new(mp.outputs[0], grad.inputs[0])
    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.inputs["To Min"].default_value = 0.0
    ramp.inputs["To Max"].default_value = 0.22
    nt.links.new(grad.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    em.inputs[1].default_value = 0.0
    em.inputs[1].keyframe_insert("default_value", frame=8)
    em.inputs[1].default_value = 1.0
    em.inputs[1].keyframe_insert("default_value", frame=30)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 8.2, 0.012))
    fl = bpy.context.object
    fl.scale = (1.3, 7.6, 1)
    fl.data.materials.append(beam)
    cam, tgt = camera((0.35, -1.0, 1.05), (0, 12, 1.45), 32)
    key(cam, 1, location=Vector((0.3, -1.0, 1.0)))
    key(cam, n, location=Vector((0.1, 2.6, 1.15)))
    sc.frame_start, sc.frame_end = 1, n


def network(sc, n=171, cut_frame=118):
    """'In 2007, Eberhard ... was pushed out of his own company.'
    The company as a lit network of people-nodes; Eberhard's links snap and his node drops into darkness."""
    sc.cycles.samples = min(sc.cycles.samples, 32)
    floor = mat("floor", (0.008, 0.009, 0.012), 0.2)
    obj_box((40, 40, 0.1), (0, 0, -1.6), floor)
    nodes = {  # name: position, colour
        "MUSK": ((0.0, 0.3, 1.35), (1.0, 0.12, 0.06)),
        "EBERHARD": ((0.0, 0.0, 0.0), (1.0, 0.8, 0.35)),
        "TARPENNING": ((-1.15, 0.2, -0.55), (0.15, 0.45, 1.0)),
        "BOARD": ((1.15, 0.25, -0.45), (0.15, 0.45, 1.0)),
        "ENGINEERS": ((-0.55, 0.5, -1.3), (0.15, 0.45, 1.0)),
        "INVESTORS": ((0.85, 0.6, 0.85), (0.15, 0.45, 1.0)),
    }
    objs = {}
    for name, (p, c) in nodes.items():
        m = mat(f"n_{name}", c, 0.3, emit=c, es=1.6 if name != "EBERHARD" else 2.2)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17 if name in ("MUSK", "EBERHARD") else 0.12, location=p,
                                             segments=48, ring_count=24)
        o = bpy.context.object
        o.data.materials.append(m)
        bpy.ops.object.shade_smooth()
        objs[name] = (o, m)
        lab = text(name, 0.12, 0.0, (p[0], p[1] - 0.05, p[2] - 0.36), (math.radians(90), 0, 0),
                   mat(f"l_{name}", (1, 1, 1), 0.5, emit=(0.9, 0.92, 1.0), es=1.2), font=FONT_INTER)
        lab.parent = o
        lab.location = (0, -0.05, -0.36)
        o.location = p
    links = [("EBERHARD", "MUSK"), ("EBERHARD", "TARPENNING"), ("EBERHARD", "BOARD"), ("EBERHARD", "ENGINEERS"),
             ("EBERHARD", "INVESTORS"), ("MUSK", "INVESTORS"), ("MUSK", "BOARD"), ("TARPENNING", "ENGINEERS"),
             ("BOARD", "INVESTORS")]
    for a, b in links:
        pa, pb = Vector(nodes[a][0]), Vector(nodes[b][0])
        d = pb - pa
        lm = mat(f"ln_{a}_{b}", (0.3, 0.5, 1.0), 0.5, emit=(0.25, 0.5, 1.0), es=1.4)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=d.length, location=(pa + pb) / 2, vertices=12)
        c = bpy.context.object
        c.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
        c.data.materials.append(lm)
        if "EBERHARD" in (a, b):
            e = lm.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
            e.default_value = 1.4
            e.keyframe_insert("default_value", frame=cut_frame - 14)
            e.default_value = 6.0
            e.keyframe_insert("default_value", frame=cut_frame - 4)
            e.default_value = 0.0
            e.keyframe_insert("default_value", frame=cut_frame)
            c.keyframe_insert("scale", frame=cut_frame - 1)
            c.scale = (1, 1, 0.001)
            c.keyframe_insert("scale", frame=cut_frame + 1)
    # Musk node grows (taking control), Eberhard dims and is pushed out, falling into darkness
    mo, mm = objs["MUSK"]
    key(mo, 1, scale=(1, 1, 1))
    key(mo, cut_frame - 20, scale=(1.35, 1.35, 1.35))
    eo, em = objs["EBERHARD"]
    key(eo, cut_frame - 2, location=Vector((0, 0, 0)))
    key(eo, cut_frame + 10, location=Vector((-0.25, -0.15, -0.35)))
    key(eo, n, location=Vector((-0.9, -0.3, -3.2)))
    ee = em.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    ee.default_value = 2.2
    ee.keyframe_insert("default_value", frame=cut_frame)
    ee.default_value = 0.4
    ee.keyframe_insert("default_value", frame=n)
    eb = em.node_tree.nodes["Principled BSDF"].inputs["Emission Color"]
    eb.default_value = (1.0, 0.8, 0.35, 1)
    eb.keyframe_insert("default_value", frame=cut_frame)
    eb.default_value = (1.0, 0.25, 0.2, 1)
    eb.keyframe_insert("default_value", frame=cut_frame + 8)
    light("AREA", (0, -4, 3), 60, 4, (0.6, 0.7, 1.0), target=(0, 0, 0))
    cam, tgt = camera((0.0, -6.4, 0.6), (0, 0, 0.0), 38)
    key(cam, 1, location=Vector((-0.6, -6.8, 0.9)))
    key(cam, cut_frame, location=Vector((0.2, -5.6, 0.5)))
    key(cam, n, location=Vector((0.1, -6.2, 0.2)))
    key(tgt, cut_frame, location=Vector((0, 0, 0.1)))
    key(tgt, n, location=Vector((-0.4, 0, -0.9)))
    sc.frame_start, sc.frame_end = 1, n


def names(sc, n=123):
    """'Most people have never heard their names.' - the two founders' names in darkness,
    a slow light sweep reveals them, then the light dies out."""
    sc.cycles.samples = min(sc.cycles.samples, 24)
    steel = mat("steel", (0.8, 0.8, 0.82), 0.28, metal=1.0)
    floor = mat("floor", (0.004, 0.004, 0.005), 0.9)
    obj_box((30, 30, 0.1), (0, 0, -0.05), floor)
    a = text("MARTIN", 0.74, 0.08, (0, 0, 2.45), (math.radians(90), 0, 0), steel, bevel=0.01)
    b = text("EBERHARD", 0.74, 0.08, (0, 0, 1.8), (math.radians(90), 0, 0), steel, bevel=0.01)
    c = text("MARC", 0.74, 0.08, (0, 0, 0.95), (math.radians(90), 0, 0), steel, bevel=0.01)
    d = text("TARPENNING", 0.74, 0.08, (0, 0, 0.3), (math.radians(90), 0, 0), steel, bevel=0.01)
    sweep = light("AREA", (-4, -3, 2.5), 0, 2.5, (1.0, 0.92, 0.82), target=(0, 0, 1.4))
    key(sweep, 1, location=Vector((-4.5, -3, 2.6)))
    key(sweep, n, location=Vector((4.5, -3, 2.0)))
    key(sweep.data, 1, energy=0.0)
    key(sweep.data, 14, energy=900.0)
    key(sweep.data, 70, energy=900.0)
    key(sweep.data, 118, energy=0.0)
    rim = light("AREA", (0, 2.5, 2.2), 0, 2, (0.55, 0.7, 1.0), target=(0, 0, 1.4))
    key(rim.data, 1, energy=0.0)
    key(rim.data, 20, energy=220.0)
    key(rim.data, 75, energy=220.0)
    key(rim.data, 116, energy=0.0)
    cam, tgt = camera((0.0, -7.0, 1.4), (0, 0, 1.38), 35)
    key(cam, 1, location=Vector((-0.4, -7.4, 1.3)))
    key(cam, n, location=Vector((0.3, -6.3, 1.45)))
    sc.frame_start, sc.frame_end = 1, n


def main():
    shot, out = sys.argv[1], sys.argv[2]
    a = sys.argv[3:]
    res = tuple(int(v) for v in a[a.index("--res") + 1].split("x")) if "--res" in a else (720, 1280)
    samples = int(a[a.index("--samples") + 1]) if "--samples" in a else 32
    sc = reset(res, samples)
    {"year2003": year2003, "doorway": doorway, "network": network, "names": names}[shot](sc)
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

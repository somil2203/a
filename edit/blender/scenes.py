"""Blender (bpy) 3D shots for the Nokia Short.

usage: python3 scenes.py SHOT OUTDIR [--frame N] [--res WxH] [--samples S]
shots: turntable, village, battery, drop, iphone, iphone_still, nokia_still
Renders RGBA PNG sequences with Cycles (CPU).
"""
import math
import os
import sys

import bpy
from mathutils import Vector
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "_tex")
os.makedirs(TEX, exist_ok=True)
FPS = 30


# ------------------------------------------------------------ scene utils
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6
    sc.cycles.diffuse_bounces = 2
    sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 2
    sc.render.fps = FPS
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    world = bpy.data.worlds.new("w")
    sc.world = world
    world.use_nodes = True
    return sc


def world_color(col, strength=1.0):
    bg = bpy.context.scene.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (*col, 1)
    bg.inputs[1].default_value = strength


def mat(name, col, rough=0.4, metal=0.0, coat=0.0, emit=None, emit_strength=0.0, image=None):
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
        if emit_strength:
            nt.links.new(tex.outputs["Color"], p.inputs["Emission Color"])
    elif emit:
        p.inputs["Emission Color"].default_value = (*emit, 1)
    p.inputs["Emission Strength"].default_value = emit_strength
    return m


def box(name, size, loc=(0, 0, 0), bevel=0.0, segs=6, material=None, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        b = o.modifiers.new("bevel", "BEVEL")
        b.width = bevel
        b.segments = segs
        b.limit_method = "NONE"
    if material:
        o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    if parent:
        o.parent = parent
    return o


def cyl(name, r, depth, loc, scale=(1, 1, 1), rot=(0, 0, 0), material=None, parent=None, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    b = o.modifiers.new("bevel", "BEVEL")
    b.width = min(r, depth) * 0.3
    b.segments = 4
    if material:
        o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    if parent:
        o.parent = parent
    return o


def plane(name, size, loc, rot=(0, 0, 0), material=None, parent=None):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0], size[1], 1)
    bpy.ops.object.transform_apply(scale=True)
    if material:
        o.data.materials.append(material)
    if parent:
        o.parent = parent
    return o


def text3d(body, size, extrude, loc, rot=(0, 0, 0), material=None, font=None):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.data.body = body
    o.data.size = size
    o.data.extrude = extrude
    o.data.bevel_depth = extrude * 0.25
    o.data.align_x = "CENTER"
    o.data.align_y = "CENTER"
    if font:
        o.data.font = bpy.data.fonts.load(font)
    if material:
        o.data.materials.append(material)
    return o


def empty(name, loc=(0, 0, 0)):
    o = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    return o


def light(kind, loc, energy, size=1.0, col=(1, 1, 1), rot=None, target=None):
    d = bpy.data.lights.new(kind + "L", kind)
    d.energy = energy
    d.color = col
    if kind == "AREA":
        d.size = size
    o = bpy.data.objects.new(kind, d)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    if rot:
        o.rotation_euler = rot
    if target:
        look(o, target)
    return o


def look(o, target):
    d = Vector(target) - o.location
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def camera(loc, target, lens=50):
    c = bpy.data.cameras.new("cam")
    c.lens = lens
    o = bpy.data.objects.new("cam", c)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    look(o, target)
    bpy.context.scene.camera = o
    return o


def key(o, frame, **props):
    for k, v in props.items():
        setattr(o, k, v)
        o.keyframe_insert(data_path=k, frame=frame)


def smooth_all():
    for a in bpy.data.actions:
        try:
            for fc in a.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "BEZIER"
                    kp.easing = "AUTO"
        except AttributeError:  # Blender 5 layered actions
            for layer in a.layers:
                for strip in layer.strips:
                    for cb in strip.channelbags:
                        for fc in cb.fcurves:
                            for kp in fc.keyframe_points:
                                kp.interpolation = "BEZIER"


# ------------------------------------------------------------ textures
FONT_MONO = os.path.join(HERE, "..", "fonts", "jbm.woff")
FONT_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"


def tex_lcd():
    p = os.path.join(TEX, "lcd.png")
    im = Image.new("RGB", (400, 340), (150, 182, 104))
    d = ImageDraw.Draw(im)
    ink = (38, 58, 30)
    for i in range(5):
        d.rectangle((16, 290 - i * 34, 30 + i * 4, 304 - i * 34), fill=ink)
        d.rectangle((370 - i * 4, 290 - i * 34, 384, 304 - i * 34), fill=ink)
    f = ImageFont.truetype(FONT_MONO, 64)
    d.text((200, 120), "NOKIA", font=f, fill=ink, anchor="mm")
    f2 = ImageFont.truetype(FONT_MONO, 40)
    d.text((200, 200), "12:07", font=f2, fill=ink, anchor="mm")
    d.text((200, 290), "Menu", font=ImageFont.truetype(FONT_MONO, 34), fill=ink, anchor="mm")
    im.save(p)
    return p


def tex_iphone():
    p = os.path.join(TEX, "ios.png")
    w, h = 640, 960
    im = Image.new("RGB", (w, h))
    px = im.load()
    for y in range(h):
        t = y / h
        c = (int(20 + 40 * t), int(40 + 20 * t), int(110 + 60 * t))
        for x in range(w):
            px[x, y] = c
    d = ImageDraw.Draw(im)
    cols = [(255, 90, 80), (90, 200, 120), (255, 190, 60), (80, 160, 255), (240, 240, 245),
            (255, 120, 180), (120, 220, 230), (170, 120, 255), (255, 150, 60), (100, 220, 160)]
    g = 140
    for r in range(4):
        for c in range(4):
            x, y = 40 + c * g + 10, 90 + r * (g + 30)
            d.rounded_rectangle((x, y, x + 100, y + 100), radius=24, fill=cols[(r * 4 + c) % len(cols)])
    d.rectangle((0, h - 170, w, h), fill=(200, 205, 215))
    for c in range(4):
        x = 40 + c * g + 10
        d.rounded_rectangle((x, h - 140, x + 100, h - 40), radius=24, fill=cols[(c * 3 + 1) % len(cols)])
    d.text((w // 2, 30), "9:41", font=ImageFont.truetype(FONT_BOLD, 34), fill=(255, 255, 255), anchor="mm")
    im.save(p)
    return p


def tex_battery():
    p = os.path.join(TEX, "batt.png")
    im = Image.new("RGB", (600, 400), (30, 34, 44))
    d = ImageDraw.Draw(im)
    d.text((300, 90), "NOKIA", font=ImageFont.truetype(FONT_BLACK, 80), fill=(235, 240, 255), anchor="mm")
    d.text((300, 180), "Li-ion BATTERY", font=ImageFont.truetype(FONT_BOLD, 44), fill=(170, 180, 200), anchor="mm")
    for i in range(4):
        d.rounded_rectangle((90 + i * 110, 250, 180 + i * 110, 340), radius=12, fill=(60, 220, 120))
    im.save(p)
    return p


def tex_floor():
    p = os.path.join(TEX, "floor.png")
    n = 1024
    im = Image.new("RGB", (n, n), (205, 200, 192))
    d = ImageDraw.Draw(im)
    for i in range(0, n, 256):
        d.line((i, 0, i, n), fill=(150, 145, 138), width=6)
        d.line((0, i, n, i), fill=(150, 145, 138), width=6)
    im.save(p)
    return p


# ------------------------------------------------------------ models
def build_nokia(loc=(0, 0, 0), exploded=False):
    """Candybar phone ~0.48 x 1.13 x 0.2 units, screen facing -Y."""
    root = empty("nokia", loc)
    navy = mat("navy", (0.035, 0.06, 0.13), 0.28, coat=0.6)
    back = mat("navyback", (0.025, 0.04, 0.09), 0.45)
    grey = mat("keys", (0.55, 0.58, 0.63), 0.35)
    navm = mat("nav", (0.45, 0.52, 0.62), 0.25, metal=0.4)
    bez = mat("bezel", (0.02, 0.02, 0.025), 0.3)
    lcd = mat("lcd", (1, 1, 1), 0.5, image=tex_lcd(), emit_strength=0.6)
    logo = mat("logo", (0.9, 0.92, 1.0), 0.3, metal=0.6)

    front = empty("front", (0, 0, 0))
    front.parent = root
    box("shell", (0.48, 0.12, 1.13), (0, -0.04, 0), bevel=0.06, segs=8, material=navy, parent=front)
    box("bezel", (0.36, 0.02, 0.33), (0, -0.105, 0.22), bevel=0.03, material=bez, parent=front)
    plane("lcd", (0.27, 0.23), (0, -0.117, 0.225), rot=(math.radians(90), 0, 0), material=lcd, parent=front)
    t = text3d("NOKIA", 0.075, 0.006, (0, -0.105, 0.445), rot=(math.radians(90), 0, 0), material=logo, font=FONT_BLACK)
    t.parent = front
    box("slit", (0.12, 0.01, 0.018), (0, -0.103, 0.51), bevel=0.008, material=bez, parent=front)
    cyl("navkey", 0.12, 0.03, (0, -0.105, -0.03), scale=(1.45, 1, 0.55), rot=(math.radians(90), 0, 0), material=navm, parent=front)
    for r in range(4):
        for c in range(3):
            cyl(f"k{r}{c}", 0.048, 0.025, (-0.13 + c * 0.13, -0.103, -0.17 - r * 0.095),
                scale=(1.3, 1, 0.8), rot=(math.radians(90), 0, 0), material=grey, parent=front)
    rear = empty("rear", (0, 0, 0))
    rear.parent = root
    box("backcover", (0.47, 0.07, 1.11), (0, 0.06, 0), bevel=0.05, segs=8, material=back, parent=rear)
    batt = None
    if exploded:
        bm = mat("battery", (0.03, 0.035, 0.045), 0.4)
        lab = mat("batlabel", (1, 1, 1), 0.5, image=tex_battery(), emit_strength=0.35)
        batt = box("battery", (0.38, 0.05, 0.55), (0, 0.02, -0.1), bevel=0.012, material=bm, parent=root)
        plane("label", (0.34, 0.5), (0, -0.0265, 0), rot=(math.radians(90), 0, 0), material=lab, parent=batt)
    return root, front, rear, batt


def build_iphone(loc=(0, 0, 0)):
    root = empty("iphone", loc)
    alu = mat("alu", (0.75, 0.76, 0.78), 0.32, metal=1.0)
    glass = mat("glass", (0.005, 0.005, 0.006), 0.04, coat=1.0)
    scr = mat("screen", (1, 1, 1), 0.2, image=tex_iphone(), emit_strength=1.4)
    btn = mat("home", (0.02, 0.02, 0.025), 0.2)
    chrome = mat("chrome", (0.9, 0.9, 0.92), 0.1, metal=1.0)
    box("body", (0.61, 0.116, 1.15), (0, 0.0, 0), bevel=0.09, segs=10, material=alu, parent=root)
    box("bezelring", (0.615, 0.02, 1.155), (0, -0.05, 0), bevel=0.09, segs=10, material=chrome, parent=root)
    box("front", (0.6, 0.02, 1.14), (0, -0.06, 0), bevel=0.085, segs=10, material=glass, parent=root)
    plane("screen", (0.5, 0.75), (0, -0.0715, 0.01), rot=(math.radians(90), 0, 0), material=scr, parent=root)
    cyl("homebtn", 0.05, 0.01, (0, -0.0712, -0.47), rot=(math.radians(90), 0, 0), material=btn, parent=root)
    box("ear", (0.1, 0.005, 0.014), (0, -0.0712, 0.48), bevel=0.006, material=btn, parent=root)
    return root


def build_house(x, y, rot, lit_frame, s=1.0):
    wall = mat(f"wall{x}{y}", (0.32, 0.30, 0.34), 0.8)
    roof = mat(f"roof{x}{y}", (0.25, 0.07, 0.05), 0.7)
    h = empty(f"house{x}{y}", (x, y, 0))
    h.rotation_euler = (0, 0, rot)
    h.scale = (s, s, s)
    box("w", (0.8, 0.8, 0.6), (x, y, 0.3), material=wall, parent=None).parent = h
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.68, depth=0.45, location=(x, y, 0.82), rotation=(0, 0, math.radians(45)))
    r = bpy.context.object
    r.data.materials.append(roof)
    r.parent = h
    win = mat(f"win{x}{y}", (1.0, 0.75, 0.35), 0.5, emit=(1.0, 0.72, 0.3), emit_strength=0.0)
    for k, (dx, dz) in enumerate([(-0.18, 0.33), (0.18, 0.33)]):
        plane(f"win{k}", (0.16, 0.16), (x + dx, y - 0.401, dz), rot=(math.radians(90), 0, 0), material=win, parent=h)
    door = mat("door", (0.12, 0.08, 0.06), 0.7)
    plane("door", (0.16, 0.3), (x, y - 0.401, 0.15), rot=(math.radians(90), 0, 0), material=door, parent=h)
    es = win.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    es.default_value = 0.0
    es.keyframe_insert("default_value", frame=lit_frame - 1)
    es.default_value = 9.0
    es.keyframe_insert("default_value", frame=lit_frame + 3)
    # little glowing phone above the roof
    ph = mat(f"ph{x}{y}", (0.05, 0.25, 1.0), 0.4, emit=(0.08, 0.35, 1.0), emit_strength=0.0)
    p = box("phone", (0.12, 0.04, 0.26), (x, y, 1.35), bevel=0.03, material=ph)
    p.parent = h
    p.scale = (0.01, 0.01, 0.01)
    p.keyframe_insert("scale", frame=lit_frame)
    p.scale = (1.25, 1.25, 1.25)
    p.keyframe_insert("scale", frame=lit_frame + 4)
    p.scale = (1, 1, 1)
    p.keyframe_insert("scale", frame=lit_frame + 7)
    pe = ph.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    pe.default_value = 0.0
    pe.keyframe_insert("default_value", frame=lit_frame)
    pe.default_value = 2.2
    pe.keyframe_insert("default_value", frame=lit_frame + 4)
    return h


# ------------------------------------------------------------ shots
def studio(dark=(0.004, 0.006, 0.012)):
    world_color(dark, 1.0)
    light("AREA", (2.5, -3, 2.5), 400, 3, (1, 0.95, 0.9), target=(0, 0, 0))
    light("AREA", (-3, -1, 1.5), 180, 2, (0.6, 0.75, 1.0), target=(0, 0, 0))
    light("AREA", (0, 3, 2), 350, 2, (0.7, 0.85, 1.0), target=(0, 0, 0))


def shot_turntable(sc):
    """Hook: Nokia spins 360 on transparent bg (panel insert)."""
    sc.render.film_transparent = True
    studio()
    root, *_ = build_nokia()
    camera((0, -3.6, 0.35), (0, 0, 0), 60)
    sc.frame_start, sc.frame_end = 1, 60
    key(root, 1, rotation_euler=(0, 0, math.radians(-30)))
    key(root, 60, rotation_euler=(0, 0, math.radians(330)))
    for fc in _fcurves(root):
        for kp in fc.keyframe_points:
            kp.interpolation = "SINE"
            kp.easing = "EASE_OUT"


def _fcurves(o):
    ad = o.animation_data
    if not ad or not ad.action:
        return []
    a = ad.action
    if hasattr(a, "fcurves"):
        return list(a.fcurves)
    out = []
    for layer in a.layers:
        for strip in layer.strips:
            for cb in strip.channelbags:
                out += list(cb.fcurves)
    return out


def shot_village(sc, n_frames=79):
    """'Har ghar mein ek Nokia': night village, windows + phones light up in a wave."""
    sc.render.film_transparent = False
    world_color((0.02, 0.035, 0.09), 1.0)
    ground = mat("ground", (0.05, 0.06, 0.07), 0.9)
    plane("ground", (40, 40), (0, 0, 0), material=ground)
    light("SUN", (0, 0, 10), 0.9, col=(0.55, 0.65, 1.0), rot=(math.radians(50), 0, math.radians(30)))
    import random
    random.seed(4)
    houses = []
    k = 0
    for gy in range(4):
        for gx in range(3):
            x = (gx - 1) * 1.6 + random.uniform(-0.2, 0.2)
            y = gy * 1.7 + random.uniform(-0.2, 0.2)
            houses.append((x, y, random.uniform(-0.3, 0.3)))
    # light order: front to back wave
    for i, (x, y, r) in enumerate(houses):
        lit = 12 + i * 3
        build_house(x, y, r, lit, 1.0 + random.uniform(-0.1, 0.1))
    cam = camera((0.5, -5.5, 3.2), (0, 2.0, 0.4), 26)
    sc.frame_start, sc.frame_end = 1, n_frames
    key(cam, 1, location=Vector((1.4, -5.2, 3.0)))
    key(cam, n_frames, location=Vector((-0.5, -3.6, 2.0)))
    tgt = empty("tgt", (0, 2.2, 0.5))
    c = cam.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    sc.cycles.samples = min(sc.cycles.samples, 48)


def shot_battery(sc, n_frames=57):
    """'Battery khatam nahi hoti thi': exploded Nokia, battery rises glowing."""
    sc.render.film_transparent = False
    studio((0.003, 0.005, 0.01))
    root, front, rear, batt = build_nokia(exploded=True)
    floor = mat("floor", (0.01, 0.012, 0.018), 0.25)
    plane("floor", (20, 20), (0, 0, -0.62), material=floor)
    cam = camera((1.3, -3.4, 0.7), (0, -0.1, 0.15), 45)
    tgt = empty("tgt", (0, -0.15, 0.15))
    c = cam.constraints.new("TRACK_TO"); c.target = tgt; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
    sc.frame_start, sc.frame_end = 1, n_frames
    root.rotation_euler = (0, 0, math.radians(-20))
    key(front, 1, location=Vector((0, 0, 0)))
    key(front, 22, location=Vector((0, -0.55, 0)))
    key(rear, 1, location=Vector((0, 0, 0)))
    key(rear, 22, location=Vector((0, 0.38, 0)))
    key(batt, 8, location=Vector((0, 0.02, -0.1)))
    key(batt, 30, location=Vector((0.0, 0.02, 0.45)))
    key(batt, 30, rotation_euler=(0, 0, 0))
    key(batt, n_frames, rotation_euler=(0, 0, math.radians(25)))
    bl = light("POINT", (0, -0.1, 0.45), 0, col=(0.3, 1.0, 0.5))
    bl.data.shadow_soft_size = 0.2
    key(bl.data, 18, energy=0.0)
    key(bl.data, 34, energy=60.0)
    key(cam, 1, location=Vector((1.5, -3.8, 0.8)))
    key(cam, n_frames, location=Vector((1.0, -3.0, 0.6)))


def shot_drop(sc, n_frames=46, hit=32):
    """'Kabhi toot-ta nahi tha': slow-mo drop on tiles, bounce, phone fine."""
    sc.render.film_transparent = False
    world_color((0.01, 0.012, 0.02), 1.0)
    ft = mat("tiles", (1, 1, 1), 0.18, image=tex_floor())
    f = plane("floor", (6, 6), (0, 0, 0), material=ft)
    light("AREA", (1.5, -2, 3), 350, 3, (1, 0.96, 0.9), target=(0, 0, 0))
    light("AREA", (-2, 1, 1.5), 120, 2, (0.6, 0.75, 1.0), target=(0, 0, 0))
    root, *_ = build_nokia()
    cam = camera((0.8, -1.8, 1.3), (0, 0, 0.3), 40)
    tgt = empty("tgt", (0, 0, 0.3))
    c = cam.constraints.new("TRACK_TO"); c.target = tgt; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
    sc.frame_start, sc.frame_end = 1, n_frames
    r = math.radians
    key(root, 1, location=Vector((0, 0, 2.4)), rotation_euler=(r(-15), r(15), r(10)))
    key(root, hit, location=Vector((0, 0, 0.32)), rotation_euler=(r(-60), r(25), r(10)))
    key(root, hit + 5, location=Vector((0.03, 0.02, 0.5)), rotation_euler=(r(-80), r(10), r(20)))
    key(root, hit + 10, location=Vector((0.05, 0.03, 0.11)), rotation_euler=(r(-90), 0, r(25)))
    key(root, hit + 12, location=Vector((0.05, 0.03, 0.15)), rotation_euler=(r(-90), 0, r(25)))
    key(root, n_frames, location=Vector((0.05, 0.03, 0.11)), rotation_euler=(r(-90), 0, r(25)))
    for fc in _fcurves(root):
        kps = fc.keyframe_points
        if len(kps) > 1:
            kps[0].interpolation = "QUAD"
            kps[0].easing = "EASE_IN"
    key(tgt, 1, location=Vector((0, 0, 1.4)))
    key(tgt, hit, location=Vector((0, 0, 0.25)))
    key(cam, 1, location=Vector((0.9, -2.2, 2.0)))
    key(cam, hit, location=Vector((0.8, -1.7, 1.1)))
    key(cam, n_frames, location=Vector((0.6, -1.4, 1.0)))


def shot_iphone(sc, n_frames=54):
    """'Apple aaya': iPhone rises in a dark void with rim lights and a glossy floor."""
    sc.render.film_transparent = False
    world_color((0.0, 0.0, 0.0), 1.0)
    floor = mat("floor", (0.004, 0.004, 0.006), 0.08)
    plane("floor", (20, 20), (0, 0, -0.62), material=floor)
    light("AREA", (2, -2.5, 2), 300, 2.5, (1, 1, 1), target=(0, 0, 0))
    light("AREA", (-2.2, 1.5, 1), 500, 1.0, (0.55, 0.75, 1.0), target=(0, 0, 0))
    light("AREA", (2.2, 1.5, 1), 500, 1.0, (0.55, 0.75, 1.0), target=(0, 0, 0))
    ph = build_iphone()
    gold = mat("gold", (0.9, 0.62, 0.12), 0.25, metal=1.0)
    t = text3d("2007", 0.42, 0.06, (0, 0.6, 1.05), rot=(math.radians(90), 0, 0), material=gold,
               font=os.path.join(HERE, "..", "fonts", "anton.woff"))
    cam = camera((0, -3.4, 0.45), (0, 0, 0.25), 45)
    sc.frame_start, sc.frame_end = 1, n_frames
    key(ph, 1, location=Vector((0, 0, -1.8)), rotation_euler=(0, 0, math.radians(55)))
    key(ph, 22, location=Vector((0, 0, -1.8)), rotation_euler=(0, 0, math.radians(55)))
    key(ph, 40, location=Vector((0, 0, 0.02)), rotation_euler=(0, 0, math.radians(-8)))
    key(ph, n_frames, location=Vector((0, 0, 0.06)), rotation_euler=(0, 0, math.radians(8)))
    key(t, 1, scale=(0.001, 0.001, 0.001))
    key(t, 2, scale=(0.001, 0.001, 0.001))
    key(t, 7, scale=(1.15, 1.15, 1.15))
    key(t, 10, scale=(1, 1, 1))
    key(cam, 1, location=Vector((0, -3.6, 0.4)))
    key(cam, n_frames, location=Vector((0, -3.0, 0.5)))


def shot_still(sc, which):
    sc.render.film_transparent = True
    studio()
    o = build_iphone() if which == "iphone" else build_nokia()[0]
    o.rotation_euler = (0, 0, math.radians(-18))
    camera((0, -3.4, 0.25), (0, 0, 0), 60)
    sc.frame_start = sc.frame_end = 1


def main():
    shot, out = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    sc = reset()
    res = (1080, 1920)
    if "--res" in args:
        res = tuple(int(v) for v in args[args.index("--res") + 1].split("x"))
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.cycles.samples = int(args[args.index("--samples") + 1]) if "--samples" in args else 32
    {"turntable": shot_turntable, "village": shot_village, "battery": shot_battery, "drop": shot_drop,
     "iphone": shot_iphone, "iphone_still": lambda s: shot_still(s, "iphone"),
     "nokia_still": lambda s: shot_still(s, "nokia")}[shot](sc)
    os.makedirs(out, exist_ok=True)
    sc.render.filepath = os.path.join(out, "f")
    if "--frame" in args:
        f = int(args[args.index("--frame") + 1])
        sc.frame_set(f)
        sc.render.filepath = os.path.join(out, f"test_{shot}_{f}.png")
        bpy.ops.render.render(write_still=True)
    else:
        bpy.ops.render.render(animation=True)


if __name__ == "__main__":
    main()

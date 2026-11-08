"""Katha Deep 3D stills (Blender 4.2, Cycles CPU). Run: blender -b -P scenes3d.py -- SHOT OUT.png [--w 1080 --h 1920 --samples 48]
Shots: diyas2, diyas_close, chakra, fort, kundal, lotus, razor
Each shot is a still; motion (spin, push-in, flicker, embers) is added in the 2D compositor.
"""
import bpy, bmesh, math, random, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
SHOT, OUT = argv[0], argv[1]
opt = {argv[i][2:]: argv[i + 1] for i in range(2, len(argv) - 1, 2)}
W, H, SAMPLES = int(opt.get("w", 1080)), int(opt.get("h", 1920)), int(opt.get("samples", 48))
random.seed(7)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGBA"
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Medium High Contrast"
sc.world = bpy.data.worlds.new("w")
sc.world.use_nodes = True
bg = sc.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.01, 0.004, 0.003, 1)
bg.inputs[1].default_value = 1.0


def mat(name, color=(1, 1, 1), metal=0.0, rough=0.5, emit=None, estr=0.0, transmission=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = rough
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1)
        p.inputs["Emission Strength"].default_value = estr
    if transmission:
        p.inputs["Transmission Weight"].default_value = transmission
    if alpha < 1:
        p.inputs["Alpha"].default_value = alpha
    return m


def assign(o, m):
    o.data.materials.clear()
    o.data.materials.append(m)
    return o


def smooth(o):
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def cam(loc, look, lens=50):
    c = bpy.data.cameras.new("cam")
    c.lens = lens
    o = bpy.data.objects.new("cam", c)
    sc.collection.objects.link(o)
    o.location = loc
    d = Vector(look) - Vector(loc)
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    sc.camera = o
    return o


def light(kind, loc, energy, color=(1, 0.8, 0.6), size=1.0, rot=None):
    l = bpy.data.lights.new(kind, kind)
    l.energy = energy
    l.color = color
    if kind in ("AREA",):
        l.size = size
    if kind == "POINT":
        l.shadow_soft_size = size
    o = bpy.data.objects.new(kind, l)
    o.location = loc
    if rot:
        o.rotation_euler = rot
    sc.collection.objects.link(o)
    return o


GOLD = lambda: mat("gold", (1.0, 0.72, 0.3), 1.0, 0.22)
CLAY = lambda: mat("clay", (0.55, 0.2, 0.08), 0.0, 0.75)
FLAME = lambda: mat("flame", (1, 0.35, 0.05), 0, 0.5, (1.0, 0.30, 0.03), 5.0)


def diya(x, y, lit=True, scale=1.0, z=0.0):
    """Clay diya: flattened lathe bowl with a pinched spout, oil, wick and flame."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1, location=(x, y, z))
    o = bpy.context.object
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > 0.05], context="VERTS")
    for v in bm.verts:
        v.co.z *= 0.45
        if v.co.x > 0.3:  # spout
            k = (v.co.x - 0.3) / 0.7
            v.co.x += 0.55 * k * k
            v.co.y *= 1 - 0.55 * k
    bm.to_mesh(o.data)
    bm.free()
    mod = o.modifiers.new("s", "SOLIDIFY")
    mod.thickness = 0.08
    o.modifiers.new("ss", "SUBSURF").levels = 2
    o.scale = (scale, scale, scale)
    smooth(assign(o, CLAY()))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.82 * scale, depth=0.02, location=(x, y, z - 0.08 * scale))
    assign(bpy.context.object, mat("oil", (0.25, 0.12, 0.02), 0, 0.05))
    if lit:
        fx, fz = x + 1.1 * scale, z + 0.05 * scale
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.16 * scale, location=(fx, y, fz + 0.32 * scale))
        f = bpy.context.object
        f.scale = (1, 1, 2.6)
        bm = bmesh.new()
        bm.from_mesh(f.data)
        for v in bm.verts:  # teardrop: pinch the top
            if v.co.z > 0:
                v.co.x *= 1 - 0.75 * v.co.z / 0.16
                v.co.y *= 1 - 0.75 * v.co.z / 0.16
        bm.to_mesh(f.data)
        bm.free()
        smooth(assign(f, FLAME()))
        light("POINT", (fx, y, fz + 0.6 * scale), 60 * scale, (1, 0.55, 0.18), 0.1)


def ground(color=(0.18, 0.03, 0.02), rough=0.6, size=60):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, -0.45))
    return assign(bpy.context.object, mat("ground", color, 0, rough))


# ------------------------------------------------------------------ shots
def shot_diyas2():
    """Five diyas in a gentle arc; first two lit (Din 2). Low camera, shallow DOF."""
    ground((0.22, 0.03, 0.02), 0.45)
    for i in range(5):
        diya((0.55 if i % 2 else -0.55) * (1 + i * 0.3) - 0.9, i * 3.2, lit=i < 2, scale=1.0)
    c = cam((0, -5.5, 2.6), (0, 5.5, -0.2), 38)
    c.data.dof.use_dof = True
    c.data.dof.focus_distance = 7.0
    c.data.dof.aperture_fstop = 2.0
    light("AREA", (0, -3, 8), 120, (0.9, 0.5, 0.35), 8)


def shot_diyas_close():
    """One diya being lit at dusk; rows of lit diyas as bokeh behind."""
    ground((0.16, 0.05, 0.03), 0.35)
    diya(0, 0, True, 1.3)
    for row in range(3):
        for i in range(-6, 7):
            diya(i * 2.6 + row * 1.2, 9 + row * 6, True, 0.9)
    c = cam((-2.4, -5.2, 1.3), (0.6, 1.0, 0.2), 55)
    c.data.dof.use_dof = True
    c.data.dof.focus_distance = 5.4
    c.data.dof.aperture_fstop = 1.4
    bg.inputs[0].default_value = (0.08, 0.03, 0.06, 1)
    light("AREA", (6, 20, 6), 900, (0.5, 0.25, 0.6), 20)


def shot_chakra():
    """Sudarshan chakra, front-on (radially symmetric so the compositor can spin it). Transparent bg."""
    sc.render.film_transparent = True
    g = GOLD()
    bpy.ops.mesh.primitive_torus_add(major_radius=2.0, minor_radius=0.22, major_segments=96, minor_segments=24, rotation=(math.pi / 2, 0, 0))
    smooth(assign(bpy.context.object, g))
    bpy.ops.mesh.primitive_torus_add(major_radius=1.1, minor_radius=0.12, major_segments=96, minor_segments=16, rotation=(math.pi / 2, 0, 0))
    smooth(assign(bpy.context.object, g))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.3, vertices=64, rotation=(math.pi / 2, 0, 0))
    assign(bpy.context.object, mat("core", (1, 0.8, 0.4), 0, 0.3, (1, 0.75, 0.3), 25))
    n = 24
    for i in range(n):  # serrated teeth
        a = 2 * math.pi * i / n
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.28, radius2=0, depth=0.8,
                                        location=(math.cos(a) * 2.5, 0, math.sin(a) * 2.5))
        t = bpy.context.object
        t.rotation_euler = (0, -a + math.pi / 2, 0)
        t.rotation_euler = Vector((math.cos(a), 0, math.sin(a))).to_track_quat("Z", "Y").to_euler()
        t.scale = (1, 0.35, 1)
        assign(t, g)
    for i in range(12):  # spokes
        a = 2 * math.pi * i / 12
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.6, location=(math.cos(a) * 1.25, 0, math.sin(a) * 1.25))
        s = bpy.context.object
        s.rotation_euler = Vector((math.cos(a), 0, math.sin(a))).to_track_quat("Z", "Y").to_euler()
        assign(s, g)
    cam((0, -17, 0), (0, 0, 0), 50)
    light("AREA", (-4, -6, 5), 900, (1, 0.85, 0.7), 4)
    light("AREA", (5, -4, -3), 400, (1, 0.45, 0.2), 4)
    bg.inputs[0].default_value = (0.12, 0.05, 0.02, 1)


def shot_fort():
    """Pragjyotishpur at night: palace in the centre, five concentric walls -
    mountain, weapons, water, fire, wind - seen from a high angle."""
    ground((0.03, 0.02, 0.03), 0.9, 200)
    # palace
    for i, (r, h) in enumerate([(2.2, 1.6), (1.5, 1.2), (0.9, 1.0)]):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=8, location=(0, 0, sum(x[1] for x in [(2.2, 1.6), (1.5, 1.2), (0.9, 1.0)][:i]) + h / 2 - 0.45))
        assign(bpy.context.object, mat("pal", (0.12, 0.06, 0.08), 0.2, 0.6))
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.9, depth=1.6, location=(0, 0, 4.6))
    assign(bpy.context.object, mat("dome", (0.2, 0.1, 0.1), 0.6, 0.3))
    for k in range(10):
        a = random.uniform(0, 6.28)
        light("POINT", (math.cos(a) * 1.6, math.sin(a) * 1.6, random.uniform(0.5, 2.5)), 15, (1, 0.6, 0.2), 0.05)
    # 1 mountain ring
    R = 5
    for i in range(60):
        a = 2 * math.pi * i / 60
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=random.uniform(0.7, 1.1), depth=random.uniform(1.2, 2.4),
                                        location=(math.cos(a) * R, math.sin(a) * R, 0.3))
        assign(bpy.context.object, mat("rock", (0.09, 0.07, 0.08), 0, 0.9))
    # 2 weapons ring: spears
    R = 7.5
    sp = mat("steel", (0.7, 0.7, 0.75), 1.0, 0.25)
    for i in range(120):
        a = 2 * math.pi * i / 120
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.08, depth=2.2, location=(math.cos(a) * R, math.sin(a) * R, 0.6))
        o = bpy.context.object
        o.rotation_euler = (random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), 0)
        assign(o, sp)
    # 3 water ring
    R = 10
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=0.9, major_segments=128, minor_segments=12, location=(0, 0, -0.4))
    o = bpy.context.object
    o.scale = (1, 1, 0.15)
    assign(o, mat("water", (0.05, 0.25, 0.5), 0, 0.05, (0.1, 0.35, 0.8), 0.6))
    # 4 fire ring
    R = 12.5
    fire = mat("fire", (1, 0.4, 0.1), 0, 0.5, (1.0, 0.35, 0.06), 30)
    for i in range(90):
        a = 2 * math.pi * i / 90
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.35, depth=random.uniform(0.8, 1.8),
                                        location=(math.cos(a) * R, math.sin(a) * R, 0.2))
        assign(bpy.context.object, fire)
    light("POINT", (0, 0, 6), 3000, (1, 0.45, 0.15), 8)
    # 5 wind ring: translucent swirl
    R = 15
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=0.6, major_segments=128, minor_segments=12, location=(0, 0, 1.2))
    o = bpy.context.object
    o.scale = (1, 1, 1.6)
    assign(o, mat("wind", (0.5, 0.6, 0.9), 0, 0.2, (0.45, 0.6, 1.0), 0.25, alpha=0.18))
    cam((0, -27, 22), (0, 1.5, 0), 34)
    bg.inputs[0].default_value = (0.02, 0.015, 0.04, 1)
    light("SUN", (0, 0, 10), 0.4, (0.5, 0.55, 1.0), rot=(0.6, 0.2, 0))


def shot_kundal():
    """Aditi's divine earrings: a pair of ornate gold kundal, beads and drops. Transparent bg."""
    sc.render.film_transparent = True
    g = GOLD()
    ruby = mat("ruby", (0.8, 0.02, 0.05), 0, 0.05, transmission=0.6)
    emer = mat("emer", (0.02, 0.6, 0.25), 0, 0.05, transmission=0.6)
    for side in (0,):
        x = 0.0
        bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.13, major_segments=96, location=(x, 0, 0), rotation=(math.pi / 2, 0, 0))
        smooth(assign(bpy.context.object, g))
        for i in range(18):
            a = 2 * math.pi * i / 18
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(x + math.cos(a) * 1.22, 0, math.sin(a) * 1.22))
            smooth(assign(bpy.context.object, ruby if i % 3 == 0 else g))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.34, location=(x, 0, 0))
        smooth(assign(bpy.context.object, emer))
        for j, dz in enumerate((-1.45, -1.8, -2.15)):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16 - j * 0.02, location=(x, 0, dz))
            smooth(assign(bpy.context.object, g))
        bpy.ops.mesh.primitive_torus_add(major_radius=0.22, minor_radius=0.05, location=(x, 0, 1.25), rotation=(0, math.pi / 2, 0))
        assign(bpy.context.object, g)
    cam((0, -12, 0.2), (0, 0, -0.5), 50)
    light("AREA", (-4, -5, 4), 700, (1, 0.9, 0.8), 3)
    light("AREA", (4, -3, -2), 300, (1, 0.5, 0.25), 3)
    bg.inputs[0].default_value = (0.25, 0.1, 0.05, 1)


def shot_lotus():
    """Heart-lotus with a radiant point of light (the atma, 'anor aniyan')."""
    ground((0.02, 0.02, 0.04), 0.1, 80)
    pet = mat("petal", (0.95, 0.55, 0.6), 0, 0.45, (1.0, 0.45, 0.4), 0.6)
    for ring, (n, r, tilt, s) in enumerate([(8, 0.9, 0.35, 1.0), (12, 1.4, 0.75, 1.15), (16, 1.9, 1.15, 1.25)]):
        for i in range(n):
            a = 2 * math.pi * (i + 0.5 * ring) / n
            bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1)
            o = bpy.context.object
            o.scale = (0.32 * s, 0.1 * s, 0.85 * s)
            o.location = (math.cos(a) * r, math.sin(a) * r, 0.55 - ring * 0.12)
            o.rotation_euler = (0, tilt, a)
            o.rotation_euler = Vector((math.cos(a) * math.sin(tilt), math.sin(a) * math.sin(tilt), math.cos(tilt))).to_track_quat("Z", "X").to_euler()
            smooth(assign(o, pet))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(0, 0, 1.0))
    smooth(assign(bpy.context.object, mat("orb", (1, 0.9, 0.7), 0, 0.2, (1, 0.85, 0.55), 60)))
    light("POINT", (0, 0, 1.25), 400, (1, 0.8, 0.5), 0.2)
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, -0.1))
    assign(bpy.context.object, mat("pond", (0.01, 0.02, 0.05), 0.3, 0.04))
    c = cam((0, -11, 4.2), (0, 0, 0.3), 50)
    c.data.dof.use_dof = True
    c.data.dof.focus_distance = 11.8
    c.data.dof.aperture_fstop = 2.8
    bg.inputs[0].default_value = (0.01, 0.01, 0.025, 1)


def shot_razor():
    """'kshurasya dhara': a thin glowing blade-path across a dark abyss into far light."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 40, 0))
    o = bpy.context.object
    o.scale = (0.06, 80, 1.2)
    o.location = (0, 40, -0.6)
    assign(o, mat("blade", (0.85, 0.85, 0.9), 1.0, 0.08))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 40, 0.01))
    e = bpy.context.object
    e.scale = (0.012, 80, 0.02)
    assign(e, mat("edge", (1, 0.85, 0.6), 0, 0.2, (1, 0.8, 0.5), 25))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=2.5, location=(0, 95, 3.5))
    assign(bpy.context.object, mat("sun", (1, 0.8, 0.5), 0, 0.5, (1, 0.75, 0.45), 30))
    # traveller silhouette (boy with topknot), tiny on the edge
    bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.7, location=(0, 6, 0.36))
    sil = mat("sil", (0, 0, 0), 0, 1)
    assign(bpy.context.object, sil)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(0, 6, 0.83))
    assign(bpy.context.object, sil)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(0, 6.02, 0.98))
    assign(bpy.context.object, sil)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.01, 0.015, 1)
    vol = bpy.data.materials.new("fog")
    vol.use_nodes = True
    nt = vol.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    v = nt.nodes.new("ShaderNodeVolumePrincipled")
    v.inputs["Density"].default_value = 0.012
    v.inputs["Color"].default_value = (0.9, 0.6, 0.45, 1)
    nt.links.new(v.outputs[0], nt.nodes["Material Output"].inputs["Volume"])
    bpy.ops.mesh.primitive_cube_add(size=200, location=(0, 50, 0))
    assign(bpy.context.object, vol)
    cam((0.0, -3.0, 2.6), (0, 30, 0.2), 35)
    sc.cycles.volume_step_rate = 4


def shot_diya_ring():
    """Bhoot Chaturdashi: fourteen lit diyas in a ring on dark stone, seen from a high three-quarter angle."""
    ground((0.07, 0.05, 0.05), 0.5)
    for i in range(14):
        a = 2 * math.pi * i / 14
        diya(math.cos(a) * 4.2 - 0.5, math.sin(a) * 4.2, True, 0.55)
    c = cam((0, -9.5, 9.0), (0, 0.4, 0), 40)
    bg.inputs[0].default_value = (0.02, 0.015, 0.03, 1)


def shot_threshold():
    """Chhoti Diwali at the doorstep: a carved wooden door frame, a stone step and five lit diyas."""
    ground((0.12, 0.06, 0.04), 0.7)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 1.2, -0.3))
    st = bpy.context.object
    st.scale = (7, 1.6, 0.3)
    assign(st, mat("step", (0.35, 0.3, 0.27), 0, 0.8))
    wood = mat("wood", (0.25, 0.1, 0.04), 0, 0.55)
    for x in (-2.6, 2.6):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 2.3, 2.4))
        o = bpy.context.object
        o.scale = (0.5, 0.5, 5.4)
        assign(o, wood)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 2.3, 5.2))
    o = bpy.context.object
    o.scale = (5.8, 0.6, 0.6)
    assign(o, wood)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 2.6, 2.4))
    o = bpy.context.object
    o.scale = (4.7, 0.1, 5.4)
    assign(o, mat("door", (0.16, 0.06, 0.03), 0, 0.6))
    for i in range(5):
        diya(-2.2 + i * 1.1 - 0.4, 1.0, True, 0.42, z=0.0)
    cam((0.3, -6.5, 1.5), (0, 1.8, 1.6), 38)
    bg.inputs[0].default_value = (0.015, 0.01, 0.02, 1)
    light("AREA", (0, -2, 6), 60, (1, 0.6, 0.4), 6)


def _mala(fallen=False):
    """A divine flower garland: a closed loop of marigold-like blossoms with a few white flowers and leaves."""
    rng = random.Random(3)
    marigold = mat("marigold", (1.0, 0.45, 0.02), 0, 0.6, (1.0, 0.35, 0.0), 0.0 if fallen else 0.6)
    white = mat("jasmine", (0.95, 0.93, 0.85), 0, 0.5)
    leaf = mat("leaf", (0.05, 0.28, 0.06), 0, 0.5)
    n = 60
    for i in range(n):
        a = 2 * math.pi * i / n
        if fallen:   # crumpled loop lying on the ground
            r = 1.6 + 0.35 * math.sin(a * 3 + 0.7)
            x, y, z = math.cos(a) * r, math.sin(a) * r * 0.8, -0.3
        else:        # hanging U-shaped loop in the air
            x, y, z = math.sin(a) * 1.5, 0, -math.cos(a) * 2.2 + 0.4 * math.cos(2 * a)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.2, location=(x, y, z))
        o = bpy.context.object
        o.scale = (1, 1, 0.8)
        o.rotation_euler = (rng.random() * 3, rng.random() * 3, rng.random() * 3)
        o.modifiers.new("disp", "DISPLACE").strength = 0.06
        assign(o, white if i % 10 == 0 else marigold)
        if i % 5 == 2:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(x * 1.1, y - 0.12, z))
            lf = bpy.context.object
            lf.scale = (0.4, 1.4, 0.15)
            assign(lf, leaf)


def shot_mala():
    """Durvasa's divine garland, glowing in the air."""
    _mala(False)
    for k in range(18):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(random.uniform(-2.5, 2.5), random.uniform(-1, 1), random.uniform(-3, 3)))
        assign(bpy.context.object, mat("spark", (1, 0.9, 0.6), 0, 0.5, (1, 0.85, 0.5), 30))
    cam((0, -9, -0.6), (0, 0, -0.6), 45)
    light("AREA", (-3, -5, 4), 500, (1, 0.85, 0.7), 4)
    light("POINT", (0, 1.5, -0.5), 200, (1, 0.6, 0.2), 1)
    bg.inputs[0].default_value = (0.08, 0.04, 0.10, 1)


def shot_mala_fallen():
    """The same garland thrown to the ground: dull light, dust."""
    ground((0.16, 0.12, 0.10), 0.95)
    _mala(True)
    cam((0, -6.5, 4.2), (0, 0.3, -0.3), 40)
    light("AREA", (4, -2, 6), 160, (0.7, 0.75, 0.9), 5)
    bg.inputs[0].default_value = (0.03, 0.03, 0.04, 1)


def _arjuna_tree(x, tilt=0.0):
    bark = mat("bark", (0.42, 0.36, 0.30), 0, 0.85)
    leaf = mat("foliage", (0.07, 0.25, 0.06), 0, 0.7)
    root = bpy.data.objects.new("root", None)
    sc.collection.objects.link(root)
    root.location = (x, 0, -0.45)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.55, radius2=0.32, depth=7, location=(0, 0, 3.5))
    t = bpy.context.object
    assign(t, bark)
    t.parent = root
    rng = random.Random(int(x * 10) + 5)
    for k in range(14):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=rng.uniform(1.0, 1.6),
                                              location=(rng.uniform(-1.6, 1.6), rng.uniform(-1.2, 1.2), rng.uniform(6.2, 8.6)))
        f = bpy.context.object
        assign(f, leaf)
        f.parent = root
    if tilt:
        for k in range(7):   # exposed roots
            a = 2 * math.pi * k / 7
            bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.16, depth=1.8,
                                            location=(math.cos(a) * 0.5, math.sin(a) * 0.5, -0.4),
                                            rotation=(math.pi + math.sin(a) * 0.6, math.cos(a) * 0.6, 0))
            r = bpy.context.object
            assign(r, bark)
            r.parent = root
    root.rotation_euler = (0, tilt, 0)


def _okhli(x, z=0.0):
    wood = mat("okhli", (0.30, 0.14, 0.05), 0, 0.6)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.45, depth=0.9, location=(x, -0.2, z))
    assign(bpy.context.object, wood)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.47, minor_radius=0.04, location=(x, -0.2, z + 0.1))
    assign(bpy.context.object, mat("rope", (0.75, 0.6, 0.35), 0, 0.9))


def shot_trees():
    """Gokul courtyard: the twin arjuna trees standing close, the okhli (wooden mortar) between them."""
    ground((0.30, 0.20, 0.12), 0.9, 80)
    _arjuna_tree(-1.3)
    _arjuna_tree(1.3)
    _okhli(0, -0.05)
    cam((0, -14, 3.5), (0, 0, 4.2), 35)
    light("SUN", (0, 0, 10), 3.5, (1, 0.88, 0.7), rot=(0.7, 0.3, 0.4))
    bg.inputs[0].default_value = (0.55, 0.62, 0.75, 1)


def shot_trees_fallen():
    """The same two trees pulled out by the roots, falling apart; the okhli stuck between the trunks."""
    ground((0.30, 0.20, 0.12), 0.9, 80)
    _arjuna_tree(-1.4, -0.75)
    _arjuna_tree(1.4, 0.75)
    _okhli(0, 0.0)
    for k in range(40):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.05, 0.18),
                                              location=(random.uniform(-2.5, 2.5), random.uniform(-1, 1), random.uniform(-0.3, 1.5)))
        assign(bpy.context.object, mat("dirt", (0.25, 0.16, 0.08), 0, 1))
    cam((0, -14, 3.0), (0, 0, 3.0), 35)
    light("SUN", (0, 0, 10), 3.5, (1, 0.85, 0.65), rot=(0.7, -0.3, 0.4))
    bg.inputs[0].default_value = (0.5, 0.55, 0.68, 1)


def _steps(lit):
    stone = mat("stone", (0.32, 0.27, 0.24), 0, 0.85)
    for k in range(3):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, k * 1.6, -0.45 + k * 0.7 + 0.35))
        o = bpy.context.object
        o.scale = (5, 1.6, 0.7 + k * 1.4)
        o.location.z = -0.45 + (0.7 + k * 1.4) / 2
        assign(o, stone)
    for k in range(3):
        diya(-0.5, k * 1.6, lit=k < lit, scale=0.55, z=-0.45 + 0.7 + k * 1.4 + 0.05)
    light("AREA", (3, -4, 5), 40, (0.6, 0.6, 0.9), 6)


def shot_steps1():
    _steps(1); cam((0.6, -7.5, 2.0), (0, 1.6, 1.4), 38); bg.inputs[0].default_value = (0.01, 0.01, 0.02, 1)


def shot_steps2():
    _steps(2); cam((0.6, -7.5, 2.0), (0, 1.6, 1.4), 38); bg.inputs[0].default_value = (0.01, 0.01, 0.02, 1)


def shot_steps3():
    _steps(3); cam((0.6, -7.5, 2.0), (0, 1.6, 1.4), 38); bg.inputs[0].default_value = (0.01, 0.01, 0.02, 1)


{"mala": shot_mala, "mala_fallen": shot_mala_fallen, "trees": shot_trees, "trees_fallen": shot_trees_fallen, "steps1": shot_steps1, "steps2": shot_steps2, "steps3": shot_steps3, "diyas2": shot_diyas2, "diya_ring": shot_diya_ring, "threshold": shot_threshold, "diyas_close": shot_diyas_close, "chakra": shot_chakra, "fort": shot_fort,
 "kundal": shot_kundal, "lotus": shot_lotus, "razor": shot_razor}[SHOT]()
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("RENDERED", OUT)

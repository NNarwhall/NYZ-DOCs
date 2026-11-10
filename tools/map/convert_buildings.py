"""Turns NYC City Planning's 3D building model (Rhino .3dm files, one per community district) into NYZ's building list and
grey tile meshes for Unreal (GDD section 5, city buildings; section 24 milestone 1). Run with QGIS's Python, which has
osgeo, numpy, shapely and rhino3dm (installed 2026-11-10):

  "C:\\Program Files\\QGIS 4.2.2\\bin\\o4w_env.bat" && python "C:\\Game Dev Folder\\NYZ\\tools\\map\\convert_buildings.py" [district.3dm ...]

With no files given it converts every NYC_3DModel_*.3dm in RHINO_DIR. Files can also be the district zips as
downloaded (https://www.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc-3d-model/nyc_3dmodel_<district>.zip,
e.g. mn02): each is unpacked, converted and the unpacked file deleted. Run with python -P when reading downloads (the
script's and the current folder stay off the import path). For each district it writes to terrain/buildings/:
  <district>.json  the building list, kept for the city-building tool: per building an ID, its footprint, base and top
                   heights, and where its faces sit in the tile meshes (cm, the map's Unreal coordinates: +X east,
                   +Y south, Z above sea level).
  <district>.nyzb  the faces, merged into 250 m tiles, for the game repo's Tools/import_buildings.py.
The files are in New York's Long Island state-plane coordinates in US feet (EPSG 2263), heights above sea level like the
terrain's. Wall bottoms are pushed 0.5 m into the terrain where it dips below them (the model's ground is flat per
building; ours is the 2017 survey). Buildings on the grey test block (NYZ/Tools/build_test_block.py) are left out and
marked, until the test block is retired.
"""
import glob
import json
import pathlib
import shutil
import struct
import sys
import time
import zipfile

import numpy as np
import rhino3dm
import shapely
from osgeo import osr

osr.UseExceptions()
ROOT = pathlib.Path(__file__).resolve().parents[2]
RHINO_DIR = pathlib.Path(r"C:\Game Dev Folder\Rhino Files")
OUT = ROOT / "terrain/buildings"
TERRAIN = json.loads((ROOT / "terrain/NYZ_terrain.json").read_text(encoding="utf-8"))
TILE = 25000          # cm: 250 m tiles, one mesh and one map object each
FT = 30.480061        # cm per US survey foot
SINK = 50             # cm below the terrain for wall bottoms
FIND_WALL = 300       # cm: a wall or roof belongs to the nearest footprint within this
FEET_PER_UNIT = {rhino3dm.UnitSystem.Feet: 1.0, rhino3dm.UnitSystem.Inches: 1 / 12, rhino3dm.UnitSystem.Millimeters: 1 / 304.8,
                 rhino3dm.UnitSystem.Centimeters: 1 / 30.48, rhino3dm.UnitSystem.Meters: 1 / 0.3048}
def layer_kind(path):
    """What a layer under Buildings holds, by keyword: the files name them differently ("Facade Surface" in MN03,
    "Building Facade Surface" in BX03, "Surface_Facade" in QN12; outlines "Building_Facade"). Surfaces are the faces,
    the others their outlines."""
    top, _, name = path.lower().partition("::")
    if top != "buildings":
        return None
    part = "footprint" if "footprint" in name else "roof" if "roof" in name else "wall" if "facade" in name else None
    if part is None:
        return None
    surface = "surface" in name
    return {"footprint": ("footprint surface", "footprint"), "roof": ("roof", "roof outline"), "wall": ("wall", "wall outline")}[part][0 if surface else 1]


def curve_points(g):
    """A closed outline's corner points: polylines directly, other curves (QN12's PolyCurves) as a polyline if they are
    one, else sampled."""
    if isinstance(g, rhino3dm.PolylineCurve):
        return [g.Point(i) for i in range(g.PointCount)]
    poly = g.TryGetPolyline() if hasattr(g, "TryGetPolyline") else None
    if poly:
        return [poly[i] for i in range(len(poly))]
    t0, t1 = g.Domain.T0, g.Domain.T1
    return [g.PointAt(t0 + (t1 - t0) * k / 64) for k in range(65)]

LOC, SCALE = TERRAIN["unreal_location_cm"], TERRAIN["unreal_scale"]
VX, VY = TERRAIN["size_points"]
E0, N0 = TERRAIN["world_origin_utm18n_m"]["easting"], TERRAIN["world_origin_utm18n_m"]["northing"]
HEIGHTS = np.memmap(ROOT / "terrain/NYZ_terrain.r16", dtype="<u2", mode="r", shape=(VY, VX))


def ground(x, y):
    """Terrain height (cm) at Unreal x, y (arrays), nearest grid point."""
    col = np.clip(np.rint((x - LOC["x"]) / SCALE["x"]).astype(int), 0, VX - 1)
    row = np.clip(np.rint((y - LOC["y"]) / SCALE["y"]).astype(int), 0, VY - 1)
    return (HEIGHTS[row, col].astype(np.float64) - 32768) * SCALE["z"] / 128 + LOC["z"]


src, dst = osr.SpatialReference(), osr.SpatialReference()
src.ImportFromEPSG(2263)
dst.ImportFromEPSG(32618)  # UTM 18N, as the terrain
for sr in (src, dst):
    sr.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
TO_UTM = osr.CoordinateTransformation(src, dst)


def to_unreal(xyz_ft):
    """N x 3 feet (state plane) -> N x 3 cm (Unreal)."""
    utm = np.array(TO_UTM.TransformPoints(xyz_ft[:, :2].tolist()))
    return np.column_stack(((utm[:, 0] - E0) * 100, -(utm[:, 1] - N0) * 100, xyz_ft[:, 2] * FT))


def map_border():
    """The map's border polygon (the first feature of docs/map/border-draft.geojson, lon/lat) in Unreal cm."""
    g = json.loads((ROOT / "docs/map/border-draft.geojson").read_text(encoding="utf-8"))
    poly = next(f for f in g["features"] if f["geometry"]["type"] == "Polygon")
    wgs = osr.SpatialReference()
    wgs.ImportFromEPSG(4326)
    wgs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    to_utm = osr.CoordinateTransformation(wgs, dst)
    rings = [[((e - E0) * 100, -(n - N0) * 100) for e, n, *_ in to_utm.TransformPoints([tuple(p[:2]) for p in ring])]
             for ring in poly["geometry"]["coordinates"]]
    border = shapely.Polygon(rings[0], rings[1:])
    shapely.prepare(border)
    return border


def test_block_areas():
    """The grey test block and its copies (build_test_block.py: a 2 x 2 grid 300 m apart, the real block at 1,1)."""
    data = json.loads((ROOT / "NYZ/Tools/data/test_block.json").read_text(encoding="utf-8"))
    x0, y0, x1, y1 = data["bounds_cm"]
    m = 1000
    return [shapely.box(x0 + ox - m, y0 + oy - m, x1 + ox + m, y1 + oy + m) for ox in (-30000, 0) for oy in (-30000, 0)]


def outline_faces(rings):
    """Faces from wall and roof outlines (closed polylines, feet), for district files saved without meshes. Each outline
    is a flat polygon, triangulated in its own plane; a flat roof outline inside a bigger one at the same height is a
    courtyard in it. Yields (kind, points, triangles)."""
    for kind, curves in rings.items():
        polys = [np.array(c[:-1] if c[0] == c[-1] else c, dtype=np.float64) for c in curves if len(c) >= 4]
        holes, is_hole = {}, set()
        if kind == "roof":
            flat = [i for i, p in enumerate(polys) if np.ptp(p[:, 2]) < 0.1]
            shapes = [shapely.Polygon(polys[i][:, :2]) for i in flat]
            areas = shapely.area(shapes)
            tree = shapely.STRtree(shapes)
            for k, i in enumerate(flat):
                inside = [j for j in tree.query(shapes[k], predicate="within")
                          if j != k and areas[j] > areas[k] and abs(polys[flat[j]][0, 2] - polys[i][0, 2]) < 0.5]
                if inside:
                    holes.setdefault(flat[min(inside, key=lambda j: areas[j])], []).append(i)
                    is_hole.add(i)
        for i, outer in enumerate(polys):
            if i in is_hole:
                continue
            inner = [polys[h] for h in holes.get(i, [])]
            if len(outer) == 4 and not inner:  # most walls: a rectangle
                yield kind, outer, [(0, 1, 2), (0, 2, 3)]
                continue
            a, b = outer, np.roll(outer, -1, 0)
            normal = np.array([((a[:, 1] - b[:, 1]) * (a[:, 2] + b[:, 2])).sum(), ((a[:, 2] - b[:, 2]) * (a[:, 0] + b[:, 0])).sum(),
                               ((a[:, 0] - b[:, 0]) * (a[:, 1] + b[:, 1])).sum()])
            keep = [ax for ax in range(3) if ax != int(np.argmax(np.abs(normal)))]  # flatten along the polygon's facing
            points = np.vstack([outer] + inner)
            index = {tuple(np.round(p[keep], 4)): n for n, p in enumerate(points)}
            try:
                cdt = shapely.constrained_delaunay_triangles(shapely.Polygon(outer[:, keep], [h[:, keep] for h in inner]))
                triangles = [tuple(index[tuple(np.round(c, 4))] for c in np.asarray(t.exterior.coords)[:3]) for t in shapely.get_parts(cdt)]
            except (KeyError, shapely.errors.GEOSException):
                points, triangles = outer, [(0, n, n + 1) for n in range(1, len(outer) - 1)]  # a fan: fine for the convex ones
            if triangles:
                yield kind, points, triangles


def convert(path):
    start = time.time()
    district = path.stem.replace("NYC_3DModel_", "")
    f = rhino3dm.File3dm.Read(str(path))
    assert f is not None, f"could not read {path}"
    kind_of = {layer.Index: layer_kind(layer.FullPath) for layer in f.Layers}
    # Most files are in feet; some were saved in other units (MN06: millimetres, Rhino's feet being 304.8 mm).
    unit = FEET_PER_UNIT.get(f.Settings.ModelUnitSystem)
    assert unit, f"{path.name}: unexpected units {f.Settings.ModelUnitSystem}"
    pt = lambda p: (p.X * unit, p.Y * unit, p.Z * unit)  # noqa: E731

    outlines, verts, tris, face_first, face_kind = [], [], [], [0], []
    rings = {"roof": [], "wall": []}  # wall and roof outlines, for files saved without meshes
    footprint_meshes, footprint_surfaces = [], 0
    base = breps = 0
    for obj in f.Objects:
        kind, g = kind_of.get(obj.Attributes.LayerIndex), obj.Geometry
        if kind == "footprint" and isinstance(g, rhino3dm.Curve):
            outlines.append([pt(p) for p in curve_points(g)])
        elif kind == "footprint surface" and isinstance(g, rhino3dm.Brep):
            footprint_surfaces += 1
            m = g.Faces[0].GetMesh(rhino3dm.MeshType.Any)
            if m is not None:
                points = [pt(p) for p in m.Vertices.ToPoint3dArray()]
                footprint_meshes.append((points, [m.Faces[i] for i in range(len(m.Faces))]))
        elif kind in ("roof outline", "wall outline") and isinstance(g, rhino3dm.Curve):
            rings[kind.split()[0]].append([pt(p) for p in curve_points(g)])
        elif kind in ("roof", "wall") and isinstance(g, rhino3dm.Brep):
            breps += 1
            for face in g.Faces:
                m = face.GetMesh(rhino3dm.MeshType.Any)
                if m is None:
                    continue
                points = [pt(p) for p in m.Vertices.ToPoint3dArray()]
                verts.append(points)
                for a, b, c, d in (m.Faces[i] for i in range(len(m.Faces))):
                    tris.append((base + a, base + b, base + c))
                    if c != d:
                        tris.append((base + a, base + c, base + d))
                base += len(points)
                face_first.append(len(tris))
                face_kind.append(kind)
    meshed = len(face_kind) / max(breps, 1)
    # Stored meshes only when nearly every face has one: files saved without (MN06, BX03) or with some (BK04: faces
    # without one were silently lost) get all their faces from the outlines instead, which every file has.
    if meshed < 0.99:
        verts, tris, face_first, face_kind, base = [], [], [0], [], 0
        for kind, points, triangles in outline_faces(rings):
            tris.extend(tuple(base + i for i in t) for t in triangles)
            verts.append(points)
            base += len(points)
            face_first.append(len(tris))
            face_kind.append(kind)
    # Only when nearly every footprint surface has a mesh (BK10's mostly don't, and its outlines are fine).
    if len(footprint_meshes) > 0.9 * footprint_surfaces and abs(len(outlines) - footprint_surfaces) > 0.1 * footprint_surfaces:
        # The outline layer holds something else (QN01: wall outlines) or misses some (QN12): footprints from the
        # footprint surfaces instead.
        outlines = []
        for points, faces in footprint_meshes:
            shape = shapely.union_all([shapely.Polygon([points[i][:2] for i in (a, b, c, d)] if c != d else [points[i][:2] for i in (a, b, c)])
                                       for a, b, c, d in faces])
            shape = max(shapely.get_parts(shape), key=lambda p: p.area) if shape.geom_type != "Polygon" else shape
            if shape.is_empty or shape.geom_type != "Polygon":
                continue
            z = min(p[2] for p in points)
            outlines.append([(x, y, z) for x, y in shape.exterior.coords])
    # A footprint needs three corners (BK11 has some that don't).
    outlines = [o for o in outlines if len({(round(p[0], 2), round(p[1], 2)) for p in o}) >= 3]
    read_s = time.time() - start
    assert outlines and face_kind, f"{path.name}: no footprints or faces on the expected layers"

    v = to_unreal(np.array([p for face in verts for p in face], dtype=np.float64))
    tris = np.array(tris, dtype=np.int64)
    face_first = np.array(face_first)
    nface = len(face_kind)
    face_of_tri = np.repeat(np.arange(nface), np.diff(face_first))
    face_vstart = np.cumsum([0] + [len(fv) for fv in verts])

    # Wall bottoms into the ground: each wall's lowest vertices go to 0.5 m under the terrain where that's lower.
    face_of_vert = np.repeat(np.arange(nface), np.diff(face_vstart))
    is_wall = np.array([k == "wall" for k in face_kind])
    face_min = np.minimum.reduceat(v[:, 2], face_vstart[:-1])
    bottom = is_wall[face_of_vert] & (v[:, 2] <= face_min[face_of_vert] + 1)
    v[bottom, 2] = np.minimum(v[bottom, 2], ground(v[bottom, 0], v[bottom, 1]) - SINK)

    # Buildings: footprints, and each face to the nearest footprint (walls sit on its edge, roofs over it).
    feet = [np.array(o, dtype=np.float64) for o in outlines]
    rings = [to_unreal(o) for o in feet]
    polys = [shapely.Polygon(r[:, :2]) for r in rings]
    tree = shapely.STRtree(polys)
    centres = np.column_stack((np.add.reduceat(v[:, 0], face_vstart[:-1]), np.add.reduceat(v[:, 1], face_vstart[:-1])))
    centres /= np.diff(face_vstart)[:, None]
    pairs = tree.query_nearest(shapely.points(centres), max_distance=FIND_WALL, all_matches=False)
    owner = np.full(nface, -1)
    owner[pairs[0]] = pairs[1]

    # Left out: the grey test block's areas, and anything outside the map border (docs/map/border-draft.geojson).
    border = map_border()

    def off_map(c):
        return not shapely.contains_xy(border, c[0], c[1])

    blocked = test_block_areas()
    middle = np.array([[p.centroid.x, p.centroid.y] for p in polys])
    outside = ~shapely.contains_xy(border, middle[:, 0], middle[:, 1])
    # A wrong unit puts a district hundreds of km away (MN06 in millimetres read as feet); districts at the map's edge
    # are partly outside it for real (QN13), which the border handles.
    far = np.abs(middle).max(axis=1) > 10_000_000  # 100 km from the map's middle
    assert far.mean() < 0.5, f"{path.name}: {far.mean():.0%} of buildings land over 100 km away: wrong units or coordinates?"
    in_block = np.array([any(a.contains(shapely.Point(c)) for a in blocked) for c in middle])
    skip = in_block | outside
    loose_skip = np.array([off_map(c) or any(a.contains(shapely.Point(c)) for a in blocked) for c in centres[owner < 0]]) if (owner < 0).any() else []
    keep_face = np.ones(nface, bool)
    keep_face[owner >= 0] = ~skip[owner[owner >= 0]]
    keep_face[np.flatnonzero(owner < 0)[np.asarray(loose_skip, bool)]] = False

    # Tiles by building centre (loose faces by their own centre); faces sorted by tile, then building.
    fx = np.where(owner >= 0, middle[np.maximum(owner, 0), 0], centres[:, 0])
    fy = np.where(owner >= 0, middle[np.maximum(owner, 0), 1], centres[:, 1])
    tx, ty = np.floor(fx / TILE).astype(int), np.floor(fy / TILE).astype(int)
    order = np.lexsort((owner, ty, tx))
    order = order[keep_face[order]]

    buildings = [{"id": f"{district}-{i}", "footprint_cm": np.round(r[:, :2]).astype(int).tolist(), "base_cm": round(float(r[0, 2]))}
                 for i, r in enumerate(rings)]
    for i in np.flatnonzero(skip):
        buildings[i]["skipped"] = "off the map" if outside[i] else "test block"

    OUT.mkdir(parents=True, exist_ok=True)
    if not len(order):  # a district wholly outside the border (most of Staten Island)
        for old in OUT.glob(f"{district}.*"):
            old.unlink()
        print(f"{district}: {len(buildings)} buildings, all outside the map border: nothing written")
        return
    tiles, total_tris = 0, 0
    with open(OUT / f"{district}.nyzb", "wb") as out:
        out.write(b"NYZB" + struct.pack("<II", 1, 0))
        groups = np.split(order, np.flatnonzero(np.diff(tx[order] * 100000 + ty[order])) + 1) if len(order) else []
        for faces in groups:
            ctx, cty = int(tx[faces[0]]), int(ty[faces[0]])
            centre = np.array([(ctx + 0.5) * TILE, (cty + 0.5) * TILE, 0.0])
            tri_rows = np.concatenate([np.arange(face_first[k], face_first[k + 1]) for k in faces])
            used = np.unique(tris[tri_rows])
            remap = np.full(len(v), -1)
            remap[used] = np.arange(len(used))
            local_tris = remap[tris[tri_rows]]
            out.write(struct.pack("<iiII", ctx, cty, len(used), len(local_tris)))
            out.write((v[used] - centre).astype("<f4").tobytes())
            out.write(local_tris.astype("<u4").tobytes())
            # Where each building's faces sit in this tile's mesh, for the city tool.
            counts = np.diff(face_first)[faces]
            first = np.concatenate(([0], np.cumsum(counts)[:-1]))
            for b in np.unique(owner[faces]):
                if b < 0:
                    continue
                sel = owner[faces] == b
                rec = buildings[b]
                rec["tile"] = [ctx, cty]
                rec["tris"] = [int(first[sel][0]), int(counts[sel].sum())]
                rec["top_cm"] = round(float(v[np.concatenate([np.arange(face_vstart[k], face_vstart[k + 1]) for k in faces[sel]]), 2].max()))
            tiles += 1
            total_tris += len(local_tris)
        out.seek(8)
        out.write(struct.pack("<I", tiles))

    loose = int((owner < 0).sum())
    (OUT / f"{district}.json").write_text(json.dumps({
        "district": district, "source": path.name + " (NYC City Planning 3D model, 2014 buildings)",
        "units": "cm, Unreal map coordinates: +X east, +Y south, Z above sea level", "tile_size_cm": TILE,
        "faces_not_matched_to_a_footprint": loose, "buildings": buildings}), encoding="utf-8")

    in_tiles = sum(1 for b in buildings if "tile" in b)
    assert in_tiles >= 0.9 * (len(buildings) - skip.sum()), f"only {in_tiles} of {len(buildings)} buildings got faces"
    print(f"{district}: {len(buildings)} buildings ({int(in_block.sum())} left out for the test block, {int(outside.sum())} off the map, {len(buildings) - in_tiles - int(skip.sum())} "
          f"without faces), {nface} faces ({loose} not matched to a footprint), {tiles} tiles, {total_tris:,} triangles; "
          f"faces from {'stored meshes' if meshed >= 0.99 else f'outlines ({meshed:.0%} meshed)'}; read {read_s:.0f} s, total {time.time() - start:.0f} s")


def convert_zip(path):
    """A district zip as downloaded from NYC Planning: its one .3dm is unpacked, converted and deleted again
    (about 6 times the zip's size unpacked; the whole city's would be about 50 GB)."""
    with zipfile.ZipFile(path) as z:
        members = [m for m in z.namelist() if m.lower().endswith(".3dm")]
        assert len(members) == 1, f"{path.name}: expected one .3dm inside, found {members}"
        tmp = OUT / "unzipped"
        tmp.mkdir(parents=True, exist_ok=True)
        target = tmp / pathlib.PurePath(members[0]).name  # its name only: nothing written outside tmp
        with z.open(members[0]) as src, open(target, "wb") as dst:
            shutil.copyfileobj(src, dst, 16 << 20)
    try:
        convert(target)
    finally:
        target.unlink()


if __name__ == "__main__":
    files = [pathlib.Path(p) for p in sys.argv[1:]] or [pathlib.Path(p) for p in sorted(glob.glob(str(RHINO_DIR / "NYC_3DModel_*.3dm")))
                                                          if "_EXPORT" not in p]
    for p in files:
        convert_zip(p) if p.suffix.lower() == ".zip" else convert(p)

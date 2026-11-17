"""Turns the streets in NYC City Planning's district files (the same Rhino .3dm files as the buildings) into grey street
tiles for Unreal (GDD section 24, milestone 2, map stage 1). Run with QGIS's Python, like convert_buildings.py:

  "C:\\Program Files\\QGIS 4.2.2\\bin\\o4w_env.bat" && python "C:\\Game Dev Folder\\NYZ\\tools\\map\\convert_streets.py" [district.3dm or .zip ...]

With no files given it converts every NYC_3DModel_*.3dm in the Rhino folder. What the files hold (MN03, 2026-11-14):
road outlines, one per stretch between intersections and one per intersection, at a dummy height; streets on a
district's edge cut down the middle, their road left as open lines; sidewalk outlines that are whole blocks at the curb.
From them:
  roads      the road outlines, open half-roads closed along the district line: a look-only skin 1 cm above the
             terrain, on the terrain's own 2 m triangles, so you stand on the terrain and feet clip at most 1 cm.
  sidewalks  each block minus the lots lying mostly inside the blocks (plus islands inside the road and medians drawn only
             as park outlines over it; a 3 m sidewalk where a lot runs right to the curb; on to a building's wall where
             it stops short by under 2 m; never inside a building or across a road), 15 cm above the road, in 10 m
             pieces: solid. Gaps left in the street (thin medians, median tips, leftover corners) are filled as road.
  curbs      every sidewalk edge not against a wall, a face from its top down into the ground: look-only.
  street     curb ramps (solid, in the sidewalk), tree pits with placeholder trees from the 2015 tree census (trunk
  detail     posts solid), cellar doors at every other building (look-only steel plates on the sidewalk); around the test
             block, the showcase street's paint and placeholder props (street_props.py).
Before building them it smooths the ground under the streets (street_bed.py: terrain/NYZ_terrain.r16; the game repo's
Tools/update_terrain.py puts it into the map, before Tools/import_streets.py). Writes to terrain/streets/:
  <district>.nyzs  the tiles (500 m; the buildings' are 250 m) for the game repo's Tools/import_streets.py.
  <district>.json  each road piece and block with an ID and outline (cm, Unreal map coordinates), for the street tool
                   (GDD section 5).
  <district>_issues.json and .png  what the street checks found (curbs with no sidewalk, terrain showing in the street,
                   raised islands joining two blocks, specks of sidewalk, gaps between sidewalk and building), numbered on a map of
                   the district.
"""
import glob
import json
import pathlib
import struct
import sys
import time

import numpy as np
import rhino3dm
import shapely

import convert_buildings as cb  # the map's coordinates, terrain, border and test block

OUT = cb.ROOT / "terrain/streets"
TILE = 50000                        # cm: 500 m street tiles (a quarter as many objects as the buildings' 250 m: each
                                    # costs the server memory, 2026-11-15)
ROAD_UP, WALK_UP, SINK = 1, 16, 10  # cm: road skin and sidewalk above the terrain (a 15 cm curb); faces reach SINK below it
STEP, CELL = 200, 1000              # cm: the terrain's grid; sidewalk pieces (5 grid steps, so 25 to a tile)
CLEAR = 12                          # cm: a coarse sidewalk piece coming closer than this to the terrain is made finer
                                    # (at most 4 cm of sag below its 16 cm; 8 showed as dips by walls, 2026-11-15)
EDGE_CLEAR = 2                      # cm: its edges closer than this (steep ground) put its cell on the terrain's triangles
SIMPLIFY = 3                        # cm: outline points within this of a straight line are dropped
WIDEST_HALF = 2500                  # cm: half the width of the widest street a closed half-road can be
BARE_CURB_WALK = 300                # cm: sidewalk given to a curb the city's lots run right up to (MN03's median is 3.2 m)
RAMP_WIDE, RAMP_RUN = 150, 180      # cm: a curb ramp's width and the run it climbs the 15 cm curb in (1 in 12)
TREES = cb.ROOT / "terrain/trees/tree_census_2015.csv"  # NYC Parks' 2015 street tree census (NYC Open Data, uvpi-gqnh)
PIT_LONG, PIT_ACROSS, PIT_FROM_CURB = 180, 120, 25     # cm: a tree pit (4 x 6 ft, long side along the curb), its curb side
GROWN = 1.15                        # trunks thicker than in 2015 (GDD section 5: "grown a little")
POST = 300                          # cm: how high a trunk's collision post reaches (the canopy is look-only)
TO_WALL = 200                       # cm: a gap between the sidewalk and a building narrower than this is sidewalk
DOOR_WIDE, DOOR_OUT, DOOR_FRONT = 120, 150, 500  # cm: a cellar door along the wall, out from it; the street front it needs
KINDS = (("roadbed", "road"), ("sidewalk", "block"), ("lot line", "lot"), ("building footprint", "building"),
         ("parking", None), ("park", "park"), ("open space", "park"), ("community district", "district"))  # parking before park


def layer_kind(path):
    p = path.lower()
    return None if "::name" in p else next((k for key, k in KINDS if key in p), None)


def surface(x, y):
    """The terrain's surface (cm) at Unreal x, y (arrays), on its own triangles: each 2 m square split from its
    north-west to its south-east corner, as Unreal's landscape draws it (LandscapeRender.cpp: i00, i11, i10)."""
    fx, fy = (x - cb.LOC["x"]) / STEP, (y - cb.LOC["y"]) / STEP
    c, r = np.clip(np.floor(fx).astype(int), 0, cb.VX - 2), np.clip(np.floor(fy).astype(int), 0, cb.VY - 2)
    u, v = fx - c, fy - r
    h = lambda rr, cc: (cb.HEIGHTS[rr, cc].astype(np.float64) - 32768) * cb.SCALE["z"] / 128 + cb.LOC["z"]  # noqa: E731
    z00, z10, z01, z11 = h(r, c), h(r, c + 1), h(r + 1, c), h(r + 1, c + 1)
    return np.where(u >= v, z00 + u * (z10 - z00) + v * (z11 - z10), z00 + v * (z01 - z00) + u * (z11 - z01))


def area(geoms):
    """The union of the polygons among geoms (make_valid can also give lines and points)."""
    parts = shapely.get_parts(np.asarray(geoms, dtype=object))
    return shapely.union_all(parts[np.isin(shapely.get_type_id(parts), (3, 6))])


def opening(g, r):
    """g without the parts narrower than 2 r."""
    return shapely.buffer(shapely.buffer(g, -r, join_style="mitre"), r, join_style="mitre")


def segments(g):
    """g's outline as its single segments (linestrings of two points), for an STRtree."""
    pts, ring = shapely.get_coordinates(shapely.get_parts(shapely.boundary(shapely.get_parts(g))), return_index=True)  # one index per ring
    same = ring[1:] == ring[:-1]
    return shapely.linestrings(np.stack((pts[:-1][same], pts[1:][same]), 1))


def edge_share(polys, g, d, step=50):
    """The share of each polygon's outline within d of g's outline, from points every step round it. Measuring the
    outlines against a grown copy of a whole district's g took minutes on the big districts (QN12, 2026-11-16)."""
    xy, owner = shapely.get_coordinates(shapely.segmentize(shapely.boundary(polys), step), return_index=True)
    near = np.zeros(len(xy))
    near[shapely.STRtree(segments(g)).query(shapely.points(xy), predicate="dwithin", distance=d)[0]] = 1
    return np.bincount(owner, near, len(polys)) / np.maximum(np.bincount(owner, minlength=len(polys)), 1)


def boxes(x0, y0, size, n):
    """n x n squares of the given size from x0, y0, row by row, and their corners."""
    gx, gy = np.meshgrid(x0 + size * np.arange(n), y0 + size * np.arange(n))
    gx, gy = gx.ravel(), gy.ravel()
    return shapely.box(gx, gy, gx + size, gy + size), gx, gy


def squares_to_tris(gx, gy, size):
    """Two triangles per square (corner arrays), split north-west to south-east like the terrain: N x 3 x 2."""
    p00, p10, p11, p01 = (np.column_stack((gx + dx, gy + dy)) for dx, dy in ((0, 0), (size, 0), (size, size), (0, size)))
    return np.concatenate((np.stack((p00, p10, p11), 1), np.stack((p00, p11, p01), 1)))


def triangulate(pieces, owners=False):
    """Polygons (any shape) -> N x 3 x 2 triangles (and, with owners, which piece each came from)."""
    parts, owner = shapely.get_parts(pieces, return_index=True)
    keep = (shapely.get_type_id(parts) == 3) & (shapely.area(parts) > 1)
    parts, owner = parts[keep], owner[keep]
    if not len(parts):
        return (np.zeros((0, 3, 2)), np.zeros(0, dtype=int)) if owners else np.zeros((0, 3, 2))
    tris, k = shapely.get_parts(shapely.constrained_delaunay_triangles(parts), return_index=True)
    ok = shapely.area(tris) > 0.01
    tris = shapely.get_coordinates(tris[ok]).reshape(-1, 4, 2)[:, :3]
    return (tris, owner[k[ok]]) if owners else tris


def cut(geom, cells):
    """Which 10 m cells geom covers whole, which partly, and its pieces in the partly covered ones."""
    full = shapely.contains_properly(geom, cells)
    part = shapely.intersects(geom, cells) & ~full
    return full, part, shapely.intersection(geom, cells[part])


def on_terrain(pieces, cx, cy):
    """Pieces of 10 m cells (corners cx, cy) cut along the terrain's own 50 triangles in each, so every bit lies in one."""
    if not len(pieces):
        return np.zeros((0, 3, 2))
    terrain = squares_to_tris(*_grid(cx, cy), STEP)  # all squares' first triangles, then their second
    owner = np.tile(np.repeat(np.arange(len(pieces)), (CELL // STEP) ** 2), 2)
    return triangulate(shapely.intersection(pieces[owner], shapely.polygons(np.concatenate((terrain, terrain[:, :1]), 1))))


def clearance(tris, cx, cy, up=WALK_UP):
    """For flat triangles (N x 3 x 2), each inside the 10 m cell with corner cx, cy, and the sidewalk made from them:
    how far (cm) it stays above the terrain at the terrain's grid points under it, and the one where it comes closest;
    and how far its edges stay above it. The terrain is flat within each of its triangles, so those two are the only
    places the sidewalk can come closest (an edge matters on steep ground, between grid points)."""
    if not len(tris):
        return np.zeros(0), np.zeros((0, 2)), np.zeros(0)
    k = np.arange(CELL // STEP + 1) * STEP
    px = (cx[:, None, None] + k[None, None, :]).repeat(len(k), 1).reshape(len(cx), -1)
    py = (cy[:, None, None] + k[None, :, None]).repeat(len(k), 2).reshape(len(cx), -1)
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    det = (b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (c[:, 0] - a[:, 0]) * (b[:, 1] - a[:, 1])
    u = ((px - a[:, :1]) * (c[:, 1:2] - a[:, 1:2]) - (c[:, :1] - a[:, :1]) * (py - a[:, 1:2])) / det[:, None]
    v = ((b[:, :1] - a[:, :1]) * (py - a[:, 1:2]) - (px - a[:, :1]) * (b[:, 1:2] - a[:, 1:2])) / det[:, None]
    inside = (u >= -1e-6) & (v >= -1e-6) & (u + v <= 1 + 1e-6)
    z = surface(tris[..., 0], tris[..., 1]) + up  # up: one height for all, or one per corner (N x 3)
    inner = np.where(inside, z[:, :1] + u * (z[:, 1:2] - z[:, :1]) + v * (z[:, 2:3] - z[:, :1]) - surface(px, py), np.inf)
    worst = inner.argmin(1)
    rows = np.arange(len(tris))

    # Each edge where it crosses the terrain's grid lines and square diagonals (in grid units: x, y and x - y whole).
    p, q = tris, np.roll(tris, -1, axis=1)
    zp, zq = z, np.roll(z, -1, axis=1)
    g = lambda t: np.stack(((t[..., 0] - cb.LOC["x"]) / STEP, (t[..., 1] - cb.LOC["y"]) / STEP), -1)  # noqa: E731
    gp, gq = g(p), g(q)
    gp, gq = np.concatenate((gp, (gp[..., 0] - gp[..., 1])[..., None]), -1), np.concatenate((gq, (gq[..., 0] - gq[..., 1])[..., None]), -1)
    lines = np.floor(np.minimum(gp, gq))[..., None] + np.arange(1, 2 * CELL // STEP + 2)  # N x 3 edges x 3 kinds x 11
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (lines - gp[..., None]) / (gq - gp)[..., None]
    t = np.where((t > 0) & (t < 1), t, np.nan).reshape(len(tris), 3, -1)
    ex = p[..., 0, None] + t * (q - p)[..., 0, None]
    ey = p[..., 1, None] + t * (q - p)[..., 1, None]
    edge = zp[..., None] + t * (zq - zp)[..., None] - surface(np.nan_to_num(ex), np.nan_to_num(ey))
    edge = np.where(np.isnan(t), np.inf, edge).reshape(len(tris), -1).min(1)
    return inner[rows, worst], np.column_stack((px[rows, worst], py[rows, worst])), edge


def road_skin(geom, cells, gx, gy):
    """The road on the terrain's own triangles: whole 2 m squares where a 10 m cell is all road, cut pieces at the edges."""
    full, part, pieces = cut(geom, cells)
    return np.concatenate((squares_to_tris(*_grid(gx[full], gy[full]), STEP), on_terrain(pieces, gx[part], gy[part])))


def _grid(cx, cy):
    """The 2 m squares' corners inside each 10 m cell (cell corners cx, cy)."""
    k = np.arange(CELL // STEP) * STEP
    sx = (cx[:, None, None] + k[None, None, :]).repeat(len(k), 1)
    sy = (cy[:, None, None] + k[None, :, None]).repeat(len(k), 2)
    return sx.reshape(-1), sy.reshape(-1)


def walk_top(geom, cells, gx, gy):
    """The sidewalk: two triangles per 10 m cell it covers whole, its cut pieces elsewhere. A triangle that comes within
    CLEAR of the terrain (or under it: on MN03 the terrain rises 42 cm over 6 m in places) is split at the terrain point
    closest to it, until none does; splitting inside a triangle keeps its edges, so no cracks open. Where the terrain
    could still rise through between its grid points (steep ground), the whole cell follows the terrain's own triangles."""
    full, part, pieces = cut(geom, cells)
    part_tris, k = triangulate(pieces, owners=True)
    tris = np.concatenate((squares_to_tris(gx[full], gy[full], CELL), part_tris))
    cell = np.concatenate((np.tile(np.flatnonzero(full), 2), np.flatnonzero(part)[k]))
    done, done_cell = [], []
    for _ in range(12):
        gap, worst, _ = clearance(tris, gx[cell], gy[cell])
        bad = gap < CLEAR
        done.append(tris[~bad])
        done_cell.append(cell[~bad])
        if not bad.any():
            break
        t, p, cell = tris[bad], worst[bad], np.tile(cell[bad], 3)
        tris = np.concatenate((np.stack((t[:, 0], t[:, 1], p), 1), np.stack((t[:, 1], t[:, 2], p), 1), np.stack((t[:, 2], t[:, 0], p), 1)))
        e1, e2 = tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]
        keep = np.abs(e1[:, 0] * e2[:, 1] - e1[:, 1] * e2[:, 0]) > 1  # a point on an edge leaves one side empty
        tris, cell = tris[keep], cell[keep]
    else:
        done.append(tris)
        done_cell.append(cell)
    tris, cell = np.concatenate(done), np.concatenate(done_cell)
    steep = np.zeros(len(cells), bool)
    steep[cell[clearance(tris, gx[cell], gy[cell])[2] < EDGE_CLEAR]] = True
    steep_part = steep[part]
    return np.concatenate((tris[~steep[cell]], squares_to_tris(*_grid(gx[full & steep], gy[full & steep]), STEP),
                           on_terrain(pieces[steep_part], gx[part][steep_part], gy[part][steep_part])))


def ramp_top(ramps, road, cells, gx, gy):
    """Curb ramps: flat triangles from road level at the curb to the sidewalk's top RAMP_RUN in (how far in: distance to
    the road). Their corners are on the terrain's surface plus that, so in between the terrain could poke through: such
    a ramp is raised as a whole until it clears by ROAD_UP (MN03: 99% by under 2.3 cm); one that would need more than
    5 cm (rough ground) follows the terrain's own triangles instead. N x 3 x 3."""
    if not len(ramps):
        return np.zeros((0, 3, 3))
    ri, ci = shapely.STRtree(cells).query(ramps, predicate="intersects")
    pieces = shapely.intersection(ramps[ri], cells[ci])
    rise = lambda t: ROAD_UP + (WALK_UP - ROAD_UP) * np.clip(  # noqa: E731
        shapely.distance(shapely.points(t.reshape(-1, 2)), road).reshape(-1, 3) / RAMP_RUN, 0, 1)
    tris, k = triangulate(pieces, owners=True)
    up = rise(tris)
    gap, _, edge = clearance(tris, gx[ci[k]], gy[ci[k]], up)
    raise_by = np.zeros(len(ramps))
    np.maximum.at(raise_by, ri[k], ROAD_UP - np.minimum(gap, edge))
    rough = raise_by > 5
    flat = ~rough[ri[k]]
    exact = on_terrain(pieces[rough[ri]], gx[ci[rough[ri]]], gy[ci[rough[ri]]])
    return np.concatenate((lift(tris[flat], up[flat] + raise_by[ri[k][flat]][:, None]), lift(exact, rise(exact))))


def curb_faces(edges, walk, cells):
    """A face under every sidewalk edge (lines), from its top down into the ground, facing out."""
    lines = shapely.get_parts(shapely.intersection(edges, cells))
    lines = lines[shapely.get_type_id(lines) == 1]
    if not len(lines):
        return np.zeros((0, 3, 3))
    xy, index = shapely.get_coordinates(lines, return_index=True)
    same = index[1:] == index[:-1]
    a, b = xy[:-1][same], xy[1:][same]
    d = b - a
    keep = np.hypot(d[:, 0], d[:, 1]) > 0.5
    a, b, d = a[keep], b[keep], d[keep]
    # Facing out: a point a little to the right of a -> b inside the sidewalk means a -> b runs the other way.
    m = (a + b) / 2 + np.column_stack((d[:, 1], -d[:, 0])) / np.hypot(d[:, 0], d[:, 1])[:, None] * 5
    flip = shapely.contains_xy(walk, m[:, 0], m[:, 1])
    a, b = np.where(flip[:, None], b, a), np.where(flip[:, None], a, b)
    top_a, top_b = surface(a[:, 0], a[:, 1]) + WALK_UP, surface(b[:, 0], b[:, 1]) + WALK_UP
    A_top, B_top = np.column_stack((a, top_a)), np.column_stack((b, top_b))
    A_bot, B_bot = np.column_stack((a, top_a - WALK_UP - SINK)), np.column_stack((b, top_b - WALK_UP - SINK))
    return np.concatenate((np.stack((A_bot, B_bot, B_top), 1), np.stack((A_bot, B_top, A_top), 1)))


def lift(tris2d, up):
    """N x 3 x 2 flat triangles -> N x 3 x 3 on the terrain, up cm above it, all facing up."""
    z = surface(tris2d[..., 0], tris2d[..., 1]) + up
    return face_up(np.concatenate((tris2d, z[..., None]), 2))


def face_up(t):
    """N x 3 x 3 triangles wound to face up."""
    e1, e2 = t[:, 1, :2] - t[:, 0, :2], t[:, 2, :2] - t[:, 0, :2]
    down = e1[:, 0] * e2[:, 1] - e1[:, 1] * e2[:, 0] < 0
    t[down] = t[down][:, [0, 2, 1]]
    return t


def weld(tris, colours=None):
    """N x 3 x 3 triangles (and an sRGB colour each, N x 3; white if none) -> shared vertices (to the mm), their RGBA
    colours and index triples."""
    if not len(tris):
        return np.zeros((0, 3)), np.zeros((0, 4), np.uint8), np.zeros((0, 3), dtype=np.int64)
    rgb = np.full((len(tris), 3), 255) if colours is None else colours
    keys, inverse = np.unique(np.column_stack((np.round(tris.reshape(-1, 3), 1), np.repeat(rgb, 3, 0))), axis=0, return_inverse=True)
    return keys[:, :3], np.column_stack((keys[:, 3:], np.full(len(keys), 255))).astype(np.uint8), inverse.reshape(-1, 3)


def read(path):
    f = rhino3dm.File3dm.Read(str(path))
    assert f is not None, f"could not read {path}"
    unit = cb.FEET_PER_UNIT.get(f.Settings.ModelUnitSystem)
    assert unit, f"{path.name}: unexpected units {f.Settings.ModelUnitSystem}"
    kind_of = {layer.Index: layer_kind(layer.FullPath) for layer in f.Layers}
    shapes, open_roads = {k: [] for _, k in KINDS}, []
    for obj in f.Objects:
        kind, g = kind_of.get(obj.Attributes.LayerIndex), obj.Geometry
        if kind is None or not isinstance(g, rhino3dm.Curve):
            continue
        pts = np.array([(p.X * unit, p.Y * unit, 0.0) for p in cb.curve_points(g)])
        if len(pts) < 2:
            continue
        xy = cb.to_unreal(pts)[:, :2]
        if g.IsClosed and len(pts) >= 4:
            shapes[kind].append(shapely.make_valid(shapely.Polygon(xy)))
        elif kind == "road":
            open_roads.append(shapely.LineString(xy))
    return shapes, open_roads


def test_block_rooms():
    """The grey test block's buildings and copies (build_test_block.py: each the smallest rectangle around its outline,
    a 2 x 2 grid 300 m apart): sidewalks would poke up through their ground floors."""
    data = json.loads((cb.ROOT / "NYZ/Tools/data/test_block.json").read_text(encoding="utf-8"))
    rects = [shapely.oriented_envelope(shapely.Polygon(b["outline_cm"])) for b in data["buildings"]]
    return shapely.union_all([shapely.transform(r, lambda p, o=(ox, oy): p + o) for r in rects for ox in (-30000, 0) for oy in (-30000, 0)])


LAPS = {}  # seconds per stage of the last conversion, printed with its summary (to see what's slow)


def lap(name, start=[0.0]):
    """Time since the last lap, kept under name. lap(None) starts the clock."""
    now = time.time()
    if name:
        LAPS[name] = LAPS.get(name, 0) + now - start[0]
    start[0] = now


def streets(path):
    """A district file's road, sidewalks and their parts (Unreal cm)."""
    lap(None)
    shapes, open_roads = read(path)
    lap("read")
    blocks, lots, road = area(shapes["block"]), area(shapes["lot"]), area(shapes["road"])
    # Every file carries every district's outline: this one holds most of the file's blocks.
    reps = shapely.get_coordinates(shapely.point_on_surface(np.array(shapes["block"], dtype=object)))
    outline = max(shapes["district"], key=lambda d: shapely.contains_xy(d, reps[:, 0], reps[:, 1]).sum())

    # What's left between blocks, lots and road pieces: half-roads at the district's edge and the FDR's strips (kept:
    # narrow and along an open road line) and islands inside the road (raised like sidewalks).
    # The outline runs out into the water, so the half-roads join wide open areas: only the narrow parts count.
    space = opening(shapely.difference(outline, shapely.union_all([blocks, lots, road])), 50)
    narrow = shapely.get_parts(opening(shapely.difference(space, opening(space, WIDEST_HALF)), 50))
    lines = shapely.union_all(open_roads) if open_roads else shapely.LineString()
    half = narrow[shapely.dwithin(narrow, lines, 100)]
    road_halves = shapely.union_all(half)
    gaps = shapely.get_parts(space)
    gaps = gaps[~shapely.dwithin(gaps, lines, 100)]
    islands = gaps[edge_share(gaps, road, 50) > 0.9]  # islands and medians: nearly all their edge against road (outlines meet only roughly)
    road = shapely.union_all([road, road_halves])
    # Medians the city draws only as park outlines over the road (Houston Street): raised like the islands.
    parks = shapely.get_parts(np.asarray(shapes["park"], dtype=object))
    parks = parks[shapely.get_type_id(parks) == 3]
    medians = shapely.intersection(parks[shapely.area(shapely.intersection(parks, road)) > 0.5 * shapely.area(parks)], road)
    islands = np.concatenate([islands, medians[~shapely.is_empty(medians)]])
    road = shapely.difference(road, shapely.union_all(medians))

    lap("half-roads, islands")
    # Most sidewalk outlines are whole blocks with their lots inside, but in housing projects and some parks they are the
    # sidewalks and paths themselves, inside one big lot: only lots lying mostly within the blocks are cut out.
    lot_parts, block_parts = shapely.get_parts(np.asarray(shapes["lot"], dtype=object)), shapely.get_parts(blocks)
    lot_parts = lot_parts[shapely.get_type_id(lot_parts) == 3]
    li, bi = shapely.STRtree(block_parts).query(lot_parts, predicate="intersects")
    held = np.bincount(li, shapely.area(shapely.intersection(lot_parts[li], block_parts[bi])), len(lot_parts)) > 0.5 * shapely.area(lot_parts)
    walk = shapely.union_all([opening(shapely.difference(blocks, shapely.union_all(lot_parts[held])), 20), *islands])
    # Where a lot still runs right to the curb, the usual sidewalk along it.
    bare = shapely.difference(shapely.intersection(shapely.boundary(blocks), shapely.buffer(road, 50)), shapely.buffer(walk, 50))
    walk = shapely.union(walk, shapely.intersection(blocks, shapely.buffer(bare, BARE_CURB_WALK, cap_style="flat")))
    # Not into buildings, nor across a road (some sidewalk outlines lie over a street, under the Manhattan Bridge): a
    # piece lying over the road that reaches its edge in two places, little of its outline being that edge. Where they
    # only overlap a road's edge (corners, widened sidewalks) or lie inside it (medians), the sidewalk wins.
    lap("sidewalk from blocks and lots")
    over = shapely.get_parts(shapely.intersection(walk, road))
    over = over[shapely.get_type_id(over) == 3]
    # Each piece's outline against the road's edge near it: against the whole edge at once it ran out of memory on big
    # districts (BK15, QN12, 2026-11-15).
    edge = segments(road)
    rims = shapely.boundary(over)
    oi, ei = shapely.STRtree(edge).query(rims, predicate="dwithin", distance=5)
    bits = shapely.intersection(rims[oi], shapely.buffer(edge[ei], 5))
    groups = np.split(bits[np.argsort(oi, kind="stable")], np.cumsum(np.bincount(oi, minlength=len(over)))[:-1])
    # only a piece touching the edge in more than one bit can reach it in two places
    touch = np.array([shapely.line_merge(shapely.union_all(g)) if len(g) > 1 else (g[0] if len(g) else shapely.LineString())
                      for g in groups], dtype=object)
    across = over[(shapely.length(touch) < 0.3 * shapely.length(over)) & (shapely.get_num_geometries(touch) >= 2)]
    rooms = test_block_rooms()
    buildings = area(shapes["building"])
    walk = shapely.difference(walk, shapely.union_all([buildings, rooms, *across]))
    lap("across the road")
    # Building outlines stand a little back from the lot lines the sidewalk ends at (MN03: typically 0.5-1 m along 55 km
    # of fronts, a sunken strip): the sidewalk runs on to the wall where the gap is under TO_WALL.
    housed = shapely.union(buildings, rooms)
    joined = shapely.buffer(shapely.buffer(shapely.union(walk, housed), TO_WALL / 2, join_style="mitre"), -TO_WALL / 2, join_style="mitre")
    walk = shapely.union(walk, shapely.difference(shapely.intersection(joined, shapely.buffer(walk, TO_WALL)), shapely.union(housed, road)))
    # Only this district's streets: neighbours' files draw some border streets too (2026-11-15: 121,000 road points in
    # two districts, two road skins there and the ground set by whichever converted last). Streets outside every
    # district's outline (parks, airports between districts) stay with whichever file has them.
    lap("to the wall")
    # Most files carry their own outline twice (BK04, BX01: first and again among the rest), so "the others" are those
    # covering little of it; leaving out only the one picked took away almost all of 33 districts' streets (2026-11-16).
    others = shapely.union_all([d for d in shapes["district"] if shapely.area(shapely.intersection(d, outline)) < 0.5 * outline.area])
    assert shapely.area(shapely.intersection(others, outline)) < 0.05 * outline.area, "the other districts' outlines cover this one's"
    border = shapely.difference(cb.map_border(), others)
    road = area(shapely.simplify(shapely.intersection(road, border), SIMPLIFY))  # polygons only: the border can leave lines
    walk = shapely.get_parts(shapely.simplify(shapely.intersection(walk, border), SIMPLIFY))
    walk = shapely.union_all(walk[(shapely.get_type_id(walk) == 3) & (shapely.area(walk) > 2000)])  # no crumbs under 0.2 m2
    s = dict(road=road, walk=walk, blocks=blocks, road_pieces=area(shapes["road"]), road_halves=road_halves, half=half,
             islands=islands, outline=outline, open_roads=open_roads, lots=lots, parks=shapely.union_all(parks),
             buildings=housed)  # the test block's rooms stand in for the buildings they replaced
    feet = shapely.get_parts(np.asarray(shapes["building"], dtype=object))
    s["footprints"] = feet[shapely.get_type_id(feet) == 3]  # one each: the union joins a row's buildings
    # Thin medians the city leaves as cracks, median tips and leftover corners: road, so no terrain shows through.
    lap("clip to district and map")
    s["filled"] = street_gaps(s)
    lap("gaps filled")
    s["road"] = shapely.union_all([road, *shapely.buffer(s["filled"], 10)])
    s["ramps"] = curb_ramps(s)
    lap("curb ramps")
    s["pits"], s["trees"] = street_trees(s)
    lap("trees")
    s["walk"] = area(shapely.difference(s["walk"], shapely.union_all([*s["ramps"], *s["pits"]])))
    s["doors"], s["leaves"] = cellar_doors(s)
    lap("cellar doors")
    s["road_piece_list"] = shapes["road"]
    return s


def area_in(g, parts, tree):
    """How much of g lies in the area made of parts (not overlapping), from the parts near it: intersecting each small
    shape with a whole district's sidewalk took hours on Queens' big districts (2026-11-15)."""
    return shapely.area(shapely.intersection(g, parts[tree.query(g)])).sum()


def street_trees(s):
    """The census's trees in this district (GDD section 5, real positions): those standing at the curb get a tree pit,
    PIT_FROM_CURB in from the nearest curb (the census points sit up to a few metres off it, many just in the road);
    a pit that would sit on a ramp or another pit, or mostly off the sidewalk, slides along the curb up to 1.5 m or is
    left out with its tree. Trees off the curb (lawns, planting strips) stand where the census puts them, unless that's
    in the road, a building or on a ramp. Returns the pits (outlines) and the trees: x, y (cm), kind (0 alive, 1 dead,
    2 stump), trunk diameter (cm). No census file: no trees."""
    if not TREES.exists():
        print(f"no tree census at {TREES}: no trees")
        return np.array([], dtype=object), np.zeros((0, 4))
    import csv
    rows = list(csv.DictReader(open(TREES, encoding="utf-8")))
    xy = cb.to_unreal(np.array([(float(r["x_sp"]), float(r["y_sp"]), 0.0) for r in rows]))[:, :2]
    here = shapely.contains_xy(s["outline"], xy[:, 0], xy[:, 1]) & shapely.contains_xy(cb.map_border(), xy[:, 0], xy[:, 1])
    rows, xy = [rows[i] for i in np.flatnonzero(here)], xy[here]
    kind = np.array([{"Alive": 0, "Dead": 1, "Stump": 2}.get(r["status"], 0) for r in rows])
    inches = np.array([float(r["stump_diam"] if k == 2 else r["tree_dbh"]) or 3 for r, k in zip(rows, kind)])
    trunk = np.maximum(8, inches * 2.54 * np.where(kind == 2, 1, GROWN))
    on_curb = np.array([r["curb_loc"] == "OnCurb" for r in rows])

    road, walk = s["road"], s["walk"]
    walk_parts = shapely.get_parts(walk)
    walk_tree = shapely.STRtree(walk_parts)
    for g in (road, walk, s["buildings"]):
        shapely.prepare(g)
    pts, line = shapely.get_coordinates(shapely.boundary(road), return_index=True)
    same = line[1:] == line[:-1]
    segments = shapely.linestrings(np.stack((pts[:-1][same], pts[1:][same]), 1))
    nearest = segments[shapely.STRtree(segments).query_nearest(shapely.points(xy), all_matches=False)[1]]
    ramps = shapely.STRtree(shapely.buffer(s["ramps"], 30)) if len(s["ramps"]) else None
    pits, trees = [], []
    for (x, y), k, d, curb, seg in zip(xy, kind, trunk, on_curb, nearest):
        p = shapely.Point(x, y)
        if curb and shapely.distance(p, seg) < 300:
            a, b = np.asarray(seg.coords)
            u = (b - a) / np.hypot(*(b - a))
            c = np.asarray(shapely.line_interpolate_point(seg, shapely.line_locate_point(seg, p)).coords[0])
            n = np.array([-u[1], u[0]])
            n = n if shapely.contains_xy(walk, *(c + 50 * n)) else -n
            if not shapely.contains_xy(walk, *(c + 50 * n)):
                continue
            others = shapely.STRtree(pits[-200:]) if pits else None
            for shift in (0, 50, -50, 100, -100, 150, -150):
                q = c + u * shift + n * (PIT_FROM_CURB + PIT_ACROSS / 2)
                du, dn = u * PIT_LONG / 2, n * PIT_ACROSS / 2
                pit = shapely.Polygon([q - du - dn, q + du - dn, q + du + dn, q - du + dn])
                if (area_in(pit, walk_parts, walk_tree) > 0.8 * pit.area
                        and not (ramps is not None and len(ramps.query(pit, predicate="intersects")))
                        and not (others is not None and len(others.query(pit, predicate="intersects")))):
                    pits.append(pit)
                    trees.append((*q, k, d))
                    break
        elif not (shapely.contains_xy(road, x, y) or shapely.contains_xy(s["buildings"], x, y)
                  or (ramps is not None and len(ramps.query(p, predicate="intersects")))):
            trees.append((x, y, k, d))
    return np.array(pits, dtype=object), np.array(trees).reshape(-1, 4)


ICO = None


def tree_meshes(trees):
    """Placeholder trees (GDD section 24, chunk 2): an 8-sided trunk and a round canopy sized from the trunk's thickness;
    dead trees a bare trunk, stumps 40 cm. Returns the trunks (bark), canopies (leaves) and each trunk's collision post
    (a square inside it, POST high: solid, merged into the tile), as N x 3 x 3 triangles facing out."""
    global ICO
    if ICO is None:  # a sphere of 80 triangles: an icosahedron with each face split in four
        g = (1 + 5 ** 0.5) / 2
        v = np.array([(-1, g, 0), (1, g, 0), (-1, -g, 0), (1, -g, 0), (0, -1, g), (0, 1, g), (0, -1, -g), (0, 1, -g),
                      (g, 0, -1), (g, 0, 1), (-g, 0, -1), (-g, 0, 1)], float)
        f = np.array([(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6),
                      (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10),
                      (8, 6, 7), (9, 8, 1)])
        a, b, c = v[f[:, 0]], v[f[:, 1]], v[f[:, 2]]
        ab, bc, ca = (a + b) / 2, (b + c) / 2, (c + a) / 2
        t = np.concatenate((np.stack((a, ab, ca), 1), np.stack((ab, b, bc), 1), np.stack((ca, bc, c), 1), np.stack((ab, bc, ca), 1)))
        ICO = t / np.linalg.norm(t, axis=2, keepdims=True)
    if not len(trees):
        z = np.zeros((0, 3, 3))
        return z, z, z
    x, y, kind, d = trees.T
    ground = surface(x, y)
    tall = np.clip(300 + 25 * d, 400, 2200)
    crown = np.clip(80 + 9 * d, 150, 800)
    top = ground + np.select([kind == 0, kind == 1], [tall - crown, 0.7 * tall], 40)
    base = ground - 10
    centre = np.column_stack((x, y))

    def prism(sides, radius, z0, z1):
        """N upright prisms (sides and a top): N x (3 * sides - 2) x 3 x 3."""
        ang = np.arange(sides) * 2 * np.pi / sides
        ring = centre[:, None, :] + radius[:, None, None] * np.stack((np.cos(ang), np.sin(ang)), -1)[None]
        lo = np.concatenate((ring, np.repeat(z0[:, None, None], sides, 1)), 2)
        hi = np.concatenate((ring, np.repeat(z1[:, None, None], sides, 1)), 2)
        nxt = np.roll(np.arange(sides), -1)
        walls = np.concatenate((np.stack((lo, lo[:, nxt], hi[:, nxt]), 2), np.stack((lo, hi[:, nxt], hi), 2)), 1)
        cap = np.stack((hi[:, :1].repeat(sides - 2, 1), hi[:, 1:-1], hi[:, 2:]), 2)
        return np.concatenate((walls, cap), 1)

    def outward(tris, centres):
        """Each triangle wound to face away from its object's centre (the trunk's axis at mid-height, the canopy's middle)."""
        n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
        flip = np.einsum("ij,ij->i", n, tris.mean(1) - centres) < 0
        tris[flip] = tris[flip][:, [0, 2, 1]]
        return tris

    post_top = np.minimum(top, ground + POST)
    trunks = prism(8, d / 2, base, top).reshape(-1, 3, 3)
    posts = prism(4, 0.9 * d / 2, base, post_top).reshape(-1, 3, 3)  # its corners on the trunk's: hidden inside it
    alive = kind == 0
    mid = np.column_stack((centre[alive], ground[alive] + tall[alive] - crown[alive]))
    canopies = (mid[:, None, None, :] + crown[alive][:, None, None, None] * ICO[None]).reshape(-1, 3, 3)
    axis = lambda z0, z1, per: np.repeat(np.column_stack((centre, (z0 + z1) / 2)), per, 0)  # noqa: E731
    return (outward(trunks, axis(base, top, 22)), outward(canopies, np.repeat(mid, len(ICO), 0)),
            outward(posts, axis(base, post_top, 10)))


def curb_ramps(s):
    """Curb ramps (outlines), two to a corner, as New York builds them now: one on each side of a block's rounded corner,
    just past the curve, straight into the sidewalk, RAMP_WIDE wide and RAMP_RUN deep. A block's corners are where
    squaring it off adds an ear (its corner point and the two ends of the curve). Only real blocks' corners at a road;
    none overlapping another."""
    blocks = shapely.get_parts(s["blocks"])
    blocks = blocks[shapely.area(blocks) > 5e6]  # 500 m2: not a median's nose
    ears, k = shapely.get_parts(shapely.difference(opening(blocks, 500), blocks), return_index=True)
    keep = (shapely.get_type_id(ears) == 3) & (shapely.area(ears) > 2000) & (shapely.area(ears) < 6e5)
    ears, k = ears[keep], k[keep]
    road = s["road"]
    shapely.prepare(road)
    near = shapely.dwithin(ears, road, 50)
    ears, k = ears[near], k[near]
    walk = shapely.get_parts(s["walk"])
    walk_tree = shapely.STRtree(walk)
    ramps, taken = [], shapely.STRtree([])
    for ear, block in zip(ears, blocks[k]):
        xy = np.asarray(ear.exterior.coords)[:-1]
        c = int(np.argmax(shapely.distance(shapely.points(xy), block)))  # the squared-off corner; its neighbours end the curve
        for end in (xy[c - 1], xy[(c + 1) % len(xy)]):
            u = (end - xy[c]) / np.hypot(*(end - xy[c]))
            q = end + u * (RAMP_WIDE / 2 + 20)
            n = np.array([-u[1], u[0]])
            n = n if shapely.contains_xy(block, *(q + 50 * n)) else -n
            w = u * RAMP_WIDE / 2
            rect = shapely.Polygon([q - w - 50 * n, q + w - 50 * n, q + w + RAMP_RUN * n, q - w + RAMP_RUN * n])
            ramp = shapely.get_parts(shapely.intersection(rect, shapely.union_all(walk[walk_tree.query(rect)])))
            ramp = ramp[shapely.get_type_id(ramp) == 3]
            if not len(ramp):
                continue
            ramp = ramp[np.argmax(shapely.area(ramp))]
            close = [r for r in (ramps[i] for i in taken.query(ramp)) if shapely.intersects(r, ramp)]
            if ramp.area < 1e4 or sum(shapely.area(shapely.intersection(ramp, r)) for r in close) > 0.2 * ramp.area:
                continue
            ramps.append(shapely.difference(ramp, shapely.union_all(close)) if close else ramp)
            taken = shapely.STRtree(ramps)
    return np.array(ramps, dtype=object)


def cellar_doors(s):
    """Placeholder cellar doors (GDD section 24, chunk 2): a random half of the buildings with at least DOOR_FRONT of
    straight street front get one against the wall, at a fixed random spot at least 1 m from the front's ends and 1 m
    from the curb, clear of ramps and tree pits (tried there, then 1 and 2 m either side). Returns the doors and their
    two leaves each (outlines; the seam between them runs out from the wall)."""
    walk, road = s["walk"], s["road"]
    walk_parts = shapely.get_parts(walk)
    walk_tree = shapely.STRtree(walk_parts)
    street = shapely.get_parts(shapely.intersection(walk, shapely.buffer(road, 1000)))  # not a housing project's paths
    # Each building's outline against the sidewalk pieces near it: against the district's whole sidewalk at once it ran
    # out of memory on big districts (BK18, 2026-11-15).
    band = shapely.buffer(street, 50)
    fi, bi = shapely.STRtree(band).query(s["footprints"], predicate="intersects")
    pieces = shapely.intersection(shapely.boundary(s["footprints"][fi]), band[bi])
    order = np.argsort(fi, kind="stable")
    front = np.split(pieces[order], np.cumsum(np.bincount(fi, minlength=len(s["footprints"])))[:-1])
    rng = np.random.default_rng(2)
    pick = np.flatnonzero(np.bincount(fi, shapely.length(pieces), len(s["footprints"])) >= DOOR_FRONT)
    pick = pick[rng.random(len(pick)) < 0.5]  # every other building (the developer), at random
    for g in (walk, road):
        shapely.prepare(g)
    taken = [*s["ramps"], *s["pits"]]
    blocked = shapely.STRtree(shapely.buffer(taken, 30)) if taken else None
    doors, leaves = [], []
    for i in pick:
        line = max(shapely.get_parts(shapely.line_merge(shapely.union_all(front[i]))), key=lambda g: g.length)
        lo, hi = 100 + DOOR_WIDE / 2, line.length - 100 - DOOR_WIDE / 2
        if hi < lo:
            continue
        spot = rng.uniform(lo, hi)
        for at in (spot, spot + 100, spot - 100, spot + 200, spot - 200):
            if not lo <= at <= hi:
                continue
            a, b = (np.asarray(shapely.line_interpolate_point(line, at + d).coords[0]) for d in (-DOOR_WIDE / 2, DOOR_WIDE / 2))
            if abs(np.hypot(*(b - a)) - DOOR_WIDE) > 2:  # the wall bends here (a corner)
                continue
            u = (b - a) / DOOR_WIDE
            n = np.array([-u[1], u[0]])
            c = (a + b) / 2
            n = n if shapely.contains_xy(walk, *(c + 30 * n)) else -n
            out = lambda w0, w1, d0=2, d1=2 + DOOR_OUT: shapely.Polygon([c + u * w0 + n * d0, c + u * w1 + n * d0,  # noqa: E731
                                                                        c + u * w1 + n * d1, c + u * w0 + n * d1])
            door = out(-DOOR_WIDE / 2, DOOR_WIDE / 2)
            if (area_in(door, walk_parts, walk_tree) > 0.98 * door.area and not shapely.dwithin(door, road, 100)
                    and not (blocked is not None and len(blocked.query(door, predicate="intersects")))):
                doors.append(door)
                leaves += [out(-DOOR_WIDE / 2, -1), out(1, DOOR_WIDE / 2)]
                break
    doors = np.array(doors, dtype=object)
    a, b = shapely.STRtree(doors).query(doors, predicate="intersects")  # two buildings' doors at an inside corner
    keep = np.ones(len(doors), bool)
    keep[b[a < b]] = False
    return doors[keep], np.array(leaves, dtype=object).reshape(-1, 2)[keep].ravel()


def drape(polys, top, up):
    """Outlines laid on a surface (N x 3 x 3 triangles), up cm above it, cut along its triangles: N x 3 x 3 facing up."""
    if not len(polys) or not len(top):
        return np.zeros((0, 3, 3))
    flat = shapely.polygons(np.concatenate((top[:, :, :2], top[:, :1, :2]), 1))
    pi, ti = shapely.STRtree(flat).query(polys, predicate="intersects")
    tris, k = triangulate(shapely.intersection(polys[pi], flat[ti]), owners=True)
    t = top[ti[k]]
    n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])  # each piece's corners on its triangle's plane
    z = t[:, :1, 2] - (n[:, None, 0] * (tris[..., 0] - t[:, :1, 0]) + n[:, None, 1] * (tris[..., 1] - t[:, :1, 1])) / n[:, None, 2]
    return face_up(np.concatenate((tris, (z + up)[..., None]), 2))


def street_gaps(s):
    """Bare ground ringed by the street and largely by road, outside blocks, lots and parks (so not lawns between paths,
    planted malls or water): terrain that shows through the street."""
    street = shapely.union_all([s["road"], s["walk"], *s.get("pits", [])])  # a tree pit's soil is the street's too
    grass = shapely.union(s["lots"], s["parks"])
    space = shapely.difference(s["outline"], shapely.union_all([s["blocks"], grass, street]))
    gaps = shapely.get_parts(opening(space, 5))
    gaps = gaps[shapely.area(gaps) > 5000]
    if not len(gaps):
        return gaps
    return gaps[(edge_share(gaps, street, 50) > 0.7) & (edge_share(gaps, s["road"], 50) > 0.4) & (edge_share(gaps, grass, 50) < 0.3)]


def audit(s):
    """Looks for the kinds of fault first found by eye in MN03 (GDD section 24, map stage 1): curbs with no sidewalk,
    terrain showing through gaps in the street, raised islands joining two blocks across a road, specks of sidewalk; and
    gaps left between a sidewalk and a building front.
    Returns [{"kind", "x", "y", "size"}]: Unreal cm, size in m (curbs) or m2."""
    road, walk, blocks = s["road"], s["walk"], s["blocks"]
    issues = []

    def add(kind, geoms, sizes):
        for p, size in zip(shapely.point_on_surface(geoms), sizes):
            issues.append({"kind": kind, "x": round(p.x), "y": round(p.y), "size": round(float(size), 1)})

    curb = shapely.intersection(shapely.boundary(blocks), shapely.buffer(shapely.boundary(road), 50))  # at the road's edge
    bare = shapely.get_parts(shapely.line_merge(shapely.difference(curb, shapely.buffer(walk, 50))))
    shapely.prepare(s["buildings"])
    bare = bare[(shapely.length(bare) > 300) & ~shapely.dwithin(bare, s["buildings"], 100)]  # a building at the curb is the city's data
    add("curb with no sidewalk", bare, shapely.length(bare) / 100)

    # streets() fills gaps under TO_WALL: one well under it left is new (nearer it, setbacks and slanted fronts are real).
    near = shapely.intersection(shapely.boundary(s["buildings"]), shapely.buffer(walk, 0.75 * TO_WALL))
    strip = shapely.get_parts(shapely.line_merge(shapely.difference(near, shapely.buffer(walk, 20))))
    strip = strip[shapely.length(strip) > 300]
    add("gap between sidewalk and building", strip, shapely.length(strip) / 100)

    gaps = street_gaps(s)  # streets() fills these: any left is new
    add("terrain showing in the street", gaps, shapely.area(gaps) / 1e4)

    big = shapely.get_parts(blocks)
    big = big[shapely.area(big) > 5e6]  # 500 m2: a real block, not the nose of a median
    near, _ = shapely.STRtree(big).query(s["islands"], predicate="dwithin", distance=50)
    strips = s["islands"][np.bincount(near, minlength=len(s["islands"])) >= 2]
    add("raised island joining two blocks", strips, shapely.area(strips) / 1e4)

    parts = shapely.get_parts(walk)
    specks = parts[shapely.area(parts) < 2e4]
    if len(s.get("ramps", [])):
        specks = specks[~shapely.dwithin(specks, shapely.union_all(s["ramps"]), 10)]  # between ramps: a corner's own top
    specks = specks[~shapely.dwithin(specks, s["buildings"], 10)]  # against a wall: the notches between bay fronts
    add("speck of sidewalk", specks, shapely.area(specks) / 1e4)
    return issues


def write_audit(district, s, issues):
    """<district>_issues.json and a map of the district with each issue numbered, for a look before the editor."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from shapely.plotting import plot_polygon

    (OUT / f"{district}_issues.json").write_text(json.dumps(
        {"district": district, "units": "x, y: cm, Unreal map coordinates; size: m (curbs) or m2",
         "issues": [{"n": i + 1, **it} for i, it in enumerate(issues)]}, indent=1), encoding="utf-8")
    fig, ax = plt.subplots(figsize=(20, 20))
    for g, shade in ((s["road"], "0.55"), (s["walk"], "0.85")):
        if not g.is_empty:  # a district with only a sliver inside the map can have no road or no sidewalk
            plot_polygon(g, ax=ax, add_points=False, facecolor=shade, edgecolor="none")
    colours = dict(zip(sorted({it["kind"] for it in issues}), ("red", "magenta", "blue", "orange", "green")))
    for i, it in enumerate(issues):
        ax.plot(it["x"], it["y"], "o", ms=14, mfc="none", mec=colours[it["kind"]], mew=2)
        ax.annotate(str(i + 1), (it["x"], it["y"]), xytext=(8, 8), textcoords="offset points", fontsize=9, color=colours[it["kind"]])
    for kind, c in colours.items():
        ax.plot([], [], "o", mfc="none", mec=c, mew=2, label=f"{kind} ({sum(it['kind'] == kind for it in issues)})")
    ax.legend(loc="upper left", fontsize=12)
    ax.set_aspect("equal")
    ax.invert_yaxis()  # +Y is south
    ax.set_title(f"{district}: street issues (numbers as in {district}_issues.json)")
    fig.savefig(OUT / f"{district}_issues.png", dpi=80, bbox_inches="tight")
    plt.close(fig)


def convert(path):
    district, s = prepare(path)
    if s:
        build(district, s)


def prepare(path):
    """A district file's streets, with the ground under them smoothed (it reads only the original heights, so districts
    can do this in any order). Returns the district's code and its streets (None if it has none). A city-wide run does
    this for every district before build(), so a street on a district line is built on its neighbour's final ground."""
    district = path.stem.replace("NYC_3DModel_", "")
    LAPS.clear()
    s = streets(path)
    if s["road"].is_empty and s["walk"].is_empty:
        print(f"{district}: no streets inside the map's border")
        return district, None
    import street_bed
    street_bed.smooth(s, district)  # the ground under the streets first: everything built sits on it
    lap("ground smoothed")
    return district, s


def build(district, s):
    """The district's tiles, check points and street checks, on the terrain as it is now (terrain/NYZ_terrain.r16)."""
    lap(None)
    import street_props  # here, not at the top: it imports this file
    s["dress"] = street_props.showcase(s)
    road, walk, blocks, road_halves, half, islands = (s[k] for k in ("road", "walk", "blocks", "road_halves", "half", "islands"))
    edges = shapely.difference(shapely.boundary(walk), shapely.buffer(s["buildings"], 10))  # none hidden in a wall
    for g in (road, walk, edges):
        shapely.prepare(g)

    # Tiles: 500 m (TILE); each split into 10 m cells.
    x0, y0, x1, y1 = shapely.GeometryCollection([road, walk]).bounds
    tiles = []
    counts = np.zeros(9, dtype=np.int64)
    trees = s["trees"]
    paint, props, _ = s["dress"] or ({}, street_props.Props(), None)
    look, look_rgb, look_at, solid, solid_at = props.arrays()
    for tx in range(int(np.floor(x0 / TILE)), int(np.floor(x1 / TILE)) + 1):
        for ty in range(int(np.floor(y0 / TILE)), int(np.floor(y1 / TILE)) + 1):
            bx, by = tx * TILE, ty * TILE
            tile = shapely.box(bx, by, bx + TILE, by + TILE)
            if not (shapely.intersects(road, tile) or shapely.intersects(walk, tile)):
                continue
            cells, gx, gy = boxes(bx, by, CELL, TILE // CELL)
            r, w, e = (shapely.intersection(g, tile) for g in (road, walk, edges))
            shapely.prepare(r)
            shapely.prepare(w)
            near = shapely.intersection(road, shapely.buffer(tile, RAMP_RUN + 100))  # a ramp's curb can be in the next tile
            ramps = shapely.intersection(s["ramps"][shapely.intersects(s["ramps"], tile)], tile)
            pits = shapely.union_all(shapely.intersection(s["pits"][shapely.intersects(s["pits"], tile)], tile))
            mine = trees[(trees[:, 0] >= bx) & (trees[:, 0] < bx + TILE) & (trees[:, 1] >= by) & (trees[:, 1] < by + TILE)]
            bark, leaves, posts = tree_meshes(mine)
            top = lift(walk_top(w, cells, gx, gy), WALK_UP)
            doors = shapely.intersection(s["leaves"][shapely.intersects(s["leaves"], tile)], tile)
            # The showcase street's paint (on the terrain's triangles, like the road skin) and props (by where they stand).
            lines, line_rgb = [np.zeros((0, 3, 3))], [np.zeros((0, 3))]
            for colour, poly in paint.items():
                piece = shapely.intersection(poly, tile)
                if not piece.is_empty:
                    lines.append(lift(road_skin(piece, cells, gx, gy), street_props.PAINT_UP))
                    line_rgb.append(np.tile(colour, (len(lines[-1]), 1)))
            inside = lambda at: (at[:, 0] >= bx) & (at[:, 0] < bx + TILE) & (at[:, 1] >= by) & (at[:, 1] < by + TILE)  # noqa: E731
            here, solid_here = inside(look_at), inside(solid_at)
            sections = [(lift(road_skin(r, cells, gx, gy), ROAD_UP), None),
                        (np.concatenate((top, ramp_top(ramps, near, cells, gx, gy), posts, solid[solid_here])), None),
                        (curb_faces(e, walk, cells), None), (lift(road_skin(pits, cells, gx, gy), ROAD_UP), None), (bark, None),
                        (leaves, None), (drape(doors, top, ROAD_UP), None), (np.concatenate(lines), np.concatenate(line_rgb)),
                        (look[here], look_rgb[here])]
            if not any(len(t) for t, _ in sections):
                continue
            tiles.append((tx, ty, [weld(*sec) for sec in sections]))
            counts += [len(t) for t, _ in sections]

    lap("tiles")
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{district}.nyzs", "wb") as out:
        out.write(b"NYZS" + struct.pack("<II", 4, len(tiles)))  # version 4: nine sections, vertex colours
        for tx, ty, sections in tiles:
            centre = np.array([(tx + 0.5) * TILE, (ty + 0.5) * TILE, 0.0])
            out.write(struct.pack("<iiI9I", tx, ty, sum(len(v) for v, _, _ in sections), *(len(t) for _, _, t in sections)))
            for v, _, _ in sections:
                out.write((v - centre).astype("<f4").tobytes())
            for _, rgba, _ in sections:
                out.write(rgba.tobytes())
            base = 0
            for v, _, t in sections:
                out.write((t + base).astype("<u4").tobytes())
                base += len(v)

    # Points for import_streets.py to trace down at: 20 on roads (the terrain must be what's hit) and 20 on sidewalks
    # (the street tile, 15 cm up), each at least 1 m and 0.5 m inside, and away from blocks and roads respectively.
    rng = np.random.default_rng(1)
    checks = []
    for on, inner, up in (("road", shapely.difference(shapely.buffer(road, -100), shapely.buffer(blocks, 100)), 0),
                          ("sidewalk", shapely.difference(shapely.buffer(walk, -50), shapely.buffer(road, 50)), WALK_UP)):
        if inner.is_empty:  # a district with only a sliver inside the map can have no road or no sidewalk
            continue
        shapely.prepare(inner)
        bx0, by0, bx1, by1 = inner.bounds
        found = []
        while len(found) < 20:
            px, py = rng.uniform(bx0, bx1, 1000), rng.uniform(by0, by1, 1000)
            ok = shapely.contains_xy(inner, px, py)
            found += list(zip(px[ok], py[ok]))
        p = np.array(found[:20])
        checks += [{"on": on, "x": round(x), "y": round(y), "z_cm": round(float(z), 1)}
                   for (x, y), z in zip(p, surface(p[:, 0], p[:, 1]) + up)]
    # 5 in tree pits, beside the trunk (the terrain: the soil is a look-only skin like the road) and 5 on trunks' collision
    # posts (the street tile, POST up or the trunk's top).
    pits = s["pits"][::max(1, len(s["pits"]) // 5)][:5]
    if len(pits):
        ring = shapely.get_coordinates(shapely.get_exterior_ring(pits)).reshape(len(pits), 5, 2)
        p = (ring[:, 0] + ring[:, 3]) / 2 * 0.15 + (ring[:, 1] + ring[:, 2]) / 2 * 0.85  # 63 cm along: clear of any trunk
        checks += [{"on": "pit", "x": round(x), "y": round(y), "z_cm": round(float(z), 1)} for (x, y), z in zip(p, surface(p[:, 0], p[:, 1]))]
    sample = s["trees"][::max(1, len(s["trees"]) // 5)][:5]
    if len(sample):
        _, _, posts = tree_meshes(sample)
        tops = posts.reshape(len(sample), 10, 3, 3)[:, 8:, :, 2].max((1, 2))
        checks += [{"on": "trunk", "x": round(x), "y": round(y), "z_cm": round(float(z), 1)} for (x, y), z in zip(sample[:, :2], tops)]
    # 5 on cellar doors (the sidewalk under them: the plates are look-only).
    doors = s["doors"][::max(1, len(s["doors"]) // 5)][:5]
    p = shapely.get_coordinates(shapely.centroid(doors)).reshape(-1, 2)
    checks += [{"on": "door", "x": round(x), "y": round(y), "z_cm": round(float(z), 1)} for (x, y), z in zip(p, surface(p[:, 0], p[:, 1]) + WALK_UP)]
    # The showcase street: 3 on paint (the terrain: paint is look-only), 3 on hydrants' posts and 3 on car roofs (solid).
    if s["dress"]:
        white = shapely.get_parts(paint.get(street_props.WHITE, shapely.Polygon()))
        white = white[shapely.area(white) > 1e4]
        p = shapely.get_coordinates(shapely.point_on_surface(white[::max(1, len(white) // 3)][:3])).reshape(-1, 2)
        checks += [{"on": "road", "x": round(x), "y": round(y), "z_cm": round(float(z), 1)} for (x, y), z in zip(p, surface(p[:, 0], p[:, 1]))]
        for kind, up in (("hydrant", WALK_UP - 6 + 80), ("car", ROAD_UP + 145)):
            p = np.array([(it["x"], it["y"]) for it in props.items if it["kind"] == kind][:3], float).reshape(-1, 2)
            checks += [{"on": "prop", "x": round(x), "y": round(y), "z_cm": round(float(z), 1)} for (x, y), z in zip(p, surface(p[:, 0], p[:, 1]) + up)]
    # And 10 on curb ramps (the street tile, at the ramp's height there, which may be raised a little to clear the terrain).
    ramps = s["ramps"][::max(1, len(s["ramps"]) // 10)][:10]
    p = shapely.get_coordinates(shapely.point_on_surface(ramps))
    rise = ROAD_UP + (WALK_UP - ROAD_UP) * np.clip(shapely.distance(shapely.points(p), road) / RAMP_RUN, 0, 1)
    checks += [{"on": "ramp", "x": round(x), "y": round(y), "z_cm": round(float(z), 1)}
               for (x, y), z in zip(p, surface(p[:, 0], p[:, 1]) + rise)]

    ints = lambda g: np.round(shapely.get_coordinates(g)).astype(int).tolist()  # noqa: E731
    (OUT / f"{district}.json").write_text(json.dumps({
        "district": district, "source": f"NYC_3DModel_{district}.3dm (NYC City Planning 3D model, street outlines)",
        "units": "cm, Unreal map coordinates: +X east, +Y south", "tile_size_cm": TILE, "checks": checks,
        "road_pieces": [{"id": f"{district}-r{i}", "outline_cm": ints(shapely.get_exterior_ring(p))}
                        for i, p in enumerate(shapely.get_parts(s["road_pieces"]))]
                       + [{"id": f"{district}-h{i}", "outline_cm": ints(shapely.get_exterior_ring(p)), "half_road": True}
                          for i, p in enumerate(shapely.get_parts(road_halves))],
        "blocks": [{"id": f"{district}-b{i}", "curb_cm": ints(shapely.get_exterior_ring(p))}
                   for i, p in enumerate(shapely.get_parts(blocks))],
        "ramps": [{"id": f"{district}-ramp{i}", "outline_cm": ints(shapely.get_exterior_ring(p))}
                  for i, p in enumerate(s["ramps"])],
        "trees": [{"x": round(x), "y": round(y), "kind": ("alive", "dead", "stump")[int(k)], "trunk_cm": round(d)}
                  for x, y, k, d in s["trees"]],
        "tree_pits": [{"outline_cm": ints(shapely.get_exterior_ring(p))} for p in s["pits"]],
        "cellar_doors": [{"outline_cm": ints(shapely.get_exterior_ring(p))} for p in s["doors"]],
        "showcase": {"area_cm": ints(shapely.get_exterior_ring(s["dress"][2])), "props": props.items} if s["dress"] else None}),
        encoding="utf-8")

    print(f"{district}: road {road.area / 1e10:.3f} km2 ({len(half)} half-road pieces), sidewalk {walk.area / 1e10:.3f} km2 "
          f"({len(islands)} islands; {len(s['filled'])} gaps in the street filled as road; {len(s['ramps'])} curb ramps; "
          f"{len(s['trees'])} trees, {len(s['pits'])} in pits; {len(s['doors'])} cellar doors), {len(tiles)} tiles; triangles: road skin {counts[0]:,}, sidewalk {counts[1]:,} (solid), "
          f"curbs {counts[2]:,}, tree pits {counts[3]:,}, trunks {counts[4]:,}, canopies {counts[5]:,}, cellar doors {counts[6]:,}, "
          f"paint {counts[7]:,}, props {counts[8]:,}; {sum(LAPS.values()):.0f} s")
    if s["dress"]:
        from collections import Counter
        kinds = Counter(it["kind"] for it in props.items)
        print(f"{district} showcase street: " + ", ".join(f"{n} {k}" for k, n in sorted(kinds.items())) + f"; paint "
              f"{sum(shapely.area(g) for g in paint.values()) / 1e4:.0f} m2; props' solid triangles {len(solid):,}")
    lap("written")
    issues = audit(s)
    lap("checks")
    write_audit(district, s, issues)
    kinds = sorted({it["kind"] for it in issues})
    print(f"{district} checks: " + ("; ".join(f"{sum(it['kind'] == k for it in issues)} {k}" for k in kinds) or "nothing found")
          + (f" (see terrain/streets/{district}_issues.png)" if issues else ""))
    print(f"{district} times: " + ", ".join(f"{k} {v:.0f} s" for k, v in LAPS.items()))


def self_check():
    """The surface meets the terrain's grid points, and halfway along a square's diagonal it's the corners' mean."""
    x = cb.LOC["x"] + STEP * np.array([8000.0, 8001.0])
    y = cb.LOC["y"] + STEP * np.array([9000.0, 9001.0])
    assert np.allclose(surface(x, y), cb.ground(x, y))
    mid = surface(np.array([x.mean()]), np.array([y.mean()]))[0]
    assert np.isclose(mid, cb.ground(x, y).mean())
    # The audit finds a curb with half its sidewalk missing and a 2 m hole in a road.
    road = shapely.difference(shapely.box(0, 0, 3000, 1000), shapely.box(1000, 400, 1200, 600))
    block, lots = shapely.box(0, 1000, 3000, 4000), shapely.box(0, 1300, 3000, 4000)
    s = dict(road=road, walk=shapely.box(0, 1000, 1500, 1300), blocks=block, lots=lots, buildings=shapely.Point(-9e6, 0), parks=shapely.Polygon(),
             outline=shapely.box(-1000, -1000, 4000, 5000), islands=np.array([], dtype=object))
    kinds = sorted(it["kind"] for it in audit(s))
    assert kinds == ["curb with no sidewalk", "terrain showing in the street"], kinds
    # A square with a hole has 8 edge segments (none joining the two rings), and a square beside it shares a quarter of
    # its outline with it.
    g = shapely.difference(shapely.box(0, 0, 1000, 1000), shapely.box(400, 400, 600, 600))
    assert len(segments(g)) == 8, len(segments(g))
    share = edge_share(np.array([shapely.box(1000, 0, 2000, 1000)]), g, 1)[0]
    assert abs(share - 0.25) < 0.02, share


if __name__ == "__main__":
    self_check()
    files = [pathlib.Path(p) for p in sys.argv[1:]] or [pathlib.Path(p) for p in sorted(glob.glob(str(cb.RHINO_DIR / "NYC_3DModel_*.3dm")))
                                                          if "_EXPORT" not in p]
    for p in files:
        cb.convert_zip(p, convert) if p.suffix.lower() == ".zip" else convert(p)

"""Places the city's sleeping zombies (GDD section 8, "How many, and where"; zombie chunk 2): about 400 per km2 in
Manhattan's built-up areas, 100 in the other built-up areas, 30 in parks and along the edges; never inside a building,
in water or outside the border. Writes NYZ/Data/NYC_zombies.bin, which the game server reads when it loads the
NYC map (UNYZZombies; out of git like the city, made from data that isn't in git). Run with QGIS's Python (numpy,
shapely, osgeo), about a minute:

  "C:\\Program Files\\QGIS 4.2.2\\bin\\o4w_env.bat" && python "C:\\Game Dev Folder\\NYZ\\tools\\map\\seed_zombies.py"

Built-up means a 100 m cell at least 3% covered by buildings from NYC's building list (terrain/buildings/*.json, made by
convert_buildings.py); Manhattan's are the cells whose buildings are mostly in MN districts. New Jersey has no buildings in
the list yet (map stage 1), so it counts as an edge for now. Water: terrain more than 1 m below sea level.

Zombies come in small groups of 3-10 and, HORDE_SHARE of them, roaming hordes of 30-100 (GDD section 8, hordes). The file
also lists refill entry points along the wall's land stretches and at the subway's street entrances (section 8: new
zombies arrive slowly from the edges and climb up out of subway entrances), from the MTA's entrance list in terrain/subway/.

File: b"NYZZ", uint32 version (3), uint32 count, then count x (float x, float y, float z, uint32 group: its group's number,
with the top bit set for a roaming horde), then uint32 wall entries and entries x (float x, float y, float z), then the
same for subway entrances; little-endian,
in the map's Unreal centimetres (+X east, +Y south, Z above sea level, on the terrain).
"""
import csv
import glob
import json
import pathlib
import struct
import sys

import numpy as np
import shapely
from osgeo import osr

osr.UseExceptions()
ROOT = pathlib.Path(__file__).resolve().parents[2]
TERRAIN = json.loads((ROOT / "terrain/NYZ_terrain.json").read_text(encoding="utf-8"))
OUT = ROOT / "NYZ/Data/NYC_zombies.bin"
SUBWAY = ROOT / "terrain/subway/mta_subway_entrances_2024.csv"  # the MTA's "Subway Entrances and Exits: 2024", data.ny.gov (downloaded 2026-11-14)
CELL = 10000             # cm: 100 m density cells
PER_KM2 = {"manhattan": 400, "built": 100, "edge": 30}
BUILT_COVER = 0.03       # share of a cell covered by buildings that makes it built-up
WATER_BELOW = -100       # cm, as the game's zombies (NYZZombies.cpp)
HORDE_SHARE = 0.05       # Claude's starting number: the share of the city's zombies in roaming hordes
HORDE_BIT = 0x80000000   # set in a horde's group number
GROUP_SPREAD, HORDE_SPREAD = 600, 1500  # cm around a group's centre
ENTRY_STEP, ENTRY_IN = 50000, 3000      # cm: refill entry points every 500 m along the wall, 30 m inside it
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else None)

# Terrain heights (build_terrain.py): point (row, col) sits at location + (col, row) * 200 cm.
cols, rows = TERRAIN["size_points"]
x0, y0 = TERRAIN["unreal_location_cm"]["x"], TERRAIN["unreal_location_cm"]["y"]
step = TERRAIN["unreal_scale"]["x"]
raw = np.memmap(ROOT / "terrain/NYZ_terrain.r16", dtype="<u2", mode="r", shape=(rows, cols))


def ground_cm(x, y):
    c = np.clip(np.rint((x - x0) / step).astype(int), 0, cols - 1)
    r = np.clip(np.rint((y - y0) / step).astype(int), 0, rows - 1)
    return (raw[r, c].astype(np.float32) - 32768) * TERRAIN["unreal_scale"]["z"] / 128


# The border, from longitude and latitude to the map's centimetres (as build_terrain.py places the terrain).
border_json = json.loads((ROOT / "docs/map/border-draft.geojson").read_text(encoding="utf-8"))
ring = next(f for f in border_json["features"] if f["properties"].get("kind") == "border")["geometry"]["coordinates"][0]
src, dst = osr.SpatialReference(), osr.SpatialReference()
src.ImportFromEPSG(4326)
dst.ImportFromEPSG(26918)
for s in (src, dst):
    s.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
to_utm = osr.CoordinateTransformation(src, dst)
e0, n0 = TERRAIN["world_origin_utm18n_m"]["easting"], TERRAIN["world_origin_utm18n_m"]["northing"]
border = shapely.Polygon([((e - e0) * 100, -(n - n0) * 100) for e, n in (to_utm.TransformPoint(lon, lat)[:2] for lon, lat in ring)])
shapely.prepare(border)

# Buildings: footprints for the inside test, and each cell's covered area, split Manhattan / elsewhere.
footprints, cover = [], {}
for path in sorted(glob.glob(str(ROOT / "terrain/buildings/*.json"))):
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    manhattan = data["district"].startswith("MN")
    for b in data["buildings"]:
        poly = shapely.Polygon(b["footprint_cm"])
        footprints.append(poly)
        c = poly.centroid
        key = (int(c.x // CELL), int(c.y // CELL))
        area = cover.setdefault(key, [0.0, 0.0])
        area[0 if manhattan else 1] += poly.area
tree = shapely.STRtree(footprints)
print(f"{len(footprints)} buildings, {len(cover)} cells with buildings")

# Each 100 m cell inside the border and above water gets its density's count, at random spots in it.
bx0, by0, bx1, by1 = border.bounds
gx = np.arange(int(bx0 // CELL), int(bx1 // CELL) + 1)
gy = np.arange(int(by0 // CELL), int(by1 // CELL) + 1)
GX, GY = np.meshgrid(gx, gy)
GX, GY = GX.ravel(), GY.ravel()
centres_x, centres_y = (GX + 0.5) * CELL, (GY + 0.5) * CELL
on_land = shapely.contains_xy(border, centres_x, centres_y) & (ground_cm(centres_x, centres_y) >= WATER_BELOW)
kinds = np.full(GX.shape, "edge", dtype=object)
for i in np.flatnonzero(on_land):
    m, other = cover.get((GX[i], GY[i]), (0.0, 0.0))
    if m + other >= BUILT_COVER * CELL * CELL:
        kinds[i] = "manhattan" if m > other else "built"
want = np.array([PER_KM2[k] * (CELL / 100000) ** 2 for k in kinds]) * on_land
cells_by_kind = {k: int(np.sum(on_land & (kinds == k))) for k in PER_KM2}

# Groups (GDD section 8, hordes): small groups of 3-10 everywhere, and HORDE_SHARE of the zombies in roaming hordes
# of 30-100 in the built-up areas. Each zombie: a spot within GROUP_SPREAD (hordes HORDE_SPREAD) of its group's centre.
members = []  # (cell, centre x, centre y, group id, spread)
group = 0
for i in np.flatnonzero(want > 0):
    for _ in range(rng.poisson(want[i] * (1 - HORDE_SHARE) / 6.5)):  # 6.5: the average of 3-10
        cx, cy = (GX[i] + rng.random()) * CELL, (GY[i] + rng.random()) * CELL
        members += [(i, cx, cy, group, GROUP_SPREAD)] * int(rng.integers(3, 11))
        group += 1
built = np.flatnonzero((kinds != "edge") & on_land)
hordes, horde_left = 0, int(want.sum() * HORDE_SHARE)
while horde_left > 0:
    i = rng.choice(built, p=want[built] / want[built].sum())
    size = min(horde_left, int(rng.integers(30, 101)))
    cx, cy = (GX[i] + rng.random()) * CELL, (GY[i] + rng.random()) * CELL
    members += [(i, cx, cy, HORDE_BIT | hordes, HORDE_SPREAD)] * size
    horde_left -= size
    hordes += 1

M = np.array([(c, x, y, sp) for c, x, y, g, sp in members], dtype=np.float64)
gids = np.array([g for c, x, y, g, sp in members], dtype=np.uint32)
cells = M[:, 0].astype(int)
points, groups_out = [], []
by_kind = {k: 0 for k in PER_KM2}
todo = np.arange(len(M))
for attempt in range(16):  # a spot in a building, in water or past the border: another spot, a little farther out
    if len(todo) == 0:
        break
    a, r = rng.random(len(todo)) * 2 * np.pi, np.sqrt(rng.random(len(todo))) * M[todo, 3] * (1 + attempt * 0.3)
    x, y = M[todo, 1] + np.cos(a) * r, M[todo, 2] + np.sin(a) * r
    z = ground_cm(x, y)
    inside = np.zeros(len(x), dtype=bool)
    hits = tree.query(shapely.points(x, y), predicate="intersects")
    inside[hits[0]] = True
    ok = ~inside & (z >= WATER_BELOW) & shapely.contains_xy(border, x, y)
    for j in np.flatnonzero(ok):
        points.append((x[j], y[j], z[j]))
        groups_out.append(gids[todo[j]])
        by_kind[kinds[cells[todo[j]]]] += 1
    todo = todo[~ok]
print(f"Not placed after 16 tries: {len(todo)}")

# Refill entry points (section 8, how many and where): along the wall's land stretches (roads and connectors, not
# water) every ENTRY_STEP, ENTRY_IN inside the border, on land and not in a building.
entries = []
for f in border_json["features"]:
    if f["properties"].get("kind") in ("road", "connector", "placeholder"):
        line = shapely.LineString([((e - e0) * 100, -(n - n0) * 100) for e, n in (to_utm.TransformPoint(lon, lat)[:2] for lon, lat in f["geometry"]["coordinates"])])
        for d in np.arange(ENTRY_STEP / 2, line.length, ENTRY_STEP):
            p, q = line.interpolate(d), line.interpolate(min(d + 100, line.length))
            t = np.array([q.x - p.x, q.y - p.y])
            if np.hypot(*t) < 1:
                continue
            nrm = np.array([-t[1], t[0]]) / np.hypot(*t) * ENTRY_IN
            for sx, sy in ((p.x + nrm[0], p.y + nrm[1]), (p.x - nrm[0], p.y - nrm[1])):
                if shapely.contains_xy(border, sx, sy) and ground_cm(np.array([sx]), np.array([sy]))[0] >= WATER_BELOW and not len(tree.query(shapely.Point(sx, sy), predicate="intersects")):
                    entries.append((sx, sy, float(ground_cm(np.array([sx]), np.array([sy]))[0])))
                    break

# Subway entrances (section 8): each street entrance inside the border, on land and not inside a building (some are in
# a building's ground floor: those would put a zombie inside its walls), one per 5 m.
subway, seen = [], set()
with open(SUBWAY, encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        e, n = to_utm.TransformPoint(float(row["Entrance Longitude"]), float(row["Entrance Latitude"]))[:2]
        x, y = (e - e0) * 100, -(n - n0) * 100
        key = (round(x / 500), round(y / 500))
        if key in seen or not shapely.contains_xy(border, x, y) or len(tree.query(shapely.Point(x, y), predicate="intersects")):
            continue
        z = float(ground_cm(np.array([x]), np.array([y]))[0])
        if z >= WATER_BELOW:
            seen.add(key)
            subway.append((x, y, z))

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "wb") as f:
    f.write(b"NYZZ" + struct.pack("<II", 3, len(points)))
    rows = np.zeros(len(points), dtype=[("x", "<f4"), ("y", "<f4"), ("z", "<f4"), ("g", "<u4")])
    rows["x"], rows["y"], rows["z"] = np.asarray(points).T
    rows["g"] = np.asarray(groups_out, dtype=np.uint32)
    f.write(rows.tobytes())
    for points_list in (entries, subway):
        f.write(struct.pack("<I", len(points_list)))
        f.write(np.asarray(points_list, dtype="<f4").reshape(-1, 3).tobytes())
for k in PER_KM2:
    print(f"  {k}: {by_kind[k]} zombies over {cells_by_kind[k] / 100:.0f} km2")
in_hordes = int(np.sum((np.asarray(groups_out, dtype=np.uint32) & HORDE_BIT) != 0))
print(f"{len(points)} zombies in {group} small groups and {hordes} roaming hordes ({in_hordes} in hordes); {len(entries)} refill entry points along the wall and {len(subway)} at subway entrances -> {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)")

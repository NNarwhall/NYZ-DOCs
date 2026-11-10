"""Fetches one real NYC block's building outlines from OpenStreetMap for the dense test block (GDD section 24,
milestone 1 point 2) and writes them in Unreal coordinates to the game repo's Tools/data/test_block.json, where
NYZ/Tools/build_test_block.py turns them into grey buildings. Run with QGIS's Python (needs osgeo):

  "C:\\Program Files\\QGIS 4.2.2\\bin\\o4w_env.bat" && python "C:\\Game Dev Folder\\NYZ\\tools\\map\\fetch_block.py"

The block is the one holding the address below: the buildings touching each other there, since streets separate blocks.
Each building gets its outline and the smallest rectangle around it (the generator builds on the rectangle).
"""
import json
import math
import pathlib
import subprocess
import time
import urllib.parse
import xml.etree.ElementTree as ET

from osgeo import ogr, osr

ADDRESS = "268 East 10th Street, New York, NY"  # the Russian and Turkish Baths: E 9th-10th St, 1st Ave-Ave A
ROOT = pathlib.Path(__file__).resolve().parents[2]
TERRAIN = json.loads((ROOT / "terrain/NYZ_terrain.json").read_text(encoding="utf-8"))
OUT = ROOT / "NYZ/Tools/data/test_block.json"
UA = "NYZ-map-draft/0.1 (solo game dev test block)"
FLOOR_M = 3.2  # used only when OSM has floors but no height


def get(url):
    time.sleep(2)  # Nominatim and the OSM API ask for at most about 1 request a second
    return subprocess.run(["curl", "-s", "-m", "120", "-A", UA, url], capture_output=True, check=True).stdout


def hull(pts):
    pts = sorted(set(pts))
    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and (out[-1][0] - out[-2][0]) * (p[1] - out[-2][1]) - (out[-1][1] - out[-2][1]) * (p[0] - out[-2][0]) <= 0:
                out.pop()
            out.append(p)
        return out[:-1]
    return half(pts) + half(pts[::-1])


def min_rectangle(pts):
    """Smallest rectangle around the points: (centre x, y, angle of its long side in degrees, long, short)."""
    h = hull(pts)
    best = None
    for (x0, y0), (x1, y1) in zip(h, h[1:] + h[:1]):
        a = math.atan2(y1 - y0, x1 - x0)
        c, s = math.cos(a), math.sin(a)
        us = [x * c + y * s for x, y in h]
        vs = [-x * s + y * c for x, y in h]
        area = (max(us) - min(us)) * (max(vs) - min(vs))
        if best is None or area < best[0]:
            u, v = (max(us) + min(us)) / 2, (max(vs) + min(vs)) / 2
            best = (area, u * c - v * s, u * s + v * c, a, max(us) - min(us), max(vs) - min(vs))
    _, cx, cy, a, du, dv = best
    if dv > du:  # make the angle point along the long side
        a, du, dv = a + math.pi / 2, dv, du
    return cx, cy, math.degrees(a) % 180, du, dv


hit = json.loads(get("https://nominatim.openstreetmap.org/search?format=jsonv2&" + urllib.parse.urlencode({"q": ADDRESS})))[0]
lat, lon = float(hit["lat"]), float(hit["lon"])
root = ET.fromstring(get(f"https://api.openstreetmap.org/api/0.6/map?bbox={lon - 0.002},{lat - 0.0015},{lon + 0.002},{lat + 0.0015}"))

src, dst = osr.SpatialReference(), osr.SpatialReference()
src.ImportFromEPSG(4326)
dst.ImportFromEPSG(32618)  # UTM zone 18N, as the terrain
for sr in (src, dst):
    sr.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
to_utm = osr.CoordinateTransformation(src, dst)
e0, n0 = TERRAIN["world_origin_utm18n_m"]["easting"], TERRAIN["world_origin_utm18n_m"]["northing"]


def unreal(lon_, lat_):  # cm; +X east, +Y south, as the terrain
    e, n = to_utm.TransformPoint(lon_, lat_)[:2]
    return (e - e0) * 100, -(n - n0) * 100


nodes = {n.get("id"): unreal(float(n.get("lon")), float(n.get("lat"))) for n in root.iter("node")}
buildings = []
for w in root.iter("way"):
    tags = {t.get("k"): t.get("v") for t in w.iter("tag")}
    refs = [nd.get("ref") for nd in w.iter("nd")]
    if "building" not in tags or len(refs) < 4 or refs[0] != refs[-1] or not all(r in nodes for r in refs):
        continue
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for r in refs:
        ring.AddPoint_2D(*nodes[r])
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    height = float(tags["height"]) if "height" in tags else float(tags.get("building:levels", 5)) * FLOOR_M
    buildings.append({"osm_way": int(w.get("id")), "poly": poly, "pts": [nodes[r] for r in refs[:-1]], "height_m": height})

# The block: buildings touching (within 1 m of) each other, starting from the one nearest the address.
qx, qy = unreal(lon, lat)
here = ogr.Geometry(ogr.wkbPoint)
here.AddPoint_2D(qx, qy)
block = [min(buildings, key=lambda b: b["poly"].Distance(here))]
rest = [b for b in buildings if b is not block[0]]
grew = True
while grew:
    near = [b for b in rest if any(b["poly"].Distance(k["poly"]) < 100 for k in block)]
    grew = bool(near)
    block += near
    rest = [b for b in rest if b not in near]
assert 10 <= len(block) <= 80, f"{len(block)} buildings: not one ordinary block, check the address"

out = []
for b in block:
    cx, cy, angle, long_cm, short_cm = min_rectangle(b["pts"])
    out.append({"osm_way": b["osm_way"], "centre_cm": [round(cx), round(cy)], "angle_deg": round(angle, 2),
                "size_cm": [round(long_cm), round(short_cm)], "height_m": round(b["height_m"], 1),
                "outline_cm": [[round(x), round(y)] for x, y in b["pts"]]})
xs = [p[0] for b in out for p in b["outline_cm"]]
ys = [p[1] for b in out for p in b["outline_cm"]]
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({
    "source": f"OpenStreetMap, the block holding {ADDRESS}, fetched {time.strftime('%Y-%m-%d')}",
    "licence": "(c) OpenStreetMap contributors, ODbL: credit OpenStreetMap in the game",
    "bounds_cm": [min(xs), min(ys), max(xs), max(ys)],
    "buildings": out}, indent=1), encoding="utf-8")
print(f"{len(out)} buildings, {(max(xs) - min(xs)) / 100:.0f} x {(max(ys) - min(ys)) / 100:.0f} m, "
      f"heights {min(b['height_m'] for b in out)}-{max(b['height_m'] for b in out)} m -> {OUT}")

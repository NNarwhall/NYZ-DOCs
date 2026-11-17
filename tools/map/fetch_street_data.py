"""Fetches the street data the showcase street needs (GDD section 24, map stage 1), each once:
  terrain/hydrants/hydrants.csv     NYC Open Data's "Hydrants" (DEP, 5bgh-vtsn): every city hydrant, its ID and position
                                    (state plane feet, as the tree census). About 4 MB; used city-wide later.
  terrain/streets/showcase_osm.json OpenStreetMap's streets around the test block (lanes, one-way, bike and bus lanes,
                                    crossings, traffic signals), in Unreal cm.
Run with QGIS's Python (needs osgeo):

  "C:\\Program Files\\QGIS 4.2.2\\bin\\o4w_env.bat" && python "C:\\Game Dev Folder\\NYZ\\tools\\map\\fetch_street_data.py"
"""
import json
import pathlib
import subprocess
import time
import xml.etree.ElementTree as ET

from osgeo import osr

osr.UseExceptions()

ROOT = pathlib.Path(__file__).resolve().parents[2]
TERRAIN = json.loads((ROOT / "terrain/NYZ_terrain.json").read_text(encoding="utf-8"))
BLOCK = json.loads((ROOT / "NYZ/Tools/data/test_block.json").read_text(encoding="utf-8"))
HYDRANTS = ROOT / "terrain/hydrants/hydrants.csv"
OSM = ROOT / "terrain/streets/showcase_osm.json"
UA = "map-data-fetch/0.1"
MARGIN = 8000  # cm around the test block: its four streets, their far sidewalks and the four intersections


def get(url):
    time.sleep(2)  # the OSM API asks for at most about 1 request a second
    return subprocess.run(["curl", "-s", "-f", "-m", "300", "-A", UA, url], capture_output=True, check=True).stdout


if not HYDRANTS.exists():
    HYDRANTS.parent.mkdir(parents=True, exist_ok=True)
    data = get("https://data.cityofnewyork.us/resource/5bgh-vtsn.csv?$select=unitid,point_x,point_y&$limit=500000")
    assert data.count(b"\n") > 100000, "the hydrant list came back short"
    HYDRANTS.write_bytes(data)
    print(f"hydrants: {data.count(b'\n') - 1:,} ({len(data) / 1e6:.1f} MB) -> {HYDRANTS}")

wgs, utm = osr.SpatialReference(), osr.SpatialReference()
wgs.ImportFromEPSG(4326)
utm.ImportFromEPSG(32618)  # UTM zone 18N, as the terrain
for sr in (wgs, utm):
    sr.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
to_utm, to_wgs = osr.CoordinateTransformation(wgs, utm), osr.CoordinateTransformation(utm, wgs)
e0, n0 = TERRAIN["world_origin_utm18n_m"]["easting"], TERRAIN["world_origin_utm18n_m"]["northing"]


def unreal(lon, lat):  # cm; +X east, +Y south, as the terrain
    e, n = to_utm.TransformPoint(lon, lat)[:2]
    return [round((e - e0) * 100), round(-(n - n0) * 100)]


x0, y0, x1, y1 = BLOCK["bounds_cm"]
corners = [to_wgs.TransformPoint(e0 + x / 100, n0 - y / 100)[:2] for x in (x0 - MARGIN, x1 + MARGIN) for y in (y0 - MARGIN, y1 + MARGIN)]
lons, lats = [c[0] for c in corners], [c[1] for c in corners]
data = get(f"https://api.openstreetmap.org/api/0.6/map?bbox={min(lons):.6f},{min(lats):.6f},{max(lons):.6f},{max(lats):.6f}")
root = ET.fromstring(data)
nodes = {n.get("id"): n for n in root.iter("node")}
tags = lambda e: {t.get("k"): t.get("v") for t in e.iter("tag")}  # noqa: E731
ways = [{"id": int(w.get("id")), "tags": tags(w),
         "points_cm": [unreal(float(nodes[r].get("lon")), float(nodes[r].get("lat"))) for r in (nd.get("ref") for nd in w.iter("nd")) if r in nodes]}
        for w in root.iter("way") if "highway" in tags(w)]
points = [{"id": int(n.get("id")), "tags": tags(n), "cm": unreal(float(n.get("lon")), float(n.get("lat")))}
          for n in nodes.values() if {"highway", "crossing", "amenity"} & set(tags(n))]
OSM.parent.mkdir(parents=True, exist_ok=True)
OSM.write_text(json.dumps({"source": f"OpenStreetMap API, around the test block, fetched {time.strftime('%Y-%m-%d')} ({len(data) / 1e6:.2f} MB)",
                           "licence": "(c) OpenStreetMap contributors, ODbL: credit OpenStreetMap in the game",
                           "units": "cm, Unreal map coordinates: +X east, +Y south", "ways": ways, "points": points}, indent=1), encoding="utf-8")
print(f"OpenStreetMap: {len(data) / 1e6:.2f} MB, {len(ways)} street ways, {len(points)} tagged points -> {OSM}")

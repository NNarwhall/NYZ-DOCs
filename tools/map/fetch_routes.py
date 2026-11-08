"""Fetch wall-road geometry without Overpass: Nominatim finds a way on each road, the main
OSM API returns that way's route relation in full. Streets with no route relation fall back
to every Nominatim match for the name. Output matches Overpass JSON so inspect_roads.py works."""
import json, subprocess, sys, time, urllib.parse
import xml.etree.ElementTree as ET

UA = "NYZ-map-draft/0.1 (solo game dev border draft)"
ROADS = {  # label -> Nominatim query
    "Cross County Parkway": "Cross County Parkway, Yonkers, NY",
    "Hutchinson River Parkway": "Hutchinson River Parkway, Bronx, NY",
    "Saw Mill River Parkway": "Saw Mill River Parkway, Yonkers, NY",
    "Cross Island Parkway": "Cross Island Parkway, Queens, NY",
    "Belt Parkway": "Belt Parkway, Queens, NY",
    "New Jersey Turnpike": "New Jersey Turnpike, Secaucus, NJ",
    "Staten Island Expressway": "Staten Island Expressway, Staten Island, NY",
    "Clove Road": "Clove Road, Staten Island, NY",
    "Yonkers Avenue": "Yonkers Avenue, Yonkers, NY",
    "Nassau Expressway": "Nassau Expressway, Queens, NY",
    "Rockaway Turnpike": "Rockaway Turnpike, Lawrence, NY",
    # v2: New Jersey
    "Grand Avenue": "Grand Avenue, Palisades Park, NJ",
    "Broad Avenue": "Broad Avenue, Palisades Park, NJ",
    "Tonnelle Avenue": "Tonnelle Avenue, North Bergen, NJ",
    "Fort Lee Road": "Fort Lee Road, Leonia, NJ",
    "Main Street (Fort Lee)": "Main Street, Fort Lee, NJ",
    "Pulaski Skyway": "Pulaski Skyway, Jersey City, NJ",
    # v2: north Bronx
    "McLean Avenue": "McLean Avenue, Yonkers, NY",
    "East 233rd Street": "East 233rd Street, Bronx, NY",
    "East 241st Street": "East 241st Street, Bronx, NY",
    "Boston Road": "Boston Road, Bronx, NY",
    # v2: east Queens and the Rockaways
    "Clearview Expressway": "Clearview Expressway, Queens, NY",
    "Francis Lewis Boulevard": "Francis Lewis Boulevard, Queens, NY",
    "Rockaway Boulevard": "Rockaway Boulevard, Queens, NY",
    "Springfield Boulevard": "Springfield Boulevard, Queens, NY",
    "Seagirt Boulevard": "Seagirt Boulevard, Queens, NY",
    "Beach 9th Street": "Beach 9th Street, Queens, NY",
}
if len(sys.argv) > 2:  # optional: only fetch the labels given after the output path
    ROADS = {k: v for k, v in ROADS.items() if k in sys.argv[2:]}

def get(url):
    time.sleep(2)  # Nominatim and OSM API ask for at most ~1 request/second; stay well under it
    return subprocess.run(["curl", "-s", "-m", "120", "-A", UA, url], capture_output=True, check=True).stdout

def nominatim(q, extra=""):
    url = "https://nominatim.openstreetmap.org/search?format=jsonv2&" + urllib.parse.urlencode({"q": q}) + extra
    for wait in (5, 15, 45, 90):  # Nominatim answers with an HTML error page when it throttles
        body = get(url)
        if body.lstrip().startswith(b"["):
            return json.loads(body)
        print(f"  throttled, retrying in {wait}s")
        time.sleep(wait)
    raise RuntimeError(f"Nominatim kept refusing: {body[:120]!r}")

def relation_ways(rel_id, label):
    root = ET.fromstring(get(f"https://api.openstreetmap.org/api/0.6/relation/{rel_id}/full"))
    nodes = {n.get("id"): (float(n.get("lon")), float(n.get("lat"))) for n in root.iter("node")}
    for w in root.iter("way"):
        pts = [nodes[nd.get("ref")] for nd in w.iter("nd") if nd.get("ref") in nodes]
        if len(pts) > 1:
            yield {"tags": {"name": label}, "geometry": [{"lon": x, "lat": y} for x, y in pts]}

elements = []
for label, q in ROADS.items():
    hits = [h for h in nominatim(q, "&limit=5") if h["osm_type"] == "way" and h["category"] == "highway"]
    if not hits:
        print(f"{label}: not found"); continue
    rels = ET.fromstring(get(f"https://api.openstreetmap.org/api/0.6/way/{hits[0]['osm_id']}/relations"))
    routes = [r for r in rels.iter("relation")
              if {t.get("k"): t.get("v") for t in r.iter("tag")}.get("route") == "road"]
    if routes:
        rid = routes[0].get("id")
        ways = list(relation_ways(rid, label))
        print(f"{label}: route relation {rid}, {len(ways)} ways")
    else:  # plain street: take every way Nominatim knows by this name
        found = nominatim(q, "&limit=50&dedupe=0&polygon_geojson=1")
        ways = [{"tags": {"name": label}, "geometry": [{"lon": x, "lat": y} for x, y in h["geojson"]["coordinates"]]}
                for h in found if h.get("geojson", {}).get("type") == "LineString"]
        print(f"{label}: no route relation, {len(ways)} ways from search")
    elements += ways

json.dump({"elements": elements}, open(sys.argv[1], "w"))

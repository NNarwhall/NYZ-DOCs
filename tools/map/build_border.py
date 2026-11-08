"""Build the NYZ map border (quarantine wall) from OpenStreetMap roads.

Run:  python build_border.py            (needs shapely; reads cache/*.json from fetch_routes.py)
Writes docs/map/border-draft.geojson, border-draft.kml and preview.html.

The border is a list of SEGMENTS, walked clockwise:
  ("road", name, from, to)    follows that road between the points nearest `from` and `to`
  ("water", [points])          straight lines through water
  ("placeholder", [points])    straight lines over land that still need a real road
  ("connector", [points])      straight lines over land the developer accepted without a road
Points are (lat, lon). A road endpoint given as ("meet", other_road) snaps to where the two roads meet.
"""
import heapq, json, math, pathlib
from shapely.geometry import LineString, Point, Polygon, mapping
from shapely.ops import linemerge, substring, nearest_points
from shapely.validation import explain_validity

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent.parent / "docs" / "map"
VERSION = "v2"

# v2 applies docs/map/border-notes.md items 1-5 (2026-10-27)
SEGMENTS = [
    # North Bronx: roughly the city line; Co-op City and Bay Plaza stay inside
    ("connector", [(40.9055, -73.9200), (40.8953, -73.8796)]),  # Hudson at Riverdale to E 233rd St
    ("road", "East 233rd Street", (40.8953, -73.8796), (40.8892, -73.8313)),
    ("connector", [(40.8903, -73.8208)]),  # end of 233rd to Eastchester Bridge
    ("road", "Hutchinson River Parkway", (40.8903, -73.8150), (40.8750, -73.8200)),
    ("placeholder", [(40.8750, -73.7900)]),  # from the Hutch across Pelham Bay Park to the Sound
    # East: down the Sound east of the Throgs Neck Bridge, into Little Neck Bay (Fort Totten stays in)
    ("water", [(40.8750, -73.7750), (40.8300, -73.7700), (40.8026, -73.7724), (40.7955, -73.7703),
               (40.7863, -73.7677)]),
    ("road", "Cross Island Parkway", (40.7844, -73.7693), (40.7882, -73.7905)),
    ("road", "Clearview Expressway", (40.7882, -73.7905), (40.7247, -73.7541)),
    ("connector", [(40.7210, -73.7593)]),  # Clearview's end to Francis Lewis Blvd
    ("road", "Francis Lewis Boulevard", (40.7210, -73.7593), (40.6961, -73.7461)),
    ("road", "Springfield Boulevard", (40.6961, -73.7461), (40.6594, -73.7613)),
    ("road", "Rockaway Boulevard", ("meet", "Springfield Boulevard"), (40.6556, -73.7661)),  # JFK's east edge
    ("connector", [(40.6397, -73.7424)]),  # rest of Rockaway Blvd along JFK (missing from the fetched data)
    # Jamaica Bay's east end (Head of Bay) down to Far Rockaway, then Beach 9th St to the ocean
    ("water", [(40.6319, -73.7550), (40.6263, -73.7624), (40.6208, -73.7634),
               (40.6152, -73.7613), (40.6118, -73.7571)]),
    ("connector", [(40.6111, -73.7508)]),  # Mott Basin to Beach 9th St along the city line
    ("road", "Beach 9th Street", (40.6091, -73.7468), (40.5951, -73.7437)),
    # South: ocean, around Breezy Point, Lower Bay
    ("water", [(40.5880, -73.7440), (40.5720, -73.8000), (40.5650, -73.8500), (40.5520, -73.9000),
               (40.5400, -73.9350), (40.5430, -73.9650), (40.5650, -74.0100), (40.5850, -74.0400),
               (40.5970, -74.0520)]),
    ("placeholder", [(40.6037, -74.0679)]),  # Fort Wadsworth shore to the expressway
    ("road", "Staten Island Expressway", (40.6037, -74.0679), ("meet", "Clove Road")),
    ("road", "Clove Road", ("meet", "Staten Island Expressway"), (40.6372, -74.1268)),
    ("water", [(40.6430, -74.1250), (40.6460, -74.1450), (40.6650, -74.1500), (40.6850, -74.1400),
               (40.7000, -74.1250), (40.7200, -74.1050), (40.7349, -74.0972)]),  # Kill Van Kull, Newark Bay, Hackensack
    # New Jersey: Pulaski Skyway / Tonnelle Ave (both US 1-9) -> Broad Ave -> Grand Ave -> Fort Lee Rd -> GWB
    ("road", "Pulaski Skyway", (40.7349, -74.0972), (40.8415, -74.0025)),
    ("road", "Broad Avenue", (40.8415, -74.0025), (40.8605, -73.9888)),
    ("connector", [(40.8639, -73.9925)]),  # end of Broad Ave across to Grand Ave
    ("road", "Grand Avenue", (40.8639, -73.9925), (40.8642, -73.9923)),
    ("road", "Fort Lee Road", (40.8642, -73.9923), (40.8579, -73.9804)),
    ("road", "Pulaski Skyway", (40.8579, -73.9804), (40.8573, -73.9733)),  # US 1-9 to the GWB plaza
    # Hudson: meet the river north of the GWB so the bridge stays crossable, then up to Riverdale
    ("connector", [(40.8565, -73.9600)]),  # north of the bridge approach to the cliff edge
    ("water", [(40.8560, -73.9530), (40.8750, -73.9380), (40.9050, -73.9220)]),
]
STITCH = {"Clove Road"}  # streets that come back as loose fragments, chained end to end

def load_roads():
    roads = {}
    for f in sorted((HERE / "cache").glob("*.json")):
        for el in json.load(open(f))["elements"]:
            roads.setdefault(el["tags"]["name"], []).append(
                LineString([(p["lon"], p["lat"]) for p in el["geometry"]]))
    return roads

def stitch(pieces):
    """Chain loose fragments into one line by always attaching the nearest free end."""
    rest = [list(p.coords) for p in pieces]
    mid = (sum(c[0][0] for c in rest) / len(rest), sum(c[0][1] for c in rest) / len(rest))
    # start from the loose end farthest from the middle, so the chain only ever grows one way
    _, i, flip = max([(math.dist(mid, c[0]), i, False) for i, c in enumerate(rest)] +
                     [(math.dist(mid, c[-1]), i, True) for i, c in enumerate(rest)])
    chain = rest.pop(i)[::-1] if flip else rest.pop(i)
    while rest:
        best = min([(math.dist(chain[-1], c[0]), i, False) for i, c in enumerate(rest)] +
                   [(math.dist(chain[-1], c[-1]), i, True) for i, c in enumerate(rest)])
        c = rest.pop(best[1])
        chain += c[::-1] if best[2] else c
    return LineString(chain)

def road_line(roads, name):
    merged = linemerge(roads[name])
    pieces = list(merged.geoms) if merged.geom_type == "MultiLineString" else [merged]
    return [stitch(sorted(pieces, key=lambda p: -p.length))] if name in STITCH else pieces

def resolve(roads, pt, name):
    if pt[0] != "meet":
        return Point(pt[1], pt[0])
    best = min(((x.distance(y), x, y) for x in road_line(roads, name) for y in road_line(roads, pt[1])),
               key=lambda t: t[0])
    return nearest_points(best[1], best[2])[0]

LON_SCALE = math.cos(math.radians(40.7))  # a degree of longitude is shorter than a degree of latitude here
HOP = 0.0006   # ~65 m: lets the path step between the two one-way halves of a divided road
GAP = 0.004    # ~440 m: bridges holes between loose fragments (search results miss some ways)

def dist(u, v):
    return math.hypot((u[0] - v[0]) * LON_SCALE, u[1] - v[1])

def road_graph(lines, gap):
    graph = {}
    for l in lines:
        for u, v in zip(l.coords, l.coords[1:]):
            graph.setdefault(u, []).append((v, dist(u, v)))
            graph.setdefault(v, []).append((u, dist(u, v)))
    ends = [n for n, e in graph.items() if len(e) == 1]
    grid = {}
    for n in graph:
        grid.setdefault((int(n[0] // HOP), int(n[1] // HOP)), []).append(n)
    for n in list(graph):
        cx, cy = int(n[0] // HOP), int(n[1] // HOP)
        for gx in (cx - 1, cx, cx + 1):
            for gy in (cy - 1, cy, cy + 1):
                for m in grid.get((gx, gy), ()):
                    if m != n and dist(n, m) < HOP:
                        graph[n].append((m, dist(n, m)))
    # bridge fragment gaps: link each loose end to the nearest end of a *different* piece,
    # penalized so the real road is always preferred where it exists
    parent = {n: n for n in graph}
    def root(n):
        while parent[n] != n:
            parent[n] = parent[parent[n]]
            n = parent[n]
        return n
    for n, edges in graph.items():
        for m, _ in edges:
            parent[root(n)] = root(m)
    for n in ends:
        near = [m for m in ends if root(m) != root(n) and dist(n, m) < gap]
        if near:
            m = min(near, key=lambda m: dist(n, m))
            graph[n].append((m, 2 * dist(n, m)))
            graph[m].append((n, 2 * dist(n, m)))
            parent[root(n)] = root(m)
    return graph

def shortest_path(roads, name, pa, pb, gap=GAP):
    """Follow the road's own ways from the node nearest pa to the node nearest pb (Dijkstra).
    Returns None when those nodes aren't connected."""
    graph = road_graph(roads[name], gap)
    start = min(graph, key=lambda n: dist(n, (pa.x, pa.y)))
    goal = min(graph, key=lambda n: dist(n, (pb.x, pb.y)))
    best, prev, todo = {start: 0.0}, {}, [(0.0, start)]
    while todo:
        d, n = heapq.heappop(todo)
        if n == goal:
            path = [n]
            while path[-1] in prev:
                path.append(prev[path[-1]])
            return path[::-1]
        if d > best[n]:
            continue
        for m, w in graph[n]:
            if d + w < best.get(m, math.inf):
                best[m], prev[m] = d + w, n
                heapq.heappush(todo, (d + w, m))
    return None

def cut(roads, name, a, b):
    pa, pb = resolve(roads, a, name), resolve(roads, b, name)
    for gap in (GAP, 2 * GAP, 4 * GAP):  # widen gap bridging only when the fragments don't connect
        path = shortest_path(roads, name, pa, pb, gap)
        if path and len(path) > 1:
            return path
    # fallback: the single merged piece that passes closest to both ends
    line = min(road_line(roads, name), key=lambda l: l.distance(pa) + l.distance(pb))
    da, db = line.project(pa), line.project(pb)
    part = substring(line, min(da, db), max(da, db))
    coords = list(part.coords)
    return coords if da <= db else coords[::-1]

def km2(poly):
    k = math.cos(math.radians(40.7))  # local flat projection; error well under 1% at this size
    return Polygon([(x * 111.32 * k, y * 110.54) for x, y in poly.exterior.coords]).area

def main():
    roads = load_roads()
    ring, features = [], []
    for seg in SEGMENTS:
        if seg[0] == "road":
            coords = cut(roads, seg[1], seg[2], seg[3])
            label = seg[1]
        else:
            coords = [(lon, lat) for lat, lon in seg[1]]
            label = seg[0]
        shown = ring[-1:] + coords  # start each drawn piece where the last one ended, so the line has no gaps
        ring += coords
        features.append({"type": "Feature", "geometry": {"type": "LineString", "coordinates": shown},
                         "properties": {"kind": seg[0], "name": label}})
    poly = Polygon(ring)
    if not poly.is_valid:  # still write the files so the problem can be seen on the preview
        print("WARNING border crosses itself:", explain_validity(poly))
    area = km2(poly)
    stats = {"version": VERSION, "area_km2": round(area, 1), "area_sq_mi": round(area / 2.58999, 1)}
    features.insert(0, {"type": "Feature", "geometry": mapping(poly), "properties": {"kind": "border", **stats}})
    others = [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": list(l.coords)},
               "properties": {"kind": "candidate", "name": n}}
              for n in roads for l in road_line(roads, n)]

    gj = {"type": "FeatureCollection", "features": features}
    (OUT / "border-draft.geojson").write_text(json.dumps(gj))
    kml_coords = " ".join(f"{x:.6f},{y:.6f},0" for x, y in poly.exterior.coords)
    (OUT / "border-draft.kml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document>'
        f'<name>NYZ border draft {VERSION}</name><Placemark><name>NYZ map border {VERSION}</name>'
        '<Style><LineStyle><color>ff0000ff</color><width>3</width></LineStyle>'
        '<PolyStyle><color>330000ff</color></PolyStyle></Style>'
        f'<Polygon><outerBoundaryIs><LinearRing><coordinates>{kml_coords}</coordinates>'
        '</LinearRing></outerBoundaryIs></Polygon></Placemark></Document></kml>\n')
    html = (HERE / "preview_template.html").read_text(encoding="utf-8")
    html = html.replace("/*BORDER*/null", json.dumps(gj)).replace("/*CANDIDATES*/null",
                        json.dumps({"type": "FeatureCollection", "features": others}))
    (OUT / "preview.html").write_text(html, encoding="utf-8")
    print(stats)

if __name__ == "__main__":
    main()

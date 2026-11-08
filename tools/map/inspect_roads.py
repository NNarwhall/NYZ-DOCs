"""Summarize fetched roads: per name, merged line pieces with length and endpoints."""
import json, sys, math
from collections import defaultdict
from shapely.geometry import LineString
from shapely.ops import linemerge

data = json.load(open(sys.argv[1]))
by_name = defaultdict(list)
for el in data["elements"]:
    name = el.get("tags", {}).get("name") or el.get("tags", {}).get("ref")
    by_name[name].append(LineString([(p["lon"], p["lat"]) for p in el["geometry"]]))

KM_PER_DEG_LAT, KM_PER_DEG_LON = 110.54, 111.32 * math.cos(math.radians(40.7))
for name, lines in sorted(by_name.items()):
    merged = linemerge(lines)
    parts = list(merged.geoms) if merged.geom_type == "MultiLineString" else [merged]
    parts.sort(key=lambda l: -l.length)
    print(f"\n{name}: {len(lines)} ways -> {len(parts)} pieces")
    for p in parts[:6]:
        (x0, y0), (x1, y1) = p.coords[0], p.coords[-1]
        km = sum(math.hypot((bx - ax) * KM_PER_DEG_LON, (by - ay) * KM_PER_DEG_LAT)
                 for (ax, ay), (bx, by) in zip(p.coords, p.coords[1:]))
        print(f"  {km:6.2f} km  ({y0:.4f},{x0:.4f}) -> ({y1:.4f},{x1:.4f})")

"""Placeholder dressing for the showcase street, the four streets around the test block (GDD section 24, map stage 1;
the look in section 5): road markings laid out from OpenStreetMap's lanes, hydrants at NYC's real positions, lamp posts,
signal poles with street and one-way signs, litter baskets, abandoned cars and trash bag piles. All placeholders: the
developer makes or finds the real models, and the street tool (section 5) takes this over. Called by convert_streets.py
for the district holding the test block; needs tools/map/fetch_street_data.py's two files.
"""
import csv
import json

import numpy as np
import shapely

import convert_buildings as cb
import convert_streets as cs

AROUND = 3500   # cm out from the test block's curb: its four streets, their far sidewalks and the four intersections
OSM = cb.ROOT / "terrain/streets/showcase_osm.json"
HYDRANTS = cb.ROOT / "terrain/hydrants/hydrants.csv"
TEST_BLOCK = cb.ROOT / "NYZ/Tools/data/test_block.json"
PAINT_UP = 2    # cm over the terrain (the road skin is at 1; the paint's material is also drawn further toward the camera)
# Bands across a street (cm): parking, painted bike lane, protected bike track and its buffer, bus lane, double yellow.
PARKING, BIKE, TRACK, BUFFER, BUS, CENTRE, MIN_LANE = 240, 150, 240, 90, 340, 30, 270
LINE, DASH, GAP = 10, 300, 900   # lane lines: 10 cm wide; dashes 3 m long, 9 m apart (NYC's 10 and 30 ft)
BAR, BAR_GAP, CROSSWALK = 60, 60, 400   # zebra crosswalk bars, the gaps between them, the crosswalk's width
LAMP_EVERY = 3300
LAMP_SLIDES = (0, 50, -50, 100, -100, 150, -150, 200, -200, 250, -250, 300, -300, 350, -350, 400, -400)  # cm along the curb, to clear canopies
# sRGB colours
WHITE, YELLOW, GREEN, RED = (230, 230, 222), (226, 176, 40), (62, 140, 72), (160, 52, 42)
HYDRANT, METAL, SIGNAL, BASKET = (170, 30, 25), (58, 60, 62), (95, 85, 25), (35, 62, 42)
SIGN_GREEN, SIGN_WHITE, TYRE = (20, 100, 55), (232, 232, 232), (22, 22, 22)
CARS = [(210, 210, 205), (150, 152, 155), (30, 30, 32), (70, 72, 75), (30, 45, 80), (120, 25, 25), (40, 70, 50), (230, 170, 20)]
CAR_ODDS = [0.2, 0.2, 0.15, 0.12, 0.1, 0.08, 0.05, 0.1]   # the last: yellow cabs
BAGS = [(24, 24, 26), (30, 40, 32)]


def unit(v):
    return v / np.hypot(*v)


def rect(c, u, along, across):
    """A rectangle centred on c, its `along` side on unit u."""
    n = np.array([-u[1], u[0]])
    return shapely.Polygon([c - u * along / 2 - n * across / 2, c + u * along / 2 - n * across / 2,
                            c + u * along / 2 + n * across / 2, c - u * along / 2 + n * across / 2])


def outward(tris, centre):
    """Triangles wound to face away from their object's centre (convex shapes)."""
    nrm = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    flip = np.einsum("ij,ij->i", nrm, tris.mean(1) - centre) < 0
    tris[flip] = tris[flip][:, [0, 2, 1]]
    return tris


def box(c, u, along, across, z0, z1):
    """An upright box (six sides) centred on c: 12 triangles facing out."""
    ring = np.asarray(rect(c, u, along, across).exterior.coords)[:4]
    lo, hi = np.column_stack((ring, np.full(4, z0))), np.column_stack((ring, np.full(4, z1)))
    tris = [t for i in range(4) for t in ((lo[i], lo[i - 3], hi[i - 3]), (lo[i], hi[i - 3], hi[i]))]
    tris += [(hi[0], hi[1], hi[2]), (hi[0], hi[2], hi[3]), (lo[0], lo[1], lo[2]), (lo[0], lo[2], lo[3])]
    return outward(np.array(tris, float), np.array([*c, (z0 + z1) / 2]))


def prism(c, r, z0, z1, sides=8):
    """An upright prism with a top: 3 * sides - 2 triangles facing out."""
    a = np.arange(sides) * 2 * np.pi / sides
    ring = c + r * np.column_stack((np.cos(a), np.sin(a)))
    lo, hi = np.column_stack((ring, np.full(sides, z0))), np.column_stack((ring, np.full(sides, z1)))
    tris = [t for i in range(sides) for t in ((lo[i], lo[i - 1], hi[i - 1]), (lo[i], hi[i - 1], hi[i]))]
    tris += [(hi[0], hi[i], hi[i + 1]) for i in range(1, sides - 1)]
    return outward(np.array(tris, float), np.array([*c, (z0 + z1) / 2]))


G = (1 + 5 ** 0.5) / 2
ICO_V = np.array([(-1, G, 0), (1, G, 0), (-1, -G, 0), (1, -G, 0), (0, -1, G), (0, 1, G), (0, -1, -G), (0, 1, -G),
                  (G, 0, -1), (G, 0, 1), (-G, 0, -1), (-G, 0, 1)], float) / np.hypot(1, G)
ICO_F = np.array([(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6),
                  (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7),
                  (9, 8, 1)])


def blob(centre, radii, angle):
    """A squashed 20-sided ball (a trash bag)."""
    c, s = np.cos(angle), np.sin(angle)
    v = ICO_V * radii
    v = np.column_stack((v[:, 0] * c - v[:, 1] * s, v[:, 0] * s + v[:, 1] * c, v[:, 2])) + centre
    return outward(v[ICO_F].copy(), np.asarray(centre, float))


class Props:
    """What's been placed: look-only triangles with a colour each, solid triangles, each with the point that decides its
    tile, and a list for the street tool."""

    def __init__(self):
        self.look, self.colours, self.look_at, self.solid, self.solid_at, self.items, self.taken = [], [], [], [], [], [], []

    def add(self, kind, at, angle, parts, solid=()):
        for tris, colour in parts:
            self.look.append(tris)
            self.colours.append(np.tile(colour, (len(tris), 1)))
            self.look_at.append(np.tile(at, (len(tris), 1)))
        for tris in solid:
            self.solid.append(tris)
            self.solid_at.append(np.tile(at, (len(tris), 1)))
        self.items.append({"kind": kind, "x": round(at[0]), "y": round(at[1]), "angle_deg": round(float(np.degrees(angle)) % 360, 1)})

    def arrays(self):
        cat = lambda a, shape: np.concatenate(a) if a else np.zeros(shape)  # noqa: E731
        return (cat(self.look, (0, 3, 3)), cat(self.colours, (0, 3)).astype(np.uint8), cat(self.look_at, (0, 2)),
                cat(self.solid, (0, 3, 3)), cat(self.solid_at, (0, 2)))


def layout(tags, width):
    """A street's bands across it, from its left curb facing the way's direction, from OpenStreetMap's tags:
    [(kind, from, to)] in cm from that curb; kinds parking, bike, track, buffer, bus, centre, lane (+1 with the way,
    -1 against). Travel lanes share what the rest leave; parking goes (right side first) if that's under MIN_LANE."""
    oneway = tags.get("oneway") == "yes"
    lanes = int(tags.get("lanes", 1 if oneway else 2))
    bus = min(int(tags.get("lanes:bus", 0)), 1)
    both = tags.get("cycleway") == "lane"
    track = tags.get("cycleway:left") == "track"
    parked = tags.get("parking:both", "lane") != "no"
    left = [("track", TRACK), ("buffer", BUFFER), ("parking", PARKING)] if track else \
        [("parking", PARKING)] * parked + [("bike", BIKE)] * (both or tags.get("cycleway:left") == "lane")
    right = [("bus", BUS)] if bus else [("bike", BIKE)] * (both or tags.get("cycleway:right") == "lane") + [("parking", PARKING)] * parked
    travel = lanes - bus
    while True:
        fixed = sum(w for _, w in left + right) + (0 if oneway else CENTRE)
        lane = (width - fixed) / travel
        if lane >= MIN_LANE or not any(k == "parking" for k, _ in left + right):
            break
        side = right if any(k == "parking" for k, _ in right) else left
        side.remove(("parking", PARKING))
    back = 0 if oneway else travel // 2
    middle = [("lane-", lane)] * back + ([] if oneway else [("centre", CENTRE)]) + [("lane+", lane)] * (travel - back)
    bands, at = [], 0
    for kind, w in left + middle + right:
        bands.append((kind, at, at + w))
        at += w
    return bands


def showcase(s):
    """The showcase's paint ({colour: polygon}) and props (Props), or None if the test block isn't in this district."""
    x0, y0, x1, y1 = json.loads(TEST_BLOCK.read_text(encoding="utf-8"))["bounds_cm"]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if not (OSM.exists() and HYDRANTS.exists() and shapely.contains_xy(s["outline"], cx, cy)):
        return None
    blocks = shapely.get_parts(s["blocks"])
    home = blocks[shapely.contains_xy(blocks, cx, cy)][0]
    area = shapely.buffer(home, AROUND, join_style="mitre")
    road, walk = s["road"], shapely.intersection(s["walk"], area)
    for g in (road, walk, area):
        shapely.prepare(g)
    osm = json.loads(OSM.read_text(encoding="utf-8"))
    drive = [(w["tags"], shapely.LineString(w["points_cm"])) for w in osm["ways"]
             if w["tags"].get("highway") in ("primary", "secondary", "tertiary", "residential") and len(w["points_cm"]) > 1]
    crossings = [shapely.LineString(w["points_cm"]) for w in osm["ways"] if w["tags"].get("footway") == "crossing" and len(w["points_cm"]) > 1]
    crossings = [c for c in crossings if c.intersects(area)]
    rng = np.random.default_rng(3)
    paint = {WHITE: [], YELLOW: [], GREEN: [], RED: []}

    # Crosswalks: zebra bars across each of OpenStreetMap's crossings, on the road only.
    bands = []
    for line in crossings:
        a, b = np.asarray(line.coords)[[0, -1]]
        d, length = unit(b - a), np.hypot(*(b - a))
        across = np.array([-d[1], d[0]])
        bars = [rect(a + d * t, across, CROSSWALK, BAR) for t in np.arange(BAR / 2, length, BAR + BAR_GAP)]
        paint[WHITE] += list(shapely.get_parts(shapely.intersection(shapely.union_all(bars), road)))
        bands.append((shapely.buffer(line, CROSSWALK / 2, cap_style="flat"), d))
    zebra = shapely.union_all([b for b, _ in bands]) if bands else shapely.Polygon()

    # Each stretch of road: a road piece where one street has over 75% of OpenStreetMap's line through it (else it's an
    # intersection). The city sometimes draws a stretch and the next intersection as one piece (Avenue A at East 9th
    # Street): the crossing street's box in it gets no lane lines or cars.
    pieces = [p for p in (shapely.make_valid(g) for g in s["road_piece_list"]) if p.intersects(area) and p.area > 5e5]
    stretches = []
    for piece in pieces:
        on = [(t, line, shapely.length(shapely.intersection(line, piece))) for t, line in drive]
        on = [o for o in on if o[2] > 300]
        total = {}
        for tg, _, length in on:
            total[tg.get("name")] = total.get(tg.get("name"), 0) + length
        if not total or max(total.values()) < 0.75 * sum(total.values()):
            continue
        name = max(total, key=total.get)
        tags, line, _ = max((o for o in on if o[0].get("name") == name), key=lambda o: o[2])
        boxes = shapely.union_all([shapely.buffer(ln, 650) for tg, ln, _ in on if tg.get("name") != name])
        c = np.asarray(shapely.centroid(piece).coords[0])
        along = line.project(shapely.Point(c))
        way = unit(np.asarray(line.interpolate(along + 100).coords[0]) - np.asarray(line.interpolate(along - 100).coords[0]))
        # The street's direction from its own curbs (OpenStreetMap's line can run a fraction of a degree off them: half a
        # metre at the end of a long piece): the length-weighted mean of the edges within 20 degrees of it.
        xy, ring = shapely.get_coordinates(shapely.boundary(piece), return_index=True)
        edge = (xy[1:] - xy[:-1])[ring[1:] == ring[:-1]]
        length = np.hypot(edge[:, 0], edge[:, 1])
        along_way = np.abs(edge @ way) > np.cos(np.radians(20)) * length
        mean = np.sum(length[along_way] * np.exp(2j * np.arctan2(edge[along_way, 1], edge[along_way, 0])))
        u = np.array([np.cos(np.angle(mean) / 2), np.sin(np.angle(mean) / 2)])
        u = u if u @ way > 0 else -u  # the way's direction: which side is left, which way one-way traffic goes
        n = np.array([u[1], -u[0]])  # left of the way's direction (+Y is south)
        t = (shapely.get_coordinates(piece) - c) @ u
        # Curb to curb: the median of 20 cuts across it (a corner's curve drawn into the piece mustn't widen it).
        ext = []
        for tt in np.linspace(t.min(), t.max(), 22)[1:-1]:
            cut = shapely.intersection(piece, shapely.LineString([c + u * tt + n * 5000, c + u * tt - n * 5000]))
            if not cut.is_empty:
                sv = (shapely.get_coordinates(cut) - c) @ n
                ext.append((sv.max(), sv.min()))
        left, right = np.median(ext, axis=0)
        stretches.append(dict(piece=piece, tags=tags, c=c, u=u, n=n, t0=t.min(), t1=t.max(), left=left, boxes=boxes,
                              bands=layout(tags, left - right)))

    def strip(st, s_from, s_to, t0=None, t1=None):
        """The part of a stretch between two distances from its left curb (and along it), as a polygon."""
        c, u, n = st["c"], st["u"], st["n"]
        t0, t1 = st["t0"] - 500 if t0 is None else t0, st["t1"] + 500 if t1 is None else t1
        a, b = st["left"] - s_from, st["left"] - s_to
        return shapely.Polygon([c + u * t0 + n * a, c + u * t1 + n * a, c + u * t1 + n * b, c + u * t0 + n * b])

    for st in stretches:
        clip = shapely.difference(shapely.intersection(st["piece"], area), shapely.union(shapely.buffer(zebra, 150), st["boxes"]))
        bands_ = st["bands"]
        for kind, a, b in bands_:
            if kind in ("bike", "track"):
                paint[GREEN].append(shapely.intersection(strip(st, a, b), clip))
            elif kind == "bus":
                paint[RED].append(shapely.intersection(strip(st, a, b), clip))
            elif kind == "centre":
                paint[YELLOW] += [shapely.intersection(strip(st, a + 5, a + 5 + LINE), clip), shapely.intersection(strip(st, b - 5 - LINE, b - 5), clip)]
        for (k1, _, edge), (k2, _, _) in zip(bands_, bands_[1:]):
            pair = {k1[:4], k2[:4]}
            if k1.startswith("lane") and k1 == k2:  # between lanes going the same way: dashed
                dashes = [strip(st, edge - LINE / 2, edge + LINE / 2, t, t + DASH) for t in np.arange(st["t0"], st["t1"], DASH + GAP)]
                paint[WHITE].append(shapely.intersection(shapely.union_all(dashes), clip))
            elif pair & {"bike", "bus", "buff", "trac"}:  # both edges of bike and bus lanes and the track's buffer: solid
                wide = 2 * LINE if "bus" in pair else LINE
                paint[WHITE].append(shapely.intersection(strip(st, edge - wide / 2, edge + wide / 2), clip))
        # Stop lines: 1.2 m before each crosswalk across this street, across the lanes coming to it (on a two-way street,
        # the lanes right of the centre line go with the way); one on a crosswalk's far side falls in the intersection
        # and is cut away with it.
        ci = next((i for i, (k, _, _) in enumerate(bands_) if k == "centre"), None)
        stop_clip = shapely.difference(shapely.intersection(st["piece"], area), shapely.union(zebra, st["boxes"]))
        for band, d in bands:
            if abs(d @ st["u"]) > 0.5 or not band.intersects(shapely.buffer(st["piece"], 300)):
                continue  # along this street, not across it; or elsewhere
            t = (shapely.get_coordinates(band) - st["c"]) @ st["u"]
            for way in (1, -1) if ci is not None else (1,):
                side = bands_ if ci is None else bands_[ci + 1:] if way > 0 else bands_[:ci]
                going = [(a, b) for k, a, b in side if k not in ("parking", "buffer")]
                t0 = t.min() - 180 if way > 0 else t.max() + 120
                lo, hi = min(a for a, _ in going), max(b for _, b in going)
                paint[WHITE].append(shapely.intersection(strip(st, lo, hi, t0, t0 + 60), stop_clip))

    paint = {k: shapely.union_all([g for g in v if not g.is_empty]) for k, v in paint.items() if v}
    for k in (GREEN, YELLOW, RED):  # white lines lie over the coloured lanes: one colour per spot, or they flicker
        if k in paint and WHITE in paint:
            paint[k] = shapely.difference(paint[k], paint[WHITE])
    paint = {k: cs.area([v]) for k, v in paint.items()}

    # Props, kept off ramps, tree pits, cellar doors and each other.
    props = Props()
    near = lambda arr: list(arr[shapely.intersects(arr, area)]) if len(arr) else []  # noqa: E731
    blocked = shapely.union_all(shapely.buffer(near(s["ramps"]) + near(s["pits"]) + near(s["doors"]), 20))
    shapely.prepare(blocked)
    pts, line_i = shapely.get_coordinates(shapely.intersection(shapely.boundary(road), shapely.buffer(area, 500)), return_index=True)
    same = line_i[1:] == line_i[:-1]
    curbs = shapely.linestrings(np.stack((pts[:-1][same], pts[1:][same]), 1))
    curb_tree = shapely.STRtree(curbs)

    def ground(x, y):
        return float(cs.surface(np.array([x]), np.array([y]))[0])

    trees = s["trees"][shapely.contains_xy(shapely.buffer(area, 1000), s["trees"][:, 0], s["trees"][:, 1])]
    trunk = trees[:, 3] / 2
    crown = np.where(trees[:, 2] == 0, np.clip(80 + 9 * trees[:, 3], 150, 800), trunk)  # canopy radius, as cs.tree_meshes

    def spot(p, from_curb, radius, slides=(0, 50, -50, 100, -100, 150, -150, 200, -200), canopy=False):
        """p moved onto the sidewalk from_curb in from the nearest curb, sliding along it until a disc of radius is
        clear (of trunks, or with canopy of the trees' canopies too, by 30 cm) and on the sidewalk: (point, along the
        curb, into the sidewalk) or None."""
        reach = crown + 30 if canopy else trunk
        seg = curbs[curb_tree.query_nearest(shapely.Point(p))[0]]
        a, b = np.asarray(seg.coords)
        u = unit(b - a)
        c = np.asarray(shapely.line_interpolate_point(seg, shapely.line_locate_point(seg, shapely.Point(p))).coords[0])
        n = np.array([-u[1], u[0]])
        n = n if shapely.contains_xy(walk, *(c + 50 * n)) else -n
        for d in slides:
            q = c + u * d + n * from_curb
            disc = shapely.buffer(shapely.Point(q), radius)
            if (shapely.area(shapely.intersection(disc, walk)) > 0.95 * disc.area and not blocked.intersects(disc)
                    and all(np.hypot(*(q - t[:2])) > radius + t[2] for t in props.taken)
                    and np.all(np.hypot(trees[:, 0] - q[0], trees[:, 1] - q[1]) > reach + radius)):
                props.taken.append((*q, radius))
                return q, u, n
        return None

    base = lambda q: ground(*q) + cs.WALK_UP - 6  # noqa: E731  # a little into the sidewalk: never floating

    # Hydrants at NYC's real positions (within 5 m of a curb), half a metre in from it.
    rows = list(csv.DictReader(open(HYDRANTS, encoding="utf-8")))
    hy = cb.to_unreal(np.array([(float(r["point_x"]), float(r["point_y"]), 0.0) for r in rows]))[:, :2]
    hy = hy[shapely.contains_xy(area, hy[:, 0], hy[:, 1])]
    hydrants = []
    for p in hy:
        if shapely.distance(shapely.Point(p), road) > 500 or not (got := spot(p, 50, 25)):
            continue
        q, u, n = got
        z = base(q)
        hydrants.append(q)
        props.add("hydrant", q, np.arctan2(u[1], u[0]), [
            (prism(q, 18, z, z + 12), HYDRANT), (prism(q, 12, z + 12, z + 68), HYDRANT), (prism(q, 9, z + 68, z + 82), HYDRANT),
            (box(q, u, 50, 12, z + 44, z + 56), HYDRANT)], [box(q, u, 26, 26, z - 10, z + 80)])

    # Corners: a signal pole with street-name and one-way signs, and a litter basket behind it.
    ears, k = shapely.get_parts(shapely.difference(cs.opening(blocks, 500), blocks), return_index=True)
    keep = (shapely.get_type_id(ears) == 3) & (shapely.area(ears) > 2000) & (shapely.area(ears) < 6e5) & shapely.intersects(ears, area)
    for ear, block in zip(ears[keep], blocks[k[keep]]):
        xy = np.asarray(ear.exterior.coords)[:-1]
        i = int(np.argmax(shapely.distance(shapely.points(xy), block)))
        corner = xy[i]
        curb = shapely.get_coordinates(shapely.shortest_line(block, shapely.Point(corner)))[0]
        v = unit(curb - corner)
        q = curb + v * 70
        if not shapely.contains_xy(walk, *q):
            continue
        z = base(q)
        parts = [(prism(q, 12, z, z + 520), METAL), (box(q - v * 25, v, 35, 35, z + 400, z + 510), SIGNAL),
                 (box(q + v * 20, v, 35, 35, z + 230, z + 270), SIGNAL)]
        for j, end in enumerate((xy[i - 1], xy[(i + 1) % len(xy)])):
            w = unit(end - corner)
            parts.append((box(q + w * 45, w, 90, 3, z + 330 + 26 * j, z + 352 + 26 * j), SIGN_GREEN))
            street = min(drive, key=lambda d: d[1].distance(shapely.Point(q + w * 2000 - v * 800)))
            if street[0].get("oneway") == "yes":
                parts.append((box(q + w * 45, w, 90, 3, z + 260, z + 290), SIGN_WHITE))
        props.taken.append((*q, 30))
        props.add("signal pole", q, np.arctan2(v[1], v[0]), parts, [box(q, v, 24, 24, z - 10, z + 300)])
        b = q + v * 120
        disc = shapely.buffer(shapely.Point(b), 35)
        if shapely.area(shapely.intersection(disc, walk)) > 0.95 * disc.area and not blocked.intersects(disc):
            props.taken.append((*b, 35))
            zb = base(b)
            props.add("litter basket", b, 0, [(prism(b, 30, zb, zb + 85), BASKET)], [box(b, v, 50, 50, zb - 10, zb + 85)])

    # Along each stretch's curbs: lamp posts every 33 m (the far side half a spacing on), trash bag piles every 15-35 m.
    for st in stretches:
        c, u, n = st["c"], st["u"], st["n"]
        width = sum(b - a for _, a, b in st["bands"])
        for edge, offset in ((st["left"], 0), (st["left"] - width, LAMP_EVERY / 2)):
            mid = (st["t0"] + st["t1"]) / 2 + offset
            ts = mid + LAMP_EVERY * np.arange(-10, 11)
            for t in ts[(ts > st["t0"] + 800) & (ts < st["t1"] - 800)]:
                p = c + u * t + n * edge
                if not shapely.contains_xy(area, *p) or shapely.distance(shapely.Point(p), walk) > 150 \
                        or not (got := spot(p, 60, 25, LAMP_SLIDES, canopy=True)):
                    continue
                q, uu, nn = got
                z = base(q)
                out = -nn
                props.add("lamp post", q, np.arctan2(out[1], out[0]), [
                    (prism(q, 10, z, z + 900), METAL), (box(q + out * 125, out, 250, 10, z + 870, z + 880), METAL),
                    (box(q + out * 240, out, 60, 30, z + 855, z + 870), METAL)], [box(q, out, 22, 22, z - 10, z + 300)])
            t = st["t0"] + rng.uniform(500, 2000)
            while t < st["t1"] - 500:
                p = c + u * t + n * edge
                if shapely.contains_xy(area, *p) and shapely.distance(shapely.Point(p), walk) < 150 and (got := spot(p, 75, 70, (0, 100, -100))):
                    q, uu, nn = got
                    z = base(q) + 4
                    parts = []
                    for b in range(int(rng.integers(4, 11))):
                        r = rng.uniform([22, 20, 18], [30, 26, 24])
                        at = q + uu * rng.uniform(-60, 60) + nn * rng.uniform(-25, 25)
                        lift = 0 if b < 6 else 30
                        parts.append((blob([*at, z + r[2] + lift], r, rng.uniform(0, np.pi)), BAGS[int(rng.random() < 0.25)]))
                    props.add("trash bags", q, np.arctan2(uu[1], uu[0]), parts)
                t += rng.uniform(1500, 3500)

    # Abandoned cars: most parking spots taken, a few left in the lanes.
    cars = []

    def car(q, u, length):
        footprint = rect(q, u, length + 40, 220)
        if any(footprint.intersects(o) for o in cars):
            return False
        cars.append(footprint)
        z = ground(*q) + cs.ROAD_UP
        colour = np.array(CARS[rng.choice(len(CARS), p=CAR_ODDS)])
        n = np.array([-u[1], u[0]])
        parts = [(box(q, u, length, 180, z + 25, z + 95), colour),
                 (box(q - u * 0.05 * length, u, 0.55 * length, 158, z + 95, z + 145), (colour * 0.45).astype(int))]
        parts += [(box(q + u * a * 0.32 * length + n * b * 79, u, 64, 22, z, z + 64), TYRE) for a in (-1, 1) for b in (-1, 1)]
        props.add("car", q, np.arctan2(u[1], u[0]), parts,
                  [box(q, u, length, 180, z - 10, z + 95), box(q - u * 0.05 * length, u, 0.55 * length, 158, z + 95, z + 145)])
        return True

    for st in stretches:
        clip = shapely.difference(shapely.intersection(st["piece"], area), shapely.union(shapely.buffer(zebra, 300), st["boxes"]))
        for kind, a, b in st["bands"]:
            if kind != "parking":
                continue
            lane = shapely.intersection(strip(st, a, b), clip)
            for t in np.arange(st["t0"], st["t1"], 650):
                length = rng.uniform(430, 490)
                q = st["c"] + st["u"] * (t + rng.uniform(-30, 30)) + st["n"] * (st["left"] - (a + b) / 2 + rng.uniform(-10, 10))
                body = rect(q, st["u"], length, 180)
                if (rng.random() < 0.7 and shapely.area(shapely.intersection(body, lane)) > 0.95 * body.area
                        and all(np.hypot(*(q - h)) > 450 + length / 2 for h in hydrants)):
                    car(q, st["u"], length)
        lanes = [(a, b) for k, a, b in st["bands"] if k.startswith("lane")]
        for _ in range(2 if len(lanes) > 1 else 1):
            a, b = lanes[int(rng.integers(len(lanes)))]
            t = rng.uniform(st["t0"] + 0.2 * (st["t1"] - st["t0"]), st["t1"] - 0.2 * (st["t1"] - st["t0"]))
            q = st["c"] + st["u"] * t + st["n"] * (st["left"] - (a + b) / 2)
            turn = rng.choice([-1, 1]) * np.radians(rng.uniform(15, 35))
            u = np.array([st["u"][0] * np.cos(turn) - st["u"][1] * np.sin(turn), st["u"][0] * np.sin(turn) + st["u"][1] * np.cos(turn)])
            body = rect(q, u, 460, 180)
            if shapely.area(shapely.intersection(body, clip)) > 0.9 * body.area:
                car(q, u, 460)
    return paint, props, area

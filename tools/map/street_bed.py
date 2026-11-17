"""Smooths the ground under a district's streets (GDD section 24, map stage 1). The city's height data has bumps under
the streets, ridges along building walls (laser points off the walls counted as ground) and part of the real curb, so
the road skin and sidewalks that follow it dipped and bulged, and curbs came out 12-33 cm (MN03, 2026-11-15). This
rebuilds the ground under the road from a smoothed level of the road's own middle, and under the sidewalks at the
nearest road's level (the converter's sidewalk adds the 15 cm curb on top), blending 4 m into the ground beyond (not
into buildings). The ground is lowered by at most 25 cm: past that it's a structure, not a bump (bridge approaches, the
FDR's levels, embankments and retaining walls would have come down up to 14 m in MN03), left for the decks pass. It is
raised by up to 4 m within 6 m of a building: that fills pits under a street that covers them, such as the tenements'
sunken areaways and courtyards under the sidewalk now run to the wall (the test block's walls had dips of 46 cm and more at
one spot in ten, some pits 2.3 m deep, 2026-11-15); elsewhere by at most 25 cm too (a bigger raise there was the FDR's and
the bridge approaches' low ground pulled up toward the road above it). Always from the original heights (terrain/NYZ_terrain_raw.r16, a copy
of NYZ_terrain.r16 made the first time), so rerunning a district gives the same result. Writes the street's points into
terrain/NYZ_terrain.r16 and terrain/streets/<district>_bed.json (the changed rectangle and check points) for the game
repo's Tools/update_terrain.py, which puts the new heights into the map. Called by convert_streets.py.
"""
import json
import shutil

import numpy as np
import shapely
from scipy import ndimage

import convert_buildings as cb

MAIN, RAW = cb.ROOT / "terrain/NYZ_terrain.r16", cb.ROOT / "terrain/NYZ_terrain_raw.r16"
STEP = 200            # cm between the terrain's points
SIGMA = 2             # points (4 m): how far the road's level is smoothed
KEEP = 8              # cm: road ground further than this from the smoothed level is a lump or a hole, left out
LOWER, RAISE = 25, 400  # cm: the most the ground is lowered (structures stay), raised near buildings (pits filled: a basement)
NEAR = 3              # points (6 m) from a building: where the big raise is allowed
FAR = 5               # points (10 m): sidewalk further than this from any road (plazas, paths) smooths its own ground
FEATHER = 2           # points (4 m) of blending into the ground beyond the street


def level(h, w, sigma):
    """h smoothed over the points where w is set (a normalised blur); NaN where none are near."""
    num = ndimage.gaussian_filter(np.where(w, h, 0.0), sigma)
    den = ndimage.gaussian_filter(w.astype(np.float64), sigma)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 1e-3, num / den, np.nan)


def robust(h, w, sigma):
    """level(), redone twice without the points more than KEEP from it."""
    s = level(h, w, sigma)
    for _ in range(2):
        s = level(h, w & (np.abs(h - s) < KEEP), sigma)
    return s


def smooth(s, district):
    """Smooths the ground under s's road and sidewalks; returns the number of terrain points changed."""
    if not RAW.exists() or RAW.stat().st_mtime < (cb.ROOT / "terrain/NYZ_terrain.json").stat().st_mtime:
        shutil.copyfile(MAIN, RAW)  # the first run, or the terrain was rebuilt (build_terrain.py writes the .json too)
    raw = np.memmap(RAW, dtype="<u2", mode="r", shape=(cb.VY, cb.VX))
    if s["road"].is_empty and s["walk"].is_empty:
        return 0
    x0, y0, x1, y1 = shapely.GeometryCollection([s["road"], s["walk"]]).bounds
    pad = FEATHER + 4 * SIGMA + 2
    c0, c1 = max(0, int((x0 - cb.LOC["x"]) // STEP) - pad), min(cb.VX, int((x1 - cb.LOC["x"]) // STEP) + pad + 1)
    r0, r1 = max(0, int((y0 - cb.LOC["y"]) // STEP) - pad), min(cb.VY, int((y1 - cb.LOC["y"]) // STEP) + pad + 1)
    old = raw[r0:r1, c0:c1].astype(np.float64)
    h = (old - 32768) * cb.SCALE["z"] / 128  # cm (less the map's offset)
    gx, gy = np.meshgrid(cb.LOC["x"] + STEP * np.arange(c0, c1), cb.LOC["y"] + STEP * np.arange(r0, r1))
    road = shapely.contains_xy(s["road"], gx, gy)
    walk = shapely.contains_xy(s["walk"], gx, gy) & ~road
    house = shapely.contains_xy(s["buildings"], gx, gy)

    # The road: a smoothed level of its middle (its edge row holds the curb's step and the gutter).
    inner = ndimage.distance_transform_edt(road) > 1
    level_ = robust(h, inner, SIGMA)
    level_ = np.where(np.isnan(level_), h, level_)
    new = h.copy()
    new[road] = level_[road]
    # Sidewalks: the nearest road's level; far from any road (plazas, paths), their own smoothed ground.
    d_road, (ir, ic) = ndimage.distance_transform_edt(~road, return_indices=True)
    nearest = ndimage.gaussian_filter(level_[ir, ic], 1)
    near = walk & (d_road <= FAR)
    new[near] = nearest[near]
    far = walk & (d_road > FAR)
    if far.any():
        own = robust(h, far, SIGMA)
        new[far] = np.where(np.isnan(own[far]), h[far], own[far])
    # Blend into the ground beyond. Inside a building only its first two rows of points (the sidewalk's edge is built
    # over them; the laser's ridges along walls sit there; one row missed spots where the nearest sidewalk point is two
    # steps out) follow the street (walls reach 0.5 m into the ground:
    # convert_buildings.SINK; the test block's rooms too, rebuilt on the new ground afterwards).
    street = road | walk
    d_street, (jr, jc) = ndimage.distance_transform_edt(~street, return_indices=True)
    inside = shapely.contains_xy(s["outline"], gx, gy)  # a neighbour's streets are its own (they share border streets)
    edge = ~street & inside & (d_street <= FEATHER) & (~house | (d_street < 2.5))
    weight = np.where(house[edge], 1.0, 1 - d_street[edge] / (FEATHER + 1))
    new[edge] = weight * new[jr[edge], jc[edge]] + (1 - weight) * h[edge]

    near_house = ndimage.distance_transform_edt(~house) <= NEAR
    new = h + np.clip(new - h, -LOWER, np.where(near_house, RAISE, LOWER))
    touched = street | edge
    out = np.clip(np.rint(new * 128 / cb.SCALE["z"] + 32768), 0, 65535).astype("<u2")
    changed = touched & (out != old)
    main = np.memmap(MAIN, dtype="<u2", mode="r+", shape=(cb.VY, cb.VX))
    block = main[r0:r1, c0:c1]
    block[touched] = out[touched]  # only this district's street: a neighbour's smoothing elsewhere stays
    main.flush()
    del main
    cb.HEIGHTS = np.memmap(MAIN, dtype="<u2", mode="r", shape=(cb.VY, cb.VX))  # what surface() reads from now on

    diff = np.abs(new - h)
    rows, cols = np.nonzero(changed)
    # Check points for the map: road points (no solid street over them; not in the showcase street around the test
    # block, whose parked cars are solid), the expected height there.
    bx0, by0, bx1, by1 = json.loads((cb.ROOT / "NYZ/Tools/data/test_block.json").read_text(encoding="utf-8"))["bounds_cm"]
    clear = changed & inner & ~((gx > bx0 - 8000) & (gx < bx1 + 8000) & (gy > by0 - 8000) & (gy < by1 + 8000))
    rng = np.random.default_rng(4)
    pick = rng.choice(np.flatnonzero(clear), size=min(12, int(clear.sum())), replace=False)
    pr, pc = np.unravel_index(pick, changed.shape)
    (cb.ROOT / "terrain/streets" / f"{district}_bed.json").write_text(json.dumps({
        "district": district, "heightmap": "terrain/NYZ_terrain.r16",
        "rect_points": [int(c0 + cols.min() - 1), int(r0 + rows.min() - 1), int(c0 + cols.max() + 1), int(r0 + rows.max() + 1)] if len(rows) else None,
        "changed_points": int(changed.sum()),
        "checks": [{"x": float(gx[r, c]), "y": float(gy[r, c]), "z_cm": round(float(new[r, c] + cb.LOC["z"]), 1)} for r, c in zip(pr, pc)]},
        indent=1), encoding="utf-8")
    pct = lambda a: np.round(np.percentile(a, [50, 99, 100]), 1) if a.size else "none"  # noqa: E731 (a district's slice of the map can hold no road)
    print(f"{district} street ground smoothed: {changed.sum():,} terrain points changed; how far (cm) 50/99/max: road "
          f"{pct(diff[road])}, sidewalk {pct(diff[walk])}")
    return int(changed.sum())

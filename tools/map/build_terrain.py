r"""Builds the NYC terrain heightmap for Unreal from USGS 1 m elevation tiles (GDD section 24; docs/map/terrain-notes.md).

Run with QGIS's Python, which has GDAL and numpy (one line in a command prompt):

  "C:\Program Files\QGIS 4.2.2\bin\o4w_env.bat" && python "C:\Game Dev Folder\NYZ\tools\map\build_terrain.py"

Inputs: every USGS 1 m tile in Downloads (newer surveys win where tiles overlap) and the border in
docs/map/border-draft.geojson. Outputs go to terrain/ (not in git, too big):
  NYZ_terrain.r16          16-bit heightmap for Unreal's landscape import
  NYZ_terrain_preview.png  a small greyscale picture of it
  NYZ_terrain.json         the Unreal import settings and the map's real-world position
"""
import json
import math
import pathlib
import re

import numpy as np
from osgeo import gdal, osr

gdal.UseExceptions()

ROOT = pathlib.Path(__file__).resolve().parents[2]
TILES = pathlib.Path.home() / "Downloads"
OUT = ROOT / "terrain"
SPACING = 2.0       # m between height points
COMPONENT = 127     # quads per Unreal landscape component (one 127 x 127 section); the size is a multiple of it
Z_SCALE = 100       # Unreal Z scale: 16 bits cover +/-256 m in 0.78 cm steps, sea level at landscape Z 0
SEA_FLOOR = -5.0    # m, where no tile has data (open water). Real depths and shorelines come later.
UTM = 26918         # NAD83 / UTM zone 18N, the tiles' grid

# Landmarks to check the result is 1:1 (approximate real ground heights). Also written to the JSON as checks
# for the Unreal import (NYZ/Tools/import_terrain.py), so they are spread over the map.
LANDMARKS = {
    "Bennett Park (Manhattan's highest ground, ~81 m)": (40.8541, -73.9378),
    "Central Park Great Lawn (~35 m)": (40.7812, -73.9665),
    "Battery Park (~2 m)": (40.7033, -74.0170),
    "Todt Hill's slope, Staten Island": (40.5975, -74.1132),
    "Flushing Meadows, Queens": (40.7400, -73.8407),
    "Pelham Bay Park, Bronx": (40.8650, -73.8070),
}


def tiles():
    """Each tile once (downloads like 'name (1).tif' are duplicates), oldest survey first so newer ones win overlaps."""
    by_name = {}
    for f in sorted(TILES.glob("USGS_*.tif")):
        if not (f.name.startswith("USGS_one_meter_") or f.name.startswith("USGS_1M_18_")):
            continue
        by_name.setdefault(re.sub(r" \(\d+\)", "", f.stem), f)

    def year(name):
        m = re.search(r"(20\d\d)", name) or re.search(r"_A(\d\d)$", name)  # e.g. NY_LongIsland_A24 is 2024
        return int(m.group(1)) if len(m.group(1)) == 4 else 2000 + int(m.group(1))
    return [str(by_name[k]) for k in sorted(by_name, key=year)]


def border_box():
    """The border's bounding box in UTM metres."""
    g = json.loads((ROOT / "docs/map/border-draft.geojson").read_text(encoding="utf-8"))
    pts = []

    def walk(c):
        if isinstance(c[0], (int, float)):
            pts.append(c)
        else:
            for d in c:
                walk(d)
    for f in g["features"]:
        walk(f["geometry"]["coordinates"])
    src, dst = osr.SpatialReference(), osr.SpatialReference()
    src.ImportFromEPSG(4326)
    dst.ImportFromEPSG(UTM)
    for s in (src, dst):
        s.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)  # x = longitude/easting
    to_utm = osr.CoordinateTransformation(src, dst)
    xy = [to_utm.TransformPoint(lon, lat)[:2] for lon, lat in pts]
    return min(x for x, _ in xy), min(y for _, y in xy), max(x for x, _ in xy), max(y for _, y in xy)


def main():
    OUT.mkdir(exist_ok=True)
    files = tiles()
    print(f"{len(files)} tiles")
    x0, y0, x1, y1 = border_box()

    # Grow the box to whole landscape components, centred on the border.
    step = SPACING * COMPONENT
    width = math.ceil((x1 - x0) / step) * step
    height = math.ceil((y1 - y0) / step) * step
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    xmin, xmax, ymin, ymax = cx - width / 2, cx + width / 2, cy - height / 2, cy + height / 2

    # Merge the tiles (later files win) and resample to the 2 m grid. Half a cell of margin puts each
    # pixel centre on a landscape vertex, so the grid has (quads + 1) points across.
    vrt = gdal.BuildVRT(str(OUT / "tiles.vrt"), files)
    vrt = None
    s = SPACING / 2
    warped = gdal.Warp(str(OUT / "merged_2m.tif"), str(OUT / "tiles.vrt"),
                       outputBounds=(xmin - s, ymin - s, xmax + s, ymax + s), xRes=SPACING, yRes=SPACING,
                       dstSRS=f"EPSG:{UTM}", resampleAlg="average", dstNodata=-999999, outputType=gdal.GDT_Float32,
                       multithread=True, warpMemoryLimit=2048, creationOptions=["TILED=YES", "COMPRESS=DEFLATE", "BIGTIFF=YES"])
    h = warped.GetRasterBand(1).ReadAsArray()
    geo = warped.GetGeoTransform()
    warped = None
    rows, cols = h.shape
    assert (cols - 1) % COMPONENT == 0 and (rows - 1) % COMPONENT == 0, (cols, rows)

    nodata = h < -1000
    print(f"{cols} x {rows} points; no data (open water) {100 * nodata.mean():.1f}%")
    h[nodata] = SEA_FLOOR
    print(f"heights {h.min():.2f} to {h.max():.2f} m")

    # Unreal: height (cm) = (value - 32768) * Z_SCALE / 128, with the landscape at Z 0.
    values = np.clip(np.rint(h * 100 * 128 / Z_SCALE) + 32768, 0, 65535).astype("<u2")
    values.tofile(OUT / "NYZ_terrain.r16")

    # Self-check: decoding the file gives back the source heights (within one 16-bit step).
    back = (values.astype(np.float32) - 32768) * Z_SCALE / 128 / 100
    assert np.abs(back - h).max() < 0.01, "16-bit conversion lost precision"

    # Landmarks: the real-world heights should come out roughly right.
    src, dst = osr.SpatialReference(), osr.SpatialReference()
    src.ImportFromEPSG(4326)
    dst.ImportFromEPSG(UTM)
    for sr in (src, dst):
        sr.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    to_utm = osr.CoordinateTransformation(src, dst)
    location = (-(cols - 1) * SPACING * 100 / 2, -(rows - 1) * SPACING * 100 / 2)  # Unreal cm of point (0, 0), the north-west corner
    checks = []
    for name, (lat, lon) in LANDMARKS.items():
        x, y = to_utm.TransformPoint(lon, lat)[:2]
        c, r = int(round((x - geo[0]) / geo[1] - 0.5)), int(round((y - geo[3]) / geo[5] - 0.5))
        print(f"  {name}: {back[r, c]:.1f} m")
        checks.append({"name": name, "x_cm": location[0] + c * SPACING * 100, "y_cm": location[1] + r * SPACING * 100,
                       "height_m": round(float(back[r, c]), 3)})

    # Small preview: every 16th point, heights stretched to black-white.
    small = h[::16, ::16]
    grey = np.clip((small - small.min()) / (small.max() - small.min()) * 255, 0, 255).astype(np.uint8)
    mem = gdal.GetDriverByName("MEM").Create("", grey.shape[1], grey.shape[0], 1, gdal.GDT_Byte)
    mem.GetRasterBand(1).WriteArray(grey)
    gdal.GetDriverByName("PNG").CreateCopy(str(OUT / "NYZ_terrain_preview.png"), mem)

    settings = {
        "file": "NYZ_terrain.r16 (raw 16-bit, little-endian)",
        "size_points": [cols, rows],
        "size_km": [round((cols - 1) * SPACING / 1000, 3), round((rows - 1) * SPACING / 1000, 3)],
        "unreal_scale": {"x": SPACING * 100, "y": SPACING * 100, "z": Z_SCALE},
        "unreal_location_cm": {"x": location[0], "y": location[1], "z": 0},
        "component": {"section_size_quads": COMPONENT, "sections_per_component": 1,
                      "components": [(cols - 1) // COMPONENT, (rows - 1) // COMPONENT]},
        "sea_level_z_cm": 0,
        "world_origin_utm18n_m": {"easting": cx, "northing": cy,
                                  "note": "Unreal (0,0) is this point; +X is east, +Y is south (image rows run north to south)."},
        "height_range_m": [round(float(h.min()), 2), round(float(h.max()), 2)],
        "no_data_filled_with_m": SEA_FLOOR,
        "checks": checks,
        "tiles": [pathlib.Path(f).name for f in files],
    }
    (OUT / "NYZ_terrain.json").write_text(json.dumps(settings, indent=2), encoding="utf-8")
    print(json.dumps({k: settings[k] for k in ("size_points", "size_km", "unreal_scale", "unreal_location_cm", "component")}, indent=2))


if __name__ == "__main__":
    main()

# Terrain: how the NYC heightmap was made (reconstructed 2026-11-09)

The developer built a 1:1 NYC terrain in September 2026 (project NYZv409, map `/Game/FirstPerson/Lvl_FirstPerson`) but didn't remember the steps. Reconstructed from QGIS's processing history (`%APPDATA%\QGIS\QGIS4\profiles\default\user-history.db`), the files left on disk, and the landscape's settings read from the project.

## The old process (September 2026)

1. **Data:** USGS 3DEP 1 m elevation tiles (The National Map), 10 × 10 km each, named by their grid square in UTM zone 18N (EPSG:26918), e.g. `x58y452` = easting 580–590 km, northing 4510–4520 km (the `y` number is the top edge). Downloaded to `Downloads`:
   - 3 Sep: a 30 km square (x57–x59, y451–y453), projects `NY_CMPG_2013`, `NJ_SdL5_2014`, plus newer `NJ_NW_New_Jersey_6_County_Lidar_2017` (x57y452–453) and `NY_FEMAR2_Central_2018` (x59y453).
   - 13 Sep: extended to a 40 km square: x60 (`NY_LongIsland_A24`, `NY_FEMAR2_Central_2018`) and row y450.
2. **QGIS 4.2.2:** Raster ▸ Miscellaneous ▸ **Build Virtual Raster** (all tiles, 1 m), then **Merge**. Kept outputs in `Documents`: `NYZLANDSCAPE_DEM.tif` (30 km square, 1 m, Float32, heights -14.3 to 132.4 m) and `NYCHM_16bit.tif` / `NYCHM16.tif` (same square at 20,413 px, still Float32 despite the name).
3. **Heightmap for Unreal:** the 40 km square resized to **8,129 × 8,129** (a standard Unreal landscape size) and saved as 16-bit with the heights stretched over the full 0–65535 range. That file isn't on disk anymore (probably a temporary QGIS output).
4. **Unreal 5.8, World Partition landscape** (imported 17 Sep):
   - X/Y scale **492.27** (40.012 km ÷ 8,128 squares = 4.92 m between height points)
   - Z scale **28.74** (16-bit range covers 512 × Z cm = 147 m, the data's height spread)
   - location Z **58.43 m** (about the middle of the height range), X/Y at -4,064 m
   - World Partition grid 508 squares (2.5 km cells): 256 streaming chunks
   - Result: **40.01 × 40.01 km at true 1:1**.

## Heights in Unreal, for any 16-bit heightmap

Unreal height (cm) = (value − 32768) × Z scale / 128 + landscape Z location. So with the heights stretched over 0–65535: Z scale = (max − min in m) × 100 / 512, and landscape Z = the middle of the range (min + max) / 2.

## Gaps against the current border (draft v2)

The border spans easting 571.6–606.5 km, northing 4488.0–4529.0 km. The 40 km square (570–610 × 4490–4530) misses:
- `x57y450` (Staten Island's north-east corner, Upper Bay): `NY_CMPG_2013` 347 MB, `NJ_SdL5_2014` 11 MB
- row y449 (south of 4490 km): `x57y449` 60 MB, `x58y449` 7 MB, `x59y449` 13 MB (`NY_CMPG_2013`); none at x60 (open ocean)

Download pattern: `https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1m/Projects/<project>/TIFF/USGS_one_meter_<tile>_<project>.tif`

## The new process (built 2026-11-09): one command

The five missing tiles were downloaded on 2026-11-09 (the developer: "go ahead and download the 5 missing tiles"). The old steps 2–3 are now `tools/map/build_terrain.py`, run with QGIS's Python:

```
"C:\Program Files\QGIS 4.2.2\bin\o4w_env.bat" && python "C:\Game Dev Folder\NYZ\tools\map\build_terrain.py"
```

It takes about a minute and:
1. collects every USGS 1 m tile in `Downloads` once (ignores "name (1).tif" duplicates), oldest survey first, so newer surveys win where tiles overlap;
2. cuts to the border's rectangle (from `docs/map/border-draft.geojson`), grown to whole 127-quad landscape components and centred on the border;
3. resamples to a **2 m grid** (average of the 1 m points);
4. fills spots with no data (open water outside the surveys) with a -5 m sea floor;
5. writes `terrain/NYZ_terrain.r16` (16-bit raw heightmap), `NYZ_terrain_preview.png` and `NYZ_terrain.json` (the import settings), and checks the 16-bit file decodes back to the source heights.

**First build (2026-11-09):** 37 tiles; **17,273 × 20,321 points = 34.5 × 40.6 km**; heights -26.9 to 133.0 m; 9.7% open water filled. Checks: Central Park's Great Lawn 33.5 m (real ~35 m), Battery Park 2.5 m (~2 m), Bennett Park 74.6 m (summit ~81 m; the 2 m average smooths the summit rock). No holes on land inside the border: the 38.7 km² with no data inside it is all open water (Long Island Sound off City Island, the Narrows).

**Height method (changed from the old one):** a fixed Z scale of 100 (16 bits cover ±256 m in 0.78 cm steps) with the landscape at Z 0, so **sea level is Z 0** and the import settings stay the same however the data changes. The old method stretched each build's own min–max over the 16 bits, which changes the Z scale and offset every rebuild.

### Importing into Unreal: the import tool (2026-11-10)

**Don't use Landscape mode ▸ New ▸ Import from File for this map.** Unreal 5.8's own import (read in the engine source) does work region by region in a World Partition map, but frees nothing until the end, so all 21,760 components sit in memory at once: the likely reason the September import kept crashing (its crash reports on disk are from other things, so this isn't proven). Use the game repo's tool instead, with the editor closed, from PowerShell:

```
& "C:\UE5.8.4 Raw\UnrealEngine-release\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" --% "C:\Game Dev Folder\NYZ\NYZ\NYZ.uproject" -ExecutePythonScript="C:\Game Dev Folder\NYZ\NYZ\Tools\import_terrain.py" -RenderOffScreen -unattended -nosplash
```

- It makes `/Game/Maps/NYC` (World Partition, with a sun and sky to see by) and brings the terrain in **one 4 km region (16 × 16 components) at a time**: create, fill, save, unload, free memory, next. A line per region shows the time, the editor's memory and "0 proxies still loaded" (anything else means regions pile up).
- **After a crash or power cut, run it again**: finished regions are listed in `NYZ/Saved/TerrainImport/progress.txt`, and a half-done region is reloaded and redone, never duplicated. To start over, delete the map.
- At the end it checks ground heights in Unreal against the heightmap at the six landmarks (`checks` in `NYZ_terrain.json`, spread from Staten Island to the Bronx): right place, right way round, right heights.
- Streaming pieces ("proxies") are 4 × 4 components, about 1 km: 1,360 of them.
- **Tested 2026-11-10** with the launcher engine on a 10 × 6 component piece around Central Park (6 regions of 4, three partial): heights exact at every check, 15 pieces as expected, every region freed, and both a crash and a resume handled. About 16 components a second there, so the whole map should take roughly 25–40 minutes.
- The settings it uses (all from `NYZ_terrain.json`): section size **127 × 127 quads**, 1 section per component, **136 × 160 components**, location **X -1,727,200, Y -2,032,000, Z 0** cm (the map's centre at Unreal's origin), scale **X 200, Y 200, Z 100**. Unreal's origin is the UTM 18N easting/northing given in the JSON; **+X is east, +Y is south**.
- Code: `NYZ/Source/NYZEditor/NYZTerrainImport.cpp` (an editor-only module; its component-adding part is a copy of the engine's private one) and `NYZ/Tools/import_terrain.py`.

### Known limits of the bare terrain
- Water is flat: the surveys flatten rivers and the harbour at the water's surface (about 0 m), and open water outside them is a flat -5 m, so there are small underwater steps where coverage ends. A water pass will carve real depths (needed for swimming and boats).
- Lighting normals along region edges are worked out without the next region, so a faint line every 4 km is possible (the tool's one known shortcut); fix only if it shows.
- The Iris grid bounds now cover it: ±18 km × ±21 km (`NYZ/Config/DefaultEngine.ini`, 2026-11-10).

## Tools on this PC

QGIS 4.2.2 at `C:\Program Files\QGIS 4.2.2`; its `bin` folder has the GDAL command-line tools (`gdalinfo`, `gdalbuildvrt`, `gdalwarp`, `gdal_translate`, `gdaltransform`), which can script steps 2–3.

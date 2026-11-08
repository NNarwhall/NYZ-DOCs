# Border change list

Changes requested for the border. **They're collected first and applied together in one pass**, as the developer asked.
The border is defined in `tools/map/build_border.py` (the `SEGMENTS` list) and described in GDD §5.

## Pending for v3

- Short placeholders still needing a real road: **across Pelham Bay Park** (Hutch to the Sound) and **Fort Wadsworth to the Verrazzano** (Staten Island).

## Applied in v2 (2026-10-27)

All five changes from review round 1. Result: **about 910 km² (351 sq mi) including water** (v1: about 1,000 km²).

1. **New Jersey cut back** to the developer's line ([drawing](../images/border-v1-nj-proposal.webp)).
   - Roads: **Pulaski Skyway → Tonnelle Avenue** (both US 1-9) from the Hackensack north to Ridgefield, then **Broad Avenue**, a short connector to **Grand Avenue** in Leonia, **Fort Lee Road** east, then **US 1-9** to the GWB plaza.
   - The dashed stretch in the drawing became the Pulaski Skyway, a main road, from the Hackensack to Tonnelle Circle.
   - Secaucus, Ridgefield Park, the Meadowlands and north Leonia are out. Fort Lee (south of I-95), Edgewater, Cliffside Park, Fairview, Guttenberg, West New York, Union City, Weehawken, Hoboken, Jersey City and Bayonne are in.
2. **GWB crossable:** the wall runs along the north side of the bridge approach and meets the Hudson north of the bridge.
3. **Breezy Point included:** the ocean line now runs south of the whole tip ([drawing](../images/border-v1-breezy-point.png)).
4. **North Bronx moved down to roughly the city line** ([drawing](../images/border-v1-north-bronx-proposal.png)): connector from the Hudson at Riverdale to **East 233rd Street**, which runs east past Woodlawn, then a connector to the **Hutchinson River Parkway** at Eastchester Bridge and south. Yonkers, Mount Vernon and Pelham are out. **Co-op City and Bay Plaza are in.**
5. **East Queens cut:**
   - Water comes down the Sound **east of the Throgs Neck Bridge** into Little Neck Bay (Fort Totten stays in).
   - Then a short stretch of the **Cross Island Parkway**, the **Clearview Expressway (I-295)** south to its end, **Francis Lewis Boulevard**, **Springfield Boulevard** south to JFK, and **Rockaway Boulevard** along JFK's east edge.
   - Through **Head of Bay** to Far Rockaway, then **Beach 9th Street** to the ocean. **The whole Rockaway peninsula is in.**
   - Throgs Neck Bridge, Bronx–Whitestone Bridge, the Cross Island Parkway between them, their approach highways and **JFK** are all inside.
   - Douglaston, Little Neck, Bellerose, Glen Oaks, eastern Queens Village, Cambria Heights, Laurelton and Rosedale are out.

**Connectors** (land without a road, accepted by the developer): Hudson to E 233rd St; end of 233rd to Eastchester Bridge; Clearview's end to Francis Lewis Blvd; Broad Ave to Grand Ave; Rockaway Blvd along JFK (that stretch was missing from the fetched data, but follows the road); Mott Basin to Beach 9th St; GWB approach to the Hudson cliff.

## Settled, no change
- **Staten Island piece stays as in v1** (north-east corner west to Clove Road, about 8.6 sq mi including edge water). (2026-10-27)

# Production notes — "The Cocaine in Coca-Cola" (9:16 Short, ~54.6 s)

## 1. VO master (`01_VO/MASTER_VO.wav`, `master_vo.py`)
- **Raw recording:** 54.4 s at −25.5 LUFS with an LRA of 6.6 LU. The noise floor sits around −87 dBFS and there's no hum.
- **Processing:** the same light chain as the Tesla Short.
- **Pauses:** trimmed to 0.34 s. A few beats were kept longer: after "cocaine in it?", around "Coca… Cola.", and after "Of course it did."
- **Result:** 52.8 s at −16.1 LUFS, LRA 3.5 LU, −1.5 dBTP. A transcript of the master confirms all 138 words survived.

## 2. Fact check
| Claim | Verdict | Handling |
|---|---|---|
| 1886, Atlanta, pharmacist John Pemberton | ✅ | Map + archival portrait |
| Pemberton struggled with morphine addiction (from Civil War wounds) and sought a cure | ✅ widely documented | 3D apothecary |
| "a medicine made from two ingredients, coca leaves and cola nuts" | ⚠️ The drink was **named** after two key ingredients; it also contained sugar, flavourings and more | On screen: "named after two key ingredients" |
| "cola nuts" | spelling | Captions read **kola** nuts |
| People said it gave energy and cured headaches | ✅ period advertising claims | Shown as "Claims of the era" banners over a real 1890s ad |
| Around 1903 the company removed the cocaine | ✅ | "c. 1903" |
| Coca leaves never fully left; decocainized coca-leaf extract processed at one New Jersey plant | ✅ widely reported (Stepan Company, Maywood NJ, DEA-licensed to import coca leaf) | Labelled "as reported" |
| Cocaine structure | ✅ PubChem CID 446220 3D conformer, C17H21NO4 (43 atoms) | Real coordinates, not an illustration |

## 3. Shot list (master-VO seconds)

| t | VO | Visual | Medium |
|---|---|---|---|
| 0.0 | What if I told you… | Cola pour on red (Mixkit 5081, 4K) | B-roll |
| 2.2 | …had cocaine in it? | Bubbles macro (5080); "COCA-COLA" → "COCAINE?" | B-roll + type |
| 5.16 | This is not a joke. | Real 1890s ad (LoC) | Archive |
| 6.98 | It's 1886, Atlanta. | Natural Earth map: Georgia → Atlanta pin | Map |
| 9.52 | A pharmacist named John Pemberton | Framed archival portrait | Archive |
| 11.22 | morphine addiction… a cure | 3D apothecary shelf; focus racks MORPHINE → COCA | 3D |
| 15.1 | So he creates a drink | Vertical bottle pour (5096, 4K vertical) | B-roll |
| 16.85 | a medicine… two ingredients | "MEDICINE" with two ingredient slots over the 1893 document | MG |
| 18.96 | coca leaves and kola nuts | Split screen: real coca + kola photos | Photo |
| 21.45 | Coca… Cola. | 1893 trademark registration, COCA + COLA | Document |
| 23.34 | energy, headaches, amazing | Victorian claim banners over the 1890s ad | MG |
| 27.66 | Of course it did. | 3D cocaine molecule assembles (PubChem) | 3D |
| 29.04 | But here's the crazy part. | Kinetic type, music drops out | Typography |
| 30.72 | Around 1903, public fear | Timeline 1886 → 1903 | MG |
| 33.82 | quietly removed the cocaine | Molecule scatters on "removed" | 3D |
| 36.14 | coca leaves never fully left | 3D coca leaves drifting | 3D |
| 39.06 | To this day… | Can pour (5077, 4K) | B-roll |
| 41.88 | coca-leaf extract, cocaine taken out | Lab (4719, 4K) + struck-out COCAINE badge | B-roll + MG |
| 45.12 | processed… New Jersey | Map flight Atlanta → Maywood NJ | Map |
| 48.36 | next time you open a Coke | Bottle cap pops on "open" (5093, 4K) | B-roll |
| 50.48 | remember where that name came from | Vertical pour (5083) + COCA (leaf) + COLA (nut) | B-roll + type |

## 4. Licensing decisions
- **Mixkit videos:** every page was checked for `videoFree`, and only Free-licensed clips were downloaded.
- **Wikimedia:** it rate-limited this environment, so Openverse and Flickr were used for the CC photos. The Pemberton portrait came from a Wikimedia thumbnail of a public-domain file.
- **Library of Congress:** both items are marked "No known restrictions on publication".
- **Tools:** no external repositories were used. The pipeline is FFmpeg, Blender/bpy, Pillow, NumPy and pyshp (MIT), plus original code in this folder.

## 5. Rebuild
Run `./build.sh` from this folder.

# Production notes — "Who Really Started Tesla?" (9:16 Short, ~49.6 s)

## 1. VO master (`01_VO/MASTER_VO.wav`, `master_vo.py`)

**Measured on the raw recording**
- Noise floor in the pauses is −70 to −87 dBFS; speech sits around −26 dBFS RMS.
- Integrated loudness is −24.9 LUFS with an LRA of 9.1 LU.
- The MP3 is band-limited at 16 kHz.
- There is no mains hum. The peaks at 50 and 60 Hz are voice harmonics, so they were left alone; a notch filter would have thinned the voice.

**Processing**
- Pauses tightened from 50.4 s to 48.0 s. Dramatic beats were kept longer: before "Wrong.", before "Money.", after "the crazy part.", and after "the real founders?".
- Then, in order: de-click, light FFT noise reduction, 70 Hz HPF, −1.5 dB at 280 Hz, de-esser, 2.5:1 compression, +1.5 dB presence at 3.2 kHz, +1 dB air shelf.
- Two-pass loudnorm to −16 LUFS / −1.5 dBTP. The resulting LRA is 4.6 LU.
- A transcript of the master confirms that all 116 words survived the pause edits.

## 2. Fact check (Rule 12)

| Claim in VO | Verdict | Handling |
|---|---|---|
| Tesla started in 2003 by Martin Eberhard and Marc Tarpenning | ✅ Founded 1 July 2003, San Carlos CA | Caption spelling corrected: VO "Mark" is shown as **Marc** |
| Named after Nikola Tesla | ✅ | Archival LoC photo |
| "Then in 2004, a young **billionaire** walks in" | ❌ Inaccurate | On-screen FACT CHECK chip: in 2004 Musk had ~$180M from PayPal and became a billionaire years later. **Recommend re-recording "billionaire" as "multimillionaire".** |
| Invests millions, becomes chairman | ✅ Feb 2004 Series A: $6.5M of $7.5M, chairman and largest shareholder | Data viz ring |
| 2007: Eberhard pushed out | ✅ Removed as CEO in 2007 | 3D network metaphor |
| He sued; the settlement lets Musk call himself a co-founder | ✅ Suit filed June 2009, settled September 2009; five people may use the title | Document recreation, labelled "illustrative recreation of publicly reported terms" |

## 3. Shot list and medium mix (master-VO seconds)

| t | VO | Visual | Medium |
|---|---|---|---|
| 0.0 | Who started Tesla? | Glass search bar, typed query | UI |
| 1.85 | Elon Musk, right? | Answer card with Musk 2006 photo | Photo |
| 3.86 | Wrong. | Card shatters (Voronoi), WRONG slam | VFX |
| 4.5 | It's 2003. | Gold 3D digits rise | 3D |
| 6.18 | Two engineers… | Engineer at night (Mixkit 39839, 4K) | B-roll |
| 7.4 | Martin Eberhard and Marc Tarpenning… crazy idea | Dossier cards, then a blueprint of the real Roadster drawing itself | MG |
| 11.0 | An electric car… | Headlight flare (Mixkit 49, 4K) | B-roll |
| 11.95 | …actually cool | 2008 Tesla Roadster (real photo) | Photo |
| 13.3 | named the company after… | Storm + lightning (Mixkit 4422, 4K) + procedural bolt | B-roll/VFX |
| 15.0 | Nikola Tesla | LoC photo c. 1890, arcs | Archive |
| 17.0 | one problem. Money. | Empty wallet (Mixkit 18299, 4K), MONEY slam | B-roll |
| 19.18 | Then in 2004 | 3D corridor, door opens into light | 3D |
| 21.3 | a young billionaire walks in | Silhouette in spotlight (Mixkit 1038) + fact-check | B-roll |
| 22.81 | Elon Musk. | Photo reveal + name | Photo |
| 23.75 | invests millions, chairman, control | Series A ring $6.5M / $7.5M, chips | Data viz |
| 27.34 | But here's the crazy part. | Black, kinetic type, riser, music drop-out | Typography |
| 29.04 | In 2007, Eberhard… pushed out | 3D company network; Eberhard's links snap and he falls | 3D |
| 34.75 | He sued | Signing (Mixkit 307, 4K) | B-roll |
| 35.91 | settlement… co-founder | Settlement document recreation, highlight + stamp | Document |
| 39.8 | almost everyone believes… | Shibuya crowd (Mixkit 4401) + "MUSK" tracking tags | B-roll + MG |
| 43.86 | but the real founders? | Founder cards | Photo/MG |
| 45.87 | never heard their names | 3D steel names, light sweeps then dies | 3D |

The rough split is: B-roll ~30%, 3D ~25%, MG/data ~17%, photos/docs ~16%, UI/typography ~9%.

## 4. Licensing decisions
- Every Mixkit video page was checked for `videoFree` versus `videoRestricted`. **Six clips were rejected as Restricted** (non-commercial only): 23126, 35576, 47947, 28362, 22957 and 15478. They were replaced with Free-licensed alternatives.
- Wikimedia's API rate-limited this environment, so photos were sourced through Openverse, which carries license metadata. The CC BY / BY-SA photos are credited on screen and in `ATTRIBUTION.md`.
- A photo captioned with Tarpenning shows two unnamed people. It was **not used**, to avoid mislabelling a real person.
- No external code repositories ended up in the final pipeline. Every tool used is either system software (FFmpeg, Blender/bpy under GPL, Pillow, NumPy) or original code in this folder.

## 5. Rebuild
Run `./build.sh` from this folder. It masters the VO, renders the 3D, composes the picture, mixes the audio and muxes the result to `12_RENDERS/FINAL_VIDEO.mp4`.

# Katha Deep — Production Studio (restored 7 Nov 2026)

Everything needed to produce a Katha Deep reel lives in this folder. Rebuild any episode with
`cd <episode> && python3 edit.py all` then `python3 ../tools/finalize.py <episode>` (mux + QC + cover).

## 1. Continuity bible — the four supplied videos

| | A · Master reference (Video-10243) | B · Deepotsav Din 1 | C · Dhanteras Special 2 | D · Dhanteras Special 3 |
|---|---|---|---|---|
| Length / format | 128.5 s, **720×1280**, 30 fps | 88.8 s, 1080×1920, 30 fps | 77.6 s, 1080×1920, 30 fps | 103.1 s, 1080×1920, 30 fps |
| Loudness | −14.1 LUFS, peak −0.1 dBFS | −14.3 LUFS, TP −2.7 | −14.5 LUFS, TP −2.0 | −14.3 LUFS, TP −1.5 |
| Narration | English on-screen text series "DIWALI · DAY 1/5" | Hindi VO (Rudra voice) | Hindi VO (same) | Hindi VO (same) |
| Story | Diwali = 5 days; Dhanteras: Yama, prophecy of snakebite on night 4 of marriage, wife's lamps + gold blind the serpent; Dhanvantari; "first wealth = health" | Diwali = Lakshmi Puja → where did Lakshmi come from? Samudra Manthan, Kurma, Halahal/Neelkanth, ratnas, Lakshmi, Dhanvantari + Amrit kalash → Dhan-teras | Golden Lanka was Kubera's; tapasya, Brahma's 3 boons, Pushpak; step-brother Ravana takes Lanka + Pushpak; Kubera to Alaka near Kailash; Ram returns in Pushpak → Diwali; Pushpak returned to Kubera | Kathopanishad: Vajashravas' gift of old cows, "to whom will you give me?", "to Death", 3 nights at Yama's door, 3 boons, Yama tempts with sons, gold, elephants; "na vittena tarpaniyo manushyah" (1.1.27) |
| Visual language | Original **flat storybook illustration** (custom characters, havelis, diyas), English kinetic type, calendar/compass props | **Museum paintings (The Met, CC0)** with Ken Burns + warm grade; red mandala plates; 3D gold kalash on purple plate; 5-diya campaign tracker | Met paintings + sculptures; 3D Pushpak on sky plate; 3D gold coin heap; family tree chips | Met paintings (Calcutta Art Studio Yama print 849512); Nachiketa as vector **boy silhouette with topknot**; 3D diya; 3D Yamlok door; Devanagari shloka cards; "VAR 1/2/3" chips |
| Typography | Condensed caps, white + red/gold second line, top-left | **Anton**-style caps, line 1 cream, line 2 gold/red, top-left; Space Mono tag "DEEPOTSAV · DIN 1/5" top-right; mono credit "ART: THE MET · OPEN ACCESS (CC0)" | same type, no tag | same type + Devanagari serif cards |
| Hook (first 3 s) | "DIWALI = 1 DAY?" | "Diwali par… Lakshmi ji aayi kahan se?" | "Sone ki Lanka Ravan ki nahi thi" | "Yamraj ne ek bachche ko duniya ka saara dhan diya… aur usne thukra diya" |
| **Ending (exact)** | "YAMA AGAIN? FOLLOW for Day 2" | **"Kal doosra diya, Chhoti Diwali aur Narakasur ki kahani. Follow kar lijiye, paanchon diye saath jalayenge."** | **"Par Ravan aur Kuber ki kahani mein ek mod abhi baaki hai. Part 2 kal. Aur aaj raat: Yamraj vs 1 bachcha."** | **"Par Yamraj ne Nachiketa ko jawab kya diya — maut ke baad kya hota hai? Part 2 kal."** |

**Key finding:** B, C and D do *not* use the master reference's illustration style. They are a museum-art + 3D + kinetic-type
format. The continuation episodes follow **B–D** (that is the series viewers saw yesterday) and borrow from A only what fits:
layered depth (2.5D moves over art, 3D props), particles, and a campaign tracker. Reproducing A's custom illustration
would need an image-generation API with credits (see audit) — none is available today.

**Character continuity rules** (and your rule: *no figure repeats*): every scene uses a different image; characters stay
recognisable by iconography — Yamraj: dark skin, crown, red robe, mace/noose (Calcutta Art Studio prints / Yama with buffalo);
Nachiketa: the same vector silhouette with topknot used in Part 1; Kubera: seated bronzes; Ravana: shown only through painted
court/army scenes or typography. No image used in B, C or D is reused in the Part 2s, and no image is shared across the three Part 2s.

## 2. Tool / API audit

| Tool / API | Purpose | Status | Credential | Action needed | Alternative |
|---|---|---|---|---|---|
| ElevenLabs | Hindi narration | ✅ connected (Starter, ~6 k chars left this cycle) | ✅ saved as an environment network secret (proxy-injected; never in files) | **Delete the old key you pasted in chat** in ElevenLabs → API Keys | — |
| ElevenLabs voice | Series narrator | ✅ identified: **Rudra – Intense Documentary Narrator** (`vIdhHAZdn1bGjKe1dFw8`) on **eleven_v3** — 0.94 speaker match to B/C/D | — | none (no clone needed) | IVC clone from episode stems (prepared, not used) |
| vidIQ (MCP) | IG publishing, analytics, AI video/music/TTS | ✅ connected; **@kathadeeps** linked with publish + insights | ✅ OAuth | Only **4 credits** — AI video/music/voice unusable until 19 Nov refill or top-up | Blender + procedural score |
| Google Drive (MCP) | Source footage in/out | ✅ connected | ✅ OAuth | — | — |
| Image generation (custom illustration like A) | Original characters/environments | ❌ none connected (no OpenAI/Replicate/fal/Stability key; vidIQ out of credits) | ❌ | Add a key (e.g. Replicate or OpenAI) via environment secret if you want A-style illustration | The Met Open Access CC0 art (used) |
| Image-to-video AI | Animating stills | ❌ (vidIQ video gen needs ~160+ credits/shot) | — | Top up vidIQ credits | 2.5D Ken Burns + particles + 3D (used) |
| Blender 4.2.3 LTS | 3D props/environments | ✅ installed this session (`/opt/blender`) | n/a | Not persistent: add to a setup script (offered) | — |
| FFmpeg 6 / Pillow + raqm / NumPy | Compositing, Devanagari shaping, encode | ✅ | n/a | — | — |
| faster-whisper (medium) | VO read-back QC, transcription of references | ✅ installed this session | n/a | add to setup script | — |
| Demucs + Resemblyzer | Voice isolation / speaker matching | ✅ installed this session | n/a | add to setup script | — |
| The Met Collection API (v1.1) | CC0 art search + download | ✅ (`/v1/search` was retired 1 Oct 2026; using `/v1.1/search`) | none needed | — | Openverse |
| Mixkit SFX | Sound effects (free licence) | ✅ | none | — | — |
| Music | BGM | ✅ original procedural score (`tools/music.py`: tanpura, pads, tabla theka, bells, bansuri) | none | — | vidIQ music gen after credit refill |
| Wikimedia / Flickr | Photos | ⚠️ blocked from this environment | — | — | Openverse / typographic cards |
| Previous Katha Deep project files | Old scripts/assets | ❌ not in this environment or either GitHub repo; repo `a` holds the earlier Tesla/Coca-Cola/Nokia pipeline, whose compositor/mix approach this studio reuses | — | If you have the old files on Drive, share the folder | Rebuilt here |

## 3. Pipeline (per episode)
1. `vo/script.txt` → `tools/tts.py` (ElevenLabs with character timestamps) → `tools/vo_qc.py` (Whisper read-back + speaker match ≥ 0.9).
2. `edit.py` scenes keyed to spoken words (`Timing.at("…")`): Met art Ken Burns, 3D stills from `tools/scenes3d.py`, plates, chips, Devanagari shloka cards, captions.
3. `edit.py audio`: VO master (HPF, de-mud, 2.5:1 comp, presence, −16 LUFS) + procedural score ducked under voice + Mixkit SFX → −14 LUFS / −1.5 dBTP.
4. `tools/finalize.py`: mux → `tools/qc.py` gate (size/fps, black, frozen, loudness, true peak, clipping, A/V length) → cover.

## 4. Sources used
- Kathopanishad 1.2.1–2, 1.2.18, 1.2.20, 1.3.3–4, 1.3.9, 1.3.14, 2.3.18.
- Valmiki Ramayana Uttarakanda 13–15 (envoy, Alaka, Pushpaka), 26 (Rambha, Nalakubara's curse, seven pieces); Yuddhakanda 13 (Brahma's curse, Punjikasthala) — shown as a separate version.
- Bhagavata Purana 10.59 (Bhauma/Naraka, Mura, Aditi's earrings, Varuna's umbrella, 16,000 princesses sent to Dvaraka); Satyabhama-as-slayer labelled folk tradition. 10.10 (Nalakubara freed — tease only).

## 5. QC catches this round (fixed before render)
- ElevenLabs slurred "मर्यादा **नहीं**" (heard as "dint" by two ASR models) → that line regenerated and spliced in place.
- Met 38036 was assumed to show Ravana; its inscriptions read **सीता / वाल्मीकि / लक्ष्मण** (Sita at Valmiki's ashram) → Ravana beat moved to a typographic plate.
- A Sheshashayi print crop showed Lakshmi, not Bhumi Devi → replaced with the Vishnu–Sri–Bhu print.
- One Bhagavata folio was cropped 3× → cut to 2 distinct figure groups; one image swapped.

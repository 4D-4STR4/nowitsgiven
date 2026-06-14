# Art, Audio & Production Plan — SALVAGE

_Source: production research agent. Team assumption: 2–3 core (1 generalist dev/designer,
1 part-time/AI-assisted artist, 1 part-time/contract sound designer) + targeted contractors._

> **Strategic thesis:** Lethal Company sold ~640k+ copies (~$5.7M gross) as a *solo* project
> with a deliberately ugly PS1 look. The lesson isn't "be ugly" — it's that
> **constraint-as-style + audio + emergent social comedy/horror beats fidelity.** Every
> decision below serves: *cheap to produce, intentional-looking, streamable.*

---

## 1. Art Direction — "Salvage-Industrial Low-Poly"

Flat/vertex-lit low-poly geometry, hard darkness, dynamic point lights, palette-locked per
wreck, heavy fog + grain post. PS1-adjacent but pushed toward *Iron Lung's* claustrophobic
monochrome-with-one-accent and *Inside's* silhouette-and-light discipline — **not** Lethal
Company's cartoon goofiness. Horror comes from **what light reveals**, not polygon count.

**Style bible (the law):**
- **Geometry:** low-poly, hard-edged, flat-shaded (no smoothing groups on industrial surfaces).
  200–1500 tris/prop. Flat shading reads as intentional retro, hides topology sins, renders cheap.
- **Textures:** 128² / 256² max, point-filtered (no bilinear). Trim-sheets + atlases — one 1024
  atlas can skin an entire room kit.
- **Lighting is the art.** The wreck is *powered down*; bake almost nothing. 1–3 real-time lights
  per visible cluster. Diegetic sources only: flashlight, flares, sputtering emergency strips,
  monster glow, console screens. **Darkness is free content — 60% of every level is black, so 60%
  needs no detail.**
- **Palette lock per wreck type:** each "biome" gets a 4–6 color palette (Reactor = sodium-orange
  + black; Cryo = cyan-white + deep blue; Med-bay = sickly green + rust). Makes mismatched/bought
  assets cohere instantly; becomes a streamer-recognizable signature.
- **Emergency lighting as mechanic + aesthetic:** red rotating beacons, power-state-triggered
  flickers, alarm strobes. Highest-value cheap effect; ties power-routing mechanic to mood.
- **Post stack (the "free coat of paint"):** film grain, *optional* (toggleable) CRT/scanlines,
  chromatic aberration on damage, vignette, volumetric/height fog, per-biome color LUT, dithering.
  Build once, pays forever — unifies mismatched sources.
- **Fog as a budget tool, literally:** aggressive fog = short draw distance = build only what's in
  the flashlight cone = fewer assets, higher FPS, more dread. The single most important line item.

**Why cheap:** flat shading hides bad normals; tiny textures are AI-generatable; darkness +
fog mean authoring a fraction of each room; post stack unifies sources.
**Anti-goal:** do NOT chase Lethal Company's exact look — be *darker, more monochrome, more
architectural* (Iron Lung / Inside / Signalis, not Garry's-Mod goofy).

---

## 2. Audio Direction — the cheapest, highest-ROI fear lever

Audio is the genre's emotional engine and its marketing department. Budget it like a feature.
- **Middleware: FMOD** (fast Unity/Godot integration) or **Wwise** (free Indie tier <$250k budget;
  unmatched room/portal occlusion). Both free at our scale.
- **Proximity voice IS gameplay AND marketing** — non-negotiable, the reason this genre streams.
  Distance-attenuated, occluded positional voice → emergent comedy ("where ARE you") and horror
  ("...why did you stop talking"). Walkie-talkie items add a mechanic and an isolation fear vector.
  Prove it in the prototype; it's on the critical path.
- **Spatial sound design:** everything diegetic/positional; occlusion so players triangulate threats
  by ear. Turns darkness into navigable space; makes the flashlight a fear tradeoff (light = seen).
- **Monster audio = the monster.** Design enemies audio-first: a creature you *hear* breathing two
  rooms away that goes *silent* when close is scarier and cheaper than one animated beautifully.
  Distinct audio signatures (clicking, wet drag, mimicked voice) let players ID threats blind.
- **Ambient dread bed:** continuous sub-bass hull tone + sparse randomized one-shots, driven by a
  real-time "tension" parameter rising with time-on-wreck / power drain.
- **Music: minimal, reactive, mostly absent.** Silence is the score. Low drone for exploration;
  stingers/risers on detection; panic cue on aggro. ~5–8 cues. One contractor composer for a
  6-cue adaptive pack is high-ROI.

---

## 3. Asset Pipeline & Sourcing

**Core principle: modular kit + procedural assembly.** You don't build levels; you build *parts*
and let code assemble derelicts.
- **Modular wreck kit (the spine):** one grid-snapping set (4m grid) — corridors, junctions,
  doorways, room shells, stairs/ladders, hull-breach pieces, debris. **~20–30 pieces → effectively
  unlimited layouts.** Make in-house (controls style + grid). The single most important investment.
- **Prop library:** ~40–60 unique props at 1.0, palette-tinted so one mesh recolors per biome.
- **Make vs buy:** *make* the kit, hero loot, enemies (the identity). *Buy/CC0* filler props,
  greebles, UI icons — Kenney.nl, Quaternius, Poly Pizza, Sketchfab CC, Unity Asset Store. **Run
  every bought asset through the post/palette pipeline** so it inherits house style.
- **AI acceleration (with care):** textures (256px tiling industrial → point-filter), concept/mood
  boards + palettes + enemy silhouettes (concept only; humans model finals), audio *raw material*
  (drones, creature vocals → processed in FMOD), tooling/boilerplate. **Cautions:** keep provenance
  clean (CC0/licensed/own-generated) for Steam's AI-disclosure requirement; don't AI-generate hero
  enemies (need authored anim + audio sync); disclose generated textures honestly.

---

## 4. Minimal Lovable Product (MLP) — must feel complete, not small

| Category | MLP count | Notes |
|---|---|---|
| Modular kit pieces | ~20 | One biome's worth; varied procedural layouts |
| Biomes / wreck types | 2 | e.g. Freighter + Reactor — distinct palettes, same kit recolored |
| Unique props | ~25 | Recolored/scaled for variety |
| Loot/salvage items | ~10 | Distinct values/handling (heavy=slow, fragile, hazardous) |
| Enemies | 3 | Audio-driven stalker, ambusher, environmental hazard |
| Hazards | ~4 | Hull breach/vacuum, radiation, electrical, structural collapse |
| Tools | ~5 | Flashlight, scanner, walkie-talkie, flares, extraction beacon |
| Distinct sounds | ~60–80 | Most-loaded bucket — over-index on audio intentionally |
| Music cues | ~6 | Adaptive: explore, tension, detection, panic, extraction, death |

**Phased roadmap:** Phase 0 vertical slice (1 biome/1 enemy, the "is it fun & scary" gate) →
Phase 1 Next Fest demo (15–25 min best experience, ends on wishlist prompt) → Phase 2 EA launch
(full MLP, fun for 8–15h, stable co-op) → Phase 3 EA drops every 6–10 weeks → Phase 4 1.0
(4–5 biomes, 6–8 enemies, full progression, controller, localization, polish).

---

## 5. Timeline & Milestones (~14–20 months to 1.0; revenue at EA ~month 9–11)

| Phase | Duration | Gate |
|---|---|---|
| Pre-production + prototype | 1.5–2 mo | Core loop + proximity voice + procedural assembler + post stack in gray-box. **Fun gate.** |
| Vertical slice | 2–3 mo | 1 biome fully styled, 1–2 enemies; capture trailer footage |
| Steam page live + wishlist build | parallel | **68–88% of wishlists come from the store page, not the demo** — capsule + 60s trailer are critical path |
| Demo build + polish | 1.5–2 mo | 15–25 min, ends on wishlist prompt, ~20% conversion target |
| Steam Next Fest | event | Enter with >1,000 WL (below that, median gain ~462) |
| EA content build | 3–4 mo | Fill to EA scope, harden co-op netcode |
| **Early Access launch** | ~mo 9–11 | Revenue begins; streamer push |
| EA live-ops | 4–6 mo | Drops every 6–10 weeks |
| **1.0** | ~mo 14–20 | Full content, polish, localization, marketing beat #2 |

**Critical path:** (1) procedural assembler + modular grid; (2) proximity voice netcode;
(3) co-op stability; (4) Steam page + capsule + trailer; (5) the style filter (post + palette).

---

## 6. Budget (USD, lean launch)

| Item | Shoestring | Comfortable |
|---|---|---|
| Steam Direct fee | $100 | $100 |
| Engine / audio middleware | $0 | $0 |
| Asset store / kits | $50 | $300 |
| AI tooling subs | $50–150 | $200–400 |
| **Capsule + store art** | $150 | $600 | *(don't cheap out — drives 68–88% of wishlists)* |
| Audio contractor | $0 (DIY) | $1,500–4,000 |
| Trailer (60s) | $0 (DIY) | $400–1,000 |
| Localization (1.0) | $0 | $500–1,500 |
| Marketing / creator outreach | $100 | $1,000–3,000 |
| Contingency / hosting | $100 | $500 |
| **Total to lean launch** | **~$700–900** | **~$6,000–12,000** |

**Spend priority if any money exists:** (1) capsule/store art, (2) audio contractor, (3) trailer,
(4) creator outreach — the four *conversion* line items.

---

## 7. Scope Discipline — the traps (and rules)

1. **"More biomes" disease** → ship EA with **2 biomes**; new biomes are post-launch live-ops.
2. **Enemy-roster bloat** → **3 enemies at EA**, audio-first, mechanically distinct.
3. **Fidelity creep** → the style bible is law; if it fails the flat-shade/palette/fog filter, it
   doesn't ship. Ugliness-with-intent is the brand.
4. **Bespoke hand-authored levels** → everything assembles from the kit; at most a few injected
   set-piece anchor rooms.
5. **Netcode underestimation** → prove voice + 4-player sync in the prototype, before content.
6. **Narrative scope** → environmental/audio-log storytelling only; "why" is a thin frame.
7. **Feature-chasing the comps** → one signature mechanic executed deeply > five borrowed ones.
8. **Polishing the demo instead of shipping it** → demo = best 20 min, ends on wishlist prompt, stop.

**Governing discipline:** *narrow and deep, dark and loud.*

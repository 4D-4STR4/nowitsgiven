# Playable Prototype — Core Loop Gray-Box

_Location: `game/prototype/` · Run by opening `index.html` in any modern browser (no build, no deps)._

## What it is
An engine-independent, single-player **gray-box** that validates the one question that must be
answered before committing engine time: **is the core loop fun?** It implements the full
greed-vs-extraction loop the Unity build will reproduce. It is intentionally *not* the production
codebase — it's a runnable design spec + the "fun gate" the production plan (`04`) demands.

## Controls
- **WASD / Arrows** — move (heavier hold = slower; load caps at 40 kg → forces trip-planning)
- **E** — grab nearby salvage / **extract** at the cyan AIRLOCK (banks your hold toward quota)
- **F** — toggle flashlight (light lets you see — *and be seen* by stalkers)
- **V** — vent a hull breach (the signature toy: explosive decompression kills nearby threats and
  shoves you, but spikes Instability +18 and costs O2)
- **R** — generate a new wreck (seeded)

## The loop it proves
1. **Procedural wreck** — seeded modular rooms + L-corridors; airlock at the entrance, reactor in the
   deepest room (mirrors the net-deterministic generation in `03`).
2. **Risk = reward** — salvage value/weight scales with depth; the reactor room always holds a `core`.
3. **Greed wakes the wreck** — Wreck Instability climbs with time, **proximity to the reactor**, and
   **carried value**. At 100% → **reactor meltdown** on a 24s countdown.
4. **Extraction tension** — only salvage you carry back and **extract** at the airlock counts. Death
   (meltdown / O2-out) or a stalker hit drops your hold in the dark.
5. **Resource pressure** — flashlight (visibility vs. being hunted), oxygen drain, weight-vs-speed.
6. **The signature hook** — venting a breach to clear a pursuer at a cost demonstrates the
   "break the machine against itself" identity in miniature.
7. **Win condition** — bank the quota before the wreck (or your greed) kills you.

## How it maps to the Unity build
| Prototype concept | Unity system (`03`) |
|---|---|
| Seeded room/corridor gen | `WreckGen/` modular kit + room-graph, seed-synced across clients |
| Salvage value/weight/depth | `Inventory/` ItemDef ScriptableObjects + WeightSystem |
| Wreck Instability + meltdown | `Systems/ReactorSystem` (server-authoritative) |
| Flashlight/darkness, O2 | `Systems/Lighting`, `Player/SuitState` |
| Vent / hull breach | `Systems/AtmosphereSystem` (the signature mechanic) |
| Stalker (light/noise drawn) | `Enemies/` sensor-driven behaviors |
| Extract-or-lose-it | `Extraction/` + economy/quota validation |

## Validation performed
- `node --check game.js` → syntax valid.
- Headless smoke test (stubbed DOM, 300+ simulated frames exercising generation, movement,
  instability, meltdown, enemies, oxygen, vent, and extract) → no runtime exceptions.

## What it deliberately omits (it's a loop gray-box, not the game)
Networking/co-op, real 3D/first-person, art/audio, the full tool/role kit, meta-progression
persistence, and the home-tug economy — all specified in the design docs and scheduled for the
Unity vertical slice.

## Co-op note
Every rule is authored to scale to the 1–4 player listen-server design in `03`: instability/threat
density and wreck size scale with crew size, the hold/extraction economy is per-crew, and proximity
voice + the vent toy are the emergent-moment generators that make it *better* with friends.

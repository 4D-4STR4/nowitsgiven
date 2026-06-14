# Technical Architecture & Engine Plan — SALVAGE

_Status: orchestrator-authored (tech research agent stalled on rate-limit). Decisive by design._

---

## 1. Engine recommendation — **Unity** (primary), Godot 4 (credible free alt)

**Recommendation: Unity.** Reasoning is grounded in the competitive data: **every breakout in our
exact lane — Lethal Company, R.E.P.O., Content Warning, Phasmophobia — is built in Unity.** That is
not a coincidence; it's the proven path with the deepest de-risking for THIS genre:

| Factor | Unity | Godot 4 |
|---|---|---|
| Proven for this exact genre | ✅ all comps are Unity | ⚠️ fewer co-op-horror precedents |
| 3D capability | ✅ mature | ✅ good, improving |
| Netcode ecosystem | ✅ Netcode for GameObjects, **FishNet**, Mirror, Photon | ⚠️ high-level multiplayer (lighter, less battle-tested for this) |
| Steamworks integration | ✅ **Facepunch.Steamworks**, Steamworks.NET (mature) | ⚠️ GodotSteam (works, smaller community) |
| Proximity voice | ✅ **Dissonance**, Steam Voice, Photon Voice | ⚠️ roll-your-own / Steam Voice |
| Asset store / cheap content | ✅ vast (critical for tiny team) | ⚠️ smaller |
| Modding ecosystem | ✅ **BepInEx** (the Lethal Company longtail driver) | ⚠️ ad hoc |
| AI-assisted dev (C#) | ✅ excellent | ✅ GDScript good, C# ok |
| Cost / runtime fee | ✅ runtime fee **reversed (2024)**; Personal free under $200k | ✅ MIT, truly free |

**The deciding factor:** Unity's netcode + Steamworks + asset + modding ecosystem for co-op extraction
horror is a paved road our comps already walked. Godot's only real edge (no fee) was neutralized when
Unity killed the runtime fee. **Pick Unity.** (If the team has zero Unity experience and strong
Godot/GDScript preference, Godot 4 is acceptable — the architecture below is engine-agnostic.)

---

## 2. Multiplayer architecture — single code path for SP & MP

**The cardinal rule (the #1 lesson from the market research):** single-player is **"host a session
with one player."** SP and MP share ONE code path. There is no separate "singleplayer mode" — solo is
just a local-host listen-server with no remote clients. This is the only way to avoid a painful co-op
retrofit AND to guarantee solo viability (the lineage's biggest gap, and our moat against the
empty-lobby death spiral).

- **Topology: listen-server (host-authoritative P2P), NOT dedicated servers.** The host player's
  client is authoritative; others connect P2P. This beats the cold-start problem (no servers to keep
  alive, no live-service cost) and matches the friend-group "atomic network" that lets co-op survive.
- **Transport: Steam Datagram Relay via Facepunch.Steamworks** (Steam Networking Sockets). Free relay,
  NAT punch-through, no IP exposure, Steam lobby invites. Fall back to direct IP for testing.
- **Authority model:**
  - **Server-authoritative:** wreck seed/generation, instability/meltdown state, enemy AI, salvage
    spawn & ownership, power/atmosphere simulation, extraction validation, economy.
  - **Client-predicted:** local player movement + camera (reconciled), held-item pose. Keep it simple —
    this is co-op PvE, not competitive; minor desync is tolerable, so prefer **simplicity over
    rollback**. (R.E.P.O.'s complaints were networking jank — budget netcode polish early.)
- **Networking lib:** **FishNet** (free, performant, great docs, prediction built-in) or Unity
  **Netcode for GameObjects**. Recommendation: **FishNet**.
- **Proximity voice:** **Dissonance Voice Chat** (Unity Asset Store, integrates with FishNet/Steam) —
  positional, occludable, the genre's marketing engine. Prototype it EARLY; it's on the critical path.
- **Drop-in/out:** lobby at the tug between runs (mandatory); mid-run join as a stretch (host streams
  current wreck state to joiner).

---

## 3. Project structure (Unity)

```
SalvageGame/
  Assets/
    _Project/
      Scripts/
        Core/            # GameManager, RunManager, SessionBootstrap, seeded RNG
        Networking/      # NetworkManager wrapper, Steam transport, ownership helpers
        Player/          # PlayerController, FirstPersonCamera, SuitState (O2/health)
        Inventory/       # Item, PhysicsItem, Inventory, WeightSystem, Appraisal
        WreckGen/        # ModuleKit, RoomGraph, WreckGenerator (seed-deterministic)
        Systems/         # PowerSystem, AtmosphereSystem, ReactorSystem (instability), Lighting
        Enemies/         # EnemyBase, sensors (sound/light/heat), behaviors
        Extraction/      # ExtractionZone, Quota/Debt economy, runResult
        Save/            # MetaProgression (unlocks), PlayerProfile, cloud-save hooks
        UI/              # HUD, ScanReadout, TugHub/Shop, Lobby
      Art/  Audio/  Prefabs/  Scenes/  ScriptableObjects/   # WreckClass, ItemDef, EnemyDef, Modifier
    ThirdParty/          # FishNet, Facepunch.Steamworks, Dissonance, FMOD
  Packages/  ProjectSettings/
  game/docs/             # (this design doc set, repo root)
```

**Data-driven via ScriptableObjects:** `WreckClassDef`, `ItemDef`, `EnemyDef`, `ShiftModifierDef`,
`UpgradeNodeDef` — so designers/AI can add content without code, and so the procedural generator and
economy stay tunable.

---

## 4. Procedural wreck generation (net-deterministic)

- **Modular kit** (~20–30 grid-snapped pieces on a 4m grid): corridors, junctions, doorways, room
  shells, stairs/ladders, hull-breach pieces, debris.
- **Room-graph assembly:** airlock → arteries → objective spaces → reactor/vault. Generate a graph,
  place modules along it, validate connectivity, decorate with seeded prop/loot/hazard tables per
  `WreckClassDef`.
- **Determinism:** the host picks a seed; **all clients generate identical geometry from the seed**
  (only dynamic entity/physics/loot-ownership state is replicated, not the static mesh layout). This
  keeps bandwidth tiny and is the standard approach for procedural co-op.
- Optional hand-authored "anchor" set-piece rooms the generator can inject for memorability.

---

## 5. Steam integration (Steamworks SDK via Facepunch.Steamworks)

Needed for EA launch: **lobbies + invites/matchmaking** (Steam lobbies), **P2P transport** (Datagram
Relay), **cloud saves** (meta-progression), **achievements**, **rich presence**. Steam Deck verified is
a stretch but valuable (controller support + perf). Steam Direct fee $100.

---

## 6. Tooling / CI

- **Git + Git LFS** for binary assets (textures/audio/models). `.gitignore` Unity's `Library/`,
  `Temp/`, `Logs/`, `Build/`.
- **CI:** GameCI (GitHub Actions) for automated Windows builds + EditMode/PlayMode tests.
- **Testing:** unit tests on deterministic systems (wreck gen seeds, economy, weight/instability math —
  exactly what the prototype validates); playtest builds via Steam playtest branch.
- **Repo layout for AI-assisted iteration:** small, single-responsibility scripts; data in
  ScriptableObjects; clear module boundaries (above) so an agent can edit one system safely.

---

## 7. MVP technical milestones (ordered)

1. **Empty project + listen-server bootstrap** — host-with-one-player runs; FishNet + Steam transport
   connect two clients in a lobby.
2. **Player controller + camera + suit state** (O2/health), networked.
3. **Wreck generator (gray-box)** — seed-deterministic modular assembly; identical on all clients.
4. **Salvage items + inventory + weight** → movement penalty; appraisal/scan.
5. **Instability/reactor system + extraction** — the core loop closes (board → loot → escape → bank).
6. **Lighting/darkness + flashlight; one enemy** with sound/light sensing.
7. **Proximity voice** (Dissonance) integrated.
8. **Tug hub + economy/debt + meta-progression save.**
9. **Atmosphere/breach/vent system** — the signature hook.
10. **Vertical slice polish** → the "is it fun?" gate → trailer capture.

**Build order priority (from the production critical path):** procedural assembler → proximity voice
netcode → co-op stability → the loop closing → the signature vent/breach toy.

---

## 8. Starter scaffold & the playable prototype

Because the engine project can't be *run/verified* in this cloud environment, we de-risk the most
important question first — **"is the core loop fun?"** — with an engine-independent **playable
browser prototype** (`game/prototype/index.html`). It implements the loop end-to-end: procedural
wreck, salvage value/weight, weight-vs-speed, flashlight/darkness, rising **Wreck Instability** →
meltdown countdown, extraction-or-lose-it, and the **vent** signature mechanic. This is the gray-box
"fun gate" the production plan calls for *before* committing Unity time, and it doubles as a precise,
runnable spec of the mechanics the Unity systems above must reproduce.

See `game/prototype/` (run by opening `index.html` in any browser) and `08-PROTOTYPE.md`.

# Game Design Document — **SALVAGE** (working title)

_Status: v0.1 — orchestrator-authored, to be reconciled with research deliverables._
_Genre: Co-op derelict-salvage extraction roguelite. 1–4 players. SP-first, co-op-core._

---

## 1. High Concept

> **You are a salvage crew working off your debt to the company.** Each shift, you
> jump your tug to a dead, drifting spacecraft, cut your way inside, and strip it
> for everything valuable before its failing reactor, its hull, or whatever's
> still moving in the dark gets you first. Haul it back to the airlock, extract,
> and turn salvage into better tools, a better ship, and a deeper run into the
> graveyard of the void.

**One-line pitch:** *Lethal Company's dread and chaos, in the systemic, breaking-down
spaceships of Barotrauma, with the run-by-run progression of Deep Rock Galactic.*

**The core fantasy:** competent, terrified people doing a dangerous blue-collar job
in a hostile machine — and the machine is actively dying around you.

### Design pillars
1. **Risk you can feel.** Loot value scales with depth and danger. The decision to
   push one room further — or run for the airlock now — is the whole game, made
   every 30 seconds.
2. **The wreck is the enemy.** Before any monster: darkness, vacuum, failing power,
   reactor heat, weight, and structural collapse. Environmental dread over jump scares.
3. **Better together, not punished alone.** Roles and logistics make a 4-stack sing,
   but every system is solvable solo. We never gate the solo player.
4. **Emergent stories, not scripted ones.** Systemic simulation + physics + proximity
   voice = moments players *have* to clip.

---

## 2. Why this wins (grounded in research)

- **Co-op PvE is the best-monetizing pattern on Steam** ($4.1B H1 2025; all top-5 new
  sellers co-op). Co-op titles over-convert wishlists **50–260×** vs ~0.15× median.
- **PvE extraction is proven without PvP** (Escape from Duckov: 3M copies).
- **Sci-fi/space co-op is the named-underserved "2026 trend."** The comedy-horror
  *facility* corner (Lethal Company, R.E.P.O., Content Warning) is saturated; the
  **systemic-ship + roguelite + space-salvage** pocket is white space.
- **Streamable by construction:** proximity voice + systemic disasters + extraction
  tension produce 15-second clips by default — the test R.E.P.O./PEAK passed and the
  clones failed.

**Our differentiation vs the lineage:** the level isn't a static map you memorize — it's
a **simulated dying machine**. Reactors melt down, hull breaches vent atmosphere and
*suck players into space*, power must be rerouted to open doors, and the wreck's layout
is procedurally assembled every run. That systemic + roguelite depth is what the
session-based comedy clones lack, and it's what gives us a 50–100h retention tail.

---

## 3. Core Gameplay Loop

### 3a. Moment-to-moment (the 30-second loop)
Move through a dark, cramped wreck → **scan/appraise** what's around you (value vs weight
vs risk) → **cut / pry / unbolt** salvage → manage your light, oxygen, and load → react to
a threat (a breach, a flicker, a sound) → decide: *grab it or leave it.* Tension comes from
**information scarcity** (you can't see far, you can't carry much, you can't be sure what's
ahead) and **commitment** (cutting salvage takes time and makes noise/light).

### 3b. The run / shift (the 10–20 minute loop)
1. **Briefing** aboard your tug: pick a wreck from the sector map (each shows risk tier,
   wreck class, known hazards, and a salvage-value estimate). Equip loadout from what you own.
2. **Insertion:** breach the wreck. A **soft timer** starts — the wreck is decaying. Power is
   low, systems are failing, and the longer you stay the worse it gets (reactor instability
   climbs, more of the dark "wakes up," hull integrity drops).
3. **Salvage:** explore, appraise, extract valuables, solve light systemic puzzles (restore
   power to reach a sealed cargo bay; vent a flooded-with-coolant section; stabilize a reactor
   to loot the core). Carry capacity forces **trip planning** — stash near the airlock, or risk
   a heavy run.
4. **The turn:** at some point the wreck crosses a threshold — alarms, a reactor breach
   countdown, a hull failure, a hunting entity escalating — and the run flips from *greed* to
   *escape*.
5. **Extraction:** get yourself **and your haul** back to the airlock/tug and undock before
   the wreck (or you) dies. **Only extracted salvage counts.** Death drops your carried haul
   in the wreck.

### 3c. Meta (the multi-run loop)
Back at the **tug / home dock:** sell salvage → pay down the **company debt** (the framing
goal + soft difficulty governor) → buy **tools, ship modules, suit upgrades, consumables** →
unlock **new sectors** (harder wreck classes, new hazards, new salvage) → take a bigger run.
Roguelite spine: **persistent unlocks** (tools, blueprints, ship upgrades) + **per-run
volatility** (wreck seed, modifiers, what you choose to risk).

### 3d. How player count changes the experience (for the better)
| Players | Experience |
|---|---|
| **1 (solo)** | Slow, methodical, genuinely scary. You are the engineer, hauler, and lookout. Lower threat density, smaller wrecks, no revive — every decision is yours. Mastery fantasy. |
| **2** | Buddy-system tension. One cuts while one watches the dark. Shared hauling doubles greed-vs-safety drama. |
| **3** | Role specialization emerges (power/engineering, navigation/scanning, hauling, security). Bigger wrecks, parallel objectives. |
| **4** | Full systemic chaos: someone's rerouting power while someone's venting a breach while someone screams that it's in the vents. Peak clip generation. |

Difficulty and reward **scale with crew size** (more threats, bigger/richer wrecks, more to
carry) so 4-stacks aren't trivial and solo isn't impossible.

---

## 4. The Signature Hook (the ONE thing)

**"The wreck fights back — and you can break it on purpose."**

Every wreck is a **systemic, destructible, decaying machine** you manipulate against itself:
- **Reroute power** to open doors, charge your cutter, or run the lights — but every system you
  power draws from a failing reactor you're destabilizing.
- **Breach hulls deliberately** to vent a section: blow a window to suck an enemy (or a
  teammate) into space, or to drain a flooded compartment — at the cost of explosive
  decompression you'd better be braced for.
- **Race the reactor:** the richest salvage is in the reactor core / sealed vaults, reachable
  only by pushing the wreck toward meltdown. The deeper the greed, the louder the countdown.

This is the clippable, word-of-mouth identity: *"we vented the cargo bay to space to kill the
thing chasing us and lost half our loot doing it."* No competitor in the Lethal-Company lineage
has the **systemic-ship sabotage + space vacuum physics** as the core toy. That's our 15-second
clip and our moat.

---

## 5. Systems

### 5.1 Salvage & appraisal
- Salvage has **value, weight, volume, and fragility.** A scanner/appraiser tool reveals value;
  some salvage must be **cut, unbolted, or carefully extracted** (time + noise + light).
- **Greed economy:** richest items are heaviest, deepest, or guarded by a hazard. Carry capacity
  and the extraction timer force constant triage.
- **Stash-and-trip** logistics: drop salvage near the airlock to bank trips, but anything not
  *extracted* (undocked with) is lost on death/wreck-collapse.

### 5.2 Threat & escalation (the heartbeat)
A single rising **"Wreck Instability"** meter governs tension (not a visible countdown clock —
felt through diegetic signals: flickering lights, groaning hull, reactor alarms, more activity
in the dark). Drivers:
- Time inside.
- Systems you power on (greed costs stability).
- Noise/light you generate (attracts entities).
- Deliberate sabotage (venting, overloading) spikes it.
At thresholds: lights fail → gravity flickers → reactor warning → **hard countdown to
catastrophe** (meltdown / total hull failure). Crossing the final threshold flips the run to escape.

### 5.3 Resource management (the wreck-as-enemy systems)
- **Light:** darkness is the default. Flashlights, flares, helmet lamps, and *restoring wreck
  power* are all light sources with tradeoffs (battery, noise, attracting things). Running dark
  is quieter but blind.
- **Oxygen/atmosphere:** sections may be vacuum, flooded with coolant, or full of toxic gas.
  Suit O2 is finite; breaches change atmosphere dynamically.
- **Power:** a finite, reroute-able resource on the wreck. The central management puzzle.
- **Weight/load:** governs movement speed, stamina, and ladder/zero-g handling. Overloading is a
  real, tempting mistake.
- **Reactor heat/instability:** the meltdown clock; also a loot gate.

### 5.4 Roles & asymmetry (teamwork without forced classes)
No hard classes — instead **tools and skill points** let players *drift* into roles:
Engineer (power/reactor), Scanner/Navigator (mapping, appraisal), Hauler (capacity, rigging),
Security (the few combat/deterrent tools). Solo players carry a generalist kit. This rewards
coordination without locking anyone out of a feature.

### 5.5 Combat, threats & death
- **Combat is a last resort, not a power fantasy.** Most entities are avoided, deterred, lured,
  or vented — not gunned down. Limited, situational tools (welder, EMP, flare, lure, the
  environment itself). This keeps art/AI scope lean and keeps tension high.
- **Entities** are systemic, not scripted: drawn by light/noise/heat, with simple legible
  behaviors that combine into emergent danger. v1 ships **3–4 archetypes** (e.g. a sound-hunter,
  a light-averse stalker, a hull-parasite that causes breaches, an environmental hazard-swarm).
- **Death:** carried salvage drops where you die. **Co-op:** downed → revivable within a window
  (drag the body to safety / use a med-tool); full death = wait at the tug or respawn next shift
  depending on difficulty. **Solo:** no revive — death ends the shift, you keep only banked/
  extracted salvage. Roguelite framing means death is a setback, not a wipe (persistent unlocks
  remain).

### 5.6 Procedural wreck generation
- Wrecks are assembled from a **modular kit** of rooms/corridors/junctions snapped along a
  **room-graph** (airlock → arteries → objective spaces → reactor/vault), seeded per run.
- Each wreck has a **class** (freighter, mining rig, science vessel, derelict warship, colony
  hauler) defining layout grammar, salvage tables, hazard palette, and aesthetic.
- **Net-deterministic:** seed-synced so all clients generate identical geometry; only entity/
  physics state is replicated. (See tech doc.)
- Hand-authored modules + procedural assembly = variety on a tiny art budget, with the
  systemic layer (power/atmosphere/reactor) making even repeated modules play differently.

---

## 6. Meta-progression & retention

- **Debt-driven goal:** an escalating company debt is the spine — pay it off to "win" a sector,
  unlocking the next, harder one. Doubles as a soft difficulty/economy governor.
- **Persistent unlocks:** tools, blueprints, suit/ship modules, sector access. These are the
  roguelite backbone that makes "just one more run" pull.
- **Per-run variety:** wreck seed + class + **shift modifiers** (e.g. "ion storm: no comms,"
  "salvage rush: double value, half time," "blackout: no wreck power," "infestation") keep runs
  fresh and create build/route decisions.
- **Mastery curve:** systemic depth (power routing, atmosphere, reactor brinkmanship) gives a
  high skill ceiling so 50–100h players still improve. **Anti-grind:** progression gates content,
  not numbers — no boring stat-walls; new tools open new *tactics*, not just bigger numbers.
- **Weekly seed / leaderboard** (post-EA): a shared seeded wreck with a value-extracted
  leaderboard for the hardcore + streamer competition.

---

## 7. Co-op design specifics
- **Drop-in / drop-out** between shifts (lobby at the tug); ideally mid-run join for friends.
- **Proximity voice** is core: a gameplay system, not a chat feature. Distance + walls + radio
  relays matter; comms break down as the wreck dies (a tension and comedy generator).
- **Shared economy, individual stakes:** salvage is pooled to the crew; death's personal sting
  (dropped haul, being the one stuck venting the breach) drives the social drama.
- **Trust/friendly-fire:** vacuum, venting, and heavy doors mean you *can* kill a teammate
  (usually by accident). We lean into emergent-accident comedy, with options to soften FF for
  public lobbies.
- **Emergent-moment generators (by design):** breaches, power loss, reactor countdowns,
  comms blackout, weight-induced "I can't make it!" sprints to the airlock.

---

## 8. Content scope — Minimal Lovable Product (Early Access)

Ship **small but complete**, then expand (the proven EA path of Lethal Company / R.E.P.O.):
- **1 sector**, **2 wreck classes** (e.g. freighter + mining rig) with distinct grammar/loot/hazards.
- **3–4 entity archetypes.**
- **The full systemic core:** power rerouting, atmosphere/vacuum + breaches, reactor/meltdown,
  light, weight, extraction.
- **~8–12 tools** (cutter, scanner, flashlight/flares, welder, rigging/hauler kit, EMP, med-tool,
  a couple sabotage tools).
- **Meta loop:** tug hub, debt economy, ~20–30 unlock nodes, 4–6 shift modifiers.
- **1–4 player co-op + solo**, proximity voice, Steam lobbies.

**Post-EA roadmap:** more sectors/wreck classes, more entities, deeper ship-upgrade tree,
weekly seed/leaderboards, cosmetics, modding support, console ports.

---

## 9. Name candidates & store hook

**Working titles** (evocative, short, searchable):
1. **SALVAGE** (placeholder; generic/SEO-weak — likely rename)
2. **DERELICT**
3. **HOLLOW HAUL**
4. **DEADWEIGHT**
5. **VOIDPICKERS**
6. **SCRAPLINE**
7. **LAST SHIFT**
8. **REACTOR DEBT** / **DEBT TO THE VOID**

**Store short hook (draft):**
> *Strip dead starships for everything they're worth — before the dark, the vacuum, or the
> reactor takes it back. A 1–4 player co-op salvage roguelite where the wreck is the enemy and
> greed is the only way out of debt.*

---

## 10. Open questions for reconciliation
- First/third-person (or both)? (Leaning **first-person** for immersion/fear + cheaper animation;
  confirm with tech/art docs.)
- Permadeath severity on solo vs co-op default.
- How hard to lean into comedy vs horror (the tonal dial that defines marketing).
- Title (SALVAGE is a placeholder).

# Competitive Teardown & Differentiation — SALVAGE

_Synthesized by orchestrator from competitive sub-research (Lethal Company, R.E.P.O., Content
Warning, Phasmophobia, Deep Rock Galactic, Barotrauma, Valheim)._
_All sales/revenue are third-party estimates; concurrent peaks are SteamDB-tracked._

---

## 1. The comp set at a glance

| Game | Team | Price | Peak CCU | Est. copies | The hook | Top complaint |
|---|---|---|---|---|---|---|
| **Lethal Company** (2023) | Solo (Zeekerss) | $9.99 | 240,817 | ~10M+ | Room-acoustic proximity chat + permadeath | Repetition, content drought, **no solo viability** |
| **R.E.P.O.** (2025) | ~8–12 (Semiwork) | $9.99 | 271,571 | ~15M | Physics-handling of fragile loot | Solo scaling, networking jank, repetitive counterplay |
| **Content Warning** (2024) | 5 (Landfall) | $7.99 | 204,439 | Film-the-monster (SpookTube) | Thin long-term content |
| **Phasmophobia** (2020) | 1→small (Kinetic) | ~$13.99 | 112,717 | Investigate ghosts w/ proximity comms | Grind, dated feel pre-rework |
| **Deep Rock Galactic** (2018) | ~32–44 (Ghost Ship) | $29.99 | 53,558 | 4 hard-distinct classes + destructible caves | Content cadence, overclock RNG grind |
| **Barotrauma** (2019) | ~dozen (FakeFish) | $34.99 | 19,627 | Systemic crew chaos, "everything breaks" + traitor | **Brutal learning curve, weak solo bots** |
| **Valheim** (2021) | 5→16 (Iron Gate) | $19.99 | 502,000 | Approachable survival + boss-gated biomes | Content drought (18mo between updates) |

---

## 2. Pattern synthesis — the shared success ingredients

1. **Proximity voice chat as the engine.** Every breakout (Lethal, R.E.P.O., Content Warning,
   Phasmo) makes spatial/occluded voice *core*. It manufactures the emergent comedy + horror that
   gets clipped — the game writes the streamer's content for them.
2. **Cheap + monetization-clean.** $8–$15, buy-once, no pay-for-power. Communities cite clean
   monetization (DRG/R.E.P.O.) as a loyalty driver. The friend-group multiplier rewards low price.
3. **A single legible "verb"/hook** that reads in a 15-second clip (Lethal's proximity-death,
   R.E.P.O.'s fragile-physics, Content Warning's filming). Clones without a fresh hook are the dead 79%.
4. **Fair-but-tense risk/reward loop:** go in → grab loot under escalating threat → extract → spend
   → harder run. Greed vs. safety, decided constantly.
5. **Procedural variety + a hub/meta loop** for replayability (DRG missions, Lethal quotas, Valheim
   biomes).
6. **Cheap to run** (P2P/listen-server friend-groups, not matchmaking-dependent) → survives the
   cold-start problem PvP games die to.
7. **Streamability is the marketing.** ~41 hours-watched ≈ 1 sale; multiplayer over-converts.

**Shared failure modes:** content drought from tiny teams (Lethal, Valheim, DRG all hit it);
networking jank (R.E.P.O.); repetitive levels/counterplay; **weak solo play** (Lethal & R.E.P.O.
are barely solo-viable; Barotrauma's solo bots are infamous); and brutal onboarding capping reach
(Barotrauma — 25× smaller peak than the approachable Valheim).

---

## 3. Differentiation map — our white space

Most Lethal-lineage hits are **earthbound facility comedy-horror** (Lethal, R.E.P.O., Content
Warning) or **party/climbing** (PEAK). The **derelict-spacecraft + systemic-ship simulation +
roguelite progression** combination is genuinely underpopulated. Our sharp differentiators:

1. **The wreck is a systemic, breakable machine (Barotrauma's DNA, made accessible).** Reactors melt
   down, hulls breach and vent atmosphere, power must be rerouted. *But we ruthlessly flatten the
   onboarding curve that caps Barotrauma's reach* — the #1 lesson from the DRG-vs-Barotrauma contrast.
2. **Deliberate sabotage + vacuum physics as the signature toy.** Vent a section to space to kill a
   pursuer (or lose your loot doing it). No lineage competitor has systemic-ship sabotage + vacuum as
   the core verb — this is our R.E.P.O.-grade clippable hook.
3. **Genuine solo viability** — the unsolved gap in Lethal Company AND R.E.P.O. (both "barely solo").
   We design SP as a first-class tense survival-horror experience (difficulty/threat-density scale
   with crew size), widening the buyer base beyond friend-groups (cf. Escape from Duckov's PvE solo
   extraction → 3M copies).
4. **Roguelite meta-progression depth** the session-based comedy clones lack — the retention tail
   (DRG/Valheim hundreds of hours) without DRG's overclock-RNG grind.
5. **Sci-fi/space setting** — the explicitly named underserved "2026 co-op trend," vs. the saturated
   facility-horror corner.

---

## 4. Feature steal-list (attributed, adapted)

- **Room-acoustic proximity voice** (Lethal Company) → core comms + isolation fear; walkie-talkies.
- **Physics-driven fragile loot handling** (R.E.P.O.) → salvage has weight/fragility; hauling drama.
- **Hard-distinct roles/tools** (Deep Rock Galactic) → soft role drift via tools, *not* forced classes.
- **Systemic damage + reactor/flood sim + traitor option** (Barotrauma) → the wreck-as-enemy systems,
  accessible.
- **Boss/biome-gated progression** (Valheim) → sector/wreck-class gating via the debt economy.
- **Free earned-only cosmetics, no FOMO** (DRG/R.E.P.O.) → loyalty + clean monetization.
- **Built-in content-capture** (Content Warning's SpookTube) → consider a "salvage-cam"/replay/photo
  mode that produces shareable footage (designed-for-the-flywheel).

---

## 5. Anti-pattern list — mistakes we must avoid

- **No solo viability** (Lethal/R.E.P.O.) → we make solo first-class.
- **Brutal onboarding** (Barotrauma) → progressive disclosure, tutorialized systems, forgiving early
  wrecks.
- **Networking jank** (R.E.P.O. desync/item-drop bugs) → invest in authoritative-host netcode early;
  it's on the critical path.
- **Content drought** (Lethal/Valheim/DRG) → realistic post-launch cadence; withhold a 1.0 splash;
  procedural variety reduces per-update content pressure.
- **Repetitive levels/counterplay** ("hide under a table till it leaves") → systemic + roguelite
  variety; enemies with real, varied counterplay.
- **Mod-dependency for core QoL** (Lethal needs hot-join/loot-total mods) → ship hot-join, run
  summaries, and helmet-cam-style features in the base game.
- **Predatory monetization** → never; it's a loyalty *liability* in this community.
- **Empty-lobby / matchmaking dependence** → co-op friend-group "atomic network" + solo fallback +
  AI/bots so the game is always playable.

---

## 6. Positioning statement

> **For co-op players who love the tension and chaos of Lethal Company and R.E.P.O. but are tired of
> facility reskins and games that fall apart solo — SALVAGE is the space-salvage extraction roguelite
> where the derelict itself is a breakable, simulated machine you loot, sabotage, and barely escape.
> Unlike Lethal Company, it's genuinely great solo and systemically deep; unlike Barotrauma, anyone
> can pick it up.**

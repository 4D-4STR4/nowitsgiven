# Master Plan — SALVAGE (orchestrator synthesis)

_The single-page decision document. Synthesizes the market, GDD, tech, art/production, business,
and competitive docs into one recommendation + roadmap._

---

## 1. The recommendation (go / no-go)

**GO.** Build **SALVAGE** — a 1–4 player co-op **derelict-salvage extraction roguelite** — as a
lean, Early-Access-first Steam title. The evidence is unusually strong and consistent across all six
research streams:

- **The lane is the best risk/reward bet in indie gaming.** Co-op PvE generated **$4.1B in H1 2025**;
  all of Steam's top-5 new sellers of 2025 were co-op. The format keeps minting hits (R.E.P.O. ~15M
  copies, PEAK 10M, Content Warning 2.2M paid) **from teams of 1–12 people on budgets from ~$0 to
  <$200k.**
- **The risk/reward shape is forgiving:** at a PEAK-style budget ($20–60k incl. labor), even the
  **pessimistic** scenario (~5–15k copies) roughly breaks even; **base** nets **~$150–300k**;
  **optimistic ~$1.5M+**; the viral tail is uncapped ($10M+). Break-even ≈ **2–6k copies**.
- **We have defensible white space.** The comedy-horror *facility* corner is saturated, but
  **space-salvage + systemic-ship simulation + roguelite progression + genuine solo viability** is
  underserved — and "sci-fi/space co-op" is the named **2026 trend**.

The bet is **winnable but not a lottery ticket**: success requires (1) one legible clippable hook,
(2) solo viability, (3) clean execution, and (4) ~20–40k wishlists driven by an early demo. All four
are within a small team's control.

---

## 2. What we're building (one paragraph)

You're a salvage crew working off a company debt. Each shift you jump to a **procedurally-assembled
dead starship**, cut your way in, and strip it for valuable salvage while the wreck **actively dies
around you** — failing power, vacuum, darkness, and a **rising Wreck Instability** that ends in
reactor meltdown. The richest salvage is the deepest and heaviest, so every second is a **greed-vs-
escape** decision. **Extract to the airlock before the clock kills you** — only extracted salvage
counts — then upgrade gear/ship/crew at the home tug and jump deeper. Fully tense **solo**; pure
chaos in **co-op** with proximity voice. **Signature hook:** the wreck is a breakable machine you can
**sabotage** — vent a hull breach to suck a pursuer (or your loot) into space.

## 3. The differentiators (our moat)
1. **The wreck is a systemic, breakable machine** (Barotrauma DNA) — *made accessible* (the lesson
   from Barotrauma's reach-capping difficulty vs. approachable Valheim/DRG).
2. **Deliberate vacuum-vent sabotage** as the signature clippable toy — no lineage competitor has it.
3. **Genuine solo viability** — the unsolved gap in Lethal Company AND R.E.P.O., and our defense
   against the empty-lobby death spiral that kills co-op indies.
4. **Roguelite meta-progression depth** the session-based clones lack → the 50–100h retention tail.

## 4. The non-negotiables (lessons from the graveyard)
- **Single SP/MP code path** ("host with one player") — solo is first-class, co-op is never a retrofit.
- **Listen-server P2P (Steam Relay), no dedicated servers** — beats cold-start; no live-service cost.
- **Clean monetization forever** — premium $14.99→$19.99, cosmetics only later, never pay-for-power.
  (Tarkov's "Unheard" P2W scandal and Hunt's "1896" review-bomb show betrayal is existential.)
- **Audio + proximity voice as core**, not polish — it's the genre's fear engine *and* its marketing.
- **Procedural variety + roguelite** to dodge the content-drought cliff that hit every comp.
- **Ship hot-join, run summaries, helmet-cam-style features in-base** (don't force the mod-dependency
  Lethal Company has).

---

## 5. Engine & tech (see `03-TECH-ARCHITECTURE.md`)
**Unity** (every comp uses it; best netcode/Steamworks/asset/modding ecosystem) + **FishNet**
networking + **Facepunch.Steamworks** P2P relay + **Dissonance** proximity voice + **FMOD** audio.
Net-deterministic seeded procedural wrecks from a ~20–30-piece modular kit. Godot 4 is the acceptable
free fallback; the architecture is engine-agnostic.

## 6. Art & production (see `04-ART-AUDIO-PRODUCTION.md`)
**"Salvage-Industrial Low-Poly"**: flat-shaded low-poly, palette-locked per wreck, diegetic-only
lighting, heavy fog + grain post — cheap to make, distinctive, and *darkness is free content*.
**MLP:** 2 wreck classes, 3 enemies, full systemic core, ~5–10 tools, the meta loop. Budget
**~$700–900 shoestring / ~$6–12k comfortable**. **~14–20 months to 1.0**, revenue at EA ~month 9–11.

## 7. Business & GTM (see `05-BUSINESS-GTM.md`)
Premium **$14.99 EA → $19.99 1.0**. Target **20–40k wishlists** via an **early free demo + build-in-
public TikTok/Shorts + small-creator key seeding**, cashed in at your **one Next Fest**. Launch into
Popular Upcoming with a wishlist blast; protect a Very Positive score with launch-week responsiveness.
Predictable update cadence; cosmetic-only MTX after goodwill is banked; seasonal events for the tail.

---

## 8. Roadmap (phased)

| Phase | Goal | Exit gate |
|---|---|---|
| **0. Prototype (now)** | Validate the core loop is fun (gray-box) | ✅ Playable loop proven — see `game/prototype/` |
| **1. Vertical slice** | 1 wreck class fully styled, 1–2 enemies, proximity voice + co-op sync, the loop *feels* shipped | "Is it fun & scary?" + trailer footage |
| **2. Steam page + demo** | Coming Soon page live, capsule + 60s trailer, free demo out early | Wishlist velocity climbing |
| **3. Next Fest** | Cash in accumulated wishlists | Land in Popular Upcoming territory |
| **4. Early Access launch** | Full MLP, stable co-op, 8–15h of fun | Revenue begins; Very Positive reviews |
| **5. EA live-ops** | Content drops every 6–10 weeks; react to data | Sustained CCU + wishlist tail |
| **6. 1.0** | Withheld content splash, polish, localization, controller | Second marketing beat; price → $19.99 |

## 9. Immediate next steps (the critical path)
1. **Lock the title** (SALVAGE is a placeholder; DERELICT is the lead alternative) and resolve the
   open GDD questions (first-person; comedy↔horror tonal dial; solo permadeath severity).
2. **Stand up the Unity project** from the scaffold in `03` — listen-server bootstrap + FishNet +
   Steam transport connecting two clients first (prove the SP=MP code path).
3. **Port the prototype's proven loop** (seeded wreck gen, salvage value/weight, instability/meltdown,
   extraction) into Unity systems — the prototype *is* the spec.
4. **Prove proximity voice + 4-player sync early** (the hardest tech risk, on the critical path).
5. **Build the vertical slice** to the "is it fun?" gate; capture trailer footage.
6. **Put the Steam page live ASAP** — wishlists compound from day one.

## 10. Financial summary (net, after Steam + refunds + VAT/regional ≈ gross × ~0.52)

| Scenario | Units (yr 1) | Net | vs. lean budget ($20–60k) |
|---|---|---|---|
| Pessimistic | 5,000 | ~$50k | ~break-even to small profit |
| Base | 30,000 | ~$300k | **5–15× return** |
| Optimistic | 150,000+ | ~$1.5M+ | life-changing |
| Viral tail | 1M+ | $10M+ | unplannable, build for it |

**Bottom line:** the floor is survivable, the ceiling is uncapped, and the plan is *familiar proven
chassis + one genuinely fresh, streamable twist (systemic-ship vacuum sabotage) + solo viability.*

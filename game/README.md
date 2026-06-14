# SALVAGE

A 1–4 player co-op **derelict-salvage extraction roguelite** for Steam. Board procedurally-generated
dead starships, strip them for salvage while the wreck dies around you (failing power, vacuum,
darkness, rising reactor instability), and **extract before the meltdown clock kills you**. Spend your
haul to upgrade gear, ship, and crew — then jump deeper. Tense **solo**, chaotic in **co-op** with
proximity voice. *Lethal Company × Barotrauma × Deep Rock Galactic, with a roguelite spine.*

> Working title — **SALVAGE** is a placeholder; **DERELICT** is the lead alternative.

## Repository layout
```
game/
  README.md            ← you are here
  docs/                ← the full plan (research + design + business + tech)
    00-VISION.md           project vision & doc index  (start with 07, then this)
    01-MARKET-RESEARCH.md  what sells on Steam; revenue math; wishlist mechanics
    02-GDD.md              game design document — loops, systems, the signature hook
    03-TECH-ARCHITECTURE.md engine (Unity), SP/MP-shared netcode, project scaffold
    04-ART-AUDIO-PRODUCTION.md art/audio direction, scope, budget, timeline
    05-BUSINESS-GTM.md     monetization, pricing, marketing, launch playbook
    06-COMPETITIVE-TEARDOWN.md why the hits won; our differentiation & anti-patterns
    07-MASTER-PLAN.md     ★ the synthesis + go/no-go + roadmap — READ THIS FIRST
    08-PROTOTYPE.md       how to run the prototype & how it maps to the Unity build
  prototype/           ← a runnable, dependency-free core-loop gray-box
    index.html             open in any browser to play
    game.js                the loop logic (validates "is it fun?" before engine work)
```

## Play the prototype
Open `game/prototype/index.html` in any modern browser. **WASD** move · **E** grab/extract ·
**F** flashlight · **V** vent a hull breach · **R** new wreck. Bank the quota before the reactor
melts down — only *extracted* salvage counts.

## The thesis (one line)
The most reliably-monetizing pattern on Steam (cheap, streamable, co-op PvE) + a defensible white
space (systemic-ship space salvage + roguelite + genuine solo viability) + clean, lean execution.
See `docs/07-MASTER-PLAN.md`.

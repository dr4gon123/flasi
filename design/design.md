# FLASI Design System

Status: **in ideation** — built stage by stage with @dr4gon123. Nothing below
is final until its section says `LOCKED`. No visual mockups until §1–§3 exist.

Supersedes `design/brand.md` when §1–§5 are filled (then brand.md gets deleted).

---

## §0 Taste & references `LOCKED`
*What we love, what we hate, and why. The root of every later decision.*
Board: [`flasi-reference-board.html`](../../.zcode/v2/visualizations/c61cacb3da0d15884fa7034dfc86def95b5465c78d2274ef5bb4e94361f8d0a5/flasi-reference-board.html)

### Feels like FLASI
- **7 · Swiss International Style** (Müller-Brockmann, *Beethoven*, 1955) —
  composition from structure; grid, type, one element; nothing decorative exists.
- **3 · Teenage Engineering** — mono labels, quiet grey, one warm accent,
  hardware-plate precision.

### The discovery (user's words)
> "FLASI is more fluid. Logs are a constant chaotic stream of data.
> FLASI finds meaning in chaos."

Two *structure* styles chosen to describe a *fluid* product → the tension is
the brand. Rigid system outside, living stream inside. Structure is the frame;
the data's motion is the only decoration allowed.

### Canvas
Dark, high contrast — matches the maintainer's own Grafana dashboards and the
SOC-at-2am audience. Dark-first canon.

### Not FLASI
- **suckless-style hostile minimalism** — unfinished ≠ honest.
- The polished dark-SaaS default (Linear costume) — the AI-slop lane.
- Corporate-safe friendliness — disappears into the infrastructure crowd.

### What this rules in / out (implications, not decisions yet)
- In: grids, disciplined typography, mono labeling, few accents used precisely,
  motion only as *data* motion.
- Out: glow-for-glow's-sake, decoration without a job, beige-retro costume,
  hostile bare-bones.

## §1 Voice `LOCKED`

### Positioning pivot (user, 2025-11)
> "Even if FLASI were not free, it would be better than any other solution.
> The real value of FLASI is the analytics done to 'understand' firewall logs."

**Cost is a footer fact, never the headline.** The old hook ("Tired of
expensive SIEMs?") is retired from hero copy. The value is *understanding*:
analytics that read the chaos.

### Register: mythic operator
Mythic cadence (option D), grounded by operator vocabulary. Short declarative
sentences. Present tense. The stream is a living thing; FLASI reads it.
Never salesy, never corporate, never cute.

### Lexicon
- **Keeper words (operator pool, fully adopted):** hunt · signal · intercept ·
  trace · watch · threat. These may appear anywhere, including headlines.
- **Working words (engineering):** parse · pipeline · field · schema · query ·
  throughput. Docs and feature sections only — never headlines.
- **Demoted (honest product):** free · open source · hours-not-weeks. Facts
  section and footer only. State them plainly, never as the pitch.

### Banned words (proposed, user to confirm)
seamless · enterprise-grade · revolutionary · AI-powered · "free/cheap" in any
headline.

## §2 Organizing idea `LOCKED` — A + B fused

One idea every visual decision must serve. If a decoration doesn't serve it,
it dies.

**The shared core (already locked by §0+§1):** firewall logs are a constant,
chaotic stream. FLASI is the thing that *reads* it. The dragon is that reader —
a creature of the stream, formed by the stream, hunting in it.

Candidate statements of the idea (pick / remix):

- **A · "The reader in the stream."**
  Every visual = a frame (grid, plate, label) applied to flowing data. The
  frame is calm; the data is alive. FLASI is the reader standing in the current.

- **B · "Signal out of chaos."**
  Every visual shows a gradient of order: raw chaos at the edges, structured
  meaning at the focus. Pages progress from flood to focus.

- **C · "The hunt is continuous."**
  Every visual implies watchfulness: the stream never stops, neither does the
  scan. Motion is ambient, perpetual, patient.

Recommendation: **A**, with B as its compositional rule. A names the dragon;
B tells layouts what to do.

**LOCKED as A+B fused:** *"The reader in the stream"* is the story; *"signal
out of chaos"* is its compositional rule (layouts flow from flood to focus).
C ("the hunt is continuous") is absorbed as the motion rule in §3.

### The one-line test
Every visual decision must pass: *"Does this help the reader read the stream?"*
If it only decorates, it dies.

## §3 Art direction `PROPOSED LOCK — 2 decision points`
Graphic language derived from §2. Swiss + TE (§0) applied to *the reader in
the stream*.

1. **Grid — the frame.** A strict columnar grid; content always aligns. The
   grid may reveal itself as 1px hairlines (chassis silkscreen), at panel
   edges only. Never decorative randomness.

2. **The stream — the only texture.** Flowing data/log lines are the sole
   permitted decorative element. Always channeled: inside a framed band, or
   very low contrast behind content. Horizontal only (the stream's direction),
   constant patient speed — no bounces, no entrances (C's rule).
   **Amendment (user, stage 5):** the texture is *real log lines*, grayed —
   not abstract dashes. The page itself is alive: a constant grayed log stream
   flows behind the hero (and may re-appear as inter-section dividers at even
   lower contrast). Implementation note: CSS-transform drift of prerendered
   columns first (GPU-cheap); [`@chenglou/pretext`](https://github.com/chenglou/pretext)
   (canvas text measurement, no reflow) as the substrate if streams become
   layout-aware/dynamic. Pretext measures; it does not animate.

3. **Flood → focus (B's rule).** Every layout moves from raw chaos at the
   edges to structured meaning at the focus: stream texture fades as content
   takes over. Sections progress from flood (hero) to focus (install/CTA).

4. **Type — two voices.**
   - *The reader* (FLASI speaking): a precise grotesk for display and UI text.
     TE-style mono caps for labels (fig. 01 · TRAFFIC · 48H).
   - *The stream* (the machine speaking): monospace log text, treated as
     material — columns of raw fields, data tables, terminal plates.
   - This retires round 1's all-mono idea → decision point **D2** below.

5. **Color — the fight lives in the data.**
   - Canvas: dark, high contrast (locked in §0).
   - **One brand accent** for the reader's marks (links, active states, the
     dragon) → decision point **D1** below.
   - **Data colors are data-only:** red = threat/deny, blue = analyst/insight,
     amber = warn, green = permit. They appear in charts, logs, badges — never
     as brand chrome. The red/blue fight from round 1 survives, but only
     inside the stream where it means something.

6. **Product shots — plates, not screenshots.** Dashboards and terminals are
   presented as specimens: framed, labeled (fig. 01 — traffic · 48h window),
   floating on the grid. Swiss plate discipline, TE caption style.

7. **Dragon treatment.** Small: solid silhouette stamp, like a chassis mark.
   Hero: the one spectacle per page — stream-formed (lines flowing through the
   silhouette). Never mascot-waving, never cartoon.

### Decision points
- **D1 · Brand accent:** warm signal amber (TE homage, warm-on-cold contrast)
  vs. monochrome chrome (accent = data colors only). Rec: warm amber.
- **D2 · Display face:** grotesk display + mono machines (Swiss-true, rec)
  vs. mono display (terminal purist).

## §4 Foundations `LOCKED` — verified on specimen sheet

Decisions D1 (monochrome chrome) and D2 (grotesk display + mono machines)
applied. Everything below is a consequence, not a choice.

### Color — tokens
```css
/* chrome — greys only, hierarchy via contrast & weight */
--void:   #0A0C10;  /* canvas */
--panel:  #10141B;  /* plates: terminals, framed screenshots */
--panel2: #151A23;  /* nested surface */
--line:   #232A36;  /* hairlines: grid, borders, rules */
--text:   #E9EDF2;  /* primary */
--dim:    #97A1B0;  /* secondary */
--faint:  #5C6675;  /* labels, captions */
/* data — data surfaces only (charts, logs, badges, status) */
--threat:  #FF3B4E;  /* deny / adversary */
--analyst: #46A8FF;  /* insight / ECS mapping / analyst action */
--warn:    #FFB454;  /* WARN */
--permit:  #3DDC97;  /* permit / ok */
```
Rules: no `--accent` token exists. Primary button = solid `--text` fill with
`--void` text; ghost = 1px `--line`. Links = `--text` underlined. Hue appears
only inside data. The stream-formed dragon may carry data hues because it is
literally made of the stream; every other brand surface is monochrome.

### Type — two voices `LOCKED: P2`
- **P2 chosen:** **Archivo** (display + body — the reader) +
  **IBM Plex Mono** (machines — the stream). Highest between-voice contrast:
  poster-grotesque DNA vs documentation-mono DNA. Chosen over Space Grotesk +
  Space Mono (same-family harmony blurs the voices) and Inter + JetBrains Mono
  (neutral-on-neutral, erases them).
- Machines: labels, logs, tables, captions.
  Label style: `11px · caps · +0.14em tracking · --faint`.
- Scale: display clamp(40–88px)/1.05 · h2 32/1.15 · body 16/1.6 ·
  label 11 mono. Few sizes, big display, tight leading.

### Space
8px base grid; container 1200px; hairline rules preferred over boxes.
"No box unless the box is the plate" (terminals, framed screenshots, decode
panels).

### Elevation & chrome
Flat. No shadows, no gradients, no rounded-glass. Depth = hairline + contrast.
Radius: 0–6px max (plates 4px; chips 3px). Icons: functional only, 1.5px
stroke, mono text labels preferred (TE style); no decorative icon rows.

### Motion — the hunt is continuous
- **Amended (user, stage 5) — three tiers:**
  - **Ambient (always):** the grayed log stream drifts horizontally, linear,
    constant slow speed; log lines arrive at steady cadence. Never stops.
  - **Response (on interaction):** hover/touch may highlight, reveal, connect —
    one mechanism per element, quiet, instant.
  - **Assemble (once, on load):** content may build in *once*, calmly and
    fast (<800ms total, no bounce, no stagger-lag) — then it is still.
    Nothing loops except the stream.
- Counters (EPS) may tick — honest data motion.
- `prefers-reduced-motion`: freeze ambient + assemble; page must stand static.

## §5 Components & layout `BASELINE APPROVED — polish from here`
Wireframe: [`flasi-wireframe.html`](../../.zcode/v2/visualizations/c61cacb3da0d15884fa7034dfc86def95b5465c78d2274ef5bb4e94361f8d0a5/flasi-wireframe.html)
Landing baseline (approved 2025-11): [`landing.html`](landing.html) —
self-contained, opens in any browser; plates embedded as data URLs.

- Argument: flood (01 hero) → proof (02 live parse) → understanding (03 moves,
  04 architecture) → evidence (05 plates, 06 numbers) → invitation (07).
- **W1 = (b):** dragon spectacle once per page, at the §02→§03 divider — the
  turning point from chaos to reading. Stamp everywhere else.
- **W2:** dashboard plates after architecture.
- **§02:** full interactive parse plate kept for live review; **fallback if it
  feels gadget-y in situ: cut the block** — structure must survive without it.
- Background: real grayed log stream per §3.2 amendment.

## Appendix
- [assets/dragon-traced.svg](assets/dragon-traced.svg) — vectorized logo silhouette (usable regardless of direction)

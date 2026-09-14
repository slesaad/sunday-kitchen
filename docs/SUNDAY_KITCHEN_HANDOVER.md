# Sunday Kitchen Handover

**Purpose:** let a fresh session change the meal plan, recipes, or site without rediscovering the architecture or re-making the mistakes below.
**Created:** 2026-08-10
**Status:** in use — the couple ran their first full prep session 2026-08-09. Times below are estimates, not yet validated against a completed session.

Single handover, no separate inventory: the open items are unvalidated estimates and deferred content, not a multi-PR cleanup.

---

## Who this is for

- **Two people, one household.** Vegetarian moving toward vegan. Both lift; goal is muscle gain with fat loss.
- **Person A ~103 lb / 47 kg** → 90–95 g protein, 1,900–2,050 kcal. **Deliberately not in a deficit** — at that bodyweight a deficit costs lean mass. Do not "helpfully" cut their calories.
- **Person B ~183 lb / 83 kg** → 155–165 g protein, 2,600–2,850 kcal.
- The 1.7× spread is handled by **boosting at the plate**, never by cooking two versions.
- Kit: Instant Pot, oven, air fryer, food processor. Shops at Asian + Indian groceries and Costco.
- **Dairy: out. Eggs: 2 dishes max, both droppable. Impossible/TVP: once a week max.**
- **Friday lunch is eaten out** (since 2026-09-13). Four lunch days, **eight containers**, not ten. The aloo tama anchor feeds only Tuesday dinner, so six of its eight servings freeze and one batch lasts four Tuesdays.
- **No amchur, no five-spice** (2026-09-13) — lemon juice finishes the chana and rajma; the Sichuan crumble zone is Sichuan pepper and chili crisp only.
- Likes Yeung Man Cooking and Rainbow Plant Life. The tofu crumbles are adapted from the former.

## Hard constraints — do not quietly relax these

| Rule | Why |
|---|---|
| Same dish twice a week max, never consecutive days | The stated reason previous meal-prep attempts failed |
| Weekend prep ≤ ~3 hrs for two people | Same |
| Weeknight assembly, not cooking | They have 4 evening hours and were losing 2 to cooking |
| Times quoted are **wall clock**, not hands-on | They caught under-estimates twice; see History |

---

## Architecture — read before editing anything

**`build.py` is the single source of truth for all 26 recipes.** It generates:

| Generated | Never edit by hand |
|---|---|
| `recipes.html` | ✅ generated |
| `recipes/*.md` (27 files incl. README) | ✅ generated |
| `icon-{32,180,512}.png`, `manifest.webmanifest` | ✅ generated |
| `Sunday Kitchen Meal Prep.paprikarecipes` | ✅ generated, **gitignored** |

```bash
cd /Users/sadhikar/repo/slesaad/mealprep
python3 build.py              # site + markdown + icons
python3 build.py --paprika    # also rebuild the Paprika archive
```

**Hand-authored files:** `index.html`, `style.css`, `app.js`, `README.md`, `01-the-plan.md`, `02-prep-session.md`, `04-shopping-list.md`, `05-nutrition.md`.

- The PNG icons are written by a hand-rolled encoder in `build.py` (`png()` / `icon_pixel()`) — **PIL is not installed** on this machine.
- Paprika format: ZIP → one **gzipped** JSON per recipe, entry name `<Name>.paprikarecipe`. Schema was reverse-engineered from a real export and matches it key-for-key. JSON is written `ensure_ascii=True` on purpose so no consumer can misread UTF-8 as latin-1.

## Deploy

```bash
git add -A && git commit -m "..." && git push origin main
# Pages rebuilds in ~30-45s
curl -s https://slesaad.github.io/sunday-kitchen/ | grep -c "<some new string>"
```

- Repo: `github.com/slesaad/sunday-kitchen` (**public**, `gh` authed as `slesaad`).
- Site: **https://slesaad.github.io/sunday-kitchen** — added to their phone home screens, so **`index.html` and `recipes.html` are the primary artifacts**, not the markdown.
- `.gitignore`: `*.paprikarecipes`, `prompt.md` (contains their daily schedule — deliberately not public), `.DS_Store`, `__pycache__/`.
- **Never add `Co-Authored-By: Claude`** to commits (user's global rule).

---

## Gotchas — these have already cost time

1. **`index.html` mixes HTML entities and literal glyphs.** `&mdash;`, `&frac12;`, `&middot;`, `&deg;F` appear as entities in most places — but not all. The Saturday-soak paragraph, for one, uses a literal `—`. A `grep` or `str.replace` for either form alone will silently miss half the file. Always `grep -o` the real line first, and let a `count(old) == 1` assert catch you when you guess wrong.
2. **Never `str.replace('', x)`.** A slice built from two `.index()` calls returned empty when the end marker preceded the start marker; `replace('', new)` inserted the block between every character and produced a 57 MB file. Recovered with `git checkout -- index.html`. **Guard every patch with `assert old and s.count(old) == 1`.**
3. **Patch via a script file, not a heredoc.** Apostrophes and backslashes in prose break `<<'PY'` quoting. Write the script to the scratchpad, run it, iterate.
4. **Validate after every HTML edit** — see snippet below.
5. **`gh api .../pages` returns before the build finishes.** Poll the live URL for a known new string.

### Validation snippet — run after any HTML change

```bash
cd /Users/sadhikar/repo/slesaad/mealprep
python3 - <<'PY'
import re, os, html.parser
class V(html.parser.HTMLParser):
    VOID={'meta','link','br','hr','img','input','source','area','base','col','embed','param','track','wbr'}
    def __init__(s): super().__init__(); s.stack=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t not in s.VOID: s.stack.append(t)
    def handle_endtag(s,t):
        if t in s.VOID: return
        if s.stack and s.stack[-1]==t: s.stack.pop()
        else: s.err.append(t)
ok=True
rid=set(re.findall(r'id="([^"]+)"', open("recipes.html").read()))
for f in ("index.html","recipes.html"):
    src=open(f).read(); v=V(); v.feed(src)
    if v.err or v.stack: ok=False; print(f, v.err[:3], v.stack[:3])
    for m in re.finditer(r'(?:href|src)="([^"#:]+)"', src):
        t=m.group(1).split('#')[0]
        if t and not t.startswith('http') and not os.path.exists(t): ok=False; print(f,"missing",t)
    for m in re.finditer(r'href="recipes\.html#([^"]+)"', src):
        if m.group(1) not in rid: ok=False; print(f,"dead anchor",m.group(1))
print("validation:", "OK" if ok else "PROBLEMS")
PY
```

---

## Design decisions worth not re-litigating

- **Anchors + Kit**, not "5 finished dishes". Two freezer-proof anchors carry all lunches and low-energy nights; a component kit carries fresh dinners. Rejected alternatives are in `~/repo/claude-docs/mealprep/2026-08-08-mealprep-design.md`.
- **The Instant Pot anchor's fridge half covers one lunch AND one dinner** — that's why it's 4 servings, not 2. This is the single most confusing thing about the plan; it has its own "Where every batch goes" section on the site. The stovetop anchor is dinner-only since Friday lunch went: 2 in the fridge, 6 frozen.
- **Dinners are never packed into containers.** Held back in a labelled tub. Only the 8 lunch containers get assembled.
- **Tracks are "wet" and "dry", not "Person 1/2".** Deliberate: tracks are interchangeable, whereas Person A/B is fixed by bodyweight. An outside review suggested unifying on A/B — **don't**, it would imply the lighter partner must take the wet track.
- **Mediterranean bowls use roasted chickpeas, not crumbles** — keeps chickpeas and crumbles from competing for the same slot.
- **Freeze only 2 tofu blocks** (crispy tofu). The crumbles are hand-crumbled from *fresh* tofu.
- **Three-zone crumbles**: one sheet pan, three spice profiles, three ingredients out. Sichuan → Wed; cumin-garam → Thu; chili-lime → Fri.

---

## History of corrections — the pattern to expect

Every one of these came from them actually cooking. **Assume remaining estimates are also optimistic.**

| What was wrong | Fix | Commit |
|---|---|---|
| Weeknight times ignored boiling water and chopping (10–15 min claimed) | Now 15–18 wall clock, hands-on stated separately | `ae4a2fd` |
| Wet track had **zero** minutes for washing/chopping its own produce | +12 min knife work at 0:05; session 2h30 → 2h45 | `ae4a2fd` |
| "soy" / "maple" / "balsamic" ambiguous mid-cook | Spelled out everywhere | `bc266a5` |
| "Freeze four blocks" contradicted the crumbles recipe | Freeze two | `43735bc` |
| Falafel had no slot in the Sunday timeline | Pulse 1:10, form during portioning; +15 min on those weeks | `43735bc` |
| Week B "50 min" put crumbles in the oven at 0:00 (a 15-min job) | ~1 hr for two, ~1h30 solo | `43735bc` |
| Rice badly undersized: 3 cups dry ≈ 8 cups cooked, week needs ~17 | 5 cups IP + 3 cups stovetop at 1:28 | `0f98a08` |
| Salad greens and broccoli on the shopping list, used in no recipe | Greens dropped; broccoli became a cauliflower option | `ae4a2fd`, `43735bc` |
| Week B said "marinate the tofu at 0:17" with no marinade; the recipe said "toss in the marinade" | Week B is a real timeline with the marinade inline; recipe step spells it out | see git log |
| Shopping lines bundled several items ("Light soy · dark soy") — hard to tick, easy to miss one | One ingredient per line, each with its purpose | see git log |
| "One 28 oz can of crushed tomatoes a week" bought two cans; anchors are only cooked on Week A | One can per anchor batch; freezer weeks need none | see git log |
| No per-meal macros; "¼ cup crumbles = 8 g" and "Med bowl ≈ 33 g" were both overstated (½ cup ≈ 7 g; Med bowl ≈ 20 g for A) | Macros table on the site and in every meal recipe, computed by `macros.py`; cheat sheet corrected | see git log |
| Friday lunch was planned; they eat out on Fridays | Friday bowl removed; 8 containers; aloo tama freezes 6; chili-cumin veg is 6 portions | see git log |
| Crumbles and veg trays had no portion counts; "roasted veg" named either tray; a stray "roasted chickpeas, 1 can" row contradicted the two-can tray | Batch table states portions per meal and how to split at 1:40; every "roasted veg" now says harissa or chili-cumin; harissa veg = the four Med bowls only | see git log |

---

## Open items

| # | Item | Notes |
|---|---|---|
| 1 | **Validate 2h45 against a real session** | They ran it 2026-08-09. Ask what it actually took. Every prior estimate was low. |
| 2 | **Rice quantity unvalidated** | Just changed to 5+3 cups dry (~19 cooked). Confirm it lasted the week and fit the pot. |
| 3 | **Mobile layout never verified at true phone width** | Chrome window resize was clamped by the OS. CSS is mobile-first so the phone layout is the default case, but nobody has seen it on a phone. |
| 4 | **Anchor rotation cycles 2–5 have no recipes** | Named only: rajma, dal tadka, sambar-style, aloo chana; palak tofu, tofu keema matar, kwati, mismas tarkari. Needed ~week 3 onward. |
| 5 | **`01-the-plan.md` / `02-prep-session.md` overlap `index.html`** | Two sources that will drift. Offered to fold them into the site and delete; user has not decided. **Ask before deleting.** |
| 6 | **Swaps page offered, not built** | They hit 4 substitution questions in a row (harissa, edamame, balsamic, yogurt). Candidates: vital wheat gluten, gochujang, chili crisp, tahini, amchur, dark soy, kashmiri chili, fennel seeds, caraway. |
| 7 | Week 3 seitan session not yet run | Char siu → Mon, chorizo → Fri tacos, shawarma → Med lunch bowls. |
| 8 | Week 5 tempeh | Only if the Asian grocery stocks it. Steam 10 min before cooking. |

**Skip / deferred deliberately:**
- **A separate master ingredient list** — mise en place + inline quantities already cover it; a third copy re-creates the drift problem.
- **Labelling ingredients "Person A / Person B"** — category error. Ingredients aren't per-person; portions are.
- **Anonymising bodyweights** — offered when making the repo public; user chose plain public.

---

## Likely next tasks

### 1. Debrief the first real session
Ask: actual wall-clock time, whether the rice lasted, what ran out, what was unclear.
**Verify:** TBD — every number in `02-prep-session.md` and the `index.html` timeline matches what they report, or is corrected.

### 2. Write anchor rotation cycle 2 (rajma + palak tofu)
Add to `RECIPES` in `build.py` with slugs `anchor-rajma`, `anchor-palak-tofu`. Match the existing anchor shape: 8 servings, `used_in` links, rotation-partner note.
**Verify:** `python3 build.py` reports 27 recipes; `recipes/anchor-rajma.md` exists; validation snippet OK.

**Note:** both anchors are South Asian as of the aloo tama swap, so anchor 2 must contrast on axis — sour, green, minced or brothy — not on cuisine. See the note under the rotation table in `01-the-plan.md`.

### 3. Build the swaps reference (only if asked)
New `REFERENCE`-group recipe, slug `reference-swaps`.
**Verify:** `python3 build.py` succeeds; `recipes.html#reference-swaps` resolves.

---

## Reference commits

- `af5d93b` — name the contents of both roasting trays in the batch table
- `0f98a08` — batch-allocation table, dinners section, rice quantity fix
- `08fb5bc` — ragù balsamic substitutions
- `9898b4b` — pantry harissa recipe
- `9b69f05` — edamame shelled-vs-pods, soy yogurt marked optional
- `43735bc` — tofu freezing count, falafel in the timeline, Week B timing
- `bc266a5` — spell out soy sauce / maple syrup / balsamic vinegar
- `ae4a2fd` — mise en place, chopping time, inline quantities
- `81dda16` — initial: plan, site, recipe pipeline

## Files cheat sheet

| Path | Purpose |
|---|---|
| `build.py` | **Source of truth for all recipes** + generators for site, markdown, icons, Paprika |
| `index.html` | The plan: week, batches, lunches, dinners, Sunday timeline, shopping, numbers |
| `recipes.html` | Generated — all 26 recipes |
| `style.css` | Mobile-first; phone styles are the defaults, media queries add at 34rem / 48rem |
| `app.js` | Expand/collapse, wake lock, shopping-list persistence, wet/dry track toggle |
| `01-the-plan.md` | Weekly rotation, portioning, ramp-up (overlaps `index.html` — see open item 5) |
| `02-prep-session.md` | Mise en place + minute-by-minute Sunday timeline |
| `04-shopping-list.md` | By store |
| `05-nutrition.md` | Targets, per-meal macros, micronutrients |
| `~/repo/claude-docs/mealprep/macros.py` | **Per-meal macro calculator.** Rerun after any portion or recipe change; paste its output into `index.html#numbers` and `05-nutrition.md` |
| `~/repo/claude-docs/mealprep/2026-08-08-mealprep-design.md` | Original design spec + rejected approaches |

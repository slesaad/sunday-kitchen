# Sunday Kitchen

Meal prep plan + static site for two people. Published to GitHub Pages at
**https://slesaad.github.io/sunday-kitchen** and used on their phones while cooking.

## Read this first

**[`docs/SUNDAY_KITCHEN_HANDOVER.md`](docs/SUNDAY_KITCHEN_HANDOVER.md)** — who this is for,
the hard constraints, design decisions not worth re-litigating, the history of corrections,
and the open items. Read it before changing anything.

## The one architectural rule

**`build.py` is the single source of truth for all recipes.** It generates `recipes.html`,
every file in `recipes/`, the icons, the manifest, `anchors.js`, and the Paprika archive.

**Never hand-edit `recipes.html`, `recipes/*.md`, or `anchors.js`** — edit `RECIPES` (or
`ANCHOR_SWAP`, for the plan page's anchor picker) in `build.py` and rerun:

```bash
python3 build.py              # site + markdown + icons
python3 build.py --paprika    # also rebuild the Paprika archive (gitignored)
```

Hand-authored: `index.html`, `style.css`, `app.js`, `README.md`, and the numbered
`0*.md` files.

## The anchor picker

The plan page can switch its Instant Pot anchor (chana / rajma). The cooking facts that
differ live in `ANCHOR_SWAP` in `build.py`, which emits `anchors.js`; `app.js` drops them
into `[data-anchor-slot]` elements in `index.html`. **Adding a fact that differs by anchor
means adding a key to `ANCHOR_SWAP` and a matching `data-anchor-slot` in `index.html`** —
otherwise it silently keeps saying "chana" on a rajma week. Grep `index.html` for `chana`
after any change; only the picker button, the rotation table, and the rajma note should
mention it once rajma is selected.

## Editing index.html

- It uses **HTML entities**, not literal glyphs: `&ugrave;`, `&mdash;`, `&frac12;`,
  `&middot;`, `&deg;F`. Grepping for `frac12` or `—` finds nothing where the entity is used.
  `grep -o` the real line first — and note that some lines mix literal glyphs with entities.
- Patch with a **script file**, not a shell heredoc — apostrophes break the quoting.
- **Guard every replace:** `assert old and s.count(old) == 1`. A `replace('', x)` from an
  empty slice once produced a 57 MB file.
- **Run the validation snippet** in the handover after any HTML change.

## Deploying

`git push origin main` → Pages rebuilds in ~30–45s. Poll the live URL for a new string to
confirm; the Pages API reports "built" before the content is actually served.

## Conventions

- **Times are wall clock**, including come-to-pressure, natural release, and boiling water.
  Every estimate that ignored prep time has already had to be corrected upward.
- **Spell out ingredients** — "soy sauce" not "soy", "maple syrup" not "maple". They cook
  from this on a phone.
- **Say what an item is for.** Every shopping-list confusion so far came from an item with
  no stated purpose.
- Do **not** add `Co-Authored-By: Claude` trailers to commits.

# Sunday Kitchen

A weekday meal system for two people: vegetarian moving toward vegan, lifting, aiming to
add muscle and lose fat. Built to survive contact with a Tuesday.

**Live site: https://slesaad.github.io/sunday-kitchen**

Add it to your home screen — it has an app icon, opens full-screen, and the recipes page
has a "Screen on" button so your phone doesn't dim mid-recipe.

## The idea in one paragraph

Cook **two anchor dishes** and **one component kit** on the weekend. The anchors are
finished, freezer-proof, and get better as the week goes on — they cover every lunch and
any night you have nothing left. The kit is a handful of parts (crispy tofu, tofu
crumbles, rice, roasted veg, three sauces, a shredded stir-fry pack, a bag of edamame)
that combine into a different dinner every night. Anchors are cooked in **double batches**,
so every other weekend is nearly free.

## What it costs

| | Time |
|---|---|
| Week A (full prep, double batches) | **~2h30**, two people in parallel |
| Week B (freezer week) | **~50 min** |
| Any weeknight | **15–18 min wall clock**, 6–15 min hands-on |
| Average per week | **~1h40** |

Against roughly ten hours a week of weeknight cooking.

These are honest numbers — they include the Instant Pot coming to pressure, natural
release, chopping two trays of vegetables, and waiting for pasta water to boil. There's a
trim list in [`02-prep-session.md`](02-prep-session.md) that gets Sunday closer to two
hours.

## Layout

| Path | What's in it |
|---|---|
| `index.html` | The site: the week, lunches, Sunday timeline, shopping, numbers |
| `recipes.html` | All 25 recipes — **generated, don't edit by hand** |
| `build.py` | **The source of truth for every recipe** |
| `style.css`, `app.js` | Shared styles and progressive enhancements |
| [`recipes/`](recipes/) | Markdown copy of each recipe — **generated** |
| [`01-the-plan.md`](01-the-plan.md) | Weekly rotation, portioning, ramp-up |
| [`02-prep-session.md`](02-prep-session.md) | Minute-by-minute weekend timeline, by person |
| [`04-shopping-list.md`](04-shopping-list.md) | By store — Costco, Asian, Indian, regular |
| [`05-nutrition.md`](05-nutrition.md) | Protein targets, macros, supplements |

## Changing a recipe

Recipes live in **one place**: the `RECIPES` list in `build.py`. Edit there, then:

```sh
python3 build.py              # rebuilds recipes.html, recipes/*.md, icons
python3 build.py --paprika    # also rebuilds the Paprika archive
```

Everything else is generated from it, so there's nothing to keep in sync.

The `.paprikarecipes` archive is **gitignored** — build it locally when you want to import
into Paprika (double-click on Mac, or AirDrop to your phone). It imports all 25 at once,
filed under `Meal Prep: Anchors / Components / Sauces / Dinners / Lunches / Breakfast /
Projects / Reference`.

## Three ideas doing most of the work

**Run four heat sources at once.** Instant Pot, oven, stovetop and air fryer are all
unattended once loaded. Most meal prep is slow because people use one at a time.

**Split into a wet track and a dry track.** One person owns the Instant Pot, stovetop and
food processor. The other owns knife work, sheet pans, air fryer and containers. Neither
waits on the other.

**Boost portions at the plate, not in the pot.** There's a large bodyweight difference
between you two, so cooking two versions of everything would double the work. Every meal
is the same; the higher-protein portion gets a scoop of edamame or extra tofu at serving.

## Rules that keep it honest

- **Same dish twice a week, maximum**, never on consecutive days.
- **Impossible / TVP once a week, maximum** — Friday treat night, not a staple.
- **Eggs in two dishes only**, both written so you can drop them.
- **No dairy.** Soy milk, soy yogurt, tahini and cashew cream cover everything it did.
- **The anchor rotates.** Same slot, same technique, different dish each week.

## Getting started

1. Read [`01-the-plan.md`](01-the-plan.md) for the shape of the week.
2. Shop from the list. The first trip is the big one — spices and dry goods last months.
3. Run the Week A timeline in [`02-prep-session.md`](02-prep-session.md) with a timer.
4. Do that twice before adding anything new. **Week 3** is the seitan session.

Your first session will run long — you're reading while cooking. The second one lands
close to the times listed.

#!/usr/bin/env python3
"""Single source of truth for the recipes.

Generates, from the RECIPES list below:
  recipes/*.md                        human-readable reference
  recipes/README.md                   index
  recipes.html                        the mobile site
  icons                               apple-touch-icon, favicon, manifest icon
  Sunday Kitchen Meal Prep.paprikarecipes   (only with --paprika; gitignored)

Run:  python3 build.py            # site + markdown + icons
      python3 build.py --paprika  # also rebuild the Paprika archive
"""
import gzip, hashlib, html, io, json, os, re, struct, sys, uuid, zlib, zipfile

CREATED = "2026-08-08 12:00:00"
SOURCE = "Sunday Kitchen meal prep plan"

ANCHOR, COMPONENT, SAUCE = "Anchors", "Components", "Sauces"
DINNER, LUNCH, BREAKFAST = "Dinners", "Lunches", "Breakfast"
PROJECT, REFERENCE = "Projects", "Reference"

GROUP_ORDER = [ANCHOR, COMPONENT, SAUCE, DINNER, LUNCH, BREAKFAST, PROJECT, REFERENCE]
GROUP_BLURB = {
    ANCHOR: "Cooked in double batches. Half this week, half flat-frozen for next.",
    COMPONENT: "The kit. Made on prep day, combined into dinners all week.",
    SAUCE: "The three bowl sauces, in the order that saves washing the processor bowl — plus a harissa you make once and keep for weeks.",
    DINNER: "Assembly, not cooking. Wall clock first, hands-on second.",
    LUNCH: "All assembled on the weekend. Zero weekday cost.",
    BREAKFAST: "",
    PROJECT: "",
    REFERENCE: "",
}

RECIPES = []


def add(slug, name, group, ing, steps, notes="", desc="", servings="", prep="",
        cook="", total="", cuisine=(), used_in=()):
    RECIPES.append(dict(
        slug=slug, name=name, group=group, cuisine=list(cuisine),
        ingredients=ing.strip("\n"),
        directions="\n".join(s.strip() for s in steps if s.strip()),
        notes=notes.strip("\n"), description=desc.strip(),
        servings=servings, prep_time=prep, cook_time=cook, total_time=total,
        used_in=list(used_in),
    ))


# ================================================================= ANCHORS

add("anchor-chana-masala", "Chana Masala", ANCHOR,
    """2 cups dried chickpeas, soaked overnight
2 large onions, finely diced
6 cloves garlic, minced
2 tbsp ginger, minced
1 can (28 oz) crushed tomatoes
2 tbsp tomato paste
2 tsp cumin seeds
2 tbsp ground coriander
1 tbsp ground cumin
2 tsp turmeric
1-2 tsp kashmiri chili powder
1 tbsp garam masala
2 tsp amchur, or juice of 1 lemon
2 tbsp oil
2 tsp salt
2 1/2 cups water
Cilantro, to finish""",
    ["Sauté mode. Oil, then cumin seeds until they sizzle and darken, about 30 seconds.",
     "Onions, a full 10 minutes, until genuinely golden. This is the step everyone rushes and it's where the depth comes from.",
     "Garlic and ginger, 1 minute. Then tomato paste and all the GROUND spices, 1 minute — blooming them in fat is what separates this from a spice-flavored stew.",
     "Crushed tomatoes, drained chickpeas, water, salt. Cancel sauté, seal, 18 min high pressure, then 10 minutes natural release. It takes about 12 minutes to come to pressure at this volume, so it's done at the one-hour mark, not the 38-minute mark.",
     "Mash a handful of chickpeas against the side of the pot to thicken the gravy.",
     "Stir in the garam masala and amchur OFF the heat — they're aromatics, not base notes."],
    """Four servings this week, four flat-frozen for next. Better on day three than day one.

Canned chickpeas work — 4 x 15 oz, drained, and drop the pressure time to 5 minutes.

TO PUSH THE PROTEIN HIGHER: add 1/2 cup red lentils with the water. They dissolve completely, thicken the gravy, and add about 18 g across the batch.

WITH GARDEN TOMATOES: use about 2 lb fresh, cut the added water to 1 1/2 cups, and cook the tomatoes down for 5-8 minutes during the sauté stage before sealing. A pressure cooker evaporates nothing, so fresh tomatoes would otherwise thin the gravy into soup.

Cool on a sheet pan before bagging. Freeze half, flat — flat bags stack, and thaw in an hour instead of a day.

ROTATION PARTNERS for this slot: rajma, dal tadka, sambar-style lentil & vegetable, aloo chana.""",
    "The Instant Pot anchor. Carries Monday's lunch and Thursday's dinner, and half the batch goes flat into the freezer.",
    "8", "15 min", "50 min", "65 min", ["South Asian"],
    ["lunch-mon-chana-bowl", "dinner-thu-chana-jeera-rice"])

add("anchor-lentil-walnut-ragu", "Lentil-Walnut Ragù", ANCHOR,
    """1 1/2 cups dried brown or green lentils
1 cup walnuts, toasted and coarsely chopped
1 large onion, finely diced
2 carrots, finely diced
2 celery stalks, finely diced
6 cloves garlic
1 can (28 oz) crushed tomatoes
3 tbsp tomato paste
3 cups water or vegetable broth
2 tbsp soy sauce
1 tbsp balsamic vinegar
2 tsp dried oregano
1 tsp dried thyme
1 tsp fennel seeds, crushed
Chili flakes, to taste
3 tbsp olive oil
Salt and pepper""",
    ["Toast the walnuts in a dry pan, 4 minutes, until they smell like walnuts. Chop coarse and set aside.",
     "Pulse the onion, carrot and celery in the food processor — a 90-second job instead of a ten-minute one, and nobody can tell.",
     "Olive oil, soffritto, 12 minutes until soft and sweet. Garlic, 1 minute.",
     "Tomato paste, 2 minutes, until it darkens to brick red.",
     "Crushed tomatoes, lentils, liquid, soy sauce, balsamic, herbs. Simmer uncovered 30-35 minutes, stirring occasionally, until the lentils are tender and it's thick.",
     "Walnuts in for the last 5 minutes. Salt aggressively at the end."],
    """THE FENNEL SEEDS ARE THE WHOLE TRICK. They're what make this read as sausage ragù rather than lentils in tomato sauce. Don't leave them out.

Four servings this week, four flat-frozen for next.

WITH GARDEN TOMATOES: use about 2 lb fresh and simmer 10-20 minutes longer. Judge by look — when a spoon dragged through the pan leaves a channel that doesn't immediately fill, it's ready.

NO BALSAMIC? It is one tablespoon in a pot holding two cans of tomatoes, there for acidity and a touch of sweetness. Swap in 1 tbsp red wine vinegar or apple cider vinegar plus a pinch of sugar, or 2 tsp white vinegar, or 1 tbsp lemon juice. Balsamic dressing works too, but it is roughly a third vinegar, so use 2-3 tbsp and add it at the END rather than with the tomatoes — dressings vary in sweetness and a 35-minute simmer concentrates sugar. Or leave it out and add a squeeze of lemon at the end if it tastes flat.

ROTATION PARTNERS for this slot: roasted red pepper & white bean, chickpea puttanesca, creamy cashew-tomato with lentils.""",
    "The stovetop anchor. Tuesday's pasta and Friday's lunch bowl, with half frozen flat for next week.",
    "8", "20 min", "40 min", "60 min", ["Italian"],
    ["dinner-tue-rigatoni-ragu", "lunch-fri-ragu-rice-bowl"])

# ============================================================== COMPONENTS

add("component-crispy-tofu", "Crispy Marinated Tofu", COMPONENT,
    """2 blocks (about 800 g) extra-firm tofu, frozen then thawed
3 tbsp soy sauce
1 tbsp rice vinegar
1 tbsp maple syrup
2 tsp sesame oil
3 cloves garlic, grated
1 tbsp ginger, grated
2 tbsp cornstarch""",
    ["AHEAD: put the tofu blocks in the freezer, still in their packages, midweek. Move them to the fridge the day before to thaw. Frozen-then-thawed tofu turns spongy and chewy, drinks marinade, and crisps far better — and you never have to press it again.",
     "Squeeze the thawed blocks hard over the sink. They release a startling amount of water. Cube.",
     "Toss in the marinade.",
     "Air fryer 400°F, 18 minutes, shaking at 9. Or oven at 425°F for 30 minutes."],
    """The cornstarch is what gives you the crust. Don't skip it.

REHEATING: 4-5 minutes in the air fryer, no preheat needed. This is the difference between crispy tofu and sad tofu, and it costs nothing.

Seasoned deliberately neutral-savory so it can go Chinese on Monday and Mediterranean on Thursday without arguing.

Roughly half goes to Monday's dinner. The rest is the week's booster protein — about 10 g per 100 g.""",
    "Built on the freeze-thaw trick, which eliminates pressing entirely.",
    "4", "8 min", "18 min", "26 min", (), ["dinner-mon-sticky-tofu"])

add("component-tofu-crumbles", "Three-Zone Tofu Crumbles", COMPONENT,
    """2 blocks (about 800 g) extra-firm tofu
SHARED BASE
3 tbsp soy sauce
2 tbsp chili oil or chili crisp
1 tbsp rice vinegar
2 tbsp cornstarch
2 tsp garlic powder
1 tsp onion powder
Black pepper
SICHUAN ZONE
1/2 tsp five-spice powder
1/2 tsp ground Sichuan pepper
Extra chili crisp
CUMIN-GARAM MASALA ZONE
1 tsp ground cumin
1 tsp ground coriander
1/2 tsp garam masala
1/2 tsp turmeric
1/2 tsp kashmiri chili powder
CHILI-LIME ZONE
1 tsp smoked paprika
1 tsp ground cumin
1/2 tsp chipotle powder
Zest of 1 lime""",
    ["Crumble the tofu BY HAND into pea-to-marble sized pieces. A knife gives you cubes; hands give you texture. No pressing, no freezing needed.",
     "Toss everything in the shared base.",
     "Spread on one parchment-lined sheet pan in three separate sections.",
     "Season each section differently — Sichuan, cumin-garam masala, chili-lime. Same pan, same bake, three ingredients out.",
     "425°F, 25-30 minutes, stirring at 15. They should be chewy with crisp edges, not dry.",
     "Squeeze lime over the chili-lime section AFTER baking."],
    """THE CORNSTARCH IS WHAT MAKES THEM CRISP. It's not optional.

Adapted from Yeung Man Cooking's baked tofu crumbles.

WHERE EACH ZONE GOES, about 2 cups each:
Sichuan — Wednesday lunch bowls x2, Wednesday dinner chowmein.
Cumin-garam masala — Thursday dinner sabzi x2, scattered on Monday's lunch.
Chili-lime — Friday dinner tacos x2.

Store them separately from wet food, and keep the three zones apart — they go soft against rice, and the whole point is that they're three different things.

Whatever's left over is the snack. That isn't a consolation prize.""",
    "One sheet pan, three spice profiles, three ingredients out.",
    "6", "15 min", "30 min", "45 min", (),
    ["lunch-wed-sichuan-crumble-bowl", "dinner-wed-chowmein",
     "dinner-thu-chana-jeera-rice", "dinner-fri-tacos"])

add("component-falafel", "Falafel, Formed and Frozen Raw", COMPONENT,
    """2 cups dried chickpeas, soaked 18-24 hours (NEVER cooked, never canned)
1 onion, roughly chopped
5 cloves garlic
1 packed cup parsley
1 packed cup cilantro
2 tsp ground cumin
1 tsp ground coriander
1/2 tsp cayenne
1 1/2 tsp salt
Black pepper
1 tsp baking powder
2-3 tbsp flour, only if it won't hold""",
    ["Soak a bowl of dried chickpeas overnight — separate from any you're cooking for other dishes. These ones do NOT get cooked. Drain and pat them properly dry.",
     "Pulse everything except the baking powder in the food processor to a coarse, couscous-like texture — NOT a purée. Squeeze a handful; it should hold. Over-processing is the second most common way to ruin falafel.",
     "Rest 30 minutes in the fridge.",
     "Stir in the baking powder LAST, just before forming — it's what makes them fluffy inside.",
     "Form into PATTIES, not balls. Patties get more contact with the air fryer basket and cook far more evenly.",
     "Freeze on a tray until solid, then bag. Keeps three months.",
     "TO COOK FROM FROZEN: air fryer at 375°F, 15 minutes, sprayed with oil, flipping halfway. No thawing."],
    """THE RULE THAT MATTERS: dried soaked chickpeas, never cooked ones. Canned or cooked chickpeas make a wet paste that falls apart in the pan and tastes mushy. There is no way around this one.

Freeze it in the right state — formed raw, cooked fresh. Cooked falafel reheated on day four is dry and sad. Raw frozen falafel air-fried on the night is excellent.

Air-fried is good, not great. Deep-fried is genuinely better — crisper shell, fluffier interior. The raw frozen patties fry beautifully straight from the freezer if you ever want to do it properly.

PROTEIN: about 19 g per serving, noticeably less dense than tofu or seitan. Add a full cup of edamame or a scoop of hummus alongside for a bigger portion.""",
    "15 minutes on prep day, zero on the night.",
    "4", "15 min", "15 min", "30 min", ["Middle Eastern"],
    ["dinner-fri-falafel-night"])

add("component-basmati-rice", "Basmati Rice", COMPONENT,
    """5 cups basmati rice (Instant Pot batch)
5 cups water
3 cups basmati rice (stovetop batch)
4 1/2 cups water
Pinch of salt""",
    ["Rinse the rice until the water runs clear. That's what keeps the grains separate.",
     "INSTANT POT BATCH: 5 cups rice, 5 cups water, a pinch of salt. Check your pot's half-full line first — 5 cups dry is about the limit on a 6-quart.",
     "6 minutes high pressure.",
     "FULL 10 minute natural release — cutting it short gives you wet rice.",
     "Fluff and spread on a sheet pan to cool fast.",
     "STOVETOP BATCH: one batch is not enough. 3 cups rinsed rice, 4 1/2 cups water, boil then lowest heat, lid on, 15 minutes, rest 10. Run this on the stovetop once the ragu is off it."],
    """Both batches together yield about 19 cups cooked, which is what the week actually needs: roughly 11 cups across the ten lunch containers, about 4 cups held back for Monday and Thursday dinners, and 4 cups frozen flat.

STORAGE: half to the fridge, half frozen flat in portions. Frozen rice microwaves better than four-day-old fridge rice, and it skips the food-safety question entirely — cooked rice wants to get cold quickly and be eaten within four days.
Reheat: 3 minutes from frozen, 90 seconds from the fridge.

JEERA RICE VARIATION: hot oil, 1 tsp cumin seeds until they pop, then cold rice tossed through with salt, 4 minutes.

The Instant Pot does the chana first and the rice second — don't try to run both at once, the pressure times aren't compatible.""",
    "About 19 cups across two batches — the week's grain.",
    "19 cups", "5 min", "25 min", "30 min")

add("component-roasted-vegetables", "Roasted Vegetables, Two Trays", COMPONENT,
    """HARISSA TRAY
1 head cauliflower, or broccoli
1 red pepper
1 red onion
1 zucchini
1 can chickpeas, drained and patted dry
2 tbsp harissa
2 tbsp olive oil
Salt
CHILI-CUMIN TRAY
2 sweet potatoes
1 red onion
1 bell or poblano pepper
1 cup corn
2 tsp ground cumin
2 tsp chili powder
1 tsp smoked paprika
Oil
Salt""",
    ["Cut everything roughly the same size. This matters more than what you cut.",
     "Toss the harissa tray with harissa, olive oil and salt. Jarred is fine; the five-minute Pantry Harissa in the sauces section is better and cheaper. The chickpeas roast crisp and become the protein in both Mediterranean bowls.",
     "Toss the chili-cumin tray with cumin, chili powder, smoked paprika, oil and salt.",
     "Both trays at 425°F for 30 minutes."],
    """Budget 20 minutes of chopping for the pair — it's the longest single job in the prep session.

SHORTCUT: a bag of pre-cut vegetables for one tray saves about 10 minutes.

On a freezer week, pick different vegetables and a different spice profile from the week before. It's the cheapest variety in the whole system.""",
    "Two trays, two spice profiles. The backbone of hands-off prep.",
    "8", "20 min", "30 min", "50 min", (),
    ["dinner-mon-sticky-tofu", "dinner-thu-chana-jeera-rice", "lunch-mediterranean-bowl"])

add("component-stir-fry-pack", "Wednesday Stir-Fry Pack", COMPONENT,
    """1/2 medium cabbage, shredded
2 carrots, shredded
1 capsicum / bell pepper, sliced
1 onion, sliced""",
    ["Shred everything into one bag. That's the whole recipe."],
    """The highest-value fifteen minutes in the prep session. Chopping these fresh on a Wednesday is what turns a 15-minute chowmein into a 28-minute one. Doing it on prep day moves that work to a day when you actually have the time.

NEVER CUT THIS from the prep session. Along with the anchors and the crumbles, it's one of the three things the week depends on.

SHORTCUT WORTH TAKING: a bag of pre-shredded coleslaw mix is the same cabbage and carrot, costs about a dollar, and saves twelve of those fifteen minutes. Add a sliced onion and capsicum to it.""",
    "Fifteen minutes on prep day that buys ten back on a Wednesday night.",
    "2", "15 min", "", "15 min", (), ["dinner-wed-chowmein"])

add("component-pickled-onions", "Quick-Pickled Onions", COMPONENT,
    """1 red onion, sliced thin
1/2 cup vinegar, white or apple cider
1/2 cup hot water
1 tbsp sugar
1 1/2 tsp salt""",
    ["Slice the onion as thin as you can be bothered to — thinner onions pickle faster and taste less raw.",
     "Combine everything in a jar.",
     "Ready in 30 minutes."],
    "Keeps three weeks, and makes leftovers taste deliberate.",
    "Five minutes of work that makes everything else taste deliberate.",
    "1 jar", "5 min", "", "5 min", (),
    ["lunch-mediterranean-bowl", "dinner-fri-tacos", "dinner-fri-falafel-night"])

# ================================================================== SAUCES

add("sauce-tahini-lemon", "Tahini-Lemon Sauce", SAUCE,
    """1/2 cup tahini
1/4 cup lemon juice
2 cloves garlic
1/2 tsp ground cumin
1/2 tsp salt
4-6 tbsp cold water""",
    ["Blitz everything in the food processor, adding the water last and slowly.",
     "IT WILL SEIZE INTO CEMENT BEFORE IT LOOSENS. This alarms everyone the first time. Keep adding water. Keep going. It comes back."],
    "Make this FIRST in the sauce sequence — tahini, then peanut-lime, then gochujang-sesame — and you never have to wash the food processor bowl between them.",
    "", "1 jar", "5 min", "", "5 min", (),
    ["lunch-mediterranean-bowl", "dinner-fri-falafel-night"])

add("sauce-peanut-lime", "Peanut-Lime Sauce", SAUCE,
    """1/2 cup peanut butter
3 tbsp soy sauce
2 tbsp lime juice
2 tbsp maple syrup
1 clove garlic
1 tbsp ginger
1-2 tsp chili crisp
4-6 tbsp water""",
    ["Blitz, thinning with water to a pourable consistency."],
    """Second in the sauce sequence, straight after the tahini-lemon — no washing needed between them.

For grain bowls, satay tempeh, and anything that wants a Southeast Asian turn.""",
    "", "1 jar", "5 min", "", "5 min")

add("sauce-gochujang-sesame", "Gochujang-Sesame Sauce", SAUCE,
    """3 tbsp gochujang
2 tbsp rice vinegar
2 tbsp toasted sesame oil
1 tbsp maple syrup
1 tbsp soy sauce
1 tbsp sesame seeds
1 clove garlic, grated""",
    ["Whisk together in the jar you'll store it in. That's it."],
    "This one never touches the food processor, which is why it comes last in the sequence.",
    "", "1 jar", "3 min", "", "3 min", (), ["lunch-wed-sichuan-crumble-bowl"])

add("sauce-harissa", "Pantry Harissa", SAUCE,
    """3 tbsp kashmiri chili powder (or 2 tbsp smoked paprika + 1 tsp cayenne)
2 tbsp tomato paste
5 cloves garlic, grated
1 tsp ground cumin
1 tsp ground coriander
1 tsp caraway seeds, toasted and ground (optional, but it is the signature note)
1 tbsp lemon juice
1/2 tsp salt
5 tbsp olive oil""",
    ["If you have caraway seeds, toast them in a dry pan for 30 seconds until fragrant, then grind. This is the flavour that makes harissa taste like harissa rather than a generic chili paste.",
     "Stir everything together into a thick, spoonable paste, adding the olive oil last and a little at a time. It should hold its shape on a spoon, like tomato paste, not pour.",
     "Taste for salt and heat. Kashmiri chili is mild and mostly there for colour, so add cayenne if you want it hotter.",
     "Store in a jar with a thin film of olive oil on top. Keeps about 3 weeks in the fridge."],
    """Harissa is a Tunisian chili paste: dried red chilies, garlic, olive oil, and a spice trio of caraway, coriander and cumin. This is the five-minute pantry version, built from things this plan already has you buying.

THE PROPER VERSION, if you want it: soak 10 dried red chilies (kashmiri, guajillo or New Mexico) in boiling water for 20-30 minutes with the stems and most seeds removed, then blend with 5 cloves garlic, 1 tsp each toasted caraway, cumin and coriander, 1 tsp salt, 1 tbsp lemon juice and 4-5 tbsp olive oil. Better texture and a rounder flavour, 30 minutes instead of 5.

CARAWAY IS THE ONE TO CHASE. It is not interchangeable with cumin despite the similar look. Without it you get a very good chili-garlic paste that is not quite harissa.

IF YOU SKIP HARISSA ENTIRELY: season the roasting tray with smoked paprika, cumin, garlic, olive oil and lemon instead. It stops being a harissa tray, but it roasts just as well and still works under tahini in the Mediterranean bowls.

You need 2 tbsp per roasting tray, so one batch covers a month.""",
    "The five-minute pantry version, from spices this plan already buys. One batch covers a month.",
    "About 1/2 cup", "5 min", "", "5 min", ["Middle Eastern"],
    ["component-roasted-vegetables"])

# ================================================================= DINNERS

add("dinner-mon-sticky-tofu", "Monday — Sticky Tofu, Rice, Roasted Veg", DINNER,
    """Crispy marinated tofu, from the prep session
Cooked rice
Chili-cumin roasted vegetables
3 tbsp soy sauce
2 tbsp maple syrup
1 tbsp rice vinegar
2 cloves garlic, grated
1 tsp ginger, grated
1/2 tsp chili flakes
1 tsp cornstarch slurried in 2 tbsp water
Sesame seeds
Scallions""",
    ["Crispy tofu into the air fryer, 400°F for 5 minutes. No preheat needed for a reheat, and this is the difference between crispy tofu and sad tofu.",
     "Rice into the microwave — 3 minutes from frozen, 90 seconds from the fridge.",
     "The glaze, in a pan: soy, maple, rice vinegar, garlic, ginger, chili flakes, cornstarch slurry. Bubble 2 minutes until glossy. Warm the chili-cumin veg in the same pan alongside.",
     "TOSS THE TOFU THROUGH THE GLAZE OFF THE HEAT. Do it over the flame and the crust goes soft.",
     "Sesame seeds, scallions."],
    """15 minutes wall clock, 10 minutes hands-on.

ROTATION: from week 3 this slot alternates with char siu seitan — sear the slices hard in a dry pan, then the same glaze off the heat. From week 5, optionally satay tempeh with the peanut-lime sauce. Steam the tempeh 10 minutes first — that removes the bitterness, and skipping it is why most people think they don't like tempeh.""",
    "", "2", "5 min", "10 min", "15 min", ["Chinese"])

add("dinner-tue-rigatoni-ragu", "Tuesday — Rigatoni + Ragù", DINNER,
    """Lentil-walnut ragù, from the prep session
Rigatoni
Toasted breadcrumbs or nutritional yeast""",
    ["PUT THE WATER ON BEFORE YOU DO ANYTHING ELSE. Before you change, before you sit down. An electric kettle takes this to 12 minutes: boil the kettle, pour into the pot, back to a rolling boil in about a minute.",
     "Rigatoni, 11 minutes. Warm the ragù while it cooks.",
     "Save half a cup of pasta water. Toss everything together in the pan with a splash — that's what makes sauce cling instead of sit.",
     "Toasted breadcrumbs or nutritional yeast on top."],
    """18 minutes wall clock, 6 minutes hands-on. Twelve of those eighteen minutes are water and pasta doing their own thing.

ROTATION: the anchor in this slot changes every cycle — lentil-walnut ragù, roasted red pepper & white bean, chickpea puttanesca, creamy cashew-tomato with lentils.""",
    "", "2", "3 min", "15 min", "18 min", ["Italian"])

add("dinner-wed-chowmein", "Wednesday — Veggie Chowmein", DINNER,
    """Chowmein or lo mein noodles, for 2
Wednesday stir-fry pack (shredded cabbage, carrot, capsicum, onion)
2 eggs, optional
1 cup shelled edamame
1 cup Sichuan tofu crumbles, optional or instead of the eggs
2 cloves garlic
Oil
3 tbsp soy sauce
1 tbsp dark soy sauce
1 tbsp rice vinegar
1 tsp sugar
White pepper
Chili
Scallions""",
    ["Kettle water into a pot. Noodles 3 minutes, drain, toss with a little oil so they don't weld together.",
     "Biggest pan you own, as hot as it goes. Oil, garlic, then THE WHOLE STIR-FRY PACK — 5 minutes, hard heat, keep it moving. Crowding steams it; you want char.",
     "Push the veg aside and scramble the eggs in the space. Or skip them and add a cup of Sichuan crumbles — the dish doesn't miss them.",
     "Noodles and edamame in, then the sauce. Toss hard, 2 minutes.",
     "Scallions."],
    """18 minutes wall clock, 14 hands-on. The longest dinner of the week, because a stir-fry has to be watched the whole time.

THIS ASSUMES THE STIR-FRY PACK EXISTS. Chopping the vegetables fresh puts this at 28 minutes.

TO GET IT TO 12 MINUTES: cook the noodles on prep day, two minutes under, tossed in oil — that's how restaurants hold lo mein. They're slightly softer by Wednesday, but it removes the boil from the weeknight entirely.""",
    "", "2", "4 min", "14 min", "18 min", ["Nepali", "Indo-Chinese"])

add("dinner-thu-chana-jeera-rice", "Thursday — Chana, Jeera Rice, Crumble Sabzi", DINNER,
    """Chana masala, from the prep session
Cooked rice
1 tsp cumin seeds
Oil
Salt
Cumin-garam masala tofu crumbles
Roasted vegetables
Lemon
Cilantro
Soy yogurt, cucumber and cumin, for optional raita""",
    ["Two pans at once.",
     "PAN 1, jeera rice: hot oil, cumin seeds until they pop, then cold rice tossed through with salt, 4 minutes.",
     "PAN 2, sabzi: cumin-garam masala crumbles warmed with roasted veg, 4 minutes. Lemon, cilantro.",
     "Chana in the microwave, 4 minutes.",
     "Optional raita: soy yogurt, grated cucumber, cumin, salt."],
    """15 minutes wall clock, 12 hands-on.

WITH GARDEN TOMATOES: kachumber is the right foil for a heavy curry — diced tomato, cucumber, red onion, lemon, cumin, cilantro. Five minutes.

ROTATION: the anchor in this slot changes every cycle — chana masala, rajma, dal tadka, sambar-style lentil & vegetable, aloo chana.""",
    "", "2", "3 min", "12 min", "15 min", ["South Asian"])

add("dinner-fri-tacos", "Friday — Tacos with Chili-Lime Crumbles", DINNER,
    """Chili-lime tofu crumbles
1 can black beans
1 tsp ground cumin
2 cloves garlic
Tortillas
1/4 cabbage, shredded
2 limes
Quick-pickled onions
1 avocado
Salsa, or fresh pico de gallo
Cilantro
Salt""",
    ["Black beans with cumin and garlic, 5 minutes.",
     "Chili-lime crumbles in the same pan after, 4 minutes with a squeeze of lime.",
     "Slaw — shredded cabbage, lime, salt. 3 minutes.",
     "Tortillas blistered directly over the flame, 4 minutes.",
     "Assemble with pickled onions, avocado, salsa, cilantro."],
    """18 minutes wall clock, 15 hands-on. Each component is simple, but there are five of them.

TREAT NIGHT: if Impossible grounds or TVP are going to appear in the week, they appear here, and only here. Once a week, maximum.

WITH GARDEN TOMATOES: fresh pico de gallo instead of jarred salsa — tomato, onion, jalapeño, lime, cilantro, salt. Five minutes, and it's not close.

Alternates with falafel night.""",
    "", "2", "5 min", "15 min", "18 min", ["Mexican"])

add("dinner-fri-falafel-night", "Friday, alternate — Falafel Night", DINNER,
    """Falafel patties, frozen raw
Pita or flatbread
1/4 cabbage, shredded
1 lemon
Olive oil
Tahini-lemon sauce
Quick-pickled onions
Cucumber
Tomato
Parsley
Salt""",
    ["Falafel patties from the freezer into the air fryer. 375°F, 15 minutes, sprayed with oil, flipped halfway. Walk away.",
     "Warm the pita — over the flame, or in the air fryer for the last 2 minutes.",
     "Slaw: shredded cabbage, lemon, salt, olive oil. 3 minutes.",
     "Assemble with tahini-lemon, pickled onions, cucumber, tomato, parsley."],
    """18 minutes wall clock, 8 hands-on — most of it is the air fryer working alone.

The same assembly as taco night with different seasonings, which is exactly why it slots here: warm flatbread, a crisp protein, pickled onions, a creamy sauce, a slaw. Three of those five are already in the kit. Pita instead of tortillas is the only new item.

OPTIONAL HUMMUS takes four minutes in the food processor you already have out on prep day — chickpeas, tahini, lemon, garlic, ice water. Worth it on falafel weeks for the extra protein, but tahini alone does the job.""",
    "", "2", "3 min", "15 min", "18 min", ["Middle Eastern"])

# ================================================================= LUNCHES

add("lunch-mon-chana-bowl", "Monday Lunch — Chana Masala Bowl", LUNCH,
    """Chana masala
Cooked rice
Shelled edamame
Cilantro
Lemon wedge, packed separately""",
    ["Layer chana masala, rice and edamame in the container. Cilantro on top.",
     "The edamame goes in STRAIGHT FROM FROZEN — it thaws in the fridge overnight and reheats with everything else.",
     "Scatter cumin-garam masala crumbles on top if there are spare.",
     "Lemon wedge in a separate corner. Assembled on prep day."],
    "PORTIONS: Person A — 1 1/2 cups chana, 1 cup rice, 1/2 cup edamame. Person B — 2 cups chana, 1 1/2 cups rice, 1 cup edamame.",
    "", "1", "5 min", "", "5 min")

add("lunch-mediterranean-bowl", "Tuesday & Thursday Lunch — Mediterranean Bowl", LUNCH,
    """Cooked rice
Harissa roasted vegetables
Roasted chickpeas, from the harissa tray
Cucumber
Cherry tomato
Quick-pickled onions
Parsley
Tahini-lemon sauce, PACKED SEPARATELY""",
    ["Layer rice, harissa veg, roasted chickpeas, cucumber, cherry tomato, pickled onion and parsley.",
     "TAHINI-LEMON GOES IN ITS OWN CONTAINER. Dressing it on prep day turns the grains to paste by Tuesday. Dress it at your desk.",
     "Tuesday's is packed on prep day; Thursday's is packed Wednesday night, so nothing you eat is five days old."],
    """This is the one bowl with no tofu in it, and that's deliberate — the protein is the roasted chickpeas off the harissa tray plus the tahini, around 33 g. It keeps chickpeas and crumbles from competing for the same slot. Add an edamame scoop if you're short.

IT'S GENUINELY GOOD COLD. Don't feel obliged to microwave it.

From week 3, sliced shawarma seitan turns this into a shawarma bowl and takes it to about 50 g of protein. The tahini and pickled onions are already there.""",
    "", "1", "5 min", "", "5 min", ["Middle Eastern"])

add("lunch-wed-sichuan-crumble-bowl", "Wednesday Lunch — Sichuan Crumble Rice Bowl", LUNCH,
    """Cooked rice
Roasted vegetables
Shelled edamame
Cucumber
Sichuan tofu crumbles, PACKED SEPARATELY
Gochujang-sesame sauce, PACKED SEPARATELY""",
    ["Rice, roasted veg, edamame and cucumber in the main container.",
     "Sichuan crumbles and gochujang-sesame in two small separate containers.",
     "At work: reheat the main container, THEN scatter the crumbles on and add the sauce."],
    "Crumbles packed against wet rice lose everything that makes them worth making. The two extra containers are worth the thirty seconds.",
    "", "1", "5 min", "", "5 min")

add("lunch-fri-ragu-rice-bowl", "Friday Lunch — Ragù Rice Bowl", LUNCH,
    """Lentil-walnut ragù
Cooked rice
Roasted vegetables
Nutritional yeast, packed separately""",
    ["Ragù over rice, roasted veg alongside.",
     "Nutritional yeast in a separate corner.",
     "Packed Wednesday night rather than prep day, so it's two days old rather than five."],
    "OVER RICE, NOT PASTA. Reheated pasta in a container goes gluey and sad by Friday. Rice takes exactly the same sauce and holds up for four days.",
    "", "1", "5 min", "", "5 min")

# =============================================================== BREAKFAST

add("breakfast-shake", "Post-Workout Breakfast Shake", BREAKFAST,
    """1 scoop protein powder
5 g creatine monohydrate
1/2 cup rolled oats (3/4 cup for a larger portion)
1 frozen banana, peeled before freezing
1 tbsp ground flax
1 1/2 cups soy milk, fortified
2 tbsp peanut butter, for a larger portion""",
    ["Blend everything.",
     "About 44 g protein and 570 kcal for the smaller portion; 55 g and 815 kcal with the extra oats and peanut butter."],
    """SOY MILK, NOT WATER. It adds 7-8 g of protein per cup and turns a supplement into breakfast. Check that yours is fortified with calcium, B12 and D.

PEEL THE BANANAS BEFORE FREEZING THEM. Frozen banana peel is a genuinely miserable thing to deal with at 7am.

CREATINE TIMING IS IRRELEVANT — 3-5 g daily, no loading phase needed. It's in the shake because that's the easiest place to remember it, not because morning is optimal. Plant-based eaters start with lower muscle creatine stores and tend to respond better than omnivores.

The oats are the lever for calories. Move them up or down before you touch the protein.""",
    "", "1", "2 min", "", "2 min")

# ================================================================ PROJECTS

add("project-seitan", "Seitan, Three Flavors", PROJECT,
    """BASE DOUGH
2 cups vital wheat gluten
1/4 cup nutritional yeast
1 tsp garlic powder
1 tsp onion powder
1 1/2 cups vegetable broth
2 tbsp soy sauce
1 tbsp oil
1 tbsp tomato paste or miso
SHAWARMA
Cumin, coriander, smoked paprika, cinnamon, garlic
CHAR SIU
Five-spice, hoisin, soy sauce, a little maple
CHORIZO
Smoked paprika, chipotle, oregano, garlic, red wine vinegar""",
    ["Whisk the dry ingredients, whisk the wet, then combine.",
     "KNEAD 3-5 MINUTES — long enough to develop strands, not so long it turns rubbery. Rest 20 minutes.",
     "Divide into three. Knead a different flavoring into each.",
     "Wrap each tightly in foil, twisting the ends like a cracker.",
     "STEAM 60-75 MINUTES. Steaming beats boiling — boiled seitan waterlogs.",
     "COOL COMPLETELY BEFORE SLICING. The texture sets as it cools; slice it warm and it's spongy. Overnight in the fridge is better.",
     "Slice thin, portion, freeze flat.",
     "Reheats best seared hard in a dry-ish pan — it should get brown edges."],
    """One two-hour session, about 3 kg. Vital wheat gluten is cheap at the Indian grocery and roughly 75% protein by weight.

Don't attempt this until the core weekly system feels automatic — week 3 at the earliest.

WHERE EACH FLAVOR GOES:
Char siu — Monday, alternating with sticky tofu. Same glaze, same technique.
Chorizo — Friday tacos, alternating with the chili-lime crumbles. Crumble it into the pan rather than slicing.
Shawarma — the Tuesday and Thursday Mediterranean lunch bowls. Takes them from about 33 g protein to about 50 g.

No new shopping, no new sauces, no new techniques. And a seitan week is LESS prep-day work — if seitan takes the Monday slot, you skip marinating and air-frying the tofu.""",
    "", "12", "30 min", "75 min", "2 hrs")

# =============================================================== REFERENCE

add("reference-garden-tomatoes", "Using Garden Tomatoes", REFERENCE,
    """1 can (28 oz) crushed tomatoes = about 2 lb / 900 g fresh
1 can (14 oz) crushed tomatoes = about 1 lb / 450 g fresh
Tomato paste = KEEP IT, don't substitute""",
    ["CONVERSION: canned tomatoes are already cooked down; fresh ones are about 94% water. That's why you need more by weight, and why the tomato paste matters MORE, not less — it carries the depth and body the fresh fruit can't.",
     "RAGÙ, stovetop and uncovered — easy. Swap them in and simmer 10-20 minutes longer. The water evaporates on its own. Judge by look: when a spoon dragged through the pan leaves a channel that doesn't immediately fill, it's ready.",
     "CHANA MASALA, Instant Pot — needs two changes, because a sealed pressure cooker evaporates nothing and fresh tomatoes would thin the gravy into soup. First, cut the added water from 2 1/2 cups to 1 1/2 cups. Second, cook the tomatoes down during the sauté stage: after the spices bloom, let them break down and darken for 5-8 minutes before the chickpeas go in and you seal.",
     "WHICH TOMATOES: paste types are best — Roma, San Marzano, Amish Paste, any plum shape. Less water, more flesh. Beefsteaks work but need more reduction. Cherry tomatoes are excellent and sweet.",
     "SKINS, fastest first: blitz them whole in the food processor, skins and all — it's already out, and the skins pulverize and disappear. Or grate them on a box grater, cut side down, holding onto the skin, so the flesh goes through and the skin stays in your hand — about 5 minutes for 2 lb. Or blanch and peel: score an X, 30 seconds in boiling water, ice bath, skins slip off. Best result, slowest.",
     "Don't leave skins whole in a long simmer — they curl into little rolls that are unpleasant to find."],
    """TASTE BEFORE YOU FOLLOW THE RECIPE. Canned tomatoes are consistent and fairly acidic. Garden tomatoes vary a lot, and are often sweeter and less acidic, especially late in the season. You'll likely need less sugar (or none) in the ragù, and MORE acid at the end — a squeeze of lemon in the chana, an extra splash of balsamic in the ragù — to stop it tasting flat. This is the one place in the plan where the recipe can't tell you the answer.

WHEN YOU HAVE TOO MANY: freeze them whole and raw. Wash, dry, bag, freeze. That's the entire method. The skins slip off under warm water as they thaw, and frozen tomatoes are only good for cooking anyway — which is all you need them for here. Zero prep.

OR ROAST A TRAY: halve them, olive oil, garlic, salt, 400°F for 45 minutes until collapsed and a little caramelized. Freeze flat in 2-cup portions. These are genuinely BETTER than canned in the ragù. The oven is free late in the prep session, so a glut week costs almost nothing.

OTHER PLACES THEY EARN THEIR SPOT: fresh pico de gallo instead of jarred salsa on Friday; kachumber alongside Thursday's chana — diced tomato, cucumber, red onion, lemon, cumin, cilantro; and the Mediterranean bowls already use them raw.""",
    "Conversions, skins, and what to do with a glut. Not a recipe — a cheat sheet.",
    "", "", "", "")


# ============================================================== RENDERING

BY_SLUG = {r["slug"]: r for r in RECIPES}
ING_HEAD = re.compile(r"^[A-Z0-9][A-Z0-9 \-/&']*$")
LEAD_CAPS = re.compile(r"^([A-Z][A-Z0-9 ,\-/&']{3,}(?:, [a-z][^:.]*)?)(:| —)")


def meta_bits(r):
    out = []
    if r["servings"]:
        out.append(f"{r['servings']} servings" if r["servings"].isdigit() else r["servings"])
    if r["total_time"]:
        out.append(r["total_time"])
    return out


def emphasise(text):
    """Bold a leading ALL-CAPS lead-in, then escape the rest."""
    m = LEAD_CAPS.match(text)
    if m:
        return (f"<strong>{html.escape(m.group(1))}</strong>"
                f"{html.escape(m.group(2))}{html.escape(text[m.end():])}")
    return html.escape(text)


def recipe_html(r):
    parts = [f'<article class="recipe" id="{r["slug"]}">']
    parts.append('<details>')
    meta = " · ".join(meta_bits(r))
    parts.append(
        f'<summary><span class="r-name">{html.escape(r["name"])}</span>'
        f'{f"<span class=\"r-meta\">{html.escape(meta)}</span>" if meta else ""}</summary>')
    parts.append('<div class="r-body">')

    if r["description"]:
        parts.append(f'<p class="r-desc">{html.escape(r["description"])}</p>')

    parts.append('<h3 class="r-h">Ingredients</h3><ul class="ing">')
    for line in r["ingredients"].splitlines():
        line = line.strip()
        if not line:
            continue
        if ING_HEAD.match(line) and len(line.split()) <= 5:
            parts.append(f'<li class="ing-head">{html.escape(line)}</li>')
        else:
            parts.append(f'<li><label><input type="checkbox">'
                         f'<span>{html.escape(line)}</span></label></li>')
    parts.append('</ul>')

    parts.append('<h3 class="r-h">Method</h3><ol class="steps">')
    for s in r["directions"].splitlines():
        if s.strip():
            parts.append(f'<li>{emphasise(s.strip())}</li>')
    parts.append('</ol>')

    if r["notes"]:
        parts.append('<h3 class="r-h">Notes</h3><div class="notes">')
        for para in r["notes"].split("\n\n"):
            if para.strip():
                parts.append(f'<p>{emphasise(para.strip())}</p>')
        parts.append('</div>')

    if r["used_in"]:
        links = " · ".join(
            f'<a href="#{s}">{html.escape(BY_SLUG[s]["name"])}</a>'
            for s in r["used_in"] if s in BY_SLUG)
        parts.append(f'<p class="used-in"><span>Used in</span> {links}</p>')

    parts.append('</div></details></article>')
    return "\n".join(parts)


def write_recipes_html():
    groups = {g: [r for r in RECIPES if r["group"] == g] for g in GROUP_ORDER}
    nav = "".join(
        f'<li><a href="#g-{g.lower()}">{g}</a></li>'
        for g in GROUP_ORDER if groups[g])

    body = []
    for g in GROUP_ORDER:
        if not groups[g]:
            continue
        body.append(f'<section class="group" id="g-{g.lower()}">')
        body.append(f'<div class="group-head"><h2>{g}</h2>')
        if GROUP_BLURB[g]:
            body.append(f'<p>{html.escape(GROUP_BLURB[g])}</p>')
        body.append('</div>')
        body += [recipe_html(r) for r in groups[g]]
        body.append('</section>')

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Recipes · Sunday Kitchen</title>
<meta name="description" content="Every recipe in the Sunday Kitchen meal prep plan.">
<meta name="theme-color" content="#F3F5F0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121510" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Kitchen">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-32.png" sizes="32x32">
<link rel="manifest" href="manifest.webmanifest">
<link rel="stylesheet" href="style.css">
</head>
<body>
<nav class="topbar">
  <a class="back" href="./">&larr; Plan</a>
  <ol class="jump">{nav}</ol>
  <button id="wake" class="wake" type="button" aria-pressed="false"
          title="Keep the screen awake while cooking">Screen&nbsp;on</button>
</nav>
<main class="wrap">
  <header class="page-head">
    <h1>Recipes</h1>
    <p>{len(RECIPES)} recipes. Tap any ingredient to check it off — it resets when you reload.</p>
    <div class="controls">
      <button type="button" data-all="open">Expand all</button>
      <button type="button" data-all="close">Collapse all</button>
    </div>
  </header>
  {"".join(body)}
</main>
<footer class="foot">
  <p><a href="./">Back to the plan</a></p>
</footer>
<script src="app.js"></script>
</body>
</html>
"""
    open("recipes.html", "w").write(doc)
    return len(RECIPES)


def write_markdown():
    os.makedirs("recipes", exist_ok=True)
    for r in RECIPES:
        meta = " · ".join(meta_bits(r))
        L = [f"# {r['name']}", ""]
        if meta:
            L += [f"**{meta}**", ""]
        if r["description"]:
            L += [r["description"], ""]
        if r["used_in"]:
            links = " · ".join(f"[{BY_SLUG[s]['name']}]({s}.md)"
                               for s in r["used_in"] if s in BY_SLUG)
            L += [f"**Used in:** {links}", ""]
        L += ["## Ingredients", ""]
        for line in r["ingredients"].splitlines():
            line = line.strip()
            if not line:
                continue
            if ING_HEAD.match(line) and len(line.split()) <= 5:
                L += ["", f"**{line}**", ""]
            else:
                L.append(f"- {line}")
        L += ["", "## Method", ""]
        for i, s in enumerate(r["directions"].splitlines(), 1):
            if s.strip():
                L.append(f"{i}. {s.strip()}")
        if r["notes"]:
            L += ["", "## Notes", ""]
            for para in r["notes"].split("\n\n"):
                if para.strip():
                    L += [para.strip(), ""]
        open(f"recipes/{r['slug']}.md", "w").write("\n".join(L).rstrip() + "\n")

    idx = ["# Recipes", "",
           "One file per recipe. **These files are generated** — edit `build.py` and rerun",
           "`python3 build.py`, or your changes will be overwritten.", ""]
    for g in GROUP_ORDER:
        rs = [r for r in RECIPES if r["group"] == g]
        if not rs:
            continue
        idx += [f"## {g}", ""]
        if GROUP_BLURB[g]:
            idx += [GROUP_BLURB[g], ""]
        idx += ["| Recipe | Yield | Time |", "|---|---|---|"]
        for r in rs:
            idx.append(f"| [{r['name']}]({r['slug']}.md) | {r['servings'] or '—'} "
                       f"| {r['total_time'] or '—'} |")
        idx.append("")
    idx += ["---", "", "Back to [the plan](../01-the-plan.md) · "
            "[the prep session](../02-prep-session.md) · "
            "[shopping](../04-shopping-list.md) · [nutrition](../05-nutrition.md)"]
    open("recipes/README.md", "w").write("\n".join(idx) + "\n")
    return len(RECIPES) + 1


def write_paprika():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for r in RECIPES:
            payload = {
                "uid": str(uuid.uuid4()).upper(), "created": CREATED,
                "hash": hashlib.sha256(
                    (r["name"] + r["ingredients"] + r["directions"]).encode()
                ).hexdigest().upper(),
                "name": r["name"], "description": r["description"],
                "ingredients": r["ingredients"], "directions": r["directions"],
                "notes": r["notes"], "nutritional_info": "",
                "prep_time": r["prep_time"], "cook_time": r["cook_time"],
                "total_time": r["total_time"], "difficulty": "",
                "servings": r["servings"], "rating": 0,
                "source": SOURCE, "source_url": "",
                "photo": None, "photo_large": None, "photo_hash": None,
                "image_url": None,
                "categories": [f"Meal Prep: {r['group']}"] + r["cuisine"],
                "photos": [],
            }
            z.writestr(
                r["name"].replace("/", "-") + ".paprikarecipe",
                gzip.compress(json.dumps(payload).encode('ascii'), mtime=0))
    open("Sunday Kitchen Meal Prep.paprikarecipes", "wb").write(buf.getvalue())
    return len(RECIPES)


# ================================================================== ICONS

def png(path, size, fn):
    """Minimal RGB PNG writer — no third-party imaging library needed."""
    rows = bytearray()
    for y in range(size):
        rows.append(0)
        for x in range(size):
            rows += bytes(fn(x, y, size))
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))
    out = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
           + chunk(b"IEND", b""))
    open(path, "wb").write(out)


PINE, CREAM, AMBER = (26, 60, 48), (242, 234, 214), (224, 164, 74)


def icon_pixel(x, y, size):
    """A bowl with steam. Coordinates normalised to a 180px design."""
    s = size / 180.0
    fx, fy = x / s, y / s
    # steam: three rounded bars
    for cx in (66, 90, 114):
        if abs(fx - cx) <= 5.5 and 34 <= fy <= 78:
            return AMBER
    # rim: wide bar with rounded ends
    if abs(fy - 96) <= 8 and abs(fx - 90) <= 62:
        return CREAM
    # bowl: lower half of an ellipse
    if fy > 100 and ((fx - 90) / 54.0) ** 2 + ((fy - 100) / 46.0) ** 2 <= 1:
        return CREAM
    return PINE


def write_icons():
    for n in (32, 180, 512):
        png(f"icon-{n}.png", n, icon_pixel)
    open("manifest.webmanifest", "w").write(json.dumps({
        "name": "Sunday Kitchen", "short_name": "Kitchen",
        "start_url": "./", "display": "standalone",
        "background_color": "#F3F5F0", "theme_color": "#F3F5F0",
        "icons": [
            {"src": "icon-180.png", "sizes": "180x180", "type": "image/png"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png",
             "purpose": "any maskable"},
        ],
    }, indent=2) + "\n")
    return 3


if __name__ == "__main__":
    print(f"recipes.html      {write_recipes_html()} recipes")
    print(f"recipes/*.md      {write_markdown()} files")
    print(f"icons + manifest  {write_icons()} icons")
    if "--paprika" in sys.argv:
        print(f"paprika archive   {write_paprika()} recipes")
    else:
        print("paprika archive   skipped (pass --paprika to rebuild)")

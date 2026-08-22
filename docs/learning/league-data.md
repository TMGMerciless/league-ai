# League Data Learning Notes

## Purpose

These notes document what has been learned about League of Legends static data, Riot Data Dragon, schema inspection, raw data preservation, and preparation for machine-learning use.

The goal is not just to download Riot data.

The goal is to understand:

- what Riot provides
- what each field means
- which fields are useful
- which fields are presentation-only
- what should be preserved
- what should eventually be normalized
- how patch/version changes should be handled

---

# Riot Data Dragon

Riot Data Dragon provides versioned static League of Legends data.

Examples include:

- champions
- champion details
- items
- runes
- spells
- images and assets
- patch/version information

The League AI project currently uses Data Dragon as the primary static-data source.

---

# Version Discovery

Instead of hard-coding a League patch version, the ingestion code retrieves:

```text
https://ddragon.leagueoflegends.com/api/versions.json
````

The first returned version is treated as the latest currently published Data Dragon version.

Example:

```text
16.16.1
```

This allows the application to discover new Data Dragon versions automatically.

Conceptually:

```text
versions.json
    ↓
latest version
    ↓
build version-specific URLs
```

---

# Why Versioning Matters

League changes frequently.

Champion values, items, abilities, and other game data can change between patches.

Therefore data should be stored with its source version.

Current raw-data structure:

```text
data/
└── raw/
    └── 16.16.1/
        ├── champion.json
        └── champions/
```

This prevents accidentally mixing data from multiple patches.

---

# Champion Index

The first champion endpoint inspected was:

```text
champion.json
```

This provides broad information for all champions.

The current dataset returned:

```text
173 champions
```

The champion index is useful for:

* discovering champion IDs
* retrieving broad metadata
* finding the list of champions to process
* constructing detailed champion URLs

---

# Champion Index Fields

Useful fields identified include:

```text
id
name
info
tags
stats
partype
```

Not every field needs to become a machine-learning feature.

The first task is to understand what each field represents.

---

# id

Example:

```text
Aatrox
```

The champion ID provides a stable programmatic identifier.

It is useful for:

* URLs
* dictionary keys
* joining datasets
* file naming
* internal references

---

# name

Example:

```text
Aatrox
```

The name is the human-readable champion name.

It may look identical to the ID for some champions, but IDs and display names should conceptually remain separate.

---

# tags

Riot provides broad champion categories such as:

```text
Fighter
Tank
Mage
Marksman
Assassin
Support
```

These tags may be useful as coarse model features.

However, they should not necessarily be treated as a complete description of how a champion functions.

---

# info

The `info` field contains Riot-provided descriptive metrics such as:

```text
attack
defense
magic
difficulty
```

These are useful because they provide simple structured metadata.

Example future use:

```text
Riot difficulty
+
player historical performance
=
personalized champion recommendation
```

For example, if a player consistently performs poorly on champions Riot rates as highly difficult, `difficulty` may become one feature in a recommendation model.

Important:

> Riot-provided metadata is useful input, but it is not objective ground truth.

---

# difficulty

Difficulty was identified as potentially useful for personalization.

Example:

```text
difficulty = 8
```

This might eventually be combined with real player statistics.

The system could learn relationships such as:

```text
This player performs worse on high-difficulty champions.
```

That would be more useful than blindly treating Riot's difficulty value as absolute truth.

---

# stats

The `stats` section contains structured champion statistics.

Examples can include:

```text
health
health growth
armor
magic resistance
attack damage
attack speed
movement speed
```

These are potentially valuable because they provide numerical game characteristics that can later become features.

---

# partype

`partype` describes the champion's resource type.

Examples can include:

```text
Mana
Energy
Fury
```

Aatrox displayed:

```text
Blood Well
```

This raised an important lesson.

Some official Data Dragon fields may contain legacy or stale terminology.

Therefore:

> Official data should still be inspected critically.

---

# Official Data Can Still Be Imperfect

The presence of older labels such as:

```text
Blood Well
```

demonstrates that official datasets may contain:

* legacy semantics
* outdated labels
* fields maintained for compatibility
* information that does not perfectly reflect the current client

This means League AI should not blindly assume every field is current or appropriate for modeling.

---

# Champion Detail Endpoint

After inspecting the broad champion index, detailed champion data was retrieved.

Example pattern:

```text
champion/Aatrox.json
```

Detailed champion data provides additional fields such as:

* passive
* abilities/spells
* lore
* skins
* tooltips
* cooldowns
* costs
* ranges
* rank information

This distinction is important:

```text
Champion index
    =
broad metadata for every champion
```

while:

```text
Champion detail
    =
deeper gameplay information for one champion
```

---

# Passive Data

The passive section contains information such as:

```text
name
description
image
```

The passive description contains semantic gameplay information that may not exist as clean numeric fields.

Therefore text should not automatically be discarded.

---

# Image Metadata

Image objects can contain:

```text
x
y
w
h
```

These values are not gameplay coordinates.

They describe image/sprite positioning.

Conceptually:

```text
x = horizontal location in sprite
y = vertical location in sprite
w = image width
h = image height
```

These fields are useful for a UI displaying Riot assets.

They are likely irrelevant for most gameplay prediction tasks.

Important lesson:

> Some fields describe presentation rather than gameplay.

---

# Spell Data

Detailed champion records contain a list of spells.

Useful spell fields may include:

```text
id
name
description
tooltip
maxrank
cooldown
cost
costType
effect
range
resource
```

Not every field needs to be retained in the same form.

---

# Spell ID

Example:

```text
AatroxQ
```

This identifies the ability.

It should not be interpreted as:

> The player physically presses the Q keyboard key.

A better internal representation is:

```text
slot: Q
spell_id: AatroxQ
```

The slot is a logical ability position.

Physical keybindings can be customized by the user.

---

# Cooldown

`cooldown` contains structured cooldown values by ability rank.

Example conceptually:

```text
[14, 12, 10, 8, 6]
```

This is preferable for modeling because it is structured numeric data.

---

# cooldownBurn

`cooldownBurn` is generally a display-friendly/string representation of cooldown values.

Conceptually:

```text
cooldown
    =
structured numeric data

cooldownBurn
    =
formatted/display representation
```

When both exist, the structured numeric value is generally more useful for normalization.

---

# cost and costBurn

The same general pattern applies:

```text
cost
    =
structured values

costBurn
    =
display representation
```

Aatrox displayed zeroed costs because his relevant abilities do not use normal mana costs.

Different champions may populate these fields differently.

---

# effect and effectBurn

Again:

```text
effect
    =
structured values

effectBurn
    =
formatted representation
```

These fields should be inspected carefully because ability mechanics may not always map perfectly to these arrays.

---

# range and rangeBurn

`range` provides structured range values.

`rangeBurn` provides formatted/display-oriented values.

Range may become valuable later for:

* threat modeling
* engage distance
* poke classification
* positioning analysis

---

# maxrank

`maxrank` describes the maximum number of ranks an ability can receive.

This is structured gameplay information and should likely be retained.

---

# maxammo

Some abilities can have charges/ammunition.

Where relevant, `maxammo` may be useful.

For champions that do not use this mechanic, the value may not matter.

---

# Description vs Tooltip

Both description and tooltip can contain useful semantic information.

## Description

Usually provides a simpler human-readable explanation.

## Tooltip

Can contain richer mechanical detail such as:

* scaling
* recasts
* bonus damage
* crowd control
* conditions
* ability interactions

These text fields may contain information not fully represented by numeric Data Dragon fields.

Therefore they should be preserved in raw data.

---

# Structured vs Semantic Data

A useful design distinction is:

```text
STRUCTURED DATA

spell_id
slot
cooldown
cost
cost_type
range
max_rank
effects
```

versus:

```text
SEMANTIC DATA

name
description
tooltip
```

Both may be useful.

Structured fields are easier to use directly in algorithms and ML features.

Semantic text may later require additional processing to convert mechanics into structured features.

---

# Future Derived Features

League AI may eventually derive structured gameplay concepts such as:

```text
has_dash
has_knockup
has_stun
has_root
has_heal
has_shield
has_recast
damage_type
engage_range
poke_range
mobility_level
crowd_control_count
```

These values may not exist directly in Riot's source data.

They may need to be derived from:

```text
structured fields
+
ability text
+
external verified knowledge
```

This is where feature engineering becomes more important.

---

# Raw Data Should Be Preserved

The project intentionally stores Riot's original JSON before normalization.

Conceptually:

```text
Riot Data Dragon
      ↓
RAW DATA
      ↓
NORMALIZATION
      ↓
LEAGUE AI SCHEMA
```

This allows later debugging.

If something looks wrong, we can compare:

```text
Riot source
vs
our transformation
```

instead of losing the original evidence.

---

# Raw Data Is Not Committed to Git

Downloaded Data Dragon data is reproducible.

Therefore:

```text
data/raw/
```

is excluded using `.gitignore`.

Git stores:

```text
the ingestion code
```

instead of storing every downloaded version of every JSON file.

This prevents unnecessary repository growth.

---

# Current Data Ingestion Pipeline

Current architecture:

```text
Data Dragon versions.json
        ↓
get_latest_version()
        ↓
latest Data Dragon version
        ↓
champion.json
        ↓
champion index
        ↓
173 champion IDs
        ↓
for loop
        ↓
champion/{champion_id}.json
        ↓
173 detailed champion records
        ↓
versioned raw storage
```

---

# Current Python Flow

Relevant helper functions include:

```text
get_latest_version()
download_json()
save_json()
```

The `main()` function coordinates the workflow.

Conceptually:

```text
main()
  ↓
discover version
  ↓
download index
  ↓
save index
  ↓
loop over champion IDs
  ↓
download detailed champion
  ↓
save detailed champion
```

---

# Verification

After downloading detailed champion records, the project did not simply trust the success messages.

The output directory was verified with:

```bash
find data/raw/16.16.1/champions -type f -name "*.json" | wc -l
```

Result:

```text
173
```

This matched the number of champions in the index.

This confirmed:

```text
expected = 173
actual   = 173
```

---

# JSON Validation

The champion index was validated using:

```bash
python -m json.tool data/raw/16.16.1/champion.json > /dev/null && echo "Valid JSON"
```

This confirmed that the stored file could be successfully parsed as JSON.

---

# Data Discovery Before Schema Design

One of the most important lessons so far:

Do not invent the League AI schema before understanding the source.

The project first inspected:

```text
versions.json
champion.json
Aatrox.json
Aatrox passive
Aatrox spells
Aatrox Q details
```

Only after inspecting the data should normalization be designed.

This avoids building abstractions around assumptions that the source data does not actually support.

---

# Possible Normalized Champion Schema

An early conceptual normalized champion record might contain:

```text
id
name
tags
resource_type

riot_info:
    attack
    defense
    magic
    difficulty

stats

passive

abilities:
    Q
    W
    E
    R
```

Each ability could eventually contain standardized fields such as:

```text
spell_id
slot
name
max_rank
cooldowns
cost
cost_type
range
description
tooltip
```

The final schema has not yet been decided.

It should evolve based on actual product requirements.

---

# Do Not Normalize Too Early

Normalization is useful, but premature normalization can destroy useful information.

For example, if the project initially decides:

```text
tooltip is unnecessary
```

and deletes it from all normalized records, later analysis may discover that important mechanics existed only inside tooltip text.

Therefore:

> Preserve raw data permanently and normalize conservatively.

---

# Static Data vs Dynamic Game Data

Data Dragon is primarily static game data.

Examples:

```text
champions
abilities
items
runes
base stats
```

The eventual League AI system will also need dynamic data.

Examples:

```text
current level
current items
game time
current score
objectives
events
player state
```

The two should remain conceptually separate.

```text
STATIC KNOWLEDGE
       +
DYNAMIC GAME STATE
       ↓
DECISION ENGINE
```

---

# Why Static Data Matters

Dynamic data might tell the system:

```text
Enemy champion = X
Enemy level = 12
Enemy items = Y
```

Static data tells the system what those things mean:

```text
What is champion X?
What abilities does X have?
What stats does the item provide?
What role does the champion typically represent?
```

The coach ultimately needs both.

---

# Personalization Layer

A third category will eventually exist:

```text
PLAYER-SPECIFIC DATA
```

Examples:

```text
historical performance
champion preferences
difficulty tolerance
build tendencies
duo performance
notes
personal mistakes
```

A future architecture may therefore combine:

```text
STATIC LEAGUE DATA
        +
LIVE / MATCH DATA
        +
PLAYER HISTORY
        ↓
LEAGUE AI
```

---

# Data Quality Is an AI Problem

AI performance is not determined only by the model architecture.

If the source data is:

* stale
* mislabeled
* incomplete
* misunderstood
* incorrectly normalized

then the resulting model may learn incorrect relationships.

Therefore data inspection and validation are part of AI engineering.

---

# Current Definition of Done for Champion Ingestion

The current champion ingestion milestone is considered successful because:

* latest Data Dragon version is discovered automatically
* champion index downloads successfully
* detailed champion data downloads automatically
* all 173 champion files are present
* raw data is stored by version
* JSON is valid
* raw generated data is excluded from Git
* ingestion code is reproducible
* source code is version-controlled

---

# Next Data Engineering Step

The next major step is:

```text
RAW RIOT DATA
      ↓
NORMALIZATION
      ↓
LEAGUE AI CHAMPION SCHEMA
```

This will involve deciding:

* which fields should remain unchanged
* which fields should be renamed
* which redundant fields should be dropped
* how spell slots should be represented
* how abilities should be structured consistently
* which Riot metadata should be retained
* how future patches should be handled
* how normalized output should be validated

Normalization will create the first League-specific internal representation owned by this project.

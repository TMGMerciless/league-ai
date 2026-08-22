# General Coding & Engineering Practices

## Purpose

This file captures general software-engineering lessons learned while building League AI.

These concepts are not specific to Python, Linux, Git, or machine learning. They describe how to approach building reliable software.

---

## Understand Before Automating

When learning a new system, manually inspect and understand a small example before automating the entire process.

Example from League AI:

1. Manually retrieve Data Dragon's version.
2. Inspect the champion index.
3. Inspect Aatrox.
4. Inspect one Aatrox ability.
5. Understand the schema.
6. Only then build automated ingestion for all 173 champions.

This prevents building large systems around incorrect assumptions.

---

## Build Incrementally

Avoid trying to build the complete application at once.

Current League AI progression:

```text
Environment
    ↓
GPU verification
    ↓
ML fundamentals
    ↓
Git repository
    ↓
Static data discovery
    ↓
Single champion inspection
    ↓
Automated champion ingestion
    ↓
Normalization
    ↓
Tests
    ↓
Game-state representation
    ↓
Baseline decision engine
    ↓
Machine learning
```

Each step should produce something understandable and testable.

---

## Write → Check → Execute → Verify

A useful development pattern:

```text
WRITE
  ↓
CHECK
  ↓
EXECUTE
  ↓
VERIFY
  ↓
TEST
  ↓
COMMIT
```

Example:

```bash
python -m py_compile src/data_ingest.py
```

checks whether Python can parse the script.

Then:

```bash
python src/data_ingest.py
```

actually executes it.

Then:

```bash
find data/raw/16.16.1/champions -type f -name "*.json" | wc -l
```

verified that all 173 expected champion files existed.

The program printing:

```text
Saved 173 champions
```

was not considered sufficient proof.

---

## Syntax Correct Does Not Mean Program Correct

A program can have valid syntax while still doing the wrong thing.

Example:

```python
result = 2 + 2
```

is valid Python.

So is:

```python
result = 2 - 2
```

If the intended operation was addition, the second program is syntactically valid but logically incorrect.

Different levels of confidence include:

```text
Valid syntax
    ↓
Program executes
    ↓
Expected output produced
    ↓
Automated tests pass
    ↓
Behavior validated against real requirements
```

---

## Preserve Raw Source Data

When consuming external data, preserve the original source before transforming it.

League AI currently follows:

```text
Riot Data Dragon
       ↓
Raw JSON
       ↓
Normalization
       ↓
League AI representation
```

This is better than:

```text
Riot
 ↓
Immediately modify everything
 ↓
Lose original representation
```

Preserving raw data makes debugging and reproducibility easier.

If something later looks incorrect, we can ask:

```text
Was Riot's source wrong?
Was ingestion wrong?
Was normalization wrong?
Was the model wrong?
```

---

## Raw Data vs Normalized Data

Raw data is the original representation received from a source.

Normalized data is our application's cleaned and standardized representation.

Example raw Riot data may contain:

```text
cooldown
cooldownBurn
effect
effectBurn
sprite
image coordinates
description
tooltip
```

League AI may normalize that into only the information needed by the application.

Never confuse:

> Data exists

with:

> Data is useful for the model.

---

## Data Engineering Before Machine Learning

Machine learning depends on the quality and structure of its data.

Before training a model, understand:

- where data comes from
- what each field means
- whether fields are reliable
- how values are represented
- how data changes between versions
- what should become a feature
- what should be ignored
- how data can be reproduced

A sophisticated neural network trained on poorly understood data is still a poorly engineered system.

---

## Metadata Is Not Ground Truth

External datasets may provide useful descriptive metadata without that metadata being objectively correct.

Example:

Riot provides champion values for:

```text
attack
defense
magic
difficulty
```

These may be useful features.

However:

```text
difficulty = 8
```

does not mean the champion is objectively difficulty 8 for every player and situation.

It means Riot provided a coarse descriptive value.

League AI can later compare this against actual player performance.

---

## Separate Data From Presentation

Some external data exists only to display information in an application.

Example Data Dragon fields:

```text
x
y
w
h
```

may describe where an icon exists inside an image sprite sheet.

These values are useful for displaying the icon.

They are probably irrelevant for predicting League gameplay.

Ask:

> Does this field describe the game, or does it describe how information should be displayed?

---

## Keep Structured and Semantic Data

Not all useful information arrives as clean numbers.

For an ability, structured information might include:

```text
spell ID
slot
cooldown
cost
range
max rank
```

Semantic information might include:

```text
name
description
tooltip
```

The text may describe mechanics that are not completely represented by the numeric fields.

Rather than throwing text away, preserve it and decide later how it should be transformed.

---

## Prefer Reproducibility Over Manual Work

Instead of manually downloading 173 champion files, write a program capable of reproducing the dataset.

Better:

```bash
python src/data_ingest.py
```

than:

```text
Download Aatrox
Download Ahri
Download Akali
...
```

Reproducibility matters because:

- League patches change
- datasets change
- other developers may clone the project
- bugs need to be reproduced
- experiments need consistent inputs

---

## Generated Artifacts vs Source Code

Source control should generally track things required to reproduce the project.

Examples worth tracking:

```text
Python source
tests
documentation
configuration
dependency definitions
scripts
```

Examples usually not worth tracking:

```text
.venv/
__pycache__/
downloaded reproducible raw data
temporary files
compiled artifacts
```

The general principle is:

> Track the recipe, not every disposable result of running the recipe.

---

## Isolate Development Environments

Project dependencies should not unnecessarily modify or depend on the operating system's core environment.

For Python, League AI uses:

```text
.venv/
```

This provides an isolated Python environment.

Benefits include:

- avoiding dependency conflicts
- protecting system Python
- easier reproduction
- clearer dependency management
- safer experimentation

---

## Separate Responsibilities

A function or module should ideally have a clear responsibility.

Current ingestion helpers demonstrate this:

```python
get_latest_version()
download_json()
save_json()
main()
```

Instead of one enormous function doing everything:

```text
get_latest_version
    → determine version

download_json
    → retrieve JSON

save_json
    → write JSON

main
    → coordinate the workflow
```

This makes individual pieces easier to understand and eventually test.

---

## Use Meaningful Names

Prefer names that communicate purpose.

Good:

```python
champion_index
champion_url
champion_data
get_latest_version()
download_json()
```

Less useful:

```python
x
thing
stuff
data2
func()
```

Short variable names can be appropriate in mathematical contexts, but application code benefits from descriptive names.

---

## Comments Should Explain Why

Comments should add information the code itself does not clearly communicate.

Less useful:

```python
# Print champion
print(champion)
```

More useful:

```python
# Preserve Riot's original response before normalization
save_json(data, raw_path)
```

The code already explains what happens.

The comment should explain why it happens.

---

## Document Modules

Important source files should have a short module-level explanation.

Example:

```python
"""
League AI - Data Dragon ingestion

Retrieves versioned static League of Legends data from Riot's
Data Dragon service and stores the original JSON locally.

Raw data is intentionally preserved before normalization so that
downstream processing can be reproduced and audited.
"""
```

This helps another developer quickly understand why the file exists.

It also helps future me understand decisions I may have forgotten.

---

## Verify External Assumptions

External systems can:

- change
- contain legacy fields
- contain incomplete information
- lag behind another system
- use fields differently than expected

Example:

Aatrox's Data Dragon data contained the resource label:

```text
Blood Well
```

even though this may represent legacy semantics.

Lesson:

> Official data is valuable, but official does not automatically mean perfectly current or appropriate for every use case.

---

## Version External Data

League changes over time.

Data should therefore be associated with the version from which it came.

Example:

```text
data/
└── raw/
    └── 16.16.1/
        ├── champion.json
        └── champions/
```

This prevents accidentally mixing information from different patches.

---

## Build Baselines Before Complex Models

Do not assume machine learning is automatically better than simple logic.

Eventually League AI should have deterministic baselines such as:

```text
IF enemy damage is heavily magic
AND player has little magic resistance
THEN increase priority of magic-resistance items
```

A machine-learning model should then be evaluated against that baseline.

If the model cannot outperform simple logic, its additional complexity may not be justified.

---

## Complexity Must Earn Its Place

Do not add technology simply because it sounds advanced.

Examples:

- neural networks
- language models
- databases
- microservices
- distributed systems
- complex frameworks

Each component should solve a real problem.

The goal is not:

> Use as much AI as possible.

The goal is:

> Build the simplest system that reliably solves each part of the problem, then increase complexity when evidence justifies it.

---

## Separate the Decision Engine From the Explanation Layer

A future architecture may look like:

```text
League Data
    ↓
Game State
    ↓
Decision Engine
    ↓
Recommendation
    ↓
Explanation Layer
    ↓
Human-readable response
```

The language model does not necessarily need to be responsible for making every underlying decision.

A structured engine can make measurable decisions while a language model explains those decisions naturally.

This improves:

- testability
- explainability
- reliability
- debugging

---

## Failures Are Useful Data

Failed experiments should be documented when they teach something.

Example from early ML experiments:

A reasonable learning rate converged toward the desired answer.

A learning rate that was too high caused increasingly large overshooting:

```text
target
  ↓
step past target
  ↓
large correction backward
  ↓
even larger correction forward
  ↓
divergence
```

The memorable interpretation:

> The robot tried to walk toward the target, overshot it, threw itself backward, kept overcorrecting, and eventually transformed into a dog.

The joke is useful because the underlying concept is memorable:

**A learning rate that is too large can cause gradient descent to diverge rather than converge.**

---

## Keep a Learning Journal Separate From Reference Notes

Reference notes should eventually become clean explanations:

```text
What is a gradient?
What does git add do?
What does python -m mean?
```

The journal should preserve the learning process:

```text
What confused me?
What assumption did I make?
What failed?
What finally made the concept click?
What would I explain differently now?
```

Both are valuable for different reasons.

---

## Security Is Part of Engineering

Do not treat security as something added at the end.

Examples already encountered:

- SSH host fingerprints
- public vs private SSH keys
- GitHub authentication
- private email protection
- avoiding credentials in Git
- reviewing files before commits

Never commit:

```text
passwords
private SSH keys
API secrets
access tokens
credentials
```

---

## Small Commits Create Useful History

A commit should represent a meaningful project checkpoint.

Examples:

```text
Initialize League AI project structure

Add Data Dragon champion ingestion pipeline

Add detailed champion data ingestion
```

This produces a readable development history.

It is much easier to understand than one giant commit called:

```text
finished project
```

---

## Current Core Engineering Philosophy

League AI should be developed using:

```text
Understand
    ↓
Build smallest useful piece
    ↓
Verify
    ↓
Test
    ↓
Document
    ↓
Commit
    ↓
Measure
    ↓
Improve
```

The goal is not merely to produce working code.

The goal is to understand why it works, know how to verify that it works, and be able to reproduce the result.


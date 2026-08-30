# League AI Learning Journal

## Project Intent

The goal of this project is not only to build a League of Legends AI system, but to understand the underlying engineering and machine-learning concepts well enough to explain, test, and defend the design decisions.

The project is being built incrementally with an emphasis on:

- understanding before abstraction
- reproducibility
- measurable progress
- documenting failures and corrections
- keeping architecture modular
- learning AI from first principles rather than treating models as black boxes

---

## Entry 1 — Environment and GPU Foundations

I decided to use my NVIDIA-equipped laptop as the primary AI development machine and configured it as a dual-boot Ubuntu system.

The initial goal was to create as close to a bare-metal Linux AI environment as practical.

Key setup milestones included:

- Ubuntu installation
- NVIDIA driver validation
- GPU detection with `nvidia-smi`
- Python virtual environment creation
- PyTorch installation
- CUDA-capable PyTorch execution
- successful tensor operations on the RTX 4060 Laptop GPU

One early misconception was assuming I needed to manually install a complete CUDA toolkit immediately.

I learned that PyTorch can provide the CUDA runtime components needed for its own GPU workloads without requiring a standalone system-wide CUDA development toolkit.

### Lesson

Do not install components simply because a command suggests them.

Understand which software layer actually requires the dependency first.

---

## Entry 2 — Why GPUs Matter

I was challenged to understand why NVIDIA and CUDA are so common in AI rather than simply accepting that GPUs are faster.

The important concept was parallelism.

A CPU is designed to perform many different kinds of general-purpose work.

A GPU is designed to perform enormous numbers of similar mathematical operations in parallel.

Neural networks rely heavily on matrix and tensor calculations, which map well to GPU hardware.

A CPU vs GPU matrix-multiplication experiment made this tangible.

The GPU completed the large matrix operation substantially faster than the CPU.

### Correction

I initially thought of tensors as small hardware processing units inside the GPU.

That was wrong.

A tensor is a mathematical data structure.

The GPU contains hardware capable of performing many operations on tensor data in parallel.

---

## Entry 3 — First Artificial Neuron

I manually built a single artificial neuron in PyTorch.

The neuron used:

- three inputs
- three weights
- one bias
- a weighted sum
- a ReLU activation function

This helped connect the basic mathematical structure of a neuron:

```text
inputs
    ↓
weights
    ↓
weighted sum
    ↓
+ bias
    ↓
activation
    ↓
output

Important Concept

Weights control how strongly individual inputs affect the neuron.

Bias is a separate additive learnable parameter that shifts the neuron's response.

Bias does not directly modify an individual weight.

Entry 4 — ReLU and Nonlinearity

ReLU was the first activation function explored.
ReLU(x) = max(0, x)
Positive values pass through.

Negative values become zero.

I initially misunderstood this as meaning neural networks needed to eliminate negative values.

The more important reason for activation functions is nonlinearity.

Without nonlinear activation functions, stacking many linear transformations still collapses mathematically into another linear transformation.

Lesson

The important feature of ReLU is not that it removes negative numbers.

The important feature is that it introduces nonlinearity into the network.

Entry 5 — Prediction, Loss, and Gradients

The next step was giving a neuron a target value and measuring how wrong its prediction was.

This introduced the concept of loss.

Loss answers:

How bad was the prediction?

Backpropagation then calculated gradients.

I originally confused the gradient with the numerical prediction error.

That was incorrect.

A gradient answers something closer to:

How sensitive is the loss to changing this particular parameter, and in which direction?

Different learnable parameters can receive different gradients.

Important Distinction
Error / Loss
=
How wrong was the prediction?

Gradient
=
How would changing this parameter affect that loss?

Entry 6 — First Training Loop

A tiny model was created with one learnable weight.

The target required the correct weight to approach:

0.5

The model started with:

0.2

Using repeated:

prediction
→ loss
→ backward pass
→ gradient
→ parameter update

the model quickly converged toward the correct value.

This was the first time I watched a parameter change automatically through training instead of manually choosing the answer.

Lesson

Training is not the model being directly told the correct parameter values.

Training provides examples and an objective, then uses optimization to gradually discover useful parameter values.

Entry 7 — Learning Rate Failure

The initial training experiment used a learning rate of:

0.1

The model converged successfully.

I then changed the learning rate to:

1.0

The result was catastrophic divergence.

The model repeatedly overshot the correct parameter value.

Each incorrect jump created a larger error, which created larger gradients and increasingly extreme updates.

A memorable analogy emerged:

The robot was trying to walk toward the target. Instead of taking a small step, it launched itself past the target, threw itself backward, kept overcorrecting, and eventually transformed into a dog.

Lesson

A correct gradient direction does not guarantee successful training.

The learning rate determines how aggressively the optimizer responds to the gradient.

Too large:

overshoot
→ instability
→ divergence

Too small:

slow progress
→ excessive training time
Entry 8 — SSH and Headless Development

The Ubuntu laptop was configured for remote development from my primary computer.

This included:

OpenSSH Server
SSH key authentication
Windows SSH agent
lid-close behavior configured through systemd
successful headless operation

The laptop can now remain closed while being managed remotely over SSH.

Engineering Lesson

Infrastructure quality matters even during learning.

Reducing friction makes it easier to spend time on the actual project rather than constantly fighting the development environment.

Entry 9 — Git and GitHub

The League AI project was converted into a Git repository.

GitHub was added as a remote repository.

Key concepts learned included:

Git vs GitHub
local vs remote repositories
staging
commits
branches
remotes
.gitignore
SSH authentication
host fingerprints
public vs private SSH keys

The repository was moved to a main branch and pushed successfully to GitHub.

Lesson

Git is not just backup.

It creates a history of both the project and the engineering decisions that produced it.

Entry 10 — First Real League Data

The project moved from generic machine-learning exercises into actual League data engineering.

Riot Data Dragon was inspected manually before writing automation.

The process included:

discovering the latest Data Dragon version
retrieving the champion index
identifying 173 champions
inspecting Aatrox metadata
inspecting Aatrox passive data
inspecting Aatrox spell data
distinguishing gameplay fields from image/presentation fields
Important Discovery

Not all official fields are equally useful.

Some fields exist for:

gameplay

while others exist for:

display
legacy compatibility
human-readable formatting

This reinforced the need to inspect source data before designing a schema.

Entry 11 — First Data Ingestion Pipeline

The first permanent League AI data-ingestion module was created.

The pipeline now:

detects current Data Dragon version
        ↓
downloads champion index
        ↓
extracts champion IDs
        ↓
downloads detailed champion JSON
        ↓
stores raw data by version

The script downloaded detailed records for all:

173 champions

The result was verified using:

find ... | wc -l

rather than trusting program output alone.

Lesson

A program saying:

Saved 173 champions

does not prove 173 usable files exist.

Verify outputs independently.

Entry 12 — Raw Data and Reproducibility

Downloaded Riot data is intentionally excluded from Git.

Instead, Git stores the code capable of reproducing the dataset.

Raw data is preserved locally before normalization.

The architecture is:

Riot source
    ↓
raw data
    ↓
normalization
    ↓
League AI representation
Lesson

Preserving raw data provides an audit trail.

If future behavior is incorrect, the problem can be traced to:

source data
ingestion
normalization
model behavior

rather than losing the original evidence.

Current Reflection

The biggest change in my understanding so far is that AI is becoming less mysterious.

The system is starting to look less like:

A model somehow thinks.

and more like:

data
→ mathematical representation
→ weighted transformations
→ prediction
→ error measurement
→ gradients
→ optimization
→ repeated learning

At the same time, it is becoming clear that building a useful AI product requires much more than a neural network.

The project already involves:

Linux
GPU computing
Python
data engineering
Git
software architecture
testing
documentation
machine learning

The next major engineering challenge is converting Riot's raw champion data into a normalized League AI schema that can eventually support deterministic logic and machine-learning features.

## Champion Normalization and Automated Testing

### Normalization Pipeline

Built `src/normalize_champions.py` to transform Riot Data Dragon champion data into a project-controlled schema.

Development started with Aatrox as a single controlled example before generalizing the implementation.

The normalization layer now separates Riot's representation from the League AI representation.

Examples of field translation include:

- `spellblock` → `magic_resist`
- `spellblockperlevel` → `magic_resist_per_level`
- `attackdamage` → `attack_damage`
- `attackdamageperlevel` → `attack_damage_per_level`
- `partype` → `resource_type`

The normalized schema currently preserves:

- Champion ID and name
- Champion tags
- Resource type
- Riot attack, defense, magic, and difficulty metadata
- Selected base statistics
- Selected per-level growth statistics
- Passive name and description
- Ability IDs
- Ability names
- Descriptions and semantic tooltips
- Maximum ability ranks
- Cooldowns
- Costs and cost types
- Ranges

Presentation-only information such as sprite coordinates is intentionally excluded.

### Generalizing Beyond Aatrox

The original implementation used Aatrox to understand the Data Dragon structure.

After validating the approach, the normalization logic was moved into:

`normalize_champion(champion)`

The function does not contain champion-specific logic.

Champion files are discovered dynamically using:

`glob("*.json")`

The champion ID is derived from each filename using:

`Path.stem`

This removed the need to maintain a hard-coded champion list.

The pipeline successfully normalized all 173 champions available in Data Dragon patch 16.16.1.

This design should automatically discover newly added champions as long as their Data Dragon structure remains compatible with the assumptions made by the normalizer.

### Automated Testing

Installed pytest and created:

`tests/test_normalize_champions.py`

The initial test processed all champions inside one test function.

This worked, but pytest reported only one collected test because the champion loop existed inside the test.

The test was then refactored using pytest parametrization.

Each champion is now treated as an independent test case.

Current result:

`173 passed`

This improves debugging because a future failure can identify the specific champion that violates an assumption.

### Schema Validation

Automated tests now verify both successful normalization and the structure of the resulting schema.

Tests validate:

- Required top-level champion fields
- Riot metadata fields
- Base-stat fields
- Passive fields
- Ability fields
- Non-empty champion IDs and names
- Positive base HP
- Presence of passive names
- Presence of abilities

This changes validation from manual inspection of generated JSON into an automated contract.

Instead of visually checking 173 output files after every change, pytest verifies the assumptions automatically.

### Reproducible Dependencies

Updated `requirements.txt` with intentionally selected project dependencies:

- NumPy 2.5.2
- PyTorch 2.13.0
- pytest 9.1.1

Learned the difference between direct project dependencies and transitive dependencies.

For example, PyTorch installs additional CUDA and Python packages that do not need to be manually listed as direct project requirements.

Generated and environment-specific content remains excluded from Git:

- `.venv/`
- `__pycache__/`
- `data/raw/`
- `data/normalized/`

The repository stores the code necessary to reproduce generated data rather than storing the generated datasets themselves.

### Current Architecture

The project currently follows this general flow:

Data Dragon  
→ version discovery  
→ raw data ingestion  
→ versioned raw JSON  
→ normalization  
→ project-controlled champion schema  
→ automated schema validation

The project has not yet moved into meaningful League ML model development.

The current work is intentionally establishing a reliable and testable data-engineering foundation before feature engineering and model development.

### Important Correction to Earlier Understanding

The project is version-aware and can discover Data Dragon versions, but full conditional update logic has not yet been implemented.

The desired future behavior is:

local version  
→ compare against current Data Dragon version  
→ download/update only when necessary

This should not be considered complete until explicitly implemented and tested.

## Continuous Integration with GitHub Actions

### Goal

The project reached the point where automated tests should run somewhere other than the development laptop.

The purpose of Continuous Integration (CI) is to verify that committed code can work in a clean environment rather than only working because of files, packages, or configuration already present on the development system.

### Project Python Version

Created:

`.python-version`

with:

`3.14.4`

The GitHub Actions workflow reads this file instead of maintaining a separate hard-coded Python version.

This establishes the Python version as part of the project's configuration.

A system Python upgrade should not silently change the project's expected Python version. Python upgrades should instead be intentional project changes.

### GitHub Actions Workflow

Created:

`.github/workflows/tests.yml`

The workflow currently:

1. Runs on pushes and pull requests.
2. Creates a fresh Ubuntu runner.
3. Checks out the repository.
4. Reads the Python version from `.python-version`.
5. Configures Python.
6. Installs pytest.
7. Runs the self-contained unit tests while excluding integration tests.

The test command is:

`python -m pytest -m "not integration" -v`

This allows the repository to test normalization logic without requiring the locally downloaded Riot Data Dragon dataset.

### Unit Tests vs. Integration Tests

The real Riot champion tests were marked with:

`@pytest.mark.integration`

The custom marker was registered in:

`pytest.ini`

This creates an important distinction:

- Unit tests use controlled, self-contained input and can run on a clean machine.
- Integration tests validate the normalization pipeline against locally downloaded Riot Data Dragon data.

This distinction allows fast and reproducible CI testing while retaining broader validation against the real dataset during local development.

### First CI Failure

The first GitHub Actions run failed.

The failure was:

`FileNotFoundError: data/raw`

Even though the workflow used:

`-m "not integration"`

pytest still imported and collected `tests/test_normalize_champions.py`.

During collection, the parametrization called:

`get_champion_files()`

which attempted to inspect `data/raw/`.

The GitHub runner did not have this directory because raw Riot data is intentionally excluded from Git.

This demonstrated an important testing concept:

**Test collection happens before the selected tests are executed.**

Code that accesses external resources during module import or test collection can therefore fail even when those tests are later supposed to be excluded by a pytest marker.

### Fix

The integration-test module now checks whether the Riot dataset exists:

```python
if not RAW_DATA_DIR.exists():
    pytest.skip(
        "Riot Data Dragon data not available",
        allow_module_level=True,
    )

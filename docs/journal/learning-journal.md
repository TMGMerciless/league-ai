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



# AI / Machine Learning Learning Notes

## Purpose

These notes document the AI and machine-learning concepts learned while building League AI from first principles.

The goal is not only to use existing AI frameworks, but to understand what is happening underneath them.

---

# Why Build From First Principles?

Instead of beginning by calling an existing frontier language model, this project began with:

- Linux
- NVIDIA GPU compute
- CUDA
- PyTorch
- tensors
- individual artificial neurons
- activation functions
- loss
- gradients
- gradient descent
- learning rates

The goal is to understand the mechanics underneath machine learning before relying on increasingly abstract frameworks.

---

# CPU vs GPU

A CPU and GPU are both processors, but they are designed around different workloads.

## CPU

A CPU has a relatively small number of powerful, general-purpose processing cores.

It is good at:

- operating-system tasks
- branching logic
- sequential workloads
- many different kinds of computation
- general application execution

## GPU

A GPU contains a very large number of simpler execution resources designed to perform many similar mathematical operations simultaneously.

This makes GPUs particularly useful for operations common in:

- graphics
- matrix multiplication
- machine learning
- neural networks

The advantage is not simply:

> GPU is faster than CPU.

The important idea is:

> Many machine-learning calculations can be broken into huge numbers of similar mathematical operations that can be executed in parallel.

---

# Parallelism

Parallelism means performing multiple calculations at the same time rather than executing every calculation sequentially.

Conceptually:

```text
Sequential:

Calculation 1
     ↓
Calculation 2
     ↓
Calculation 3
     ↓
Calculation 4
```

Parallel:

```text
Calculation 1 ─┐
Calculation 2 ─┤
Calculation 3 ─┼─→ results
Calculation 4 ─┘
```

Real GPUs operate at a much larger scale than four operations.

Neural-network operations frequently involve large matrices containing thousands or millions of values.

GPUs are designed to perform many of those operations concurrently.

---

# CUDA

CUDA is NVIDIA's parallel-computing platform and programming model.

It allows software to execute supported computations on NVIDIA GPUs.

CUDA is one major reason NVIDIA hardware is widely used in machine learning.

Conceptually:

```text
Python application
      ↓
PyTorch
      ↓
CUDA
      ↓
NVIDIA GPU
```

This is simplified, but useful as a mental model.

---

# PyTorch

PyTorch is a machine-learning framework.

It provides tools for:

- tensors
- GPU execution
- neural-network layers
- automatic differentiation
- optimization
- loss functions
- model training

A useful memory aid has been:

> PyTorch helps light the way for our computations to reach the GPU.

This is a memory device rather than the literal definition of PyTorch.

Example:

```python
x = x.to("cuda")
```

This tells PyTorch to move the tensor to a CUDA-capable device so supported operations can execute on the GPU.

PyTorch does much more than GPU routing.

It also provides the mathematical and neural-network framework used to construct and train models.

---

# Tensors

A tensor is NOT a physical component inside a GPU.

A tensor is a mathematical/data structure.

A useful progression is:

```text
Scalar
5

Vector
[1, 2, 3]

Matrix
[
  [1, 2],
  [3, 4]
]

Higher-dimensional tensor
[
  [
    [ ... ]
  ]
]
```

In machine learning, tensors hold things such as:

- model inputs
- weights
- activations
- gradients
- images
- batches of training examples

PyTorch represents these using:

```python
torch.Tensor
```

---

# Tensor Does Not Mean GPU Core

An early misconception was thinking of tensors as small physical sectors or processing units inside the GPU.

Correction:

```text
Tensor
    =
mathematical data structure
```

while:

```text
GPU execution resources
    =
hardware that can perform operations on tensor data
```

Many operations involving tensors can be parallelized across GPU hardware.

---

# CPU vs GPU Experiment

A matrix-multiplication experiment was performed using approximately:

```python
size = 5000
```

and matrices:

```python
x = torch.rand((size, size))
y = torch.rand((size, size))
```

The operation:

```python
z = x @ y
```

performs matrix multiplication.

Observed results showed the GPU completing the workload substantially faster than the CPU.

The important lesson was not the exact benchmark number.

The lesson was:

> Large mathematical workloads that parallelize well can benefit enormously from GPU execution.

---

# GPU Timing and Synchronization

GPU operations can execute asynchronously.

Therefore timing GPU work requires synchronization.

Example:

```python
torch.cuda.synchronize()

start = time.perf_counter()

z = x @ y

torch.cuda.synchronize()

elapsed = time.perf_counter() - start
```

Without synchronization, Python may measure how quickly work was submitted rather than how long the GPU actually took to complete it.

---

# Artificial Neuron

A basic artificial neuron was manually constructed.

Example inputs:

```text
x1 =  2.0
x2 =  1.5
x3 = -1.0
```

Weights:

```text
w1 =  0.8
w2 = -0.4
w3 =  0.3
```

Bias:

```text
b = 0.2
```

The neuron computes:

```text
z = x1*w1 + x2*w2 + x3*w3 + b
```

Using the values:

```text
(2.0 × 0.8)
+
(1.5 × -0.4)
+
(-1.0 × 0.3)
+
0.2
```

becomes:

```text
1.6 - 0.6 - 0.3 + 0.2
```

resulting in approximately:

```text
0.9
```

---

# Inputs

Inputs are information provided to a model.

For League AI, future inputs might include:

```text
gold difference
level difference
champions
items
health
game time
objectives
ability availability
damage composition
player history
```

We generally determine what information is available to the model.

These input variables are often called:

```text
features
```

---

# Weights

Weights are learnable parameters.

A weight controls how strongly an input contributes to a neuron's calculation.

Conceptually:

```text
input × weight
```

Example:

```text
gold advantage = 0.5
gold weight    = 0.8
```

Contribution:

```text
0.5 × 0.8 = 0.4
```

A positive weight can increase the neuron's signal as the input increases.

A negative weight can cause increasing input to decrease the signal.

The magnitude controls the strength of the relationship.

---

# We Usually Do Not Manually Choose Final Weights

When constructing a network, we define:

- inputs
- architecture
- training objective

The model learns useful weights through training.

Weights normally begin from an initialization strategy and are repeatedly adjusted using gradients.

Conceptually:

```text
initial weights
      ↓
prediction
      ↓
loss
      ↓
gradients
      ↓
update weights
      ↓
new prediction
      ↓
repeat
```

---

# Weighted Sum

A neuron combines its weighted inputs.

For three inputs:

```text
weighted_sum =
    x1*w1
  + x2*w2
  + x3*w3
```

More generally:

```text
weighted_sum = Σ(xᵢwᵢ)
```

Then bias is added:

```text
z = weighted_sum + bias
```

Important correction:

> Bias does not multiply the weighted sum.

The neuron calculates:

```text
weighted sum + bias
```

not:

```text
weighted sum × bias
```

---

# Bias

Bias is a separate learnable parameter.

For a neuron:

```text
z = weighted_sum + bias
```

Bias acts as an additive offset.

Example:

```text
weighted sum = 1.21
bias         = -0.40

z = 0.81
```

Bias does NOT directly change an individual input's weight.

Incorrect mental model:

```text
weight = 0.5
bias = -0.1

new weight = 0.4
```

That is not what neuron bias means.

Correct structure:

```text
input1*weight1
+
input2*weight2
+
input3*weight3
+
bias
```

---

# Why Bias Is Useful

Without bias, the neuron's response is constrained by the weighted inputs.

Bias allows the neuron to shift its activation threshold or response.

A useful mental model is:

> Weights determine how strongly inputs pull on the neuron. Bias shifts the neuron's baseline.

Both weights and biases can be learned during training.

---

# Activation Functions

After computing:

```text
weighted sum + bias
```

a neuron commonly passes the result through an activation function.

Conceptually:

```text
inputs
   ↓
weights
   ↓
weighted sum
   ↓
+ bias
   ↓
activation function
   ↓
neuron output
```

Activation functions are crucial because they introduce nonlinearity.

---

# ReLU

ReLU means:

```text
Rectified Linear Unit
```

Its function is:

```text
ReLU(x) = max(0, x)
```

Examples:

```text
Input     Output

  5   →     5
  1   →     1
  0   →     0
 -1   →     0
-10   →     0
```

Positive values pass through.

Negative values become zero.

---

# Why ReLU Exists

The goal is NOT simply:

> Negative numbers are bad, so remove them.

ReLU is useful because it introduces nonlinearity.

Without nonlinear activation functions, stacking many linear layers still collapses mathematically into another linear transformation.

Conceptually:

```text
Linear
  ↓
Linear
  ↓
Linear

still behaves like:

Linear
```

Adding nonlinear activation functions allows neural networks to represent much more complicated relationships.

---

# Linear vs Nonlinear

A linear transformation follows relationships that can ultimately be represented by linear combinations.

Neural networks need to model relationships much more complicated than a single straight boundary.

League contains interactions such as:

```text
champion
×
items
×
level
×
health
×
position
×
enemy composition
×
game time
```

The effect of one feature can depend heavily on the others.

Nonlinearity allows networks to represent these complex interactions.

---

# One League Neuron Example

Imagine a neuron receiving:

```text
Gold advantage
Level advantage
Health advantage
```

After normalization:

```text
x1 = 0.5
x2 = 0.3
x3 = 0.7
```

Suppose its current weights are:

```text
w1 = 0.8
w2 = 0.6
w3 = 0.9
```

Then:

```text
0.5*0.8
+
0.3*0.6
+
0.7*0.9
```

equals:

```text
1.21
```

With:

```text
bias = -0.4
```

the pre-activation result becomes:

```text
0.81
```

An activation function can then transform that result.

---

# Many Inputs Can Feed One Neuron

A neuron does not have to receive only one input.

It can receive many inputs.

Conceptually:

```text
x1 ─w1─┐
x2 ─w2─┤
x3 ─w3─┼→ neuron
x4 ─w4─┤
x5 ─w5─┘
```

Each connection has its own weight.

---

# Many Neurons Form Layers

A neural network contains many neurons organized into layers.

Conceptually:

```text
INPUTS
  ↓
LAYER 1
  ↓
LAYER 2
  ↓
LAYER 3
  ↓
OUTPUT
```

Each neuron can learn different combinations of the information it receives.

---

# Neural Networks Are Not If/Then Trees

A neural network can sometimes feel conceptually similar to many interacting conditions, but it is not literally a giant collection of:

```text
if X then Y
```

Instead, layers perform mathematical transformations.

A simplified layer can be represented as:

```text
output = activation(Wx + b)
```

where:

```text
x = input vector
W = weight matrix
b = bias vector
```

The network learns useful transformations through training.

---

# Prediction

A prediction is the model's output for an input.

Example:

```text
Game state
    ↓
model
    ↓
78% predicted probability of winning fight
```

The prediction is not the target.

It is what the current model believes.

---

# Target / Label

The target or label represents the desired or observed answer during supervised training.

Example:

```text
Prediction:
78% chance of winning fight

Actual result:
fight lost
```

The actual result becomes training information.

---

# Loss

Loss is a numerical measure of how poorly the model's prediction matches the training target.

Conceptually:

```text
prediction
     ↓
compare with target
     ↓
loss
```

Higher loss generally means the prediction was worse according to the chosen loss function.

The exact meaning depends on the loss function being used.

---

# Loss Is Not the Gradient

Important distinction:

```text
LOSS
=
How bad was the prediction?
```

while:

```text
GRADIENT
=
How would changing a particular parameter affect that loss?
```

These are related but different concepts.

---

# Gradient

A gradient describes the sensitivity of the loss to a learnable parameter.

For a particular weight, the gradient answers something like:

> If I slightly increase this weight, which direction will the loss move, and how strongly?

A gradient therefore contains:

- direction
- sensitivity/magnitude

It is NOT simply:

```text
prediction - target
```

although the prediction error contributes to gradient calculations.

---

# Error vs Gradient

Suppose:

```text
target = 2
prediction = 4
```

The prediction is numerically off by:

```text
2
```

That error alone is not necessarily the gradient for every parameter.

Different parameters contributed differently to producing the prediction.

Therefore they can receive different gradients.

Example:

```text
gold weight gradient      = 0.18
level weight gradient     = 0.07
health weight gradient    = 0.25
bias gradient             = 0.36
```

The exact numbers depend on the model and loss function.

---

# Backpropagation

Backpropagation calculates how the final loss depends on parameters throughout the network.

Conceptually:

```text
FORWARD PASS

inputs
  ↓
layer
  ↓
layer
  ↓
prediction
  ↓
loss
```

Then:

```text
BACKWARD PASS

loss
  ↓
gradients for later layer
  ↓
gradients for earlier layer
  ↓
gradients for weights and biases
```

Backpropagation works backward through the mathematical operations used to produce the prediction.

---

# Gradients Exist for Learnable Parameters Throughout the Network

There is not simply one gradient for the entire neural network.

Learnable parameters can receive their own gradients.

That includes:

```text
weights
biases
```

across many layers.

Modern neural networks can therefore contain enormous numbers of parameters, each participating in the optimization process.

---

# Gradient Descent

Gradient descent uses gradients to update parameters in a direction intended to reduce loss.

A simplified update rule is:

```text
parameter =
parameter - learning_rate × gradient
```

This is applied repeatedly during training.

---

# Learning Rate

The learning rate controls how aggressively parameters change in response to gradients.

Conceptually:

```text
small learning rate
=
small parameter updates

large learning rate
=
large parameter updates
```

The learning rate does not make the gradient itself more accurate.

It controls the size of the step taken using that gradient.

---

# Learning Rate Experiment

A simple model was trained with a reasonable learning rate.

Observed behavior:

```text
Step 1: prediction=0.4000, loss=0.360000, weight=0.4400
Step 2: prediction=0.8800, loss=0.014400, weight=0.4880
Step 3: prediction=0.9760, loss=0.000576, weight=0.4976
Step 4: prediction=0.9952, loss=0.000023, weight=0.4995
...
prediction → 1.0000
weight     → 0.5000
loss       → 0
```

The model converged toward a parameter value that produced the desired result.

---

# Learning Rate Too High

The learning rate was then increased dramatically.

Observed behavior:

```text
prediction=0.4000
prediction=5.2000
prediction=-28.4000
prediction=206.8000
prediction=-1439.6001
prediction=10085.2012
...
```

Instead of approaching the target, the model repeatedly overshot it.

The corrections became increasingly large.

This is called:

```text
divergence
```

---

# Learning Rate Mental Model

A useful mental model:

Imagine trying to walk toward a target.

With an appropriate learning rate:

```text
start
  ↓
small step
  ↓
closer
  ↓
small step
  ↓
closer
  ↓
target
```

With an excessively large learning rate:

```text
start
  ↓
launch past target
  ↓
huge correction backward
  ↓
launch even farther past target
  ↓
larger correction
  ↓
diverge
```

Memorable version:

> Instead of walking toward the target, the robot ran into a wall, threw itself backward, kept overcorrecting, and eventually transformed into a dog.

---

# Learning Rate Too Low

A learning rate can also be too small.

Then:

```text
parameter updates
=
tiny
```

Training may:

- converge very slowly
- require excessive computation
- make little progress during available training time

Therefore both extremes can be undesirable.

---

# Training Loop

A simplified supervised-learning loop looks like:

```text
1. Provide input
2. Model makes prediction
3. Compare prediction to target
4. Calculate loss
5. Backpropagate
6. Calculate gradients
7. Optimizer updates parameters
8. Repeat
```

Or:

```text
INPUT
  ↓
FORWARD PASS
  ↓
PREDICTION
  ↓
LOSS
  ↓
BACKPROPAGATION
  ↓
GRADIENTS
  ↓
OPTIMIZER
  ↓
UPDATED PARAMETERS
  ↓
REPEAT
```

---

# Optimizer

An optimizer applies parameter updates using gradient information.

The simplified gradient-descent rule is:

```text
parameter =
parameter - learning_rate × gradient
```

Real optimizers can use more sophisticated strategies.

PyTorch provides optimizers such as:

```text
SGD
Adam
AdamW
```

These will be explored later.

---

# Parameters

Parameters are values the model learns during training.

Common examples:

```text
weights
biases
```

Inputs are not the same thing as parameters.

Example:

```text
player gold
```

may be an input.

The learned connection determining how strongly that input affects a neuron is a parameter.

---

# Feature Engineering

Feature engineering means deciding how real-world information should be represented for a model.

For League:

Raw values might include:

```text
player gold = 8400
enemy gold  = 7600
```

A useful feature might instead be:

```text
gold difference = +800
```

or a normalized representation.

Feature engineering connects:

```text
real-world League data
```

to:

```text
machine-learning mathematics
```

---

# Normalization

Different features can exist on wildly different numerical scales.

Example:

```text
gold difference   = 1000
level difference  = 1
health difference = 20
```

Feeding these values directly into a model can create undesirable scale differences.

Normalization transforms features into more comparable numerical ranges.

Teaching example:

```text
Gold advantage    → 0.5
Level advantage   → 0.3
Health advantage  → 0.7
```

The exact normalization strategy depends on the feature and model.

---

# League AI Example

Imagine trying to estimate whether a fight is favorable.

Potential inputs:

```text
gold advantage
level advantage
health advantage
items
champions
cooldowns
position
team composition
game time
```

A simple model could eventually produce:

```text
Fight success probability = 0.78
```

If the fight is then lost, training compares the prediction with the observed result.

The resulting loss is backpropagated through the model.

Gradients tell the optimizer how the learnable parameters contributed to that loss.

Parameters are then updated.

---

# The Model Does Not Automatically Know Why It Was Wrong

Suppose:

```text
gold advantage = high
health advantage = high
level advantage = high
```

and the model predicts:

```text
78% chance of winning
```

but the fight is lost.

The model does not simply reason:

> Gold must have been the problem.

Instead, backpropagation mathematically calculates how changes to each learnable parameter would affect the loss.

Over many examples, useful relationships can emerge.

---

# Personalization Example

Riot provides champion metadata such as:

```text
difficulty
attack
defense
magic
```

These can potentially become model features.

For example:

```text
Riot difficulty = 8
```

might be combined with player history showing:

```text
Player performs poorly on high-difficulty champions
```

The system could eventually learn that lower-difficulty champions have higher expected success for that particular player.

This demonstrates the difference between:

```text
global metadata
```

and:

```text
personalized learned behavior
```

---

# Neural Network Scaling

One artificial neuron performs something resembling:

```text
activation(
    x1*w1
  + x2*w2
  + ...
  + bias
)
```

A neural network performs huge numbers of related operations across many neurons and layers.

Matrix operations allow these calculations to be performed efficiently.

This is one reason tensors and GPUs become important.

---

# Why GPUs Matter More as Models Scale

For one tiny neuron, GPU acceleration may not matter.

For networks involving:

```text
millions
billions
or more parameters
```

the number of mathematical operations becomes enormous.

Many of these operations can be expressed as tensor/matrix operations that GPUs execute efficiently in parallel.

Therefore:

```text
tensor mathematics
+
parallel GPU execution
+
large neural networks
```

fit together naturally.

---

# AI Is More Than Neural Networks

Not every problem requires a neural network.

League AI may eventually combine:

```text
deterministic rules
data engineering
statistics
machine learning
neural networks
language models
```

Different tools should solve the problems they are best suited for.

---

# Deterministic Baseline

Before training sophisticated ML models, League AI should establish simple rule-based baselines.

Example:

```text
Enemy damage:
mostly magic

Player defenses:
low magic resistance

Candidate item:
provides strong magic resistance

→ increase recommendation score
```

Then machine-learning models can be measured against the baseline.

If ML does not improve performance, additional complexity may not be justified.

---

# Decision Engine vs Language Model

The eventual system does not need a language model to perform every calculation.

Possible architecture:

```text
League Data
    ↓
Game-State Representation
    ↓
Decision / Prediction Engine
    ↓
Structured Recommendation
    ↓
Language Model
    ↓
Natural Explanation
```

Example structured result:

```json
{
  "recommendation": "magic_resist",
  "confidence": 0.84,
  "reason": [
    "enemy_magic_damage_high",
    "primary_magic_threat_ahead",
    "current_magic_resistance_low"
  ]
}
```

A language layer could translate that into:

```text
Their AP carry is currently the biggest threat and
you already have enough armor. Prioritize MR.
```

This makes the underlying decision easier to test and evaluate.

---

# Important Corrections Learned

## Tensor

Incorrect:

> Tensor is a little physical processing sector inside the GPU.

Correct:

> Tensor is a mathematical data structure that hardware can perform operations on.

---

## Bias

Incorrect:

> Bias modifies an individual weight.

Correct:

> Bias is a separate additive learnable parameter applied after the weighted sum.

```text
z = weighted_sum + bias
```

---

## Gradient

Incorrect:

> Gradient is simply how far the prediction is from the target.

Correct:

> Gradient describes how sensitive the loss is to changing a particular learnable parameter.

---

## Learning Rate

Incorrect:

> Learning rate determines the accuracy of the gradient.

Correct:

> Learning rate controls how large a parameter update is made using the gradient.

---

## ReLU

Incorrect:

> ReLU exists because neural networks need to eliminate negative answers.

Correct:

> ReLU is an activation function that introduces nonlinearity by mapping negative values to zero while passing positive values through.

---

## Neural Network

Incorrect:

> Thousands of tensors independently calculate answers and vote on the result.

Correct:

> Tensors hold data, while neural-network layers perform interconnected mathematical transformations using learned parameters.

---

# Current Mental Model

The current simplified understanding of supervised neural-network training is:

```text
REAL-WORLD DATA
      ↓
FEATURES / INPUTS
      ↓
WEIGHTS
      ↓
WEIGHTED SUM
      ↓
+ BIAS
      ↓
ACTIVATION
      ↓
MORE LAYERS
      ↓
PREDICTION
      ↓
COMPARE WITH TARGET
      ↓
LOSS
      ↓
BACKPROPAGATION
      ↓
GRADIENT FOR EACH LEARNABLE PARAMETER
      ↓
OPTIMIZER
      ↓
LEARNING-RATE-CONTROLLED UPDATE
      ↓
NEW WEIGHTS + BIASES
      ↓
REPEAT
```

---

# Concepts Learned So Far

Current foundational concepts include:

- CPU vs GPU computation
- parallelism
- CUDA
- PyTorch
- tensors
- matrix multiplication
- artificial neurons
- inputs/features
- weights
- weighted sums
- bias
- activation functions
- ReLU
- linear vs nonlinear transformations
- predictions
- targets/labels
- loss
- gradients
- gradient descent
- backpropagation
- learning rate
- convergence
- divergence
- parameters
- feature engineering
- normalization
- deterministic baselines
- layered neural networks

These concepts will continue to be refined as the League AI system becomes more sophisticated.

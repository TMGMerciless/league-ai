# Python Learning Notes

## Python in This Project

Python is the primary programming language being used for the League AI project.

Current uses include:

- downloading Riot Data Dragon data
- parsing JSON
- transforming data
- building machine-learning components with PyTorch
- writing reusable scripts and tests

## System Python vs Project Python

Ubuntu has a system Python installation, for example:

```bash
/usr/bin/python3
````

The League AI project uses its own isolated Python environment:

```bash
~/league-ai/.venv/
```

This prevents project dependencies from interfering with Ubuntu's system Python.

Activate the project environment:

```bash
source .venv/bin/activate
```

Deactivate it:

```bash
deactivate
```

## pip

`pip` is Python's package installer.

Example:

```bash
python -m pip install numpy
```

Packages installed while the virtual environment is active are installed into that project's environment rather than globally.

General distinction:

* `apt` → operating-system packages
* `pip` → Python packages

## python -m

The `-m` flag means:

> Run a Python module as a program.

Examples:

```bash
python -m pip
python -m venv
python -m py_compile
```

This is useful because Python resolves and runs the module using the currently active Python environment.

## py_compile

Example:

```bash
python -m py_compile src/data_ingest.py
```

`py_compile` attempts to parse and compile a Python source file.

If the command returns no error, the file is syntactically valid.

Important:

**Valid syntax does not guarantee correct behavior.**

The script can still contain logical errors.

A useful workflow is:

**write → syntax check → execute → verify output → test**

## Running a Python Script

Example:

```bash
python src/data_ingest.py
```

This executes the Python file.

That is different from:

```bash
python -m py_compile src/data_ingest.py
```

which checks whether Python can parse and compile the file.

## Imports

Imports make code from Python's standard library or installed packages available.

Example:

```python
import json
```

This provides functions for working with JSON data.

Example:

```python
from pathlib import Path
```

This imports the `Path` class from Python's `pathlib` module.

Example:

```python
from urllib.request import urlopen
```

This imports `urlopen`, which can open URLs and retrieve data.

## Functions

Functions group reusable logic under a name.

Example:

```python
def get_latest_version():
    url = "https://ddragon.leagueoflegends.com/api/versions.json"

    with urlopen(url) as response:
        versions = json.load(response)

    return versions[0]
```

Important parts:

```python
def
```

defines a function.

```python
get_latest_version
```

is the function name.

```python
return
```

sends a result back to the code that called the function.

Using the function:

```python
version = get_latest_version()
```

This means:

> Run `get_latest_version()` and store the returned result in `version`.

## Variables

Variables store values.

Example:

```python
version = "16.16.1"
```

Example:

```python
url = "https://example.com"
```

Example:

```python
champion_index = download_json(champion_index_url)
```

The variable name can then be used instead of repeating the full value or calculation.

## Strings

Strings represent text.

Example:

```python
name = "Aatrox"
```

Python supports formatted strings, called f-strings.

Example:

```python
print(f"Saved champion details: {champion_id}")
```

The value inside `{}` is inserted into the string.

Example:

```python
url = f"{DDRAGON_BASE}/cdn/{version}/data/en_US/champion.json"
```

This allows variables to be embedded into text.

## Lists

A list stores an ordered collection of values.

Example:

```python
cooldowns = [14, 12, 10, 8, 6]
```

List values can be accessed by index.

Python indexing begins at zero:

```python
cooldowns[0]
```

returns the first value.

```python
cooldowns[1]
```

returns the second value.

## Dictionaries

A dictionary stores data as key-value pairs.

Example:

```python
champion = {
    "name": "Aatrox",
    "difficulty": 4
}
```

Access a value using its key:

```python
champion["name"]
```

returns:

```text
Aatrox
```

Riot's JSON data is loaded into nested Python dictionaries and lists.

Example:

```python
champion_index["data"]
```

accesses the value stored under the `"data"` key.

## Indexing Nested Data

Data can be nested several levels deep.

Example:

```python
data["data"]["Aatrox"]
```

This means:

1. access `"data"`
2. inside that, access `"Aatrox"`

Example:

```python
data["data"]["Aatrox"]["stats"]
```

continues one level deeper.

## for Loops

A `for` loop repeats an operation for every item in a collection.

Example from the League ingestion pipeline:

```python
for champion_id in champion_index["data"]:
    print(champion_id)
```

Conceptually:

```text
Aatrox
Ahri
Akali
...
```

The loop takes one champion ID at a time and performs the indented code beneath it.

A more complete example:

```python
for champion_id in champion_index["data"]:
    champion_url = (
        f"{DDRAGON_BASE}/cdn/{version}/data/en_US/"
        f"champion/{champion_id}.json"
    )

    champion_data = download_json(champion_url)
```

This repeats the download process for every champion.

## Indentation

Python uses indentation to define code blocks.

Example:

```python
for champion_id in champion_index["data"]:
    print(champion_id)
```

The indented `print()` belongs to the loop.

Incorrect indentation can either:

* create a syntax error
* change the program's behavior

Indentation is part of Python's structure, not just visual formatting.

## if Statements

An `if` statement runs code only when a condition is true.

Example:

```python
if version == "16.16.1":
    print("Expected version")
```

Conceptually:

> If this condition is true, execute the indented code.

## if **name** == "**main**"

Our ingestion script ends with:

```python
if __name__ == "__main__":
    main()
```

This means:

> Run `main()` when this file is executed directly.

If the file is imported into another Python program, `main()` will not automatically run.

This makes the file reusable as both:

* an executable script
* an importable module

## with Statements

Example:

```python
with urlopen(url) as response:
    data = json.load(response)
```

`with` manages a resource for a defined block of code.

When the block finishes, Python automatically handles cleanup such as closing the network response.

Another example:

```python
with path.open("w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
```

The file is automatically closed when the block ends.

## JSON

JSON is a common structured data format used by APIs and configuration systems.

Python's standard `json` module can parse JSON into Python data structures.

Example:

```python
data = json.load(response)
```

Typically:

* JSON objects become Python dictionaries
* JSON arrays become Python lists
* strings become Python strings
* numbers become Python numeric values
* booleans become `True` or `False`

## Saving JSON

Example:

```python
json.dump(data, f, indent=2)
```

This writes Python data back into JSON format.

`indent=2` formats the file so humans can read it more easily.

## pathlib and Path

`pathlib` provides an object-oriented way to work with files and directories.

Example:

```python
from pathlib import Path
```

Create a path:

```python
DATA_DIR = Path("data/raw")
```

Combine paths:

```python
DATA_DIR / version / "champion.json"
```

This is cleaner and more portable than manually constructing strings such as:

```python
"data/raw/" + version + "/champion.json"
```

## Creating Parent Directories

From the ingestion script:

```python
path.parent.mkdir(parents=True, exist_ok=True)
```

Breaking it down:

```python
path.parent
```

gets the directory containing the file.

```python
mkdir()
```

creates the directory.

```python
parents=True
```

allows missing parent directories to be created.

```python
exist_ok=True
```

prevents an error if the directory already exists.

## urlopen

Example:

```python
with urlopen(url) as response:
```

`urlopen` opens the URL and gives the program access to the response returned by the server.

In this project it is being used to retrieve Riot Data Dragon JSON.

## Reusable Helper Functions

Instead of repeating the same logic several times, helper functions were created.

Example:

```python
def download_json(url):
    with urlopen(url) as response:
        return json.load(response)
```

Now instead of rewriting the download logic:

```python
champion_data = download_json(champion_url)
```

This improves:

* readability
* maintainability
* reuse
* testing

## Main Function

The ingestion pipeline uses:

```python
def main():
```

`main()` acts as the central workflow for the script.

It currently:

1. determines the latest Data Dragon version
2. creates the champion index URL
3. downloads champion data
4. saves the raw data
5. downloads detailed champion files

Helper functions perform smaller individual tasks.

This separation makes the code easier to understand and test.

## Python Bytecode and **pycache**

Running Python can create:

```text
__pycache__/
```

These directories contain generated Python bytecode.

They are not source code and generally should not be committed to Git.

The project ignores:

```text
__pycache__/
*.py[cod]
```

## Comments

Comments explain code to humans and are ignored by Python.

Example:

```python
# Download champion details
```

Good comments should explain **why** something is being done when the reason is not obvious.

Avoid comments that simply repeat obvious code.

Bad:

```python
# Print champion
print(champion)
```

More useful:

```python
# Preserve Riot's original response before normalization
save_json(data, raw_path)
```

## Module Docstrings

A file can begin with a documentation string explaining its purpose.

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

This explains the purpose and engineering intent of the module.

## Current League AI Python Flow

The ingestion script currently performs:

```text
Python script
    ↓
get_latest_version()
    ↓
Data Dragon versions.json
    ↓
download_json()
    ↓
champion index
    ↓
for loop over champion IDs
    ↓
download each detailed champion JSON
    ↓
save_json()
    ↓
versioned local raw dataset
```

## Engineering Lessons

A useful development flow is:

**write → syntax check → execute → verify → test → commit**

Specific lessons so far:

* keep project Python isolated using `.venv`
* use functions to avoid duplicated logic
* inspect external data before designing around it
* preserve raw source data before transforming it
* do not confuse valid syntax with correct behavior
* verify generated output instead of trusting print statements
* ignore generated Python bytecode in Git
* use clear variable and function names
* use comments and docstrings to explain intent
* keep scripts reproducible instead of depending on manual downloads


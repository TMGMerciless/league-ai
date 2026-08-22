
# Git / GitHub Learning Notes

## Git vs GitHub

Git and GitHub are related but are not the same thing.

### Git

Git is a version-control system running locally on the computer.

Git tracks:

- files
- changes
- commits
- branches
- project history

Git does not require GitHub.

### GitHub

GitHub is a remote service that can host Git repositories.

It provides:

- remote backup
- collaboration
- portfolio visibility
- issue tracking
- pull requests
- repository hosting

General idea:

```text
Local Computer                         GitHub

Working Files
     ↓
git add
     ↓
Staging Area
     ↓
git commit
     ↓
Local Repository
     ↓
git push
     ↓
                                  Remote Repository
````

## Creating a Repository

The League AI repository was initialized with:

```bash
git init
```

This created:

```text
.git/
```

inside the project directory.

The `.git` directory contains Git's internal repository information.

Do not manually modify `.git` while learning Git.

The project directory remains:

```text
~/league-ai/
```

The `.git` directory is Git's internal database, not the location where project files should be created.

## git status

```bash
git status
```

shows the current state of the repository.

It can show files as:

* untracked
* modified
* staged
* deleted
* renamed

This is one of the safest commands to run when unsure what Git is currently doing.

A good habit is to run:

```bash
git status
```

before staging and before committing.

## Untracked Files

An untracked file exists in the project directory but Git has not been told to track it.

Example:

```text
Untracked files:
    README.md
```

Creating a file does not automatically put it into Git history.

## Staging

The staging area contains the exact changes intended for the next commit.

Stage a file:

```bash
git add README.md
```

Stage multiple files:

```bash
git add .gitignore src/data_ingest.py
```

Conceptually:

```text
Working Directory
       ↓
    git add
       ↓
  Staging Area
       ↓
   git commit
       ↓
Git Repository
```

Important:

`git add` does not upload anything.

It prepares the current version of a file for the next commit.

If a file is modified again after being staged, the new changes must be staged again if they should be included in the commit.

## Commits

A commit creates a permanent checkpoint in the local Git repository.

Example:

```bash
git commit -m "Initialize League AI project structure"
```

The `-m` flag provides the commit message.

Another project example:

```bash
git commit -m "Add Data Dragon champion ingestion pipeline"
```

Good commit messages should describe what changed.

Prefer:

```text
Add detailed champion data ingestion
```

instead of:

```text
stuff
```

or:

```text
changes
```

## Commit Workflow

A common workflow is:

```text
EDIT FILES
    ↓
git status
    ↓
git add
    ↓
git status
    ↓
git commit
    ↓
git push
```

The second `git status` provides a chance to verify exactly what will be committed.

## .gitignore

`.gitignore` tells Git which files or directories should normally not be tracked.

Current examples from League AI:

```text
.venv/

__pycache__/
*.py[cod]

data/raw/
```

### Why .venv Is Ignored

`.venv/` contains the project's generated Python virtual environment and installed packages.

Those dependencies can be recreated.

Git should track dependency definitions rather than thousands of generated environment files.

### Why **pycache** Is Ignored

Python automatically generates bytecode files in directories such as:

```text
__pycache__/
```

These are generated artifacts rather than source code.

### Why data/raw Is Ignored

Downloaded Riot data is reproducible through the ingestion pipeline.

Instead of storing hundreds of generated JSON files in Git, the repository stores the code capable of recreating them.

General principle:

> Track the instructions needed to reproduce generated artifacts rather than unnecessarily tracking the artifacts themselves.

## Local vs Remote

A Git repository can exist entirely locally.

A commit does not automatically appear on GitHub.

```text
git commit
```

creates a local checkpoint.

```text
git push
```

sends local commits to a configured remote repository.

## Remotes

A remote is another Git repository that the local repository knows about.

The League AI GitHub repository was configured as:

```text
origin
```

A remote can be added using:

```bash
git remote add origin REMOTE_ADDRESS
```

View configured remotes:

```bash
git remote -v
```

Conceptually:

```text
origin = nickname for the GitHub repository
```

`origin` is conventional but is not a special requirement.

## SSH GitHub Remote

The project uses SSH authentication with GitHub.

An SSH GitHub repository address generally looks like:

```text
git@github.com:USERNAME/REPOSITORY.git
```

SSH allows Git operations without repeatedly entering a GitHub username and password.

## SSH Keys

SSH uses public-key cryptography.

A key pair contains:

```text
Private Key
Public Key
```

### Private Key

The private key stays on the computer.

Never share the private key.

Example location:

```text
~/.ssh/id_ed25519
```

### Public Key

The public key can be given to services that should trust the computer.

Example:

```text
~/.ssh/id_ed25519.pub
```

The public key was added to GitHub so the Ubuntu machine could authenticate.

## Creating an SSH Key

Example:

```bash
ssh-keygen -t ed25519
```

`ed25519` identifies the cryptographic algorithm used for the key.

The default files are commonly:

```text
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

## Different SSH Relationships

The project involved two separate SSH relationships:

```text
Main Computer
      ↓
     SSH
      ↓
Ubuntu AI Laptop
```

and:

```text
Ubuntu AI Laptop
      ↓
     SSH
      ↓
GitHub
```

These are separate trust relationships and may require separate SSH configuration.

An SSH key that allows the main computer to access Ubuntu does not automatically give Ubuntu access to GitHub.

## SSH Host Fingerprints

The first time SSH connects to a new server, it may ask whether the server's host fingerprint should be trusted.

This protects against connecting to an impersonating server.

Do not blindly accept security fingerprints.

Verify the displayed fingerprint against the service's official published fingerprint when appropriate.

Once trusted, the host information is normally stored in:

```text
~/.ssh/known_hosts
```

## Testing GitHub SSH Authentication

GitHub SSH authentication can be tested with:

```bash
ssh -T git@github.com
```

A successful connection confirms that GitHub recognizes the SSH key.

GitHub does not provide a normal interactive shell through this connection; the command is primarily an authentication test.

## Git Identity

Git commits contain author information.

Configure the author name:

```bash
git config --global user.name "NAME"
```

Configure the author email:

```bash
git config --global user.email "EMAIL"
```

View Git configuration:

```bash
git config --global --list
```

The commit name does not have to be a legal name.

A GitHub-provided `noreply` email can be used to associate commits with a GitHub account without exposing a personal email address.

## Branches

A branch represents a line of development.

The project's primary branch is:

```text
main
```

The initial local branch was renamed using:

```bash
git branch -M main
```

`-M` forces the branch rename.

For this project:

```text
master → main
```

## First Push

The first push used:

```bash
git push -u origin main
```

Breaking this down:

```text
git push
```

send commits to a remote.

```text
origin
```

the remote repository.

```text
main
```

the branch being pushed.

```text
-u
```

sets the upstream tracking relationship.

After this relationship is established, future pushes can usually be:

```bash
git push
```

## Upstream Tracking

After:

```bash
git push -u origin main
```

the local branch knows it corresponds to:

```text
origin/main
```

Conceptually:

```text
Local:
main

tracks

Remote:
origin/main
```

## git push

```bash
git push
```

uploads local commits that the remote repository does not yet have.

It does not upload every file on the computer.

Only committed Git history is transferred.

## git pull

Conceptually:

```bash
git pull
```

brings remote changes down to the local repository and integrates them.

This becomes more important when:

* working from multiple computers
* collaborating with other developers
* changes are made directly through GitHub

## Moving Tracked Files

A tracked file can be moved using:

```bash
git mv OLD_PATH NEW_PATH
```

Project example:

```bash
git mv docs/learning-journal.md docs/journal/learning-journal.md
```

This changes the file's location while allowing Git to track the change as part of repository history.

## File Modes

A commit may display something like:

```text
create mode 100644 README.md
```

`100644` is Git's normal mode for a non-executable file.

This is expected for documentation and ordinary source files.

## Git Does Not Track Empty Directories

Creating:

```bash
mkdir tests
```

does not necessarily make `tests/` appear in Git.

Git tracks files, not empty directories.

Once a tracked file exists inside the directory, Git can represent that directory structure.

## Current League AI Git Workflow

The current project workflow is:

```text
Write or modify code
        ↓
Test/verify behavior
        ↓
git status
        ↓
git add selected files
        ↓
git status
        ↓
git commit -m "Meaningful description"
        ↓
git push
        ↓
GitHub
```

## Repository Hygiene

The repository should contain things such as:

```text
source code
tests
documentation
configuration
dependency definitions
reproducible scripts
```

It should generally avoid unnecessary generated artifacts such as:

```text
virtual environments
Python bytecode
temporary files
reproducible downloaded datasets
credentials
private keys
```

## Security Lessons

Never commit:

* passwords
* API keys
* private SSH keys
* access tokens
* secrets
* private credentials

Public SSH keys are designed to be shared with trusted services.

Private SSH keys are not.

Always inspect:

```bash
git status
```

before committing sensitive or unexpected files.

## Engineering Lessons

Git is more than backup.

It provides a documented history of how a project evolved.

Useful habits learned so far:

* make small, meaningful commits
* verify before committing
* use descriptive commit messages
* separate generated artifacts from source code
* understand what is local versus remote
* use SSH keys instead of repeatedly entering credentials
* never blindly accept security fingerprints
* never expose private keys
* use `.gitignore` intentionally
* preserve reproducibility
* commit working milestones instead of giant batches of unrelated changes

For a portfolio project, Git history can demonstrate not only the final result but the engineering process used to build it.



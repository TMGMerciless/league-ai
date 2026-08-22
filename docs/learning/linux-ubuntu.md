# Linux / Ubuntu Learning Notes

## Environment

Ubuntu is being used as the primary development environment for the League AI project.

The laptop was configured as a dual-boot system so Windows could remain available while Ubuntu provides a Linux-based AI/ML development environment.

## Package Management

### apt

`apt` manages software packages installed at the Ubuntu operating-system level.

Examples:

```bash
sudo apt install openssh-server
sudo apt install python3-venv
````

General distinction:

* `apt` → operating-system packages
* `pip` → Python packages, preferably installed inside a virtual environment

## Python Virtual Environments

A virtual environment isolates Python packages used by a project from the system Python installation.

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Exit the environment:

```bash
deactivate
```

The shell displays `(.venv)` when the environment is active.

This prevents project dependencies from interfering with Ubuntu's system Python environment.

## SSH

OpenSSH Server was installed so the Ubuntu AI laptop can be operated remotely.

```bash
sudo apt install openssh-server
```

SSH connection from another computer:

```bash
ssh USER@IP_ADDRESS
```

Key-based authentication was configured instead of relying only on passwords.

The laptop was also configured to remain operational when the lid is closed, allowing it to function as a headless development machine.

## systemd

`systemd` manages many Linux services and system behaviors.

Examples:

```bash
sudo systemctl status ssh
sudo systemctl restart SERVICE
```

Lid behavior was configured through systemd-logind configuration.

A useful command for viewing the effective configuration is:

```bash
systemd-analyze cat-config systemd/logind.conf
```

## Linux Pipes

The pipe operator:

```text
|
```

takes the output of one command and provides it as input to another.

Example:

```bash
find data/raw/16.16.1/champions -type f -name "*.json" | wc -l
```

This:

1. Finds JSON files.
2. Sends the filenames to `wc`.
3. Counts the resulting lines.

## find

`find` searches directories.

Example:

```bash
find docs -type f
```

* `docs` → directory to search
* `-type f` → return files only

Another example:

```bash
find data/raw/16.16.1/champions -type f -name "*.json"
```

* `-name "*.json"` → restrict results to JSON files

## wc

`wc` means word count, but it can count several things.

```bash
wc -l
```

counts lines.

Common options:

* `-l` → lines
* `-w` → words
* `-c` → bytes

When `find` outputs one filename per line, piping it into `wc -l` provides a convenient file count.

## File and Directory Commands

Create a directory:

```bash
mkdir directory
```

Create directories including missing parent directories:

```bash
mkdir -p path/to/directory
```

Create an empty file:

```bash
touch filename
```

List files:

```bash
ls
```

Include hidden files:

```bash
ls -la
```

Display file contents:

```bash
cat filename
```

## nano

`nano` is a terminal text editor.

Save:

```text
Ctrl+O
Enter
```

Exit:

```text
Ctrl+X
```

## Shutdown and Reboot

Shutdown:

```bash
sudo shutdown -h now
```

Reboot:

```bash
sudo reboot
```

## Engineering Lessons

Do not assume a command succeeded simply because it produced no obvious error.

Use a pattern of:

**write → verify → apply → test**

Examples from this project include:

* verifying system configuration before closing the laptop lid
* verifying downloaded JSON
* counting downloaded champion files
* checking Git status before committing
* checking configuration before restarting services
* preserving the system Python environment by using a virtual environment

```
```

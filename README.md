# Python Config Manager

A simple CLI tool for backing up and managing configuration files of bash, zsh, git, vim, kitty.

## Quick Start

```bash
python main.py
```

The script will:
1. Ask to create `Configs/` folder for backups
2. Ask to create `info.csv` and `symlink.csv` log files for tracking
3. Show an script menu

## Supported Programs

Config files are searched for:
- **bash** — `.bashrc`, `.bash_profile`, `.bash_aliases`
- **zsh** — `.zshrc`, `.zprofile`, `.zshenv`
- **git** — `.gitconfig`, `.gitignore_global`
- **vim** — `.vimrc`, `.gvimrc`
- **kitty** — `kitty.conf`

To add more programs, edit `paths_info.py`.

## How It Works

1. **Backup**: Copies detected config files to `Configs/<program>/`
2. **Symlink**: Replaces originals with symlinks to backups (with optional backup)
3. **Restore**: Moves configs back to original locations

## Project Structure
```
config-manager/
├── main.py
├── paths_info.py
└── README.md
```

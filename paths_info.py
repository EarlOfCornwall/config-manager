POPULAR_CONFIGS = {
    "bash": {
        "files": [".bashrc", ".bash_profile", ".bash_aliases"],
        "paths": ["~"],
    },
    "zsh": {
        "files": [".zshrc", ".zprofile", ".zshenv"],
        "paths": ["~"],
    },
    "git": {
        "files": [".gitconfig", ".gitignore_global"],
        "paths": ["~", "~/.config", "~/.config/git/"],
    },
    "vim": {
        "files": [".vimrc", ".gvimrc"],
        "paths": ["~", "~/.config", "~/.config/vim/"],
    },
    "kitty": {"files": ["kitty.conf"], "paths": ["~/.config/kitty/"]},
    "vscode": {
        "files": [
            "settings.json",
            "keybindings.json",
            "snippets",
            "tasks.json",
            "launch.json",
        ],
        "paths": ["~/.config/Code/User/"],
    },
    "cursor": {
        "files": [
            "settings.json",
            "keybindings.json",
            "cli-config.json",
            "mcp.json",
            "cli.json",
        ],
        "paths": ["~/.config/Cursor/User/", "~/.cursor/", "~/.cursor/User/"],
    },
    "opencode": {
        "files": ["opencode.json", "tui.json", "opencode.jsonc"],
        "paths": ["~/.config/opencode/"],
    },
    "lmstudio-mcp": {"files": ["mcp.json"], "paths": ["~/.lmstudio/"]},
}

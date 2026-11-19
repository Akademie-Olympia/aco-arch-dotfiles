# Commands

Every command ACO ships – plus the standard `pacman` commands you use to manage the system. ACO uses **only pacman** for updating;
`aco` adds just what pacman cannot do (activating and merging user configuration).

## `aco` – manage the configuration

Runs **without** `sudo` as a normal user (except `aco update`, which asks for `pacman` itself).
The old names keep working: `adot`, `arch-dot`, `arch-dotfiles`, `arch-dotfiles-config`.

| Command | Effect |
| --- | --- |
| `aco update` | `sudo pacman -Syu`, then merge new defaults with your changes. There are deliberately no partial updates. |
| `aco sync` | Only the merge, when you already ran `pacman -Syu` yourself |
| `aco install [module …]` | Activate installed modules (backs up existing files, links `~/.config/<module>`) |
| `aco deactivate [module …]` | Undo the activation and restore backed-up settings |
| `aco status` | Shows whether everything is active and where copies and backups live |
| `aco list` | Installed `aco-arch-dotfiles*` packages |
| `aco keys [--menu] [app …]` | Searchable list of **all** shortcuts (Hyprland, tmux, Neovim, Vim, Kitty, Ghostty, shell). In Hyprland: {kbd}`Super + K` |
| `aco packages [package …]` | Install packages with a full system upgrade (no argument: the meta package) |
| `aco path` | Directory of your editable copies (`~/.local/share/arch-dotfiles/config`) |
| `aco commands` | These commands as short help |
| `aco docs` | Address of the documentation |
| `aco scripts` | Shipped programs (`aco`, `screenshot`, `wallpaper`, …) |

### Manage monitors

The Hyprland module ships `monitors.sh` ({kbd}`Super + Shift + D` opens the menu):

```bash
~/.config/hypr/monitors.sh status                 # monitors and modes
~/.config/hypr/monitors.sh map                    # text sketch of the layout
~/.config/hypr/monitors.sh arrange HDMI-A-1 above eDP-1 center   # place relative to another monitor
~/.config/hypr/monitors.sh extend right           # side by side (left/above/below possible)
~/.config/hypr/monitors.sh mirror                 # external mirrors internal
~/.config/hypr/monitors.sh only external          # laptop display off
~/.config/hypr/monitors.sh scale HDMI-A-1 1.5
~/.config/hypr/monitors.sh profile save office    # remember the layout; plugging the same monitors in again restores it
~/.config/hypr/monitors.sh reset                  # back to automatic
```

The script writes `~/.config/hypr/monitors.local.lua` (loaded by `hyprland.lua`) and reloads Hyprland.

### Manage wallpapers

```bash
wallpaper                                # menu: choose target and image
wallpaper set forest.png --monitor DP-1  # image for one monitor
wallpaper fit contain --monitor DP-1     # cover | contain | tile | fill | default, per monitor
wallpaper dirs add ~/Pictures/Nature     # extra image folder (kept in the state, not in the config)
```

Module names: `foot fuzzel ghostty gtk-3.0 gtk-4.0 hypr kitty libfm nvim pcmanfm tmux vim wallpaper waybar yazi zsh`.

### Synchronise automatically

```bash
systemctl --user enable --now aco-arch-dotfiles-sync.timer
```

The timer merges new defaults automatically after a `pacman -Syu` (about two minutes later). Optionally a second timer reconciles the registry
with `main` (needs `gh auth login`):

```bash
systemctl --user enable --now aco-arch-dotfiles-registry-kick.timer
```

## `pacman` – manage packages

| Command | Effect |
| --- | --- |
| `sudo pacman -Syu` | Update everything, including ACO |
| `sudo pacman -S aco-arch-dotfiles-nvim` | Install a single module |
| `sudo pacman -S aco-arch-dotfiles` | The complete environment (meta package) |
| `sudo pacman -Rns aco-arch-dotfiles-nvim` | Remove a module with unused dependencies (run `aco deactivate nvim` first) |
| `pacman -Qs aco-arch-dotfiles` | Search installed ACO packages |
| `pacman -Qi aco-arch-dotfiles-core` | Show version and dependencies |
| `pacman -Ql aco-arch-dotfiles-tmux` | List a package's files |
| `pacman -Qkk aco-arch-dotfiles-hypr` | Check files for modifications |
| `pacman -U /path/package.pkg.tar.zst` | Reinstall an older version from the cache |

To undo a broken update: `ls /var/cache/pacman/pkg/aco-arch-dotfiles-*` and install the previous version with `sudo pacman -U …`. The release keeps
the two newest versions of every package.

## Shipped programs

| Command | Package | Effect |
| --- | --- | --- |
| `screenshot region\|window\|monitor\|full` | `aco-arch-dotfiles-hypr` | Capture, save, copy and edit in Satty |
| `wallpaper list\|set\|fit\|dirs\|add\|doctor\|tui` | `aco-arch-dotfiles-wallpaper` | Wallpapers per monitor – see the [Wallpaper guide](https://aco-docs.readthedocs.io/en/latest/wallpaper/guide/) |
| `y` | `aco-arch-dotfiles-zsh` | Yazi with directory change (shell function) |

Find keys in the [cheatsheet](cheatsheet.md) and the complete bindings in the manuals of
[Hyprland](https://aco-hypr.readthedocs.io/en/latest/keybindings/),
[tmux](https://aco-tmux.readthedocs.io/en/latest/keybindings/quick/),
[Neovim](https://aco-nvim.readthedocs.io/en/latest/) and [Vim](https://aco-vim.readthedocs.io/en/latest/keybindings/).

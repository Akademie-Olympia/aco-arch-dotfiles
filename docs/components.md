# Components and individual packages

Every component has its own GitHub repository with the sources in the root and its own
`packaging/arch/PKGBUILD`. The mapping lives in
[`repositories.json`](https://github.com/Akademie-Olympia/aco-arch-dotfiles/blob/main/repositories.json).
The paths below refer to activated user copies under `~/.config`, not to the read-only package files in `/usr`.

**Where the documentation lives:** the large components have their own site (Hyprland, Neovim, tmux, Zsh, Vim, Kitty, Ghostty).
The small ones – Waybar, Wallpaper, Fuzzel, Foot, Yazi, PCManFM, libfm, GTK 3 and GTK 4 – are documented together in the
[ACO Components](https://aco-docs.readthedocs.io/en/latest/) site, so the ecosystem needs one Read the Docs project instead of nine.
The sidebar of every site lists all of them.

## Installation, development and updates

```bash
# Only selected configurations, including their dependencies:
curl -fsSL https://raw.githubusercontent.com/Akademie-Olympia/aco-arch-dotfiles/main/install.sh | bash -s -- nvim tmux
# The complete environment: run the command without module names.
```

The installer activates the user copies and the sync timer. Afterwards run `sudo pacman -Syu` and, if you want it immediately, `aco sync`;
otherwise the timer merges the defaults within about two minutes. Your own changes are offered as `.pacnew` for merging, never overwritten.
See the [package guide](arch-package.md).

Development happens in separate checkouts, not by editing `/usr`:

```bash
bash scripts/clone-repos.sh  # from the central hub checkout
cd ../aco-nvim
# edit, commit and push to main
git push origin main
```

After a push to `main` the component workflow requests a central build once the package check succeeds. An optional local registry timer
additionally compares the published commits. There is no scheduled build: CI only runs on changes. A manual start is possible with
`gh workflow run packages.yml -R Akademie-Olympia/aco-arch-dotfiles`. The new package version is available through `-Syu` only after a successful build and signing.

## Neovim

- Package: `aco-arch-dotfiles-nvim`; source: [aco-nvim](https://github.com/Akademie-Olympia/aco-nvim).
- Entry point: `~/.config/nvim/init.lua`; modules under `lua/`; plugins are vendored.
- [Full manual](https://aco-nvim.readthedocs.io/en/latest/): installation, IDE and language tools, keymaps, plugins and diagnostics.
- `:NvimConfigHealth` checks optional tools; language servers are deliberately not fetched as a root installation step.

## tmux

- Package: `aco-arch-dotfiles-tmux`; source: [aco-tmux](https://github.com/Akademie-Olympia/aco-tmux).
- Entry point: `~/.config/tmux/tmux.conf`; customisations in `local-options.conf` and `local.conf`.
- [Full manual](https://aco-tmux.readthedocs.io/en/latest/).
- tmux 3.8 claims keys that used to be free: the extras now live on `prefix G` (scratch terminal), `prefix J` (fetch pane) and `prefix B` (last window).
  `g`, `@` and `Tab` keep their tmux defaults. `prefix H` opens the key explorer, `prefix R` reloads the configuration.

## Vim

- Package: `aco-arch-dotfiles-vim`; source: [aco-vim](https://github.com/Akademie-Olympia/aco-vim).
- Entry point: `~/.config/vim/vimrc`, plus `~/.vimrc` as a managed link.
- [Full manual](https://aco-vim.readthedocs.io/en/latest/) for key bindings, status line and local customisation. No plugins are downloaded.

## Ghostty

- Package: `aco-arch-dotfiles-ghostty`; source: [aco-ghostty](https://github.com/Akademie-Olympia/aco-ghostty).
- File: `~/.config/ghostty/config`.
- [Full manual](https://aco-ghostty.readthedocs.io/en/latest/). The configured Zsh process is declared as a package dependency.

## Kitty

- Package: `aco-arch-dotfiles-kitty`; source: [aco-kitty](https://github.com/Akademie-Olympia/aco-kitty).
- File: `~/.config/kitty/kitty.conf`.
- [Full manual](https://aco-kitty.readthedocs.io/en/latest/): colours, font, tabs and shortcuts. `Ctrl+Shift+F5` reloads the settings.

## Hyprland

- Package: `aco-arch-dotfiles-hypr`; source: [aco-hypr](https://github.com/Akademie-Olympia/aco-hypr).
- Entry point: `~/.config/hypr/hyprland.lua`. Desktop components, screenshot tools and the programs in use are installed through dependencies.
- Adjust machine-specific monitor rules in `~/.config/hypr/monitors.local.lua` – or let `monitors.sh` (`Super + Shift + D`) write it; this file is not distributed.
- [Desktop, screenshots and key bindings](https://aco-hypr.readthedocs.io/en/latest/guide/).
  Neither the installer nor the tests restart a running graphical session.

## Zsh

- Package: `aco-arch-dotfiles-zsh`; source: [aco-zsh](https://github.com/Akademie-Olympia/aco-zsh).
- Files: `~/.config/zsh/zshrc`, `aliases.zsh`, `themes/`; `~/.zshrc` is linked.
- Oh My Zsh and the two highlighting/suggestion plugins are managed through packages. The packaged Oh My Zsh copy does not update itself through git.
- [Shell guide](https://aco-zsh.readthedocs.io/en/latest/guide/): `j`/`ji`, `y`, fzf, editor and tmux aliases.
  Switch your login shell yourself with `chsh -s /usr/bin/zsh` if you want it.

## Small components (documented in aco-docs)

| Component | Package | Source | Files | Documentation |
| --- | --- | --- | --- | --- |
| Waybar | `aco-arch-dotfiles-waybar` | [aco-waybar](https://github.com/Akademie-Olympia/aco-waybar) | `~/.config/waybar/config.jsonc`, `style.css`, `power_menu.xml` | [Waybar](https://aco-docs.readthedocs.io/en/latest/waybar/) |
| Wallpaper | `aco-arch-dotfiles-wallpaper` | [aco-wallpaper](https://github.com/Akademie-Olympia/aco-wallpaper) | `~/.config/wallpaper/wallpaper.conf`; command `wallpaper` / `wp` | [Wallpaper](https://aco-docs.readthedocs.io/en/latest/wallpaper/) |
| Fuzzel | `aco-arch-dotfiles-fuzzel` | [aco-fuzzel](https://github.com/Akademie-Olympia/aco-fuzzel) | `~/.config/fuzzel/fuzzel.ini` | [Fuzzel](https://aco-docs.readthedocs.io/en/latest/fuzzel/) |
| Foot | `aco-arch-dotfiles-foot` | [aco-foot](https://github.com/Akademie-Olympia/aco-foot) | `~/.config/foot/foot.ini` | [Foot](https://aco-docs.readthedocs.io/en/latest/foot/) |
| Yazi | `aco-arch-dotfiles-yazi` | [aco-yazi](https://github.com/Akademie-Olympia/aco-yazi) | `~/.config/yazi/yazi.toml`, `theme.toml`, `flavors/` | [Yazi](https://aco-docs.readthedocs.io/en/latest/yazi/) |
| PCManFM | `aco-arch-dotfiles-pcmanfm` | [aco-pcmanfm](https://github.com/Akademie-Olympia/aco-pcmanfm) | `~/.config/pcmanfm/default/pcmanfm.conf` | [PCManFM](https://aco-docs.readthedocs.io/en/latest/pcmanfm/) |
| libfm | `aco-arch-dotfiles-libfm` | [aco-libfm](https://github.com/Akademie-Olympia/aco-libfm) | `~/.config/libfm/libfm.conf` | [libfm](https://aco-docs.readthedocs.io/en/latest/libfm/) |
| GTK 3 | `aco-arch-dotfiles-gtk-3.0` | [aco-gtk3](https://github.com/Akademie-Olympia/aco-gtk3) | `~/.config/gtk-3.0/settings.ini`, `gtk.css` | [GTK 3](https://aco-docs.readthedocs.io/en/latest/gtk3/) |
| GTK 4 | `aco-arch-dotfiles-gtk-4.0` | [aco-gtk4](https://github.com/Akademie-Olympia/aco-gtk4) | `~/.config/gtk-4.0/settings.ini`, `gtk.css` | [GTK 4](https://aco-docs.readthedocs.io/en/latest/gtk4/) |

Wallpaper in short: images are not distributed; put them in `~/Pictures/Wallpapers` or in the user library
`~/.local/share/arch-dotfiles/config/pictures`. `wallpaper set forest.png`, `wallpaper set ocean.png --monitor DP-1`,
`wallpaper fit contain --monitor DP-1`, `wallpaper dirs add ~/Pictures/Nature`, `wallpaper doctor`. Manage a private image repository
separately with git, not with the former `aco wallpapers`/subtree commands. The full command reference is in the
[Wallpaper guide](https://aco-docs.readthedocs.io/en/latest/wallpaper/guide/).

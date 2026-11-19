# ACO Arch Dotfiles

**Install once. Develop in individual repositories. Update with `pacman -Syu`.**

**[Full documentation](https://aco-arch-dotfiles.readthedocs.io/en/latest/)** ·
[Components](https://aco-arch-dotfiles.readthedocs.io/en/latest/components/) ·
[Verify an installation](https://aco-arch-dotfiles.readthedocs.io/en/latest/verification/) ·
[Small components](https://aco-docs.readthedocs.io/en/latest/)

This repository holds the installer, package management and the signed pacman registry. The 16 configurations live in **their own GitHub
repositories**, no longer as subtrees or configuration copies inside this repository.

## Installation

On Arch Linux as a normal user with `sudo`:

```bash
curl -fsSL https://raw.githubusercontent.com/Akademie-Olympia/aco-arch-dotfiles/main/install.sh | bash
```

Or install only selected configurations:

```bash
curl -fsSL https://raw.githubusercontent.com/Akademie-Olympia/aco-arch-dotfiles/main/install.sh | bash -s -- nvim tmux
```

The installer verifies the hard-coded signing key, sets up the pacman repository, installs packages with their dependencies, backs up existing
settings and activates the user configurations. A user timer takes over updated defaults later. Your own changes are never overwritten; new
defaults appear as `.pacnew`. System services and the login shell are not switched automatically. As with every remote installer you trust the
source code of this GitHub repository when you run it; you can download and read `install.sh` first.

Signing key fingerprint:

```text
11FB 2A9A B0F5 B8AC 4F4B A79C 27CD 0D52 E7E0 08F2
```

## Updates

```bash
sudo pacman -Syu
```

After a successful registry build, new configuration packages are normal pacman updates. The installed user timer synchronises the defaults
within about two minutes. Immediate synchronisation: `aco sync`. Reload or restart the affected application if necessary.

## Everyday tools

- `aco keys` (or `Super + K` in Hyprland) – searchable list of every shortcut of every component.
- `monitors.sh` (`Super + Shift + D`) – monitor manager: layout, arrangement, scale, profiles that restore themselves.
- `wallpaper` (`Super + Shift + W`) – wallpapers per monitor with fit modes and extra folders.

## Development: independent repositories

```bash
mkdir -p ~/git/config
git clone git@github.com:Akademie-Olympia/aco-arch-dotfiles.git ~/git/config/aco-arch-dotfiles
bash ~/git/config/aco-arch-dotfiles/scripts/clone-repos.sh
```

Afterwards all repositories sit next to each other:

```text
~/git/config/
  aco-arch-dotfiles/ # installer, registry, shared management
  aco-docs/          # documentation of the small components (one Read the Docs project)
  aco-nvim/          # own git history, main, sources and PKGBUILD
  aco-tmux/
  aco-hypr/
  aco-zsh/
  ...
```

The full mapping is in [`repositories.json`](repositories.json). Existing working copies are never overwritten. Explicit update of clean `main`
checkouts: `bash scripts/clone-repos.sh --update`.

Example:

```bash
cd ~/git/config/aco-nvim
# edit the configuration
git add lua/config
git commit -m "Adjust editor configuration"
git push origin main
```

After a push to `main`, a successful package check automatically requests the central registry build. Waiting and build time come on top; after it
succeeds the next `pacman -Syu` delivers the new version. No manual version bump is needed for normal configuration changes. Immediate build start
for maintainers:

```bash
gh workflow run packages.yml -R Akademie-Olympia/aco-arch-dotfiles
```

## Documentation layout

- **This hub** – installation, commands, packages, security, cheatsheet.
- **Large components** (Hyprland, Neovim, tmux, Zsh, Vim, Kitty, Ghostty) – one Read the Docs project each.
- **[aco-docs](https://github.com/Akademie-Olympia/aco-docs)** – Waybar, Wallpaper, Fuzzel, Foot, Yazi, PCManFM, libfm, GTK 3 and GTK 4 together,
  so that the ecosystem needs 9 Read the Docs projects instead of 17. Every site's sidebar still lists all components.
- Every component has a generated “Design & dependencies” page (`scripts/gen-design.py`): rationale, required packages, libraries and tested versions.

All documentation is written in English.

## Package structure

- 16 configuration packages, each from its own repository.
- `aco-arch-dotfiles-core`: `aco`, activation, backups and user synchronisation.
- `aco-arch-dotfiles-oh-my-zsh`: separately pinned Oh My Zsh runtime.
- `aco-arch-dotfiles`: optional meta package for the complete environment.

Every configuration maintains its dependencies and recipe itself in `packaging/arch/PKGBUILD`. Only the three shared package folders remain
under `packages/` here. All packages and repository data are published signed as assets of the GitHub release
[`repo`](https://github.com/Akademie-Olympia/aco-arch-dotfiles/releases/tag/repo). `sources.json` there documents the commits that were actually built.

**[Builds, security, migration and removal](packaging/arch/README.md)** ·
**[Application documentation](https://aco-arch-dotfiles.readthedocs.io/en/latest/)**

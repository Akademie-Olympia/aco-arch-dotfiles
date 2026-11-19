# Installation

The supported Arch installation uses individual pacman packages instead of git subtrees and a monolithic dotfiles installer.

One-time installer:

```bash
curl -fsSL https://raw.githubusercontent.com/Akademie-Olympia/aco-arch-dotfiles/main/install.sh | bash
```

Alternatively, by hand:

1. Set up the signed GitHub repository following the [package guide](arch-package.md) and verify the signing key independently.
2. Pick the configuration packages you want; pacman installs the dependencies.
3. Activate them as a normal user so existing settings are backed up and editable copies are created.

```bash
sudo pacman -Syu --needed aco-arch-dotfiles-nvim aco-arch-dotfiles-tmux
aco-arch-dotfiles-config activate nvim tmux

# Or the complete desktop/terminal environment:
sudo pacman -Syu --needed aco-arch-dotfiles
aco-arch-dotfiles-config activate
```

Updates: `aco update`, or `sudo pacman -Syu` followed by `aco-arch-dotfiles-config update`. Optionally the user timer
`aco-arch-dotfiles-sync.timer` synchronises the defaults automatically. Your own changes are never overwritten; new defaults appear as `.pacnew`.

A push to `main` of a component requests a central registry build once its package check succeeds. The optional timer
`aco-arch-dotfiles-registry-kick.timer` (part of `aco-arch-dotfiles-core`) is an additional safeguard: it compares the published
`sources.json` with `main` of all components and the hub and starts the central `Arch packages` workflow exactly when a package is behind
`main`. It needs a logged-in `gh` (`gh auth login`); without it the timer exits without action and the build is triggered by the push to `main`.
Nothing is built or signed here — the dispatch is only a request to the existing security and publication steps.

The package guide also covers local builds, migrating from the former monolith, individual removals and backups. Services and the login shell
are never changed automatically. On other platforms you can use the sources of the individual `aco-*` repositories by hand; the pacman registry
is explicitly meant for Arch Linux.

# Migrating from git subtrees

Git subtrees are no longer updated or distributed. The full sources live in standalone GitHub repositories listed in `repositories.json`
and are published as individually versioned pacman packages.

Installed systems do not need a git checkout; they receive packages and updates from the signed GitHub pacman repository.

```bash
sudo pacman -Syu --needed aco-arch-dotfiles-nvim aco-arch-dotfiles-tmux
aco-arch-dotfiles-config activate nvim tmux
sudo pacman -Syu
aco-arch-dotfiles-config update
```

See [installation, publication and safe migration](arch-package.md).

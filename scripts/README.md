# Migration entry points

The actual programs now live in the package `packages/aco-arch-dotfiles-core/`. `scripts/aco`, `install.sh` and `install-links.sh` delegate to the
installed package. No git subtrees, Oh My Zsh clones or former full installations are started.

`update-subtrees.sh` is only an aborting migration notice. `install-wallpapers.sh` remains a separate helper, to be called explicitly, for the
private `pictures/` repository; it is not part of the packages.

Maintenance scripts: `gen-cheatsheet.py` (cheatsheet from the component sources), `gen-design.py` (design and dependency pages),
`sync-docs-kit.py` (shared documentation kit), `clone-repos.py` (all repositories side by side).

See the [package guide](../packaging/arch/README.md).

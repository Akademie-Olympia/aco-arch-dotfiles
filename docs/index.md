# ACO Arch Dotfiles

::::{div} aco-hero
**Your complete Arch desktop as signed pacman packages.**
One command installs Hyprland, Waybar, terminal, editors and shell – after that
`pacman -Syu` keeps everything current. Your own changes are preserved.

```bash
curl -fsSL https://raw.githubusercontent.com/Akademie-Olympia/aco-arch-dotfiles/main/install.sh | bash
```
::::

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} Installation
:link: installation
:link-type: doc

Requirements, installer, single modules, updating and removing.
:::

:::{grid-item-card} Cheatsheet
:link: cheatsheet
:link-type: doc

The most important keys for desktop, tmux, Neovim, Vim and shell. `aco keys` (Super + K) searches all of them.
:::

:::{grid-item-card} Commands
:link: commands
:link-type: doc

`aco`, `pacman`, `screenshot`, `wallpaper` – everything you can type.
:::

:::{grid-item-card} Components
:link: components
:link-type: doc

Every configuration as its own package and repository.
:::

:::{grid-item-card} Packages & security
:link: verification
:link-type: doc

Signatures, checks, update and recovery.
:::

:::{grid-item-card} Develop
:link: arch-package
:link-type: doc

Repositories, CI and how a push becomes a package update.
:::
::::

## The manuals

Every component has a manual in the same design. The sidebar leads from anywhere to all the others.

::::{grid} 2 3 4 4
:gutter: 2

:::{grid-item-card} Hyprland
:link: https://aco-hypr.readthedocs.io/en/latest/
:link-type: url

Desktop, window slots, monitors, keys
:::

:::{grid-item-card} Neovim
:link: https://aco-nvim.readthedocs.io/en/latest/
:link-type: url

Editor, LSP, debugger
:::

:::{grid-item-card} Vim
:link: https://aco-vim.readthedocs.io/en/latest/
:link-type: url

Lean configuration
:::

:::{grid-item-card} tmux
:link: https://aco-tmux.readthedocs.io/en/latest/
:link-type: url

Sessions, panes, key explorer
:::

:::{grid-item-card} Zsh
:link: https://aco-zsh.readthedocs.io/en/latest/
:link-type: url

Shell, aliases, prompt
:::

:::{grid-item-card} Kitty
:link: https://aco-kitty.readthedocs.io/en/latest/
:link-type: url

Terminal
:::

:::{grid-item-card} Ghostty
:link: https://aco-ghostty.readthedocs.io/en/latest/
:link-type: url

Terminal
:::

:::{grid-item-card} ACO Components
:link: https://aco-docs.readthedocs.io/en/latest/
:link-type: url

Waybar, Wallpaper, Fuzzel, Foot, Yazi, PCManFM, libfm, GTK 3/4
:::
::::

The small components share one site, **ACO Components**; the sidebar of every site links straight to each of its pages.

```{toctree}
:hidden:
:maxdepth: 2
:caption: Start

installation
cheatsheet
commands
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: System

components
terminals
pakete
verification
arch-package
subtrees
```

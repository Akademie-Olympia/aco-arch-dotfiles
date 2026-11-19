# ACO Arch Dotfiles

::::{div} aco-hero
**Dein kompletter Arch-Desktop als signierte Pacman-Pakete.**
Ein Befehl installiert Hyprland, Waybar, Terminal, Editoren und Shell – danach hält
`pacman -Syu` alles aktuell. Eigene Änderungen bleiben erhalten.

```bash
curl -fsSL https://raw.githubusercontent.com/Akademie-Olympia/aco-arch-dotfiles/main/install.sh | bash
```
::::

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} Installation
:link: installation
:link-type: doc

Voraussetzungen, Installer, einzelne Module, Aktualisieren und Entfernen.
:::

:::{grid-item-card} Cheatsheet
:link: cheatsheet
:link-type: doc

Die wichtigsten Tasten für Desktop, tmux, Neovim, Vim und Shell.
:::

:::{grid-item-card} Befehle
:link: commands
:link-type: doc

`aco`, `pacman`, `screenshot`, `wallpaper` – alles, was du tippen kannst.
:::

:::{grid-item-card} Komponenten
:link: components
:link-type: doc

Jede Konfiguration als eigenes Paket und Repository.
:::

:::{grid-item-card} Pakete & Sicherheit
:link: verification
:link-type: doc

Signaturen, Prüfungen, Update und Wiederherstellung.
:::

:::{grid-item-card} Entwickeln
:link: arch-package
:link-type: doc

Repositories, CI und wie ein Push zum Paket-Update wird.
:::
::::

## Die Handbücher

Jede Komponente hat ihr eigenes Handbuch im selben Design. Die Seitenleiste führt
von überall zu allen anderen.

::::{grid} 2 3 4 4
:gutter: 2

:::{grid-item-card} Hyprland
:link: https://aco-hypr.readthedocs.io/en/latest/
:link-type: url

Desktop, Fenster-Slots, Tasten
:::

:::{grid-item-card} Waybar
:link: https://aco-waybar.readthedocs.io/en/latest/
:link-type: url

Statusleiste, Powermenü
:::

:::{grid-item-card} Neovim
:link: https://aco-nvim.readthedocs.io/en/latest/
:link-type: url

Editor, LSP, Debugger
:::

:::{grid-item-card} Vim
:link: https://aco-vim.readthedocs.io/en/latest/
:link-type: url

Schlanke Konfiguration
:::

:::{grid-item-card} tmux
:link: https://aco-tmux.readthedocs.io/en/latest/
:link-type: url

Sitzungen, Panes, Key Explorer
:::

:::{grid-item-card} Zsh
:link: https://aco-zsh.readthedocs.io/en/latest/
:link-type: url

Shell, Aliase, Prompt
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

:::{grid-item-card} Foot
:link: https://aco-foot.readthedocs.io/en/latest/
:link-type: url

Terminal
:::

:::{grid-item-card} Yazi
:link: https://aco-yazi.readthedocs.io/en/latest/
:link-type: url

Dateimanager im Terminal
:::

:::{grid-item-card} Fuzzel
:link: https://aco-fuzzel.readthedocs.io/en/latest/
:link-type: url

Anwendungsstarter
:::

:::{grid-item-card} Wallpaper
:link: https://aco-wallpaper.readthedocs.io/en/latest/
:link-type: url

Hintergründe pro Monitor
:::
::::

PCManFM, libfm, GTK 3 und GTK 4 findest du in der Seitenleiste unter „ACO Ökosystem".

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

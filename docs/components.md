# Komponenten und Einzelpakete

Alle Komponenten haben ein eigenes GitHub-Repository mit Quellen im Root und
einem eigenen `packaging/arch/PKGBUILD`. Die Zuordnung steht in
[`repositories.json`](https://github.com/Akademie-Olympia/aco-arch-dotfiles/blob/main/repositories.json).
Die hier beschriebenen Pfade beziehen sich auf aktivierte Benutzerkopien unter
`~/.config`, nicht auf schreibgeschützte Paketdateien unter `/usr`.

## Installation, Entwicklung und Updates

```bash
# Nur bestimmte Konfigurationen einschließlich ihrer Abhängigkeiten:
curl -fsSL https://raw.githubusercontent.com/Akademie-Olympia/aco-arch-dotfiles/main/install.sh | bash -s -- nvim tmux
# Die komplette Umgebung: den Aufruf ohne Modulnamen verwenden.
```

Der Installer aktiviert die Benutzerkopien und den Sync-Timer. Anschließend:
`sudo pacman -Syu`, optional sofort `aco sync`; sonst übernimmt der Timer die
Defaults innerhalb von etwa zwei Minuten. Eigene Änderungen werden als `.pacnew`
zum Zusammenführen angeboten, nicht überschrieben. Siehe [Paket-Anleitung](arch-package.md).

Entwickelt wird in separaten Checkouts, nicht durch Bearbeiten von `/usr`:

```bash
bash scripts/clone-repos.sh  # aus dem zentralen dotfiles-Checkout
cd ../nvim-config
# Änderungen bearbeiten, committen und auf main pushen.
git push origin main
```

Nach einem Push auf `main` fordert der Komponenten-Workflow nach erfolgreicher
Paketprüfung automatisch einen zentralen Build an. Zusätzlich prüft ein lokaler,
optionaler Registry-Timer die veröffentlichten Commits. Es gibt keinen
zeitgesteuerten Build mehr: CI läuft nur bei Änderungen. Ein manueller Start ist mit
`gh workflow run packages.yml -R Akademie-Olympia/aco-arch-dotfiles` möglich. Erst nach
erfolgreichem Build und Signierung ist die neue Paketversion per `-Syu` verfügbar.

## Neovim

- Paket: `aco-arch-dotfiles-nvim`; Quelle: [nvim-config](https://github.com/Akademie-Olympia/aco-nvim).
- Einstieg: `~/.config/nvim/init.lua`; Module unter `lua/`; Plugins sind vendort.
- [Vollständiges Handbuch](https://aco-nvim.readthedocs.io/en/latest/):
  Installation, IDE-/Sprachwerkzeuge, Keymaps, Plugins und Fehlerdiagnose.
- `:NvimConfigHealth` prüft optionale Werkzeuge; Sprachserver werden bewusst nicht
  als Root-Installationsschritt nachgeladen.

## tmux

- Paket: `aco-arch-dotfiles-tmux`; Quelle: [tmux-config](https://github.com/Akademie-Olympia/aco-tmux).
- Einstieg: `~/.config/tmux/tmux.conf`; Anpassungen in `local-options.conf` und `local.conf`.
- [Vollständiges Handbuch](https://aco-tmux.readthedocs.io/en/latest/).
- tmux 3.8 belegt früher freie Keys: Zusatzfunktionen liegen jetzt auf
  `prefix G` (Scratch-Terminal), `prefix J` (Pane holen) und `prefix B`
  (letztes Fenster). `g`, `@` und `Tab` behalten ihre tmux-Standardfunktion.
  `prefix H` öffnet den Key Explorer, `prefix R` lädt die Konfiguration neu.

## Vim

- Paket: `aco-arch-dotfiles-vim`; Quelle: [vim-config](https://github.com/Akademie-Olympia/aco-vim).
- Einstieg: `~/.config/vim/vimrc`, zusätzlich `~/.vimrc` als verwalteter Link.
- [Vollständiges Handbuch](https://aco-vim.readthedocs.io/en/latest/) für
  Keybindings, Statusline und lokale Anpassungen. Es werden keine Plugins nachgeladen.

## Ghostty

- Paket: `aco-arch-dotfiles-ghostty`; Quelle: [ghostty-config](https://github.com/Akademie-Olympia/aco-ghostty).
- Datei: `~/.config/ghostty/config`.
- [Vollständiges Handbuch](https://aco-ghostty.readthedocs.io/en/latest/).
  Der konfigurierte Zsh-Prozess ist als Paketabhängigkeit deklariert.

## Kitty

- Paket: `aco-arch-dotfiles-kitty`; Quelle: [kitty-config](https://github.com/Akademie-Olympia/aco-kitty).
- Datei: `~/.config/kitty/kitty.conf`.
- [Vollständiges Handbuch](https://aco-kitty.readthedocs.io/en/latest/):
  Farben, Schrift, Tabs und Tastenkombinationen. `Ctrl+Shift+F5` lädt die Einstellungen neu.

## Foot

- Paket: `aco-arch-dotfiles-foot`; Quelle: [foot-config](https://github.com/Akademie-Olympia/aco-foot).
- Datei: `~/.config/foot/foot.ini`; Wayland-Terminal mit Zsh.
- [Terminal-Anleitung](terminals.md) und `man foot.ini` beschreiben die Einstellungen.
  Änderungen gegebenenfalls durch Neustart eines Terminalfensters übernehmen.

## Hyprland

- Paket: `aco-arch-dotfiles-hypr`; Quelle: [hypr-config](https://github.com/Akademie-Olympia/aco-hypr).
- Einstieg: `~/.config/hypr/hyprland.lua`. Desktop-Komponenten, Screenshot-
  Werkzeuge und verwendete Programme werden über Abhängigkeiten installiert.
- Rechnerabhängige Monitore in `~/.config/hypr/monitors.local.lua` anpassen;
  diese Datei wird nicht verteilt.
- [Desktop, Screenshots und Keybindings](https://aco-hypr.readthedocs.io/en/latest/guide/).
  Eine laufende grafische Sitzung wird weder vom Installer noch von Tests neugestartet.

## Waybar

- Paket: `aco-arch-dotfiles-waybar`; Quelle: [waybar-config](https://github.com/Akademie-Olympia/aco-waybar).
- Dateien: `~/.config/waybar/config.jsonc`, `style.css`, `power_menu.xml`.
- [Panel-Anleitung](https://aco-waybar.readthedocs.io/en/latest/guide/) beschreibt Module, Bedienung und Anpassungen.
  Für die Darstellung werden Wayland, die passenden Schriftarten und eine laufende Sitzung benötigt.

## Fuzzel

- Paket: `aco-arch-dotfiles-fuzzel`; Quelle: [fuzzel-config](https://github.com/Akademie-Olympia/aco-fuzzel).
- Datei: `~/.config/fuzzel/fuzzel.ini` für Schrift, Farben, Layout und Verhalten.
- Fuzzel ist Anwendungsstarter und `--dmenu`-Frontend für Desktop-Helfer.
  [Hyprland-Anleitung](https://aco-hypr.readthedocs.io/en/latest/guide/) dokumentiert die Starter-/Menü-Tasten.
  Starten lässt es sich in einer Wayland-Sitzung mit `fuzzel`.

## Wallpaper

- Paket: `aco-arch-dotfiles-wallpaper`; Quelle: [wallpaper-config](https://github.com/Akademie-Olympia/aco-wallpaper).
- Datei: `~/.config/wallpaper/wallpaper.conf`; Programm: `wallpaper` bzw. `wp`.
- Private Bilder werden nicht verteilt. Bilder in `~/Pictures/Wallpapers` oder
  der Benutzerbibliothek unter `~/.local/share/arch-dotfiles/config/pictures` ablegen.
- `WALLPAPER_DIRS`, `WALLPAPER_FIT` und `WALLPAPER_NOTIFY` steuern Suchpfade,
  Skalierung und Benachrichtigungen.

```bash
wallpaper list
wallpaper set forest.png
wallpaper set ocean.png --monitor DP-1
wallpaper set city.png --all
wallpaper monitor DP-1 default
wallpaper current
wallpaper add ~/Downloads/background.png --set
wallpaper doctor
```

Ohne Monitoroption gilt ein globaler Default; ein Monitor-Override bleibt davon
unabhängig. `--all` entfernt die Overrides. `apply` stellt den gespeicherten
Zustand wieder her, `reload` startet hyprpaper neu. `next`, `prev` und `random`
wechseln Bilder. `dirs` zeigt die effektiven Suchpfade; `open` öffnet die Bibliothek.
Ein privates Bilder-Repository separat mit Git verwalten, nicht mit früheren
`aco wallpapers`-/Subtree-Kommandos.

## Yazi

- Paket: `aco-arch-dotfiles-yazi`; Quelle: [yazi-config](https://github.com/Akademie-Olympia/aco-yazi).
- `~/.config/yazi/yazi.toml`: Layout, Sortierung und Bedienung.
- `theme.toml` wählt die mitgelieferte Catppuccin-Mocha-Flavor aus `flavors/`;
  `package.toml` dokumentiert die Flavor-Quelle.
- `yazi` startet den Dateimanager. Die Zsh-Funktion `y [pfad]` wechselt nach dem
  Beenden in das zuletzt besuchte Verzeichnis; siehe [Shell-Anleitung](https://aco-zsh.readthedocs.io/en/latest/guide/).

## Zsh

- Paket: `aco-arch-dotfiles-zsh`; Quelle: [zsh-config](https://github.com/Akademie-Olympia/aco-zsh).
- Dateien: `~/.config/zsh/zshrc`, `aliases.zsh`, `themes/`; `~/.zshrc` wird verlinkt.
- Oh My Zsh und die beiden Highlighting-/Vorschlags-Plugins werden über Pakete
  verwaltet. Die paketierte Oh-My-Zsh-Kopie aktualisiert sich nicht selbst per Git.
- [Shell-Anleitung](https://aco-zsh.readthedocs.io/en/latest/guide/): `j`/`ji`, `y`, FZF, Editor- und tmux-Aliase.
  Die Login-Shell bei Bedarf selbst mit `chsh -s /usr/bin/zsh` umstellen.

## GTK3

- Paket: `aco-arch-dotfiles-gtk-3.0`; Quelle: [gtk3-config](https://github.com/Akademie-Olympia/aco-gtk3).
- Dateien: `~/.config/gtk-3.0/settings.ini` und `gtk.css`.
- `settings.ini` legt GTK-Einstellungen fest; `gtk.css` enthält das Styling.
  Nach Änderungen betroffene GTK3-Anwendungen neu starten, nicht die gesamte Sitzung.

## GTK4

- Paket: `aco-arch-dotfiles-gtk-4.0`; Quelle: [gtk4-config](https://github.com/Akademie-Olympia/aco-gtk4).
- Dateien: `~/.config/gtk-4.0/settings.ini` und `gtk.css`.
- GTK3 und GTK4 verwenden getrennte Konfigurationen. Anwendungen können eigene
  Theme-Regeln oder libadwaita verwenden; nicht jede Anwendung übernimmt jedes CSS.

## LibFM

- Paket: `aco-arch-dotfiles-libfm`; Quelle: [libfm-config](https://github.com/Akademie-Olympia/aco-libfm).
- Datei: `~/.config/libfm/libfm.conf` für den von PCManFM verwendeten Backend.
- Das Paket enthält Einstellungen, keine zusätzliche Desktop-Sitzung und keine
  persönlichen Mount-Zugangsdaten. PCManFM nach Änderungen neu starten.

## PCManFM

- Paket: `aco-arch-dotfiles-pcmanfm`; Quelle: [pcmanfm-config](https://github.com/Akademie-Olympia/aco-pcmanfm).
- Datei: `~/.config/pcmanfm/default/pcmanfm.conf` für Fenster, Ansicht und Bedienung.
- LibFM- und GTK3-Konfiguration sind als Abhängigkeiten deklariert.
  `pcmanfm` startet den Dateimanager; Mounts und Berechtigungen bleiben Aufgabe
  des jeweiligen Systems und seiner Benutzer-/Sitzungsdienste.

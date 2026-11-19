# Befehle

Alle Befehle, die ACO mitbringt – plus die Standard-`pacman`-Befehle, mit denen
du das System verwaltest. ACO nutzt **ausschließlich Pacman** zum Aktualisieren;
`aco` ergänzt nur das, was Pacman nicht kann (Benutzerkonfiguration aktivieren und zusammenführen).

## `aco` – Konfiguration verwalten

Läuft **ohne** `sudo` als normaler Benutzer (Ausnahme: `aco update` fragt für `pacman` selbst nach).
Alte Namen funktionieren weiter: `adot`, `arch-dot`, `arch-dotfiles`, `arch-dotfiles-config`.

| Befehl | Wirkung |
| --- | --- |
| `aco update` | `sudo pacman -Syu`, danach neue Vorgaben mit deinen Änderungen zusammenführen. Teil-Updates gibt es bewusst nicht. |
| `aco sync` | Nur die Zusammenführung, wenn du `pacman -Syu` schon selbst gemacht hast |
| `aco install [modul …]` | Installierte Module aktivieren (sichert vorhandene Dateien, verlinkt `~/.config/<modul>`) |
| `aco deactivate [modul …]` | Aktivierung aufheben und gesicherte Einstellungen wiederherstellen |
| `aco status` | Zeigt, ob alles aktiv ist, und wo Kopien und Backups liegen |
| `aco list` | Installierte `aco-arch-dotfiles*`-Pakete |
| `aco packages [paket …]` | Pakete mit vollständigem System-Upgrade installieren (ohne Argument: das Metapaket) |
| `aco path` | Verzeichnis deiner bearbeitbaren Kopien (`~/.local/share/arch-dotfiles/config`) |
| `aco commands` | Diese Befehle als Kurzhilfe |
| `aco docs` | Adresse der Dokumentation |
| `aco scripts` | Mitgelieferte Programme (`aco`, `screenshot`, `wallpaper`, …) |

Modul-Namen: `foot fuzzel ghostty gtk-3.0 gtk-4.0 hypr kitty libfm nvim pcmanfm tmux vim wallpaper waybar yazi zsh`.

### Automatisch synchronisieren

```bash
systemctl --user enable --now aco-arch-dotfiles-sync.timer
```

Der Timer führt neue Vorgaben nach einem `pacman -Syu` automatisch zusammen
(etwa zwei Minuten später). Optional gleicht ein zweiter Timer das Registry mit `main` ab (braucht `gh auth login`):

```bash
systemctl --user enable --now aco-arch-dotfiles-registry-kick.timer
```

## `pacman` – Pakete verwalten

| Befehl | Wirkung |
| --- | --- |
| `sudo pacman -Syu` | Alles aktualisieren, auch ACO |
| `sudo pacman -S aco-arch-dotfiles-nvim` | Ein einzelnes Modul installieren |
| `sudo pacman -S aco-arch-dotfiles` | Die komplette Umgebung (Metapaket) |
| `sudo pacman -Rns aco-arch-dotfiles-nvim` | Modul samt unbenutzter Abhängigkeiten entfernen (vorher `aco deactivate nvim`) |
| `pacman -Qs aco-arch-dotfiles` | Installierte ACO-Pakete suchen |
| `pacman -Qi aco-arch-dotfiles-core` | Version und Abhängigkeiten ansehen |
| `pacman -Ql aco-arch-dotfiles-tmux` | Dateien eines Pakets auflisten |
| `pacman -Qkk aco-arch-dotfiles-hypr` | Dateien auf Veränderungen prüfen |
| `pacman -U /pfad/paket.pkg.tar.zst` | Eine ältere Version aus dem Cache zurückspielen |

Ein defektes Update rückgängig machen: `ls /var/cache/pacman/pkg/aco-arch-dotfiles-*`
und mit `sudo pacman -U …` die vorige Version installieren. Das Release hält pro Paket
die beiden neuesten Versionen vor.

## Mitgelieferte Programme

| Befehl | Paket | Wirkung |
| --- | --- | --- |
| `screenshot region\|window\|monitor\|full` | `aco-arch-dotfiles-hypr` | Aufnahme speichern, kopieren und in Satty bearbeiten |
| `wallpaper list\|set\|add\|doctor\|tui` | `aco-arch-dotfiles-wallpaper` | Hintergrundbilder pro Monitor – siehe [Wallpaper-Handbuch](https://aco-wallpaper.readthedocs.io/en/latest/cli/) |
| `y` | `aco-arch-dotfiles-zsh` | Yazi mit Verzeichniswechsel (Shell-Funktion) |

Tasten findest du im [Cheatsheet](cheatsheet.md), die vollständigen Belegungen in den Handbüchern
von [Hyprland](https://aco-hypr.readthedocs.io/en/latest/keybindings/),
[tmux](https://aco-tmux.readthedocs.io/en/latest/keybindings/quick/),
[Neovim](https://aco-nvim.readthedocs.io/en/latest/) und [Vim](https://aco-vim.readthedocs.io/en/latest/keybindings/).

# ACO Arch Dotfiles

**Einmal installieren. In einzelnen Repositories entwickeln. Mit `pacman -Syu` aktualisieren.**

**[Vollständige Dokumentation](https://aco-arch-dotfiles.readthedocs.io/en/latest/)** ·
[Komponenten](https://aco-arch-dotfiles.readthedocs.io/en/latest/components/) ·
[Installation prüfen](https://aco-arch-dotfiles.readthedocs.io/en/latest/verification/)

Dieses Repository enthält Installer, Paketverwaltung und die signierte
Pacman-Registry. Die 16 Konfigurationen liegen in **eigenen GitHub-Repositories**,
nicht mehr als Subtrees oder Konfigurationskopien in diesem Repository.

## Installation

Auf Arch Linux als normaler Benutzer mit `sudo`:

```bash
curl -fsSL https://raw.githubusercontent.com/Akademie-Olympia/aco-arch-dotfiles/main/install.sh | bash
```

Oder nur ausgewählte Konfigurationen installieren:

```bash
curl -fsSL https://raw.githubusercontent.com/Akademie-Olympia/aco-arch-dotfiles/main/install.sh | bash -s -- nvim tmux
```

Der Installer prüft den fest hinterlegten Signierschlüssel, richtet das
Pacman-Repository ein, installiert Pakete samt Abhängigkeiten, sichert bestehende
Einstellungen und aktiviert die Benutzerkonfigurationen. Ein User-Timer übernimmt
künftig aktualisierte Defaults. Eigene Änderungen werden nicht überschrieben;
neue Defaults erscheinen als `.pacnew`. Dienste des Systems und Login-Shell werden
nicht automatisch umgestellt. Wie bei jedem Remote-Installer vertraust du beim
Ausführen dem Quellcode dieses GitHub-Repositories; du kannst `install.sh` vorher
herunterladen und prüfen.

Signierschlüssel-Fingerprint:

```text
11FB 2A9A B0F5 B8AC 4F4B A79C 27CD 0D52 E7E0 08F2
```

## Updates

```bash
sudo pacman -Syu
```

Nach erfolgreichem Registry-Build sind neue Konfigurationspakete normale
Pacman-Updates. Der installierte User-Timer synchronisiert die Defaults innerhalb
von etwa zwei Minuten. Sofortige Synchronisation: `aco sync`.
Die betroffene Anwendung gegebenenfalls neu laden/starten.

## Entwicklung: unabhängige Repositories

```bash
mkdir -p ~/git/config
git clone git@github.com:Akademie-Olympia/aco-arch-dotfiles.git ~/git/config/aco-arch-dotfiles
bash ~/git/config/aco-arch-dotfiles/scripts/clone-repos.sh
```

Danach liegen alle Repositories nebeneinander:

```text
~/git/config/
  aco-arch-dotfiles/ # Installer, Registry, gemeinsame Verwaltung
  aco-nvim/       # eigene Git-Historie, main, Quellen und PKGBUILD
  aco-tmux/
  aco-hypr/
  aco-zsh/
  ...
```

Die vollständige Zuordnung steht in [`repositories.json`](repositories.json).
Vorhandene Arbeitskopien werden nicht überschrieben. Explizite Updates sauberer
`main`-Checkouts: `bash scripts/clone-repos.sh --update`.

Beispiel:

```bash
cd ~/git/config/nvim-config
# Konfiguration bearbeiten
git add lua/config
git commit -m "Adjust editor configuration"
git push origin main
```

Nach einem Push auf `main` fordert die erfolgreiche Paketprüfung automatisch den
zentralen Registry-Build an. Hinzu kommen Warte- und Build-Zeit. Nach dessen Erfolg erhält
das nächste `pacman -Syu` die neue Version. Es ist kein manuelles Versionsbumpen
für normale Konfigurationsänderungen erforderlich. Sofortiger Build-Start für
Maintainer:

```bash
gh workflow run packages.yml -R Akademie-Olympia/aco-arch-dotfiles
```

## Paketstruktur

- 16 Konfigurationspakete, jeweils aus einem eigenen Repository.
- `aco-arch-dotfiles-core`: `aco`, Aktivierung, Backups und User-Synchronisation.
- `aco-arch-dotfiles-oh-my-zsh`: separat gepinnter Oh-My-Zsh-Runtime.
- `aco-arch-dotfiles`: optionales Metapaket für die komplette Umgebung.

Jede Konfiguration pflegt ihre Abhängigkeiten und ihr Rezept selbst in
`packaging/arch/PKGBUILD`. Hier bleiben nur die drei gemeinsamen Paketordner
unter `packages/`. Alle Pakete und Repository-Daten werden signiert als Assets
des GitHub-Releases [`repo`](https://github.com/Akademie-Olympia/aco-arch-dotfiles/releases/tag/repo)
veröffentlicht. `sources.json` dort dokumentiert die tatsächlich gebauten Commits.

**[Builds, Sicherheit, Migration und Deinstallation](packaging/arch/README.md)** ·
**[Anwendungsdokumentation](https://aco-arch-dotfiles.readthedocs.io/en/latest/)**

#!/usr/bin/env python3
"""Generate docs/design.md ("Aufbau und Abhängigkeiten") for every component repository.

    python3 scripts/gen-design.py [--root DIR]

Facts come from the sources, not from memory: package dependencies from each
packaging/arch/PKGBUILD, vendored plugins from plugins.lock (Neovim),
vendor-manifest/plugins.toml (tmux), package.toml (Yazi) and the Oh My Zsh pin of
the hub. "Getestet mit" versions come from the local pacman database, so run the
script on an up-to-date system. The reasoning ("Warum so gebaut") is curated below.
"""
import argparse
import csv
from datetime import date
from pathlib import Path
import re
import subprocess
import sys
import tomllib

HUB = Path(__file__).resolve().parent.parent
MODULES = {  # module -> repository directory name
    "foot": "aco-foot", "fuzzel": "aco-fuzzel", "ghostty": "aco-ghostty", "gtk-3.0": "aco-gtk3",
    "gtk-4.0": "aco-gtk4", "hypr": "aco-hypr", "kitty": "aco-kitty", "libfm": "aco-libfm",
    "nvim": "aco-nvim", "pcmanfm": "aco-pcmanfm", "tmux": "aco-tmux", "vim": "aco-vim",
    "wallpaper": "aco-wallpaper", "waybar": "aco-waybar", "yazi": "aco-yazi", "zsh": "aco-zsh",
}
TITLE = {"gtk-3.0": "GTK 3", "gtk-4.0": "GTK 4", "hypr": "Hyprland", "nvim": "Neovim", "pcmanfm": "PCManFM",
         "libfm": "libfm", "zsh": "Zsh", "tmux": "tmux", "vim": "Vim", "yazi": "Yazi", "foot": "Foot",
         "kitty": "Kitty", "ghostty": "Ghostty", "fuzzel": "Fuzzel", "waybar": "Waybar", "wallpaper": "Wallpaper"}
DOCS = "https://{}.readthedocs.io/en/latest/"

# Why each upstream package is needed (shared wording; per-module overrides below).
REASON = {
    "hyprland": "Wayland-Compositor; die Konfiguration ist Lua (ab 0.55) und braucht mindestens 0.56",
    "hyprpaper": "Hintergrund-Daemon, vom Wallpaper-Befehl per IPC gesteuert",
    "hyprlock": "Bildschirmsperre (`Super + L`, Power-Menü)",
    "hypridle": "Leerlauf-Erkennung (Sperren/Standby)",
    "xdg-desktop-portal-hyprland": "Bildschirmfreigabe und Datei-Dialoge für Wayland-Programme",
    "wl-clipboard": "`wl-copy`/`wl-paste` für die Zwischenablage (Screenshots, Skripte)",
    "grim": "Bildschirmaufnahme", "slurp": "Bereichsauswahl für Screenshots",
    "satty": "Screenshot-Editor (Beschriften, Speichern, Kopieren)",
    "brightnessctl": "Helligkeitstasten", "jq": "JSON aus `hyprctl` auswerten (Skripte)",
    "util-linux": "Basiswerkzeuge der Skripte (`flock`, `getopt` …)", "procps-ng": "`pgrep`/`pkill` in den Menü-Skripten",
    "sudo": "Grafische Passwortabfrage über `askpass.sh`", "firefox": "Standard-Browser (`Super + B`)",
    "fuzzel": "Anwendungsstarter und dmenu-Menü", "foot": "Terminal", "kitty": "Terminal", "ghostty": "Terminal",
    "zsh": "Login-Shell der Terminals", "tmux": "Terminal-Multiplexer",
    "ttf-jetbrains-mono-nerd": "Schrift mit Nerd-Font-Symbolen (Waybar, Yazi, Neovim, Terminals)",
    "gtk3": "GTK-3-Bibliothek (Dateimanager, Dialoge)", "gtk4": "GTK-4-/libadwaita-Bibliothek",
    "adwaita-icon-theme": "Symbolsatz `Adwaita`", "libfm": "Dateioperationen, Papierkorb, Miniaturbilder",
    "pcmanfm": "Grafischer Dateimanager", "waybar": "Statusleiste",
    "libpulse": "Audio-Schnittstelle für Lautstärke-Module", "networkmanager": "Netzwerkstatus (`network`-Modul, `nmtui`)",
    "bluez-utils": "Bluetooth-Werkzeuge", "power-profiles-daemon": "Energieprofile",
    "yazi": "Terminal-Dateimanager", "file": "Dateityp-Erkennung für Vorschauen", "fd": "Schnelle Dateisuche (`z` in Yazi, Telescope)",
    "ripgrep": "Volltextsuche (Yazi, Neovim `<leader>fg`)", "fzf": "Fuzzy-Suche (Shell-Verlauf, Yazi, tmux, Neovim)",
    "zoxide": "Häufige Ordner anspringen (`j`, Yazi `Z`)", "poppler": "PDF-Vorschau", "imagemagick": "Bildvorschau",
    "ffmpeg": "Videovorschau", "7zip": "Archivvorschau", "findutils": "`find` für die Bildersuche",
    "zsh-autosuggestions": "Vorschläge aus dem Verlauf", "zsh-syntax-highlighting": "Live-Einfärbung der Befehlszeile",
    "neovim": "Editor; benötigt mindestens 0.12 (native LSP-/Plugin-APIs)", "vim": "Editor",
    "git": "Versionsverwaltung (Gitsigns, Fugitive, Skripte)", "curl": "Downloads für Mason-Werkzeuge",
    "tar": "Archive entpacken (Mason)", "gzip": "Archive entpacken (Mason)", "unzip": "Archive entpacken (Mason)",
    "bash": "Interpreter der Skripte", "base-devel": "Optional: Treesitter-Parser kompilieren",
    "nodejs": "Optional: Sprachwerkzeuge (LSP/Formatter)", "npm": "Optional: Mason-Werkzeuge",
    "python-pip": "Optional: Python-Werkzeuge",
}
# Why a module exists the way it is built (curated).
WHY = {
    "foot": ["Foot ist die **leichte** Terminal-Option neben Kitty und Ghostty: schnell, wenig Speicher, nur Wayland. Deshalb enthält die Konfiguration nur Schrift, Farben und Shell.",
             "Farben und Schrift sind identisch mit Kitty und Ghostty, damit ein Terminalwechsel nichts Sichtbares ändert.",
             "Tabs/Splits fehlen absichtlich – das übernehmen Hyprland und tmux."],
    "kitty": ["Kitty ist das **Standard-Terminal** des Desktops (`Super + Enter`): GPU-beschleunigt, Bildprotokoll für Yazi-Vorschauen, Fernsteuerung.",
              "Transparenz (`background_opacity 0.90`) und Schrift entsprechen Foot und Ghostty; die Login-Shell ist fest `/usr/bin/zsh`."],
    "ghostty": ["Ghostty ist die **moderne Alternative** mit eigener Shell-Integration; die Konfiguration hält Farben, Schrift und Shell mit Kitty/Foot deckungsgleich.",
                "`shell-integration-features = no-cursor` lässt den Cursor-Stil der Konfiguration unangetastet."],
    "fuzzel": ["Ein einziges Menü für alles: Starter, Fenster-Wechsler, Power-Menü, Wallpaper-Wahl, Bildschirm-Menü und Tastenliste benutzen `fuzzel --dmenu`. So sieht und bedient sich jedes Menü gleich.",
               "Fuzzel startet in Millisekunden und braucht kein Toolkit – passend zu einem Desktop ohne Animationen."],
    "waybar": ["Die Leiste zeigt **nur Dauerhaftes**: Workspaces, Uhr, Lautstärke, Akku, Power. Programme starten und Fenster wechseln liegen auf Tastenkürzeln und im Fuzzel-Menü.",
               "Sie hängt über die Hyprland-IPC am Compositor (`hyprland/workspaces`) und nutzt für Power-Aktionen dessen Skripte."],
    "wallpaper": ["Hyprpaper kennt nur ein Bild je Anweisung; der Befehl ergänzt **Zustand** (Default + Overrides), Ordnersuche, Menü und Wiederherstellung beim Anstecken.",
                  "Der Zustand liegt außerhalb der Konfiguration (`~/.local/state`), damit Updates ihn nie überschreiben; Bilder gehören nicht ins Paket (Urheberrecht)."],
    "hypr": ["Reaktionsschnell statt hübsch: keine Animationen, Unschärfe, Schatten oder Abstände – maximale Bildfläche.",
             "Mehrere Monitore sind der Normalfall: Fokus-/Fenster-Sprung, Fenster-Slots (`Super + F1…F4`), Workspace-Tausch; neue Monitore ordnen sich automatisch rechts an.",
             "Die Konfiguration ist **Lua**; `scripts/gen-docs.py` erzeugt die Tastenliste direkt daraus, damit Doku und Belegung nicht auseinanderlaufen.",
             "Sie zieht die übrigen Desktop-Pakete (Terminal, Menü, Leiste, Wallpaper, tmux, Yazi, PCManFM, Browser) als Abhängigkeiten nach, damit eine Installation sofort funktioniert."],
    "tmux": ["Standards bleiben erhalten; es gibt keinen globalen `unbind-key -a`. Plugins sind **mitgeliefert (vendored) und aus**, bis man sie einschaltet.",
             "Fähigkeiten (Terminal, Zwischenablage, OSC 52, Symbole) werden **erkannt**, nicht angenommen – SSH ist ein gleichberechtigter Einsatzort.",
             "Siehe [Philosophie](philosophy) und [Architektur](architecture) für die ausführliche Begründung."],
    "vim": ["Vim ist die **schlanke Rückfallebene** (Server, Notfall, `sudo vim`): eine einzige `vimrc`, kein Plugin-Manager.",
            "Leader (`Space`) und Tastenbelegung sind mit Neovim abgeglichen, damit die Muskelerinnerung in beiden Editoren gilt."],
    "nvim": ["Eine IDE, die **offline und reproduzierbar** startet: alle Plugins liegen im Repository (`pack/vendor`), festgehalten in `plugins.lock`; beim ersten Start wird nichts geladen.",
             "Natives LSP und modularer Aufbau statt großer Plugin-Frameworks; Werkzeuge (Sprachserver, Formatter) holt Mason bei Bedarf.",
             "Siehe [Architektur](architecture) und [Plugins](plugins) für Details und das Update-Verfahren."],
    "zsh": ["Oh My Zsh ist **auf einen Commit gepinnt** und als eigenes Paket geliefert (`aco-arch-dotfiles-oh-my-zsh`); es wird nichts per `git clone` nachgeladen.",
            "Autosuggestions und Syntax-Highlighting kommen als Arch-Pakete, nicht als Plugin-Klone – Updates laufen über pacman.",
            "Kleine, klare Alltagsbefehle: `y` (Yazi mit Verzeichniswechsel), `j` (zoxide), `tm`, `nv`/`v`, `wp`."],
    "yazi": ["Ergänzt PCManFM für die Tastatur: schnell navigieren, Vorschau, Verzeichniswechsel in die Shell (`y`).",
             "Das Farb-Flavor liegt im Paket, festgehalten in `package.toml` – kein Download beim ersten Start."],
    "gtk-3.0": ["GTK-Programme sollen nicht aus dem Stil fallen. `settings.ini` setzt Verhalten, `gtk.css` die Farben; das Thema bleibt `Adwaita-dark`, damit Layout vertraut bleibt."],
    "gtk-4.0": ["GTK 4/libadwaita ignoriert Themennamen weitgehend und liest benannte Farben – deshalb setzt `gtk.css` genau diese und nichts darüber hinaus."],
    "libfm": ["Das Verhalten des Dateimanagers (Papierkorb, Terminal, Miniaturen) ist von seinem Aussehen getrennt: libfm bestimmt das **Was**, PCManFM das **Wie**."],
    "pcmanfm": ["Der grafische Dateimanager für Maus-Aufgaben (Datenträger, Drag & Drop); Yazi übernimmt die Tastatur-Arbeit.",
                "Verhalten kommt aus libfm, Aussehen aus GTK 3 – beide sind Abhängigkeiten dieses Pakets."],
}
# Runtime relations between modules: (module, other, why). Rendered in both directions.
USES = [
    ("hypr", "kitty", "Standard-Terminal (`Super + Enter`), auch für `kitty -e yazi` und `kitty -e tmux`"),
    ("hypr", "fuzzel", "Starter und alle Menü-Skripte (`powermenu.sh`, `windowswitcher.sh`, `askpass.sh`)"),
    ("hypr", "waybar", "Wird beim Start der Sitzung gestartet (`Super + Shift + B` lädt neu)"),
    ("hypr", "wallpaper", "Hintergründe beim Start und bei `monitor.added`; `Super + Shift + W`"),
    ("hypr", "tmux", "`Super + Shift + Enter` öffnet Kitty mit der tmux-Sitzung `main`"),
    ("hypr", "yazi", "`Super + Y` öffnet Yazi im Terminal"),
    ("hypr", "pcmanfm", "`Super + E` öffnet den grafischen Dateimanager"),
    ("waybar", "hypr", "Workspaces über die Hyprland-IPC; Power-Menü ruft `powermenu.sh`, `hyprlock` und `hyprctl`"),
    ("wallpaper", "hypr", "`hyprctl` und `hyprpaper`; die Sitzung ruft `wallpaper apply` beim Start und Anstecken auf"),
    ("wallpaper", "fuzzel", "Auswahlmenü (`wallpaper` ohne Argumente)"),
    ("fuzzel", "kitty", "`terminal=kitty -e` für Programme, die ein Terminal brauchen"),
    ("libfm", "kitty", "`terminal=kitty` für „Im Terminal ausführen“"),
    ("pcmanfm", "libfm", "Dateioperationen, Papierkorb, Seitenleiste"),
    ("pcmanfm", "gtk-3.0", "Farben und Schrift"),
    ("kitty", "zsh", "Login-Shell `/usr/bin/zsh`"),
    ("ghostty", "zsh", "Login-Shell `/usr/bin/zsh`"),
    ("foot", "zsh", "Login-Shell `/usr/bin/zsh`"),
    ("yazi", "zsh", "Der Befehl `y` (Verzeichniswechsel beim Beenden) steckt in `aliases.zsh`"),
    ("zsh", "yazi", "`y` startet Yazi"),
    ("zsh", "tmux", "`tm` öffnet die Sitzung `main`"),
    ("zsh", "nvim", "`nv` / `EDITOR=nvim`"),
    ("zsh", "vim", "`v`"),
    ("zsh", "wallpaper", "`wp` ist der Wallpaper-Befehl"),
    ("zsh", "hypr", "`SUDO_ASKPASS` zeigt auf `askpass.sh` (grafische Passwortabfrage)"),
    ("tmux", "kitty", "Zwischenablage über OSC 52 funktioniert in Kitty, Ghostty und Foot"),
    ("vim", "nvim", "Gemeinsame Leader-Taste und Tastenbelegung"),
    ("nvim", "vim", "Gemeinsame Leader-Taste und Tastenbelegung"),
    ("gtk-4.0", "gtk-3.0", "Gleiche Palette und gleiche `settings.ini`; unterschiedliche CSS-Namen"),
    ("gtk-3.0", "gtk-4.0", "Gleiche Palette und gleiche `settings.ini`; unterschiedliche CSS-Namen"),
]
NOTES = {
    "waybar": ["`networkmanager`, `bluez-utils` und `power-profiles-daemon` stehen im `PKGBUILD`, die ausgelieferte `config.jsonc` nutzt aber **kein** Modul dafür – sie sind für eigene Erweiterungen vorgesehen (siehe [Anleitung](guide)).",
               "Für Klick und Mausrad der Lautstärke ruft die Leiste `wpctl` auf (Paket `wireplumber`). Es ist nicht als Abhängigkeit deklariert und kommt mit der PipeWire-Installation."],
    "hypr": ["`brightnessctl`, `wl-clipboard`, `grim`, `slurp` und `satty` werden nur von den Skripten (`screenshot.sh`) und Tastenkürzeln benutzt – ohne sie fehlt genau die zugehörige Taste.",
             "Mit `Super + Shift + D` verwaltet `monitors.sh` die Bildschirme und schreibt `monitors.local.lua` – diese Datei liegt außerhalb des Pakets."],
    "wallpaper": ["`hyprctl` stammt aus dem Paket `hyprland`; es ist hier nicht als Abhängigkeit eingetragen, weil der Befehl nur in einer Hyprland-Sitzung sinnvoll ist."],
}

SHARED = """## Gemeinsame Grundlagen

Diese Regeln gelten für **alle** ACO-Komponenten:

- **Ein Repository je Komponente**, mit eigenem `PKGBUILD` und eigener CI. Jede Konfiguration lässt sich einzeln installieren, testen und entwickeln;
  nach dem Push baut die zentrale Registry das signierte Paket ([Aufbau der Paketierung](https://aco-arch-dotfiles.readthedocs.io/en/latest/arch-package/)).
- **Pacman ist der einzige Updater.** Kein Git-Pull zur Laufzeit; `aco` führt nur neue Vorgaben mit deinen Änderungen zusammen (`.pacnew`).
- **Deine Kopie, nicht die des Pakets.** `~/.config/<modul>` zeigt auf `~/.local/share/arch-dotfiles/config/<modul>/`; das Paket liegt unverändert unter `/usr/share/arch-dotfiles/<modul>/`.
- **Eine Palette, eine Schrift:** Catppuccin Mocha und JetBrainsMono Nerd Font in jeder Komponente, damit nichts aus dem Stil fällt.
- **Der Kern** `aco-arch-dotfiles-core` (Befehl `aco`, Aktivierung, Backups, Synchronisation) ist Abhängigkeit jedes Pakets.
"""


def parse_pkgbuild(path):
    text = path.read_text()
    def arr(name):
        m = re.search(rf"^{name}=\((.*?)\)", text, re.M | re.S)
        return re.findall(r"'([^']+)'", m.group(1)) if m else []
    return arr("depends"), arr("optdepends")


def installed(name):
    try:
        out = subprocess.run(["pacman", "-Q", name], capture_output=True, text=True)
        return out.stdout.split()[1] if out.returncode == 0 else None
    except FileNotFoundError:
        return None


def split_dep(dep):
    m = re.match(r"([^<>=:]+)(?:([<>]=?|=)([^:]+))?(?::\s*(.*))?$", dep)
    return m.group(1), (m.group(2) + m.group(3)) if m.group(2) else "", (m.group(4) or "")


def vendored(root, module):
    repo = root / MODULES[module]
    rows = []
    if module == "nvim":
        with open(repo / "plugins.lock", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                rows.append((row["name"], row["url"].removesuffix(".git"), row["sha"][:7], row["load_type"]))
        head = "| Plugin | Quelle | Stand (Commit) | Laden |\n| --- | --- | --- | --- |"
        body = [f"| {n} | <{u}> | `{s}` | {'beim Start' if t == 'start' else 'bei Bedarf'} |" for n, u, s, t in rows]
        return "Neovim-Plugins (`plugins.lock`, im Repository unter `pack/vendor/`)", head, body
    if module == "tmux":
        data = tomllib.loads((repo / "vendor-manifest/plugins.toml").read_text())
        head = "| Plugin | Zweck | Stand | Option |\n| --- | --- | --- | --- |"
        body = []
        for name, entry in data.items():
            if name == "meta":
                continue
            sha = entry.get("last_synced_commit", "")[:7]
            stand = f"`{sha}` ({entry['last_synced_date']})" if sha else "noch nicht eingebunden"
            body.append(f"| {name} | {entry['purpose']} | {stand} | `{entry['option']}` (Standard: aus) |")
        return "tmux-Plugins (`vendor-manifest/plugins.toml`, optional)", head, body
    if module == "yazi":
        data = tomllib.loads((repo / "package.toml").read_text())
        head = "| Flavor | Revision |\n| --- | --- |"
        body = [f"| {d['use']} | `{d['rev']}` |" for d in data.get("flavor", {}).get("deps", [])]
        return "Yazi-Flavor (`package.toml`)", head, body
    if module == "zsh":
        pkgbuild = (HUB / "packages/aco-arch-dotfiles-oh-my-zsh/PKGBUILD").read_text()
        commit = re.search(r"_omz_commit=(\w+)", pkgbuild).group(1)[:7]
        head = "| Bestandteil | Quelle | Stand |\n| --- | --- | --- |"
        body = [f"| Oh My Zsh | Paket `aco-arch-dotfiles-oh-my-zsh` (gepinnt) | Commit `{commit}` |"]
        return "Mitgelieferte Laufzeit", head, body
    return None


def render(module, root):
    repo = root / MODULES[module]
    depends, optdepends = parse_pkgbuild(repo / "packaging/arch/PKGBUILD")
    name = TITLE[module]
    out = [f"<!-- GENERATED by scripts/gen-design.py (aco-arch-dotfiles) – do not edit by hand. -->", "",
           f"# Aufbau und Abhängigkeiten", "",
           f"Warum {name} so gebaut ist, was es von anderen ACO-Komponenten braucht, welche Bibliotheken es nutzt und mit welchen Versionen es getestet wurde.", "",
           "## Warum so gebaut", ""]
    out += [f"- {line}" for line in WHY[module]] + [""]

    uses = [(o, w) for m, o, w in USES if m == module]
    used_by = [(m, w) for m, o, w in USES if o == module]
    out += ["## Was diese Konfiguration von anderen braucht", ""]
    if uses:
        out += ["| Komponente | Wofür |", "| --- | --- |"]
        out += [f"| [{TITLE[o]}]({DOCS.format(MODULES[o])}) | {w} |" for o, w in uses]
    else:
        out += ["Nichts – diese Konfiguration steht für sich."]
    out += ["", "## Wer diese Konfiguration braucht", ""]
    if used_by:
        out += ["| Komponente | Wofür |", "| --- | --- |"]
        out += [f"| [{TITLE[m]}]({DOCS.format(MODULES[m])}) | {w} |" for m, w in used_by]
    else:
        out += ["Keine andere Komponente setzt sie voraus."]

    out += ["", "## Pakete und Bibliotheken", "",
            "Aus dem `PKGBUILD` dieses Repositories; „Getestet mit“ ist die installierte Version auf dem Entwicklungsrechner "
            f"(Arch Linux, Stand {date.today().isoformat()}).", "",
            "| Paket | Mindestversion | Getestet mit | Wofür |", "| --- | --- | --- | --- |"]
    for dep in depends:
        pkg, minimum, _ = split_dep(dep)
        if pkg == "aco-arch-dotfiles-core":
            why = "Befehl `aco`, Aktivierung und Synchronisation"
        elif pkg.startswith("aco-arch-dotfiles-"):
            mod = {"gtk-3.0": "gtk-3.0", "gtk-4.0": "gtk-4.0"}.get(pkg.removeprefix("aco-arch-dotfiles-"), pkg.removeprefix("aco-arch-dotfiles-"))
            why = f"ACO-Komponente {TITLE.get(mod, mod)}"
        else:
            why = REASON.get(pkg, "")
        out.append(f"| `{pkg}` | {'≥ ' + minimum.lstrip('>=') if minimum else '–'} | {installed(pkg) or '–'} | {why} |")
    if optdepends:
        out += ["", "Optional:", ""]
        for dep in optdepends:
            pkg, _, note = split_dep(dep)
            out.append(f"- `{pkg}` – {note or REASON.get(pkg, '')}")

    extra = vendored(root, module)
    if extra:
        title, head, body = extra
        out += ["", f"## {title}", "", head] + body

    if module in NOTES:
        out += ["", "## Hinweise", ""] + [f"- {n}" for n in NOTES[module]]
    out += ["", SHARED.rstrip(), ""]
    return "\n".join(out)


def ensure_index(docs):
    """Register guide.md/design.md in the start page (card + first toctree) if missing."""
    index = docs / "index.md"
    text = index.read_text()
    cards = {"guide": ("Anleitung", "Alltag, Einstellungen im Detail, Fehlersuche."),
             "design": ("Aufbau & Abhängigkeiten", "Warum so gebaut, benötigte Pakete, Bibliotheken und Versionen.")}
    for page, (title, blurb) in cards.items():
        if not (docs / f"{page}.md").exists() or re.search(rf"^{page}$", text, re.M):
            continue
        card = f":::{{grid-item-card}} {title}\n:link: {page}\n:link-type: doc\n\n{blurb}\n:::\n\n"
        if f":link: {page}\n" not in text and ":::{grid-item-card}" in text:
            text = text.replace(":::{grid-item-card}", card + ":::{grid-item-card}", 1)
        text = re.sub(r"(```\{toctree\}\n(?::[^\n]*\n)*\n)", rf"\1{page}\n", text, count=1)
    index.write_text(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=HUB.parent / "layout")
    args = parser.parse_args()
    bad = 0
    for module in MODULES:
        docs = args.root / MODULES[module] / "docs"
        text = render(module, args.root)
        target = docs / "design.md"
        target.write_text(text)
        ensure_index(docs)
        print("wrote", target)
    return bad


if __name__ == "__main__":
    sys.exit(main())

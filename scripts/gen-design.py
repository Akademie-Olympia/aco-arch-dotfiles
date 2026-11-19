#!/usr/bin/env python3
"""Generate the "Design and dependencies" page of every component.

    python3 scripts/gen-design.py [--root DIR]

Pages of the large components go to <repo>/docs/design.md; the small ones are documented in
the shared aco-docs repository and go to aco-docs/docs/<page>/design.md.

Facts come from the sources, not from memory: package dependencies from each
packaging/arch/PKGBUILD, vendored plugins from plugins.lock (Neovim),
vendor-manifest/plugins.toml (tmux), package.toml (Yazi) and the Oh My Zsh pin of
the hub. "Tested with" versions come from the local pacman database, so run the
script on an up-to-date system. The reasoning ("Why it is built this way") is curated above.
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
# Small components are documented in the shared aco-docs repository: module -> page directory.
SHARED_DOCS = {"foot": "foot", "fuzzel": "fuzzel", "gtk-3.0": "gtk3", "gtk-4.0": "gtk4", "libfm": "libfm",
               "pcmanfm": "pcmanfm", "wallpaper": "wallpaper", "waybar": "waybar", "yazi": "yazi"}
TITLE = {"gtk-3.0": "GTK 3", "gtk-4.0": "GTK 4", "hypr": "Hyprland", "nvim": "Neovim", "pcmanfm": "PCManFM",
         "libfm": "libfm", "zsh": "Zsh", "tmux": "tmux", "vim": "Vim", "yazi": "Yazi", "foot": "Foot",
         "kitty": "Kitty", "ghostty": "Ghostty", "fuzzel": "Fuzzel", "waybar": "Waybar", "wallpaper": "Wallpaper"}
DOCS = "https://{}.readthedocs.io/en/latest/"


def site(module):
    """Public URL of a module's documentation."""
    if module in SHARED_DOCS:
        return DOCS.format("aco-docs") + SHARED_DOCS[module] + "/"
    return DOCS.format(MODULES[module])


# Why each upstream package is needed (shared wording).
REASON = {
    "hyprland": "Wayland compositor; the configuration is Lua (since 0.55) and needs at least 0.56",
    "hyprpaper": "Wallpaper daemon, controlled by the wallpaper command over IPC",
    "hyprlock": "Screen lock (`Super + L`, power menu)",
    "hypridle": "Idle detection (lock/suspend)",
    "xdg-desktop-portal-hyprland": "Screen sharing and screenshot portal for Wayland programs",
    "xdg-desktop-portal-gtk": "File chooser and settings portal (dark preference) for Wayland programs",
    "wl-clipboard": "`wl-copy`/`wl-paste` for the clipboard (screenshots, scripts)",
    "grim": "Screen capture", "slurp": "Region selection for screenshots",
    "satty": "Screenshot editor (annotate, save, copy)",
    "brightnessctl": "Brightness keys", "jq": "Parse JSON from `hyprctl` (scripts)",
    "util-linux": "Basic tools used by the scripts (`flock`, `getopt` …)", "procps-ng": "`pgrep`/`pkill` in the menu scripts",
    "psmisc": "`killall`, used to reload Waybar", "wireplumber": "`wpctl` for the volume keys and the Waybar volume module",
    "sudo": "Graphical password prompt through `askpass.sh`", "firefox": "Default browser (`Super + B`)",
    "fuzzel": "Application launcher and dmenu menu", "foot": "Terminal", "kitty": "Terminal", "ghostty": "Terminal",
    "zsh": "Login shell of the terminals", "tmux": "Terminal multiplexer",
    "ttf-jetbrains-mono-nerd": "Font with Nerd Font symbols (Waybar, Yazi, Neovim, terminals, GTK)",
    "gtk3": "GTK 3 library (file manager, dialogs)", "gtk4": "GTK 4 / libadwaita library",
    "adwaita-icon-theme": "`Adwaita` icon set", "libfm": "File operations, trash, thumbnails",
    "pcmanfm": "Graphical file manager", "waybar": "Status bar",
    "gvfs": "Mounting and trash backend of PCManFM", "udisks2": "Mount and unmount drives",
    "ffmpegthumbnailer": "Video thumbnails in PCManFM",
    "networkmanager": "Network status (`network` module, `nmtui`)", "bluez-utils": "Bluetooth tools",
    "power-profiles-daemon": "Power profiles",
    "yazi": "Terminal file manager", "file": "File type detection for previews", "fd": "Fast file search (`z` in Yazi, Telescope)",
    "ripgrep": "Text search (Yazi, Neovim `<leader>fg`)", "fzf": "Fuzzy search (shell history, Yazi, tmux, Neovim)",
    "zoxide": "Jump to frequent folders (`j`, Yazi `Z`)", "poppler": "PDF preview", "imagemagick": "Image preview",
    "ffmpeg": "Video preview", "7zip": "Archive preview", "findutils": "`find` for the image search",
    "zsh-autosuggestions": "Suggestions from history", "zsh-syntax-highlighting": "Live colouring of the command line",
    "neovim": "Editor; needs at least 0.12 (native LSP and plugin APIs)", "vim": "Editor",
    "git": "Version control (Gitsigns, Fugitive, scripts)", "curl": "Downloads for Mason tools",
    "tar": "Unpack archives (Mason)", "gzip": "Unpack archives (Mason)", "unzip": "Unpack archives (Mason)",
    "bash": "Interpreter of the scripts", "base-devel": "Optional: compile Treesitter parsers",
    "nodejs": "Optional: language tools (LSP/formatters)", "npm": "Optional: Mason tools",
    "python-pip": "Optional: Python tools",
}
# Why each module is built the way it is (curated).
WHY = {
    "foot": ["Foot is the **lightweight** terminal next to Kitty and Ghostty: fast, low memory, Wayland only. That is why the configuration contains only font, colours and shell.",
             "Colours and font are identical to Kitty and Ghostty, so switching terminals changes nothing visible.",
             "Tabs and splits are missing on purpose – Hyprland and tmux handle that."],
    "kitty": ["Kitty is the **default terminal** of the desktop (`Super + Enter`): GPU accelerated, image protocol for Yazi previews, remote control.",
              "Transparency (`background_opacity 0.90`) and font match Foot and Ghostty; the login shell is fixed to `/usr/bin/zsh`."],
    "ghostty": ["Ghostty is the **modern alternative** with its own shell integration; the configuration keeps colours, font and shell identical to Kitty and Foot.",
                "`shell-integration-features = no-cursor` leaves the cursor style of the configuration untouched."],
    "fuzzel": ["One menu for everything: launcher, window switcher, power menu, wallpaper picker, monitor menu and the shortcut list all use `fuzzel --dmenu`. Every menu looks and behaves the same.",
               "Fuzzel starts in milliseconds and needs no toolkit – fitting for a desktop without animations."],
    "waybar": ["The bar shows **only what is permanent**: workspaces, clock, volume, battery, power. Launching programs and switching windows live on shortcuts and in the Fuzzel menu.",
               "It attaches to the compositor through the Hyprland IPC (`hyprland/workspaces`) and uses Hyprland's scripts for the power actions."],
    "wallpaper": ["Hyprpaper only knows one image per instruction; the command adds **state** (default + overrides), folder search, a menu and restoring the assignment when a monitor is plugged in.",
                  "The state lives outside the configuration (`~/.local/state`) so updates never overwrite it; images are not part of the package (copyright)."],
    "hypr": ["Responsive instead of pretty: no animations, blur, shadows or gaps – maximum screen space.",
             "Several monitors are the normal case: focus and window jumps, window slots (`Super + F1…F4`), workspace swap, a monitor tool with profiles; new monitors arrange themselves to the right.",
             "The configuration is **Lua**; `scripts/gen-docs.py` generates the key list straight from it so documentation and bindings cannot drift apart.",
             "It pulls the other desktop packages (terminal, menu, bar, wallpaper, tmux, Yazi, PCManFM, browser) in as dependencies so an installation works immediately."],
    "tmux": ["Defaults are preserved; there is no global `unbind-key -a`. Plugins are **vendored and off** until you enable them.",
             "Capabilities (terminal, clipboard, OSC 52, symbols) are **detected**, not assumed – SSH is an equal environment.",
             "See [Philosophy](philosophy) and [Architecture](architecture) for the full rationale."],
    "vim": ["Vim is the **lean fallback** (servers, emergencies, `sudo vim`): one `vimrc`, no plugin manager.",
            "Leader (`Space`) and key layout match Neovim so muscle memory works in both editors."],
    "nvim": ["An IDE that starts **offline and reproducibly**: every plugin lives in the repository (`pack/vendor`), pinned in `plugins.lock`; nothing is downloaded on first start.",
             "Native LSP and a modular layout instead of large plugin frameworks; tools (language servers, formatters) are fetched by Mason on demand.",
             "See [Architecture](architecture) and [Plugins](plugins) for details and the update procedure."],
    "zsh": ["Oh My Zsh is **pinned to one commit** and shipped as its own package (`aco-arch-dotfiles-oh-my-zsh`); nothing is cloned with `git` at runtime.",
            "Autosuggestions and syntax highlighting come as Arch packages, not plugin clones – updates go through pacman.",
            "Small, clear daily commands: `y` (Yazi with directory change), `j` (zoxide), `tm`, `nv`/`v`, `wp`."],
    "yazi": ["Complements PCManFM for the keyboard: navigate quickly, preview, change the shell directory (`y`).",
             "The colour flavor ships in the package, pinned in `package.toml` – no download on first start."],
    "gtk-3.0": ["GTK programs should not fall out of style. `settings.ini` sets behaviour, `gtk.css` the colours; the theme stays `Adwaita-dark` so the layout stays familiar."],
    "gtk-4.0": ["GTK 4/libadwaita largely ignores theme names and reads named colours – so `gtk.css` sets exactly those and nothing beyond."],
    "libfm": ["The behaviour of the file manager (trash, terminal, thumbnails) is separate from its looks: libfm decides **what**, PCManFM **how**."],
    "pcmanfm": ["The graphical file manager for mouse tasks (drives, drag & drop); Yazi handles keyboard work.",
                "Behaviour comes from libfm, appearance from GTK 3 – both are dependencies of this package. `gvfs` and `udisks2` provide mounting."],
}
# Runtime relations between modules: (module, other, why). Rendered in both directions.
USES = [
    ("hypr", "kitty", "Default terminal (`Super + Enter`), also for `kitty -e yazi` and `kitty -e tmux`"),
    ("hypr", "fuzzel", "Launcher and all menu scripts (`powermenu.sh`, `windowswitcher.sh`, `askpass.sh`)"),
    ("hypr", "waybar", "Started with the session (`Super + Shift + B` reloads it)"),
    ("hypr", "wallpaper", "Backgrounds at start and on `monitor.added`; `Super + Shift + W`"),
    ("hypr", "tmux", "`Super + Shift + Enter` opens Kitty with the tmux session `main`"),
    ("hypr", "yazi", "`Super + Y` opens Yazi in a terminal"),
    ("hypr", "pcmanfm", "`Super + E` opens the graphical file manager"),
    ("waybar", "hypr", "Workspaces through the Hyprland IPC; the power menu calls `powermenu.sh`, `hyprlock` and `hyprctl`"),
    ("wallpaper", "hypr", "`hyprctl` and `hyprpaper`; the session calls `wallpaper apply` at start and on plug-in"),
    ("wallpaper", "fuzzel", "Selection menu (`wallpaper` without arguments)"),
    ("fuzzel", "kitty", "`terminal=kitty -e` for programs that need a terminal"),
    ("libfm", "kitty", "`terminal=kitty` for “run in terminal”"),
    ("pcmanfm", "libfm", "File operations, trash, side panel"),
    ("pcmanfm", "gtk-3.0", "Colours and font"),
    ("kitty", "zsh", "Login shell `/usr/bin/zsh`"),
    ("ghostty", "zsh", "Login shell `/usr/bin/zsh`"),
    ("foot", "zsh", "Login shell `/usr/bin/zsh`"),
    ("yazi", "zsh", "The `y` command (change directory on quit) lives in `aliases.zsh`"),
    ("zsh", "yazi", "`y` starts Yazi"),
    ("zsh", "tmux", "`tm` opens the session `main`"),
    ("zsh", "nvim", "`nv` / `EDITOR=nvim`"),
    ("zsh", "vim", "`v`"),
    ("zsh", "wallpaper", "`wp` is the wallpaper command"),
    ("zsh", "hypr", "`SUDO_ASKPASS` points to `askpass.sh` (graphical password prompt)"),
    ("tmux", "kitty", "Clipboard over OSC 52 works in Kitty, Ghostty and Foot"),
    ("vim", "nvim", "Shared leader key and key layout"),
    ("nvim", "vim", "Shared leader key and key layout"),
    ("gtk-4.0", "gtk-3.0", "Same palette and the same `settings.ini`; different CSS names"),
    ("gtk-3.0", "gtk-4.0", "Same palette and the same `settings.ini`; different CSS names"),
]
NOTES = {
    "waybar": ["`networkmanager`, `bluez-utils` and `power-profiles-daemon` are **optional**: the shipped `config.jsonc` has no module for them; install them when you add the matching module (see the [guide](guide)).",
               "The bar needs `hyprland` (workspace module, `hyprctl`) and `hyprlock` (power menu); it does not depend on the ACO Hyprland package because that package depends on the bar."],
    "hypr": ["`brightnessctl`, `wl-clipboard`, `grim`, `slurp` and `satty` are only used by the scripts (`screenshot.sh`) and shortcuts – without them exactly the matching key is missing.",
             "`Super + Shift + D` opens `monitors.sh`, which manages monitors and writes `monitors.local.lua` – that file lives outside the package.",
             "Notifications from the scripts use Hyprland's built-in `hyprctl notify`; no notification daemon is required."],
    "wallpaper": ["`hyprctl` ships with `hyprland`, which is a declared dependency; the command only makes sense inside a Hyprland session."],
    "pcmanfm": ["`gvfs` and `udisks2` are hard dependencies because `mount_on_startup`/`mount_removable` need them; `ffmpegthumbnailer` (optional) adds video thumbnails."],
}
SHARED = """## Shared foundations

These rules apply to **every** ACO component:

- **One repository per component**, with its own `PKGBUILD` and CI. Each configuration can be installed, tested and developed on its own;
  after a push the central registry builds the signed package ([packaging overview](https://aco-arch-dotfiles.readthedocs.io/en/latest/arch-package/)).
- **Pacman is the only updater.** No git pull at runtime; `aco` only merges new defaults with your changes (`.pacnew`).
- **Your copy, not the package's.** `~/.config/<module>` points to `~/.local/share/arch-dotfiles/config/<module>/`; the package stays untouched in `/usr/share/arch-dotfiles/<module>/`.
- **One palette, one font:** Catppuccin Mocha and JetBrainsMono Nerd Font in every component so nothing falls out of style.
- **The core** `aco-arch-dotfiles-core` (the `aco` command, activation, backups, synchronisation) is a dependency of every package.
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
        head = "| Plugin | Source | Pinned commit | Loaded |\n| --- | --- | --- | --- |"
        body = [f"| {n} | <{u}> | `{s}` | {'at startup' if t == 'start' else 'on demand'} |" for n, u, s, t in rows]
        return "Neovim plugins (`plugins.lock`, vendored under `pack/vendor/`)", head, body
    if module == "tmux":
        data = tomllib.loads((repo / "vendor-manifest/plugins.toml").read_text())
        head = "| Plugin | Purpose | Pinned | Option |\n| --- | --- | --- | --- |"
        body = []
        for name, entry in data.items():
            if name == "meta":
                continue
            sha = entry.get("last_synced_commit", "")[:7]
            stand = f"`{sha}` ({entry['last_synced_date']})" if sha else "not vendored yet"
            body.append(f"| {name} | {entry['purpose']} | {stand} | `{entry['option']}` (default: off) |")
        return "tmux plugins (`vendor-manifest/plugins.toml`, optional)", head, body
    if module == "yazi":
        data = tomllib.loads((repo / "package.toml").read_text())
        head = "| Flavor | Revision |\n| --- | --- |"
        body = [f"| {d['use']} | `{d['rev']}` |" for d in data.get("flavor", {}).get("deps", [])]
        return "Yazi flavor (`package.toml`)", head, body
    if module == "zsh":
        pkgbuild = (HUB / "packages/aco-arch-dotfiles-oh-my-zsh/PKGBUILD").read_text()
        commit = re.search(r"_omz_commit=(\w+)", pkgbuild).group(1)[:7]
        head = "| Component | Source | Pinned |\n| --- | --- | --- |"
        body = [f"| Oh My Zsh | Package `aco-arch-dotfiles-oh-my-zsh` | Commit `{commit}` |"]
        return "Shipped runtime", head, body
    return None


def render(module, root):
    repo = root / MODULES[module]
    depends, optdepends = parse_pkgbuild(repo / "packaging/arch/PKGBUILD")
    name = TITLE[module]
    out = [f"<!-- GENERATED by scripts/gen-design.py (aco-arch-dotfiles) - do not edit by hand. -->", "",
           "# Design and dependencies", "",
           f"Why {name} is built the way it is, what it needs from other ACO components, which libraries it uses and which versions it was tested with.", "",
           "## Why it is built this way", ""]
    out += [f"- {line}" for line in WHY[module]] + [""]

    uses = [(o, w) for m, o, w in USES if m == module]
    used_by = [(m, w) for m, o, w in USES if o == module]
    out += ["## What this configuration needs from others", ""]
    if uses:
        out += ["| Component | Why |", "| --- | --- |"]
        out += [f"| [{TITLE[o]}]({site(o)}) | {w} |" for o, w in uses]
    else:
        out += ["Nothing – this configuration stands on its own."]
    out += ["", "## Who needs this configuration", ""]
    if used_by:
        out += ["| Component | Why |", "| --- | --- |"]
        out += [f"| [{TITLE[m]}]({site(m)}) | {w} |" for m, w in used_by]
    else:
        out += ["No other component requires it."]

    out += ["", "## Packages and libraries", "",
            "From the `PKGBUILD` of this component; “Tested with” is the version installed on the development machine "
            f"(Arch Linux, as of {date.today().isoformat()}).", "",
            "| Package | Minimum | Tested with | Purpose |", "| --- | --- | --- | --- |"]
    for dep in depends:
        pkg, minimum, _ = split_dep(dep)
        if pkg == "aco-arch-dotfiles-core":
            why = "The `aco` command, activation and synchronisation"
        elif pkg.startswith("aco-arch-dotfiles-"):
            mod = {"gtk-3.0": "gtk-3.0", "gtk-4.0": "gtk-4.0"}.get(pkg.removeprefix("aco-arch-dotfiles-"), pkg.removeprefix("aco-arch-dotfiles-"))
            why = f"ACO component {TITLE.get(mod, mod)}"
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
        out += ["", "## Notes", ""] + [f"- {n}" for n in NOTES[module]]
    out += ["", SHARED.rstrip(), ""]
    return "\n".join(out)


def ensure_index(docs):
    """Register guide.md/design.md in the start page (card + first toctree) if missing."""
    index = docs / "index.md"
    text = index.read_text()
    cards = {"guide": ("Guide", "Daily use, settings in detail, troubleshooting."),
             "design": ("Design & dependencies", "Why it is built this way, required packages, libraries and versions.")}
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
        docs = (args.root / "aco-docs" / "docs" / SHARED_DOCS[module]) if module in SHARED_DOCS \
            else args.root / MODULES[module] / "docs"
        text = render(module, args.root)
        target = docs / "design.md"
        target.write_text(text)
        if module not in SHARED_DOCS:
            ensure_index(docs)
        print("wrote", target)
    return bad


if __name__ == "__main__":
    sys.exit(main())

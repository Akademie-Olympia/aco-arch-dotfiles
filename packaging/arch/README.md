# ACO Arch Dotfiles: installation, development and registry

## Quick install

As a normal Arch user, not as root:

```bash
curl -fsSL https://raw.githubusercontent.com/Akademie-Olympia/aco-arch-dotfiles/main/install.sh | bash
# Or only selected packages:
curl -fsSL https://raw.githubusercontent.com/Akademie-Olympia/aco-arch-dotfiles/main/install.sh | bash -s -- nvim tmux
```

Alternatively download the script, read it and run `bash install.sh`.
Options: `--help`, `--dry-run`, `--yes`, `--no-activate`, `--no-sync`.
Existing differing registry settings are not overwritten (the one exception is the known pre-organisation file, which is replaced after a backup).

The installer downloads the public key and compares its fingerprint with the hard-coded value before importing it into pacman and signing it
locally. It enables package **and** database signature checks:

```ini
[arch-dotfiles]
SigLevel = Required DatabaseRequired
Server = https://github.com/Akademie-Olympia/aco-arch-dotfiles/releases/download/repo
```

The file lives in `/etc/pacman.d/arch-dotfiles.conf`; an idempotent include is added to `/etc/pacman.conf`. A manually added section of the
same name must be reviewed first and replaced by this include. You should also verify the publicly known fingerprint independently.
A compromised remote installer would be dangerous even with signature checks; only run source code you trust.

## What gets installed?

16 independently maintained configurations, one shared management package, an Oh My Zsh runtime package and an optional all-in-one meta package.
The configurations live in their own repositories listed in `repositories.json`; their `packaging/arch/PKGBUILD` determines the dependencies.
For example `aco-arch-dotfiles-nvim` does not install the whole Hyprland desktop, whereas desktop configurations explicitly declare the other
desktop components they need as dependencies. Every component's “Design and dependencies” page lists them with reasons and tested versions.

Pacman owns the defaults under `/usr/share/arch-dotfiles`, programs under `/usr/bin` and user units under `/usr/lib/systemd/user`.
Neither package scriptlets nor root hooks touch home directories.

## Activation and updates

`aco-arch-dotfiles-config activate [module ...]` backs up existing settings and creates user-owned copies in
`${XDG_DATA_HOME:-~/.local/share}/arch-dotfiles/config`. They are linked to `~/.config/<module>`; Zsh, tmux and Vim get their home entry points.
Backups and the activation journal live in `${XDG_STATE_HOME:-~/.local/state}/arch-dotfiles`. Local monitor rules and tmux `local*.conf` are kept.
`XDG_CONFIG_HOME` must be `~/.config`; custom absolute data/state paths are supported.

The installer enables `aco-arch-dotfiles-sync.timer` for the calling user:

```bash
sudo pacman -Syu                    # install new configuration packages
aco sync                            # optional: immediately instead of waiting for the timer
```

The timer runs about every two minutes and synchronises only active modules. Unchanged files are replaced; your own changes stay with the new
defaults next to them as `.pacnew`. Reload the application after a merge. Other users have to activate and enable their timer themselves.
There is no automatic restart of the graphical session. Without the timer, `aco-arch-dotfiles-config update` is an explicit separate step.

## Develop and publish

```bash
bash scripts/clone-repos.sh
cd ../aco-nvim
# edit, commit and push to main
git push origin main
```

The central workflow `packages.yml` clones the `main` state of all repositories and checks for changes on central `main` pushes, on dispatch from a
component and on manual starts. After a successful build and publish the next `pacman -Syu` contains the new configurations. A push alone does not
mean a package is available; the status is visible in the central Actions workflow.

```bash
gh workflow run packages.yml -R Akademie-Olympia/aco-arch-dotfiles
```

Packages automatically get a version of the form `0.3.0.r<source-commit-count>.g<commit>-<hub-commit-count>`. Configuration changes therefore need
no manual version bump. A hub commit additionally raises the packaging revision so that central export changes also produce new packages.
Do not force-push `main`: the commit count is a monotonically increasing version component. After an intentional history rewrite the base version
in the recipe must be raised.

Unchanged sources are reused from already published artifacts. The publisher reconciles packages published in the meantime and uses their original
bytes so database checksums match. Newer existing package versions are never downgraded by older builds. Old package files stay available for
clients with cached databases. `sources.json` in the release documents the source commits of the build. While the separate database/signature
files are swapped a download can fail; repeat `pacman -Syu` later and never disable signature checking.

## Local builds

```bash
sudo pacman -Syu --needed base-devel git python
bash scripts/clone-repos.sh
bash packaging/arch/build.sh aco-arch-dotfiles-nvim
bash packaging/arch/build.sh all
python3 packaging/arch/check-artifacts.py
```

Run as a normal user. Results land in `packaging/arch/build/<package>/`. Add new files in the source repository with `git add` before building:
only git-tracked sources are exported. Git metadata, CI files, package recipes, private wallpapers, monitor overrides and tmux overrides are not
shipped. Plugin licences are preserved. Oh My Zsh is built from a pinned commit with a fixed SHA-256. Builds install nothing; pacman resolves runtime
dependencies at installation. Install locally built internal dependencies together with `pacman -U` when they are not already available from the registry.

`ARCH_DOTFILES_SOURCE_ROOT` overrides the folder containing the component repositories; by default the neighbouring directories of the hub checkout
are used. `scripts/clone-repos.sh --update` fast-forwards only clean `main` checkouts. No local changes are overwritten.

## Signing key and CI

Only the hub repository needs the `pacman-repository` environment:

- Secret `PACMAN_SIGNING_KEY`: armoured private package signing key.
- Optional secret `PACMAN_SIGNING_PASSPHRASE`.
- Variable `PACMAN_SIGNING_FINGERPRINT`: the full fingerprint.

Component repositories receive **no private signing key and no cross-repository push token** – only the organisation secret
`DOTFILES_DISPATCH_TOKEN` (Actions read/write on the hub) to request a build. Pull requests never publish. Keep a protected backup of the private
key outside GitHub (for example as an attachment in a password manager); losing it or rotating it requires a planned pacman key changeover.

GitHub Releases are the download server, not GHCR/GitHub Packages. The repository files are public; private source repositories would need separate
CI authentication and are not intended with this setup.

## Migration and removal

Migrate from the former local monolithic package cleanly first:

```bash
aco-arch-dotfiles-config deactivate
sudo pacman -R aco-arch-dotfiles
# then run the new installer
```

No forced `--overwrite '*'` installations. Backups and user copies are preserved. Former subtree working copies of this restructuring are backed up
locally, not published on GitHub.

Remove a single package:

```bash
aco-arch-dotfiles-config deactivate nvim
sudo pacman -Rns aco-arch-dotfiles-nvim
```

If the meta package is installed, remove it first with `pacman -R aco-arch-dotfiles` so individual dependencies can be removed. Complete removal:

```bash
systemctl --user disable --now aco-arch-dotfiles-sync.timer
aco-arch-dotfiles-config deactivate
sudo pacman -Rns aco-arch-dotfiles
```

`-Rns` removes only unneeded packages that were installed as dependencies. Your copies, backups, images and previously explicitly installed
applications are kept. Modified activation links are not overwritten.

## Tests

```bash
python3 -B -m unittest discover -s packaging/arch/tests -v
```

The tests install nothing and use temporary homes. They expect the component repositories next to the hub (or `ARCH_DOTFILES_SOURCE_ROOT`).

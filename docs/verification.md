# Verifying the installation and avoiding mistakes

## On an installed machine

```bash
pacman -Q | grep '^aco-arch-dotfiles'
pacman -Qkk $(pacman -Qq | grep '^aco-arch-dotfiles')
aco-arch-dotfiles-config status
systemctl --user status aco-arch-dotfiles-sync.timer
systemctl --user status aco-arch-dotfiles-sync.service
```

A complete installation has 19 packages; a deliberately selective one has fewer. `-Qkk` checks the package files under `/usr`, not your editable
copies. A successful oneshot sync service may show up as `inactive (dead)`; what matters is exit code 0 and an active timer.

```bash
aco sync
find "${XDG_DATA_HOME:-$HOME/.local/share}/arch-dotfiles/config" -name '*.pacnew*'
journalctl --user -u aco-arch-dotfiles-sync.service -n 30 --no-pager
```

Your own changes are not merged automatically. Review `.pacnew` files and only then reload the affected application. Never edit the `/usr`
defaults, run activation as root, or hide conflicts with `--overwrite '*'`. An existing manual pacman repository section with the same name
must be reviewed before you use the installer again (the installer replaces only the known pre-organisation file, with a backup).

## Keeping the registry fresh

The registry is built from the hub repository. After a component's check succeeds, a push to `main` requests the central build directly.
In addition `aco-arch-dotfiles-registry-kick` compares the published `sources.json` (all component commits plus the hub) with `main` of every
source and starts the central `Arch packages` workflow exactly when a package is behind `main`. The dispatch is only a request — building,
signing and publishing is done solely by the checked hub workflow.

```bash
aco-arch-dotfiles-registry-kick          # compares, dispatches only on drift
systemctl --user status aco-arch-dotfiles-registry-kick.timer
journalctl --user -u aco-arch-dotfiles-registry-kick.service -n 30 --no-pager
```

Without `gh`, or without `gh auth login`, the script exits with a hint and status 0 — responsibility then lies with the dispatch after a push
to `main` (`Arch packages` workflow). “GitHub not reachable” is a delay, retried on the next timer tick, not an error.

### From push to package

1. `git push origin main` in a component repository starts its `Package safety` workflow. Pull requests are checked too but do not publish.
2. Only after a successful check does the workflow request the hub's `Arch packages` workflow using the Actions secret
   `DOTFILES_DISPATCH_TOKEN`. The secret needs access to GitHub Actions in the hub; its value never belongs in git.
   A missing or invalid secret makes the dispatch job fail visibly.
3. The hub clones the components at `main`, checks and builds the packages, tests installation and updates in isolation and publishes signed
   packages and repository databases. A push to the hub starts the same workflow directly.
4. `sudo pacman -Syu` installs published updates. `aco sync` then reconciles the user copy; the optional sync timer does that as well. Your
   changes are preserved; differing new defaults land next to them as `.pacnew` and need review.

The dispatch requests a build; it guarantees neither a successful build nor a fixed publication time. GitHub Actions and the signing
environment must be available. The registry timer is an additional way to retry, not a package updater.

## Automatic safety checks

- Every component repository checks its package recipe, shell/Python/TOML/JSONC/INI/XML syntax, entry points, module inventory and the isolated
  `/usr` payload on push and pull request. Git metadata and links escaping the package are forbidden.
- Repositories with a `.readthedocs.yaml` build their documentation with the same Python version and `sphinx-build -W --keep-going` before
  changes count as green.
- Central unit and documentation tests run before a registry build.
- Before **every publication of changed packages** a repository is built with a key created only for the test. Pacman must reject missing
  signatures and be able to install all 19 packages into a temporary root.
- Before that, full dependency resolution is checked offline against the existing official Arch sync databases. No programs are installed on the
  developer machine for this test.
- Activation, editor/shell/tmux start, conflict-free updates, `.pacnew` and restoring the backups are tested in temporary homes.

```bash
python3 -B -m unittest discover -s packaging/arch/tests -v
python3 packaging/arch/check-component.py
bash packaging/arch/build.sh all
python3 packaging/arch/check-artifacts.py
python3 packaging/arch/smoke-install.py
```

The smoke test runs **without real root privileges** using `fakeroot`, its own pacman databases and its own homes. It needs the build tools, GnuPG
and current Arch sync databases. Install scriptlets are disabled in the temporary root; production scriptlets only print hints and never touch
home directories.

These tests do not replace a visual check in a real Wayland session. Monitors, graphics drivers, audio, Bluetooth, portals and personal services
are machine dependent. CI never starts or ends a running graphical user session.

## GitHub CLI for maintainers

The GitHub CLI must be permanently on `PATH`, not only in a temporary build folder. On Arch install it regularly with
`sudo pacman -Syu --needed github-cli`. Alternatively the official binary, verified against the release checksum, works from `~/.local/bin/gh`;
that manual installation is not updated by pacman.

```bash
command -v gh
gh --version
gh auth status
gh run list -R Akademie-Olympia/aco-arch-dotfiles --workflow packages.yml
```

Never commit tokens or private signing keys to issue/CI logs or git.

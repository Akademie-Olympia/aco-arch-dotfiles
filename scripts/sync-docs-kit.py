#!/usr/bin/env python3
"""Copy the shared docs kit (docs/_aco) into every component repository.

    python3 scripts/sync-docs-kit.py [--root DIR] [--check]

Components are looked up next to this repository (the layout created by
scripts/clone-repos.sh). With --check nothing is written; the exit status is 1
when a component is out of date, which CI can use to detect drift.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys

HUB = Path(__file__).resolve().parent.parent
KIT = HUB / "docs" / "_aco"
REQUIREMENTS = """sphinx>=8.0.0
furo>=2024.8.6
myst-parser>=4.0.0
sphinx-copybutton>=0.5.2
sphinx-design>=0.6.1
"""
READTHEDOCS = """version: 2

build:
  os: ubuntu-24.04
  tools:
    python: "3.12"

sphinx:
  configuration: docs/conf.py
  builder: dirhtml
  fail_on_warning: true

python:
  install:
    - requirements: docs/requirements.txt
"""


def kit_files():
    return sorted(p for p in KIT.rglob("*") if p.is_file() and "__pycache__" not in p.parts
                  and p.name != "README.md" or p == KIT / "README.md")


def wanted(repo):
    files = {Path("docs/_aco") / p.relative_to(KIT): p.read_bytes() for p in kit_files()}
    files[Path("docs/requirements.txt")] = REQUIREMENTS.encode()
    if not (repo / ".readthedocs.yaml").exists():
        files[Path(".readthedocs.yaml")] = READTHEDOCS.encode()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=HUB.parent)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    repositories = json.loads((HUB / "repositories.json").read_text())
    stale = []
    for module, full in sorted(repositories.items()):
        repo = args.root / full.split("/")[1]
        if not repo.is_dir():
            print(f"skip {module}: {repo} is not cloned")
            continue
        for relative, content in wanted(repo).items():
            target = repo / relative
            if target.exists() and target.read_bytes() == content:
                continue
            stale.append(f"{repo.name}/{relative}")
            if not args.check:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
        # Remove kit files that no longer exist in the hub.
        installed = repo / "docs" / "_aco"
        if installed.is_dir():
            current = {Path("docs/_aco") / p.relative_to(KIT) for p in kit_files()}
            for path in sorted(installed.rglob("*")):
                relative = path.relative_to(repo)
                if path.is_file() and relative not in current and "__pycache__" not in path.parts:
                    stale.append(f"{repo.name}/{relative} (obsolete)")
                    if not args.check:
                        path.unlink()
    for item in stale:
        print(("outdated: " if args.check else "updated: ") + item)
    if args.check and stale:
        return 1
    print("docs kit is current" if not stale else f"{len(stale)} file(s) {'outdated' if args.check else 'written'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

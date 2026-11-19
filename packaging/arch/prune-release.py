#!/usr/bin/env python3
"""Select superseded package files in the published release for deletion.

Reads `gh release view repo --json assets` and the packages referenced by the
published database. Anything the database references is kept, as are the
newest KEEP versions of every package so a bad update can be rolled back.
Prints one asset name per line; deletion itself is done by the workflow.
"""
import json
import re
import sys
import tarfile

KEEP = 2
PACKAGE = re.compile(r"^(?P<name>.+)-(?P<version>[^-]+)-(?P<release>\d+)-(?P<arch>[^-]+)\.pkg\.tar\.zst$")


def referenced(database):
    """File names of every package the database points at."""
    names = set()
    with tarfile.open(database) as tar:
        for member in tar.getmembers():
            if member.name.endswith("/desc"):
                text = tar.extractfile(member).read().decode()
                match = re.search(r"%FILENAME%\n(.+)\n", text)
                if match:
                    names.add(match.group(1))
    return names


def select_deletions(assets, keep_files, keep=KEEP):
    packages = {}
    for name in assets:
        match = PACKAGE.match(name)
        if match:
            packages.setdefault(match["name"], []).append((int(match["release"]), name))
    delete = []
    for versions in packages.values():
        versions.sort()
        newest = {name for _, name in versions[-keep:]}
        for _, name in versions:
            if name not in newest and name not in keep_files:
                delete += [name, name + ".sig", name + ".source.sha256"]
    return [name for name in delete if name in set(assets)]


def main(argv):
    assets = [a["name"] for a in json.load(open(argv[1]))["assets"]]
    for name in select_deletions(assets, referenced(argv[2])):
        print(name)


if __name__ == "__main__":
    main(sys.argv)

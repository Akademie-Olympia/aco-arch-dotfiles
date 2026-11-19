import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("prune", Path(__file__).resolve().parents[1] / "prune-release.py")
prune = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prune)


def files(name, release):
    base = f"{name}-0.3.0.r1.gabc-{release}-any.pkg.tar.zst"
    return [base, base + ".sig", base + ".source.sha256"]


class PruneTest(unittest.TestCase):
    def test_keeps_newest_two_and_referenced(self):
        assets = sum((files("aco-arch-dotfiles-nvim", r) for r in (50, 51, 52, 53)), []) + ["sources.json"]
        kept = {files("aco-arch-dotfiles-nvim", 50)[0]}
        deleted = prune.select_deletions(assets, kept)
        self.assertEqual(deleted, files("aco-arch-dotfiles-nvim", 51))

    def test_never_touches_databases_or_keys(self):
        assets = ["arch-dotfiles.db", "arch-dotfiles-key.asc", "sources.json"] + files("a-b", 1)
        self.assertEqual(prune.select_deletions(assets, set()), [])

    def test_packages_are_independent(self):
        assets = files("aco-arch-dotfiles-a", 5) + files("aco-arch-dotfiles-b", 1)
        self.assertEqual(prune.select_deletions(assets, set()), [])


if __name__ == "__main__":
    unittest.main()

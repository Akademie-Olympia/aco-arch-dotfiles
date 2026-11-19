"""Sphinx configuration for the ACO hub. Shared settings live in docs/_aco."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from _aco.base import configure  # noqa: E402

configure(globals(), slug="aco-arch-dotfiles", title="ACO Arch Dotfiles", language="de")

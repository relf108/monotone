"""Factory for creating Dependency objects."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from args import Lang, args
from colour import err, warn
from langs.python import Python

if TYPE_CHECKING:
    from dependency import Dependency

COMMENT_CHARS = ("--", "#", "//")


class DependencyFactory:
    """Factory for creating Dependency objects."""

    def __init__(self: DependencyFactory) -> None:
        """Initialize the DependencyFactory."""
        self.parent_dir, self._dependency_map = self._init_dependency_map()
        self.lang: Lang = args.lang

    def names(self: DependencyFactory, loaded_only: False) -> list[str]:
        """Return a list of dependency names."""
        if loaded_only:
            return [k for k, v in self._dependency_map.items() if v.loaded]
        return list(self._dependency_map.keys())

    def deps(self: DependencyFactory) -> list[Dependency]:
        """Return a list of dependency names."""
        return list(self._dependency_map.values())

    def map(self: DependencyFactory) -> dict[str, Dependency]:
        """Return a list of dependency names."""
        return self._dependency_map

    def get(self: DependencyFactory, dependency_name: str) -> Dependency:
        """Return a Dependency object."""
        return self._dependency_map[dependency_name]

    def populate_dependency_map(
        self: DependencyFactory,
        parent_dir: Path,
        lib_name: str,
        dependency_map: dict[str, Dependency],
    ) -> Path:
        """Populate the dependency map with the given library name."""
        try:
            egg_path = yield parent_dir.rglob(f"{lib_name}.egg*")
            parent = Path(egg_path[0]).parent
            dependency_map[lib_name] = Python(
                parent,
                lib_name,
            )
        except IndexError:
            dependency_map.pop(lib_name)
            warn(f"warning: could not find {lib_name} in {parent_dir}")

        return parent

    def _init_dependency_map(
        self: DependencyFactory,
    ) -> tuple[Path, dict[str, Dependency]]:
        """Read monotone_deps.txt and return a dictionary of dependency names to paths."""
        mono_deps = Path(f"{Path.cwd()}/monotone_deps.txt")
        if not Path.exists(mono_deps):
            err(f"ERROR: Could not find monotone_deps.txt at {mono_deps}")
            sys.exit(1)

        parent_dir: Path = mono_deps.parent
        dependency_map: dict[str, Dependency] = {}

        with Path.open(mono_deps, encoding="utf-8") as mono_dep_file:
            lines = mono_dep_file.readlines()
            for line in [x.strip() for x in lines]:
                if line.startswith(COMMENT_CHARS) or len(line) == 0:
                    continue

                split = line.split("==")

                if len(split) == len("=="):
                    path = split[1]
                    if "$HOME" in path:
                        path = path.replace("$HOME", str(Path.home()))

                    if split[0] == "PARENT_DIR":
                        parent_dir = Path(path)
                        continue

                    dependency_map[split[0]] = Python(Path(path), split[0])
                    continue

                dependency_map[line] = Python(Path(parent_dir), line)

        names = [k for k, v in dependency_map.items() if v.path == parent_dir]
        for lib_name in names:
            parent_dir = self.populate_dependency_map(
                parent_dir,
                lib_name,
                dependency_map,
            )

        return parent_dir, dependency_map

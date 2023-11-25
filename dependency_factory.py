"""Factory for creating Dependency objects"""

import glob
import sys
from pathlib import Path

from args import Lang, args
from colour import err, warn
from dependency import Dependency
from langs.python import Python

COMMENT_CHARS = tuple(["--", "#", "//"])

class DependencyFactory:
    """Factory for creating Dependency objects"""

    def __init__(self):
        self.parent_dir, self._dependency_map = self._init_dependency_map()
        self.lang: Lang = args.lang

    def names(self) -> list[str]:
        """Return a list of dependency names"""
        return list(self._dependency_map.keys())

    def deps(self) -> list[Dependency]:
        """Return a list of dependency names"""
        return list(self._dependency_map.values())

    def map(self) -> dict[str, Dependency]:
        """Return a list of dependency names"""
        return self._dependency_map

    def get(self, dependency_name: str) -> Dependency:
        """Return a Dependency object"""
        return self._dependency_map[dependency_name]

    def _init_dependency_map(self) -> tuple[Path, dict[str, Dependency]]:
        """Read monotone_deps.txt and return a dictionary\
        of dependency names to paths."""

        mono_deps = Path(f"{Path.cwd()}/monotone_deps.txt")
        if not Path.exists(mono_deps):
            err(f"ERROR: Could not find monotone_deps.txt at {mono_deps}")
            sys.exit(1)

        parent_dir: Path = mono_deps.parent
        dependency_map: dict[str, Dependency] = {}

        with open(mono_deps, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()

                if line.startswith(COMMENT_CHARS) or len(line) == 0:
                    continue

                split = line.split("==")

                if len(split) == 2:
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
            try:
                egg_path = glob.glob(f"{parent_dir}/**/{lib_name}.egg-info")
                parent = Path(egg_path[0]).parent
                dependency_map[lib_name] = Python(
                    parent,
                    lib_name,
                )
            except IndexError:
                dependency_map.pop(lib_name)
                warn(f"WARNING: Could not find {lib_name} in {parent_dir}")
                continue

        return parent_dir, dependency_map

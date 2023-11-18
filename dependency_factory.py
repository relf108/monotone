import glob
from pathlib import Path

from colour import err, warn
from dependency import Dependency


class DependencyFactory:
    def __init__(self):
        self.parent_dir, self._dependency_map = self._init_dependency_map()

    def names(self) -> list[str]:
        """Return a list of dependency names"""
        return list(self._dependency_map.keys())

    def map(self) -> dict[str, Dependency]:
        """Return a list of dependency names"""
        return self._dependency_map

    def get(self, dependency_name: str) -> Dependency:
        """Return a Dependency object"""
        return self._dependency_map[dependency_name]

    def _init_dependency_map(self) -> tuple[Path, dict[str, Dependency]]:
        """Read monotone_deps.txt and return a dictionary of dependency names to paths."""

        mono_deps = Path(f"{Path.cwd()}/monotone_deps.txt")
        if not Path.exists(mono_deps):
            err(f"ERROR: Could not find monotone_deps.txt at {mono_deps}")
            exit(1)

        parent_dir: Path = mono_deps.parent
        dependency_map: dict[str, Dependency] = {}

        with open(mono_deps, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()

                if line.startswith("--") or len(line) == 0:
                    continue

                split = line.split("==")

                if len(split) == 2:
                    path = split[1]
                    if "$HOME" in path:
                        path = path.replace("$HOME", str(Path.home()))

                    if split[0] == "PARENT_DIR":
                        parent_dir = Path(path)
                        continue

                    dependency_map[split[0]] = Dependency(Path(path))
                    continue

                dependency_map[line] = Dependency(Path(parent_dir))

        for lib_name in [k for k, v in dependency_map.items() if v.path == parent_dir]:
            try:
                dependency_map[lib_name] = Dependency(
                    Path(glob.glob(f"{parent_dir}/**/{lib_name}.egg-info")[0])
                )
            except IndexError:
                dependency_map.pop(lib_name)
                warn(f"WARNING: Could not find {lib_name} in {parent_dir}")
                continue

        return parent_dir, dependency_map

from pathlib import Path
import glob


class DependencyFactory:
    def __init__(self):
        self._dependency_paths = self._init_dependency_paths()

    def _init_dependency_paths(self) -> dict[str, Path]:
        """Read monotone_deps.txt and return a dictionary of dependency names to paths."""

        deps = Path(f"{Path.cwd()}/monotone_deps.txt")
        if not Path.exists(deps):
            raise FileNotFoundError(f"Could not find monotone_deps.txt at {deps}")

        parent_dir: Path = deps.parent
        dependency_paths: dict[str, Path] = {}

        with open(deps, "r") as f:
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

                    dependency_paths[split[0]] = Path(path)
                    continue

                dependency_paths[line] = Path(parent_dir)

        for g_path in glob.glob(f"{parent_dir}/**/*.egg-info"):
            g_path = Path(g_path)

            if g_path.name.split(".")[0] not in dependency_paths.keys():
                continue

            dependency_paths[g_path.name] = g_path.parent

        return dependency_paths

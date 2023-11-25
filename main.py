""" Main entry point for the program. """

from colour import ok, warn
from dependency_factory import DependencyFactory

if __name__ == "__main__":
    dep_factory = DependencyFactory()

    for dep in dep_factory.deps():
        dep.load()

    loaded = dep_factory.names(loaded_only=True)
    failed = list(set(dep_factory.names()) ^ set(loaded))

    if len(failed) > 0:
        warn(f"Failed to install: {', '.join(failed)}")

    ok(f"Installed: {', '.join(loaded)}")

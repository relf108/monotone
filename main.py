""" Main entry point for the program. """
from time import perf_counter

from colour import ok
from dependency_factory import DependencyFactory


def main():
    """Main entry point for the program."""

    dep_factory = DependencyFactory()

    for dep in dep_factory.deps():
        dep.load()

    ok(dep_factory.names())


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    ok(f"Program executed in {end - start} seconds.")

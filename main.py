from time import perf_counter

from colour import ok
from dependency_factory import DependencyFactory


def main():
    dep_factory = DependencyFactory()
    ok(dep_factory.names())


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    ok(f"Program executed in {end - start} seconds.")

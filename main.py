from dependency_factory import DependencyFactory


def main():
    dep_factory = DependencyFactory()
    paths = dep_factory._dependency_paths
    print(paths)


if __name__ == "__main__":
    main()

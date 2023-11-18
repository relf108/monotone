class Colour:
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


def ok(text: str | list[str]):
    if isinstance(text, list):
        for line in text:
            print(f"{Colour.OKGREEN}{line}{Colour.ENDC}")
        return
    print(f"{Colour.OKGREEN}{text}{Colour.ENDC}")


def warn(text: str | list[str]):
    if isinstance(text, list):
        for line in text:
            print(f"{Colour.WARNING}{line}{Colour.ENDC}")
        return
    print(f"{Colour.WARNING}{text}{Colour.ENDC}")


def err(text: str | list[str]):
    if isinstance(text, list):
        for line in text:
            print(f"{Colour.FAIL}{line}{Colour.ENDC}")
        return
    print(f"{Colour.FAIL}{text}{Colour.ENDC}")

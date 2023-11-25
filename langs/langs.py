""" Enum for languages supported by the program. """

from enum import Enum

from langs.python import Python


class Lang(Enum):
    """Enum for languages supported by the program."""

    PYTHON = Python.lang_str()

    def __str__(self):
        return self.value

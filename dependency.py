""" This file contains the Dependency class which represents a dependecy of\
an abstract language"""

from abc import ABC, abstractmethod
from pathlib import Path


class Dependency(ABC):
    """A dependency of an abstract language"""

    def __init__(self, path: Path, name: str):
        self.name = name
        self.path = path
        self.loaded = False

    @staticmethod
    @abstractmethod
    def lang_str():
        """The language of the dependency"""

    @abstractmethod
    def load(self):
        """Load the dependecy into the current environment"""

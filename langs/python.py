""" This file contains the Dependency class which represents a dependecy\
 of an abstract language"""

import subprocess

from dependency import Dependency


class Python(Dependency):
    """A dependency of an abstract language"""

    @staticmethod
    def lang_str():
        """The language of the dependency"""
        return "python"

    def load(self):
        """Load the dependecy into the current environment"""
        args = ["pip", "install", "-e", str(self.path)]
        try:
            subprocess.run(args, check=True)
        except subprocess.CalledProcessError:
            print(f"ERROR: Could not install local lib at path: {self.path}")

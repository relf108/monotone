""" Command line arguments for Monotone. """
import argparse

from langs.langs import Lang

parser = argparse.ArgumentParser(description="Monotone")
parser.add_argument(
    "lang",
    type=Lang,
)
args = parser.parse_args()

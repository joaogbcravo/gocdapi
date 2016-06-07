"""
Command-line entry-point to display library version.
"""
import sys

from gocdapi import __version__ as version


def main():
    sys.stdout.write(version)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

"""Exercise 14 — create a left-handed, [0, 1]-depth projection matrix."""

from Matrix import projection
from math import pi

def main() -> None:
    matrix = projection(pi / 2, 1.0, 0.1, 100.0).to_column_major()
    for column in matrix:
        print(", ".join(str(value) for value in column))


if __name__ == "__main__":
    main()

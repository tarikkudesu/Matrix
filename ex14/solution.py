#!/usr/bin/env python3

"""Exercise 14 — create a left-handed, [0, 1]-depth projection matrix."""

from Matrix import projection


def main() -> None:
    matrix = projection(0.1, 3.0 / 2.0, 2.0, 10.)
    for column in matrix:
        print(", ".join(str(value) for value in column))


if __name__ == "__main__":
    main()

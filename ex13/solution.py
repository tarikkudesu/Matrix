#!/usr/bin/env python3

"""Exercise 13 — calculate rank from the number of pivots."""

from Matrix import Matrix


def main() -> None:
    print(Matrix([[1.0, 2.0, 0.0, 0.0], [2.0, 4.0, 0.0, 0.0], [-1.0, 2.0, 1.0, 1.0]]).rank())


if __name__ == "__main__":
    main()

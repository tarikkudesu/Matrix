#!/usr/bin/env python3

"""Exercise 12 — invert a non-singular square matrix."""

from Matrix import Matrix


def main() -> None:
    print(Matrix([[8.0, 5.0, -2.0], [4.0, 7.0, 20.0], [7.0, 6.0, 1.0]]).inverse())


if __name__ == "__main__":
    main()

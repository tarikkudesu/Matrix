#!/usr/bin/env python3

"""Exercise 08 — use ``Matrix.trace`` on a square matrix."""

from Matrix import Matrix


def main() -> None:
    print(Matrix([[2.0, -5.0, 0.0], [4.0, 3.0, 7.0], [-2.0, 3.0, 4.0]]).trace())


if __name__ == "__main__":
    main()

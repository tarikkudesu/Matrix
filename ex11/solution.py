#!/usr/bin/env python3

"""Exercise 11 — calculate a determinant through Gaussian elimination."""

from Matrix import Matrix


def main() -> None:
    print(Matrix([[8.0, 5.0, -2.0], [4.0, 7.0, 20.0], [7.0, 6.0, 1.0]]).determinant())


if __name__ == "__main__":
    main()

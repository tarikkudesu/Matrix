#!/usr/bin/env python3

"""Exercise 02 — interpolation for scalars, vectors, and matrices."""

from Matrix import Matrix, Vector, lerp


def main() -> None:
    print(lerp(21.0, 42.0, 0.3))
    print(lerp(Vector([2.0, 1.0]), Vector([4.0, 2.0]), 0.3))
    print(lerp(Matrix([[2.0, 1.0], [3.0, 4.0]]), Matrix([[20.0, 10.0], [30.0, 40.0]]), 0.5))


if __name__ == "__main__":
    main()

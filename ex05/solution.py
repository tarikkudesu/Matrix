#!/usr/bin/env python3

"""Exercise 05 — calculate a normalized inner product with ``angle_cos``."""

from Matrix import Vector, angle_cos


def main() -> None:
    print(angle_cos(Vector([1.0, 2.0, 3.0]), Vector([4.0, 5.0, 6.0])))


if __name__ == "__main__":
    main()

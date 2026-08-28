#!/usr/bin/env python3

"""Exercise 06 — calculate the cross product of two 3D vectors."""

from Matrix import Vector, cross_product


def main() -> None:
    print(cross_product(Vector([1.0, 2.0, 3.0]), Vector([4.0, 5.0, 6.0])))


if __name__ == "__main__":
    main()

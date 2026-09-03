#!/usr/bin/env python3

"""Exercise 01 — linear combinations of equally sized vectors."""

from Matrix import Vector, linear_combination


def main() -> None:
    basis = [Vector([1.0, 0.0, 0.0]), Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0])]
    print(linear_combination(basis, [10.0, -2.0, 0.5]))

if __name__ == "__main__":
    main()

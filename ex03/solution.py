#!/usr/bin/env python3

"""Exercise 03 — use ``Vector.dot`` to calculate an inner product."""

from Matrix import Vector


def main() -> None:
    print(Vector([-1.0, 6.0]).dot(Vector([3.0, 2.0])))


if __name__ == "__main__":
    main()

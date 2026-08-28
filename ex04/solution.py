#!/usr/bin/env python3

"""Exercise 04 — the 1-, 2-, and infinity-norm methods on ``Vector``."""

from Matrix import Vector


def main() -> None:
    vector = Vector([1.0, 2.0, 3.0])
    print(vector.norm_1(), vector.norm(), vector.norm_inf())


if __name__ == "__main__":
    main()

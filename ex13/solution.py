#!/usr/bin/env python3

"""Exercise 13 — calculate rank from the number of pivots."""

from Matrix import Matrix


def main() -> None:
    print(Matrix(
        [[1.0, 0.0, 0.0],
         [0.0, 1.0, 0.0],
         [0.0, 0.0, 1.0]]
        ).rank())
    print(Matrix(
        [[1.0, 2.0, 0.0, 0.0],
         [2.0, 4.0, 0.0, 0.0],
         [-1.0, 2.0, 1.0, 1.0]]
        ).rank())
    print(Matrix(
        [[8.0, 5.0, -2.0],
         [4.0, 7.0, 20.0],
         [7.0, 6.0, 1.0],
         [21.0, 18.0, 7.0]]
        ).rank())

if __name__ == "__main__":
    main()

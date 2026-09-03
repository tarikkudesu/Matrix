#!/usr/bin/env python3

"""Exercise 10 — calculate reduced row-echelon form (as in the subject examples)."""

from Matrix import Matrix


def main() -> None:
    matrix = Matrix(
        [[1.0, 0.0, 0.0],
         [0.0, 1.0, 0.0],
         [0.0, 0.0, 1.0]]
        )
    print(matrix.row_echelon())
    matrix = Matrix(
        [[1.0, 2.0],
         [3.0, 4.0]]
        )
    print(matrix.row_echelon())
    matrix = Matrix(
        [[1.0, 2.0],
         [2.0, 4.0]]
        )
    print(matrix.row_echelon())
    matrix = Matrix(
        [[8.0, 5.0, -2.0, 4.0, 28.0],
         [4.0, 2.5, 20.0, 4.0, -4.0],
         [8.0, 5.0, 1.0, 4.0, 17.0]]
        )
    print(matrix.row_echelon())

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

"""Exercise 00 — mutable vector and matrix addition, subtraction, and scaling."""

from Matrix import Matrix, Vector


def main() -> None:
    vector = Vector([2.0, 3.0])
    vector.add(Vector([5.0, 7.0]))
    print(vector)

    matrix = Matrix([[1.0, 2.0], [3.0, 4.0]])
    matrix.scl(2.0)
    print(matrix)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

"""Exercise 07 — use ``Matrix.mul_vec`` and ``Matrix.mul_mat``."""

from Matrix import Matrix, Vector


def main() -> None:
    print(Matrix([[2.0, -2.0], [-2.0, 2.0]]).mul_vec(Vector([4.0, 2.0])))
    print(Matrix([[3.0, -5.0], [6.0, 8.0]]).mul_mat(Matrix([[2.0, 1.0], [4.0, 2.0]])))


if __name__ == "__main__":
    main()

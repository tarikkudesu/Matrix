#!/usr/bin/env python3

"""Exercise 15 — reuse the generic implementation with Python complex numbers."""

from Matrix import Matrix, Vector


def main() -> None:
    vector = Vector([1 + 2j, 3 - 1j])
    print("inner product:", vector.dot(vector))
    print("norm:", vector.norm())
    print("matrix product:")
    print(Matrix([[1 + 1j, 2], [3, 4 - 1j]]).mul_vec(Vector([2j, 1])))


if __name__ == "__main__":
    main()

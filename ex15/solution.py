#!/usr/bin/env python3

"""Exercise 15 — demonstrate exercises 00–13 with complex numbers."""

from Matrix import Matrix, Vector, angle_cos, cross_product, lerp, linear_combination


def main() -> None:
    vector = Vector([1 + 2j, 3 - 1j])
    vector.add(Vector([2 - 1j, -1 + 3j]))
    print("vector addition:", vector)

    vector = Vector([1 + 2j, 3 - 1j])
    vector.sub(Vector([2 - 1j, -1 + 3j]))
    print("vector subtraction:", vector)

    vector = Vector([1 + 2j, 3 - 1j])
    vector.scl(2 - 1j)
    print("vector scaling:", vector)

    matrix = Matrix([[1 + 1j, 2 - 1j], [3 + 2j, 4 - 1j]])
    matrix.add(Matrix([[2 - 1j, 1 + 2j], [-1 + 1j, 3 + 1j]]))
    print("matrix addition:")
    print(matrix)

    matrix = Matrix([[1 + 1j, 2 - 1j], [3 + 2j, 4 - 1j]])
    matrix.sub(Matrix([[2 - 1j, 1 + 2j], [-1 + 1j, 3 + 1j]]))
    print("matrix subtraction:")
    print(matrix)

    matrix = Matrix([[1 + 1j, 2 - 1j], [3 + 2j, 4 - 1j]])
    matrix.scl(1 + 1j)
    print("matrix scaling:")
    print(matrix)

    vectors = [Vector([1 + 1j, 2]), Vector([2 - 1j, -1 + 2j])]
    coefficients = [2 - 1j, 1 + 1j]
    print(linear_combination(vectors, coefficients))

    print("scalar:", lerp(1 + 2j, 5 - 2j, 0.25))
    print("vector:", lerp(Vector([1 + 1j, 2 - 2j]), Vector([5 - 3j, -2 + 2j]), 0.5))
    print(
        "matrix:",
        lerp(
            Matrix([[1 + 1j, 2], [3j, 4 - 1j]]),
            Matrix([[3 - 1j, -2j], [2 + 1j, 8 + 3j]]),
            0.5,
        ),
        sep="\n",
    )

    left = Vector([1 + 2j, 3 - 1j])
    right = Vector([2 - 1j, -1 + 3j])
    print("dot:", left.dot(right))

    vector = Vector([3 + 4j, 1 - 1j, -2j])
    print("norm_1:", vector.norm_1())
    print("norm_2:", vector.norm())
    print("norm_inf:", vector.norm_inf())

    print("angle cosine:", angle_cos(left, right))

    print(
        cross_product(
            Vector([1 + 1j, 2, -1j]),
            Vector([2 - 1j, 1 + 2j, 3]),
        )
    )

    matrix = Matrix([[1 + 1j, 2 - 1j], [3, 4 + 2j]])
    print("matrix × vector:", matrix.mul_vec(Vector([2j, 1 - 1j])))
    print(
        "matrix × matrix:",
        matrix.mul_mat(Matrix([[1 - 1j, 2], [2 + 1j, -1j]])),
        sep="\n",
    )

    print("trace:", Matrix([[1 + 2j, 3], [4 - 1j, 2 - 3j]]).trace())

    print(Matrix([[1 + 1j, 2, 3 - 1j], [4j, 5 + 2j, 6]]).transpose())

    echelon_matrix = Matrix(
        [
            [1 + 1j, 2, 1 - 1j],
            [2 + 2j, 4, 2 - 2j],
            [1, -1j, 2 + 1j],
        ]
    )
    print(echelon_matrix.row_echelon())

    invertible = Matrix([[1 + 1j, 1], [0, 2]])
    print("determinant:", invertible.determinant())

    inverse = invertible.inverse()
    print("inverse:")
    print(inverse)
    print("matrix × inverse:")
    print(invertible.mul_mat(inverse))

    dependent = Matrix(
        [
            [1 + 1j, 2, -1j],
            [2 + 2j, 4, -2j],
            [1, 0, 1 - 1j],
        ]
    )
    print("rank:", dependent.rank())


if __name__ == "__main__":
    main()

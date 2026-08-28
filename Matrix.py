#!/usr/bin/env python3

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from math import tan
from typing import Generic, TypeAlias, TypeVar, overload

Scalar: TypeAlias = int | float | complex
T = TypeVar("T", bound=Scalar)

EPSILON = 1e-12


class DimensionError(ValueError):
    """Raised when an operation is attempted on incompatible dimensions."""


class SingularMatrixError(ValueError):
    """Raised when an inverse is requested for a singular matrix."""


def _is_near_zero(value: Scalar, *, epsilon: float = EPSILON) -> bool:
    return abs(value) <= epsilon


def _clean(value: Scalar, *, epsilon: float = EPSILON) -> Scalar:
    """Turn negligible floating-point noise into zero without changing exact values."""
    return 0 if _is_near_zero(value, epsilon=epsilon) else value


@dataclass
class Vector(Generic[T]):
    """A mutable finite-dimensional vector.

    ``add``, ``sub``, and ``scl`` deliberately mutate the vector to mirror the
    assignment's Rust method signatures.  Methods that compute a new value (for
    example ``cross_product``) leave their arguments untouched.
    """

    values: list[T]

    def __init__(self, values: Iterable[T]) -> None:
        self.values = list(values)

    def __len__(self) -> int:
        return len(self.values)

    def __iter__(self) -> Iterator[T]:
        return iter(self.values)

    def __getitem__(self, index: int) -> T:
        return self.values[index]

    def __repr__(self) -> str:
        return f"Vector({self.values!r})"

    def __str__(self) -> str:
        return "\n".join(f"[{value}]" for value in self.values)

    def copy(self) -> Vector[T]:
        return Vector(self.values)

    def check_same_dimension(self, other: Vector[Scalar]) -> None:
        if len(self) != len(other):
            raise DimensionError(f"vector dimensions differ: {len(self)} and {len(other)}")

    def add(self, other: Vector[T]) -> None:
        """Add ``other`` to this vector in place.  Complexity: O(n)."""
        self.check_same_dimension(other)
        for index, value in enumerate(other):
            self.values[index] += value  # type: ignore[operator]

    def sub(self, other: Vector[T]) -> None:
        """Subtract ``other`` from this vector in place.  Complexity: O(n)."""
        self.check_same_dimension(other)
        for index, value in enumerate(other):
            self.values[index] -= value  # type: ignore[operator]

    def scl(self, scalar: T) -> None:
        """Scale this vector by ``scalar`` in place.  Complexity: O(n)."""
        for index in range(len(self)):
            self.values[index] *= scalar  # type: ignore[operator]

    def dot(self, other: Vector[T]) -> T:
        """Return the inner product.  Complex inputs use conjugation on ``self``."""
        self.check_same_dimension(other)
        total: Scalar = 0
        for left, right in zip(self, other):
            # ``conjugate`` exists on int, float, and complex.
            total += left.conjugate() * right
        return total  # type: ignore[return-value]

    def norm_1(self) -> float:
        """Return the Manhattan (1-) norm.  Complexity: O(n)."""
        return float(sum(abs(value) for value in self))

    def norm(self) -> float:
        """Return the Euclidean (2-) norm.  Complexity: O(n)."""
        return float(sum(abs(value) ** 2 for value in self) ** 0.5)

    def norm_inf(self) -> float:
        """Return the supremum (infinity-) norm.  Complexity: O(n)."""
        return float(max((abs(value) for value in self), default=0))


@dataclass
class Matrix(Generic[T]):
    """A mutable, rectangular matrix stored as a list of rows."""

    rows: list[list[T]]

    def __init__(self, rows: Iterable[Iterable[T]]) -> None:
        self.rows = [list(row) for row in rows]
        if self.rows:
            width = len(self.rows[0])
            if any(len(row) != width for row in self.rows):
                raise DimensionError("all matrix rows must have the same length")

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.rows), len(self.rows[0]) if self.rows else 0)

    @property
    def row_count(self) -> int:
        return self.shape[0]

    @property
    def column_count(self) -> int:
        return self.shape[1]

    def __getitem__(self, index: int) -> list[T]:
        return self.rows[index]

    def __iter__(self) -> Iterator[list[T]]:
        return iter(self.rows)

    def __repr__(self) -> str:
        return f"Matrix({self.rows!r})"

    def __str__(self) -> str:
        return "\n".join(str(row) for row in self.rows)

    def copy(self) -> Matrix[T]:
        return Matrix(self.rows)

    @classmethod
    def identity(cls, size: int) -> Matrix[float]:
        if size < 0:
            raise ValueError("identity size must be non-negative")
        return Matrix([[1.0 if row == column else 0.0 for column in range(size)] for row in range(size)])

    @classmethod
    def from_column_major(cls, values: Iterable[Iterable[T]]) -> Matrix[T]:
        """Build a matrix from column-major columns, as used by the display tool."""
        columns = [list(column) for column in values]
        if not columns:
            return cls([])
        height = len(columns[0])
        if any(len(column) != height for column in columns):
            raise DimensionError("all columns must have the same length")
        return cls([[columns[column][row] for column in range(len(columns))] for row in range(height)])

    def to_column_major(self) -> list[list[T]]:
        """Return columns suitable for a column-major renderer/file format."""
        return [[self.rows[row][column] for row in range(self.row_count)] for column in range(self.column_count)]

    def check_same_shape(self, other: Matrix[Scalar]) -> None:
        if self.shape != other.shape:
            raise DimensionError(f"matrix shapes differ: {self.shape} and {other.shape}")

    def _require_square(self) -> None:
        if self.row_count != self.column_count:
            raise DimensionError(f"operation requires a square matrix, got {self.shape}")

    def add(self, other: Matrix[T]) -> None:
        """Add ``other`` to this matrix in place.  Complexity: O(mn)."""
        self.check_same_shape(other)
        for row in range(self.row_count):
            for column in range(self.column_count):
                self.rows[row][column] += other.rows[row][column]  # type: ignore[operator]

    def sub(self, other: Matrix[T]) -> None:
        """Subtract ``other`` from this matrix in place.  Complexity: O(mn)."""
        self.check_same_shape(other)
        for row in range(self.row_count):
            for column in range(self.column_count):
                self.rows[row][column] -= other.rows[row][column]  # type: ignore[operator]

    def scl(self, scalar: T) -> None:
        """Scale this matrix by ``scalar`` in place.  Complexity: O(mn)."""
        for row in range(self.row_count):
            for column in range(self.column_count):
                self.rows[row][column] *= scalar  # type: ignore[operator]

    def mul_vec(self, vector: Vector[T]) -> Vector[T]:
        """Return this matrix multiplied by ``vector``.  Complexity: O(mn)."""
        if self.column_count != len(vector):
            raise DimensionError(f"matrix/vector dimensions are incompatible: {self.shape} and {len(vector)}")
        result: list[Scalar] = []
        for row in self.rows:
            total: Scalar = 0
            for matrix_value, vector_value in zip(row, vector):
                total += matrix_value * vector_value
            result.append(total)
        return Vector(result)  # type: ignore[arg-type]

    def mul_mat(self, other: Matrix[T]) -> Matrix[T]:
        """Return this matrix multiplied by ``other``.  Complexity: O(mnp)."""
        if self.column_count != other.row_count:
            raise DimensionError(f"matrix dimensions are incompatible: {self.shape} and {other.shape}")
        result: list[list[Scalar]] = []
        for row in range(self.row_count):
            result_row: list[Scalar] = []
            for column in range(other.column_count):
                total: Scalar = 0
                for pivot in range(self.column_count):
                    total += self.rows[row][pivot] * other.rows[pivot][column]
                result_row.append(total)
            result.append(result_row)
        return Matrix(result)  # type: ignore[arg-type]

    def trace(self) -> T:
        """Return the trace of a square matrix.  Complexity: O(n)."""
        self._require_square()
        total: Scalar = 0
        for index in range(self.row_count):
            total += self.rows[index][index]
        return total  # type: ignore[return-value]

    def transpose(self) -> Matrix[T]:
        """Return the transposed matrix.  Complexity: O(mn)."""
        return Matrix([[self.rows[row][column] for row in range(self.row_count)] for column in range(self.column_count)])

    def _reduced_rows(self) -> tuple[list[list[Scalar]], int]:
        """Compute a reduced row-echelon copy and its number of pivots."""
        rows: list[list[Scalar]] = [list(row) for row in self.rows]
        pivot_row = 0
        pivot_count = 0

        for column in range(self.column_count):
            if pivot_row == self.row_count:
                break

            best_row = max(
                range(pivot_row, self.row_count),
                key=lambda row: abs(rows[row][column]),
            )
            if _is_near_zero(rows[best_row][column]):
                continue

            rows[pivot_row], rows[best_row] = rows[best_row], rows[pivot_row]
            pivot = rows[pivot_row][column]
            rows[pivot_row] = [value / pivot for value in rows[pivot_row]]

            for row in range(self.row_count):
                if row == pivot_row:
                    continue
                factor = rows[row][column]
                if not _is_near_zero(factor):
                    rows[row] = [value - factor * pivot_value for value, pivot_value in zip(rows[row], rows[pivot_row])]

            pivot_row += 1
            pivot_count += 1

        return [[_clean(value) for value in row] for row in rows], pivot_count

    def row_echelon(self) -> Matrix[Scalar]:
        """Return reduced row-echelon form, matching the assignment examples.

        Partial pivoting avoids needlessly dividing by a very small value.  The
        operation takes O(min(m, n) * m * n), which is O(n³) for square matrices.
        """
        rows, _ = self._reduced_rows()
        return Matrix(rows)

    def determinant(self) -> T:
        """Return the determinant using Gaussian elimination.  Complexity: O(n³)."""
        self._require_square()
        size = self.row_count
        if size == 0:
            return 1  # type: ignore[return-value]

        rows: list[list[Scalar]] = [list(row) for row in self.rows]
        sign: Scalar = 1
        determinant: Scalar = 1

        for column in range(size):
            best_row = max(range(column, size), key=lambda row: abs(rows[row][column]))
            pivot = rows[best_row][column]
            if _is_near_zero(pivot):
                return 0  # type: ignore[return-value]
            if best_row != column:
                rows[column], rows[best_row] = rows[best_row], rows[column]
                sign = -sign
            pivot = rows[column][column]
            determinant *= pivot
            for row in range(column + 1, size):
                factor = rows[row][column] / pivot
                for inner_column in range(column + 1, size):
                    rows[row][inner_column] -= factor * rows[column][inner_column]

        return _clean(sign * determinant)  # type: ignore[return-value]

    def inverse(self) -> Matrix[Scalar]:
        """Return the inverse through Gauss-Jordan elimination.  Complexity: O(n³)."""
        self._require_square()
        size = self.row_count
        rows: list[list[Scalar]] = [list(row) + [1 if row_index == column else 0 for column in range(size)] for row_index, row in enumerate(self.rows)]

        for column in range(size):
            best_row = max(range(column, size), key=lambda row: abs(rows[row][column]))
            if _is_near_zero(rows[best_row][column]):
                raise SingularMatrixError("matrix is singular and cannot be inverted")
            rows[column], rows[best_row] = rows[best_row], rows[column]

            pivot = rows[column][column]
            rows[column] = [value / pivot for value in rows[column]]
            for row in range(size):
                if row == column:
                    continue
                factor = rows[row][column]
                if not _is_near_zero(factor):
                    rows[row] = [value - factor * pivot_value for value, pivot_value in zip(rows[row], rows[column])]

        return Matrix([[_clean(value) for value in row[size:]] for row in rows])

    def rank(self) -> int:
        """Return the count of linearly independent rows/columns.  Complexity: O(n³)."""
        _, pivot_count = self._reduced_rows()
        return pivot_count


def linear_combination(vectors: Sequence[Vector[T]], coefficients: Sequence[T]) -> Vector[T]:
    """Return ``Σ coefficient[i] * vector[i]``.  Complexity: O(kn)."""
    if len(vectors) != len(coefficients):
        raise DimensionError("the vector and coefficient counts must match")
    if not vectors:
        return Vector([])

    dimension = len(vectors[0])
    if any(len(vector) != dimension for vector in vectors):
        raise DimensionError("all vectors in a linear combination need the same dimension")

    result: list[Scalar] = [0 for _ in range(dimension)]
    for vector, coefficient in zip(vectors, coefficients):
        for index, value in enumerate(vector):
            result[index] += coefficient * value
    return Vector(result)  # type: ignore[arg-type]


@overload
def lerp(u: Vector[T], v: Vector[T], t: float) -> Vector[T]: ...


@overload
def lerp(u: Matrix[T], v: Matrix[T], t: float) -> Matrix[T]: ...


@overload
def lerp(u: T, v: T, t: float) -> T: ...


def lerp(u: Vector[T] | Matrix[T] | T, v: Vector[T] | Matrix[T] | T, t: float):
    """Linearly interpolate between matching scalars, vectors, or matrices.

    ``t`` is intentionally not clamped: extrapolation is part of the assignment.
    """
    if isinstance(u, Vector) and isinstance(v, Vector):
        u.check_same_dimension(v)
        return Vector([left + (right - left) * t for left, right in zip(u, v)])
    if isinstance(u, Matrix) and isinstance(v, Matrix):
        u.check_same_shape(v)
        return Matrix([[left + (right - left) * t for left, right in zip(u_row, v_row)] for u_row, v_row in zip(u, v)])
    if isinstance(u, (Vector, Matrix)) or isinstance(v, (Vector, Matrix)):
        raise TypeError("lerp inputs must have the same kind")
    return u + (v - u) * t


def angle_cos(u: Vector[T], v: Vector[T]) -> T:
    """Return the normalized inner product of non-zero, matching vectors."""
    u.check_same_dimension(v)
    denominator = u.norm() * v.norm()
    if _is_near_zero(denominator):
        raise ValueError("the angle with a zero vector is undefined")
    return u.dot(v) / denominator  # type: ignore[return-value]


def cross_product(u: Vector[T], v: Vector[T]):
    """Return the 3D cross product ``u × v``."""
    if len(u) != 3 or len(v) != 3:
        raise DimensionError("cross product requires two three-dimensional vectors")
    return Vector(
        [
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0],
        ]
    )


def projection(fov: float, ratio: float, near: float, far: float) -> Matrix[float]:
    """Build a left-handed perspective projection matrix.

    ``fov`` is in radians.  The resulting matrix maps depth from ``near`` to 0
    and depth from ``far`` to 1, while x/y map to the assignment's [-1, 1] NDC.
    Call ``to_column_major`` before supplying it to the provided display program.
    """
    if fov <= 0 or fov >= 3.141592653589793:
        raise ValueError("fov must be strictly between 0 and pi radians")
    if ratio <= 0:
        raise ValueError("ratio must be positive")
    if near <= 0 or far <= near:
        raise ValueError("require 0 < near < far")

    scale = 1.0 / tan(fov / 2.0)
    depth_scale = far / (far - near)
    depth_offset = -(far * near) / (far - near)
    return Matrix(
        [
            [scale / ratio, 0.0, 0.0, 0.0],
            [0.0, scale, 0.0, 0.0],
            [0.0, 0.0, depth_scale, depth_offset],
            [0.0, 0.0, 1.0, 0.0],
        ]
    )

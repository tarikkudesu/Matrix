#!/usr/bin/env python3

"""Exercise 14 — create a left-handed, [0, 1]-depth projection matrix."""

from Matrix import projection


def main() -> None:
    # fov is in radians.  The display program expects the columns below in this order.
    matrix = projection(1.0471975512, 16 / 9, 0.1, 100.0)
    for column in matrix.to_column_major():
        print(", ".join(str(value) for value in column))


if __name__ == "__main__":
    main()

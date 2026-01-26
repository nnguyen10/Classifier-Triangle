"""
Triangle Classification Program
Author: Winnie Nguyen
Date: 2026-01-26

This program classifies a triangle based on user input.
It determines whether the triangle is equilateral, isosceles, or scalene,
and whether it is also a right triangle using the Pythagorean theorem.
"""

import math


def classify_triangle(a, b, c):
    """
    Classifies a triangle given sides a, b, and c.
    c is assumed to be the hypotenuse.
    """

    # Validate input types
    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except ValueError:
        print("Invalid input. Numbers only, please. This is math, not poetry.")
        return

    # Check for negative or zero values
    if a <= 0 or b <= 0 or c <= 0:
        print("Invalid input. Triangles don’t exist in negative dimensions. Nice try.")
        return

    # Check for imaginary numbers (Python floats can't be imaginary,
    # but this protects against misuse)
    if any(isinstance(x, complex) for x in [a, b, c]):
        print("Imaginary numbers? This isn’t a sci-fi triangle.")
        return

    # Triangle inequality check
    if a + b <= c or a + c <= b or b + c <= a:
        print("Invalid triangle. Those sides wouldn’t survive reality.")
        return

    # Determine triangle type
    if a == b == c:
        triangle_type = "equilateral"
    elif a == b or b == c or a == c:
        triangle_type = "isosceles"
    else:
        triangle_type = "scalene"

    # Check for right triangle using Pythagorean theorem
    is_right = math.isclose(c**2, a**2 + b**2, rel_tol=1e-9)

    # Output result
    if is_right:
        print(f"This triangle is {triangle_type} and also a right triangle.")
    else:
        print(f"This triangle is {triangle_type} and not a right triangle.")


def main():
    """
    Main routine to interact with the user.
    """
    print("Triangle Classifier")
    print("Enter the lengths of the three sides.")
    print("Reminder: c is the hypotenuse.\n")

    a = input("Enter side a: ")
    b = input("Enter side b: ")
    c = input("Enter side c: ")

    classify_triangle(a, b, c)


if __name__ == "__main__":
    main()

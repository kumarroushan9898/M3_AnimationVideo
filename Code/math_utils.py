"""One source for the transformation and an exact SymPy verification."""
import numpy as np
import sympy as sp

A = np.array([[2, 1], [0, 1]])
I = np.eye(2)
E1_POINT = (1, 0)
E2_POINT = (0, 1)
INPUT = (2, 1)
ORIGIN = (0, 0)
UNIT_SQUARE = (ORIGIN, E1_POINT, (1, 1), E2_POINT)
ROTATION = np.array([[0, -1], [1, 0]])
REFLECTION = np.array([[-1, 0], [0, 1]])
SCALING = np.diag([2, 2])
SHEAR = np.array([[1, 1], [0, 1]])
PROJECTION = np.diag([1, 0])


def mapped(point, matrix=A):
    """Return the two-dimensional image of a point or vector."""
    return tuple(np.asarray(matrix) @ point)


def intermediate(alpha, matrix=A):
    """Interpolate the map itself so all corresponding objects share one map."""
    return I + alpha * (matrix - I)


def verify_math():
    matrix = sp.Matrix(A.tolist())
    e1, e2, v, zero = map(sp.Matrix, (E1_POINT, E2_POINT, INPUT, ORIGIN))
    x, y, a, b, c = sp.symbols("x y a b c", real=True)
    u, w = sp.Matrix([x, y]), sp.Matrix([a, b])
    images = [tuple(matrix * sp.Matrix(p)) for p in UNIT_SQUARE]
    vertices = [sp.Point(*p) for p in images]
    checks = {
        "first column": matrix * e1 == matrix[:, 0] == sp.Matrix([2, 0]),
        "second column": matrix * e2 == matrix[:, 1] == sp.Matrix([1, 1]),
        "input decomposition": v == 2 * e1 + e2,
        "basis calculation": matrix * v == 2 * matrix * e1 + matrix * e2,
        "row calculation": matrix * v == sp.Matrix([2 * 2 + 1 * 1, 0 * 2 + 1 * 1])
        == sp.Matrix([5, 1]),
        "general formula": matrix * u == sp.Matrix([2 * x + y, y]),
        "symbolic additivity": (matrix * (u + w) - matrix * u - matrix * w).expand() == zero,
        "symbolic homogeneity": (matrix * (c * u) - c * matrix * u).expand() == zero,
        "origin": matrix * zero == zero,
        "square images": images == [(0, 0), (2, 0), (3, 1), (1, 1)],
        "area and invertibility": sp.Polygon(*vertices).area == matrix.det() == 2,
        "parallel direction": matrix * sp.Matrix([3, 0]) == 3 * matrix * e1
        and matrix * sp.Matrix([0, 2]) == 2 * matrix * e2,
        "line collapse example": mapped((0, 3), PROJECTION) == mapped((0, -1), PROJECTION) == ORIGIN,
        "rotation": mapped((1, 0), ROTATION) == (0, 1),
        "reflection": mapped((1, 0), REFLECTION) == (-1, 0),
        "scaling": mapped((1, 1), SCALING) == (2, 2),
        "shear": mapped((0, 1), SHEAR) == (1, 1),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ValueError("Mathematical verification failed: " + ", ".join(failed))
    return checks


if __name__ == "__main__":
    print(f"Verified {len(verify_math())} exact mathematical claims.")

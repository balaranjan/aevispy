import numpy as np
import pytest
from aevispy import functions
from aevispy import utilities


def test_gsd_to_cif():
    gsd_file_name = "test.gsd"
    atoms = utilities.convert_gsd_to_cif(gsd_file_name)

    cell = np.array([[28.0, 0.0, 0.0], [0.0, 28.0, 0.0], [0.0, 0.0, 28.0]])

    pos = [[-13.0, -13.0, -13.0], [-13.0, -13.0, -11.0], [-13.0, -13.0, -9.0]]

    assert atoms.cell.array == cell
    assert atoms.positions[:3] == pos


def test_dot_product_2D_list():
    a = [1, 2]
    b = [3, 4]
    expected = 11.0
    actual = functions.dot_product(a, b)
    assert actual == expected


def test_dot_product_3D_list():
    a = [1, 2, 3]
    b = [4, 5, 6]
    expected = 32.0
    actual = functions.dot_product(a, b)
    assert actual == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        # Test whether the dot product function works with 2D and 3D vectors
        # C1: lists, expect correct float output
        ([1, 2], [3, 4], 11.0),
        ([1, 2, 3], [4, 5, 6], 32.0),
        # C2: tuples, expect correct float output
        ((1, 2), (3, 4), 11.0),
        ((1, 2, 3), (4, 5, 6), 32.0),
        # C3: numpy arrays, expect correct float output
        (np.array([1, 2]), np.array([3, 4]), 11.0),
        (np.array([1, 2, 3]), np.array([4, 5, 6]), 32.0),
    ],
)
def test_dot_product(a, b, expected):
    actual = functions.dot_product(a, b)
    assert actual == expected

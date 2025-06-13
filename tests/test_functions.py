import numpy as np
from aevispy import utilities


def test_gsd_to_cif():
    gsd_file_name = "test.gsd"
    atoms = utilities.convert_gsd_to_cif(gsd_file_name)

    cell = np.array([[28.0, 0.0, 0.0], [0.0, 28.0, 0.0], [0.0, 0.0, 28.0]])

    pos = [[-13.0, -13.0, -13.0], [-13.0, -13.0, -11.0], [-13.0, -13.0, -9.0]]

    assert atoms.cell.array == cell
    assert atoms.positions[:3] == pos

from ase import Atoms
from ase.io import read
from ase.build import make_supercell
from gsd.pygsd import GSDFile
import os


def convert_gsd_to_cif(gsd_filename, frame_to_read):

    gsd_file = GSDFile(open(gsd_filename, "rb"))

    data_blocks = gsd_file.find_matching_chunk_names("")

    for block in ["configuration/box", "particles/position"]:
        if block not in data_blocks:
            print(f"Block {block} not found in {gsd_file}")
            return

    box = gsd_file.read_chunk(frame=frame_to_read, name="configuration/box")
    positions = gsd_file.read_chunk(
        frame=frame_to_read, name="particles/position"
    )
    # symbols = gsd_file.read_chunk(frame=frame_to_read,
    # name="particles/types")

    atoms = Atoms(
        symbols=[
            1 for _ in range(positions.shape[0])
        ],  # TODO : Add symbols or numbers
        positions=positions,
        pbc=True,
    )
    atoms.set_cell(box[:3])

    return atoms


def make_supercell_from_atoms(atoms, nx, ny, nz):

    P = [[nx, 0, 0], [0, ny, 0], [0, 0, nz]]
    atoms = make_supercell(atoms, P)

    return atoms


def get_atoms(input_filename, frame_to_read=0, nx=None, ny=None, nz=None):
    if input_filename[-3:] not in ["gsd", "cif"]:
        print("Only .gsd and .cif files are supported.")
        return

    if not os.path.isfile(input_filename):
        print(f"File {input_filename} not found!")
        return

    if input_filename.endswith("cif"):
        atoms = read(input_filename)
    elif input_filename.endswith("gsd"):
        atoms = convert_gsd_to_cif(
            gsd_filename=input_filename, frame_to_read=frame_to_read
        )

    if nx and ny and nz:
        atoms = make_supercell_from_atoms(atoms, nx, ny, nz)

    return atoms

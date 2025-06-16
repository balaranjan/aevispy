import argparse
from .utilities import get_atoms
from .get_pythia_descs import get_pythia_descs
from .clustering import color_atoms


def main():

    description = """
    Command line tool for AEVisPy

    The following descriptor options are available.
    Default is 11 (all descriptors)

    1 .  amean
    2 .  bispectrum_sphs
    3 .  neighborhood_angle_sorted
    4 .  neighborhood_distance_sorted
    5 .  neighborhood_range_angle_singvals
    6 .  neighborhood_range_distance_singvals
    7 .  normalized_radial_distance
    8 .  spherical_harmonics_abs_neighbor_average
    9 .  steinhardt_q
    10.  voronoi_angle_histogram
    11.  all of the above
    """

    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument(
        "envs", nargs="+", help="Number of environments. e.g. 4 or 4 6"
    )
    parser.add_argument(
        "-d", "--desc", nargs="+", help="Descriptors. e.g. 4 or 4 6"
    )
    parser.add_argument(
        "-s",
        "--supercell",
        nargs="+",
        help="Multipliers for making super cell. e.g. 2 2 2 or 2",
    )
    parser.add_argument(
        "-f", "--frame", help="Frame number to get from gsd file.", type=int
    )

    descriptors = [
        "amean",
        "bispectrum_sphs",
        "neighborhood_angle_sorted",
        "neighborhood_distance_sorted",
        "neighborhood_range_angle_singvals",
        "neighborhood_range_distance_singvals",
        "normalized_radial_distance",
        "spherical_harmonics_abs_neighbor_average",
        "steinhardt_q",
        "voronoi_angle_histogram",
    ]

    # defaults
    frame_to_read = 0
    nx, ny, nz = None, None, None
    desc = list(range(1, 11))

    args = parser.parse_args()
    input_filename = args.input_file

    envs = [int(i) for i in args.envs]

    if args.frame:
        frame_to_read = int(args.frame)
    else:
        if args.input_filename.endswith(".cif"):
            print(
                "For .gsd files, the first frame will be read by default.  \
                  \nPlease specify the frame number using -f flag, if needed."
            )

    if args.desc:
        desc = [int(v) for v in args.desc]

    if args.supercell:
        if len(args.supercell) == 3:
            nx, ny, nz = [int(v) for v in args.supercell]
        else:
            nx = int(args.supercell[0])
            ny, nz = nx, nx

    print("Parsing input file......", end=" ")
    atoms = get_atoms(
        input_filename=input_filename,
        frame_to_read=frame_to_read,
        nx=nx,
        ny=ny,
        nz=nz,
    )
    print("done")

    box = []
    for i, v in enumerate(atoms.cell.array.tolist()):
        box.append(v[i])

    box.extend([0.0, 0.0, 0.0])

    print("Calculating descriptors......", end=" ")
    py_descriptors = get_pythia_descs(
        positions=atoms.positions,
        box=box,
        descriptor_names=[descriptors[i - 1] for i in desc],
    )
    print("done")

    print("Clustering and plotting......", end=" ")
    for num_env in envs:
        color_atoms(
            descriptors=py_descriptors,
            num_environments=num_env,
            atoms=atoms,
            name=f"{input_filename[:-4]}_n_{num_env}",
        )
    print("done")

    return


if __name__ == "__main__":
    main()

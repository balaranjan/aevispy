from collections import namedtuple
import numpy as np
import freud
import pythia
import scipy as sp

# Source: https://github.com/glotzerlab/pythia/tree/master/examples

FakeBox = namedtuple("FakeBox", ["Lx", "Ly", "Lz", "xy", "xz", "yz"])


params = dict(
    amean=dict(neigh_max=12, lmax=12),
    voronoi_angle_histogram=dict(bins=32),
    normalized_radial_distance=dict(neighbors=16),
    neighborhood_range_angle_singvals=dict(neigh_min=4, neigh_max=32),
    neighborhood_angle_sorted=dict(neighbors=16),
    neighborhood_range_distance_singvals=dict(neigh_min=4, neigh_max=32),
    neighborhood_distance_sorted=dict(neighbors=16),
    steinhardt_q=dict(neighbors=12, lmax=20),
    bispectrum_sphs=dict(neighbors=4, lmax=6),
    spherical_harmonics_abs_neighbor_average=dict(
        neigh_min=4, neigh_max=32, lmax=12
    ),
)


def split_graph(box, positions):
    fbox = freud.box.Box.from_box(FakeBox(*box))
    aq = freud.AABBQuery(fbox, positions)
    nlist = aq.query(
        positions, dict(num_neighbors=16, exclude_ii=True)
    ).toNeighborList()
    rijs = (
        positions[nlist.point_indices] - positions[nlist.query_point_indices]
    )
    rijs = fbox.wrap(rijs)
    weights = np.linalg.norm(rijs, axis=-1)

    neighbor_graph = sp.sparse.coo_matrix(
        (weights, (nlist.query_point_indices, nlist.point_indices)),
        shape=(len(positions), len(positions)),
    ).tocsr()
    tree = sp.sparse.csgraph.minimum_spanning_tree(neighbor_graph).todok()

    return sp.sparse.csgraph.connected_components(tree)


def calculate_descriptors(positions, box, mode):

    box = FakeBox(*box)

    kwargs = params[mode]
    try:
        if mode == "amean":
            descriptors = pythia.spherical_harmonics.neighbor_average(
                box, positions, negative_m=False, **kwargs
            )
        elif mode == "voronoi_angle_histogram":
            descriptors = pythia.voronoi.angle_histogram(
                box, positions, **kwargs
            )
        elif mode == "normalized_radial_distance":
            descriptors = pythia.bonds.normalized_radial_distance(
                box, positions, **kwargs
            )
        elif mode == "neighborhood_distance_singvals":
            descriptors = pythia.bonds.neighborhood_distance_singvals(
                box, positions, **kwargs
            )
        elif mode == "neighborhood_range_distance_singvals":
            descriptors = pythia.bonds.neighborhood_range_distance_singvals(
                box, positions, **kwargs
            )
        elif mode == "neighborhood_distance_sorted":
            descriptors = pythia.bonds.neighborhood_distance_sorted(
                box, positions, **kwargs
            )
        elif mode == "neighborhood_angle_singvals":
            descriptors = pythia.bonds.neighborhood_angle_singvals(
                box, positions, **kwargs
            )
        elif mode == "neighborhood_range_angle_singvals":
            descriptors = pythia.bonds.neighborhood_range_angle_singvals(
                box, positions, **kwargs
            )
        elif mode == "neighborhood_angle_sorted":
            descriptors = pythia.bonds.neighborhood_angle_sorted(
                box, positions, **kwargs
            )
        elif mode == "steinhardt_q":
            descriptors = pythia.spherical_harmonics.steinhardt_q(
                box, positions, **kwargs
            )
        elif mode == "bispectrum_sphs":
            descriptors = pythia.spherical_harmonics.bispectrum(
                box, positions, **kwargs
            )
        elif mode == "spherical_harmonics_abs_neighbor_average":
            descriptors = pythia.spherical_harmonics.abs_neighbor_average(
                box, positions, **kwargs
            )
        else:
            raise NotImplementedError(
                "Unknown descriptor mode {}".format(mode)
            )

        return np.asarray(descriptors, dtype=np.float32)
    except ValueError:
        print(
            f"\nError calculating {mode} descriptor. \
                \nThis may occur if the cell is small.  \
                Make a super cell using the -s flag. e.g. -s 3"
        )


def get_pythia_descs(positions, box, descriptor_names):

    descriptors = {}
    for descriptor_name in descriptor_names:
        descriptor = calculate_descriptors(
            positions=positions, box=box, mode=descriptor_name
        )

        if descriptor is not None:
            descriptors[descriptor_name] = descriptor
        else:
            print(
                f"\nNo values returned for {descriptor_name} descriptor. \
                    \nThis may occur if the cell is small.  \
                    Make a super cell using the -s flag. e.g. -s 3"
            )

    return descriptors

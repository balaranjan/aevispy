from matplotlib import pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
import numpy as np
import os


def get_PCs(X, n=8):
    pca = PCA(n_components=n)

    return pca.fit_transform(X), pca.explained_variance_ratio_


def get_gmm(X, explained_vars, num_clusters, name, desc_name):
    # colors = [
    #     "tab:blue",
    #     "tab:orange",
    #     "tab:green",
    #     "tab:red",
    #     "tab:purple",
    #     "tab:brown",
    #     "tab:pink",
    #     "tab:gray",
    #     "tab:olive",
    #     "tab:cyan",
    # ]

    gmm = GaussianMixture(n_components=num_clusters, covariance_type="full")
    gmm.fit(X)

    # labels = gmm.predict(X)
    # legends_added = []
    # for x, y, l in zip(X[:, 0], X[:, 1], labels):
    #     c = colors[l]
    #     if l not in legends_added:
    #         plt.scatter(x, y, label=f"Group {l}", c=c)
    #         legends_added.append(l)
    #     else:
    #         plt.scatter(x, y, c=c)

    # plt.xlabel(f"PC1 ({explained_vars[0]:2.1f})%")
    # plt.ylabel(f"PC2 ({explained_vars[1]:2.1f})%")
    # plt.legend()
    # plt.tight_layout()
    # plt.savefig(f"{name}_pca_of_desc_{desc_name}.png")

    return gmm


def color_atoms(descriptors, num_environments, atoms, name):

    colors = [
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:brown",
        "tab:pink",
    ]

    descriptor_names = sorted(list(descriptors.keys()))

    plt.close()
    plt.figure()
    fig, ax = plt.subplots(nrows=len(descriptor_names), ncols=3)
    fig.set_size_inches(10, len(descriptor_names) * 3)

    for row, descriptor_name in enumerate(descriptor_names):
        PCs, evs = get_PCs(descriptors[descriptor_name])
        gmm = get_gmm(
            X=PCs,
            explained_vars=evs,
            num_clusters=num_environments,
            name=name,
            desc_name=descriptor_name,
        )

        xy, xz, yz = [], [], []
        for atom, desc in zip(atoms, PCs):
            cl = gmm.predict(desc.reshape(1, -1))[0]
            p = atom.position
            xy.append([p[0], p[1], colors[cl]])
            xz.append([p[0], p[2], colors[cl]])
            yz.append([p[1], p[2], colors[cl]])

        for col, (positions, title) in enumerate(
            zip([xy, xz, yz], ["xy", "xz", "yz"])
        ):
            atom_colors = [_v[-1] for _v in positions]
            positions = np.array([_v[:2] for _v in positions])

            if len(descriptors) == 1:
                ax[col].scatter(
                    positions[:, 0],
                    positions[:, 1],
                    c=atom_colors,
                    alpha=0.7,
                    s=5,
                )

                # add axis labels
                ax[col].arrow(
                    positions[:, 0].min() - 1.0,
                    positions[:, 1].min() - 1.0,
                    2,
                    0,
                    head_width=0.5,
                    head_length=0.5,
                    fc="black",
                    ec="black",
                )

                ax[col].text(
                    positions[:, 0].min() + 2.0,
                    positions[:, 1].min() - 2.0,
                    s=title[0],
                    size=10,
                )

                ax[col].arrow(
                    positions[:, 0].min() - 1.0,
                    positions[:, 1].min() - 1.0,
                    0,
                    2,
                    head_width=0.5,
                    head_length=0.5,
                    fc="black",
                    ec="black",
                )

                ax[col].text(
                    positions[:, 0].min() - 2.0,
                    positions[:, 1].min() + 2.0,
                    s=title[1],
                    size=10,
                )

                ax[col].set_aspect("equal")

                if col == 1:
                    ax[col].set_title(f"{descriptor_name}")
                ax[col].axis("off")
            else:
                ax[row, col].scatter(
                    positions[:, 0],
                    positions[:, 1],
                    c=atom_colors,
                    alpha=0.7,
                    s=5,
                )

                # add axis labels
                ax[row, col].arrow(
                    positions[:, 0].min() - 1.0,
                    positions[:, 1].min() - 1.0,
                    2,
                    0,
                    head_width=0.5,
                    head_length=0.5,
                    fc="black",
                    ec="black",
                )

                ax[row, col].text(
                    positions[:, 0].min() + 2.0,
                    positions[:, 1].min() - 2.0,
                    s=title[0],
                    size=10,
                )

                ax[row, col].arrow(
                    positions[:, 0].min() - 1.0,
                    positions[:, 1].min() - 1.0,
                    0,
                    2,
                    head_width=0.5,
                    head_length=0.5,
                    fc="black",
                    ec="black",
                )

                ax[row, col].text(
                    positions[:, 0].min() - 2.0,
                    positions[:, 1].min() + 2.0,
                    s=title[1],
                    size=10,
                )

                ax[row, col].set_aspect("equal")

                if col == 1:
                    ax[row, col].set_title(f"{descriptor_name}")
                ax[row, col].axis("off")

    title = name.split(os.sep)[-1]
    n = title.split("_")[-1]
    title = "_".join(title.split("_")[:-2])
    title += r" $N$"
    title += f" = {n}"

    plt.tight_layout()
    fig.suptitle(title)
    fig.set_constrained_layout(True)

    plt.savefig(f"{name}.png", dpi=300)

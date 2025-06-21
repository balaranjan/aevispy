# Atomic Environment Visualization using Pythia (aevispy)

[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)

This package finds and colors different coordination environments in a given structure. The common use case is the outputs from MD simulations, where there are different coordination environments present in the output. This uses descriptors from the Pythia package (https://github.com/glotzerlab/pythia/tree/master) and uses Gaussian Mixture Model for unsupervised classification of the environments. The input file number of expected environments (used to specify clusters) are required arguments.

## Demo

![aevispy-demo-gif](assets/aevispy.gif)

## ![Youtube Tutorial](https://youtu.be/VaPWo6KVTyQ)

## How to install `aevispy` locally

`cd` into the project directory:

```bash
cd aevispy
```

Create and activate a new conda environment:

```bash
conda create -n aevispy_env python=3.8
conda activate aevispy_env
```

### Method 1: Install your package with dependencies sourced from pip

It's simple. The only command required is the following:

```bash
pip install .
```

> The above command will automatically install the dependencies listed in `requirements/pip.txt`.

## Verify your package has been installed

Verify the installation:

```bash
pip list
```

## Run

To get started, type

```
aevispy -h

usage: aevispy [-h] [-d  [...]] [-s  [...]] [-f] input_filename envs [envs ...]

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


positional arguments:
  input_filename        Path to the input file
  envs                  Number of environments. e.g. 4 or 4 6

optional arguments:
  -h, --help            show this help message and exit
  -d  [ ...], --desc  [ ...]
                        Descriptors. e.g. 4 or 4 6
  -s  [ ...], --supercell  [ ...]
                        Multipliers for making super cell. e.g. 2 2 2 or 2
  -f , --frame          Frame number to get from gsd file.
```

To color your own files, run

```
aevispy my_structure.cif number_of_envs_expected ...optional options
```

e.g.

```
aevispy CrFe.cif 4 -s 3 -d 8 9
```

## Example Output

After running the command, you will get an output similar to the following:

![Example output](https://github.com/balaranjan/aevispy/blob/main/examples/test_n_4.png)

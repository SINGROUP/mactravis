from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range, zip, round, input, int, pow, object)

import math
import numpy as np
import unittest

import scipy.sparse
from scipy.signal import find_peaks_cwt

from dscribe.descriptors import MBTR

from ase.build import bulk
from ase import Atoms
from ase.visualize import view
import ase.geometry

import matplotlib.pyplot as mpl

from testbaseclass import TestBaseClass

default_grid = {
    "k1": {
        "min": 1,
        "max": 90,
        "sigma": 0.1,
        "n": 50,
    },
    "k2": {
        "min": 0,
        "max": 1/0.7,
        "sigma": 0.1,
        "n": 50,
    },
    "k3": {
        "min": -1,
        "max": 1,
        "sigma": 0.1,
        "n": 50,
    }
}


H2O = Atoms(
    cell=[
        [5.0, 0.0, 0.0],
        [0.0, 5.0, 0.0],
        [0.0, 0.0, 5.0]
    ],
    positions=[
        [0, 0, 0],
        [0.95, 0, 0],
        [0.95*(1+math.cos(76/180*math.pi)), 0.95*math.sin(76/180*math.pi), 0.0]
    ],
    symbols=["H", "O", "H"],
)

H2O_2 = Atoms(
    cell=[[5.0, 0.0, 0], [0, 5, 0], [0, 0, 5.0]],
    positions=[[0.95, 0, 0], [0, 0, 0], [0.95*(1+math.cos(76/180*math.pi)), 0.95*math.sin(76/180*math.pi), 0.0]],
    symbols=["O", "H", "H"],
)

HHe = Atoms(
    cell=[
        [5.0, 0.0, 0.0],
        [0.0, 5.0, 0.0],
        [0.0, 0.0, 5.0]
    ],
    positions=[
        [0, 0, 0],
        [0.71, 0, 0],
    ],
    symbols=["H", "He"],
)

H = Atoms(
    cell=[
        [5.0, 0.0, 0.0],
        [0.0, 5.0, 0.0],
        [0.0, 0.0, 5.0]
    ],
    positions=[
        [0, 0, 0],
    ],
    symbols=["H"],
)


class MBTRTests(TestBaseClass, unittest.TestCase):

    def test_constructor(self):
        """Tests different valid and invalid constructor values.
        """
        # Cannot create a sparse and non-flattened output.
        with self.assertRaises(ValueError):
            MBTR(
                atomic_numbers=[1],
                k=[1],
                grid=default_grid,
                periodic=False,
                flatten=False,
                sparse=True,
            )

        # Invalid k value not in an iterable
        with self.assertRaises(ValueError):
            MBTR(
                atomic_numbers=[1],
                k=0,
                grid=default_grid,
                periodic=False,
            )

        # Invalid k value
        with self.assertRaises(ValueError):
            MBTR(
                atomic_numbers=[1],
                k=[-1, 2],
                grid=default_grid,
                periodic=False,
            )

        # Unsupported k=4
        with self.assertRaises(ValueError):
            MBTR(
                atomic_numbers=[1],
                k={1, 4},
                grid=default_grid,
                periodic=False,
            )

        # Invalid weighting function
        with self.assertRaises(ValueError):
            MBTR(
                atomic_numbers=[1],
                k={2},
                grid=default_grid,
                weighting={"k2": {"function": "exp"}},
                periodic=True,
            )

        # Missing cutoff and scale
        with self.assertRaises(ValueError):
            MBTR(
                atomic_numbers=[1],
                k={2},
                grid=default_grid,
                weighting={"k2": {"function": "exponential"}},
                periodic=True,
            )

        # Missing scale
        with self.assertRaises(ValueError):
            MBTR(
                atomic_numbers=[1],
                k={2},
                grid=default_grid,
                weighting={"k2": {"function": "exponential", "cutoff": 1e-2}},
                periodic=True,
            )

        # Weighting not provided for finite system is fine
        MBTR(
            atomic_numbers=[1],
            k={2},
            grid=default_grid,
            periodic=False,
        )

        # Weighting needs to be provided for periodic system and terms k>1
        with self.assertRaises(ValueError):
            MBTR(
                atomic_numbers=[1],
                k={2},
                grid=default_grid,
                periodic=True,
                weighting={"k2": {"function": "unity"}},
            )

    def test_number_of_features(self):
        """Tests that the reported number of features is correct.
        """
        # K = 1
        n = 100
        atomic_numbers = [1, 8]
        n_elem = len(atomic_numbers)
        mbtr = MBTR(
            atomic_numbers=atomic_numbers,
            k=[1],
            grid={
                "k1": {
                    "min": 1,
                    "max": 8,
                    "sigma": 0.1,
                    "n": 100,
                }
            },
            periodic=False,
            flatten=True
        )
        n_features = mbtr.get_number_of_features()
        expected = n_elem*n
        self.assertEqual(n_features, expected)

        # K = 2
        mbtr = MBTR(
            atomic_numbers=atomic_numbers,
            k={1, 2},
            grid={
                "k1": {
                    "min": 1,
                    "max": 8,
                    "sigma": 0.1,
                    "n": 100,
                },
                "k2": {
                    "min": 0,
                    "max": 1/0.7,
                    "sigma": 0.1,
                    "n": n,
                }
            },
            weighting={"k2": {"function": "exponential", "scale": 0.5, "cutoff": 1e-2}},
            periodic=False,
            flatten=True
        )
        n_features = mbtr.get_number_of_features()
        expected = n_elem*n + 1/2*(n_elem)*(n_elem+1)*n
        self.assertEqual(n_features, expected)

        # K = 3
        mbtr = MBTR(
            atomic_numbers=atomic_numbers,
            k={1, 2, 3},
            grid={
                "k1": {
                    "min": 1,
                    "max": 8,
                    "sigma": 0.1,
                    "n": 100,
                },
                "k2": {
                    "min": 0,
                    "max": 1/0.7,
                    "sigma": 0.1,
                    "n": n,
                },
                "k3": {
                    "min": -1,
                    "max": 1,
                    "sigma": 0.1,
                    "n": n,
                }
            },
            periodic=False,
            flatten=True
        )
        n_features = mbtr.get_number_of_features()
        expected = n_elem*n + 1/2*(n_elem)*(n_elem+1)*n + n_elem*1/2*(n_elem)*(n_elem+1)*n
        self.assertEqual(n_features, expected)

    def test_flatten(self):
        system = H2O
        n = 10
        n_species = len(set(system.get_atomic_numbers()))

        # K1 unflattened
        desc = MBTR([1, 8], k=[1], grid={"k1": {"n": n, "min": 1, "max": 8, "sigma": 0.1}}, periodic=False, flatten=False, sparse=False)
        feat = desc.create(system)["k1"]
        self.assertEqual(feat.shape, (n_species, n))

        # K1 flattened. The sparse matrix only supports 2D matrices, so the first
        # dimension is always present, even if it is of length 1.
        desc = MBTR([1, 8], k=[1], grid={"k1": {"n": n, "min": 1, "max": 8, "sigma": 0.1}}, periodic=False)
        feat = desc.create(system)
        self.assertEqual(feat.shape, (1, n_species*n))

    def test_sparse(self):
        """Tests the sparse matrix creation.
        """
        # Dense
        desc = MBTR([1, 8], k=[1], grid=default_grid, periodic=False, flatten=True, sparse=False)
        vec = desc.create(H2O)
        self.assertTrue(type(vec) == np.ndarray)

        # Sparse
        desc = MBTR([1, 8], k=[1], grid=default_grid, periodic=False, flatten=True, sparse=True)
        vec = desc.create(H2O)
        self.assertTrue(type(vec) == scipy.sparse.coo_matrix)

    def test_k1_weights_and_geoms_finite(self):
        """Tests that the values of the weight and geometry functions are
        correct for the k=1 term.
        """
        mbtr = MBTR([1, 8], k=[1], grid=default_grid, periodic=False)
        mbtr.create(H2O)
        weights = mbtr._k1_weights
        geoms = mbtr._k1_geoms

        # Test against the assumed weights
        assumed_weights = {
            (0,): [1, 1],
            (1,): [1]
        }
        self.dict_comparison(weights, assumed_weights)

        # Test against the assumed geometry values
        assumed_geoms = {
            (0,): [1, 1],
            (1,): [8]
        }
        self.dict_comparison(geoms, assumed_geoms)

        # Test against system with different indexing
        mbtr = MBTR(
            [1, 8],
            k=[1],
            grid={"k1": {"min": 1, "max": 8, "sigma": 0.1, "n": 10}},
            periodic=False
        )
        mbtr.create(H2O_2)
        weights2 = mbtr._k1_weights
        geoms2 = mbtr._k1_geoms
        self.dict_comparison(weights, weights2)
        self.dict_comparison(geoms, geoms2)

    def test_k2_weights_and_geoms_finite(self):
        """Tests that the values of the weight and geometry functions are
        correct for the k=2 term.
        """
        mbtr = MBTR([1, 8], k=[2], grid=default_grid, periodic=False)
        mbtr.create(H2O)
        weights = mbtr._k2_weights
        geoms = mbtr._k2_geoms

        # Test against the assumed weights
        pos = H2O.get_positions()
        assumed_weights = {
            (0, 0): [1],
            (0, 1): [1, 1]
        }
        self.dict_comparison(weights, assumed_weights)

        # Test against the assumed geometry values
        pos = H2O.get_positions()
        assumed_geoms = {
            (0, 0): [1/np.linalg.norm(pos[0] - pos[2])],
            (0, 1): 2*[1/np.linalg.norm(pos[0] - pos[1])]
        }
        self.dict_comparison(geoms, assumed_geoms)

        # Test against system with different indexing
        mbtr = MBTR([1, 8], k=[2], grid=default_grid, periodic=False)
        mbtr.create(H2O_2)
        weights2 = mbtr._k2_weights
        geoms2 = mbtr._k2_geoms
        self.dict_comparison(geoms, geoms2)
        self.dict_comparison(weights, weights2)

    def test_k2_weights_and_geoms_periodic(self):
        """Tests that the values of the weight and geometry functions are
        correct for the k=2 term in periodic systems.
        """
        atoms = Atoms(
            cell=[
                [10, 0, 0],
                [10, 10, 0],
                [10, 0, 10],
            ],
            symbols=["H", "C"],
            scaled_positions=[
                [0.1, 0.5, 0.5],
                [0.9, 0.5, 0.5],
            ]
        )

        mbtr = MBTR(
            [1, 6],
            k=[2],
            grid=default_grid,
            periodic=True,
            weighting={
                "k2": {
                    "function": "exponential",
                    "scale": 0.8,
                    "cutoff": 1e-3
                },
            },
        )
        mbtr.create(atoms)
        weights = mbtr._k2_weights
        geoms = mbtr._k2_geoms

        # Test against the assumed geometry values
        pos = atoms.get_positions()
        distances = np.array([
            np.linalg.norm(pos[0] - pos[1]),
            np.linalg.norm(pos[0] - pos[1] + atoms.get_cell()[0, :]),
            np.linalg.norm(pos[1] - pos[0] - atoms.get_cell()[0, :])
        ])
        assumed_geoms = {
            (0, 1): 1/distances
        }
        self.dict_comparison(geoms, assumed_geoms)

        # Test against the assumed weights
        weight_list = np.exp(-0.8*distances)

        # The periodic distances are halved
        weight_list[1:3] /= 2
        assumed_weights = {
            (0, 1): weight_list
        }

        self.dict_comparison(weights, assumed_weights)

    def test_k2_periodic_cell_translation(self):
        """Tests that the final spectra does not change when translating atoms
        in a periodic cell. This is not trivially true unless the weight of
        distances between periodic neighbours are not halfed. Notice that the
        values of the geometry and weight functions are not equal before
        summing them up in the final graph.
        """
        # Original system with atoms separated by a cell wall
        atoms = Atoms(
            cell=[
                [10, 0, 0],
                [10, 10, 0],
                [10, 0, 10],
            ],
            symbols=["H", "C"],
            scaled_positions=[
                [0.1, 0.5, 0.5],
                [0.9, 0.5, 0.5],
            ],
            pbc=True
        )

        # Translated system with atoms next to each other
        atoms2 = atoms.copy()
        atoms2.translate([5, 0, 0])
        atoms2.wrap()

        mbtr = MBTR(
            [1, 6],
            k=[2],
            grid={
                "k2": {
                    "min": 0,
                    "max": 0.8,
                    "sigma": 0.01,
                    "n": 200,
                }
            },
            periodic=True,
            weighting={
                "k2": {
                    "function": "exponential",
                    "scale": 0.8,
                    "cutoff": 1e-3
                },
            },
        )

        # The resulting spectra should be indentical
        spectra1 = mbtr.create(atoms).toarray()[0, :]
        spectra2 = mbtr.create(atoms2).toarray()[0, :]
        self.assertTrue(np.allclose(spectra1, spectra2, rtol=0, atol=1e-8))

    def test_k3_weights_and_geoms_finite(self):
        """Tests that all the correct angles are present in finite systems.
        There should be n*(n-1)*(n-2)/2 unique angles where the division by two
        gets rid of duplicate angles.
        """
        # Test with water molecule
        mbtr = MBTR([1, 8], k=[3], grid=default_grid, periodic=False)
        mbtr.create(H2O)
        geoms = mbtr._k3_geoms
        weights = mbtr._k3_weights

        assumed_geoms = {
            (0, 1, 0): 1*[math.cos(104/180*math.pi)],
            (0, 0, 1): 2*[math.cos(38/180*math.pi)],
        }
        self.dict_comparison(geoms, assumed_geoms)

        assumed_weights = {
            (0, 1, 0): [1],
            (0, 0, 1): [1, 1],
        }
        self.dict_comparison(weights, assumed_weights)

        # Test against system with different indexing
        mbtr = MBTR([1, 8], k=[3], grid=default_grid, periodic=False)
        mbtr.create(H2O_2)
        weights2 = mbtr._k3_weights
        geoms2 = mbtr._k3_geoms
        self.assertEqual(weights, weights2)
        self.assertEqual(geoms, geoms2)

    def test_k3_geoms_finite_concave(self):
        """Test with four atoms in a "dart"-like arrangement. This arrangement
        has both concave and convex angles.
        """
        atoms = Atoms(
            positions=[
                [0, 0, 0],
                [np.sqrt(2), np.sqrt(2), 0],
                [2*np.sqrt(2), 0, 0],
                [np.sqrt(2), np.tan(np.pi/180*15)*np.sqrt(2), 0],
            ],
            symbols=["H", "H", "H", "He"]
        )
        # view(atoms)

        mbtr = MBTR([1, 2, 10], k=[3], grid=default_grid, periodic=False)
        mbtr.create(atoms)
        angles = mbtr._k3_geoms

        # In finite systems there are n*(n-1)*(n-2)/2 unique angles.
        n_atoms = len(atoms)
        n_angles = sum([len(x) for x in angles.values()])
        self.assertEqual(n_atoms*(n_atoms-1)*(n_atoms-2)/2, n_angles)

        assumed = {
            (0, 1, 0): [math.cos(105/180*math.pi), math.cos(150/180*math.pi), math.cos(105/180*math.pi)],
            (0, 0, 0): [math.cos(90/180*math.pi), math.cos(45/180*math.pi), math.cos(45/180*math.pi)],
            (0, 0, 1): [math.cos(45/180*math.pi), math.cos(30/180*math.pi), math.cos(45/180*math.pi), math.cos(30/180*math.pi), math.cos(15/180*math.pi), math.cos(15/180*math.pi)]
        }
        self.dict_comparison(angles, assumed)

    def test_k3_geoms_and_weights_periodic(self):
        """Tests that the final spectra does not change when translating atoms
        in a periodic cell. This is not trivially true unless the weight of
        distances between periodic neighbours are not halfed. Notice that the
        values of the geometry and weight functions are not equal before
        summing them up in the final graph.
        """
        # Original system with atoms separated by a cell wall
        atoms = Atoms(
            cell=[
                [10, 0, 0],
                [0, 10, 0],
                [0, 0, 10],
            ],
            symbols=3*["H"],
            scaled_positions=[
                [0.05, 0.40, 0.5],
                [0.05, 0.60, 0.5],
                [0.95, 0.5, 0.5],
            ],
            pbc=True
        )
        # view(atoms)

        scale = 0.85
        mbtr = MBTR(
            [1],
            k=[3],
            grid={
                "k3": {
                    "min": -1,
                    "max": 1,
                    "sigma": 0.01,
                    "n": 200,
                }
            },
            periodic=True,
            weighting={
                "k3": {
                    "function": "exponential",
                    "scale": scale,
                    "cutoff": 1e-3
                },
            },
        )
        mbtr.create(atoms)
        weights = mbtr._k3_weights
        geoms = mbtr._k3_geoms

        # Test against the assumed geometry values
        angle_list = np.cos(np.array([45, 45, 90, 90, 45, 45])*np.pi/180)
        assumed_geoms = {
            (0, 0, 0): angle_list
        }
        self.dict_comparison(geoms, assumed_geoms)

        # Test against the assumed weights
        distance = 2+2*np.sqrt(2)  # The total distance around the three atoms
        distances = np.array(6*[distance])
        weight_list = np.exp(-scale*distances)

        # The periodic distances are halved
        weight_list /= 2
        assumed_weights = {
            (0, 0, 0): weight_list
        }

        self.dict_comparison(weights, assumed_weights)

    def test_k3_periodic_cell_translation(self):
        """Tests that the final spectra does not change when translating atoms
        in a periodic cell. This is not trivially true unless the weight of
        distances between periodic neighbours are not halfed. Notice that the
        values of the geometry and weight functions are not equal before
        summing them up in the final graph.
        """
        # Original system with atoms separated by a cell wall
        atoms = Atoms(
            cell=[
                [10, 0, 0],
                [0, 10, 0],
                [0, 0, 10],
            ],
            symbols=["H", "H", "H", "H"],
            scaled_positions=[
                [0.1, 0.50, 0.5],
                [0.1, 0.60, 0.5],
                [0.9, 0.50, 0.5],
                [0.9, 0.60, 0.5],
            ],
            pbc=True
        )

        # Translated system with atoms next to each other
        atoms2 = atoms.copy()
        atoms2.translate([5, 0, 0])
        atoms2.wrap()

        mbtr = MBTR(
            [1],
            k=[3],
            grid={
                "k3": {
                    "min": -1,
                    "max": 1,
                    "sigma": 0.01,
                    "n": 200,
                }
            },
            periodic=True,
            weighting={
                "k3": {
                    "function": "exponential",
                    "scale": 1,
                    "cutoff": 1e-3
                },
            },
        )

        # The resulting spectra should be indentical
        spectra1 = mbtr.create(atoms).toarray()[0, :]
        spectra2 = mbtr.create(atoms2).toarray()[0, :]
        self.assertTrue(np.allclose(spectra1, spectra2, rtol=0, atol=1e-8))

    def test_gaussian_distribution(self):
        """Check that the broadening follows gaussian distribution.
        """
        # Check with normalization
        std = 1
        start = -3
        stop = 11
        n = 500
        mbtr = MBTR(
            [1, 8],
            k=[1],
            grid={
                "k1": {
                    "min": start,
                    "max": stop,
                    "sigma": std,
                    "n": n
                }
            },
            periodic=False,
            normalize_gaussians=True,
            flatten=False,
            sparse=False)
        y = mbtr.create(H2O)["k1"]
        k1_axis = mbtr._axis_k1

        # Find the location of the peaks
        peak1_x = np.searchsorted(k1_axis, 1)
        peak1_y = y[0, peak1_x]
        peak2_x = np.searchsorted(k1_axis, 8)
        peak2_y = y[1, peak2_x]

        # Check against the analytical value
        gaussian = lambda x, mean, sigma: 1/(sigma*np.sqrt(2*np.pi))*np.exp(-(x-mean)**2/(2*sigma**2))
        self.assertTrue(np.allclose(peak1_y, 2*gaussian(1, 1, std), rtol=0, atol=0.001))
        self.assertTrue(np.allclose(peak2_y, gaussian(8, 8, std), rtol=0, atol=0.001))

        # Check the integral
        pdf = y[0, :]
        dx = (stop-start)/(n-1)
        sum_cum = np.sum(0.5*dx*(pdf[:-1]+pdf[1:]))
        exp = 2
        self.assertTrue(np.allclose(sum_cum, exp, rtol=0, atol=0.001))

        # Check without normalization
        std = 1
        start = -3
        stop = 11
        n = 500
        mbtr = MBTR(
            [1, 8],
            k=[1],
            grid={
                "k1": {
                    "min": start,
                    "max": stop,
                    "sigma": std,
                    "n": n
                }
            },
            periodic=False,
            normalize_gaussians=False,
            flatten=False,
            sparse=False)
        y = mbtr.create(H2O)["k1"]
        k1_axis = mbtr._axis_k1

        # Find the location of the peaks
        peak1_x = np.searchsorted(k1_axis, 1)
        peak1_y = y[0, peak1_x]
        peak2_x = np.searchsorted(k1_axis, 8)
        peak2_y = y[1, peak2_x]

        # Check against the analytical value
        gaussian = lambda x, mean, sigma: np.exp(-(x-mean)**2/(2*sigma**2))
        self.assertTrue(np.allclose(peak1_y, 2*gaussian(1, 1, std), rtol=0, atol=0.001))
        self.assertTrue(np.allclose(peak2_y, gaussian(8, 8, std), rtol=0, atol=0.001))

        # Check the integral
        pdf = y[0, :]
        dx = (stop-start)/(n-1)
        sum_cum = np.sum(0.5*dx*(pdf[:-1]+pdf[1:]))
        exp = 2/(1/math.sqrt(2*math.pi*std**2))
        self.assertTrue(np.allclose(sum_cum, exp, rtol=0, atol=0.001))

    def test_symmetries(self):

        def create(system):
            desc = MBTR(
                atomic_numbers=[1, 8],
                k=[1, 2, 3],
                periodic=False,
                grid={
                    "k1": {
                        "min": 10,
                        "max": 18,
                        "sigma": 0.1,
                        "n": 100,
                    },
                    "k2": {
                        "min": 0,
                        "max": 0.7,
                        "sigma": 0.01,
                        "n": 100,
                    },
                    "k3": {
                        "min": -1.0,
                        "max": 1.0,
                        "sigma": 0.05,
                        "n": 100,
                    }
                },
                weighting={
                    "k2": {
                        "function": "exponential",
                        "scale": 0.5,
                        "cutoff": 1e-3
                    },
                    "k3": {
                        "function": "exponential",
                        "scale": 0.5,
                        "cutoff": 1e-3
                    },
                },
                flatten=True
            )
            return desc.create(system)

        # Rotational check
        self.assertTrue(self.is_rotationally_symmetric(create))

        # Translational
        self.assertTrue(self.is_translationally_symmetric(create))

        # Permutational
        self.assertTrue(self.is_permutation_symmetric(create))

    def test_unit_cells(self):
        """Tests that arbitrary unit cells are accepted.
        """
        desc = MBTR(
            atomic_numbers=[1, 8],
            k=[1, 2, 3],
            periodic=False,
            grid={
                "k1": {
                    "min": 10,
                    "max": 18,
                    "sigma": 0.1,
                    "n": 100,
                },
                "k2": {
                    "min": 0,
                    "max": 0.7,
                    "sigma": 0.01,
                    "n": 100,
                },
                "k3": {
                    "min": -1.0,
                    "max": 1.0,
                    "sigma": 0.05,
                    "n": 100,
                }
            },
            weighting={
                "k2": {
                    "function": "exponential",
                    "scale": 0.5,
                    "cutoff": 1e-3
                },
                "k3": {
                    "function": "exponential",
                    "scale": 0.5,
                    "cutoff": 1e-3
                },
            },
            flatten=True
        )

        molecule = H2O.copy()

        molecule.set_cell([
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]
        ])
        nocell = desc.create(molecule)

        molecule.set_pbc(True)
        molecule.set_cell([
            [2.0, 0.0, 0.0],
            [0.0, 2.0, 0.0],
            [0.0, 0.0, 2.0]
        ])
        cubic_cell = desc.create(molecule)

        molecule.set_cell([
            [0.0, 2.0, 2.0],
            [2.0, 0.0, 2.0],
            [2.0, 2.0, 0.0]
        ])
        triclinic_smallcell = desc.create(molecule)

    def test_periodic_images(self):
        """Tests that periodic images are handled correctly.
        """
        decay = 1
        desc = MBTR(
            atomic_numbers=[1],
            k=[1, 2, 3],
            periodic=True,
            grid={
                "k1": {
                    "min": 0,
                    "max": 2,
                    "sigma": 0.1,
                    "n": 21,
                },
                "k2": {
                    "min": 0,
                    "max": 1.0,
                    "sigma": 0.02,
                    "n": 21,
                },
                "k3": {
                    "min": -1.0,
                    "max": 1.0,
                    "sigma": 0.02,
                    "n": 21,
                },
            },
            weighting={
                "k2": {
                    "function": "exponential",
                    "scale": decay,
                    "cutoff": 1e-4
                },
                "k3": {
                    "function": "exponential",
                    "scale": decay,
                    "cutoff": 1e-4
                },
            },
            normalize_by_volume=True,  # This normalizes the spectrum with the system volume
            flatten=True
        )

        # Tests that a system has the same spectrum as the supercell of
        # the same system.
        molecule = H.copy()
        a = 1.5
        molecule.set_cell([
            [a, 0.0, 0.0],
            [0.0, a, 0.0],
            [0.0, 0.0, a]
        ])
        cubic_cell = desc.create(molecule).toarray()
        suce = molecule * (2, 1, 1)
        cubic_suce = desc.create(suce).toarray()

        diff = abs(np.sum(cubic_cell[0, :] - cubic_suce[0, :]))
        cubic_sum = abs(np.sum(cubic_cell[0, :]))
        self.assertTrue(diff/cubic_sum < 0.05)  # A 5% error is tolerated

        # Same test but for triclinic cell
        molecule.set_cell([
            [0.0, 2.0, 1.0],
            [1.0, 0.0, 1.0],
            [1.0, 2.0, 0.0]
        ])

        triclinic_cell = desc.create(molecule).toarray()
        suce = molecule * (2, 1, 1)
        triclinic_suce = desc.create(suce).toarray()

        diff = abs(np.sum(triclinic_cell[0, :] - triclinic_suce[0, :]))
        tricl_sum = abs(np.sum(triclinic_cell[0, :]))
        self.assertTrue(diff/tricl_sum < 0.05)

        # Testing that the same crystal, but different unit cells will have a
        # similar spectrum when they are normalized. There will be small
        # differences in the shape (due to not double counting distances)
        a1 = bulk('H', 'fcc', a=2.0)
        a2 = bulk('H', 'fcc', a=2.0, orthorhombic=True)
        a3 = bulk('H', 'fcc', a=2.0, cubic=True)

        triclinic_cell = desc.create(a1).toarray()
        orthorhombic_cell = desc.create(a2).toarray()
        cubic_cell = desc.create(a3).toarray()

        diff1 = abs(np.sum(triclinic_cell[0, :] - orthorhombic_cell[0, :]))
        diff2 = abs(np.sum(triclinic_cell[0, :] - cubic_cell[0, :]))
        tricl_sum = abs(np.sum(triclinic_cell[0, :]))
        self.assertTrue(diff1/tricl_sum < 0.05)
        self.assertTrue(diff2/tricl_sum < 0.05)

        # Tests that the correct peak locations are present in a cubic periodic
        # system.
        desc = MBTR(
            atomic_numbers=[1],
            k=[3],
            periodic=True,
            grid={
                "k3": {
                    "min": -1.1,
                    "max": 1.1,
                    "sigma": 0.010,
                    "n": 600,
                },
            },
            weighting={
                "k3": {
                    "function": "exponential",
                    "scale": decay,
                    "cutoff": 1e-4
                },
            },
            normalize_by_volume=True,  # This normalizes the spectrum with the system volume
            flatten=True
        )
        a = 2.2
        system = Atoms(
            cell=[
                [a, 0.0, 0.0],
                [0.0, a, 0.0],
                [0.0, 0.0, a]
            ],
            positions=[
                [0, 0, 0],
            ],
            symbols=["H"],
        )
        cubic_spectrum = desc.create(system).toarray()[0, :]
        x3 = desc._axis_k3

        peak_ids = find_peaks_cwt(cubic_spectrum, [2])
        peak_locs = x3[peak_ids]

        assumed_peaks = np.cos(np.array(
            [
                180,
                90,
                np.arctan(np.sqrt(2))*180/np.pi,
                45,
                np.arctan(np.sqrt(2)/2)*180/np.pi,
                0
            ])*np.pi/180
        )
        self.assertTrue(np.allclose(peak_locs, assumed_peaks, rtol=0, atol=5*np.pi/180))

        # Tests that the correct peak locations are present in a system with a
        # non-cubic basis
        desc = MBTR(
            atomic_numbers=[1],
            k=[3],
            periodic=True,
            grid={
                "k3": {
                    "min": -1.0,
                    "max": 1.0,
                    "sigma": 0.035,
                    "n": 200,
                },
            },
            weighting={
                "k3": {
                    "function": "exponential",
                    "scale": 1.5,
                    "cutoff": 1e-4
                },
            },
            normalize_by_volume=True,  # This normalizes the spectrum with the system volume
            flatten=True
        )
        a = 2.2
        system = Atoms(
            cell=[
                [a, 0.0, 0.0],
                [0.0, a, 0.0],
                [0.0, 0.0, a]
            ],
            positions=[
                [0, 0, 0],
            ],
            symbols=["H"],
        )
        angle = 30
        system = Atoms(
            cell=ase.geometry.cellpar_to_cell([3*a, a, a, angle, 90, 90]),
            positions=[
                [0, 0, 0],
            ],
            symbols=["H"],
        )
        tricl_spectrum = desc.create(system).toarray()
        x3 = desc._axis_k3

        peak_ids = find_peaks_cwt(tricl_spectrum[0, :], [3])
        peak_locs = x3[peak_ids]

        angle = (6)/(np.sqrt(5)*np.sqrt(8))
        assumed_peaks = np.cos(np.array([180, 105, 75, 51.2, 30, 0])*np.pi/180)
        self.assertTrue(np.allclose(peak_locs, assumed_peaks, rtol=0, atol=5*np.pi/180))

    def test_grid_change(self):
        """Tests that the calculation of MBTR with new grid settings works.
        """
        grid = {
            "k1": {
                "min": 1,
                "max": 8,
                "sigma": 0.1,
                "n": 50,
            },
            "k2": {
                "min": 0,
                "max": 1/0.7,
                "sigma": 0.1,
                "n": 50,
            },
            "k3": {
                "min": -1,
                "max": 1,
                "sigma": 0.1,
                "n": 50,
            }
        }

        desc = MBTR(
            atomic_numbers=[1, 8],
            k=[1, 2, 3],
            periodic=True,
            grid=grid,
            weighting={
                "k2": {
                    "function": "exponential",
                    "scale": 1,
                    "cutoff": 1e-4
                },
                "k3": {
                    "function": "exponential",
                    "scale": 1,
                    "cutoff": 1e-4
                }
            },
            flatten=True
        )

        # Initialize scalars with a given system
        desc.initialize_scalars(H2O)

        # Request spectrum with different grid settings
        spectrum1 = desc.create_with_grid().toarray()[0]
        grid["k1"]["sigma"] = 0.09
        grid["k2"]["sigma"] = 0.09
        grid["k3"]["sigma"] = 0.09
        spectrum2 = desc.create_with_grid(grid).toarray()[0]

        # Check that contents are not equal, but have same peaks
        self.assertFalse(np.allclose(spectrum1, spectrum2))
        peak_ids1 = find_peaks_cwt(spectrum1, [5])
        peak_ids2 = find_peaks_cwt(spectrum2, [5])
        self.assertTrue(np.array_equal(peak_ids1, peak_ids2))

        # # Visually check the contents
        # x = np.arange(len(spectrum1))
        # mpl.plot(x, spectrum1)
        # mpl.plot(x, spectrum2)
        # mpl.legend()
        # mpl.show()

    def test_basis(self):
        """Tests that the output vectors behave correctly as a basis.
        """
        sys1 = Atoms(symbols=["H"], positions=[[0, 0, 0]], cell=[2, 2, 2], pbc=True)
        sys2 = Atoms(symbols=["O"], positions=[[0, 0, 0]], cell=[2, 2, 2], pbc=True)
        sys3 = sys2*[2, 2, 2]

        desc = MBTR(
            atomic_numbers=[1, 8],
            k=[1, 2, 3],
            periodic=True,
            grid={
                "k1": {
                    "min": 1,
                    "max": 8,
                    "sigma": 0.1,
                    "n": 50,
                },
                "k2": {
                    "min": 0,
                    "max": 1/0.7,
                    "sigma": 0.1,
                    "n": 50,
                },
                "k3": {
                    "min": -1,
                    "max": 1,
                    "sigma": 0.1,
                    "n": 50,
                }
            },
            weighting={
                "k2": {
                    "function": "exponential",
                    "scale": 1,
                    "cutoff": 1e-4
                },
                "k3": {
                    "function": "exponential",
                    "scale": 1,
                    "cutoff": 1e-4
                }
            },
            flatten=True
        )

        # Create normalized vectors for each system
        vec1 = desc.create(sys1).toarray()[0, :]
        vec1 /= np.linalg.norm(vec1)

        vec2 = desc.create(sys2).toarray()[0, :]
        vec2 /= np.linalg.norm(vec2)

        vec3 = desc.create(sys3).toarray()[0, :]
        vec3 /= np.linalg.norm(vec3)

        # The dot-product should be zero when there are no overlapping elements
        dot = np.dot(vec1, vec2)
        self.assertEqual(dot, 0)

        # The dot-product should be rougly one for a primitive cell and a supercell
        dot = np.dot(vec2, vec3)
        self.assertTrue(abs(dot-1) < 1e-3)


if __name__ == '__main__':
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(MBTRTests))
    alltests = unittest.TestSuite(suites)
    result = unittest.TextTestRunner(verbosity=0).run(alltests)

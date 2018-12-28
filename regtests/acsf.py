from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range, zip, round, input, int, pow, object)

import math
import unittest

import numpy as np

import scipy.linalg

from dscribe.descriptors import ACSF
from testbaseclass import TestBaseClass

from ase import Atoms


H2O = Atoms(
    cell=[
        [15.0, 0.0, 0.0],
        [0.0, 15.0, 0.0],
        [0.0, 0.0, 15.0]
    ],
    positions=[
        [0, 0, 0],
        [0.95, 0, 0],
        [0.95*(1+math.cos(76/180*math.pi)), 0.95*math.sin(76/180*math.pi), 0.0]
    ],
    symbols=["H", "O", "H"],
)

H = Atoms(
    cell=[
        [15.0, 0.0, 0.0],
        [0.0, 15.0, 0.0],
        [0.0, 0.0, 15.0]
    ],
    positions=[
        [0, 0, 0],

    ],
    symbols=["H"],
)

default_desc = ACSF(
    atomic_numbers=[1, 8],
    g2_params=[[1, 2]],
    # g2_params=[[1, 2], [4, 5]],
    # g3_params=[1, 2, 3, 4],
    # g4_params=[[1, 2, 3], [3, 1, 4], [4, 5, 6], [7, 8, 9]],
    # g5_params=[[1, 2, 3], [3, 1, 4], [4, 5, 6], [7, 8, 9]],
)


class ACSFTests(TestBaseClass, unittest.TestCase):

    def test_constructor(self):
        """Tests different valid and invalid constructor values.
        """
        # Invalid atomic_numbers
        with self.assertRaises(ValueError):
            ACSF(atomic_numbers=None)

        # Invalid bond_params
        with self.assertRaises(ValueError):
            ACSF(atomic_numbers=[1, 6, 8], g2_params=[1, 2, 3])

        # Invalid bond_cos_params
        with self.assertRaises(ValueError):
            ACSF(atomic_numbers=[1, 6, 8], g3_params=[[1, 2], [3, 1]])

        # Invalid bond_cos_params
        with self.assertRaises(ValueError):
            ACSF(atomic_numbers=[1, 6, 8], g3_params=[[1, 2, 4], [3, 1]])

        # Invalid ang4_params
        with self.assertRaises(ValueError):
            ACSF(atomic_numbers=[1, 6, 8], g4_params=[[1, 2], [3, 1]])

        # Invalid ang5_params
        with self.assertRaises(ValueError):
            ACSF(atomic_numbers=[1, 6, 8], g5_params=[[1, 2], [3, 1]])

    def test_number_of_features(self):
        """Tests that the reported number of features is correct.
        """
        atomic_numbers = [1, 8]
        n_elem = len(atomic_numbers)

        desc = ACSF(atomic_numbers=atomic_numbers)
        n_features = desc.get_number_of_features()
        self.assertEqual(n_features, n_elem)

        desc = ACSF(atomic_numbers=atomic_numbers, g2_params=[[1, 2], [4, 5]])
        n_features = desc.get_number_of_features()
        self.assertEqual(n_features, n_elem * (2+1))

        desc = ACSF(atomic_numbers=[1, 8], g3_params=[1, 2, 3, 4])
        n_features = desc.get_number_of_features()
        self.assertEqual(n_features, n_elem * (4+1))

        desc = ACSF(atomic_numbers=[1, 8], g4_params=[[1, 2, 3], [3, 1, 4], [4, 5, 6], [7, 8, 9]])
        n_features = desc.get_number_of_features()
        self.assertEqual(n_features, n_elem + 4 * 3)

        desc = ACSF(atomic_numbers=[1, 8], g2_params=[[1, 2], [4, 5]], g3_params=[1, 2, 3, 4],
            g4_params=[[1, 2, 3], [3, 1, 4], [4, 5, 6], [7, 8, 9]])
        n_features = desc.get_number_of_features()
        self.assertEqual(n_features, n_elem * (1 + 2 + 4) + 4 * 3)

    def test_flatten(self):
        """Tests the flattening.
        """

    def test_sparse(self):
        """Tests the sparse matrix creation.
        """
        # Sparse
        default_desc.sparse = True
        vec = default_desc.create(H2O)
        self.assertTrue(type(vec) == scipy.sparse.coo_matrix)

        # Dense
        default_desc.sparse = False
        vec = default_desc.create(H2O)
        self.assertTrue(type(vec) == np.ndarray)

    def test_features(self):
        """Tests that the correct features are present in the descriptor.
        """
        eta = 1
        rs = 0.5
        kappa = 1
        eta = 1
        lmbd = 1
        zeta = 1

        # Test against assumed values
        # print(H2O)
        dist_oh = H2O.get_distance(0, 1)
        dist_hh = H2O.get_distance(0, 2)
        ang_hoh = H2O.get_angle(0, 1, 2) * np.pi / 180.0
        ang_hho = H2O.get_angle(1, 0, 2) * np.pi / 180.0
        ang_ohh = - H2O.get_angle(2, 0, 1) * np.pi / 180.0
        rc = 5.0

        # G1
        desc = ACSF(atomic_numbers=[1, 8])
        acsfg1 = desc.create(H2O)
        g1_ho = 0.5 * (np.cos(np.pi*dist_oh / rc) + 1)
        g1_hh = 0.5 * (np.cos(np.pi*dist_hh / rc) + 1)
        g1_oh = 2 * 0.5 * (np.cos(np.pi*dist_oh / rc) + 1)
        self.assertAlmostEqual(acsfg1[0, 0], g1_hh)
        self.assertAlmostEqual(acsfg1[0, 1], g1_ho)
        self.assertAlmostEqual(acsfg1[1, 0], g1_oh)

        # G2
        desc = ACSF(atomic_numbers=[1, 8], g2_params=[[eta, rs]])
        acsfg2 = desc.create(H2O)
        g2_hh = np.exp(-eta * np.power((dist_hh - rs), 2)) * g1_hh
        g2_ho = np.exp(-eta * np.power((dist_oh - rs), 2)) * g1_ho
        g2_oh = np.exp(-eta * np.power((dist_oh - rs), 2)) * g1_oh
        self.assertAlmostEqual(acsfg2[0, 1], g2_hh)
        self.assertAlmostEqual(acsfg2[0, 3], g2_ho)
        self.assertAlmostEqual(acsfg2[1, 1], g2_oh)

        # G3
        desc = ACSF(atomic_numbers=[1, 8], g3_params=[kappa])
        acsfg3 = desc.create(H2O)
        g3_hh = np.cos(dist_hh * kappa) * g1_hh
        g3_ho = np.cos(dist_oh * kappa) * g1_ho
        g3_oh = np.cos(dist_oh * kappa) * g1_oh
        self.assertAlmostEqual(acsfg3[0, 1], g3_hh)
        self.assertAlmostEqual(acsfg3[0, 3], g3_ho)
        self.assertAlmostEqual(acsfg3[1, 1], g3_oh)

        # G4
        desc = ACSF(atomic_numbers=[1, 8], g4_params=[[eta, lmbd, zeta]])
        acsfg4 = desc.create(H2O)
        gauss = np.exp(-eta * (2 * dist_oh * dist_oh + dist_hh * dist_hh)) * g1_ho * g1_hh * g1_ho
        g4_h_ho = np.power(2, 1 - zeta) * np.power((1 + lmbd*np.cos(ang_hho)), zeta) * gauss
        g4_h_oh = np.power(2, 1 - zeta) * np.power((1 + lmbd*np.cos(ang_ohh)), zeta) * gauss
        g4_o_hh = np.power(2, 1 - zeta) * np.power((1 + lmbd*np.cos(ang_hoh)), zeta) * gauss
        self.assertAlmostEqual(acsfg4[0, 3], g4_h_ho)
        self.assertAlmostEqual(acsfg4[2, 3], g4_h_oh)
        self.assertAlmostEqual(acsfg4[1, 2], g4_o_hh)

        # G5
        desc = ACSF(atomic_numbers=[1, 8], g5_params=[[eta, lmbd, zeta]])
        acsfg5 = desc.create(H2O)
        gauss = np.exp(-eta * (dist_oh * dist_oh + dist_hh * dist_hh)) * g1_ho * g1_hh
        g5_h_ho = np.power(2, 1 - zeta) * np.power((1 + lmbd*np.cos(ang_hho)), zeta) * gauss
        g5_h_oh = np.power(2, 1 - zeta) * np.power((1 + lmbd*np.cos(ang_ohh)), zeta) * gauss
        g5_o_hh = np.power(2, 1 - zeta) * np.power((1 + lmbd*np.cos(ang_hoh)), zeta) * np.exp(-eta * (2 * dist_oh * dist_oh)) * g1_ho * g1_ho
        self.assertAlmostEqual(acsfg5[0, 3], g5_h_ho)
        self.assertAlmostEqual(acsfg5[2, 3], g5_h_oh)
        self.assertAlmostEqual(acsfg5[1, 2], g5_o_hh)

    def test_symmetries(self):
        """Tests translational and rotational symmetries
        """
        def create(system):
            acsf = default_desc.create(system)
            return acsf

        # Rotational check
        self.assertTrue(self.is_rotationally_symmetric(create))

        # Translational
        self.assertTrue(self.is_translationally_symmetric(create))

    def test_basis(self):
        """Tests that the output vectors behave correctly as a basis.
        """
        sys1 = Atoms(symbols=["H", "H"], positions=[[0, 0, 0], [1, 0, 0]], cell=[2, 2, 2], pbc=True)
        sys2 = Atoms(symbols=["H", "O"], positions=[[0, 0, 0], [1, 0, 0]], cell=[2, 2, 2], pbc=True)

        # Create normalized vectors for each system
        vec1 = default_desc.create(sys1, positions=[0])[0, :]
        vec1 /= np.linalg.norm(vec1)

        vec2 = default_desc.create(sys2, positions=[0])[0, :]
        vec2 /= np.linalg.norm(vec2)

        vec3 = default_desc.create(sys1, positions=[1])[0, :]
        vec3 /= np.linalg.norm(vec3)

        vec4 = default_desc.create(sys2, positions=[1])[0, :]
        vec4 /= np.linalg.norm(vec4)

        # The dot-product should be zero when the environment does not have the
        # same elements
        dot = np.dot(vec1, vec2)
        self.assertEqual(dot, 0)

        # The dot-product should be one for identical environments, even if the
        # central atom is different
        dot = np.dot(vec3, vec4)
        self.assertEqual(dot, 1)

    def test_unit_cells(self):
        """Tests if arbitrary unit cells are accepted.
        """
        # No cell
        molecule = H2O.copy()
        molecule.set_cell([
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]
        ])
        nocell = default_desc.create(molecule)

        # Large cell
        molecule.set_pbc(True)
        molecule.set_cell([
            [20.0, 0.0, 0.0],
            [0.0, 30.0, 0.0],
            [0.0, 0.0, 40.0]
        ])
        largecell = default_desc.create(molecule)

        # Cubic cell
        molecule.set_cell([
            [2.0, 0.0, 0.0],
            [0.0, 2.0, 0.0],
            [0.0, 0.0, 2.0]
        ])
        cubic_cell = default_desc.create(molecule)

        # Triclinic cell
        molecule.set_cell([
            [0.0, 2.0, 2.0],
            [2.0, 0.0, 2.0],
            [2.0, 2.0, 0.0]
        ])
        triclinic_smallcell = default_desc.create(molecule)


if __name__ == '__main__':
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(ACSFTests))
    alltests = unittest.TestSuite(suites)
    result = unittest.TextTestRunner(verbosity=0).run(alltests)

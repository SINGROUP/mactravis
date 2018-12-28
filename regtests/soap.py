from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range, zip, round, input, int, pow, object)

import math
import unittest

import numpy as np

import scipy
import scipy.sparse
from scipy.integrate import tplquad
from scipy.linalg import sqrtm

from dscribe.descriptors import SOAP
from testbaseclass import TestBaseClass

from ase import Atoms


H2O = Atoms(
    cell=[
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
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


# class SoapTests(TestBaseClass, unittest.TestCase):
class SoapTests(unittest.TestCase):

    # def test_constructor(self):
        # """Tests different valid and invalid constructor values.
        # """
        # Invalid atomic numbers
        # with self.assertRaises(ValueError):
            # SOAP(atomic_numbers=[-1, 2], rcut=5, nmax=5, lmax=5, periodic=True)

        # Invalid gaussian width
        # with self.assertRaises(ValueError):
            # SOAP(atomic_numbers=[-1, 2], rcut=5, sigma=0, nmax=5, lmax=5, periodic=True)
        # with self.assertRaises(ValueError):
            # SOAP(atomic_numbers=[-1, 2], rcut=5, sigma=-1, nmax=5, lmax=5, periodic=True)

        # Invalid rcut
        # with self.assertRaises(ValueError):
            # SOAP(atomic_numbers=[-1, 2], rcut=0.5, sigma=0, nmax=5, lmax=5, periodic=True)

    # def test_number_of_features(self):
        # """Tests that the reported number of features is correct.
        # """
        # lmax = 5
        # nmax = 5
        # n_elems = 2
        # desc = SOAP(atomic_numbers=[1, 8], rcut=5, nmax=nmax, lmax=lmax, periodic=True)

        # Test that the reported number of features matches the expected
        # n_features = desc.get_number_of_features()
        # n_blocks = n_elems*(n_elems+1)/2
        # expected = int((lmax + 1) * nmax * (nmax + 1) / 2 * n_blocks)
        # self.assertEqual(n_features, expected)

        # Test that the outputted number of features matches the reported
        # n_features = desc.get_number_of_features()
        # vec = desc.create(H2O)
        # self.assertEqual(n_features, vec.shape[1])

    # def test_multiple_species(self):
        # """Tests multiple species are handled correctly.
        # """
        # lmax = 5
        # nmax = 5
        # atomic_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        # desc = SOAP(atomic_numbers=atomic_numbers, rcut=5, nmax=nmax, lmax=lmax, periodic=False, sparse=False, normalize=True)

        # pos = np.expand_dims(np.linspace(0, 8, 8), 1)
        # pos = np.hstack((pos, pos, pos))
        # sys = Atoms(
            # symbols=atomic_numbers[0:8],
            # positions=pos,
            # pbc=False
        # )
        # vec1 = desc.create(sys)

        # sys2 = Atoms(
            # symbols=atomic_numbers[8:],
            # positions=pos,
            # pbc=False
        # )
        # vec2 = desc.create(sys2)

        # sys3 = Atoms(
            # symbols=atomic_numbers[4:12],
            # positions=pos,
            # pbc=False
        # )
        # vec3 = desc.create(sys3)

        # dot1 = np.dot(vec1[6, :], vec2[6, :])
        # dot2 = np.dot(vec1[3, :], vec3[3, :])
        # dot3 = np.dot(vec2[3, :], vec3[3, :])

        # The dot product for systems without overlap in species should be zero
        # self.assertTrue(abs(dot1) <= 1e-8)

        # The systems with overlap in the elements should have onerlap in the
        # dot product
        # self.assertTrue(abs(dot2) > 1e-3)
        # self.assertTrue(abs(dot3) > 1e-3)

    # def test_flatten(self):
        # """Tests the flattening.
        # """

    # def test_soap_structure(self):
        # """Tests that when no positions are given, the SOAP for the full
        # structure is calculated.
        # """
        # lmax = 5
        # nmax = 5
        # desc = SOAP(atomic_numbers=[1, 8], rcut=5, nmax=nmax, lmax=lmax, periodic=True)

        # vec = desc.create(H2O)
        # self.assertTrue(vec.shape[0] == 3)

    # def test_sparse(self):
        # """Tests the sparse matrix creation.
        # """
        # Dense
        # desc = SOAP(atomic_numbers=[1, 8], rcut=5, nmax=5, lmax=5, periodic=True, sparse=False)
        # vec = desc.create(H2O)
        # self.assertTrue(type(vec) == np.ndarray)

        # Sparse
        # desc = SOAP(atomic_numbers=[1, 8], rcut=5, nmax=5, lmax=5, periodic=True, sparse=True)
        # vec = desc.create(H2O)
        # self.assertTrue(type(vec) == scipy.sparse.coo_matrix)

    # def test_positions(self):
        # """Tests that different positions are handled correctly.
        # """
        # desc = SOAP([1, 6, 8], 10.0, 2, 0, periodic=False, crossover=True)
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O, positions=[[0, 0, 0]]).shape[1])
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O, positions=[0]).shape[1])
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O).shape[1])

        # desc = SOAP([1, 6, 8], 10.0, 2, 0, periodic=True, crossover=True,)
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O, positions=[[0, 0, 0]]).shape[1])
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O, positions=[0]).shape[1])
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O).shape[1])

        # desc = SOAP([1, 6, 8], 10.0, 2, 0, periodic=True, crossover=False,)
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O, positions=[[0, 0, 0]]).shape[1])
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O, positions=[0]).shape[1])
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O).shape[1])

        # desc = SOAP([1, 6, 8], 10.0, 2, 0, periodic=False, crossover=False,)
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O, positions=[[0, 0, 0]]).shape[1])
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O, positions=[0]).shape[1])
        # self.assertEqual(desc.get_number_of_features(), desc.create(H2O).shape[1])

        # with self.assertRaises(ValueError):
            # desc.create(H2O, positions=['a'])

    # def test_unit_cells(self):
        # """Tests if arbitrary unit cells are accepted"""
        # desc = SOAP([1, 6, 8], 10.0, 2, 0, periodic=False, crossover=True,)

        # molecule = H2O.copy()

        # molecule.set_cell([
            # [0.0, 0.0, 0.0],
            # [0.0, 0.0, 0.0],
            # [0.0, 0.0, 0.0]
        # ])

        # nocell = desc.create(molecule, positions=[[0, 0, 0]])

        # desc = SOAP([1, 6, 8], 10.0, 2, 0, periodic=True, crossover=True,)

        # Invalid unit cell
        # molecule.set_cell([
            # [0.0, 0.0, 0.0],
            # [0.0, 0.0, 0.0],
            # [0.0, 0.0, 0.0]
        # ])
        # with self.assertRaises(ValueError):
            # desc.create(molecule, positions=[[0, 0, 0]])

        # molecule.set_pbc(True)
        # molecule.set_cell([
        # [20.0, 0.0, 0.0],
        # [0.0, 30.0, 0.0],
        # [0.0, 0.0, 40.0]
            # ],
            # )

        # largecell = desc.create(molecule, positions=[[0, 0, 0]])

        # molecule.set_cell([
            # [2.0, 0.0, 0.0],
            # [0.0, 2.0, 0.0],
            # [0.0, 0.0, 2.0]
        # ])

        # cubic_cell = desc.create(molecule, positions=[[0, 0, 0]])

        # molecule.set_cell([
            # [0.0, 2.0, 2.0],
            # [2.0, 0.0, 2.0],
            # [2.0, 2.0, 0.0]
        # ])

        # triclinic_smallcell = desc.create(molecule, positions=[[0, 0, 0]])

    # def test_is_periodic(self):
        # """Tests whether periodic images are seen by the descriptor"""
        # desc = SOAP([1, 6, 8], 10.0, 2, 0, periodic=False, crossover=True,)

        # H2O.set_pbc(False)
        # nocell = desc.create(H2O, positions=[[0, 0, 0]])

        # H2O.set_pbc(True)
        # H2O.set_cell([
            # [2.0, 0.0, 0.0],
            # [0.0, 2.0, 0.0],
            # [0.0, 0.0, 2.0]
        # ])
        # desc = SOAP([1, 6, 8], 10.0, 2, 0, periodic=True, crossover=True,)

        # cubic_cell = desc.create(H2O, positions=[[0, 0, 0]])

        # self.assertTrue(np.sum(cubic_cell) > 0)

    # def test_periodic_images(self):
        # """Tests the periodic images seen by the descriptor
        # """
        # desc = SOAP([1, 6, 8], 10.0, 2, 0, periodic=False, crossover=True,)

        # molecule = H2O.copy()

        # non-periodic for comparison
        # molecule.set_cell([
            # [0.0, 0.0, 0.0],
            # [0.0, 0.0, 0.0],
            # [0.0, 0.0, 0.0]
        # ])
        # nocell = desc.create(molecule, positions=[[0, 0, 0]]).toarray()

        # Make periodic
        # desc = SOAP([1, 6, 8], 10.0, 2, 0, periodic=True, crossover=True,)
        # molecule.set_pbc(True)

        # Cubic
        # molecule.set_cell([
            # [3.0, 0.0, 0.0],
            # [0.0, 3.0, 0.0],
            # [0.0, 0.0, 3.0]
        # ])
        # cubic_cell = desc.create(molecule, positions=[[0, 0, 0]]).toarray()
        # suce = molecule * (2, 1, 1)
        # cubic_suce = desc.create(suce, positions=[[0, 0, 0]]).toarray()

        # Triclinic
        # molecule.set_cell([
            # [0.0, 2.0, 2.0],
            # [2.0, 0.0, 2.0],
            # [2.0, 2.0, 0.0]
        # ])
        # triclinic_cell = desc.create(molecule, positions=[[0, 0, 0]]).toarray()
        # suce = molecule * (2, 1, 1)
        # triclinic_suce = desc.create(suce, positions=[[0, 0, 0]]).toarray()

        # self.assertTrue(np.sum(np.abs((nocell[:3] - cubic_suce[:3]))) > 0.1)
        # self.assertAlmostEqual(np.sum(cubic_cell[:3] - cubic_suce[:3]), 0)
        # self.assertAlmostEqual(np.sum(triclinic_cell[:3] - triclinic_suce[:3]), 0)

    # def test_symmetries(self):
        # """Tests that the descriptor has the correct invariances.
        # """
        # def create(system):
            # desc = SOAP(
                # atomic_numbers=system.get_atomic_numbers(),
                # rcut=8.0,
                # lmax=5,
                # nmax=5,
                # periodic=False,
                # crossover=True
            # )
            # return desc.create(system)

        # Rotational check
        # self.assertTrue(self.is_rotationally_symmetric(create))

        # Translational
        # self.assertTrue(self.is_translationally_symmetric(create))

        # Permutational
        # self.assertTrue(self.is_permutation_symmetric(create))

    # def test_average(self):
        # """Tests that the average output is created correctly.
        # """
        # sys = Atoms(symbols=["H", "C"], positions=[[-1, 0, 0], [1, 0, 0]], cell=[2, 2, 2], pbc=True)

        # Create the average output
        # desc = SOAP(
            # atomic_numbers=[1, 6, 8],
            # rcut=5,
            # nmax=3,
            # lmax=5,
            # periodic=False,
            # crossover=True,
            # average=True,
            # sparse=False
        # )
        # average = desc.create(sys)[0, :]

        # Create individual output for both atoms
        # desc = SOAP(
            # atomic_numbers=[1, 6, 8],
            # rcut=5,
            # nmax=3,
            # lmax=5,
            # periodic=False,
            # crossover=True,
            # average=False,
            # sparse=False
        # )
        # first = desc.create(sys, positions=[0])[0, :]
        # second = desc.create(sys, positions=[1])[0, :]

        # Check that the normalization is done correctly, by first normalizing
        # the outputs and then averaging them.
        # first_normalized = first/np.linalg.norm(first, axis=0)
        # second_normalized = second/np.linalg.norm(second, axis=0)
        # assumed_average = (first_normalized+second_normalized)/2
        # self.assertTrue(np.array_equal(average, assumed_average))

    # def test_basis(self):
        # """Tests that the output vectors behave correctly as a basis.
        # """
        # sys1 = Atoms(symbols=["H", "H"], positions=[[1, 0, 0], [0, 1, 0]], cell=[2, 2, 2], pbc=True)
        # sys2 = Atoms(symbols=["O", "O"], positions=[[1, 0, 0], [0, 1, 0]], cell=[2, 2, 2], pbc=True)
        # sys3 = Atoms(symbols=["C", "C"], positions=[[1, 0, 0], [0, 1, 0]], cell=[2, 2, 2], pbc=True)
        # sys4 = Atoms(symbols=["H", "C"], positions=[[-1, 0, 0], [1, 0, 0]], cell=[2, 2, 2], pbc=True)
        # sys5 = Atoms(symbols=["H", "C"], positions=[[1, 0, 0], [0, 1, 0]], cell=[2, 2, 2], pbc=True)
        # sys6 = Atoms(symbols=["H", "O"], positions=[[1, 0, 0], [0, 1, 0]], cell=[2, 2, 2], pbc=True)
        # sys7 = Atoms(symbols=["C", "O"], positions=[[1, 0, 0], [0, 1, 0]], cell=[2, 2, 2], pbc=True)

        # desc = SOAP(
            # atomic_numbers=[1, 6, 8],
            # rcut=5,
            # nmax=3,
            # lmax=5,
            # periodic=False,
            # crossover=True,
            # normalize=True,
            # sparse=False
        # )

        # Create normalized vectors for each system
        # vec1 = desc.create(sys1, positions=[[0, 0, 0]])[0, :]
        # vec2 = desc.create(sys2, positions=[[0, 0, 0]])[0, :]
        # vec3 = desc.create(sys3, positions=[[0, 0, 0]])[0, :]
        # vec4 = desc.create(sys4, positions=[[0, 0, 0]])[0, :]
        # vec5 = desc.create(sys5, positions=[[0, 0, 0]])[0, :]
        # vec6 = desc.create(sys6, positions=[[0, 0, 0]])[0, :]
        # vec7 = desc.create(sys7, positions=[[0, 0, 0]])[0, :]

        # The dot-product should be zero when there are no overlapping elements
        # dot = np.dot(vec1, vec2)
        # self.assertEqual(dot, 0)
        # dot = np.dot(vec2, vec3)
        # self.assertEqual(dot, 0)

        # The dot-product should be non-zero when there are overlapping elements
        # dot = np.dot(vec4, vec5)
        # self.assertNotEqual(dot, 0)

        # Check that self-terms are in correct location
        # n_elem_feat = desc.get_number_of_element_features()
        # h_part1 = vec1[0:n_elem_feat]
        # h_part2 = vec2[0:n_elem_feat]
        # h_part4 = vec4[0:n_elem_feat]
        # self.assertNotEqual(np.sum(h_part1), 0)
        # self.assertEqual(np.sum(h_part2), 0)
        # self.assertNotEqual(np.sum(h_part4), 0)

        # Check that cross terms are in correct location
        # hc_part1 = vec1[1*n_elem_feat:2*n_elem_feat]
        # hc_part4 = vec4[1*n_elem_feat:2*n_elem_feat]
        # co_part6 = vec6[4*n_elem_feat:5*n_elem_feat]
        # co_part7 = vec7[4*n_elem_feat:5*n_elem_feat]
        # self.assertEqual(np.sum(hc_part1), 0)
        # self.assertNotEqual(np.sum(hc_part4), 0)
        # self.assertEqual(np.sum(co_part6), 0)
        # self.assertNotEqual(np.sum(co_part7), 0)

    # def test_poly_rbf(self):
        # """Tests that the polynomial radial basis set works as expected.
        # """
        # lmax = 5
        # nmax = 5
        # desc = SOAP(atomic_numbers=[1, 8], rcut=5, nmax=nmax, lmax=lmax, rbf="polynomial", periodic=True)

        # vec = desc.create(H2O, positions=[0])

    # def test_rbf_orthonormality(self):
        # """Tests that the gto radial basis functions are orthonormal.
        # """
        # sigma = 0.15
        # rcut = 2.0
        # nmax = 2
        # lmax = 3
        # soap = SOAP(atomic_numbers=[1], lmax=lmax, nmax=nmax, sigma=sigma, rcut=rcut, crossover=True, sparse=False)
        # alphas = np.reshape(soap.alphas, [10, nmax])
        # betas = np.reshape(soap.betas, [10, nmax, nmax])

        # nr = 10000
        # n_basis = 0
        # functions = np.zeros((nmax, lmax+1, nr))

        # Form the radial basis functions
        # for n in range(nmax):
            # for l in range(lmax+1):
                # gto = np.zeros((nr))
                # rspace = np.linspace(0, rcut+5, nr)
                # for k in range(nmax):
                    # gto += betas[l, n, k]*rspace**l*np.exp(-alphas[l, k]*rspace**2)
                # n_basis += 1
                # functions[n, l, :] = gto

        # Calculate the overlap integrals
        # S = np.zeros((nmax, nmax))
        # l = 0
        # for l in range(lmax+1):
            # for i in range(nmax):
                # for j in range(nmax):
                    # overlap = np.trapz(rspace**2*functions[i, l, :]*functions[j, l, :], dx=(rcut+5)/nr)
                    # S[i, j] = overlap

            # Check that the basis functions for each l are orthonormal
            # diff = S-np.eye(nmax)
            # self.assertTrue(np.allclose(diff, np.zeros((nmax, nmax)), atol=1e-3))

    # def test_gto_integration(self):
        # """Tests that the completely analytical partial power spectrum with the
        # GTO basis corresponds to the easier-to-code but less performant
        # numerical integration done with python.
        # """
        # sigma = 0.55
        # rcut = 2.0
        # nmax = 2
        # lmax = 2

        # Limits for radius
        # r1 = 0.
        # r2 = rcut+5

        # Limits for theta
        # t1 = 0
        # t2 = np.pi

        # Limits for phi
        # p1 = 0
        # p2 = 2*np.pi

        # positions = np.array([[0.5, 0.7, 0.9], [-0.3, 0.5, 0.4]])
        # symbols = np.array(["H", "C"])
        # system = Atoms(positions=positions, symbols=symbols)

        # atomic_numbers = system.get_atomic_numbers()
        # elements = set(system.get_atomic_numbers())
        # n_elems = len(elements)

        # Calculate the analytical power spectrum and the weights and decays of
        # the radial basis functions.
        # soap = SOAP(atomic_numbers=atomic_numbers, lmax=lmax, nmax=nmax, sigma=sigma, rcut=rcut, crossover=True, sparse=False)
        # analytical_power_spectrum = soap.create(system, positions=[[0, 0, 0]])[0]
        # alphagrid = np.reshape(soap.alphas, [10, nmax])
        # betagrid = np.reshape(soap.betas, [10, nmax, nmax])

        # coeffs = np.zeros((n_elems, nmax, lmax+1, 2*lmax+1))
        # for iZ, Z in enumerate(elements):
            # indices = np.argwhere(atomic_numbers == Z)[0]
            # elem_pos = positions[indices]
            # for n in range(nmax):
                # for l in range(lmax+1):
                    # for im, m in enumerate(range(-l, l+1)):

                        # Calculate numerical coefficients
                        # def soap_coeff(phi, theta, r):

                            # Regular spherical harmonic
                            # ylm_comp = scipy.special.sph_harm(np.abs(m), l, phi, theta)  NOTE: scipy swaps phi and theta

                            # Construct real (tesseral) spherical harmonics for
                            # easier integration without having to worry about the
                            # imaginary part
                            # ylm_real = np.real(ylm_comp)
                            # ylm_imag = np.imag(ylm_comp)
                            # if m < 0:
                                # ylm = np.sqrt(2)*(-1)**m*ylm_imag
                            # elif m == 0:
                                # ylm = ylm_comp
                            # else:
                                # ylm = np.sqrt(2)*(-1)**m*ylm_real

                            # Spherical gaussian type orbital
                            # gto = 0
                            # for i in range(nmax):
                                # i_alpha = alphagrid[l, i]
                                # i_beta = betagrid[l, n, i]
                                # i_gto = i_beta*r**l*np.exp(-i_alpha*r**2)
                                # gto += i_gto

                            # Atomic density
                            # rho = 0
                            # for i_pos in elem_pos:
                                # ix = i_pos[0]
                                # iy = i_pos[1]
                                # iz = i_pos[2]
                                # ri_squared = ix**2+iy**2+iz**2
                                # rho += np.exp(-1/(2*sigma**2)*(r**2 + ri_squared - 2*r*(np.sin(theta)*np.cos(phi)*ix + np.sin(theta)*np.sin(phi)*iy + np.cos(theta)*iz)))

                            # Jacobian
                            # jacobian = np.sin(theta)*r**2

                            # return gto*ylm*rho*jacobian

                        # cnlm = tplquad(
                            # soap_coeff,
                            # r1,
                            # r2,
                            # lambda r: t1,
                            # lambda r: t2,
                            # lambda r, theta: p1,
                            # lambda r, theta: p2,
                            # epsabs=0.001,
                            # epsrel=0.001,
                        # )
                        # integral, error = cnlm
                        # coeffs[iZ, n, l, im] = integral

        # Calculate the partial power spectrum
        # numerical_power_spectrum = []
        # for zi in range(n_elems):
            # for zj in range(n_elems):
                # for l in range(lmax+1):
                    # for ni in range(nmax):
                        # for nj in range(nmax):
                            # if nj >= ni:
                                # if zj >= zi:
                                    # value = np.dot(coeffs[zi, ni, l, :], coeffs[zj, nj, l, :])
                                    # prefactor = np.pi*np.sqrt(8/(2*l+1))
                                    # value *= prefactor
                                    # numerical_power_spectrum.append(value)

        # print("Numerical: {}".format(numerical_power_spectrum))
        # print("Analytical: {}".format(analytical_power_spectrum))

        # self.assertTrue(np.allclose(numerical_power_spectrum, analytical_power_spectrum, atol=0, rtol=0.01))

    def test_poly_integration(self):
        """Tests that the partial power spectrum with the polynomial basis done
        with C corresponds to the easier-to-code but less performant
        integration done with python.
        """
        sigma = 0.55
        rcut = 2.0
        nmax = 0
        lmax = 2

        # Limits for radius
        r1 = 0.
        r2 = rcut+5

        # Limits for theta
        t1 = 0
        t2 = np.pi

        # Limits for phi
        p1 = 0
        p2 = 2*np.pi

        positions = np.array([[0.5, 0.7, 0.9], [-0.3, 0.5, 0.4]])
        symbols = np.array(["H", "C"])
        system = Atoms(positions=positions, symbols=symbols)

        atomic_numbers = system.get_atomic_numbers()
        elements = set(system.get_atomic_numbers())
        n_elems = len(elements)

        # These are the analytically calculable overlap coefficients for the
        # polynomial basis: Integrate[(r - rc)^(a + 2) (r - rc)^(b + 2) r^2,
        # {r, 0, rc}]
        # S = np.zeros((nmax, nmax))
        # for i in range(nmax):
            # for j in range(nmax):
                # S[i, j] = -(2*(-rcut)**(7+i+j))/((5+i+j)*(6+i+j)*(7+i+j))
        # betas = sqrtm(np.linalg.inv(S))

        # Calculate the functions on a grid
        # nr = 10000
        # functions = np.zeros((nmax, nr))
        # rspace = np.linspace(0, rcut, nr)
        # for n in range(nmax):
            # functions[n, :] = (rcut-rspace)**(n+2)

        # # Calculate the weight matrix that orthonormalizes the set
        # S = np.zeros((nmax, nmax))
        # for i in range(nmax):
            # for j in range(nmax):
                # overlap = np.trapz(rspace**2*functions[i, :]*functions[j, :], dx=(rcut)/nr)
                # S[i, j] = overlap
        # betas = sqrtm(np.linalg.inv(S))

        # Calculate overlap again to check that the set is really orthonormal
        # orth_func = np.dot(betas, functions)
        # S = np.zeros((nmax, nmax))
        # for i in range(nmax):
            # for j in range(nmax):
                # overlap = np.trapz(rspace**2*orth_func[i, :]*orth_func[j, :], dx=(rcut)/nr)
                # S[i, j] = overlap
        # print(S)

        # Calculate the analytical power spectrum and the weights and decays of
        # the radial basis functions.
        soap = SOAP(atomic_numbers=atomic_numbers, lmax=lmax, nmax=nmax, sigma=sigma, rcut=rcut, rbf="polynomial", crossover=True, sparse=False)
        analytical_power_spectrum = soap.create(system, positions=[[0, 0, 0]])[0]

        # coeffs = np.zeros((n_elems, nmax, lmax+1, 2*lmax+1))
        # for iZ, Z in enumerate(elements):
            # indices = np.argwhere(atomic_numbers == Z)[0]
            # elem_pos = positions[indices]
            # for n in range(nmax):
                # for l in range(lmax+1):
                    # for im, m in enumerate(range(-l, l+1)):

                        # # Calculate numerical coefficients
                        # def soap_coeff(phi, theta, r):

                            # # Regular spherical harmonic
                            # ylm_comp = scipy.special.sph_harm(np.abs(m), l, phi, theta)  # NOTE: scipy swaps phi and theta

                            # # Construct real (tesseral) spherical harmonics for
                            # # easier integration without having to worry about the
                            # # imaginary part
                            # ylm_real = np.real(ylm_comp)
                            # ylm_imag = np.imag(ylm_comp)
                            # if m < 0:
                                # ylm = np.sqrt(2)*(-1)**m*ylm_imag
                            # elif m == 0:
                                # ylm = ylm_comp
                            # else:
                                # ylm = np.sqrt(2)*(-1)**m*ylm_real

                            # # Polynomial basis
                            # poly = 0
                            # for k in range(nmax):
                                # poly += betas[n, k]*(rcut-np.clip(r, 0, rcut))**(k+2)

                            # # Atomic density
                            # rho = 0
                            # for i_pos in elem_pos:
                                # ix = i_pos[0]
                                # iy = i_pos[1]
                                # iz = i_pos[2]
                                # ri_squared = ix**2+iy**2+iz**2
                                # rho += np.exp(-1/(2*sigma**2)*(r**2 + ri_squared - 2*r*(np.sin(theta)*np.cos(phi)*ix + np.sin(theta)*np.sin(phi)*iy + np.cos(theta)*iz)))

                            # # Jacobian
                            # jacobian = np.sin(theta)*r**2

                            # return poly*ylm*rho*jacobian

                        # cnlm = tplquad(
                            # soap_coeff,
                            # r1,
                            # r2,
                            # lambda r: t1,
                            # lambda r: t2,
                            # lambda r, theta: p1,
                            # lambda r, theta: p2,
                            # epsabs=0.0001,
                            # epsrel=0.0001,
                        # )
                        # integral, error = cnlm
                        # coeffs[iZ, n, l, im] = integral

        # Calculate the partial power spectrum
        # numerical_power_spectrum = []
        # for zi in range(n_elems):
            # for zj in range(n_elems):
                # for l in range(lmax+1):
                    # for ni in range(nmax):
                        # for nj in range(nmax):
                            # if nj >= ni:
                                # if zj >= zi:
                                    # value = np.dot(coeffs[zi, ni, l, :], coeffs[zj, nj, l, :])
                                    # prefactor = np.pi*np.sqrt(8/(2*l+1))
                                    # value *= prefactor
                                    # numerical_power_spectrum.append(value)

        # print("Numerical: {}".format(numerical_power_spectrum))
        # print("Analytical: {}".format(analytical_power_spectrum))

        # self.assertTrue(np.allclose(numerical_power_spectrum, analytical_power_spectrum, atol=0, rtol=0.01))

if __name__ == '__main__':
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(SoapTests))
    alltests = unittest.TestSuite(suites)
    result = unittest.TextTestRunner(verbosity=0).run(alltests)

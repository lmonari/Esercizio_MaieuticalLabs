import unittest

from random import randrange

from exercise import PolynomialCreator


class MyTestCase(unittest.TestCase):

    def test_poly_coeffs(self):
        n1 = randrange(-100, 100)
        n2 = randrange(-100, 100)
        exp_range = [min(n1, n2), max(n1, n2)]
        n_terms_min = 2
        n_terms_max = abs(exp_range[1] - exp_range[0]) + 1
        n1 = randrange(-100, 100)
        n2 = randrange(-100, 100)
        coeff_range = [min(n1, n2), max(n1, n2)]
        pl = PolynomialCreator(n_terms_min, n_terms_max, coeff_range, exp_range)

        n_terms = randrange(n_terms_min, n_terms_max)
        self.assertEqual(len(pl._polynomial_coefficients(n_terms)), n_terms)


if __name__ == '__main__':
    unittest.main()

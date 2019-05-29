import unittest
from paganini.tuner import *

class TestTuner(unittest.TestCase):

    def test_singular_btrees(self):
        """ Singular tuning of binary trees
            B = 1 + Z * B^2."""

        spec = Specification()
        z, B = spec.variable(), spec.variable()
        spec.add(B, 1 + z * B ** 2)

        spec.run_singular_tuner(z)

        self.assertAlmostEqual(z.value, 0.25)
        self.assertAlmostEqual(B.value, 2)

    def test_singular_motzkin_trees(self):
        """ Singular tuning of Motzkin trees
            M = Z * SEQ<=2(M). """

        spec = Specification()
        z, M = spec.variable(), spec.variable()
        spec.add(M, z * spec.Seq(M, leq(2)))

        spec.run_singular_tuner(z)

        self.assertAlmostEqual(z.value, 0.333333333333334)
        self.assertAlmostEqual(M.value, 1.0)

    def test_singular_motzkin_trees2(self):
        """ Singular tuning of Motzkin trees
            M = Z + Z * M + Z * M^2. """

        spec = Specification()
        z, M = spec.variable(), spec.variable()
        spec.add(M, z + z * M + z * M ** 2)

        spec.run_singular_tuner(z)

        self.assertAlmostEqual(z.value, 0.333333333333334)
        self.assertAlmostEqual(M.value, 1.0)

    def test_singular_trees(self):
        """ Singular tuning of plane trees
            T = Z * SEQ(T)."""

        spec = Specification()
        z, T = spec.variable(), spec.variable()
        spec.add(T, z * spec.Seq(T))

        spec.run_singular_tuner(z)

        self.assertAlmostEqual(z.value, 0.25)
        self.assertAlmostEqual(T.value, 0.5)

    def test_singular_lambda_terms(self):
        """ Singular tuning of plain lambda terms
            L = Z * SEQ(Z) + Z * L + Z * L^2."""

        spec = Specification()
        z, L, D = spec.variable(), spec.variable(), spec.variable()
        spec.add(L, D + z * L + z * L ** 2)
        spec.add(D, z + z * D)

        spec.run_singular_tuner(z)

        self.assertAlmostEqual(z.value, 0.295597742522085)
        self.assertAlmostEqual(L.value, 1.19148788395312)

    def test_singular_lambda_terms2(self):
        """ Singular tuning of plain lambda terms
            L = Z * SEQ(Z) + Z * L + Z * L^2."""

        spec = Specification()
        z, L = spec.variable(), spec.variable()
        spec.add(L, z * spec.Seq(z) + z * L + z * L ** 2)

        spec.run_singular_tuner(z)

        self.assertAlmostEqual(z.value, 0.295597742522085)
        self.assertAlmostEqual(L.value, 1.19148788395312)

    def test_singular_polya_trees(self):
        """ Singular tuning of Polya trees
            T = Z * SEQ(T)."""

        spec = Specification()
        z, T = spec.variable(), spec.variable()
        spec.add(T, z * spec.MSet(T))

        spec.run_singular_tuner(z)

        self.assertAlmostEqual(z.value, 0.338322112871298)
        self.assertAlmostEqual(T.value, 1)

    def test_singular_custom_trees(self):
        """ Singular tuning of some custom trees defined by
            T = Z + Z * SEQ_>=2(T)."""

        params = Params(Type.ALGEBRAIC)
        params.max_iters = 100 # required

        spec = Specification()
        z, T = spec.variable(), spec.variable()
        spec.add(T, z + z * spec.Seq(T, geq(2)))

        spec.run_singular_tuner(z, params)

        self.assertAlmostEqual(z.value, 0.333333333333335)
        self.assertAlmostEqual(T.value, 0.499999999999993)

    def test_binary_words(self):
        """ Singular tuning of binary words.
            B = SEQ(Z + Z). """

        spec = Specification()
        z, B = spec.variable(), spec.variable()
        spec.add(B, spec.Seq(z + z))

        spec.run_singular_tuner(z)
        self.assertAlmostEqual(z.value, 0.5, 5)

    def test_compositions(self):
        """ Singular tuning of all compositions.
            C = SEQ(Z * SEQ(Z)). """

        params = Params(Type.RATIONAL)
        params.max_iters = 8000 # required

        spec = Specification()
        z, C = spec.variable(), spec.variable()
        spec.add(C, spec.Seq(z * spec.Seq(z)))

        spec.run_singular_tuner(z, params)
        self.assertAlmostEqual(z.value, 0.5, 5)

    def test_compositions_with_restricted_summands(self):
        """ Singular tuning of compositions with restricted summands in {1,2}.
            C = SEQ(Z + Z^2). """

        spec = Specification()
        z, C = spec.variable(), spec.variable()
        spec.add(C, spec.Seq(z + z**2))

        spec.run_singular_tuner(z)
        self.assertAlmostEqual(z.value, 0.618034527351341, 5) # golden ratio

    def test_singular_partitions(self):
        """ Singular tuning of partitions
            P = MSET(SEQ_{k >= 1}(Z))."""

        params = Params(Type.ALGEBRAIC)
        params.max_iters = 1000 # required

        spec = Specification()
        z, P = spec.variable(), spec.variable()
        spec.add(P, spec.MSet(z * spec.Seq(z)))

        spec.run_singular_tuner(z, params)
        self.assertAlmostEqual(z.value, 0.999992520391430, 5)

    def test_minus_constant(self):

        spec = Specification()
        z, T = spec.variable(), spec.variable()
        spec.add(T, spec.Seq(2*z) - 1)

        spec.run_singular_tuner(z)
        self.assertAlmostEqual(z.value, 0.5, 5)

    def test_minus_constant2(self):

        spec = Specification()
        z, T = spec.variable(), spec.variable()
        spec.add(T, z - 2 * T)

        try:
            spec.run_singular_tuner(z)
        except ValueError:
            self.assertTrue(z.value is None)

    def test_binary_necklaces(self):
        """ Singular tuning of neckleces build using two kinds of beads.
            N = CYC(Z + Z)."""

        spec = Specification()
        z, N = spec.variable(), spec.variable()
        spec.add(N, spec.Cyc(z + z))

        spec.run_singular_tuner(z)
        self.assertAlmostEqual(z.value, 0.5, 5)

    def test_cyclic_compositions(self):
        """ Singular tuning of cyclic compositions.
            C = CYC(Z * SEQ(Z))."""

        spec = Specification()
        z, C = spec.variable(), spec.variable()
        spec.add(C, spec.Cyc(z * spec.Seq(z)))

        spec.run_singular_tuner(z)
        self.assertAlmostEqual(z.value, 0.5, 5)

    def test_unlabelled_functional_graphs(self):
        """ Singular tuning of unlabelled functional graphs.
            F = MSet(K)
            K = CYC(U)
            U = Z * MSet(U)."""

        spec = Specification()
        z, F = spec.variable(), spec.variable()
        K, U = spec.variable(), spec.variable()
        spec.add(F, spec.MSet(K))
        spec.add(K, spec.Cyc(U))
        spec.add(U, z * spec.MSet(U))

        spec.run_singular_tuner(z)
        self.assertAlmostEqual(z.value, 0.3383218568992077, 5)

if __name__ == '__main__':
    unittest.main()

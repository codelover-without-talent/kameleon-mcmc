"""
Copyright (c) 2013-2014 Heiko Strathmann
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 *
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 *
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the author.
"""

from numpy import zeros, ones, asarray
import numpy
from numpy.random import rand, randint
import unittest

from kameleon_mcmc.distribution.Distribution import Sample
from kameleon_mcmc.distribution.proposals.AddDelSwapProposal import AddDelSwapProposal


class AddDelSwapProposalUnitTest(unittest.TestCase):
    def test_contructor_wrong_mu_type_float(self):
        mu = 0
        spread = 1.
        self.assertRaises(TypeError, AddDelSwapProposal, mu, spread)
        
    def test_contructor_wrong_mu_type_none(self):
        mu = None
        spread = 1.
        self.assertRaises(TypeError, AddDelSwapProposal, mu, spread)

    def test_contructor_wrong_mu_dim_too_large(self):
        mu = zeros((1, 2), dtype=numpy.bool8)
        spread = 1.
        self.assertRaises(ValueError, AddDelSwapProposal, mu, spread)
        
    def test_contructor_wrong_mu_dimension_0(self):
        mu = zeros(0, dtype=numpy.bool8)
        spread = 1.
        self.assertRaises(ValueError, AddDelSwapProposal, mu, spread)
        
    def test_contructor_wrong_spread_type_int(self):
        mu = zeros(2, dtype=numpy.bool8)
        spread = 1
        self.assertRaises(TypeError, AddDelSwapProposal, mu, spread)
                          
    def test_contructor_wrong_spread_type_none(self):
        mu = zeros(2, dtype=numpy.bool8)
        spread = None
        self.assertRaises(TypeError, AddDelSwapProposal, mu, spread)
        
    def test_contructor_wrong_spread_range_0(self):
        mu = ones(2, dtype=numpy.bool8)
        spread = 0.
        self.assertRaises(ValueError, AddDelSwapProposal, mu, spread)
        
    def test_contructor_wrong_spread_range_1(self):
        mu = ones(2, dtype=numpy.bool8)
        spread = 1.
        self.assertRaises(ValueError, AddDelSwapProposal, mu, spread)
        
    def test_contructor_correct_mu(self):
        mu = ones(2, dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        self.assertTrue(mu is dist.mu)
        
    def test_contructor_correct_spread(self):
        mu = ones(2, dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        self.assertEqual(spread, dist.spread)
        
#     
    def test_sample_wrong_n_sameller_zero(self):
        mu = randint(0, 2, 10).astype(numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        self.assertRaises(ValueError, dist.sample, -1)
     
    def test_sample_wrong_n_type_none(self):
        mu = randint(0, 2, 10).astype(numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        self.assertRaises(TypeError, dist.sample, None)
          
    def test_sample_wrong_n_type_float(self):
        mu = randint(0, 2, 10).astype(numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        self.assertRaises(TypeError, dist.sample, float(1.))
          
    def test_sample_type(self):
        mu = randint(0, 2, 10).astype(numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        s = dist.sample(1)
        self.assertTrue(isinstance(s, Sample))
          
    def test_sample_samples_dtype(self):
        mu = randint(0, 2, 10).astype(numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        s = dist.sample(1)
        self.assertEqual(s.samples.dtype, numpy.bool8)
          
    def test_sample_dim(self):
        n = 3
        d = 2
        mu = randint(0, 2, d).astype(numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        s = dist.sample(n)
        self.assertEqual(s.samples.shape, (n, d))
        
    def test_sample_many_no_checks(self):
        num_runs = 1
        for _ in range(num_runs):
            n = randint(1, 10)
            d = 10
            mu = randint(0, 2, d).astype(numpy.bool8)
            #print 'mu='
            #print mu
            spread = rand()
            dist = AddDelSwapProposal(mu, spread)
            sample = dist.sample(n)
#                 
    def test_log_pdf_wrong_type_none(self):
        d = 2
        mu = randint(0, 2, d).astype(numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        self.assertRaises(TypeError, dist.log_pdf, None)
         
    def test_log_pdf_wrong_type_float(self):
        d = 2
        mu = randint(0, 2, d).astype(numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        self.assertRaises(TypeError, dist.log_pdf, float(1.))
         
    def test_log_pdf_wrong_array_dimension_1(self):
        d = 2
        mu = randint(0, 2, d).astype(numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        self.assertRaises(TypeError, dist.log_pdf, zeros(1))
         
    def test_log_pdf_wrong_array_dimension_3(self):
        d = 2
        mu = randint(0, 2, d).astype(numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        self.assertRaises(TypeError, dist.log_pdf, zeros(3))
         
    def test_log_pdf_wrong_dimension(self):
        d = 2
        mu = randint(0, 2, d).astype(numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        self.assertRaises(ValueError, dist.log_pdf, zeros((1, 3)))
          
    def test_log_pdf_type(self):
        mu = asarray([0], dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        X = asarray([[0]], dtype=numpy.bool8)
        self.assertEqual(type(dist.log_pdf(X)), numpy.ndarray)
     
    def test_log_pdf_returned_array_dimension_1d_X(self):
        n = 1
        mu = asarray([0], dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        X = asarray([[0]], dtype=numpy.bool8)
        self.assertEqual(dist.log_pdf(X).shape, (n,))
        
    def test_log_pdf_returned_array_dimension_2d_X(self):
        n = 1
        mu = asarray([0, 0], dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        X = asarray([[0, 1]], dtype=numpy.bool8)
        self.assertEqual(dist.log_pdf(X).shape, (n,))
        
    def test_log_pdf_returned_array_dimension_multiple_X_1d(self):
        n = 2
        mu = asarray([0], dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        X = asarray([[1], [0]], dtype=numpy.bool8)
        self.assertEqual(dist.log_pdf(X).shape, (n,))
        
    def test_log_pdf_returned_array_dimension_multiple_X_2d(self):
        n = 2
        mu = asarray([0, 1], dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        X = asarray([[1, 0], [0, 0]], dtype=numpy.bool8)
        self.assertEqual(dist.log_pdf(X).shape, (n,))
        
            
    def test_log_pdf_1n_1d_add(self):
        mu = asarray([0], dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        X = asarray([[1]], dtype=numpy.bool8)
        result = dist.log_pdf(X)
        expected = zeros(1) + numpy.nan
#         self.assertAlmostEqual(norm(result - expected), 0)
        
    def test_log_pdf_1n_1d_swap(self):
        mu = asarray([1], dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        X = asarray([[1]], dtype=numpy.bool8)
        result = dist.log_pdf(X)
        expected = zeros(1) + numpy.nan
#         self.assertAlmostEqual(norm(result - expected), 0)

    def test_log_pdf_1n_1d_del(self):
        mu = asarray([1], dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        X = asarray([[0]], dtype=numpy.bool8)
        result = dist.log_pdf(X)
        expected = zeros(1) + numpy.nan
#         self.assertAlmostEqual(norm(result - expected), 0)
        
    def test_log_pdf_2n_1d_add(self):
        mu = asarray([0], dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        X = asarray([[1], [0]], dtype=numpy.bool8)
        result = dist.log_pdf(X)
        expected = zeros(2) + numpy.nan
#         self.assertAlmostEqual(norm(result - expected), 0)
        
    def test_log_pdf_1n_2d(self):
        mu = asarray([0, 1], dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        X = asarray([[1, 1]], dtype=numpy.bool8)
        result = dist.log_pdf(X)
        expected = zeros(1) + numpy.nan
#         self.assertAlmostEqual(norm(result - expected), 0)
        
    def test_log_pdf_2n_2d(self):
        mu = asarray([0, 1], dtype=numpy.bool8)
        spread = .5
        dist = AddDelSwapProposal(mu, spread)
        X = asarray([[1, 1], [0, 1]], dtype=numpy.bool8)
        result = dist.log_pdf(X)
        expected = zeros(2) + numpy.nan
#         self.assertAlmostEqual(norm(result - expected), 0)

if __name__ == "__main__":
    unittest.main()

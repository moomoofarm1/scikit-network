#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for embeddings metrics"""

import unittest
import numpy as np
from sknetwork.toy_graphs import house_graph, star_wars_villains_graph
from sknetwork.utils.sparse_lowrank import SparseLR


class TestSparseLowRank(unittest.TestCase):

    def setUp(self):
        self.undirected = SparseLR(house_graph(), [(np.ones(5), np.ones(5))])
        self.bipartite = SparseLR(star_wars_villains_graph(), [(np.ones(4), np.ones(3))])

    def test_product(self):
        prod = self.undirected.dot(np.ones(5))
        self.assertEqual(prod.shape, (5,))
        prod = self.bipartite.dot(np.ones(3))
        self.assertEqual(np.linalg.norm(prod - np.array([5., 4., 6., 5.])), 0.)

    def test_transposition(self):
        transposed = self.undirected.T
        error = (self.undirected.sparse_mat - transposed.sparse_mat).data
        self.assertEqual(abs(error).sum(), 0.)
        transposed = self.bipartite.T
        x, y = transposed.low_rank_tuples[0]
        self.assertTrue((x == np.ones(3)).all())
        self.assertTrue((y == np.ones(4)).all())

import unittest
import sys
import os
import numpy as np

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from hybrid_collective_mind import AntColony

class TestAntColony(unittest.TestCase):
    def setUp(self):
        self.colony = AntColony(n_ants=10)

    def test_evaluate_path_ideal_sequence(self):
        # The ideal sequence is ['KAREN', 'AI', 'CERBER', 'GUARDIAN']
        # Sequence bonus: 4 + 3 + 2 + 1 = 10.0
        # Loopback bonus (starts with KAREN, ends with GUARDIAN): + 2.0
        # Full path bonus (all 4 nodes): + 3.0
        # Duplicates: 0
        # Expected: 15.0
        path = ['KAREN', 'AI', 'CERBER', 'GUARDIAN']
        score = self.colony._evaluate_path(path)
        self.assertEqual(score, 15.0)

    def test_evaluate_path_with_return_to_karen(self):
        # path = ['KAREN', 'AI', 'CERBER', 'GUARDIAN', 'KAREN']
        # Sequence bonus: 10.0 (zip only goes up to len(ideal_sequence))
        # Loopback bonus: 0 (ends with KAREN, not GUARDIAN)
        # Full path bonus: + 3.0
        # Duplicates: 1 (KAREN is repeated) -> -0.5
        # Expected: 10.0 + 3.0 - 0.5 = 12.5
        path = ['KAREN', 'AI', 'CERBER', 'GUARDIAN', 'KAREN']
        score = self.colony._evaluate_path(path)
        self.assertEqual(score, 12.5)

    def test_evaluate_path_duplicates_penalty(self):
        # path = ['KAREN', 'KAREN', 'KAREN']
        # Sequence bonus: 4.0 (index 0 matches, 1 and 2 don't)
        # Loopback bonus: 0
        # Full path bonus: 0
        # Duplicates: 3 - 1 = 2 -> -1.0
        # Expected: 4.0 - 1.0 = 3.0
        path = ['KAREN', 'KAREN', 'KAREN']
        score = self.colony._evaluate_path(path)
        self.assertEqual(score, 3.0)

    def test_evaluate_path_minimum_score(self):
        # path with negative or zero raw score should return 0.1
        # Using many duplicates of a node that doesn't match the first few positions
        # path = ['GUARDIAN'] * 10
        # Sequence bonus: Index 3 matches GUARDIAN -> +1.0
        # Duplicates: 10 - 1 = 9 -> -4.5
        # Raw score: 1.0 - 4.5 = -3.5
        # Expected: 0.1 (due to max(score, 0.1))
        path = ['GUARDIAN'] * 10
        score = self.colony._evaluate_path(path)
        self.assertEqual(score, 0.1)

    def test_evaluate_path_partial_sequence(self):
        # path = ['KAREN', 'CERBER']
        # Sequence bonus: 4.0 (index 0 matches KAREN, index 1: CERBER != AI)
        # Loopback bonus: 0 (ends with CERBER)
        # Full path bonus: 0
        # Duplicates: 0
        # Expected: 4.0
        path = ['KAREN', 'CERBER']
        score = self.colony._evaluate_path(path)
        self.assertEqual(score, 4.0)

if __name__ == '__main__':
    unittest.main()

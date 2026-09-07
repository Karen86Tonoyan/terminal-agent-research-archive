import unittest
import sys
import os
from unittest.mock import MagicMock

# Add the root directory and CERBER/src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../CERBER/src')))

from core.conscience import AIConscience, ConscienceVerdict, TonoyanFilter

class TestAIConscience(unittest.TestCase):
    def setUp(self):
        self.conscience = AIConscience('pl')

    def test_default_approve(self):
        # Default TonoyanFilter.evaluate returns (True, "OK", 0.9)
        # All filters are default, so confidence should be 0.9
        decision = self.conscience.judge("TEST_001", {"any": "context"})
        self.assertEqual(decision.verdict, ConscienceVerdict.APPROVE)
        self.assertGreaterEqual(decision.confidence, 0.85)
        self.assertEqual(len(self.conscience.decisions), 1)

    def test_verdict_question(self):
        # Mock evaluate to return 0.75 confidence
        for f in self.conscience.FILTERS:
            f.evaluate = MagicMock(return_value=(True, "MOCKED", 0.75))

        decision = self.conscience.judge("TEST_002", {})
        self.assertEqual(decision.verdict, ConscienceVerdict.QUESTION)
        self.assertAlmostEqual(decision.confidence, 0.75)

    def test_verdict_warn(self):
        # Mock evaluate to return 0.6 confidence
        for f in self.conscience.FILTERS:
            f.evaluate = MagicMock(return_value=(True, "MOCKED", 0.6))

        decision = self.conscience.judge("TEST_003", {})
        self.assertEqual(decision.verdict, ConscienceVerdict.WARN)
        self.assertAlmostEqual(decision.confidence, 0.6)

    def test_verdict_block(self):
        # Mock evaluate to return 0.4 confidence
        for f in self.conscience.FILTERS:
            f.evaluate = MagicMock(return_value=(False, "MOCKED", 0.4))

        decision = self.conscience.judge("TEST_004", {})
        self.assertEqual(decision.verdict, ConscienceVerdict.BLOCK)
        self.assertAlmostEqual(decision.confidence, 0.4)

    def test_reasoning_content(self):
        decision = self.conscience.judge("TEST_005", {})
        for f in self.conscience.FILTERS:
            expected_reason = f"#{f.filter_id} {f.name}: OK"
            self.assertIn(expected_reason, decision.reasoning)

if __name__ == '__main__':
    unittest.main()

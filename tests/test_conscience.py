import unittest
import sys
import os
from unittest.mock import MagicMock

# Add the root directory to sys.path to import CERBER.src.core.conscience
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CERBER.src.core.conscience import TonoyanFilter, AIConscience, ConscienceVerdict

class TestConscience(unittest.TestCase):
    def setUp(self):
        # Store original filters to restore after tests
        self.original_filters = AIConscience.FILTERS

    def tearDown(self):
        # Restore original filters
        AIConscience.FILTERS = self.original_filters

    def test_tonoyan_filter_evaluate(self):
        # Instantiate TonoyanFilter
        filter_id = 1
        name = "Test Filter"
        weight = 2.0
        tf = TonoyanFilter(filter_id, name, weight)

        # Test evaluate method
        context = {"test": "data"}
        passed, reason, confidence = tf.evaluate(context)

        # Assertions
        self.assertTrue(passed)
        self.assertEqual(reason, "OK")
        self.assertEqual(confidence, 0.9)
        self.assertEqual(tf.filter_id, filter_id)
        self.assertEqual(tf.name, name)
        self.assertEqual(tf.weight, weight)

    def test_ai_conscience_judge_approve_default(self):
        conscience = AIConscience('en')
        # By default TonoyanFilter returns confidence 0.9,
        # which should result in APPROVE (>= 0.85)
        decision = conscience.judge("ACTION_001", {})

        self.assertEqual(decision.verdict, ConscienceVerdict.APPROVE)
        self.assertGreaterEqual(decision.confidence, 0.85)
        self.assertEqual(decision.action_id, "ACTION_001")
        self.assertTrue(len(decision.reasoning) > 0)

    def test_ai_conscience_verdicts(self):
        # Test different confidence levels by mocking filters
        conscience = AIConscience('en')

        # Helper to mock filters with a specific confidence
        def mock_filters(confidence_value):
            mocked_filters = []
            for i in range(3):
                f = TonoyanFilter(i, f"Mock_{i}", 1.0)
                f.evaluate = MagicMock(return_value=(True, "Mock OK", confidence_value))
                mocked_filters.append(f)
            return mocked_filters

        # Test APPROVE (>= 0.85)
        AIConscience.FILTERS = mock_filters(0.9)
        decision = conscience.judge("T1", {})
        self.assertEqual(decision.verdict, ConscienceVerdict.APPROVE)

        # Test QUESTION (>= 0.70)
        AIConscience.FILTERS = mock_filters(0.75)
        decision = conscience.judge("T2", {})
        self.assertEqual(decision.verdict, ConscienceVerdict.QUESTION)

        # Test WARN (>= 0.50)
        AIConscience.FILTERS = mock_filters(0.6)
        decision = conscience.judge("T3", {})
        self.assertEqual(decision.verdict, ConscienceVerdict.WARN)

        # Test BLOCK (< 0.50)
        AIConscience.FILTERS = mock_filters(0.4)
        decision = conscience.judge("T4", {})
        self.assertEqual(decision.verdict, ConscienceVerdict.BLOCK)

if __name__ == '__main__':
    unittest.main()

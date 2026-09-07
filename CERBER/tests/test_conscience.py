import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.conscience import AIConscience, ConscienceVerdict, TonoyanFilter

class TestAIConscience(unittest.TestCase):
    def setUp(self):
        self.conscience = AIConscience(lang='pl')
        # Create a controlled set of filters for unit testing
        self.mock_filters = [
            TonoyanFilter(1, "Test Filter 1", 1.0),
            TonoyanFilter(2, "Test Filter 2", 2.0)
        ]

    def test_judge_approve(self):
        """Test case for the APPROVE verdict (confidence >= 0.85)"""
        with patch.object(AIConscience, 'FILTERS', self.mock_filters):
            with patch('core.conscience.TonoyanFilter.evaluate') as mocked_evaluate:
                # Mock evaluate to return 0.9 confidence
                mocked_evaluate.return_value = (True, "OK", 0.9)

                decision = self.conscience.judge("ACTION_001", {"test": True})

                self.assertEqual(decision.verdict, ConscienceVerdict.APPROVE)
                self.assertAlmostEqual(decision.confidence, 0.9)
                self.assertEqual(decision.action_id, "ACTION_001")

    def test_judge_question(self):
        """Test case for the QUESTION verdict (0.70 <= confidence < 0.85)"""
        with patch.object(AIConscience, 'FILTERS', self.mock_filters):
            with patch('core.conscience.TonoyanFilter.evaluate') as mocked_evaluate:
                # Mock evaluate to return 0.75 confidence
                mocked_evaluate.return_value = (True, "MAYBE", 0.75)

                decision = self.conscience.judge("ACTION_002", {"test": True})

                self.assertEqual(decision.verdict, ConscienceVerdict.QUESTION)
                self.assertAlmostEqual(decision.confidence, 0.75)

    def test_judge_warn(self):
        """Test case for the WARN verdict (0.50 <= confidence < 0.70)"""
        with patch.object(AIConscience, 'FILTERS', self.mock_filters):
            with patch('core.conscience.TonoyanFilter.evaluate') as mocked_evaluate:
                # Mock evaluate to return 0.60 confidence
                mocked_evaluate.return_value = (True, "WEAK", 0.60)

                decision = self.conscience.judge("ACTION_003", {"test": True})

                self.assertEqual(decision.verdict, ConscienceVerdict.WARN)
                self.assertAlmostEqual(decision.confidence, 0.60)

    def test_judge_block(self):
        """Test case for the BLOCK verdict (confidence < 0.50)"""
        with patch.object(AIConscience, 'FILTERS', self.mock_filters):
            with patch('core.conscience.TonoyanFilter.evaluate') as mocked_evaluate:
                # Mock evaluate to return 0.40 confidence
                mocked_evaluate.return_value = (False, "BAD", 0.40)

                decision = self.conscience.judge("ACTION_004", {"test": True})

                self.assertEqual(decision.verdict, ConscienceVerdict.BLOCK)
                self.assertAlmostEqual(decision.confidence, 0.40)

    def test_reasoning_populated(self):
        """Verify that the reasoning list is correctly populated with mock filters"""
        with patch.object(AIConscience, 'FILTERS', self.mock_filters):
            decision = self.conscience.judge("ACTION_005", {"test": True})

            self.assertEqual(len(decision.reasoning), 2)
            self.assertIn("#1 Test Filter 1", decision.reasoning[0])
            self.assertIn("#2 Test Filter 2", decision.reasoning[1])

    def test_decisions_history(self):
        """Verify the decisions history is maintained in the AIConscience instance"""
        self.conscience.judge("ACTION_A", {})
        self.conscience.judge("ACTION_B", {})

        self.assertEqual(len(self.conscience.decisions), 2)
        self.assertEqual(self.conscience.decisions[0].action_id, "ACTION_A")
        self.assertEqual(self.conscience.decisions[1].action_id, "ACTION_B")

    def test_confidence_zero_weights(self):
        """Test edge case where total_weight is 0"""
        with patch.object(AIConscience, 'FILTERS', []):
             decision = self.conscience.judge("ACTION_EMPTY", {})
             self.assertEqual(decision.confidence, 0.0)
             self.assertEqual(decision.verdict, ConscienceVerdict.BLOCK)

if __name__ == '__main__':
    unittest.main()

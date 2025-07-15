import unittest
from grading_assistant import GradingAssistant

class TestGradingAssistant(unittest.TestCase):
    def setUp(self):
        self.grader = GradingAssistant()
        
    def test_similarity_calculation(self):
        text1 = "The sky is blue"
        text2 = "The sky is blue"
        similarity = self.grader.calculate_similarity(text1, text2)
        self.assertAlmostEqual(similarity, 1.0, places=1)
        
    def test_grade_response(self):
        reference = "Python is a high-level programming language."
        student = "Python is a programming language that is high-level."
        grade, feedback, scores = self.grader.grade_response(student, reference)
        self.assertIsInstance(grade, int)
        self.assertIsInstance(feedback, str)
        self.assertIsInstance(scores, dict)
        self.assertTrue(0 <= grade <= 5)
        
        # Test that scores dict has expected keys
        expected_keys = ['content_accuracy', 'completeness', 'clarity', 'structure']
        for key in expected_keys:
            self.assertIn(key, scores)
            self.assertTrue(0 <= scores[key] <= 1)
    
    def test_grade_multiple_responses(self):
        reference = "The Earth orbits around the Sun."
        students = [
            "The Earth revolves around the Sun.",
            "Earth goes around the Sun in space.",
            "The Sun orbits the Earth."
        ]
        results = self.grader.grade_multiple_responses(students, reference)
        
        self.assertEqual(len(results), 3)
        for grade, feedback, scores in results:
            self.assertIsInstance(grade, int)
            self.assertIsInstance(feedback, str)
            self.assertIsInstance(scores, dict)
            self.assertTrue(0 <= grade <= 5)
    
    def test_assessment_methods(self):
        student_answer = "This is a well-structured answer with proper punctuation. It covers the topic comprehensively."
        reference_answer = "This covers the topic with proper structure and punctuation."
        
        # Test individual assessment methods
        completeness = self.grader._assess_completeness(student_answer, reference_answer)
        clarity = self.grader._assess_clarity(student_answer)
        structure = self.grader._assess_structure(student_answer)
        
        self.assertTrue(0 <= completeness <= 1)
        self.assertTrue(0 <= clarity <= 1)
        self.assertTrue(0 <= structure <= 1)
    
    def test_assignment_types(self):
        assignment_types = self.grader.get_assignment_types()
        self.assertIsInstance(assignment_types, list)
        self.assertIn("short_answer", assignment_types)
        self.assertIn("essay", assignment_types)
    
    def test_detailed_feedback_generation(self):
        scores = {
            'content_accuracy': 0.9,
            'completeness': 0.8,
            'clarity': 0.7,
            'structure': 0.9
        }
        feedback = self.grader.generate_detailed_feedback(scores)
        self.assertIsInstance(feedback, str)
        self.assertIn("✓", feedback)  # Should contain positive feedback symbols

if __name__ == '__main__':
    unittest.main()
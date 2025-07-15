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
        grade, feedback = self.grader.grade_response(student, reference)
        self.assertIsInstance(grade, int)
        self.assertIsInstance(feedback, str)
        self.assertTrue(0 <= grade <= 5)

if __name__ == '__main__':
    unittest.main()
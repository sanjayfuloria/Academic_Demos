import unittest
import os
from grading_assistant import GradingAssistant

class TestGradingAssistant(unittest.TestCase):
    def setUp(self):
        # Force offline mode for testing to avoid network dependencies
        os.environ["ACADEMIC_DEMOS_OFFLINE_MODE"] = "true"
        os.environ["ACADEMIC_DEMOS_FALLBACK_DUMMY"] = "true"
        os.environ["ACADEMIC_DEMOS_CONSOLE_LOG"] = "false"  # Reduce console output during tests
        
        self.grader = GradingAssistant(username="test_user", offline_mode=True)
        
    def test_initialization(self):
        """Test that grading assistant initializes properly."""
        self.assertIsNotNone(self.grader)
        self.assertIsNotNone(self.grader.model)
        
    def test_model_info(self):
        """Test that model info is available."""
        model_info = self.grader.get_model_info()
        self.assertIsInstance(model_info, dict)
        self.assertIn("model_type", model_info)
        
    def test_similarity_calculation(self):
        """Test similarity calculation between identical texts."""
        text1 = "The sky is blue"
        text2 = "The sky is blue"
        similarity = self.grader.calculate_similarity(text1, text2)
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
        # Identical texts should have high similarity
        self.assertGreater(similarity, 0.8)
        
    def test_similarity_different_texts(self):
        """Test similarity calculation between different texts."""
        text1 = "The sky is blue"
        text2 = "The ocean is deep"
        similarity = self.grader.calculate_similarity(text1, text2)
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
        
    def test_grade_response(self):
        """Test grading of a single response."""
        reference = "Python is a high-level programming language."
        student = "Python is a programming language that is high-level."
        grade, feedback = self.grader.grade_response(student, reference)
        
        self.assertIsInstance(grade, int)
        self.assertIsInstance(feedback, str)
        self.assertTrue(0 <= grade <= 5)
        self.assertGreater(len(feedback), 0)
        
    def test_grade_empty_response(self):
        """Test grading of empty student response."""
        reference = "Python is a high-level programming language."
        student = ""
        grade, feedback = self.grader.grade_response(student, reference)
        
        self.assertEqual(grade, 0)
        self.assertIn("No answer provided", feedback)
        
    def test_grade_empty_reference(self):
        """Test grading with empty reference answer."""
        reference = ""
        student = "Some student answer"
        grade, feedback = self.grader.grade_response(student, reference)
        
        self.assertEqual(grade, 0)
        self.assertIn("Error", feedback)
        
    def test_grade_multiple_responses(self):
        """Test grading multiple responses."""
        reference = "Python is a programming language."
        students = [
            "Python is a programming language.",
            "Python is used for programming.",
            "Java is a programming language."
        ]
        
        results = self.grader.grade_multiple_responses(students, reference)
        
        self.assertEqual(len(results), 3)
        for grade, feedback in results:
            self.assertIsInstance(grade, int)
            self.assertIsInstance(feedback, str)
            self.assertTrue(0 <= grade <= 5)
            
    def test_fallback_similarity(self):
        """Test fallback similarity calculation."""
        text1 = "hello world"
        text2 = "world hello"
        
        # Test the fallback method directly
        similarity = self.grader._fallback_similarity(text1, text2)
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
        
    def test_error_handling(self):
        """Test that the system handles errors gracefully."""
        # This should not raise an exception
        try:
            grade, feedback = self.grader.grade_response("test", "reference")
            self.assertIsInstance(grade, int)
            self.assertIsInstance(feedback, str)
        except Exception as e:
            self.fail(f"grade_response raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
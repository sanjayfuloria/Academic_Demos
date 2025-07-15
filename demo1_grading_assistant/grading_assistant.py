from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple, Dict
import re
from collections import Counter
import math

class GradingAssistant:
    def __init__(self):
        # Try to initialize the BERT model for semantic similarity
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.use_transformer = True
        except Exception as e:
            print(f"Warning: Could not load transformer model ({e}). Using fallback similarity method.")
            self.model = None
            self.use_transformer = False
        
        # Define feedback criteria
        self.feedback_criteria = {
            'content_accuracy': 0.4,
            'completeness': 0.3,
            'clarity': 0.2,
            'structure': 0.1
        }
    
    def _preprocess_text(self, text: str) -> List[str]:
        """Preprocess text for similarity calculation"""
        # Convert to lowercase and remove punctuation
        text = re.sub(r'[^\w\s]', '', text.lower())
        # Split into words
        words = text.split()
        return words
    
    def _cosine_similarity_fallback(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity using word frequency vectors"""
        words1 = self._preprocess_text(text1)
        words2 = self._preprocess_text(text2)
        
        # Create word frequency counters
        counter1 = Counter(words1)
        counter2 = Counter(words2)
        
        # Get all unique words
        all_words = set(counter1.keys()) | set(counter2.keys())
        
        if not all_words:
            return 0.0
        
        # Create frequency vectors
        vec1 = [counter1.get(word, 0) for word in all_words]
        vec2 = [counter2.get(word, 0) for word in all_words]
        
        # Calculate cosine similarity
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
        
    def calculate_similarity(self, text1: str, text2: str) -> float:
        # Calculate semantic similarity between two texts
        if self.use_transformer and self.model:
            try:
                embeddings = self.model.encode([text1, text2])
                similarity = np.dot(embeddings[0], embeddings[1]) / (
                    np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
                )
                return float(similarity)
            except Exception as e:
                print(f"Warning: Transformer model failed ({e}). Falling back to basic similarity.")
                self.use_transformer = False
        
        # Use fallback method
        return self._cosine_similarity_fallback(text1, text2)
    
    def _assess_completeness(self, student_answer: str, reference_answer: str) -> float:
        """Assess how complete the student answer is compared to reference"""
        student_words = set(self._preprocess_text(student_answer))
        reference_words = set(self._preprocess_text(reference_answer))
        
        if not reference_words:
            return 1.0
        
        coverage = len(student_words.intersection(reference_words)) / len(reference_words)
        return min(coverage * 1.5, 1.0)  # Give some bonus for good coverage
    
    def _assess_clarity(self, student_answer: str) -> float:
        """Assess clarity based on sentence structure and length"""
        if not student_answer.strip():
            return 0.0
        
        sentences = re.split(r'[.!?]+', student_answer)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        # Assess based on average sentence length and number of sentences
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Optimal sentence length is around 15-20 words
        if 10 <= avg_length <= 25:
            clarity_score = 1.0
        elif avg_length < 5:
            clarity_score = 0.4  # Too short
        elif avg_length > 40:
            clarity_score = 0.6  # Too long
        else:
            clarity_score = 0.8
        
        return clarity_score
    
    def _assess_structure(self, student_answer: str) -> float:
        """Assess structural quality of the answer"""
        if not student_answer.strip():
            return 0.0
        
        # Check for basic structural elements
        has_punctuation = bool(re.search(r'[.!?]', student_answer))
        has_capitalization = bool(re.search(r'[A-Z]', student_answer))
        word_count = len(student_answer.split())
        
        structure_score = 0.0
        if has_punctuation:
            structure_score += 0.4
        if has_capitalization:
            structure_score += 0.3
        if word_count >= 10:  # Adequate length
            structure_score += 0.3
        
        return structure_score

    def generate_detailed_feedback(self, scores: Dict[str, float]) -> str:
        """Generate detailed feedback based on criteria scores"""
        feedback_parts = []
        
        if scores['content_accuracy'] >= 0.8:
            feedback_parts.append("✓ Excellent content accuracy")
        elif scores['content_accuracy'] >= 0.6:
            feedback_parts.append("• Good content accuracy, but could be more precise")
        else:
            feedback_parts.append("⚠ Content accuracy needs improvement")
        
        if scores['completeness'] >= 0.8:
            feedback_parts.append("✓ Comprehensive answer")
        elif scores['completeness'] >= 0.6:
            feedback_parts.append("• Answer is somewhat complete, consider adding more details")
        else:
            feedback_parts.append("⚠ Answer is incomplete, missing key elements")
        
        if scores['clarity'] >= 0.8:
            feedback_parts.append("✓ Clear and well-expressed")
        elif scores['clarity'] >= 0.6:
            feedback_parts.append("• Generally clear, but could be more concise")
        else:
            feedback_parts.append("⚠ Clarity needs improvement - consider restructuring")
        
        if scores['structure'] >= 0.8:
            feedback_parts.append("✓ Well-structured response")
        elif scores['structure'] >= 0.6:
            feedback_parts.append("• Decent structure, minor improvements needed")
        else:
            feedback_parts.append("⚠ Structure needs work - check grammar and organization")
        
        return "\n".join(feedback_parts)

    def grade_response(self, 
                      student_answer: str, 
                      reference_answer: str,
                      assignment_type: str = "short_answer") -> Tuple[int, str, Dict[str, float]]:
        """Grade a student response with detailed feedback"""
        
        # Calculate individual criteria scores
        content_accuracy = self.calculate_similarity(student_answer, reference_answer)
        completeness = self._assess_completeness(student_answer, reference_answer)
        clarity = self._assess_clarity(student_answer)
        structure = self._assess_structure(student_answer)
        
        scores = {
            'content_accuracy': content_accuracy,
            'completeness': completeness,
            'clarity': clarity,
            'structure': structure
        }
        
        # Calculate weighted overall score
        overall_score = sum(scores[criterion] * weight 
                          for criterion, weight in self.feedback_criteria.items())
        
        # Convert to grade (0-5 scale)
        grade = round(overall_score * 5)
        grade = max(0, min(5, grade))  # Ensure grade is within bounds
        
        # Generate detailed feedback
        detailed_feedback = self.generate_detailed_feedback(scores)
        
        return grade, detailed_feedback, scores
    
    def grade_multiple_responses(self, 
                               student_answers: List[str], 
                               reference_answer: str,
                               assignment_type: str = "short_answer") -> List[Tuple[int, str, Dict[str, float]]]:
        """Grade multiple student responses"""
        return [
            self.grade_response(answer, reference_answer, assignment_type) 
            for answer in student_answers
        ]
    
    def get_assignment_types(self) -> List[str]:
        """Get available assignment types"""
        return ["short_answer", "essay", "explanation", "analysis"]
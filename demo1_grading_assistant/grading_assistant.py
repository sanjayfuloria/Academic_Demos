from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple
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
    
    def grade_response(self, 
                      student_answer: str, 
                      reference_answer: str) -> Tuple[int, str]:
        # Calculate similarity score
        similarity = self.calculate_similarity(student_answer, reference_answer)
        
        # Convert similarity to grade (0-5 scale)
        grade = round(similarity * 5)
        
        # Generate feedback based on grade
        if grade >= 4:
            feedback = "Excellent! Your answer closely matches the expected response."
        elif grade >= 3:
            feedback = "Good answer, but there's room for more detail or precision."
        elif grade >= 2:
            feedback = "Fair attempt, but important elements are missing."
        else:
            feedback = "Please review the topic again. Your answer needs significant improvement."
            
        return grade, feedback
    
    def grade_multiple_responses(self, 
                               student_answers: List[str], 
                               reference_answer: str) -> List[Tuple[int, str]]:
        return [
            self.grade_response(answer, reference_answer) 
            for answer in student_answers
        ]
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple

class GradingAssistant:
    def __init__(self):
        # Initialize the BERT model for semantic similarity
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def calculate_similarity(self, text1: str, text2: str) -> float:
        # Calculate semantic similarity between two texts
        embeddings = self.model.encode([text1, text2])
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        return float(similarity)
    
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
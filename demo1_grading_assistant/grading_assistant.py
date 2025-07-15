import os
import ssl
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple

class GradingAssistant:
    def __init__(self):
        # Try different approaches to handle SSL issues
        try:
            # First attempt: Default configuration
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e1:
            try:
                # Second attempt: Use alternative model
                self.model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
            except Exception as e2:
                try:
                    # Third attempt: Disable SSL verification (not recommended for production)
                    os.environ['CURL_CA_BUNDLE'] = ''
                    ssl._create_default_https_context = ssl._create_unverified_context
                    self.model = SentenceTransformer('all-MiniLM-L6-v2')
                except Exception as e3:
                    try:
                        # Fourth attempt: Try offline mode with smaller model
                        self.model = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=True)
                    except Exception as e4:
                        raise Exception(f"Failed to initialize model. Tried multiple approaches:\n1. {str(e1)}\n2. {str(e2)}\n3. {str(e3)}\n4. {str(e4)}\n\nTip: If you're experiencing network issues, try downloading the model manually or using an offline environment.")
        
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
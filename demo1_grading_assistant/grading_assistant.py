from sentence_transformers import SentenceTransformer
import numpy as np
import os
import ssl
from typing import List, Tuple, Optional
from config import get_config
from dummy_model import create_dummy_model

class GradingAssistant:
    def __init__(self, username: str = "sanjayfuloria", offline_mode: bool = False):
        # Setup configuration and logging
        self.config = get_config(username)
        self.logger = self.config.setup_logging()
        
        # Disable SSL warnings if configured
        self.config.disable_ssl_warnings()
        
        # Log initialization
        self.logger.info("Initializing GradingAssistant")
        env_info = self.config.get_environment_info()
        for key, value in env_info.items():
            self.logger.info(f"{key}: {value}")
        
        # Initialize the model with error handling and offline support
        self.model = self._initialize_model(offline_mode)
        self.is_dummy_model = hasattr(self.model, '_is_dummy')
        
        if self.is_dummy_model:
            self.logger.warning("Using dummy model - functionality will be limited")
        else:
            self.logger.info("Successfully initialized sentence transformer model")
    
    def _initialize_model(self, force_offline: bool = False) -> object:
        """Initialize the sentence transformer model with error handling and offline support."""
        model_name = self.config.model_config["model_name"]
        cache_dir = self.config.model_cache_dir
        
        # Check if we should use offline mode
        offline_mode = force_offline or self.config.model_config["offline_mode"]
        local_files_only = self.config.model_config["local_files_only"]
        
        try:
            # Setup SSL context for HTTPS requests
            ssl_context = self.config.setup_ssl_context()
            
            # Set environment variables for SSL configuration
            if not self.config.ssl_config["verify_ssl"]:
                os.environ["CURL_CA_BUNDLE"] = ""
                os.environ["REQUESTS_CA_BUNDLE"] = ""
                
            self.logger.info(f"Attempting to load model: {model_name}")
            self.logger.info(f"Cache directory: {cache_dir}")
            self.logger.info(f"Offline mode: {offline_mode}")
            self.logger.info(f"Local files only: {local_files_only}")
            
            # Try to load the model
            if offline_mode or local_files_only:
                # Try offline first
                self.logger.info("Attempting to load model in offline mode")
                model = SentenceTransformer(
                    model_name, 
                    cache_folder=cache_dir,
                    local_files_only=True
                )
            else:
                # Try online download
                self.logger.info("Attempting to download model from Hugging Face")
                model = SentenceTransformer(
                    model_name, 
                    cache_folder=cache_dir,
                    local_files_only=False
                )
                
            self.logger.info("Successfully loaded sentence transformer model")
            return model
            
        except Exception as e:
            self.logger.error(f"Failed to load sentence transformer model: {str(e)}")
            self.logger.error(f"Error type: {type(e).__name__}")
            
            # Try fallback strategies
            return self._try_fallback_models(model_name, cache_dir)
    
    def _try_fallback_models(self, model_name: str, cache_dir: str) -> object:
        """Try fallback strategies when the main model fails to load."""
        
        # Strategy 1: Try loading from cache only
        try:
            self.logger.info("Trying to load model from cache only")
            model = SentenceTransformer(model_name, cache_folder=cache_dir, local_files_only=True)
            self.logger.info("Successfully loaded model from cache")
            return model
        except Exception as e:
            self.logger.warning(f"Failed to load from cache: {str(e)}")
        
        # Strategy 2: Try with SSL verification disabled
        if self.config.ssl_config["verify_ssl"]:
            try:
                self.logger.info("Trying to load model with SSL verification disabled")
                # Temporarily disable SSL verification
                original_ssl_context = ssl._create_default_https_context
                ssl._create_default_https_context = ssl._create_unverified_context
                
                model = SentenceTransformer(model_name, cache_folder=cache_dir)
                
                # Restore original SSL context
                ssl._create_default_https_context = original_ssl_context
                
                self.logger.info("Successfully loaded model with SSL verification disabled")
                return model
            except Exception as e:
                # Restore original SSL context
                ssl._create_default_https_context = original_ssl_context
                self.logger.warning(f"Failed to load model with SSL disabled: {str(e)}")
        
        # Strategy 3: Use dummy model if fallback is enabled
        if self.config.model_config["fallback_to_dummy"]:
            self.logger.warning("All model loading strategies failed, using dummy model")
            self.logger.warning("Dummy model provides basic functionality but may have reduced accuracy")
            return create_dummy_model(model_name)
        
        # All strategies failed
        raise RuntimeError(f"Failed to initialize any model for {model_name}. "
                         f"Please check your internet connection, SSL settings, or enable dummy fallback.")
        
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts with error handling."""
        try:
            self.logger.debug(f"Calculating similarity between texts (lengths: {len(text1)}, {len(text2)})")
            
            if self.is_dummy_model:
                # Use dummy model similarity calculation
                embeddings = self.model.encode([text1, text2])
                similarity = self.model.similarity([embeddings[0], embeddings[1]])
            else:
                # Use real sentence transformer
                embeddings = self.model.encode([text1, text2])
                similarity = np.dot(embeddings[0], embeddings[1]) / (
                    np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
                )
            
            # Ensure similarity is in valid range [0, 1]
            similarity = max(0.0, min(1.0, float(similarity)))
            
            self.logger.debug(f"Calculated similarity: {similarity}")
            return similarity
            
        except Exception as e:
            self.logger.error(f"Error calculating similarity: {str(e)}")
            # Return a default similarity based on simple text comparison
            return self._fallback_similarity(text1, text2)
    
    def _fallback_similarity(self, text1: str, text2: str) -> float:
        """Fallback similarity calculation using simple text comparison."""
        try:
            # Simple word overlap similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 and not words2:
                return 1.0
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            similarity = len(intersection) / len(union) if union else 0.0
            self.logger.warning(f"Using fallback similarity calculation: {similarity}")
            return similarity
        except Exception as e:
            self.logger.error(f"Error in fallback similarity: {str(e)}")
            return 0.5  # Default middle value
    
    def grade_response(self, 
                      student_answer: str, 
                      reference_answer: str) -> Tuple[int, str]:
        """Grade a student response with enhanced error handling and logging."""
        try:
            self.logger.info("Grading student response")
            self.logger.debug(f"Reference answer: {reference_answer[:100]}...")
            self.logger.debug(f"Student answer: {student_answer[:100]}...")
            
            # Validate inputs
            if not student_answer.strip():
                self.logger.warning("Empty student answer provided")
                return 0, "No answer provided. Please provide a response."
            
            if not reference_answer.strip():
                self.logger.error("Empty reference answer provided")
                return 0, "Error: No reference answer available."
            
            # Calculate similarity score
            similarity = self.calculate_similarity(student_answer, reference_answer)
            
            # Convert similarity to grade (0-5 scale)
            grade = round(similarity * 5)
            
            self.logger.info(f"Similarity: {similarity:.3f}, Grade: {grade}/5")
            
            # Generate feedback based on grade
            feedback = self._generate_feedback(grade, similarity)
            
            return grade, feedback
            
        except Exception as e:
            self.logger.error(f"Error grading response: {str(e)}")
            return 0, f"Error occurred during grading: {str(e)}"
    
    def _generate_feedback(self, grade: int, similarity: float) -> str:
        """Generate detailed feedback based on grade and similarity score."""
        feedback_base = {
            5: "Excellent! Your answer closely matches the expected response.",
            4: "Very good! Your answer demonstrates strong understanding with minor differences.",
            3: "Good answer, but there's room for more detail or precision.",
            2: "Fair attempt, but important elements are missing or unclear.",
            1: "Limited understanding shown. Please review the topic and try to be more specific.",
            0: "Please review the topic again. Your answer needs significant improvement."
        }
        
        base_feedback = feedback_base.get(grade, "Unable to generate feedback.")
        
        # Add model-specific information
        if self.is_dummy_model:
            model_info = " (Note: Using offline mode with limited analysis capabilities.)"
        else:
            model_info = f" (Similarity score: {similarity:.2f})"
            
        return base_feedback + model_info
    
    def grade_multiple_responses(self, 
                               student_answers: List[str], 
                               reference_answer: str) -> List[Tuple[int, str]]:
        """Grade multiple student responses with progress logging."""
        self.logger.info(f"Grading {len(student_answers)} student responses")
        
        results = []
        for i, answer in enumerate(student_answers, 1):
            self.logger.debug(f"Grading response {i}/{len(student_answers)}")
            result = self.grade_response(answer, reference_answer)
            results.append(result)
        
        self.logger.info("Completed grading all responses")
        return results
    
    def get_model_info(self) -> dict:
        """Get information about the current model."""
        return {
            "model_type": "dummy" if self.is_dummy_model else "sentence_transformer",
            "model_name": getattr(self.model, 'model_name', 'unknown'),
            "cache_dir": self.config.model_cache_dir,
            "offline_mode": self.config.model_config["offline_mode"],
            "ssl_verify": self.config.ssl_config["verify_ssl"],
        }
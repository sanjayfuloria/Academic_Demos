"""
Dummy model implementation for offline fallback when real models are unavailable.
Provides basic text similarity computation using simple algorithms.
"""

import numpy as np
import re
from typing import List
from collections import Counter
import math


class DummySentenceTransformer:
    """
    Dummy implementation of SentenceTransformer for offline mode.
    Uses simple text similarity algorithms when real models are unavailable.
    """
    
    def __init__(self, model_name: str = "dummy-model"):
        self.model_name = model_name
        self._is_dummy = True
    
    def encode(self, sentences: List[str], **kwargs) -> np.ndarray:
        """
        Encode sentences using simple TF-IDF-like vectors.
        This is a basic implementation for offline mode.
        """
        if isinstance(sentences, str):
            sentences = [sentences]
        
        # Preprocess sentences
        processed_sentences = [self._preprocess_text(sentence) for sentence in sentences]
        
        # Create vocabulary from all sentences
        vocabulary = set()
        for sentence in processed_sentences:
            vocabulary.update(sentence.split())
        vocabulary = sorted(list(vocabulary))
        
        # Create TF-IDF-like vectors
        vectors = []
        for sentence in processed_sentences:
            vector = self._create_vector(sentence, vocabulary, processed_sentences)
            vectors.append(vector)
        
        return np.array(vectors)
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text by lowercasing and removing punctuation."""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _create_vector(self, sentence: str, vocabulary: List[str], all_sentences: List[str]) -> np.ndarray:
        """Create a TF-IDF-like vector for a sentence."""
        words = sentence.split()
        word_count = Counter(words)
        
        # Calculate term frequency
        vector = []
        for word in vocabulary:
            tf = word_count.get(word, 0) / len(words) if words else 0
            
            # Calculate inverse document frequency
            doc_count = sum(1 for sent in all_sentences if word in sent.split())
            idf = math.log(len(all_sentences) / (doc_count + 1)) + 1
            
            # TF-IDF score
            tfidf = tf * idf
            vector.append(tfidf)
        
        # Normalize vector
        vector = np.array(vector)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def similarity(self, embeddings: List[np.ndarray]) -> float:
        """Calculate cosine similarity between embeddings."""
        if len(embeddings) != 2:
            raise ValueError("Expected exactly 2 embeddings")
        
        emb1, emb2 = embeddings[0], embeddings[1]
        
        # Calculate cosine similarity
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)


def create_dummy_model(model_name: str = "all-MiniLM-L6-v2") -> DummySentenceTransformer:
    """Create a dummy model instance."""
    return DummySentenceTransformer(model_name)
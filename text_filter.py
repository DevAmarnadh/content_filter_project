from typing import List
import spacy
from transformers import pipeline
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import re

class TextFilter:
    def __init__(self):
        """
        Initialize the text filter with required models and resources.
        """
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Load BERT-based toxicity classifier
        self.toxicity_classifier = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            return_all_scores=True
        )
        
        # Initialize inappropriate words set
        self.inappropriate_words = self._load_inappropriate_words()
        
        # Load NLTK resources
        nltk.download('punkt', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        
        # Compile regex for detecting binary/non-text content
        self.binary_pattern = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\xFF]')
    
    def _load_inappropriate_words(self) -> set:
        """
        Load a predefined set of inappropriate words.
        In a real implementation, this would load from a comprehensive database.
        """
        # This is a minimal example - in production, load from a proper database
        return {
            "inappropriate", "offensive", "explicit",
            # Add more words as needed
        }
    
    def _is_binary_content(self, text: str) -> bool:
        """
        Check if the text contains binary/non-text content.
        """
        # Check for binary characters
        if self.binary_pattern.search(text):
            return True
        
        # Check for long strings of special characters
        special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
        if len(text) > 0 and special_chars / len(text) > 0.5:
            return True
        
        return False
    
    def _is_valid_text(self, text: str) -> bool:
        """
        Check if the text is valid for processing.
        """
        if not text or not text.strip():
            return False
        
        # Skip binary content
        if self._is_binary_content(text):
            return False
        
        # Check if text contains actual words
        words = [w for w in text.split() if any(c.isalpha() for c in w)]
        if not words:
            return False
        
        return True
    
    def _check_toxicity(self, text: str) -> bool:
        """
        Check if text contains toxic content using BERT model.
        """
        if not self._is_valid_text(text):
            return False
            
        results = self.toxicity_classifier(text)[0]
        for result in results:
            if result['label'] == 'toxic' and result['score'] > 0.7:
                return True
        return False
    
    def filter_text(self, text: str) -> str:
        """
        Filter inappropriate content from text by completely removing it.
        Returns empty string for toxic content.
        """
        # Skip invalid or binary content
        if not self._is_valid_text(text):
            return text
            
        # First check if entire text is toxic
        if self._check_toxicity(text):
            return ""  # Remove entire text if toxic
            
        # Tokenize text
        doc = self.nlp(text)
        filtered_words = []
        
        for token in doc:
            word = token.text.lower()
            
            # Skip inappropriate words
            if word in self.inappropriate_words:
                continue
            else:
                filtered_words.append(token.text)
        
        # Join remaining words
        return ' '.join(filtered_words)
    
    def filter_texts(self, texts: List[str]) -> List[str]:
        """
        Filter a list of texts by removing inappropriate content.
        Preserves document structure with empty lines where content was removed.
        """
        filtered_texts = []
        for text in texts:
            # Skip binary content
            if text and self._is_binary_content(text):
                filtered_texts.append('\n')
                continue
                
            # Process valid text
            if text.strip():
                filtered_text = self.filter_text(text.strip())
                if filtered_text:  # Only add non-empty filtered text
                    filtered_texts.append(filtered_text + '\n')
                else:
                    filtered_texts.append('\n')  # Keep line spacing
            else:
                filtered_texts.append('\n')
        return filtered_texts
    
    def get_content_stats(self, texts: List[str]) -> dict:
        """
        Get statistics about filtered content.
        """
        total_words = 0
        filtered_words = 0
        toxic_contexts = 0
        
        for text in texts:
            # Skip binary content
            if not self._is_valid_text(text):
                continue
                
            words = word_tokenize(text)
            total_words += len(words)
            
            # Count filtered words
            filtered_words += sum(1 for word in words if word.lower() in self.inappropriate_words)
            
            # Count toxic contexts and their words
            if self._check_toxicity(text):
                toxic_contexts += 1
                # Add all words from toxic contexts to filtered count
                filtered_words += len([w for w in words if w.lower() not in self.inappropriate_words])
        
        return {
            "total_words": total_words,
            "filtered_words": filtered_words,
            "toxic_contexts": toxic_contexts,
            "clean_ratio": (total_words - filtered_words) / total_words if total_words > 0 else 1.0
        } 
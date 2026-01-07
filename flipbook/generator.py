"""Sentence generator for flip books."""

from typing import List, Tuple
import random
from .word_lists import NOUNS, VERBS, OBJECTS


class FlipBookGenerator:
    """Generates sentences for flip books in 'noun verb noun' format."""
    
    def __init__(self, nouns: List[str] = None, verbs: List[str] = None, 
                 objects: List[str] = None):
        """
        Initialize the generator with word lists.
        
        Args:
            nouns: List of subject nouns (default: uses built-in list)
            verbs: List of action verbs (default: uses built-in list)
            objects: List of object nouns (default: uses built-in list)
        """
        self.nouns = nouns or NOUNS
        self.verbs = verbs or VERBS
        self.objects = objects or OBJECTS
        
    def generate_sentence(self, noun: str = None, verb: str = None, 
                         obj: str = None) -> Tuple[str, str, str]:
        """
        Generate a single sentence as a tuple of three parts.
        
        Args:
            noun: Specific noun to use (optional, random if not provided)
            verb: Specific verb to use (optional, random if not provided)
            obj: Specific object to use (optional, random if not provided)
            
        Returns:
            Tuple of (noun, verb, object) forming a complete sentence
        """
        noun = noun or random.choice(self.nouns)
        verb = verb or random.choice(self.verbs)
        obj = obj or random.choice(self.objects)
        
        return (noun, verb, obj)
    
    def generate_book(self, num_pages: int = 10) -> List[Tuple[str, str, str]]:
        """
        Generate multiple sentences for a flip book.
        
        Args:
            num_pages: Number of pages (sentences) to generate
            
        Returns:
            List of tuples, each containing (noun, verb, object)
        """
        return [self.generate_sentence() for _ in range(num_pages)]
    
    def format_sentence(self, sentence: Tuple[str, str, str]) -> str:
        """
        Format a sentence tuple as a readable string.
        
        Args:
            sentence: Tuple of (noun, verb, object)
            
        Returns:
            Formatted sentence string
        """
        noun, verb, obj = sentence
        return f"{noun} {verb} {obj}."
    
    def get_total_combinations(self) -> int:
        """
        Calculate the total number of possible sentence combinations.
        
        Returns:
            Total number of unique sentences possible
        """
        return len(self.nouns) * len(self.verbs) * len(self.objects)

"""Output formatters for flip book pages."""

from typing import List, Tuple
from .generator import FlipBookGenerator


class FlipBookFormatter:
    """Formats flip book sentences for printing."""
    
    def __init__(self, generator: FlipBookGenerator):
        """
        Initialize the formatter with a generator.
        
        Args:
            generator: FlipBookGenerator instance
        """
        self.generator = generator
    
    def format_for_print(self, sentences: List[Tuple[str, str, str]], 
                        page_width: int = 60) -> str:
        """
        Format sentences for printing with visual separators.
        
        Args:
            sentences: List of (noun, verb, object) tuples
            page_width: Character width for each page
            
        Returns:
            Formatted string ready for printing
        """
        output = []
        separator = "=" * page_width
        cut_line = "-" * page_width
        
        output.append("\n" + separator)
        output.append("FLIP-N-GIGGLE BOOK".center(page_width))
        output.append(separator + "\n")
        
        for i, sentence in enumerate(sentences, 1):
            noun, verb, obj = sentence
            
            output.append(f"\nPage {i}".center(page_width))
            output.append(cut_line)
            output.append(f"| {noun:^{page_width-4}} |  <- Cut here")
            output.append(cut_line)
            output.append(f"| {verb:^{page_width-4}} |  <- Cut here")
            output.append(cut_line)
            output.append(f"| {obj:^{page_width-4}} |")
            output.append(cut_line)
            output.append("")
        
        return "\n".join(output)
    
    def format_as_list(self, sentences: List[Tuple[str, str, str]]) -> str:
        """
        Format sentences as a simple numbered list.
        
        Args:
            sentences: List of (noun, verb, object) tuples
            
        Returns:
            Formatted list of sentences
        """
        output = ["Generated Sentences:", ""]
        for i, sentence in enumerate(sentences, 1):
            formatted = self.generator.format_sentence(sentence)
            output.append(f"{i}. {formatted}")
        return "\n".join(output)
    
    def save_to_file(self, sentences: List[Tuple[str, str, str]], 
                     filename: str, format_type: str = "print") -> None:
        """
        Save formatted sentences to a file.
        
        Args:
            sentences: List of (noun, verb, object) tuples
            filename: Output file name
            format_type: Either "print" or "list"
        """
        if format_type == "print":
            content = self.format_for_print(sentences)
        else:
            content = self.format_as_list(sentences)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

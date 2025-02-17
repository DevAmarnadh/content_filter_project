from typing import Dict, Tuple, List
from PIL import Image
import os

from text_filter import TextFilter
from image_filter import ImageFilter
from utils import (
    get_document_type,
    extract_docx_content,
    extract_pdf_content,
    extract_txt_content,
    save_docx,
    save_pdf,
    save_txt
)

class DocumentProcessor:
    def __init__(self):
        """
        Initialize the document processor with text and image filters.
        """
        print("Initializing filters...")
        self.text_filter = TextFilter()
        self.image_filter = ImageFilter()
        print("Filters initialized successfully")
    
    def process_document(self, input_path: str, output_path: str) -> Dict:
        """
        Process a document and filter inappropriate content.
        
        Args:
            input_path: Path to the input document
            output_path: Path where the filtered document should be saved
            
        Returns:
            Dictionary containing statistics about the filtering process
        """
        # Validate input file
        print(f"Validating input file: {input_path}")
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Get document type
        print("Determining document type...")
        doc_type = get_document_type(input_path)
        print(f"Document type: {doc_type}")
        
        # Extract content based on document type
        print("Extracting document content...")
        texts, images = self._extract_content(input_path, doc_type)
        print(f"Extracted {len(texts)} text segments and {len(images)} images")
        
        # Filter text content
        print("Filtering text content...")
        filtered_texts = self.text_filter.filter_texts(texts)
        text_stats = self.text_filter.get_content_stats(texts)
        print(f"Text filtering complete. Stats: {text_stats}")
        
        # Filter images
        print("Filtering images...")
        filtered_images, image_flags, image_categories = self.image_filter.filter_images(images)
        image_stats = self.image_filter.get_image_stats(image_flags, image_categories)
        print("Image filtering complete.")
        print(f"Total images: {image_stats['total_images']}")
        print(f"Flagged images: {image_stats['flagged_images']}")
        if image_stats['categories']:
            print("Removed by category:")
            for category, count in image_stats['categories'].items():
                print(f"- {category}: {count}")
        
        # Save filtered content
        print(f"Saving filtered content to: {output_path}")
        self._save_filtered_content(
            output_path,
            doc_type,
            filtered_texts,
            filtered_images
        )
        print("Content saved successfully")
        
        # Combine and return statistics
        return {
            "text_stats": text_stats,
            "image_stats": image_stats,
            "input_file": input_path,
            "output_file": output_path,
            "document_type": doc_type
        }
    
    def _extract_content(
        self,
        file_path: str,
        doc_type: str
    ) -> Tuple[List[str], List[Image.Image]]:
        """
        Extract text and images from the document based on its type.
        """
        if doc_type == 'docx':
            return extract_docx_content(file_path)
        elif doc_type == 'pdf':
            return extract_pdf_content(file_path)
        elif doc_type == 'txt':
            return extract_txt_content(file_path)
        else:
            raise ValueError(f"Unsupported document type: {doc_type}")
    
    def _save_filtered_content(
        self,
        output_path: str,
        doc_type: str,
        texts: List[str],
        images: List[Image.Image]
    ):
        """
        Save the filtered content to a new document.
        """
        try:
            if doc_type == 'docx':
                save_docx(texts, images, output_path)
            elif doc_type == 'pdf':
                save_pdf(texts, images, output_path)
            elif doc_type == 'txt':
                save_txt(texts, output_path)
            else:
                raise ValueError(f"Unsupported document type for saving: {doc_type}")
        except Exception as e:
            print(f"Error saving filtered content: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    processor = DocumentProcessor()
    
    # Process a document
    stats = processor.process_document(
        "input_document.docx",
        "filtered_document.docx"
    )
    
    # Print statistics
    print("Processing complete!")
    print(f"Text stats: {stats['text_stats']}")
    print(f"Image stats: {stats['image_stats']}")
    print(f"Filtered document saved to: {stats['output_file']}") 
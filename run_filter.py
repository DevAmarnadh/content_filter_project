from document_processor import DocumentProcessor
import traceback

def main():
    # Initialize the processor
    print("Initializing document processor...")
    processor = DocumentProcessor()
    
    # Process the test document
    try:
        print("\nStarting document processing...")
        print(f"Input file: test_input.txt")
        print(f"Output file: filtered_output.txt")
        
        stats = processor.process_document(
            "test_input.txt",
            "filtered_output.txt"
        )
        
        # Print statistics
        print("\nProcessing complete!")
        print("\nText Statistics:")
        print(f"Total words: {stats['text_stats']['total_words']}")
        print(f"Filtered words: {stats['text_stats']['filtered_words']}")
        print(f"Toxic contexts: {stats['text_stats']['toxic_contexts']}")
        print(f"Clean ratio: {stats['text_stats']['clean_ratio']:.2%}")
        
        print("\nDocument Information:")
        print(f"Input file: {stats['input_file']}")
        print(f"Output file: {stats['output_file']}")
        print(f"Document type: {stats['document_type']}")
        
    except Exception as e:
        print(f"\nError processing document:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main() 
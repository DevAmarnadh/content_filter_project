import streamlit as st
import os
from document_processor import DocumentProcessor
import tempfile
import chardet

st.set_page_config(
    page_title="Content Filter AI",
    page_icon="🔍",
    layout="wide"
)

def detect_encoding(file_path):
    """Detect the encoding of a file"""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def read_file_content(file_path, file_type):
    """Read file content with proper encoding detection"""
    if file_type == 'pdf':
        # For PDFs, we don't need to read the content directly
        return None
    
    try:
        # Detect encoding
        encoding = detect_encoding(file_path)
        if not encoding:
            encoding = 'utf-8'
        
        # Read file with detected encoding
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            return f.read()
    except Exception as e:
        st.warning(f"Note: Could not read original file content for preview: {str(e)}")
        return None

def main():
    st.title("Content Filter AI 🔍")
    st.subheader("Filter inappropriate content from your documents")
    
    # Initialize document processor
    @st.cache_resource
    def get_processor():
        return DocumentProcessor()
    
    processor = get_processor()
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload a document (.txt, .docx, .pdf)", 
        type=['txt', 'docx', 'pdf']
    )
    
    if uploaded_file is not None:
        # Create a temporary directory to store the files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            input_path = os.path.join(temp_dir, uploaded_file.name)
            with open(input_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            # Create output path
            file_name, file_ext = os.path.splitext(uploaded_file.name)
            output_path = os.path.join(temp_dir, f"{file_name}_filtered{file_ext}")
            
            # Process button
            if st.button("Process Document", type="primary"):
                with st.spinner("Processing document..."):
                    try:
                        # Process the document
                        stats = processor.process_document(input_path, output_path)
                        
                        # Display statistics in columns
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Text Statistics")
                            st.metric("Total Words", stats['text_stats']['total_words'])
                            st.metric("Filtered Words", stats['text_stats']['filtered_words'])
                            st.metric("Toxic Contexts", stats['text_stats']['toxic_contexts'])
                            st.metric("Clean Ratio", f"{stats['text_stats']['clean_ratio']:.1%}")
                        
                        with col2:
                            st.subheader("Image Statistics")
                            st.metric("Total Images", stats['image_stats']['total_images'])
                            st.metric("Flagged Images", stats['image_stats']['flagged_images'])
                            st.metric("Clean Ratio", f"{stats['image_stats']['clean_ratio']:.1%}")
                        
                        # Provide download link for filtered document
                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="Download Filtered Document",
                                data=f.read(),
                                file_name=f"{file_name}_filtered{file_ext}",
                                mime=uploaded_file.type
                            )
                            
                    except Exception as e:
                        st.error(f"Error processing document: {str(e)}")
                        import traceback
                        st.error(f"Detailed error: {traceback.format_exc()}")
    
    # Add information about the tool
    with st.expander("About Content Filter AI"):
        st.markdown("""
        This tool helps you filter inappropriate content from your documents:
        
        - Supports .txt, .docx, and .pdf files
        - Filters inappropriate text using AI
        - Detects and removes inappropriate images
        - Provides detailed statistics
        - Maintains document formatting
        
        Upload a document and click 'Process Document' to get started!
        """)

if __name__ == "__main__":
    main() 
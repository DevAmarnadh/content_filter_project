# Content Filter AI

An intelligent content filtering system that removes inappropriate content from documents while maintaining their structure.

## System Requirements

- Python 3.8 or higher
- Windows 10/11, macOS, or Linux
- At least 4GB RAM
- 2GB free disk space

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/content_filter_project.git
cd content_filter_project
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

## Running the Application

There are two ways to run the content filter:

### 1. Web Interface (Recommended)

Start the Streamlit web interface:
```bash
streamlit run app.py
```
This will:
- Open your default browser
- Load the web interface at http://localhost:8501
- Allow you to upload and process documents through the UI

### 2. Command Line Interface

Process documents directly from the command line:
```bash
python run_filter.py
```
This will:
- Process the test document (test_input.txt)
- Generate filtered output (filtered_output.txt)
- Show processing statistics

## Supported File Formats

- PDF (.pdf)
- Microsoft Word (.docx)
- Text files (.txt)

## Features

- Text Content Filtering:
  - Removes inappropriate words and phrases
  - Detects and removes toxic content
  - Maintains document structure
  - Handles multiple languages

- Image Content Filtering:
  - Detects inappropriate images
  - Removes flagged content
  - Supports common image formats

- Processing Statistics:
  - Word count metrics
  - Filtered content statistics
  - Processing success rate

## Configuration

The system uses default configuration values suitable for most use cases. To modify:

1. Text filtering thresholds:
   - Edit `text_filter.py`
   - Adjust `self.toxicity_classifier` parameters

2. Image filtering settings:
   - Edit `image_filter.py`
   - Modify detection thresholds in `_is_inappropriate()`

## Troubleshooting

1. If you get encoding errors:
   ```
   Solution: Ensure your Python environment uses UTF-8:
   set PYTHONIOENCODING=utf8 (Windows)
   export PYTHONIOENCODING=utf8 (Linux/Mac)
   ```

2. If you get memory errors:
   ```
   Solution: Reduce batch size in document_processor.py
   or process smaller documents
   ```

3. If models fail to load:
   ```
   Solution: Check internet connection and retry
   pip install --upgrade transformers torch
   ```

## Security Notes

- Do not expose the service directly to the internet
- Keep model files and dependencies updated
- Review filtered content before distribution
- Handle sensitive documents according to your security policy

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests:
1. Check the issues tab on GitHub
2. Create a new issue with:
   - System details
   - Error messages
   - Steps to reproduce 
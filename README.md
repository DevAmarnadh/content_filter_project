# Content Filter AI

An intelligent content filtering system that removes inappropriate content from documents while maintaining their structure.

## System Requirements

- Python 3.8 to 3.11 (3.12 not fully supported yet)
- Windows 10/11, macOS, or Linux
- At least 4GB RAM
- 2GB free disk space

## Installation

1. Ensure correct Python version is installed:
```bash
# Check Python version
python --version  # or python3 --version
# Should show Python 3.8, 3.9, 3.10, or 3.11 (NOT 3.12)
```

2. If needed, install Python 3.11:
```bash
# Windows: Download from https://www.python.org/downloads/release/python-3115/

# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv

# macOS
brew install python@3.11
```

3. Update pip to the latest version:
```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

4. Install build tools:
```bash
# Windows
python -m pip install --upgrade setuptools wheel

# macOS/Linux
python3 -m pip install --upgrade setuptools wheel
```

5. Clone the repository:
```bash
git clone https://github.com/yourusername/content_filter_project.git
cd content_filter_project
```

6. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

7. Install dependencies in correct order:
```bash
# First install core packages
pip install --upgrade pip setuptools wheel
pip install numpy==1.24.3
pip install torch==2.2.0

# Then install remaining requirements
pip install -r requirements.txt
```

8. Install spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

## Common Installation Issues

1. If you get numpy build error:
   ```
   Solution: Make sure you're using Python 3.8-3.11 (NOT 3.12)
   If using 3.12, downgrade to 3.11:
   1. Uninstall Python 3.12
   2. Install Python 3.11
   3. Create new virtual environment
   4. Follow installation steps again
   ```

2. If you get distutils error:
   ```
   This is a built-in package. No need to install it separately.
   Make sure you've installed setuptools and wheel as shown in step 4.
   ```

3. If you get build errors:
   ```
   # Windows
   pip install --upgrade Microsoft.C++-Redistributable
   
   # Linux
   sudo apt-get install python3-dev build-essential
   
   # macOS
   xcode-select --install
   ```

4. If you get SSL errors:
   ```
   # Update certificates
   pip install --upgrade certifi
   ```

5. If pip install fails:
   ```
   # Try installing with these flags
   pip install --no-cache-dir --force-reinstall numpy==1.24.3
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
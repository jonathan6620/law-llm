import os
import pdfplumber
from typing import List, Union

# Specify the directory path
def get_files_in_path(dir_path: str, suffix: Union[str, None] = None) -> List[str]:
    """ Read all files in a directory """
    files = os.listdir(dir_path)
    valid_files = list()

    # Read each file and store the content in a dictionary
    for file in files:
        file_path = os.path.join(dir_path, file)
        
        # Check if the path is a file, not a directory
        if os.path.isfile(file_path):
            if not suffix or file.endswith(suffix):
                valid_files.append(file_path)

    return valid_files


input_path = 'pdfs'
output_path = 'texts'

pdf_files = get_files_in_path("pdfs", suffix='.pdf')
os.makedirs(output_path, exist_ok=True)

for pdf_file in pdf_files:
    print(f'Converting: {pdf_file}...')
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text_pages = [page.extract_text() for page in pdf.pages] 
            text_file = os.path.join(output_path, os.path.basename(pdf_file).replace(".pdf", ".txt"))
            with open(text_file, "w") as f:
                f.write('\n'.join(text_pages))
    except Exception as e:
        print(f'Error: {e}')
        continue
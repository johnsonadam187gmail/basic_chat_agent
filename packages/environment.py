from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os

__all__ = ['load_keys', 'pdf_reader', 'read_text_file_to_string']

def load_keys():
    load_dotenv(override=True)
    openrouter_key = os.getenv('OPENROUTER_API_KEY')

    if openrouter_key:
        return True, openrouter_key
    else:
        return False
    
def pdf_reader(file_url:str) -> str:
    text_out = ""
    for page in PdfReader(file_url).pages:
        text = page.extract_text()
        if text:
            text_out += text + "\n"
    return text_out 

def read_text_file_to_string(filepath: str) -> str:
    try:
        # 'r' is for read mode, 'utf-8' is a robust encoding standard
        with open(filepath, 'r', encoding='utf-8') as f:
            # .read() reads the entire file content as one string
            file_content = f.read()
            return file_content
    except FileNotFoundError:
        # We print the error but return an empty string to keep the function safe
        print(f"Error: The file was not found at path: {filepath}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return ""
    

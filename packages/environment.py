from dotenv import load_dotenv
import os

__all__ = ['load_keys']

def load_keys():
    load_dotenv(override=True)
    openrouter_key = os.getenv('OPENROUTER_API_KEY')

    if openrouter_key:
        return True, openrouter_key
    else:
        return False
    

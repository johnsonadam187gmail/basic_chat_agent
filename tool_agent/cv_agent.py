from openai import OpenAI
from anthropic import Anthropic
from packages.environment import load_keys
from packages.cv_agent_prompts import agent_prompts
from PyPDF2 import PdfReader
import gradio as gr
import time


def reader(file_url):
    text_out = ""
    for page in PdfReader(file_url).pages:
        text = page.extract_text()
        if text:
            text_out += text + "\n"
    return text_out 





def main():
    # key_test, api_key = load_keys()
    # if key_test:
    #     client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)   
    # start_time = time.perf_counter()
    print(agent_prompts[0])
    





if __name__ == "__main__":
    pdf_file = "Profile.pdf"
    main()

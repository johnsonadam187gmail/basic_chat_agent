from openai import OpenAI
from anthropic import Anthropic
from packages.environment import load_keys
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

def main(name= "Adam Johnson", summary_file = "alj.txt", linkedin_file = "Profile.pdf"):
    key_test, api_key = load_keys()
    if key_test:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)   
    start_time = time.perf_counter()
    linkedin = reader(linkedin_file)
    summary = read_text_file_to_string(summary_file)

    system_prompt = f"""You are acting as {name}. You are answering questions on {name}'s website, \
    particularly questions related to {name}'s career, background, skills and experience. \
    Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
    You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
    Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
    If you don't know the answer, say so.\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n \
    With this context, please chat with the user, always staying in character as {name}."""

    def chat(message, history):
        messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
        response = client.chat.completions.create(
            model="openai/gpt-5", messages=messages)
        return response.choices[0].message.content
    
    gr.ChatInterface(chat, type="messages").launch()
        

if __name__ == "__main__":
    pdf_file = "tool_agent/Profile.pdf"
    txt_file = "tool_agent/alj.txt"
    main(name="Adam Johnson", summary_file=txt_file, linkedin_file=pdf_file)

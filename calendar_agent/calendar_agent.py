from pydantic import BaseModel
from openai import OpenAI
import time
from packages.environment import load_keys, pdf_reader, read_text_file_to_string


key_test, api_key = load_keys()
if key_test:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)


class CalendarEvent(BaseModel):
    title: str
    date: str
    time: str
    duration: str
    description: str
    participants: list[str]

system_prompt = """You are a helpful assistant. Your task is to extract calendar event information from user input and provide it in a structured format. """
user_prompt = """John and Steve are meeting on 25th December 2023 at 3pm for 2 hours to discuss the new project. Please add this to my calendar."""

messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
completion = client.beta.chat.completions.parse(model = "openai/gpt-5", messages = messages, response_format=CalendarEvent)
response = completion.choices[0].message.parsed
print(f"Title: {response.title}")


from dotenv import load_dotenv
import os
from openai import OpenAI
from packages.environment import load_keys


def main(question = "Why is the sky blue?", model='openai/gpt-5'):
    key_test, api_key = load_keys()
    if key_test:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

        response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
    ],
    stream=False
)
        return response.choices[0].message.content


if __name__ == "__main__":
    model_response  = main("Explain quantum physics, and the history of the discoveries that influenced the standard model, in simple terms")
    print(model_response)


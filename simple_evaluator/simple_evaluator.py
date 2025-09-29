from openai import OpenAI
from anthropic import Anthropic
from packages.environment import load_keys
import time


content = ["Your task is to formulate a question to test someone's general IQ. "
"The question should be challenging and thought-provoking, requiring deep thinking and reasoning. Avoid simple factual questions or those that can be answered with common knowledge. Instead, focus on questions that assess problem-solving skills, logical reasoning, and creativity. "
"The question should be open-ended, allowing for multiple interpretations and answers. "
"Ensure that the question is clear and concise, avoiding any ambiguity or confusion.", "Your task is to answer the question posed to you in a clear and concise manner. "
"The answer should be well-reasoned and supported by evidence or examples where appropriate. ", "Your task is to evaluate the answers provided to the question and choose the most appropriate. You will be given a dictionary of structure Model: Answer. Return the Answer and the model name, with no other commentary or formatting"]

def question_agent(question = content[0], model='openai/gpt-5'):
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
    
def answer_agent1(question, model='google/gemini-2.5-flash'):
    key_test, api_key = load_keys()
    if key_test:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

        response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": f"You are a helpful assistant. {content[1]}"},
        {"role": "user", "content": question}
    ],
    stream=False
)
        return response.choices[0].message.content, model
    

def answer_agent2(question, model='x-ai/grok-4-fast:free'):
    key_test, api_key = load_keys()
    if key_test:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

        response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": f"You are a helpful assistant. {content[1]}"},
        {"role": "user", "content": question}
    ],
    stream=False
)
        return response.choices[0].message.content, model
    
def answer_agent3(question, model='anthropic/claude-3-5-sonnet'):
    key_test, api_key = load_keys()
    if key_test:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

        response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": f"You are a helpful assistant. {content[1]}"},
        {"role": "user", "content": question}
    ],
    stream=False
)
        return response.choices[0].message.content, model
    
def evaluation_agent(question1='why is the sky blue?', model='openai/gpt-5'):
    key_test, api_key = load_keys()
    if key_test:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

        response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": f"You are a helpful assistant"},
        {"role": "user", "content": f"{content[2]}: {question1}"}
    ],
    stream=False
)
        return response.choices[0].message.content

def main():
    start_time = time.perf_counter()
    question = question_agent()
    answer1, model1 = answer_agent1(question)
    # answer2, model2 = answer_agent2(question)
    answer3, model3 = answer_agent3(question)
    answers = {model1: answer1, model3: answer3}
    final_answer = evaluation_agent(question1=answers)
    stop_time = time.perf_counter()
    timer = stop_time - start_time
    return question, final_answer, timer


if __name__ == "__main__":
    question, answer, timer  = main()
    print("----QUESTION----\n")
    print(question)
    print("----ANSWER----\n")
    print(answer)
    print("----TIME ELAPSED----\n")
    print(f"Time elapsed: {round(timer, 2)} seconds") 


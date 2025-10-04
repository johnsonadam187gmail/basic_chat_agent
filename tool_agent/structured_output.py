from pydantic import BaseModel
from openai import OpenAI
import time
from packages.environment import load_keys, pdf_reader, read_text_file_to_string


def cv_agent(summary_file, linkedin_file, job_description, feedback, previous = '', name= "Adam Johnson"):
    key_test, api_key = load_keys()
    if key_test:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)   
    

    cv_agent_system_prompt = f"""You are a CV producing expert. Your task is to take information about the individual, and a job description and produce a suitable cv for the job application.
    You will be provided with a summary of the individuals LinkedIn profile, a personal summary page, and the job description. 
    You will also take any feedback comments and , and previous outputs of cvs and factor them into the cv generation.
    You will use this information to produce a cv that is tailored to the job description.
    Be professional and engaging, a produce content that is suitable and relevant to the job description. 
    Focus your content creation around keywords and phrases in the job application. Do not produce false content, but be creative in how you present the information you have.
    Provide the finished content in markdown.
    Do not add any extra commentary or formatting (other than the markdown for the cv)."""

    cv_agent_user_prompt = f"""The candidates name is {name}. \n
    The candidates summary is: {summary_file}\n\n
    The candidates LinkedIn profile is: {linkedin_file}\n\n
    The job description is: {job_description}\n
    The feedback on the previous cv is: {feedback}\n\n
    The previous cv output is: {previous}\n\n"""


    messages = [{"role": "system", "content": cv_agent_system_prompt},{"role": "user", "content": cv_agent_user_prompt}]
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini", messages=messages)
    return response.choices[0].message.content


# structured outputs are the way we ensure specific outputs from the llm. For this wew need to use pydantic models and create a class
# from the BaseModel class. Each field in the class represents a specific piece of information we want from the llm. 
# We will tell the llm in the system prompt how to produce the output in the correct format. 
# The llm will then generate a response that can be parsed into an instance of the class.


class StructuredOutput(BaseModel):
    is_acceptable: bool
    feedback: str


def evaluataion_agent(response, job_description):

    evaluation_system_prompt = f"""You are an HR manaager. Your task is to evaulate the incoming cv. \
    You are provided with a Job application. You will also be provided a cv.
    You will evaulate the cv against the job application. Your scoring criteria is to assess how the cv uses the keywords in the job description. 
    The cv must be within what you would expect from a top 25% candidate.
    You will provide feedback on the cv, and indicate if it is acceptable for submission.
    You can NOT make up any content, you can only use the content provided in the cv and job description.
    You also can not provide feedback to make up content or lie about the candidate.
    Your feedback will be used to regenerate the cv if it is not acceptable.
    You will provide the feedback in a structured format. The format is as follows:
    is_acceptable: a boolean indicating if the cv is acceptable for submission.
    feedback: a string providing feedback on the cv. The feedback should be specific and actionable. 
    \n\n
    The job description is: {job_description}\n\n
    """

    eval_prompt = f"""Analyse the following for suitability compared to the job description:\n
    {response}"""

    key_test, api_key = load_keys()
    if key_test:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)   
    
    messages = [{"role": "system", "content": evaluation_system_prompt}, {"role": "user", "content": eval_prompt}]
    response = client.beta.chat.completions.parse(
    model="openai/gpt-5",
    messages=messages, response_format=StructuredOutput)
    return response.choices[0].message.parsed


def main(summary, linkedin, job_description, feedback, name="Adam Johnson"):
    start_time = time.perf_counter()
    #loop for cv generation and feedback
    counter = 1
    is_accepted = False
    while not is_accepted:
        cv = cv_agent(summary, linkedin, job_description, feedback, name=name)
        eval = evaluataion_agent(cv, job_description)
        is_accepted = eval.is_acceptable
        feedback = eval.feedback
        counter += 1
        check_timer = time.perf_counter()
        if check_timer - start_time > 900:
            print("Max time reached, exiting loop")
            break
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return cv, eval, run_time, counter
    

if __name__ == "__main__":
    pdf_file = "tool_agent/Profile.pdf"
    txt_file = "tool_agent/alj.txt"
    job_file = "tool_agent/job.txt"
    job_description = read_text_file_to_string(job_file)
    summary = read_text_file_to_string(txt_file)
    linkedin = pdf_reader(pdf_file)
    cv, eval, run_time, counter = main(summary, linkedin, job_description, feedback = "N/A")
    print(f"Time taken: {run_time} seconds")
    print(eval)
    print(cv)
    print(f"Number of iterations: {counter}")

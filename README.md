🤖 Agentic Patterns Showcase
A Python project demonstrating foundational agentic patterns using the OpenAI SDK and models accessed via the OpenRouter service. This repository is structured for exploring and developing different model-based architectures, starting with a simple chat agent.

Table of Contents
Project Overview

Project Structure

Features

Installation and Setup

Usage

Technologies Used

License

Contact

Project Overview
This project serves as a clear, practical example of implementing various agentic patterns in Python, primarily focusing on using the OpenAI SDK to interact with language models. All model calls are routed through OpenRouter, demonstrating flexibility in API access and model selection.

The current implementation includes:

basic_chat_agent: A simple, foundational instance of a chat completion agent.

simple_evaluator: An initial implementation of an evaluator architecture, where a larger model is used to assess, score, and select the most suitable output from other models or agents.

Project Structure
The modular design allows for easy expansion and testing of new agents or tools.

my-awesome-project/
├── basic_chat_agent/        # Core chat completion implementation
│   ├── __init__.py
│   └── simple_chat.py
├── packages/                # Shared utilities and environment setup
│   ├── __init__.py
│   └── environment.py       # Manages API keys and configuration
├── simple_evaluator/        # Evaluator agent logic
│   ├── __init__.py
│   └── simple_evaluator.py
├── README.md

Features
Simple Chat Agent: A straightforward example of one-shot chat completion using the OpenAI SDK.

Evaluator Architecture: Demonstrates how to use a superior "evaluator" model to choose the best response from candidate outputs.

OpenRouter Integration: Configured to use OpenRouter API endpoints for broader model access and cost management.

Modular Design: Separates core agent logic, evaluation logic, and shared configurations for easier development of new patterns.

Installation and Setup
This project requires Python and access to language models via the OpenRouter API.

Prerequisites
Python 3.9+

An OpenRouter API Key.

Setup Steps
Clone the repository:

git clone https://github.com/johnsonadam187gmail/basic_chat_agent.git

Install dependencies:
The project relies on the openai package and likely python-dotenv for environment management.


# Install the necessary packages
uv sync

Configure Environment Variables:
Create a file named .env in the root directory (my-awesome-project/) and add your API key:

# .env file content
OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY_HERE"

Note: The packages/environment.py file should handle loading this key and setting the appropriate base URL for the OpenAI client.

Usage
You can run the individual agent files from the project root after completing the setup.

1. Running the Simple Chat Agent
Execute the file to get a simple chat completion response:

python basic_chat_agent/simple_chat.py

2. Running the Simple Evaluator
Execute the evaluator to see how it assesses and selects the best output from a pool of responses (or a simulated set):

python simple_evaluator/simple_evaluator.py

Technologies Used
Primary Language: Python

SDK: OpenAI SDK (used for making model calls)

API Service: OpenRouter (for flexible model access)

Dependency Management: pip

License
This project is licensed under the MIT License. See the repository for the full LICENSE file.

Contact
Adam Johnson - johnsonadam187@gmail.com

Project Link: https://github.com/johnsonadam187gmail/basic_chat_agent.git
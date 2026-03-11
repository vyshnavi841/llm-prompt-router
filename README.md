# LLM Prompt Router

This project implements an intent-based prompt router using OpenAI models.

The system first classifies user intent and then routes the request to a specialized AI persona.

Supported intents:

- code
- data
- writing
- career
- unclear

The architecture follows a two-stage pipeline:

1. Intent Classification
2. Expert Persona Response

---

## Features

- Intent classification using an LLM
- Expert persona system prompts
- JSON structured responses
- Error handling for malformed JSON
- JSONL logging
- Docker containerization

---

## Project Structure

app/
 main.py
 router.py
 prompts.py
 logger.py

route_log.jsonl
Dockerfile
docker-compose.yml
.env.example

---

## Setup

Clone the repository:

git clone <repo_url>

cd llm-prompt-router

Create environment variables:

cp .env.example .env

Add your OpenAI API key.

---

## Run using Docker

docker-compose up --build

---

## Example Usage

User: how do i sort a list in python?

Detected Intent:
{
 "intent": "code",
 "confidence": 0.92
}

Assistant:
Use the built-in sorted() function.

---

## Logging

Every request is logged in:

route_log.jsonl

Each entry contains:

- intent
- confidence
- user_message
- final_response

---

## Testing

Example test inputs:

how do i sort a list in python?
what is the average of numbers 10,20,30?
help me improve this paragraph
I'm preparing for a job interview
hey
fix this bug pls
what is a pivot table
rewrite this sentence professionally
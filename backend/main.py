import os
import json
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

from backend.vector_store import search_knowledge
from evaluation.metrics import calculate_metrics


load_dotenv()


app = FastAPI(
    title="AI Support Intelligence"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


MODEL_NAME = "openai/gpt-oss-20b"


def generate_with_retry(prompt, attempts=3):

    for attempt in range(attempts):

        try:

            start_time = time.perf_counter()

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            end_time = time.perf_counter()

            metrics = calculate_metrics(
                response,
                start_time,
                end_time
            )

            return response, metrics

        except Exception as error:

            if attempt == attempts - 1:
                raise error

            print(
                f"Groq temporarily unavailable. "
                f"Retrying in 5 seconds... "
                f"({attempt + 1}/{attempts})"
            )

            time.sleep(5)


@app.get("/")
def home():

    return {
        "message": "AI Support Intelligence API is running"
    }


@app.get("/ask")
def ask_ai():

    response, metrics = generate_with_retry(
        "Explain prompt engineering in one sentence."
    )

    return {
        "response":
        response.choices[0].message.content,
        "metrics": metrics
    }


@app.post("/analyze")
def analyze_ticket(message: str):

    prompt = f"""
Analyze this customer support complaint.

Complaint:
{message}

Return ONLY valid JSON in exactly this format:

{{
  "category": "...",
  "priority": "...",
  "sentiment": "...",
  "summary": "..."
}}
"""

    response, metrics = generate_with_retry(prompt)

    content = response.choices[0].message.content

    analysis = json.loads(content)

    return {
        "complaint": message,
        "analysis": analysis,
        "metrics": metrics
    }


@app.post("/generate-response")
def generate_response(message: str):

    knowledge = search_knowledge(
        message,
        top_k=3
    )

    context = "\n\n".join(knowledge)

    prompt = f"""
You are a professional customer support agent.

Use ONLY the company knowledge provided below to answer
the customer's complaint.

COMPANY KNOWLEDGE:

{context}

CUSTOMER COMPLAINT:

{message}

Rules:

- Acknowledge the customer's issue.
- Show empathy.
- Use the company knowledge to provide accurate guidance.
- Do not invent company policies, refund timelines,
  or transaction statuses.
- Do not make promises that are not supported by the
  company knowledge.
- If information is missing, ask for the minimum
  information needed.
- Never ask for passwords, OTPs, CVV numbers,
  or full card numbers.
- Keep the response under 150 words.
"""

    response, metrics = generate_with_retry(
        prompt
    )

    return {
        "complaint": message,
        "retrieved_knowledge": knowledge,
        "support_response":
        response.choices[0].message.content,
        "metrics": metrics
    }
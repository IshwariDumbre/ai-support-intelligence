import os
import json
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


complaint = """
My payment was deducted but my order was cancelled.
I have not received my refund and it has been 5 days.
"""


PROMPT_V1 = f"""
Write a response to this customer complaint:

{complaint}

Be polite and helpful.
"""


PROMPT_V2 = f"""
You are a professional customer support agent.

Respond to the following customer complaint:

{complaint}

Requirements:
- Acknowledge the customer's problem.
- Show empathy.
- Clearly explain what information is needed next.
- Do not invent company policies or refund timelines.
- Do not make promises you cannot guarantee.
- Keep the response concise and professional.
"""


def generate_response(prompt):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except Exception as error:
            if attempt == 2:
                raise error

            print(f"Gemini temporarily unavailable. Retrying... ({attempt + 1}/3)")
            time.sleep(5)


def evaluate_response(response):
    evaluation_prompt = f"""
You are evaluating an AI-generated customer support response.

Customer complaint:
{complaint}

AI response:
{response}

Score the response from 1 to 5 for each category:

1. Relevance
2. Helpfulness
3. Empathy
4. Accuracy
5. Safety

Important:
- Penalize the response if it invents policies, refund timelines,
  guarantees, or facts that were not provided.
- Return ONLY valid JSON.

Format:
{{
    "relevance": 0,
    "helpfulness": 0,
    "empathy": 0,
    "accuracy": 0,
    "safety": 0,
    "overall_score": 0,
    "reason": "..."
}}
"""

    for attempt in range(3):
        try:
            result = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=evaluation_prompt
            )

            return json.loads(result.text)

        except Exception as error:
            if attempt == 2:
                raise error

            print(f"Gemini evaluation temporarily unavailable. Retrying... ({attempt + 1}/3)")
            time.sleep(5)


response_v1 = generate_response(PROMPT_V1)
response_v2 = generate_response(PROMPT_V2)

evaluation_v1 = evaluate_response(response_v1)
evaluation_v2 = evaluate_response(response_v2)


print("\n========== PROMPT V1 ==========")
print(response_v1)

print("\n========== V1 EVALUATION ==========")
print(json.dumps(evaluation_v1, indent=2))

print("\n========== PROMPT V2 ==========")
print(response_v2)

print("\n========== V2 EVALUATION ==========")
print(json.dumps(evaluation_v2, indent=2))
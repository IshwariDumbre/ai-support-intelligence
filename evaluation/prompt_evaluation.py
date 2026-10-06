import os

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
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text


response_v1 = generate_response(PROMPT_V1)
response_v2 = generate_response(PROMPT_V2)


print("\n========== PROMPT V1 ==========\n")
print(response_v1)

print("\n========== PROMPT V2 ==========\n")
print(response_v2)
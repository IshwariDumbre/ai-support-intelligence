import os

from dotenv import load_dotenv
from groq import Groq

from evaluation.metrics import measure_generation

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "openai/gpt-oss-20b"


prompt = """
Write a short professional customer support response
to this complaint:

My order was cancelled but I was charged.
"""


response, metrics = measure_generation(
    client,
    MODEL_NAME,
    prompt
)


print("\n========== AI RESPONSE ==========")
print(response.choices[0].message.content)

print("\n========== PERFORMANCE METRICS ==========")

for key, value in metrics.items():
    print(f"{key}: {value}")